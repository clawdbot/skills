# Twitter Bookmark Sync

Automatically ranks your Twitter bookmarks daily and delivers a curated reading list.

**The problem:** You bookmark tweets but never read them. They pile up and important content gets lost in the noise.

**This tool:** Self-learning bookmark curator that adapts to your interests, ranks by personal value, and delivers your best reads every morning.

---

## ⚡ What It Does

**Your bookmarks get smarter over time.**

The tool:
- **Learns** what you care about from your bookmarking patterns
- **Adapts** ranking weights based on what you actually save
- **Decays** old interests automatically (unless reinforced)
- **Delivers** personalized value statements every morning

The more you bookmark, the better it gets at knowing what matters to you.

Zero manual work needed.

---

## 🛠️ Getting Ready

Before installing this skill:

**You'll need:**
- **macOS 10.15 (Catalina) or later**
- **Twitter account** with bookmarks
- **Homebrew** for installing dependencies

**Install through Homebrew:**

```bash
# Install bird CLI
brew install steipete/tap/bird

# Install jq
brew install jq
```

**Set up Twitter authentication:**

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

## 🚀 Installation

```bash
clawdhub install twitter-bookmark-sync
cd ~/clawd/skills/twitter-bookmark-sync
./install.sh
```

The installer will:
- Verify dependencies
- Create your config file
- Guide you through cron setup
- Run a test sync

---

## 🔧 How It Works

**Result:** A self-learning curator that gets smarter with every bookmark.

**The schedule:**

**Midnight (00:00) - Learning & Ranking:**
1. Fetches bookmarks from last 24 hours
2. **Categorizes** each by topic and value type
3. **Updates** ranking algorithm:
   - Applies time decay (5% per day) to old interests
   - Reinforces categories you're actively bookmarking
   - Discovers new interest patterns automatically
   - Normalizes weights to maintain balance
4. **Ranks** new bookmarks using evolved criteria
5. Saves to `~/Documents/twitter-reading-YYYY-MM-DD.md`

**Morning (08:00) - Notification:**
1. Analyzes why each bookmark matters to YOU specifically
2. Sends value-focused statements (not content summaries)
3. Links to full reading list

**Self-Learning Algorithm:**

**Initial state** (from USER.md):
- London transition: weight 100
- Crypto insights: weight 100
- Career growth: weight 95
- Investment strategy: weight 90
- ... (11 categories total)

**After 30 days** (example evolution):
- If you bookmark lots of crypto → crypto weight stays high (100)
- If you stop bookmarking relationships → weight decays (90 → 85 → 81...)
- If you bookmark AI tools daily → new category emerges ("discovered_ai_tools": 65)

**Decay mechanics:**
- 5% weight reduction per day for unused categories
- When you bookmark a category again → decay resets
- Floor: minimum weight of 10 (never disappears completely)

**Configuration:**
```json5
{
  "fetch_time": "00:00",           // When to learn & rank
  "notification_time": "08:00",     // When to notify
  "lookback_hours": 24,             // How far back to check
  "notification_channel": "telegram" // Where to send
}
```

Ranking criteria stored in: `~/clawd/twitter-bookmark-sync-criteria.json`  
(Evolves automatically — you don't edit this manually)

---
---

# 📚 Additional Information

**Everything below is optional.** The skill works out-of-the-box with defaults.

This section contains:
- Advanced configuration
- Notification channel setup
- Manual usage
- Troubleshooting

**You don't need to read this for initial installation.**

---

<details>
<summary><b>Advanced Configuration</b></summary>

<br>

Edit `~/clawd/twitter-bookmark-sync-config.json`:

**Change timing:**
```json5
{
  "fetch_time": "23:00",  // 11pm instead of midnight
  "notification_time": "07:00"  // 7am instead of 8am
}
```

**Change lookback window:**
```json5
{
  "lookback_hours": 24  // Check last 24 hours instead of 16
}
```

**Customize interests:**
```json5
{
  "keywords_high": [
    "your", "specific", "interests"
  ],
  "keywords_medium": [
    "secondary", "topics"
  ]
}
```

</details>

<details>
<summary><b>Notification Channels</b></summary>

<br>

**Telegram (default):**
```json5
{
  "notification_channel": "telegram"
}
```

Results sent to your Telegram chat.

**Gmail (via gog skill):**
```json5
{
  "notification_channel": "gmail",
  "gmail_to": "your.email@gmail.com"
}
```

Requires gog skill installed and configured.

**Slack:**
```json5
{
  "notification_channel": "slack",
  "slack_channel": "#bookmarks"
}
```

Results sent to specified Slack channel.

</details>

<details>
<summary><b>Manual Usage</b></summary>

<br>

**Run sync immediately:**
```bash
cd ~/clawd/skills/twitter-bookmark-sync
./scripts/sync.sh
```

**Send notification now:**
```bash
./scripts/notify.sh
```

**Check logs:**
```bash
tail -f ~/clawd/logs/twitter-bookmark-sync.log
```

</details>

<details>
<summary><b>Troubleshooting</b></summary>

<br>

**"No bookmarks found"**

Check bird authentication:
```bash
bird whoami
```

Verify you have bookmarks:
```bash
bird bookmarks -n 5
```

**"Permission denied"**

Make scripts executable:
```bash
chmod +x ~/clawd/skills/twitter-bookmark-sync/scripts/*.sh
chmod +x ~/clawd/skills/twitter-bookmark-sync/scripts/*.py
```

**"Twitter cookies expired"**

Re-extract cookies from browser and update `~/.config/bird/config.json5`

**"Notification not sent"**

Check Clawdbot status:
```bash
clawdbot status
```

Verify notification channel in config.

</details>

---

## License

MIT
