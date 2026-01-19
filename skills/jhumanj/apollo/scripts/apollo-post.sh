#!/bin/bash
set -euo pipefail

# Usage: apollo-post.sh "/api/v1/path" '{...json...}'
# Auth: send API key via X-Api-Key header.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/apollo-config.sh"

PATH_PART="${1:-}"
JSON_BODY="${2:-}"

if [ -z "$PATH_PART" ] || [ -z "$JSON_BODY" ]; then
  echo "Usage: apollo-post.sh \"/api/v1/path\" '{...json...}'" >&2
  exit 1
fi

URL="$APOLLO_BASE_URL$PATH_PART"

curl -sS -X POST "$URL" \
  -H "X-Api-Key: $APOLLO_API_KEY" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  --data "$JSON_BODY"
