#!/bin/bash
# NocoDB CLI - Access bases, tables, columns, and rows
#
# Requires:
#   NOCODB_URL - NocoDB instance URL (e.g., https://nocodb.example.com)
#   NOCODB_TOKEN - NocoDB API token
#
# Usage:
#   nocodb.sh bases
#   nocodb.sh tables --base ID|NAME
#   nocodb.sh columns --base ID|NAME --table ID|NAME
#   nocodb.sh rows --base ID|NAME --table ID|NAME [--limit N] [--offset N] [--sort FIELD] [--where FILTER]
#   nocodb.sh insert --base ID|NAME --table ID|NAME --json '{"Field":"Value"}'
#   nocodb.sh row --base ID|NAME --table ID|NAME --id ROW_ID

set -e

if [ -z "$NOCODB_URL" ] || [ -z "$NOCODB_TOKEN" ]; then
  echo "Error: NOCODB_URL and NOCODB_TOKEN must be set" >&2
  exit 1
fi

AUTH="xc-token: ${NOCODB_TOKEN}"

api_get() {
  curl -s -H "$AUTH" "${NOCODB_URL}/$1"
}

api_post() {
  curl -s -X POST -H "$AUTH" -H "Content-Type: application/json" "${NOCODB_URL}/$1" -d "$2"
}

# Cache bases list for name resolution
_bases_cache=""
get_bases() {
  if [ -z "$_bases_cache" ]; then
    _bases_cache=$(api_get "api/v2/meta/bases" | jq -c '.list')
  fi
  echo "$_bases_cache"
}

resolve_base() {
  local INPUT="$1"
  # If it looks like an ID (starts with p), use directly
  if [[ "$INPUT" =~ ^p[a-z0-9]+$ ]]; then
    echo "$INPUT"
    return
  fi
  # Otherwise resolve by name (case-insensitive)
  local ID
  ID=$(get_bases | jq -r --arg name "$INPUT" '.[] | select(.title | ascii_downcase == ($name | ascii_downcase)) | .id' | head -1)
  if [ -z "$ID" ]; then
    echo "Error: Base '$INPUT' not found" >&2
    exit 1
  fi
  echo "$ID"
}

_tables_cache=""
get_tables() {
  local BASE_ID="$1"
  if [ -z "$_tables_cache" ]; then
    _tables_cache=$(api_get "api/v2/meta/bases/${BASE_ID}/tables" | jq -c '.list')
  fi
  echo "$_tables_cache"
}

resolve_table() {
  local BASE_ID="$1"
  local INPUT="$2"
  # If it looks like an ID (starts with m), use directly
  if [[ "$INPUT" =~ ^m[a-z0-9]+$ ]]; then
    echo "$INPUT"
    return
  fi
  local ID
  ID=$(get_tables "$BASE_ID" | jq -r --arg name "$INPUT" '.[] | select(.title | ascii_downcase == ($name | ascii_downcase)) | .id' | head -1)
  if [ -z "$ID" ]; then
    echo "Error: Table '$INPUT' not found in base" >&2
    exit 1
  fi
  echo "$ID"
}

# --- Commands ---

cmd_bases() {
  api_get "api/v2/meta/bases" | jq -r '.list[] | "\(.title) (id: \(.id))"'
}

cmd_tables() {
  local BASE=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --base) BASE="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  if [ -z "$BASE" ]; then
    echo "Error: --base is required" >&2; exit 1
  fi
  local BASE_ID
  BASE_ID=$(resolve_base "$BASE")
  api_get "api/v2/meta/bases/${BASE_ID}/tables" | jq -r '.list[] | "\(.title) (id: \(.id))"'
}

