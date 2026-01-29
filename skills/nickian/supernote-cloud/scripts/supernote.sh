#!/bin/bash
# Supernote Private Cloud CLI
# Reverse-engineered API client for file listing, upload, and storage info
#
# Requires:
#   SUPERNOTE_URL      - Cloud server URL (e.g., http://192.168.50.168:8080)
#   SUPERNOTE_USER     - Account email
#   SUPERNOTE_PASSWORD - Account password
#
# Usage:
#   supernote.sh login
#   supernote.sh ls [--dir ID] [--path PATH]
#   supernote.sh tree [--depth N]
#   supernote.sh find-dir --path PATH
#   supernote.sh upload --file PATH [--dir ID] [--dir-path PATH] [--name NAME]
#   supernote.sh capacity

set -e

if [ -z "$SUPERNOTE_URL" ] || [ -z "$SUPERNOTE_USER" ] || [ -z "$SUPERNOTE_PASSWORD" ]; then
  echo "Error: SUPERNOTE_URL, SUPERNOTE_USER, and SUPERNOTE_PASSWORD must be set" >&2
  exit 1
fi

BASE_URL="${SUPERNOTE_URL%/}"
TOKEN_FILE="/tmp/.supernote_token"

# --- Auth helpers ---

get_token() {
  # Check cached token
  if [ -f "$TOKEN_FILE" ]; then
    local TOKEN
    TOKEN=$(cat "$TOKEN_FILE")
    if is_token_valid "$TOKEN"; then
      echo "$TOKEN"
      return
    fi
  fi
  # Login fresh
  do_login
  cat "$TOKEN_FILE"
}

is_token_valid() {
  local TOKEN="$1"
  if [ -z "$TOKEN" ]; then return 1; fi
  python3 -c "
import base64, json, time, sys
parts = '$TOKEN'.split('.')
if len(parts) != 3:
    sys.exit(1)
b64 = parts[1] + '=' * (4 - len(parts[1]) % 4)
try:
    data = json.loads(base64.urlsafe_b64decode(b64))
    if data.get('exp', 0) > time.time() + 3600:
        sys.exit(0)
    else:
        sys.exit(1)
except:
    sys.exit(1)
" 2>/dev/null
}

do_login() {
  # Step 1: Get random code
  local RANDOM_RESP
  RANDOM_RESP=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -H "withCredentials: true" \
    "$BASE_URL/api/official/user/query/random/code" \
    -d "{\"countryCode\":null,\"account\":\"$SUPERNOTE_USER\"}")

  local RANDOM_CODE TIMESTAMP
  RANDOM_CODE=$(echo "$RANDOM_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['randomCode'])")
  TIMESTAMP=$(echo "$RANDOM_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d['timestamp'])")

  # Step 2: Hash password: SHA256(MD5(password) + randomCode)
  local HASHED_PASS
  HASHED_PASS=$(python3 -c "
import hashlib
md5 = hashlib.md5('$SUPERNOTE_PASSWORD'.encode()).hexdigest()
print(hashlib.sha256((md5 + '$RANDOM_CODE').encode()).hexdigest())
")

  # Step 3: Login
  local LOGIN_RESP
  LOGIN_RESP=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -H "withCredentials: true" \
    "$BASE_URL/api/official/user/account/login/new" \
    -d "{\"countryCode\":null,\"account\":\"$SUPERNOTE_USER\",\"password\":\"$HASHED_PASS\",\"browser\":\"CLI-Client\",\"equipment\":\"1\",\"loginMethod\":\"1\",\"timestamp\":$TIMESTAMP,\"language\":\"en\"}")

  local TOKEN
  TOKEN=$(echo "$LOGIN_RESP" | python3 -c "import sys,json; d=json.load(sys.stdin); print(d.get('token',''))" 2>/dev/null)

  if [ -z "$TOKEN" ]; then
    echo "Login failed: $LOGIN_RESP" >&2
    exit 1
  fi

  echo "$TOKEN" > "$TOKEN_FILE"
  chmod 600 "$TOKEN_FILE"
}

