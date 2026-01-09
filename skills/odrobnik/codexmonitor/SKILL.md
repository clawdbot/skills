---
name: codexmonitor
description: List/inspect/watch local OpenAI Codex sessions (CLI + VS Code) using the CodexMonitor Homebrew formula.
homepage: https://github.com/Cocoanetics/CodexMonitor
metadata: {"clawdbot":{"emoji":"🧾","os":["darwin"],"requires":{"bins":["codexmonitor"]},"install":[{"id":"brew","kind":"brew","formula":"cocoanetics/tap/codexmonitor","bins":["codexmonitor"],"label":"Install codexmonitor (brew)"}]}}
---

# codexmonitor

Use `codexmonitor` to browse local OpenAI Codex sessions stored in `~/.codex/sessions`.

## Requirements
- macOS
- Codex installed and producing sessions (CLI and/or VS Code extension)

## Install (Homebrew)

```sh
brew tap cocoanetics/tap
brew install codexmonitor
```

## Common commands

- List sessions (day): `codexmonitor list 2026/01/08`
- List sessions (day, JSON): `codexmonitor list --json 2026/01/08`
- Show a session: `codexmonitor show <session-id>`
- Show with ranges: `codexmonitor show <session-id> --ranges 1...3,26...28`
- Show JSON: `codexmonitor show <session-id> --json`
- Watch all: `codexmonitor watch`
- Watch specific: `codexmonitor watch --session <session-id>`

## Notes
- `codexmonitor` reads sessions from `~/.codex/sessions/YYYY/MM/DD/`.
- Sessions can be resumed/appended by id via Codex: `codex exec resume <SESSION_ID> "message"`.
