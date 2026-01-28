#!/usr/bin/env bash
set -euo pipefail

# Perplexity Deep Search
# Usage: search.sh [options] "query"

MODE="search"
RECENCY=""
DOMAINS=""
LANG=""
JSON_OUTPUT=false
QUERY=""

usage() {
  echo "Usage: $(basename "$0") [options] \"query\""
  echo ""
  echo "Modes:"
  echo "  --mode search    Quick facts via sonar-pro (default)"
  echo "  --mode reason    Complex analysis via sonar-reasoning-pro"
  echo "  --mode research  Deep reports via sonar-deep-research"
  echo ""
  echo "Options:"
  echo "  --recency hour|day|week|month   Filter by recency"
  echo "  --domains site1.com,site2.com   Restrict to domains"
  echo "  --lang pt|en|es|...             Response language"
  echo "  --json                          Raw JSON output"
  exit 1
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --mode) MODE="$2"; shift 2 ;;
    --recency) RECENCY="$2"; shift 2 ;;
    --domains) DOMAINS="$2"; shift 2 ;;
    --lang) LANG="$2"; shift 2 ;;
    --json) JSON_OUTPUT=true; shift ;;
    --help|-h) usage ;;
    -*) echo "Unknown option: $1"; usage ;;
    *) QUERY="$1"; shift ;;
  esac
done

if [[ -z "$QUERY" ]]; then
  echo "Error: No query provided" >&2
  usage
fi

if [[ -z "${PERPLEXITY_API_KEY:-}" ]]; then
  echo "Error: PERPLEXITY_API_KEY not set" >&2
  exit 1
fi

# Map mode to model
case "$MODE" in
  search)   MODEL="sonar-pro" ;;
  reason)   MODEL="sonar-reasoning-pro" ;;
  research) MODEL="sonar-deep-research" ;;
  *) echo "Error: Invalid mode '$MODE'. Use: search, reason, research" >&2; exit 1 ;;
esac

# Build user content with optional language instruction
USER_CONTENT="$QUERY"
if [[ -n "$LANG" ]]; then
  USER_CONTENT="[Respond in language: $LANG] $QUERY"
fi

# Build JSON payload
PAYLOAD=$(jq -n \
  --arg model "$MODEL" \
  --arg content "$USER_CONTENT" \
  '{
    model: $model,
    messages: [
      { role: "user", content: $content }
    ]
  }')

# Add optional parameters
if [[ -n "$RECENCY" ]]; then
  PAYLOAD=$(echo "$PAYLOAD" | jq --arg r "$RECENCY" '. + { search_recency_filter: $r }')
fi

if [[ -n "$DOMAINS" ]]; then
  # Convert comma-separated to JSON array
  DOMAIN_ARRAY=$(echo "$DOMAINS" | jq -R 'split(",")')
  PAYLOAD=$(echo "$PAYLOAD" | jq --argjson d "$DOMAIN_ARRAY" '. + { search_domain_filter: $d }')
fi

# Make API call
RESPONSE=$(curl -sS "https://api.perplexity.ai/chat/completions" \
  -H "Authorization: Bearer $PERPLEXITY_API_KEY" \
  -H "Content-Type: application/json" \
  -d "$PAYLOAD" 2>&1)

# Check for errors
if echo "$RESPONSE" | jq -e '.error' >/dev/null 2>&1; then
  ERROR_MSG=$(echo "$RESPONSE" | jq -r '.error.message // .error // "Unknown error"')
  echo "Error: $ERROR_MSG" >&2
  exit 1
fi

# Output
if [[ "$JSON_OUTPUT" == true ]]; then
  echo "$RESPONSE" | jq .
  exit 0
fi

# Extract content
CONTENT=$(echo "$RESPONSE" | jq -r '.choices[0].message.content // empty')
if [[ -z "$CONTENT" ]]; then
  echo "Error: No content in response" >&2
  echo "$RESPONSE" | jq . >&2
  exit 1
fi

echo "$CONTENT"

# Extract citations if present
CITATIONS=$(echo "$RESPONSE" | jq -r '.citations[]? // empty' 2>/dev/null)
if [[ -n "$CITATIONS" ]]; then
  echo ""
  echo "---"
  echo "Sources:"
  echo "$CITATIONS" | while IFS= read -r url; do
    echo "  - $url"
  done
fi
