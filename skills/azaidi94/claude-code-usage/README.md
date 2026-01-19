# Claude Code Usage Skill

Check your Claude Code OAuth API usage limits directly from Clawdbot.

## Features

- 📊 Session (5-hour) and Weekly (7-day) utilization tracking
- 🎨 Beautiful progress bars with color-coded status indicators
- ⚡ Smart caching (60s default) to avoid API spam
- 📤 JSON output for scripting
- 🦞 Telegram-friendly formatting
- 🔔 **NEW v1.1.0**: Automated monitoring with reset notifications

## Quick Test

```bash
cd /Users/ali/clawd/skills/claude-code-usage
./scripts/claude-usage.sh
```

## Example Output

```
🦞 Claude Code Usage

⏱️  Session (5h): 🟢 █░░░░░░░░░ 18%
   Resets in: 2h 48m

📅 Weekly (7d): 🟢 ░░░░░░░░░░ 2%
   Resets in: 6d 21h
```

## Usage in Clawdbot

Just ask:
- "How much Claude usage do I have left?"
- "Check my Claude Code limits"
- "What's my Claude quota?"

The skill automatically triggers and provides a formatted response.

## Automated Monitoring (v1.1.0+)

Get notified automatically when your quotas reset!

**Quick setup:**
```bash
cd /Users/ali/clawd/skills/claude-code-usage
./scripts/monitor-usage.sh  # Test once
```

**Configure notifications:**
See `CRON_SETUP.md` for detailed instructions on setting up automated monitoring via:
- Clawdbot Gateway config (recommended)
- System cron (alternative)

You'll receive Telegram notifications when your 5-hour or 7-day quotas reset.

## Publishing to ClawdHub

To share with the community:

```bash
cd /Users/ali/clawd/skills
clawdhub publish claude-code-usage \
  --slug claude-code-usage \
  --name "Claude Code Usage" \
  --version 1.0.0 \
  --changelog "Initial release: Session & weekly usage tracking with beautiful formatting"
```

## Author

Created for Clawdbot by RZA 🦞
