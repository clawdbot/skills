# Miniflux Skill

A Claude skill for browsing, reading, and managing Miniflux feed articles through a CLI.

## Features

- List unread/new articles with flexible filtering
- Read article content with pagination support for long articles
- Mark articles as read/unread
- Manage feeds and categories
- Search articles
- Multiple output formats (brief, summary, full, JSON, plain)
- Article statistics (word count, character count, reading time)

## Installation

This skill requires `uv` to be installed.

1. Copy the skill to your Claude skills directory
2. The CLI script will automatically install dependencies via `uv`

## Configuration

Set up your Miniflux credentials:

```bash
export MINIFLUX_URL="https://miniflux.example.org"
export MINIFLUX_API_KEY="your-api-key"
```

Or use CLI flags (saves to `~/.local/share/miniflux/config.json`):

```bash
uv run scripts/miniflux-cli.py --url="https://miniflux.example.org" --api-key="xxx" list
```

## Usage Examples

```bash
# List unread articles
uv run scripts/miniflux-cli.py list --status=unread --brief

# Get article details
uv run scripts/miniflux-cli.py get 123

# Mark as read
uv run scripts/miniflux-cli.py mark-read 123

# Show article statistics
uv run scripts/miniflux-cli.py stats --entry-id=123

# Search articles
uv run scripts/miniflux-cli.py search "rust"
```

## Output Formats

| Format | Description |
|--------|-------------|
| `--brief` / `-b` | Titles + feed + date only |
| `--summary` / `-s` | Title + content preview (200 chars) |
| `--full` / `-f` | Complete article content (default) |
| `--json` | Raw JSON output for machine processing |
| `--plain` | Single-line per entry (tab-separated) |

## Long Article Handling

For large articles (>5k words):

1. Check statistics: `uv run scripts/miniflux-cli.py stats --entry-id=123`
2. Use pagination: `uv run scripts/miniflux-cli.py get 123 --limit=5000`
3. Read next chunk: `uv run scripts/miniflux-cli.py get 123 --offset=5000 --limit=5000`

## Available Commands

| Command | Description |
|---------|-------------|
| `list` | List articles with filtering |
| `get` | Get single article by ID |
| `mark-read` | Mark article(s) as read |
| `mark-unread` | Mark article(s) as unread |
| `feeds` | List all feeds |
| `categories` | List all categories |
| `stats` | Show unread counts and article statistics |
| `refresh` | Refresh feeds |
| `search` | Search articles |

## Requirements

- Python >= 3.12
- uv
- Miniflux >= 2.0.49

## License

MIT