api_post() {
  local ENDPOINT="$1"
  local DATA="$2"
  local TOKEN
  TOKEN=$(get_token)
  curl -s -X POST \
    -H "Content-Type: application/json" \
    -H "x-access-token: $TOKEN" \
    -H "withCredentials: true" \
    "$BASE_URL$ENDPOINT" \
    -d "$DATA"
}

# --- Commands ---

cmd_login() {
  do_login
  local TOKEN
  TOKEN=$(cat "$TOKEN_FILE")
  local USER_ID
  USER_ID=$(echo "$TOKEN" | cut -d. -f2 | python3 -c "
import sys, base64, json
b64 = sys.stdin.read().strip()
b64 += '=' * (4 - len(b64) % 4)
data = json.loads(base64.urlsafe_b64decode(b64))
print(data.get('userId', 'unknown'))
")
  echo "Logged in successfully. User ID: $USER_ID"
}

cmd_ls() {
  local DIR_ID="0"
  local DIR_PATH=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --dir) DIR_ID="$2"; shift 2 ;;
      --path) DIR_PATH="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  # Resolve path to ID if given
  if [ -n "$DIR_PATH" ]; then
    DIR_ID=$(resolve_path "$DIR_PATH")
    if [ -z "$DIR_ID" ] || [ "$DIR_ID" = "null" ]; then
      echo "Error: Directory '$DIR_PATH' not found" >&2
      exit 1
    fi
  fi

  local RESP
  RESP=$(api_post "/api/file/list/query" "{\"directoryId\":\"$DIR_ID\",\"pageNo\":1,\"pageSize\":100,\"order\":\"time\",\"sequence\":\"desc\"}")

  echo "$RESP" | python3 -c "
import sys, json
data = json.load(sys.stdin)
items = data.get('userFileVOList', data.get('data', {}).get('userFileVOList', []))
if not items:
    print('(empty directory)')
else:
    for item in items:
        icon = '📁' if item.get('isFolder') == 'Y' else '📄'
        name = item.get('fileName', '?')
        fid = item.get('id', '?')
        size = item.get('size', 0)
        if item.get('isFolder') == 'Y':
            print(f'{icon} {name}  (id: {fid})')
        else:
            sz = f'{size:,}' if size else '?'
            print(f'{icon} {name}  ({sz} bytes, id: {fid})')
"
}

resolve_path() {
  local PATH_STR="$1"
  local CURRENT_ID="0"

  # Split on /
  IFS='/' read -ra PARTS <<< "$PATH_STR"
  for PART in "${PARTS[@]}"; do
    [ -z "$PART" ] && continue
    local RESP
    RESP=$(api_post "/api/file/list/query" "{\"directoryId\":\"$CURRENT_ID\",\"pageNo\":1,\"pageSize\":100,\"order\":\"time\",\"sequence\":\"desc\"}")
    local FOUND_ID
    FOUND_ID=$(echo "$RESP" | python3 -c "
import sys, json
data = json.load(sys.stdin)
target = '$PART'
for item in data.get('userFileVOList', data.get('data', {}).get('userFileVOList', [])):
    if item.get('fileName') == target and item.get('isFolder') == 'Y':
        print(item['id'])
        break
" 2>/dev/null)
    if [ -z "$FOUND_ID" ]; then
      echo ""
      return
    fi
    CURRENT_ID="$FOUND_ID"
  done
  echo "$CURRENT_ID"
}

cmd_find_dir() {
  local DIR_PATH=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --path) DIR_PATH="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  if [ -z "$DIR_PATH" ]; then
    echo "Error: --path is required" >&2; exit 1
  fi
  local DIR_ID
  DIR_ID=$(resolve_path "$DIR_PATH")
  if [ -z "$DIR_ID" ] || [ "$DIR_ID" = "null" ]; then
    echo "Directory '$DIR_PATH' not found" >&2
    exit 1
  fi
  echo "$DIR_ID"
}

cmd_tree() {
  local MAX_DEPTH=2
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --depth) MAX_DEPTH="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  print_tree "0" "" 0 "$MAX_DEPTH"
}

