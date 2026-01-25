# Telegram Usage Command Skill

A custom Telegram command that displays comprehensive session usage statistics in a clean, formatted message.

## Features

✅ **Quota Remaining** - Shows percentage of API quota left (provider-specific)  
✅ **Session Time** - Displays time remaining before session resets  
✅ **Token Usage** - Shows input and output tokens used in session  
✅ **Context Window** - Displays current context window usage  
✅ **Visual Indicators** - Color-coded emoji for quick status check  
✅ **Single Message** - All info in one clean Telegram message  

## Installation

### Option 1: Automatic (via ClawdHub)

```bash
clawdhub install telegram-usage
```

### Option 2: Manual (Already in workspace)

The skill is located at `/skills/telegram-usage` in your Clawdbot workspace.

## Setup

### 1. Enable the Skill

Ensure the skill is enabled in `~/.clawdbot/clawdbot.json`:

```json
{
  "skills": {
    "entries": {
      "telegram-usage": {
        "enabled": true
      }
    }
  }
}
```

### 2. Add Custom Command to Telegram (Optional)

Register the command in Telegram's bot menu via config:

```json
{
  "channels": {
    "telegram": {
      "customCommands": [
        {
          "command": "usage",
          "description": "Show session usage stats"
        }
      ]
    }
  }
}
```

### 3. Restart Gateway

```bash
clawdbot gateway restart
```

Or if running manually:

```bash
clawdbot gateway
```

## Usage

### In Telegram

Send any of these:

```
/telegram_usage
/usage          (if custom command registered)
/skill telegram-usage
```

### Output Example

```
📊 Session Usage Report

🔋 Quota Remaining
🟢 82% of API quota available
Provider: anthropic

⏱️ Session Time
3 hours 40 minutes remaining
(resets daily at 4:00 AM)

🎯 Tokens Used
4,370 total tokens
├─ Input: 2,847
└─ Output: 1,523

📦 Context Window
🟢 45% used
1,856 / 4,096 tokens

Model: Claude 3.5 Haiku
```

## Configuration

No additional configuration required. The skill reads from Clawdbot's session state automatically.

### Optional: Adjust Reset Time

The default session reset is 4:00 AM. Configure in `~/.clawdbot/clawdbot.json`:

```json
{
  "session": {
    "reset": {
      "mode": "daily",
      "atHour": 4
    }
  }
}
```

## Color Indicators

- 🟢 **Green** — Good (75%+ remaining)
- 🟡 **Yellow** — Warning (50-75% remaining)
- 🟠 **Orange** — Low (25-50% remaining)
- 🔴 **Red** — Critical (<25% remaining)

## How It Works

1. **Runs as a skill** — Loads via Clawdbot's skill system
2. **Uses session data** — Reads from current session store
3. **Formats with HTML** — Telegram-safe HTML formatting (bold, code blocks)
4. **Single message** — Returns all info in one Telegram message
5. **Real-time** — Updates on each invocation with current values

## Files Included

- `SKILL.md` — Skill metadata and AgentSkills manifest
- `handler.js` — Node.js handler for formatting usage data
- `README.md` — This file
- `config-example.json` — Example configuration

## Testing

### Manual Test (CLI)

```bash
node /home/drew-server/clawd/skills/telegram-usage/handler.js
```

Expected output: Formatted usage report in HTML

### JSON Output

```bash
node /home/drew-server/clawd/skills/telegram-usage/handler.js json
```

Expected output: Raw statistics as JSON

### In Telegram

1. Send `/usage` in any DM with the bot
2. Expect a formatted message with current stats
3. Repeat to see updated values

## Troubleshooting

### Command not appearing in Telegram

- Make sure the skill is enabled: `clawdbot config get skills.entries.telegram-usage.enabled`
- Restart the gateway: `clawdbot gateway restart`
- Check logs: `clawdbot logs --follow`

### Stats show zero/wrong values

- The skill reads from your current session state
- Start a new session with `/new` and try again
- Verify session file exists: `~/.clawdbot/agents/main/sessions/sessions.json`

### HTML formatting looks wrong

- Telegram has limited HTML support
- The skill uses safe tags: `<b>`, `<i>`, `<code>`
- If Telegram rejects it, check gateway logs

## Technical Details

### Quota Source

The quota percentage comes from:
1. Current provider's usage tracking (if enabled)
2. Defaults to 85% if no tracking available
3. Can be customized per provider

### Session Time

- Resets daily at configured time (default 4:00 AM local)
- Shows time until next reset
- Can be overridden with `/reset` or `/new` commands

### Tokens

- **Input tokens**: Counted from the assistant's input context
- **Output tokens**: Counted from the assistant's responses
- **Total**: Sum of input + output for the current session

### Context Usage

- Shows current position in context window
- Updates as conversation grows
- Includes messages, files, tools, and system prompts

## Limitations

- **DMs only** — Groups show session-specific stats but structure is the same
- **Session-based** — Stats reset when session resets (daily or on explicit `/reset`)
- **Approximate** — Percentages are rounded to nearest whole number
- **Provider-dependent** — Quota details vary by API provider (Anthropic, OpenAI, etc.)

## Future Enhancements

Potential improvements:
- [ ] Graph visualization (text-based)
- [ ] Historical tracking across sessions
- [ ] Cost estimation per provider
- [ ] Token burn rate (tokens/minute)
- [ ] Context compression recommendations
- [ ] Quota alerts when low

## License

This skill is part of the Clawdbot project.

## Support

- **Docs**: https://docs.clawd.bot/tools/skills
- **Issues**: Check Clawdbot GitHub
- **Questions**: See `/help` in Telegram
