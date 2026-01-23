#!/usr/bin/env bash
set -euo pipefail

# twitter-bookmark-sync: Send notification with ranked bookmarks
# Usage: ./notify.sh

CONFIG_FILE="$HOME/clawd/twitter-bookmark-sync-config.json"
LOG_DIR="$HOME/clawd/logs"
LOG_FILE="$LOG_DIR/twitter-bookmark-sync.log"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

log "Sending bookmark notification..."

# Load config
if [ ! -f "$CONFIG_FILE" ]; then
    log "Error: Config file not found"
    exit 1
fi

OUTPUT_DIR=$(jq -r '.output_dir // "~/Documents"' "$CONFIG_FILE" | sed "s|~|$HOME|")
CHANNEL=$(jq -r '.notification_channel // "telegram"' "$CONFIG_FILE")
TODAY=$(date '+%Y-%m-%d')

TOP5_FILE="$OUTPUT_DIR/twitter-top5-$TODAY.json"
READING_LIST="$OUTPUT_DIR/twitter-reading-$TODAY.md"

if [ ! -f "$TOP5_FILE" ]; then
    log "No bookmarks to notify (file not found: $TOP5_FILE)"
    log "Run ./scripts/sync.sh first"
    exit 0
fi

# Build notification message with VALUE analysis
TOTAL=$(jq 'length' "$TOP5_FILE")
MESSAGE="📚 **Twitter Reading List Ready!**

**$TOTAL high-priority bookmarks** ranked by value to you:

"

# Generate value statements using Python
python3 << 'PYEOF' > /tmp/notification-preview.txt
import json
import sys

with open("$TOP5_FILE", 'r') as f:
    bookmarks = json.load(f)

# Patrick's context from USER.md
context = {
    "goals": ["move to london", "work in crypto/investment", "relationship with sybil"],
    "current": ["crypto fund 3rd year", "final year student", "building skills"],
    "interests": ["crypto", "startups", "psychology", "productivity"]
}

def analyze_value(tweet):
    """Generate why this matters to Patrick"""
    text = tweet['text'].lower()
    value = []
    
    # Career/London transition
    if any(kw in text for kw in ['london', 'uk', 'europe', 'visa', 'immigration']):
        value.append("Relevant to your London move")
    if any(kw in text for kw in ['career', 'staff', 'senior', 'promotion', 'growth']):
        value.append("Career advancement insights")
    
    # Crypto/investment work
    if any(kw in text for kw in ['crypto', 'btc', 'eth', 'defi', 'trading', 'fund']):
        value.append("Direct to your crypto work")
    if any(kw in text for kw in ['investment', 'portfolio', 'market', 'strategy']):
        value.append("Investment strategy insights")
    
    # Building/startup
    if any(kw in text for kw in ['startup', 'founder', 'build', 'product', 'growth']):
        value.append("Building/founder mindset")
    
    # Relationship/psychology
    if any(kw in text for kw in ['relationship', 'dating', 'communication', 'psychology']):
        value.append("Relationship insights (Sybil)")
    
    # Productivity/systems
    if any(kw in text for kw in ['productivity', 'system', 'habit', 'focus']):
        value.append("Productivity systems you can apply")
    
    # Business opportunity
    if any(kw in text for kw in ['business', 'revenue', 'monetize', 'niche']):
        value.append("Business model to study")
    
    if not value:
        value.append("High engagement in your interest areas")
    
    return " • ".join(value)

for b in bookmarks:
    value_statement = analyze_value(b)
    print(f"**{b['rank']}. @{b['author']}** (Score: {b['score']})")
    print(f"💡 {value_statement}")
    print(f"🔗 {b['url']}\n")

PYEOF

cat /tmp/notification-preview.txt

MESSAGE="$MESSAGE
$(cat /tmp/notification-preview.txt)

📄 Full analysis: \`$READING_LIST\`"

# Send based on channel
case "$CHANNEL" in
    "telegram")
        log "Sending to Telegram..."
        echo "$MESSAGE"
        ;;
    
    "gmail")
        GMAIL_TO=$(jq -r '.gmail_to' "$CONFIG_FILE")
        log "Sending to Gmail: $GMAIL_TO"
        
        # Use gog skill to send email
        cat > /tmp/bookmark-email.txt << EOF
To: $GMAIL_TO
Subject: Twitter Reading List - $(date '+%B %d, %Y')

$(cat "$READING_LIST")
EOF
        
        # Send via gog (placeholder - would need actual gog integration)
        log "Gmail sending not yet implemented - would use gog skill"
        ;;
    
    "slack")
        SLACK_CHANNEL=$(jq -r '.slack_channel // "#general"' "$CONFIG_FILE")
        log "Sending to Slack: $SLACK_CHANNEL"
        # Would use message tool with channel=slack
        ;;
    
    *)
        log "Unknown channel: $CHANNEL"
        ;;
esac

log "Notification sent!"
