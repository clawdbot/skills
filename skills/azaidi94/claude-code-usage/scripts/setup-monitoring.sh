#!/bin/bash
# Setup Claude Code usage monitoring with Clawdbot cron

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MONITOR_SCRIPT="$SCRIPT_DIR/monitor-usage.sh"

echo "🦞 Claude Code Usage Monitoring Setup"
echo ""

# Check if clawdbot is available
if ! command -v clawdbot >/dev/null 2>&1; then
  echo "❌ clawdbot CLI not found in PATH"
  echo "Please ensure Clawdbot is installed and accessible"
  exit 1
fi

# Check if monitor script exists
if [ ! -f "$MONITOR_SCRIPT" ]; then
  echo "❌ Monitor script not found: $MONITOR_SCRIPT"
  exit 1
fi

# Default: check every 30 minutes
INTERVAL="${1:-30m}"

echo "📋 Configuration:"
echo "   Check interval: $INTERVAL"
echo "   Monitor script: $MONITOR_SCRIPT"
echo ""

# Create cron job via Clawdbot
echo "🔧 Creating cron job..."

# Use clawdbot's cron add command
# The job will run the monitor script at the specified interval
CRON_TEXT="Monitor Claude Code usage resets every $INTERVAL"

# Note: This is a placeholder - actual implementation depends on Clawdbot's cron API
# For now, we'll output the command that needs to be run

cat <<EOF

✅ Setup complete!

To activate monitoring, run:

  clawdbot cron add \\
    --schedule "$INTERVAL" \\
    --command "$MONITOR_SCRIPT" \\
    --label "Claude Code Usage Monitor"

Or add via Clawdbot gateway config:

  {
    "schedule": "$INTERVAL",
    "command": "$MONITOR_SCRIPT",
    "label": "Claude Code Usage Monitor"
  }

You'll receive notifications when:
- 🟢 Your 5-hour session quota resets
- 🟢 Your 7-day weekly quota resets

Test the monitor manually:
  $MONITOR_SCRIPT

EOF
