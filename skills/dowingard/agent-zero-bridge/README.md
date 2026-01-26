# Agent Zero Bridge - Clawdbot Skill

Bidirectional communication bridge between [Clawdbot](https://github.com/clawdbot/clawdbot) and [Agent Zero](https://github.com/frdel/agent-zero).

## What It Does

```
┌─────────────┐                    ┌─────────────┐
│  Clawdbot   │◄──────────────────►│ Agent Zero  │
│  (Claude)   │                    │   (A0)      │
└─────────────┘                    └─────────────┘
```

- **Clawdbot → Agent Zero**: Delegate complex coding/research tasks
- **Agent Zero → Clawdbot**: Report progress, ask questions, notify completion
- **Task Breakdown**: Break complex tasks into tracked, checkable steps

## Installation

### Option 1: Let Clawdbot Install It

Just tell Clawdbot:
> "Install the Agent Zero bridge skill"

Or if you have this repo cloned:
> "Install the Agent Zero bridge skill from ~/path/to/this/folder"

### Option 2: Manual Installation

```bash
# Clone or download this repo
git clone https://github.com/DOWingard/Clawdbot-Agent0-Bridge.git

# Copy to Clawdbot skills directory
cp -r Clawdbot-Agent0-Bridge ~/.clawdbot/skills/agent-zero-bridge

# Configure
cd ~/.clawdbot/skills/agent-zero-bridge
cp .env.example .env
# Edit .env with your API keys (see SKILL.md for details)
```

## Quick Start

After installation, tell Clawdbot:
- "Ask Agent Zero to build a REST API"
- "Delegate this coding task to A0"
- "Have Agent Zero review this code"

Or use the CLI directly:
```bash
node ~/.clawdbot/skills/agent-zero-bridge/scripts/a0_client.js "Your task here"
```

## File Structure

```
agent-zero-bridge/
├── SKILL.md          # Clawdbot skill definition + setup guide
├── .env.example      # Configuration template
├── .gitignore
├── LICENSE           # MIT
├── README.md         # This file
└── scripts/
    ├── a0_client.js        # CLI: Clawdbot → Agent Zero
    ├── clawdbot_client.js  # CLI: Agent Zero → Clawdbot
    ├── task_breakdown.js   # Task breakdown workflow
    └── lib/
        ├── config.js       # Configuration loader
        ├── a0_api.js       # Agent Zero API client
        ├── clawdbot_api.js # Clawdbot API client
        └── cli.js          # CLI argument parser
```

## Configuration

See `SKILL.md` for detailed setup instructions, including:
- How to get your Agent Zero API token
- Clawdbot Gateway configuration
- Docker deployment for bidirectional communication

## Requirements

- Node.js 18+ (for built-in fetch)
- Agent Zero running (Docker recommended)
- Clawdbot Gateway with HTTP endpoints enabled

## License

MIT
