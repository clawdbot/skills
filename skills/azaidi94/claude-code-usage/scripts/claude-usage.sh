#!/bin/bash
# Claude Code Usage Checker
# Queries Anthropic OAuth API for Claude Code rate limits

set -euo pipefail

CACHE_FILE="${CACHE_FILE:-/tmp/claude-usage-cache}"
CACHE_TTL="${CACHE_TTL:-60}"  # 1 minute default

# Parse arguments
FORCE_REFRESH=0
FORMAT="text"

while [[ $# -gt 0 ]]; do
  case $1 in
    --fresh|--force)
      FORCE_REFRESH=1
      shift
      ;;
    --json)
      FORMAT="json"
      shift
      ;;
    --cache-ttl)
      CACHE_TTL="$2"
      shift 2
      ;;
    --help|-h)
      cat << 'EOF'
Usage: claude-usage.sh [OPTIONS]

Check Claude Code OAuth usage limits (session & weekly).

Options:
  --fresh, --force    Force refresh (ignore cache)
  --json              Output as JSON
  --cache-ttl SEC     Cache TTL in seconds (default: 60)
  --help, -h          Show this help

Examples:
  claude-usage.sh                    # Use cache if fresh
  claude-usage.sh --fresh            # Force API call
  claude-usage.sh --json             # JSON output
EOF
      exit 0
      ;;
    *)
      echo "Unknown option: $1" >&2
      exit 1
      ;;
  esac
done

# Function to convert seconds to human readable
secs_to_human() {
  local secs=$1
  if [ "$secs" -lt 0 ]; then secs=0; fi
  local days=$((secs / 86400))
  local hours=$(((secs % 86400) / 3600))
  local mins=$(((secs % 3600) / 60))

  if [ "$days" -gt 0 ]; then
    echo "${days}d ${hours}h"
  elif [ "$hours" -gt 0 ]; then
    echo "${hours}h ${mins}m"
  else
    echo "${mins}m"
  fi
}

# Check cache (unless force refresh)
if [ "$FORCE_REFRESH" -eq 0 ] && [ -f "$CACHE_FILE" ]; then
  if [[ "$OSTYPE" == "darwin"* ]]; then
    age=$(($(date +%s) - $(stat -f%m "$CACHE_FILE")))
  else
    age=$(($(date +%s) - $(stat -c%Y "$CACHE_FILE")))
  fi
  
  if [ "$age" -lt "$CACHE_TTL" ]; then
    cat "$CACHE_FILE"
    exit 0
  fi
fi

# Get OAuth token from keychain (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
  CREDS=$(security find-generic-password -s "Claude Code-credentials" -w 2>/dev/null || echo "")
else
  # Linux: check common credential stores
  if command -v secret-tool >/dev/null 2>&1; then
    CREDS=$(secret-tool lookup application "Claude Code" 2>/dev/null || echo "")
  else
    echo "Error: Credential storage not found (macOS keychain or secret-tool required)" >&2
    exit 1
  fi
fi

if [ -z "$CREDS" ]; then
  if [ "$FORMAT" = "json" ]; then
    echo '{"error":"no_credentials","session":null,"weekly":null}'
  else
    echo "❌ No Claude Code credentials found"
  fi
  exit 1
fi

TOKEN=$(echo "$CREDS" | grep -o '"accessToken":"[^"]*"' | sed 's/"accessToken":"//;s/"//')

if [ -z "$TOKEN" ]; then
  if [ "$FORMAT" = "json" ]; then
    echo '{"error":"no_token","session":null,"weekly":null}'
  else
    echo "❌ Could not extract access token"
  fi
  exit 1
fi

# Fetch usage from API
RESP=$(curl -s "https://api.anthropic.com/api/oauth/usage" \
  -H "Authorization: Bearer $TOKEN" \
  -H "anthropic-beta: oauth-2025-04-20" 2>/dev/null)

if [ -z "$RESP" ]; then
  if [ "$FORMAT" = "json" ]; then
    echo '{"error":"api_error","session":null,"weekly":null}'
  else
    echo "❌ API request failed"
  fi
  exit 1
fi

# Parse session (5-hour)
SESSION=$(echo "$RESP" | grep -o '"five_hour":{[^}]*}' | grep -o '"utilization":[0-9]*' | sed 's/.*://')
SESSION_RESET=$(echo "$RESP" | grep -o '"five_hour":{[^}]*}' | grep -o '"resets_at":"[^"]*"' | sed 's/"resets_at":"//;s/"//')