cmd_columns() {
  local BASE="" TABLE=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --base) BASE="$2"; shift 2 ;;
      --table) TABLE="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  if [ -z "$BASE" ] || [ -z "$TABLE" ]; then
    echo "Error: --base and --table are required" >&2; exit 1
  fi
  local BASE_ID TABLE_ID
  BASE_ID=$(resolve_base "$BASE")
  TABLE_ID=$(resolve_table "$BASE_ID" "$TABLE")
  api_get "api/v2/meta/tables/${TABLE_ID}" | jq -r '.columns[] | "\(.title) (\(.uidt)) [id: \(.id)]"'
}

cmd_rows() {
  local BASE="" TABLE="" LIMIT=25 OFFSET=0 SORT="" WHERE=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --base) BASE="$2"; shift 2 ;;
      --table) TABLE="$2"; shift 2 ;;
      --limit) LIMIT="$2"; shift 2 ;;
      --offset) OFFSET="$2"; shift 2 ;;
      --sort) SORT="$2"; shift 2 ;;
      --where) WHERE="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  if [ -z "$BASE" ] || [ -z "$TABLE" ]; then
    echo "Error: --base and --table are required" >&2; exit 1
  fi
  local BASE_ID TABLE_ID
  BASE_ID=$(resolve_base "$BASE")
  TABLE_ID=$(resolve_table "$BASE_ID" "$TABLE")

  local URL="api/v1/db/data/noco/${BASE_ID}/${TABLE_ID}?limit=${LIMIT}&offset=${OFFSET}"
  if [ -n "$SORT" ]; then
    URL="${URL}&sort=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$SORT'))")"
  fi
  if [ -n "$WHERE" ]; then
    URL="${URL}&where=$(python3 -c "import urllib.parse; print(urllib.parse.quote('$WHERE'))")"
  fi

  api_get "$URL" | jq '.list'
}

cmd_row() {
  local BASE="" TABLE="" ID=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --base) BASE="$2"; shift 2 ;;
      --table) TABLE="$2"; shift 2 ;;
      --id) ID="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  if [ -z "$BASE" ] || [ -z "$TABLE" ] || [ -z "$ID" ]; then
    echo "Error: --base, --table, and --id are required" >&2; exit 1
  fi
  local BASE_ID TABLE_ID
  BASE_ID=$(resolve_base "$BASE")
  TABLE_ID=$(resolve_table "$BASE_ID" "$TABLE")
  api_get "api/v1/db/data/noco/${BASE_ID}/${TABLE_ID}/${ID}" | jq .
}

cmd_insert() {
  local BASE="" TABLE="" JSON=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --base) BASE="$2"; shift 2 ;;
      --table) TABLE="$2"; shift 2 ;;
      --json) JSON="$2"; shift 2 ;;
      *) shift ;;
    esac
  done
  if [ -z "$BASE" ] || [ -z "$TABLE" ] || [ -z "$JSON" ]; then
    echo "Error: --base, --table, and --json are required" >&2; exit 1
  fi
  local BASE_ID TABLE_ID
  BASE_ID=$(resolve_base "$BASE")
  TABLE_ID=$(resolve_table "$BASE_ID" "$TABLE")
  local RESPONSE
  RESPONSE=$(api_post "api/v1/db/data/noco/${BASE_ID}/${TABLE_ID}" "$JSON")
  if echo "$RESPONSE" | jq -e '.Id' > /dev/null 2>&1; then
    echo "Inserted row (Id: $(echo "$RESPONSE" | jq -r '.Id'))"
    echo "$RESPONSE" | jq .
  else
    echo "Error inserting row:" >&2
    echo "$RESPONSE" >&2
    exit 1
  fi
}

# --- Main ---
COMMAND="${1:-bases}"
shift 2>/dev/null || true

case "$COMMAND" in
  bases) cmd_bases ;;
  tables) cmd_tables "$@" ;;
  columns|cols) cmd_columns "$@" ;;
  rows|data) cmd_rows "$@" ;;
  row|get) cmd_row "$@" ;;
  insert|add) cmd_insert "$@" ;;
  *)
    echo "Usage: $0 {bases|tables|columns|rows|row|insert}" >&2
    exit 1
    ;;
esac
