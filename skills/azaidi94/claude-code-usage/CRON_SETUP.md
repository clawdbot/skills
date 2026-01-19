# Setting Up Automated Monitoring

## Option 1: Add via Clawdbot Config (Recommended)

Add this to your Clawdbot Gateway config (`~/.clawdbot/clawdbot.json`):

```json
{
  "cron": {
    "jobs": [
      {
        "name": "claude-usage-monitor",
        "schedule": "*/30 * * * *",
        "sessionTarget": "telegram:YOUR_CHAT_ID",
        "payload": {
          "kind": "exec",
          "command": "/Users/ali/clawd/skills/claude-code-usage/scripts/monitor-usage.sh"
        }
      }
    ]
  }
}
```

Replace `YOUR_CHAT_ID` with your Telegram chat ID (usually your phone number).

Then restart Clawdbot:
```bash
clawdbot daemon restart
```

## Option 2: System Cron (Alternative)

Add to your system crontab:

```bash
crontab -e
```

Add this line:
```
*/30 * * * * /Users/ali/clawd/skills/claude-code-usage/scripts/monitor-usage.sh > /tmp/claude-monitor.log 2>&1
```

**Note:** System cron won't send Telegram notifications directly. You'll need to check `/tmp/claude-monitor.log` for reset notifications.

## Option 3: Manual Testing

Test the monitor anytime:
```bash
/Users/ali/clawd/skills/claude-code-usage/scripts/monitor-usage.sh
```

## Verification

Check if monitoring is working:
```bash
# View state file
cat /tmp/claude-usage-state.json

# View last check time
cat /tmp/claude-usage-state.json | grep last_check
```

## Notification Format

When a reset is detected, you'll receive:

```
🎉 Claude Code Session Reset!

⏱️  Your 5-hour quota has reset
📊 Usage: 2%
⏰ Next reset: 4h 58m

Fresh usage available! 🦞
```
