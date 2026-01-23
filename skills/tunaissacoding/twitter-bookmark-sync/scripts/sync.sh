#!/usr/bin/env bash
set -euo pipefail

# twitter-bookmark-sync: Fetch, rank, and save Twitter bookmarks
# Usage: ./sync.sh

CONFIG_FILE="$HOME/clawd/twitter-bookmark-sync-config.json"
CRITERIA_FILE="$HOME/clawd/twitter-bookmark-sync-criteria.json"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
LOG_DIR="$HOME/clawd/logs"
mkdir -p "$LOG_DIR"

LOG_FILE="$LOG_DIR/twitter-bookmark-sync.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "Starting bookmark sync..."

# Load config
if [ ! -f "$CONFIG_FILE" ]; then
    log "Error: Config file not found at $CONFIG_FILE"
    log "Run ./install.sh first"
    exit 1
fi

# Check for criteria file
if [ ! -f "$CRITERIA_FILE" ]; then
    log "Error: Ranking criteria file not found at $CRITERIA_FILE"
    log "Run ./install.sh to initialize"
    exit 1
fi

LOOKBACK_HOURS=$(jq -r '.lookback_hours // 24' "$CONFIG_FILE")
OUTPUT_DIR=$(jq -r '.output_dir // "~/Documents"' "$CONFIG_FILE" | sed "s|~|$HOME|")
mkdir -p "$OUTPUT_DIR"

log "Fetching bookmarks (lookback: ${LOOKBACK_HOURS}h)..."

# Fetch all bookmarks
TEMP_DIR=$(mktemp -d)
bird bookmarks --all --json 2>/dev/null > "$TEMP_DIR/bookmarks.json" || {
    log "Error: Failed to fetch bookmarks"
    log "Check bird authentication: bird whoami"
    exit 1
}

TOTAL_BOOKMARKS=$(jq '.tweets | length' "$TEMP_DIR/bookmarks.json")
log "Fetched $TOTAL_BOOKMARKS total bookmarks"

# Step 2.1-2.4: Learn from bookmarks and update criteria
log "Learning from new bookmarks and updating ranking algorithm..."
python3 "$SCRIPT_DIR/learn.py" "$TEMP_DIR/bookmarks.json" "$CRITERIA_FILE" | tee -a "$LOG_FILE"

# Step 3: Rank bookmarks using updated criteria
log "Ranking bookmarks with learned criteria..."
python3 "$SCRIPT_DIR/rank.py" "$TEMP_DIR/bookmarks.json" "$CONFIG_FILE" "$CRITERIA_FILE" "$OUTPUT_DIR" | tee -a "$LOG_FILE"

# Clean up
rm -rf "$TEMP_DIR"

log "Sync complete!"