print_tree() {
  local DIR_ID="$1"
  local PREFIX="$2"
  local DEPTH="$3"
  local MAX_DEPTH="$4"

  if [ "$DEPTH" -ge "$MAX_DEPTH" ]; then return; fi

  local RESP
  RESP=$(api_post "/api/file/list/query" "{\"directoryId\":\"$DIR_ID\",\"pageNo\":1,\"pageSize\":100,\"order\":\"time\",\"sequence\":\"desc\"}")

  echo "$RESP" | python3 -c "
import sys, json
data = json.load(sys.stdin)
items = data.get('userFileVOList', data.get('data', {}).get('userFileVOList', []))
for item in items:
    icon = '📁' if item.get('isFolder') == 'Y' else '📄'
    name = item.get('fileName', '?')
    fid = item.get('id', '?')
    is_folder = item.get('isFolder') == 'Y'
    print(f'ITEM|{is_folder}|{fid}|${PREFIX}{icon} {name}')
" 2>/dev/null | while IFS='|' read -r _ IS_FOLDER FID LINE; do
    echo "$LINE"
    if [ "$IS_FOLDER" = "True" ] && [ "$((DEPTH + 1))" -lt "$MAX_DEPTH" ]; then
      print_tree "$FID" "${PREFIX}  " "$((DEPTH + 1))" "$MAX_DEPTH"
    fi
  done
}

cmd_upload() {
  local FILE_PATH="" DIR_ID="" DIR_PATH="" REMOTE_NAME=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --file) FILE_PATH="$2"; shift 2 ;;
      --dir) DIR_ID="$2"; shift 2 ;;
      --dir-path) DIR_PATH="$2"; shift 2 ;;
      --name) REMOTE_NAME="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  if [ -z "$FILE_PATH" ]; then
    echo "Error: --file is required" >&2; exit 1
  fi
  if [ ! -f "$FILE_PATH" ]; then
    echo "Error: File not found: $FILE_PATH" >&2; exit 1
  fi

  # Resolve dir
  if [ -n "$DIR_PATH" ]; then
    DIR_ID=$(resolve_path "$DIR_PATH")
    if [ -z "$DIR_ID" ] || [ "$DIR_ID" = "null" ]; then
      echo "Error: Directory '$DIR_PATH' not found" >&2; exit 1
    fi
  fi
  if [ -z "$DIR_ID" ]; then
    echo "Error: --dir or --dir-path is required" >&2; exit 1
  fi

  local FILE_NAME="${REMOTE_NAME:-$(basename "$FILE_PATH")}"
  local FILE_SIZE
  FILE_SIZE=$(stat -f%z "$FILE_PATH" 2>/dev/null || stat -c%s "$FILE_PATH" 2>/dev/null)
  local FILE_MD5
  FILE_MD5=$(python3 -c "import hashlib; print(hashlib.md5(open('$FILE_PATH','rb').read()).hexdigest())")

  local TOKEN
  TOKEN=$(get_token)
  local TIMESTAMP
  TIMESTAMP=$(python3 -c "import time; print(int(time.time()*1000))")
  local NONCE
  NONCE=$(python3 -c "import random,time; print(str(random.randint(0,9999999999)).zfill(10) + str(int(time.time()*1000)))")

  # Step 1: Apply for upload
  local APPLY_RESP
  APPLY_RESP=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -H "x-access-token: $TOKEN" \
    -H "withCredentials: true" \
    -H "timestamp: $TIMESTAMP" \
    -H "nonce: $NONCE" \
    "$BASE_URL/api/file/upload/apply" \
    -d "{\"size\":$FILE_SIZE,\"fileName\":\"$FILE_NAME\",\"directoryId\":\"$DIR_ID\",\"md5\":\"$FILE_MD5\"}")

  local UPLOAD_URL INNER_NAME
  UPLOAD_URL=$(echo "$APPLY_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('fullUploadUrl',''))" 2>/dev/null)
  INNER_NAME=$(echo "$APPLY_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('innerName',''))" 2>/dev/null)

  if [ -z "$UPLOAD_URL" ]; then
    echo "Upload apply failed: $APPLY_RESP" >&2
    exit 1
  fi

  # Step 2: Upload to OSS
  local OSS_RESP
  OSS_RESP=$(curl -s -X POST \
    -H "x-access-token: $TOKEN" \
    -F "file=@$FILE_PATH" \
    "$UPLOAD_URL")

  # Step 3: Finish upload
  local FINISH_RESP
  FINISH_RESP=$(curl -s -X POST \
    -H "Content-Type: application/json" \
    -H "x-access-token: $TOKEN" \
    -H "withCredentials: true" \
    "$BASE_URL/api/file/upload/finish" \
    -d "{\"directoryId\":\"$DIR_ID\",\"fileName\":\"$FILE_NAME\",\"fileSize\":$FILE_SIZE,\"innerName\":\"$INNER_NAME\",\"md5\":\"$FILE_MD5\"}")

  local SUCCESS
  SUCCESS=$(echo "$FINISH_RESP" | python3 -c "import sys,json; print(json.load(sys.stdin).get('success', False))" 2>/dev/null)

  if [ "$SUCCESS" = "True" ]; then
    echo "Uploaded: $FILE_NAME ($FILE_SIZE bytes) → directory $DIR_ID"
  else
    echo "Upload may have failed. Finish response: $FINISH_RESP" >&2
    exit 1
  fi
}

