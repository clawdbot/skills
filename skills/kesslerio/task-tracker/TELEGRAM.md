# Telegram Integration

This skill supports Telegram slash commands for quick access to task management features.

## Setup

Add these custom commands to your Clawdbot config (`~/.clawdbot/clawdbot.json`):

```json5
{
  channels: {
    telegram: {
      customCommands: [
        {"command": "daily", "description": "Daily standup (priorities, blockers)"},
        {"command": "weekly", "description": "Weekly priorities"},
        {"command": "done24h", "description": "Done in last 24 hours"},
        {"command": "done7d", "description": "Done in last 7 days"}
      ]
    }
  }
}
```

## Agent Recognition

Add this to your `AGENTS.md` to handle slash command invocation:

```markdown
### Slash Command Recognition

When user sends these commands (with or without leading `/`), invoke the task-tracker scripts:

- `/daily` or "daily" → `python3 ~/clawd/skills/task-tracker/scripts/standup.py`
- `/weekly` or "weekly" → `python3 ~/clawd/skills/task-tracker/scripts/tasks.py list --priority high,medium`
- `/done24h` or "done24h" or "done last 24 hours" → Show completed tasks from last 24 hours
- `/done7d` or "done7d" or "done last week" → Show completed tasks from last 7 days

Alternative: `bash ~/clawd/skills/task-tracker/scripts/telegram-commands.sh {daily|weekly|done24h|done7d}`
```

## Available Commands

| Command | Description | Direct Script |
|---------|-------------|---------------|
| `/daily` | Daily standup with priorities, blockers, recent completions | `standup.py` |
| `/weekly` | List high and medium priority tasks for the week | `tasks.py list --priority high,medium` |
| `/done24h` | Show tasks completed in the last 24 hours | `tasks.py list --status done` (filtered) |
| `/done7d` | Show tasks completed in the last 7 days | `tasks.py list --status done` (filtered) |

## Wrapper Script

The `scripts/telegram-commands.sh` wrapper provides a simple interface for all commands:

```bash
# From the skill directory
bash scripts/telegram-commands.sh daily
bash scripts/telegram-commands.sh weekly
bash scripts/telegram-commands.sh done24h
bash scripts/telegram-commands.sh done7d
```

Or create a symlink in your `~/clawd/scripts/` directory:

```bash
ln -s ~/clawd/skills/task-tracker/scripts/telegram-commands.sh ~/clawd/scripts/task-shortcuts.sh
```

## Usage

Once configured, users can:

1. **Use slash commands** in Telegram: `/daily`, `/weekly`, etc.
2. **Type natural language**: "daily standup", "show weekly priorities"
3. **Call the wrapper directly**: `bash telegram-commands.sh daily`

The agent automatically recognizes these patterns and invokes the appropriate script.

## Restart Required

After updating your config, restart Clawdbot:

```bash
clawdbot daemon restart
# or via the gateway tool
# gateway call restart --params '{"reason": "Added Telegram slash commands"}'
```

The new commands will appear in Telegram's bot menu (tap `/` to see them).
