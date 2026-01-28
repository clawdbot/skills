#!/usr/bin/env bash
set -euo pipefail

# SerpAPI Search Script
# Usage: search.sh <query> [options]
#
# Engines: google (default), google_news, google_local
# Options: --engine, --country, --lang, --location, --num, --json, --api-key

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ENGINE="google"
COUNTRY="us"
LANG="en"
LOCATION=""
NUM=10
RAW_JSON=false
API_KEY="${SERPAPI_API_KEY:-}"
QUERY=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --engine)   ENGINE="$2"; shift 2 ;;
    --country)  COUNTRY="$2"; shift 2 ;;
    --lang)     LANG="$2"; shift 2 ;;
    --location) LOCATION="$2"; shift 2 ;;
    --num)      NUM="$2"; shift 2 ;;
    --json)     RAW_JSON=true; shift ;;
    --api-key)  API_KEY="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: search.sh <query> [--engine google|google_news|google_local] [--country br] [--lang pt] [--location 'São Paulo'] [--num 10] [--json]"
      exit 0
      ;;
    *) QUERY="${QUERY:+$QUERY }$1"; shift ;;
  esac
done

if [[ -z "$QUERY" ]]; then
  echo "Error: query is required" >&2
  exit 1
fi

# Resolve API key
if [[ -z "$API_KEY" ]]; then
  SKILL_ENV="$(dirname "$SCRIPT_DIR")/.env"
  [[ -f "$SKILL_ENV" ]] && API_KEY=$(grep -E "^SERPAPI_API_KEY=" "$SKILL_ENV" 2>/dev/null | cut -d= -f2- || true)
  [[ -z "$API_KEY" && -f "$HOME/.config/serpapi/api_key" ]] && API_KEY=$(cat "$HOME/.config/serpapi/api_key")
fi

if [[ -z "$API_KEY" ]]; then
  echo "Error: No API key. Set SERPAPI_API_KEY or create ~/.config/serpapi/api_key" >&2
  exit 1
fi

# URL-encode
urlencode() { python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$1"; }

Q=$(urlencode "$QUERY")

# Build params
case "$ENGINE" in
  google)       PARAMS="engine=google&q=${Q}&api_key=${API_KEY}&gl=${COUNTRY}&hl=${LANG}&num=${NUM}" ;;
  google_news)  PARAMS="engine=google_news&q=${Q}&api_key=${API_KEY}&gl=${COUNTRY}&hl=${LANG}" ;;
  google_local) PARAMS="engine=google_local&q=${Q}&api_key=${API_KEY}&gl=${COUNTRY}&hl=${LANG}" ;;
  *) echo "Error: unknown engine '$ENGINE'" >&2; exit 1 ;;
esac

[[ -n "$LOCATION" ]] && PARAMS="${PARAMS}&location=$(urlencode "$LOCATION")"

# Fetch
TMPFILE=$(mktemp)
trap "rm -f $TMPFILE" EXIT
curl -s "https://serpapi.com/search.json?${PARAMS}" > "$TMPFILE"

# Check error
ERROR=$(python3 -c "import json;d=json.load(open('$TMPFILE'));print(d.get('error',''))" 2>/dev/null || echo "")
if [[ -n "$ERROR" ]]; then
  echo "SerpAPI Error: $ERROR" >&2
  exit 1
fi

if [[ "$RAW_JSON" == true ]]; then
  cat "$TMPFILE"
  exit 0
fi

# Format
python3 "$SCRIPT_DIR/format.py" "$TMPFILE" "$ENGINE"
