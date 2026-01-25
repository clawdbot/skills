# tmux-agents 🖥️

Run coding agents in persistent tmux sessions. They work in the background while you do other things.

## Features

- **5 agents**: Claude Code, Codex, Gemini + local Ollama variants
- **Cloud or Local**: Use API credits for speed, or run free on local Ollama
- **Parallel sessions**: Run multiple agents on different tasks
- **Persistent**: Sessions survive restarts
- **Simple workflow**: spawn → check → collect

## Installation

```bash
clawdhub install tmux-agents
```

Requires: `tmux` (auto-installs via brew if missing)

## Quick Start

```bash
# Spawn an agent with a task
./skills/tmux-agents/scripts/spawn.sh fix-bug "Fix the login validation" claude

# Check progress
./skills/tmux-agents/scripts/check.sh fix-bug

# Watch live
tmux attach -t fix-bug

# Kill when done
tmux kill-session -t fix-bug
```

## Available Agents

### ☁️ Cloud (API credits)
| Agent | Description |
|-------|-------------|
| `claude` | Claude Code (default) |
| `codex` | OpenAI Codex CLI |
| `gemini` | Google Gemini CLI |

### 🦙 Local (FREE via Ollama)
| Agent | Description |
|-------|-------------|
| `ollama-claude` | Claude Code + local model |
| `ollama-codex` | Codex + local model |

## Examples

```bash
# Quick cloud task
spawn.sh api-fix "Fix REST endpoint" claude

# Long experiment (free)
spawn.sh big-refactor "Refactor all services" ollama-claude

# Parallel agents
spawn.sh backend "Build user API" claude
spawn.sh frontend "Create dashboard" codex
spawn.sh tests "Write unit tests" ollama-claude
```

## Commands

| Script | Purpose |
|--------|---------|
| `spawn.sh <name> <task> [agent]` | Start a new agent session |
| `check.sh [name]` | Check session output |
| `status.sh` | Overview of all sessions |

## Local Setup (Optional)

For free local agents:

```bash
ollama pull glm-4.7-flash
ollama launch claude --model glm-4.7-flash --config
ollama launch codex --model glm-4.7-flash --config
```

## License

MIT
