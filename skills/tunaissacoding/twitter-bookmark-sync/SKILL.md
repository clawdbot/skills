---
name: twitter-bookmark-sync
description: Automatically ranks your Twitter bookmarks daily and delivers a curated reading list
---

# twitter-bookmark-sync

**Automated Twitter bookmark curation and notification**

Never miss important bookmarks. Automatically rank your Twitter bookmarks based on your interests and get a curated reading list delivered daily.

---

## What It Does

- **Learns** what matters to you from your bookmarking patterns
- **Adapts** ranking weights automatically (interests decay unless reinforced)
- **Categorizes** bookmarks by topic and value type
- **Delivers** personalized value statements every morning
- **Gets smarter** the more you use it

---

## Requirements

- macOS 10.15 or later
- Twitter account with bookmarks
- bird CLI (`brew install steipete/tap/bird`)
- Clawdbot (for scheduling and notifications)
- Twitter auth cookies configured (see Getting Ready)

---

## Getting Ready

### Step 1: Install bird CLI

```bash
brew install steipete/tap/bird
```

### Step 2: Configure Twitter Authentication

Extract your Twitter cookies from your browser:

1. Open browser → https://x.com (logged in)
2. DevTools (Cmd+Option+I) → Application → Cookies → https://x.com
3. Copy these values:
   - `auth_token`
   - `ct0`

4. Save to config:

```bash
mkdir -p ~/.config/bird
cat > ~/.config/bird/config.json5 << 'EOF'
{
  authToken: "your_auth_token_here",
  ct0: "your_ct0_here"
}
EOF
```

5. Test:
```bash
bird whoami
```

---

## Installation

```bash
clawdhub install twitter-bookmark-sync
cd ~/clawd/skills/twitter-bookmark-sync
./install.sh
```

The installer will:
1. Detect your timezone automatically
2. Set up daily cron jobs (fetch at midnight, notify at 8am)
3. Create your config file

---

## Configuration

Edit `~/clawd/twitter-bookmark-sync-config.json`:

```json5
{
  "fetch_time": "00:00",           // When to learn & rank (24h format)
  "notification_time": "08:00",     // When to send results
  "lookback_hours": 24,             // How far back to check
  "notification_channel": "telegram", // or "gmail", "slack"
  "output_dir": "~/Documents"      // Where to save reading lists
}
```

**Ranking criteria** (self-evolving):  
`~/clawd/twitter-bookmark-sync-criteria.json`

This file updates automatically based on your bookmarking patterns.  
**Do not edit manually** — let it learn from your behavior.

### Notification Channels

**Telegram (default):**
```json5
{
  "notification_channel": "telegram"
}
```

**Gmail (via gog skill):**
```json5
{
  "notification_channel": "gmail",
  "gmail_to": "your.email@gmail.com"
}
```

**Slack:**
```json5
{
  "notification_channel": "slack",
  "slack_channel": "#bookmarks"
}
```

---

## How It Works

### Daily Schedule

**Midnight (00:00) - Learning Phase:**
1. Fetches bookmarks from last 24 hours
2. **Categorizes** each (topic + value type)
3. **Updates ranking criteria:**
   - Applies time decay (5% per day) to unused interests
   - Boosts weights for categories you're actively bookmarking
   - Discovers new patterns automatically
   - Normalizes all weights
4. **Ranks** new bookmarks using evolved criteria
5. Saves to `~/Documents/twitter-reading-YYYY-MM-DD.md`

**Morning (08:00) - Notification:**
1. Analyzes WHY each bookmark matters to you
2. Sends value statements (not summaries)
3. Links to full reading list

Example notification:
```
📚 Twitter Reading List Ready!

**1. @someuser** (Score: 120)
💡 Career growth pathway • Investment strategy
🔗 https://x.com/...

**2. @another** (Score: 110)  
💡 Direct crypto insights • London transition
🔗 https://x.com/...
```

### Self-Learning System

**On first install:**
- Initializes from USER.md profile
- Creates `twitter-bookmark-sync-criteria.json`
- 11 value categories with initial weights (0-100)

**Every midnight:**
- Categorizes your new bookmarks
- Updates category weights based on usage
- Old interests decay 5% per day
- Active interests stay strong
- New patterns emerge automatically

**Example evolution:**
```
Day 1:  crypto_insights: 100, relationships: 90
Day 10: crypto_insights: 100 (active), relationships: 60 (decaying)
Day 30: crypto_insights: 100, AI_tools: 75 (discovered), relationships: 35
```

**Why this matters:**
- Adapts to your changing interests
- No manual keyword management
- Gets better at predicting what you'll value
- Reflects YOUR actual behavior, not generic defaults

---

## Manual Usage

**Run immediately:**
```bash
cd ~/clawd/skills/twitter-bookmark-sync
./scripts/sync.sh
```

**Change schedule:**
```bash
# Edit config
nano ~/clawd/twitter-bookmark-sync-config.json

# Reload cron jobs
./install.sh
```

---

## Troubleshooting

**"No bookmarks found"**
- Check bird authentication: `bird whoami`
- Verify you have bookmarks: `bird bookmarks -n 5`

**"Permission denied"**
- Check bird config: `~/.config/bird/config.json5`
- Verify cookies are valid (they expire)

**"Notification not sent"**
- Check Clawdbot is running: `clawdbot status`
- Verify notification channel in config
- Check logs: `~/clawd/logs/twitter-bookmark-sync.log`

---

## License

MIT
