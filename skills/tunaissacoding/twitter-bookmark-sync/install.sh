#!/usr/bin/env bash
set -euo pipefail

# twitter-bookmark-sync installer
# Sets up cron jobs for automated bookmark curation

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CONFIG_FILE="$HOME/clawd/twitter-bookmark-sync-config.json"

echo "🚀 twitter-bookmark-sync installer"
echo ""

# Check dependencies
echo "[1/4] Checking dependencies..."
command -v bird >/dev/null || {
    echo "❌ bird CLI not found"
    echo "   Install: brew install steipete/tap/bird"
    exit 1
}

command -v jq >/dev/null || {
    echo "❌ jq not found"
    echo "   Install: brew install jq"
    exit 1
}

bird whoami >/dev/null 2>&1 || {
    echo "❌ bird not authenticated"
    echo "   Configure Twitter cookies first (see SKILL.md)"
    exit 1
}

echo "✅ Dependencies OK"
echo ""

# Create config if doesn't exist
echo "[2/4] Creating config..."
if [ -f "$CONFIG_FILE" ]; then
    echo "Config already exists at: $CONFIG_FILE"
    read -p "Overwrite? (y/n): " -n 1 -r
    echo ""
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        echo "Keeping existing config"
    else
        rm "$CONFIG_FILE"
    fi
fi

if [ ! -f "$CONFIG_FILE" ]; then
    cat > "$CONFIG_FILE" << 'EOF'
{
  "fetch_time": "00:00",
  "notification_time": "08:00",
  "lookback_hours": 24,
  "notification_channel": "telegram",
  "output_dir": "~/Documents"
}
EOF
    echo "✅ Created config at: $CONFIG_FILE"
fi

# Initialize ranking criteria from USER.md
CRITERIA_FILE="$HOME/clawd/twitter-bookmark-sync-criteria.json"

echo ""
echo "Initializing self-learning ranking algorithm..."

if [ -f "$CRITERIA_FILE" ]; then
    echo "Criteria file already exists at: $CRITERIA_FILE"
    read -p "Reset to initial state? (y/n): " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        rm "$CRITERIA_FILE"
    fi
fi

if [ ! -f "$CRITERIA_FILE" ]; then
    python3 "$SCRIPT_DIR/scripts/init-criteria.py" "$CRITERIA_FILE"
    echo ""
    echo "✅ Self-learning algorithm initialized"
    echo "   It will adapt to your bookmarking patterns over time"
fi

# Make scripts executable
chmod +x "$SCRIPT_DIR/scripts/"*.sh
chmod +x "$SCRIPT_DIR/scripts/"*.py

echo ""

# Set up cron jobs using Clawdbot
echo "[3/4] Setting up schedule..."

FETCH_TIME=$(jq -r '.fetch_time' "$CONFIG_FILE")
NOTIFY_TIME=$(jq -r '.notification_time' "$CONFIG_FILE")

# Convert HH:MM to cron schedule
FETCH_HOUR=$(echo "$FETCH_TIME" | cut -d: -f1)
FETCH_MIN=$(echo "$FETCH_TIME" | cut -d: -f2)
NOTIFY_HOUR=$(echo "$NOTIFY_TIME" | cut -d: -f1)
NOTIFY_MIN=$(echo "$NOTIFY_TIME" | cut -d: -f2)

# Remove old jobs (if any)
clawdbot cron list 2>/dev/null | grep -q "twitter-bookmark-fetch" && {
    echo "Removing old fetch job..."
    # Would remove old job here
}

echo "Setting up cron jobs:"
echo "  - Fetch & rank: Daily at $FETCH_TIME"
echo "  - Notify: Daily at $NOTIFY_TIME"
echo ""

cat << EOF
To set up cron jobs, ask Clawdbot:

"Set up daily cron job at $FETCH_TIME to run:
bash $SCRIPT_DIR/scripts/sync.sh

And another daily job at $NOTIFY_TIME to run:
bash $SCRIPT_DIR/scripts/notify.sh"
EOF

echo ""

# Test run
echo "[4/4] Testing..."
read -p "Run a test sync now? (y/n): " -n 1 -r
echo ""

if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Running test sync..."
    bash "$SCRIPT_DIR/scripts/sync.sh"
    echo ""
    echo "Check your output directory:"
    OUTPUT_DIR=$(jq -r '.output_dir' "$CONFIG_FILE" | sed "s|~|$HOME|")
    ls -lh "$OUTPUT_DIR"/twitter-reading-*.md | tail -1
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "Next steps:"
echo "1. Edit config if needed: $CONFIG_FILE"
echo "2. Ask Clawdbot to set up the cron jobs (see above)"
echo "3. Check tomorrow morning for your reading list!"
