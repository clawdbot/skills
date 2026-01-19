---
name: claude-code-usage
description: Check Claude Code OAuth usage limits (session & weekly quotas). Use when user asks about Claude Code usage, remaining limits, rate limits, or how much Claude usage they have left. Includes automated monitoring to notify when quotas reset.
metadata:
  clawdbot:
    emoji: "📊"
    os:
      - darwin
      - linux
    requires:
      bins:
        - curl
---

# Claude Code Usage

Check your Claude Code OAuth API usage limits for both session (5-hour) and weekly (7-day) windows.

## Quick Start

```bash
cd {baseDir}
./scripts/claude-usage.sh
```

## Usage

```bash
# Default: show cached usage (if fresh)
./scripts/claude-usage.sh

# Force refresh from API
./scripts/claude-usage.sh --fresh

# JSON output
./scripts/claude-usage.sh --json

# Custom cache TTL
./scripts/claude-usage.sh --cache-ttl 300
```

## Output

**Text format** (default):
```
🦞 Claude Code Usage

⏱️  Session (5h): 🟢 ████░░░░░░ 40%
   Resets in: 2h 15m

📅 Weekly (7d): 🟡 ██████░░░░ 60%
   Resets in: 3d 8h
```

**JSON format** (`--json`):
```json
{
  "session": {
    "utilization": 40,
    "resets_in": "2h 15m",
    "resets_at": "2026-01-19T22:15:00Z"
  },
  "weekly": {
    "utilization": 60,
    "resets_in": "3d 8h",
    "resets_at": "2026-01-22T04:00:00Z"
  },
  "cached_at": "2026-01-19T20:00:00Z"
}
```

## Features

- 📊 **Session limit** (5-hour window) - Short-term rate limit
- 📅 **Weekly limit** (7-day window) - Long-term rate limit
- ⚡ **Smart caching** - 60-second cache to avoid API spam
- 🎨 **Beautiful output** - Progress bars, emojis, color-coded status
- 🔄 **Force refresh** - `--fresh` flag to bypass cache
- 📤 **JSON output** - Machine-readable format
- 🔔 **Automated monitoring** - Get notified when quotas reset

## Status Indicators

- 🟢 **Green** - 0-50% usage (healthy)
- 🟡 **Yellow** - 51-80% usage (moderate)
- 🔴 **Red** - 81-100% usage (high/critical)

## Requirements

- **macOS**: Uses Keychain to access Claude Code credentials
- **Linux**: Uses `secret-tool` for credential storage
- **Credentials**: Must have Claude Code CLI authenticated

## How It Works

1. Retrieves OAuth token from system keychain
2. Queries `api.anthropic.com/api/oauth/usage` with OAuth bearer token
3. Parses `five_hour` and `seven_day` utilization metrics
4. Calculates time remaining until reset
5. Formats output with progress bars and status indicators
6. Caches result for 60 seconds (configurable)

## Cache

Default cache: `/tmp/claude-usage-cache` (60s TTL)

Override:
```bash
CACHE_FILE=/tmp/my-cache CACHE_TTL=300 ./scripts/claude-usage.sh
```

## Examples

**Check usage before starting work:**
```bash
./scripts/claude-usage.sh --fresh
```

**Integrate with statusline:**
```bash
usage=$(./scripts/claude-usage.sh | grep "Session" | awk '{print $NF}')
echo "Session: $usage"
```

**Get JSON for monitoring:**
```bash
./scripts/claude-usage.sh --json | jq '.session.utilization'
```

## Automated Monitoring (New in v1.1.0)

Get automatic notifications when your Claude Code quotas reset!

### Quick Setup

Test the monitor once:
```bash
./scripts/monitor-usage.sh
```

Setup automated monitoring (runs every 30 minutes):
```bash
./scripts/setup-monitoring.sh
```

Or add via Clawdbot directly:
```bash
# Check every 30 minutes
clawdbot cron add --schedule "*/30 * * * *" \
  --command "/Users/ali/clawd/skills/claude-code-usage/scripts/monitor-usage.sh" \
  --label "Claude Code Usage Monitor"
```

### What You'll Get

When your quotas reset, you'll receive notifications like:

```
🎉 Claude Code Session Reset!

⏱️  Your 5-hour quota has reset
📊 Usage: 2%
⏰ Next reset: 4h 58m

Fresh usage available! 🦞
```

### How It Works

1. **Monitors usage** every 30 minutes (configurable)
2. **Detects resets** when usage drops significantly (>10% or <5%)
3. **Sends notifications** via Telegram when resets occur
4. **Tracks state** in `/tmp/claude-usage-state.json`

### Customization

Change check interval:
```bash
# Every 15 minutes
clawdbot cron add --schedule "*/15 * * * *" ...

# Every hour
clawdbot cron add --schedule "0 * * * *" ...
```

Custom state file location:
```bash
STATE_FILE=/path/to/state.json ./scripts/monitor-usage.sh
```

## Troubleshooting

**No credentials found:**
- Ensure Claude Code CLI is installed and authenticated
- Run `claude` once to trigger OAuth flow

**API request failed:**
- Check internet connection
- Verify OAuth token hasn't expired
- Try `--fresh` to force new request

**Linux users:**
Install `libsecret` for credential storage:
```bash
# Debian/Ubuntu
sudo apt install libsecret-tools

# Fedora/RHEL
sudo dnf install libsecret
```
