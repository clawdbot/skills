---
name: linearis
version: 1.0.0
description: Linear.app CLI for issue tracking. Use for listing, creating, updating, and searching Linear issues, comments, documents, cycles, and projects. Optimized for LLM agents with JSON output.
metadata: {"clawdbot":{"emoji":"📋","requires":{"bins":["linearis"]},"install":[{"id":"npm","kind":"node","package":"linearis","bins":["linearis"],"label":"Install linearis (npm)"}]}}
---

# linearis

CLI for [Linear.app](https://linear.app) with JSON output, designed for LLM agents.

## Setup

```bash
npm install -g linearis
```

Auth (one of):
- `echo "lin_api_..." > ~/.linear_api_token` (recommended)
- `export LINEAR_API_TOKEN="lin_api_..."`
- `--api-token <token>` flag

Get API key: Linear Settings → Security & Access → Personal API keys

## Commands

### Issues

```bash
linearis issues list -l 20              # List recent issues
linearis issues list -l 10 --team WHO   # Filter by team
linearis issues search "bug"            # Full-text search
linearis issues read ABC-123            # Get issue details
linearis issues create --title "Fix bug" --team WHO --priority 2
linearis issues update ABC-123 --status "Done"
linearis issues update ABC-123 --title "New title" --assignee user123
linearis issues update ABC-123 --labels "Bug,Critical" --label-by adding
linearis issues update ABC-123 --parent-ticket EPIC-100  # Set parent
```

### Comments

```bash
linearis comments create ABC-123 --body "Fixed in PR #456"
```

### Documents

```bash
linearis documents list
linearis documents list --project "Backend"
linearis documents create --title "Spec" --content "# Overview..."
linearis documents read <doc-id>
linearis documents update <doc-id> --content "Updated"
linearis documents delete <doc-id>
```

### File Uploads/Downloads

```bash
linearis embeds upload ./screenshot.png
linearis embeds download "<url>" --output ./file.png
```

### Teams, Users, Projects

```bash
linearis teams list
linearis users list --active
linearis projects list
linearis cycles list --team WHO --active
```

### Full Usage

```bash
linearis usage  # Complete command reference (~1k tokens)
```

## Output

All commands return JSON by default. Pipe to `jq` for processing:

```bash
linearis issues list -l 5 | jq '.[].identifier'
```

## Priority Values

- 0: No priority
- 1: Urgent
- 2: High
- 3: Medium
- 4: Low

## Links

- Docs: https://github.com/czottmann/linearis
- Blog: https://zottmann.org/2025/09/03/linearis-my-linear-cli-built.html