# Parse weekly (7-day)
WEEKLY=$(echo "$RESP" | grep -o '"seven_day":{[^}]*}' | grep -o '"utilization":[0-9]*' | sed 's/.*://')
WEEKLY_RESET=$(echo "$RESP" | grep -o '"seven_day":{[^}]*}' | grep -o '"resets_at":"[^"]*"' | sed 's/"resets_at":"//;s/"//')

SESSION=${SESSION:-0}
WEEKLY=${WEEKLY:-0}

# Calculate time until reset
NOW=$(date +%s)

if [ -n "$SESSION_RESET" ]; then
  if [[ "$OSTYPE" == "darwin"* ]]; then
    SESSION_TS=$(date -j -f "%Y-%m-%dT%H:%M:%S" "${SESSION_RESET%Z}" +%s 2>/dev/null || echo 0)
  else
    SESSION_TS=$(date -d "${SESSION_RESET}" +%s 2>/dev/null || echo 0)
  fi
  SESSION_LEFT=$(secs_to_human $((SESSION_TS - NOW)))
else
  SESSION_LEFT="unknown"
fi

if [ -n "$WEEKLY_RESET" ]; then
  if [[ "$OSTYPE" == "darwin"* ]]; then
    WEEKLY_TS=$(date -j -f "%Y-%m-%dT%H:%M:%S" "${WEEKLY_RESET%Z}" +%s 2>/dev/null || echo 0)
  else
    WEEKLY_TS=$(date -d "${WEEKLY_RESET}" +%s 2>/dev/null || echo 0)
  fi
  WEEKLY_LEFT=$(secs_to_human $((WEEKLY_TS - NOW)))
else
  WEEKLY_LEFT="unknown"
fi

# Output format
if [ "$FORMAT" = "json" ]; then
  OUTPUT=$(cat <<EOF
{
  "session": {
    "utilization": $SESSION,
    "resets_in": "$SESSION_LEFT",
    "resets_at": "$SESSION_RESET"
  },
  "weekly": {
    "utilization": $WEEKLY,
    "resets_in": "$WEEKLY_LEFT",
    "resets_at": "$WEEKLY_RESET"
  },
  "cached_at": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
)
else
  # Beautiful text output with emojis
  SESSION_BAR=""
  WEEKLY_BAR=""
  
  # Session progress bar
  SESSION_FILLED=$((SESSION / 10))
  SESSION_EMPTY=$((10 - SESSION_FILLED))
  for ((i=0; i<SESSION_FILLED; i++)); do SESSION_BAR="${SESSION_BAR}█"; done
  for ((i=0; i<SESSION_EMPTY; i++)); do SESSION_BAR="${SESSION_BAR}░"; done
  
  # Weekly progress bar
  WEEKLY_FILLED=$((WEEKLY / 10))
  WEEKLY_EMPTY=$((10 - WEEKLY_FILLED))
  for ((i=0; i<WEEKLY_FILLED; i++)); do WEEKLY_BAR="${WEEKLY_BAR}█"; done
  for ((i=0; i<WEEKLY_EMPTY; i++)); do WEEKLY_BAR="${WEEKLY_BAR}░"; done
  
  # Determine emoji based on usage level
  if [ "$SESSION" -gt 80 ]; then
    SESSION_EMOJI="🔴"
  elif [ "$SESSION" -gt 50 ]; then
    SESSION_EMOJI="🟡"
  else
    SESSION_EMOJI="🟢"
  fi
  
  if [ "$WEEKLY" -gt 80 ]; then
    WEEKLY_EMOJI="🔴"
  elif [ "$WEEKLY" -gt 50 ]; then
    WEEKLY_EMOJI="🟡"
  else
    WEEKLY_EMOJI="🟢"
  fi
  
  OUTPUT=$(cat <<EOF
🦞 Claude Code Usage

⏱️  Session (5h): $SESSION_EMOJI $SESSION_BAR $SESSION%
   Resets in: $SESSION_LEFT

📅 Weekly (7d): $WEEKLY_EMOJI $WEEKLY_BAR $WEEKLY%
   Resets in: $WEEKLY_LEFT
EOF
)
fi

# Cache the output
echo "$OUTPUT" > "$CACHE_FILE"
echo "$OUTPUT"
