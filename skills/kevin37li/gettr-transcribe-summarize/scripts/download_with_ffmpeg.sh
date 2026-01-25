#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "Usage: download_with_ffmpeg.sh <m3u8_or_mp4_url> <out.mp4>" >&2
  exit 2
fi

IN_URL="$1"
OUT_FILE="$2"

if ! command -v ffmpeg >/dev/null 2>&1; then
  echo "ffmpeg not found. Install with: brew install ffmpeg" >&2
  exit 127
fi

mkdir -p "$(dirname "$OUT_FILE")"

# Try stream copy first (fast, no re-encode). If it fails, fall back to re-encode.
set +e
ffmpeg -y -i "$IN_URL" -c copy -movflags +faststart "$OUT_FILE" 2>/dev/null
STATUS=$?
set -e

if [[ $STATUS -ne 0 ]]; then
  echo "[warn] Stream copy failed; falling back to re-encode (slower)." >&2
  ffmpeg -y -i "$IN_URL" -c:v libx264 -preset veryfast -crf 23 -c:a aac -b:a 128k -movflags +faststart "$OUT_FILE"
fi

echo "$OUT_FILE"
