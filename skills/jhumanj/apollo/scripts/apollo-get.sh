#!/bin/bash
set -euo pipefail

# Usage: apollo-get.sh "/api/v1/path" [queryString]
# Auth: sends API key via X-Api-Key header.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"
# shellcheck disable=SC1091
source "$SCRIPT_DIR/apollo-config.sh"

PATH_PART="${1:-}"
QUERY="${2:-}"

if [ -z "$PATH_PART" ]; then
  echo "Usage: apollo-get.sh \"/api/v1/path\" [queryString]" >&2
  exit 1
fi

URL="$APOLLO_BASE_URL$PATH_PART"
if [ -n "$QUERY" ]; then
  URL="$URL?$QUERY"
fi

curl -sS "$URL" \
  -H "X-Api-Key: $APOLLO_API_KEY" \
  -H "Accept: application/json"
