# Market Research (Clawdbot Native)

**Fork of the original `idea` skill**, rewritten to use Clawdbot's native `sessions_spawn` and native tg bot integration.

Don't let evil soul control your tg as root.

## Core Differences from Original

| Feature | Original `idea` | This `idea-clawdbot` |
|---------|----------------|---------------------|
| **Dependencies** | `claude` CLI + `tmux` + `telegram` CLI | None (fully native) |
| **Background execution** | Shell script → tmux → claude CLI | `sessions_spawn` built-in |
| **Result delivery** | Telegram Saved Messages | Current chat session |
| **Setup complexity** | High (3 CLIs, API keys, scripts) | Low (works out of box) |
| **Maintenance** | External tool updates needed | Self-contained |

## Why This Fork?

1. **Simpler setup**: No external CLIs to install or configure
2. **Better UX**: Results come back to the same conversation
3. **More reliable**: No platform dependencies (TikTok CLI auth, etc.)
4. **Easier to modify**: Pure Clawdbot tools, no shell script debugging

## Usage

Just say:
```
Idea: AI-powered calendar assistant that reads my emails
```

The assistant will:
1. Spawn a background research session
2. Do comprehensive analysis (3-5 minutes)
3. Save to `~/clawd/ideas/<slug>/research.md`
4. Send results back to your chat

## Installation

Already installed! Just follow the trigger pattern in AGENTS.md.

## Credits

Based on the original `idea` skill from ClawdHub.
