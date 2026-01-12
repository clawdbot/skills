---
name: miniflux
description: "Browse, read, and manage Miniflux feed articles. Use when Claude needs to work with RSS/atom feeds via Miniflux - listing unread/new articles, reading article content, marking articles as read, and managing feeds/categories. Provides CLI access with flexible output formats (headlines, summaries, full content)."
metadata: {"clawdbot":{"emoji":"📣","requires":{"bins":["uv"]}}}
---

# Miniflux Skill

Browse, read, and manage Miniflux RSS/atom feed articles through a CLI.

## Quick Start

```bash
# List unread articles (brief format)
uv run scripts/miniflux-cli.py list --status=unread --brief

# Get article details
uv run scripts/miniflux-cli.py get 123

# Mark articles as read
uv run scripts/miniflux-cli.py mark-read 123 456

# Show article statistics (word count, reading time)
uv run scripts/miniflux-cli.py stats --entry-id=123
```

## Configuration

Configuration precedence (highest to lowest):
1. **CLI flags**: `--url`, `--api-key`
2. **Environment variables**: `MINIFLUX_URL`, `MINIFLUX_API_KEY`
3. **Config file**: `~/.local/share/miniflux/config.json` (auto-created on first run)

### Setup

```bash
# Option 1: Environment variables (recommended for agents)
export MINIFLUX_URL="https://miniflux.example.org"
export MINIFLUX_API_KEY="your-api-key"

# Option 2: CLI flags (one-time, saves to config)
uv run scripts/miniflux-cli.py --url="https://miniflux.example.org" --api-key="xxx" list
```

## Subcommands

### list - List Articles

List articles with optional filtering.

```bash
# Unread articles (brief)
uv run scripts/miniflux-cli.py list --status=unread --brief

# From specific feed with summary
uv run scripts/miniflux-cli.py list --feed=42 --summary

# Search with limit
uv run scripts/miniflux-cli.py list --search="python" --limit=10

# Starred articles
uv run scripts/miniflux-cli.py list --starred
```

**Flags:**
- `--status={read,unread,removed}` - Filter by status
- `--feed=ID` - Filter by feed ID
- `--category=ID` - Filter by category ID
- `--starred` - Show only starred
- `--search=QUERY` - Search articles
- `--limit=N` - Max number of entries
- `--offset=N` - Skip first N chars in content
- `--content-limit=N` - Max characters per article
- `-b, --brief` - Titles only
- `-s, --summary` - Title + excerpt
- `-f, --full` - Full content (default)
- `--json` - JSON output
- `--plain` - Single-line per entry

### get - Get Article by ID

Fetch a single article with content control.

```bash
# Full article
uv run scripts/miniflux-cli.py get 123

# First 2000 characters
uv run scripts/miniflux-cli.py get 123 --limit=2000

# Read from character 1000 to 2000 (pagination)
uv run scripts/miniflux-cli.py get 123 --offset=1000 --limit=1000
```

When content is truncated, shows: `[...truncated, total: N chars]`

### mark-read - Mark as Read

Mark one or more articles as read.

```bash
# Single article
uv run scripts/miniflux-cli.py mark-read 123

# Multiple articles
uv run scripts/miniflux-cli.py mark-read 123 456 789
```

### mark-unread - Mark as Unread

Mark one or more articles as unread.

```bash
uv run scripts/miniflux-cli.py mark-unread 123
```

### feeds - List Feeds

List all configured feeds.

```bash
# Human-readable
uv run scripts/miniflux-cli.py feeds

# JSON format
uv run scripts/miniflux-cli.py feeds --json
```

### categories - List Categories

List all categories.

```bash
uv run scripts/miniflux-cli.py categories
```

### stats - Statistics

Show unread counts or article statistics.

```bash
# Article statistics (word count, character count, reading time)
uv run scripts/miniflux-cli.py stats --entry-id=123

# Global unread counts per feed
uv run scripts/miniflux-cli.py stats
```

### refresh - Refresh Feeds

Trigger feed refresh.

```bash
# Refresh all feeds
uv run scripts/miniflux-cli.py refresh --all

# Refresh specific feed
uv run scripts/miniflux-cli.py refresh --feed=42
```

### search - Search Articles

Convenient alias for `list --search`.

```bash
uv run scripts/miniflux-cli.py search "rust"
uv run scripts/miniflux-cli.py search "ai" --status=unread --brief
```

## Output Formats

- `--brief` / `-b` - Quick overview (titles + feed + date)
- `--summary` / `-s` - Title + content preview (200 chars)
- `--full` / `-f` - Complete article content (default)
- `--json` - Raw JSON output for machine processing
- `--plain` - Single-line per entry (tab-separated)

## Long Article Handling

For articles with large content (e.g., >5k words):

1. **Check statistics first:**
   ```bash
   uv run scripts/miniflux-cli.py stats --entry-id=123
   ```
   Shows word count, character count, reading time.

2. **Use pagination to read in chunks:**
   ```bash
   # First 5000 chars
   uv run scripts/miniflux-cli.py get 123 --limit=5000

   # Next 5000 chars (chars 5000-10000)
   uv run scripts/miniflux-cli.py get 123 --offset=5000 --limit=5000
   ```

3. **For summarization:** If article is >5000 words, use a subagent to read and summarize:
   ```bash
   # Get stats to determine word count
   uv run scripts/miniflux-cli.py stats --entry-id=123

   # If >5000 words, delegate to subagent for summarization
   ```

## Error Handling

The CLI provides helpful error messages:

- **Invalid credentials** → Check `MINIFLUX_API_KEY`
- **Article not found** → Suggests using `list` to browse
- **Missing config** → Shows config file location
- **No results** → Clear message

## Standard Flags

- `-v, --version` - Show version
- `-q, --quiet` - Suppress non-error output
- `-d, --debug` - Enable debug output
- `--no-color` - Disable colored output
- `--url=URL` - Miniflux server URL
- `--api-key=KEY` - Miniflux API key

## Examples

### Daily Workflow

```bash
# Check what's unread
uv run scripts/miniflux-cli.py list --status=unread --brief

# Read interesting articles
uv run scripts/miniflux-cli.py get 456

# Mark as read
uv run scripts/miniflux-cli.py mark-read 456
```

### Research Mode

```bash
# Search for specific topics
uv run scripts/miniflux-cli.py search "machine learning" --summary

# Get full article content
uv run scripts/miniflux-cli.py get 789
```

### Batch Processing

```bash
# Get all unread as JSON for processing
uv run scripts/miniflux-cli.py list --status=unread --json

# Mark multiple as read
uv run scripts/miniflux-cli.py mark-read 123 456 789
```

For complete help on any subcommand:
```bash
uv run scripts/miniflux-cli.py <subcommand> --help
```
