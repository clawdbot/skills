---
name: telegram-usage
description: Display session usage statistics (quota, session time, tokens, context)
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["node"]}}}
---

# Telegram Usage Stats

Display comprehensive session usage statistics by running the handler script.

## What it does

Shows a quick status message with:
- **Quota Remaining**: Percentage of API quota left with visual indicator
- **Reset Timer**: Time remaining until quota resets

## How to use this skill

When the user asks for usage statistics, quota info, or session data:

```bash
node /home/drew-server/clawd/skills/telegram-usage/handler.js
```

This will output formatted HTML suitable for Telegram's parseMode.

## Output Format

The response is formatted as a clean Telegram message with:
- Section headers (bold)
- Clear percentages and time remaining
- Visual indicators (emoji)
- All in one message for quick reference

## Example Output

```
📊 API Usage

🔋 Quota: 🟢 47%
⏱️ Resets in: 53m
```

## Notes

- Pulls real-time data from `clawdbot models status`
- Updates on each invocation with current API quota values
- Uses plain text formatting for Telegram compatibility