cmd_capacity() {
  local RESP
  RESP=$(api_post "/api/file/capacity/query" "{}")
  echo "$RESP" | python3 -c "
import sys, json
data = json.load(sys.stdin)
d = data.get('data', data)
if isinstance(d, dict):
    for k, v in d.items():
        if isinstance(v, (int, float)) and v > 1000000:
            mb = v / (1024*1024)
            print(f'{k}: {mb:.1f} MB')
        else:
            print(f'{k}: {v}')
else:
    print(json.dumps(data, indent=2))
"
}

cmd_send_article() {
  local URL="" FORMAT="epub" DIR_PATH="Document" DIR_ID="" TITLE=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --url) URL="$2"; shift 2 ;;
      --format) FORMAT="$2"; shift 2 ;;
      --dir-path) DIR_PATH="$2"; shift 2 ;;
      --dir) DIR_ID="$2"; shift 2 ;;
      --title) TITLE="$2"; shift 2 ;;
      *) URL="${URL:-$1}"; shift ;;
    esac
  done

  if [ -z "$URL" ]; then
    echo "Error: URL is required" >&2; exit 1
  fi

  local SCRIPT_DIR
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

  # Convert article
  local EXTRA_ARGS=""
  if [ -n "$TITLE" ]; then
    EXTRA_ARGS="--title \"$TITLE\""
  fi

  local OUTPUT_FILE
  OUTPUT_FILE=$(python3 "$SCRIPT_DIR/article2ebook.py" "$URL" --format "$FORMAT" $EXTRA_ARGS 2>&1 | tee /dev/stderr | tail -1)

  if [ ! -f "$OUTPUT_FILE" ]; then
    echo "Error: Failed to create ebook file" >&2
    exit 1
  fi

  echo "Uploading to Supernote..." >&2

  # Resolve directory
  if [ -z "$DIR_ID" ]; then
    DIR_ID=$(resolve_path "$DIR_PATH")
    if [ -z "$DIR_ID" ] || [ "$DIR_ID" = "null" ]; then
      echo "Error: Directory '$DIR_PATH' not found" >&2; exit 1
    fi
  fi

  # Upload
  cmd_upload --file "$OUTPUT_FILE" --dir "$DIR_ID"

  # Cleanup temp file
  rm -f "$OUTPUT_FILE"
}

# --- Main ---
COMMAND="${1:-ls}"
shift 2>/dev/null || true

case "$COMMAND" in
  login) cmd_login ;;
  ls|list) cmd_ls "$@" ;;
  tree) cmd_tree "$@" ;;
  find-dir) cmd_find_dir "$@" ;;
  upload) cmd_upload "$@" ;;
  capacity|cap) cmd_capacity ;;
  send-article|article) cmd_send_article "$@" ;;
  *)
    echo "Usage: $0 {login|ls|tree|find-dir|upload|capacity|send-article}" >&2
    exit 1
    ;;
esac
