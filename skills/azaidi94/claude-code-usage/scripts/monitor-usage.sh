#!/bin/bash
# Claude Code Usage Monitor
# Detects usage resets and sends notifications via Clawdbot

set -euo pipefail

STATE_FILE="${STATE_FILE:-/tmp/claude-usage-state.json}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Get current usage (JSON format)
CURRENT=$("$SCRIPT_DIR/claude-usage.sh" --json --fresh 2>/dev/null)

if [ -z "$CURRENT" ]; then
  echo "❌ Failed to fetch usage" >&2
  exit 1
fi

# Extract current values using better JSON parsing
SESSION_NOW=$(echo "$CURRENT" | grep -A3 '"session"' | grep '"utilization"' | grep -o '[0-9]*')
WEEKLY_NOW=$(echo "$CURRENT" | grep -A3 '"weekly"' | grep '"utilization"' | grep -o '[0-9]*')
SESSION_RESETS=$(echo "$CURRENT" | grep -A3 '"session"' | grep '"resets_in"' | sed 's/.*"resets_in": "//;s/".*//')
WEEKLY_RESETS=$(echo "$CURRENT" | grep -A3 '"weekly"' | grep '"resets_in"' | sed 's/.*"resets_in": "//;s/".*//')

SESSION_NOW=${SESSION_NOW:-0}
WEEKLY_NOW=${WEEKLY_NOW:-0}

# Check if state file exists
if [ ! -f "$STATE_FILE" ]; then
  # First run - save state and exit
  cat > "$STATE_FILE" <<EOF
{
  "session": $SESSION_NOW,
  "weekly": $WEEKLY_NOW,
  "last_check": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF
  echo "📊 Initial state saved. Monitoring started."
  exit 0
fi

# Read previous state
SESSION_PREV=$(grep '"session"' "$STATE_FILE" | grep -o '[0-9]*')
WEEKLY_PREV=$(grep '"weekly"' "$STATE_FILE" | grep -o '[0-9]*')

SESSION_PREV=${SESSION_PREV:-0}
WEEKLY_PREV=${WEEKLY_PREV:-0}

# Detect resets (usage went down significantly)
SESSION_RESET=0
WEEKLY_RESET=0

# Session reset: if usage dropped by more than 10% AND is now <10%, or dropped by >20%
if [ "$SESSION_NOW" -lt "$SESSION_PREV" ]; then
  if ([ "$SESSION_NOW" -lt 10 ] && [ "$SESSION_PREV" -gt 15 ]) || [ "$SESSION_NOW" -lt $((SESSION_PREV - 20)) ]; then
    SESSION_RESET=1
  fi
fi

# Weekly reset: if usage dropped by more than 10% AND is now <10%, or dropped by >20%
if [ "$WEEKLY_NOW" -lt "$WEEKLY_PREV" ]; then
  if ([ "$WEEKLY_NOW" -lt 10 ] && [ "$WEEKLY_PREV" -gt 15 ]) || [ "$WEEKLY_NOW" -lt $((WEEKLY_PREV - 20)) ]; then
    WEEKLY_RESET=1
  fi
fi

# Send notifications if resets detected
if [ "$SESSION_RESET" -eq 1 ] || [ "$WEEKLY_RESET" -eq 1 ]; then
  MESSAGE=""
  
  if [ "$SESSION_RESET" -eq 1 ]; then
    MESSAGE="🎉 *Claude Code Session Reset!*\n\n"
    MESSAGE+="⏱️  Your 5-hour quota has reset\n"
    MESSAGE+="📊 Usage: *${SESSION_NOW}%*\n"
    MESSAGE+="⏰ Next reset: ${SESSION_RESETS}\n"
  fi
  
  if [ "$WEEKLY_RESET" -eq 1 ]; then
    if [ -n "$MESSAGE" ]; then
      MESSAGE+="\n---\n\n"
    fi
    MESSAGE+="🎊 *Claude Code Weekly Reset!*\n\n"
    MESSAGE+="📅 Your 7-day quota has reset\n"
    MESSAGE+="📊 Usage: *${WEEKLY_NOW}%*\n"
    MESSAGE+="⏰ Next reset: ${WEEKLY_RESETS}\n"
  fi
  
  MESSAGE+="\nFresh usage available! 🦞"
  
  # Send via clawdbot message tool
  # Note: This script is typically run by Clawdbot cron, which will capture output
  # and send it as a notification automatically. For manual testing, print to stdout.
  echo -e "$MESSAGE"
  
  echo "✅ Reset notification sent"
fi

# Update state file
cat > "$STATE_FILE" <<EOF
{
  "session": $SESSION_NOW,
  "weekly": $WEEKLY_NOW,
  "last_check": "$(date -u +%Y-%m-%dT%H:%M:%SZ)"
}
EOF

# Log current status
if [ "$SESSION_RESET" -eq 1 ] || [ "$WEEKLY_RESET" -eq 1 ]; then
  echo "📊 Session: ${SESSION_PREV}% → ${SESSION_NOW}% (RESET)"
  echo "📊 Weekly: ${WEEKLY_PREV}% → ${WEEKLY_NOW}% (RESET)"
else
  echo "📊 Session: ${SESSION_PREV}% → ${SESSION_NOW}%"
  echo "📊 Weekly: ${WEEKLY_PREV}% → ${WEEKLY_NOW}%"
fi
