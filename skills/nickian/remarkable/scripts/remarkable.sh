#!/bin/bash
# reMarkable Cloud CLI wrapper
# Uses rmapi for cloud access + article2ebook for URL conversion
#
# Usage:
#   remarkable.sh ls [PATH]
#   remarkable.sh upload --file PATH [--dir PATH]
#   remarkable.sh send-article --url URL [--format epub|pdf] [--dir PATH] [--title TITLE]
#   remarkable.sh mkdir --path PATH
#   remarkable.sh find --name TEXT

set -e

RMAPI="${RMAPI_BIN:-rmapi}"

# Check rmapi is available
if ! command -v "$RMAPI" &>/dev/null; then
  echo "Error: rmapi not found. Install from https://github.com/ddvk/rmapi" >&2
  exit 1
fi

# --- Commands ---

cmd_ls() {
  local DIR="${1:-/}"
  $RMAPI ls "$DIR"
}

cmd_upload() {
  local FILE_PATH="" DIR="/"
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --file) FILE_PATH="$2"; shift 2 ;;
      --dir) DIR="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  if [ -z "$FILE_PATH" ]; then
    echo "Error: --file is required" >&2; exit 1
  fi
  if [ ! -f "$FILE_PATH" ]; then
    echo "Error: File not found: $FILE_PATH" >&2; exit 1
  fi

  $RMAPI put --coverpage=0 "$FILE_PATH" "$DIR"
  echo "Uploaded: $(basename "$FILE_PATH") → $DIR"
}

cmd_send_article() {
  local URL="" FORMAT="epub" DIR="/" TITLE=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --url) URL="$2"; shift 2 ;;
      --format) FORMAT="$2"; shift 2 ;;
      --dir) DIR="$2"; shift 2 ;;
      --title) TITLE="$2"; shift 2 ;;
      *) URL="${URL:-$1}"; shift ;;
    esac
  done

  if [ -z "$URL" ]; then
    echo "Error: URL is required" >&2; exit 1
  fi

  # Use local article2ebook.py
  local SCRIPT_DIR
  SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
  local CONVERTER="$SCRIPT_DIR/article2ebook.py"

  if [ ! -f "$CONVERTER" ]; then
    echo "Error: article2ebook.py not found" >&2; exit 1
  fi

  # Convert article
  local EXTRA_ARGS=""
  if [ -n "$TITLE" ]; then
    EXTRA_ARGS="--title \"$TITLE\""
  fi

  local OUTPUT_FILE
  OUTPUT_FILE=$(python3 "$CONVERTER" "$URL" --format "$FORMAT" $EXTRA_ARGS 2>&1 | tee /dev/stderr | tail -1)

  if [ ! -f "$OUTPUT_FILE" ]; then
    echo "Error: Failed to create ebook file" >&2
    exit 1
  fi

  echo "Uploading to reMarkable..." >&2
  $RMAPI put --coverpage=0 "$OUTPUT_FILE" "$DIR"
  echo "Sent: $(basename "$OUTPUT_FILE") → $DIR"

  # Cleanup
  rm -f "$OUTPUT_FILE"
}

cmd_mkdir() {
  local DIR_PATH=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --path) DIR_PATH="$2"; shift 2 ;;
      *) DIR_PATH="${DIR_PATH:-$1}"; shift ;;
    esac
  done

  if [ -z "$DIR_PATH" ]; then
    echo "Error: --path is required" >&2; exit 1
  fi

  $RMAPI mkdir "$DIR_PATH"
  echo "Created: $DIR_PATH"
}

cmd_find() {
  local NAME=""
  while [[ $# -gt 0 ]]; do
    case "$1" in
      --name) NAME="$2"; shift 2 ;;
      *) NAME="${NAME:-$1}"; shift ;;
    esac
  done

  if [ -z "$NAME" ]; then
    echo "Error: --name is required" >&2; exit 1
  fi

  $RMAPI find "$NAME"
}

# --- Main ---
COMMAND="${1:-ls}"
shift 2>/dev/null || true

case "$COMMAND" in
  ls|list) cmd_ls "$@" ;;
  upload|put) cmd_upload "$@" ;;
  send-article|article) cmd_send_article "$@" ;;
  mkdir) cmd_mkdir "$@" ;;
  find) cmd_find "$@" ;;
  *)
    echo "Usage: $0 {ls|upload|send-article|mkdir|find}" >&2
    exit 1
    ;;
esac
