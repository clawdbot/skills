# SoloBuddy

> Build-in-public companion for indie hackers

A living assistant, not a tool. SoloBuddy helps you maintain a consistent build-in-public presence without the cognitive overhead.

## What It Does

- **Content Workflow**: Idea backlog → Draft → Publish
- **Twitter Expert**: 2025 algorithm insights, hook formulas, engagement optimization
- **Twitter Monitor**: Proactive engagement opportunities from your watchlist
- **Soul Wizard**: Create project personalities from documentation
- **Activity Tracking**: Know which projects need attention

## Install

```bash
npx clawdhub@latest install solobuddy
```

## Quick Setup

1. Configure in `~/.clawdbot/clawdbot.json`:

```json
{
  "solobuddy": {
    "dataPath": "~/projects/my-build-in-public",
    "voice": "jester-sage"
  }
}
```

2. Create folder structure (use the same path as in config):

```bash
mkdir -p ~/projects/my-build-in-public/ideas ~/projects/my-build-in-public/drafts ~/projects/my-build-in-public/data
touch ~/projects/my-build-in-public/ideas/backlog.md
```

3. Start chatting: "show backlog", "new idea", "generate post"

## Voice Profiles

| Voice | Style |
|-------|-------|
| `jester-sage` | Ironic, raw, philosophical (default) |
| `technical` | Precise, detailed, structured |
| `casual` | Friendly, conversational |
| `custom` | Your own `voice.md` file |

## Modules

### Core
- Backlog management
- Draft creation
- Publishing flow
- Session logging

### Twitter Expert
Content strategy with:
- 5 proven hook formulas
- 2025 algorithm insights
- Quality checklist
- Anti-pattern detection

### Twitter Monitor (optional)
Requires `bird` CLI:
- Watchlist monitoring
- Engagement opportunities
- Draft comments with reasoning

### Soul Wizard
Interactive creation of project personalities:
- Nature (creature/tool/guide/artist)
- Voice attributes
- Philosophy extraction
- Dreams & pains

## Telegram Integration

Full button support for mobile workflow:
- Quick navigation
- One-tap generation
- Draft management

## Requirements

- **Required**: `gh` (GitHub CLI)
- **Optional**: `bird` (Twitter CLI for monitoring)

## Philosophy

> "A quiet companion, not a dashboard"

SoloBuddy notices patterns, asks questions, and connects ideas across projects. It's designed to reduce cognitive load while keeping you in control.

## Links

- [ClawdHub](https://clawdhub.com/skills/solobuddy)
- [GitHub](https://github.com/gHashTag/bip-buddy)
- [Clawdbot](https://clawd.bot)
