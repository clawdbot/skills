#!/bin/bash
# FreshRSS CLI - Query headlines from a FreshRSS instance
# Uses Google Reader compatible API
#
# Requires environment variables:
#   FRESHRSS_URL - Your FreshRSS instance URL (e.g., https://freshrss.example.com)
#   FRESHRSS_USER - Your FreshRSS username
#   FRESHRSS_API_PASSWORD - Your FreshRSS API password (set in FreshRSS → Settings → Profile → API)
#
# Usage:
#   freshrss.sh headlines [--count N] [--hours N] [--category NAME] [--unread]
#   freshrss.sh categories
#   freshrss.sh feeds

set -e

# --- Config ---
if [ -z "$FRESHRSS_URL" ] || [ -z "$FRESHRSS_USER" ] || [ -z "$FRESHRSS_API_PASSWORD" ]; then
  echo "Error: Required environment variables not set." >&2
  echo "Set FRESHRSS_URL, FRESHRSS_USER, and FRESHRSS_API_PASSWORD" >&2
  exit 1
fi

API_BASE="${FRESHRSS_URL}/api/greader.php"

# --- Auth ---
auth_login() {
  local RESPONSE
  RESPONSE=$(curl -s "${API_BASE}/accounts/ClientLogin?Email=${FRESHRSS_USER}&Passwd=${FRESHRSS_API_PASSWORD}")
  AUTH_TOKEN=$(echo "$RESPONSE" | grep "Auth=" | cut -d'=' -f2)
  if [ -z "$AUTH_TOKEN" ]; then
    echo "Error: Authentication failed" >&2
    echo "$RESPONSE" >&2
    exit 1
  fi
}

api_get() {
  local ENDPOINT="$1"
  curl -s -H "Authorization:GoogleLogin auth=${AUTH_TOKEN}" "${API_BASE}/reader/api/0/${ENDPOINT}"
}

# --- Commands ---

cmd_categories() {
  auth_login
  api_get "tag/list?output=json" | jq -r '.tags[] | select(.id | contains("/label/")) | .id | split("/label/")[1]'
}

cmd_feeds() {
  auth_login
  api_get "subscription/list?output=json" | jq -r '.subscriptions[] | "\(.title) [\(.categories[0].label // "uncategorized")]"'
}

cmd_headlines() {
  local COUNT=20
  local HOURS=""
  local CATEGORY=""
  local UNREAD_ONLY=false
  local STREAM="reading-list"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --count) COUNT="$2"; shift 2 ;;
      --hours) HOURS="$2"; shift 2 ;;
      --category) CATEGORY="$2"; shift 2 ;;
      --unread) UNREAD_ONLY=true; shift ;;
      *) shift ;;
    esac
  done

  auth_login

  # Build stream URL
  local URL="stream/contents"
  if [ -n "$CATEGORY" ]; then
    URL="${URL}/user/-/label/${CATEGORY}"
  else
    URL="${URL}/user/-/state/com.google/reading-list"
  fi

  URL="${URL}?output=json&n=${COUNT}"

  # Add time filter
  if [ -n "$HOURS" ]; then
    local SINCE
    SINCE=$(date -v-${HOURS}H +%s 2>/dev/null || date -d "${HOURS} hours ago" +%s 2>/dev/null)
    if [ -n "$SINCE" ]; then
      URL="${URL}&ot=${SINCE}"
    fi
  fi

  # Add unread filter
  if [ "$UNREAD_ONLY" = true ]; then
    URL="${URL}&xt=user/-/state/com.google/read"
  fi

  local RESPONSE
  RESPONSE=$(api_get "$URL")

  # Format output
  echo "$RESPONSE" | jq -r '
    .items[] |
    {
      title: .title,
      source: .origin.title,
      url: (.canonical[0].href // .alternate[0].href // ""),
      published: (.published | todate),
      categories: [.categories[] | select(contains("/label/")) | split("/label/")[1]]
    } |
    "[\(.published)] [\(.source)] \(.title)\n  \(.url)\n  Categories: \(.categories | join(", "))\n"
  ' 2>/dev/null || echo "No articles found or error parsing response" >&2
}

# --- Main ---
COMMAND="${1:-headlines}"
shift 2>/dev/null || true

case "$COMMAND" in
  headlines|news|latest) cmd_headlines "$@" ;;
  categories|cats) cmd_categories ;;
  feeds) cmd_feeds ;;
  *)
    echo "Usage: $0 {headlines|categories|feeds}" >&2
    echo "" >&2
    echo "  headlines [--count N] [--hours N] [--category NAME] [--unread]" >&2
    echo "  categories    List all categories" >&2
    echo "  feeds         List all feeds" >&2
    exit 1
    ;;
esac
