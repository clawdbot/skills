---
name: silverbullet
description: MCP server for SilverBullet note-taking app - read, write, search, and manage markdown pages
homepage: https://silverbullet.md
version: 1.0.0
metadata:
  clawdbot:
    requires:
      bins: ["python3", "uv"]
    install:
      - kind: script
        label: "Install SilverBullet MCP server"
        script: |
          cd "$SKILL_DIR"
          uv venv
          source .venv/bin/activate
          uv pip install -e .
allowed-tools: "mcporter(silverbullet:*)"
---

# SilverBullet MCP Server

This skill provides an MCP server for interacting with [SilverBullet](https://silverbullet.md/), a self-hosted markdown-based note-taking app.

## Installation

### Via ClawdHub

```bash
clawdhub install silverbullet
```

### Manual

```bash
cd ~/.clawdbot/skills/silverbullet
uv venv
source .venv/bin/activate
uv pip install -e .
```

## Configuration

### 1. Set SilverBullet URL

```bash
export SILVERBULLET_URL="http://localhost:3000"
```

Or add to your shell profile (`~/.zshrc` / `~/.bashrc`).

### 2. Configure mcporter

Add to `~/.mcporter/mcporter.json`:

```json
{
  "servers": {
    "silverbullet": {
      "command": "python",
      "args": ["{baseDir}/server.py"],
      "transport": "stdio",
      "env": {
        "SILVERBULLET_URL": "http://localhost:3000"
      }
    }
  }
}
```

Replace `{baseDir}` with the actual skill path (e.g., `~/.clawdbot/skills/silverbullet`).

### 3. Verify Installation

```bash
mcporter list silverbullet
```

Should show all available tools.

## Available Tools

| Tool | Description |
|------|-------------|
| `list_files` | List all files in the SilverBullet space |
| `read_page` | Read markdown content from a page |
| `write_page` | Create or update a page |
| `delete_page` | Delete a page |
| `append_to_page` | Append content to an existing page |
| `search_pages` | Search pages by name pattern |
| `get_page_metadata` | Get page metadata (modified, created, permissions) |
| `ping_server` | Check if SilverBullet server is available |
| `get_server_config` | Get server configuration |

## Usage Examples

### List all pages

```bash
mcporter call silverbullet.list_files
```

### Read a page

```bash
mcporter call silverbullet.read_page path:"index.md"
mcporter call silverbullet.read_page path:"journal/2024-01-15.md"
```

### Create or update a page

```bash
mcporter call silverbullet.write_page path:"notes/meeting.md" content:"# Meeting Notes\n\n- Item 1\n- Item 2"
```

### Append to a page

```bash
mcporter call silverbullet.append_to_page path:"journal/today.md" content:"## Evening Update\n\nFinished the project."
```

### Search for pages

```bash
mcporter call silverbullet.search_pages query:"meeting"
```

### Delete a page

```bash
mcporter call silverbullet.delete_page path:"drafts/old-note.md"
```

### Check server status

```bash
mcporter call silverbullet.ping_server
```

## Natural Language Examples

Once configured, you can ask Moltbot:

- "List all my SilverBullet pages"
- "Read my index page from SilverBullet"
- "Create a new page called 'Project Ideas' with a list of features"
- "Search for pages containing 'meeting' in the name"
- "Append today's notes to my journal"
- "What's the last modified date of my TODO page?"
- "Is my SilverBullet server running?"

## Troubleshooting

### Server not responding

1. Check if SilverBullet is running: `curl http://localhost:3000/.ping`
2. Verify `SILVERBULLET_URL` is set correctly
3. Check firewall/network settings

### Permission denied errors

SilverBullet pages can be read-only. Check the `X-Permission` header or use `get_page_metadata` to verify permissions.

### Tool not found

1. Verify mcporter config: `cat ~/.mcporter/mcporter.json`
2. Test server directly: `python {baseDir}/server.py` (should start without errors)
3. Check Python/uv installation: `which python3 uv`

## API Reference

See [SilverBullet HTTP API](https://silverbullet.md/HTTP%20API) for full documentation of the underlying REST API.
