# SilverBullet MCP Server

An MCP (Model Context Protocol) server for interacting with [SilverBullet](https://silverbullet.md/) note-taking app.

Works with Claude Desktop, Claude Code, Cursor, Moltbot, and any MCP-compatible client.

## Features

- **list_files** - List all files in your SilverBullet space
- **read_page** - Read markdown content from a page
- **write_page** - Create or update pages
- **delete_page** - Remove pages
- **append_to_page** - Append content to existing pages
- **search_pages** - Search pages by name
- **get_page_metadata** - Get page metadata without content
- **ping_server** - Check server availability
- **get_server_config** - Get server configuration

## Installation

### Using uv (Recommended)

```bash
# Clone or download this repository
cd silverbullet-skill

# Create virtual environment and install
uv venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
uv pip install -e .
```

### Using pip

```bash
pip install -e .
```

## Configuration

Set your SilverBullet server URL:

```bash
export SILVERBULLET_URL="http://localhost:3000"
```

## Running the Server

### Stdio Transport (Default)

For use with Claude Desktop, Claude Code, etc:

```bash
python server.py
# or
uv run server.py
```

### HTTP/SSE Transport (For Moltbot/Daemon Mode)

```bash
python server.py --http --port 8080
```

## Integration

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "silverbullet": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/silverbullet-skill",
        "run",
        "server.py"
      ],
      "env": {
        "SILVERBULLET_URL": "http://localhost:3000"
      }
    }
  }
}
```

### Claude Code

Add to your project's `.claude/settings.json` or global settings:

```json
{
  "mcpServers": {
    "silverbullet": {
      "command": "python",
      "args": ["/path/to/silverbullet-skill/server.py"],
      "env": {
        "SILVERBULLET_URL": "http://localhost:3000"
      }
    }
  }
}
```

### Moltbot (via mcporter)

#### Option 1: Stdio Transport

Add to `~/.mcporter/mcporter.json`:

```json
{
  "servers": {
    "silverbullet": {
      "command": "python",
      "args": ["/path/to/silverbullet-skill/server.py"],
      "transport": "stdio",
      "env": {
        "SILVERBULLET_URL": "http://localhost:3000"
      }
    }
  }
}
```

Then use via mcporter:

```bash
mcporter call silverbullet.list_files
mcporter call silverbullet.read_page path:"index.md"
mcporter call silverbullet.write_page path:"test.md" content:"# Hello World"
```

#### Option 2: HTTP Transport (Daemon Mode)

1. Start the server as a daemon:

```bash
python server.py --http --port 8080 &
```

2. Configure mcporter:

```json
{
  "servers": {
    "silverbullet": {
      "url": "http://localhost:8080/sse",
      "transport": "sse"
    }
  }
}
```

### Cursor

Add to Cursor's MCP settings:

```json
{
  "mcpServers": {
    "silverbullet": {
      "command": "python",
      "args": ["/path/to/silverbullet-skill/server.py"],
      "env": {
        "SILVERBULLET_URL": "http://localhost:3000"
      }
    }
  }
}
```

## Available Tools

| Tool | Description | Parameters |
|------|-------------|------------|
| `list_files` | List all files in space | `base_url?` |
| `read_page` | Read page content | `path`, `base_url?` |
| `write_page` | Create/update page | `path`, `content`, `base_url?` |
| `delete_page` | Delete a page | `path`, `base_url?` |
| `append_to_page` | Append to page | `path`, `content`, `base_url?` |
| `search_pages` | Search by name | `query`, `base_url?` |
| `get_page_metadata` | Get metadata only | `path`, `base_url?` |
| `ping_server` | Check availability | `base_url?` |
| `get_server_config` | Get server config | `base_url?` |

All tools accept an optional `base_url` parameter to override the default server URL.

## Moltbot Skill (Legacy)

The original curl-based skill is still available in `SKILL.md` for simpler setups.

## Development

```bash
# Install with dev dependencies
uv pip install -e ".[dev]"

# Run tests
pytest
```

## License

MIT
