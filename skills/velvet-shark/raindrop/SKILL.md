---
name: raindrop
description: Search, list, and manage Raindrop.io bookmarks via CLI. Use when the user wants to find saved links, browse collections, add new bookmarks, organize with tags, move bookmarks between collections, or work with their Raindrop library. Supports reading (search, list, get, tags) and writing (add, delete, move, update, bulk operations).
metadata: {"clawdbot":{"emoji":"🌧️","homepage":"https://raindrop.io","requires":{"bins":["bash","curl","jq","bc"]}}}
---

# Raindrop.io Bookmarks

Manage bookmarks via the Raindrop.io API.

## Setup

```bash
# Get token from: https://app.raindrop.io/settings/integrations → "Create test token"
echo 'RAINDROP_TOKEN="your-token"' > ~/.config/raindrop.env
```

## Quick Start

```bash
# Search bookmarks
{baseDir}/scripts/raindrop.sh search "AI tools"

# List unsorted bookmarks
{baseDir}/scripts/raindrop.sh list -1 --limit 50

# Count unsorted
{baseDir}/scripts/raindrop.sh count -1

# Create collection and move bookmarks
{baseDir}/scripts/raindrop.sh create-collection "AI Coding"
{baseDir}/scripts/raindrop.sh move 12345 66016720

# Bulk move (efficient!)
{baseDir}/scripts/raindrop.sh bulk-move "123,456,789" 66016720
```

## Commands

### Reading

| Command | Description |
|---------|-------------|
| `whoami` | Show authenticated user |
| `collections` | List all collections with IDs |
| `list [ID]` | List bookmarks (default: 0 = all) |
| `count [ID]` | Count bookmarks in collection |
| `search QUERY [ID]` | Search bookmarks |
| `get ID` | Get bookmark details |
| `tags` | List all tags with counts |
| `list-untagged [ID]` | Find bookmarks without tags |
| `cache ID` | Get permanent copy (Pro only) |

### Writing

| Command | Description |
|---------|-------------|
| `add URL [ID]` | Add bookmark (default: -1 = Unsorted) |
| `delete ID` | Delete bookmark |
| `create-collection NAME` | Create new collection |
| `move ID COLLECTION` | Move bookmark to collection |
| `update ID [opts]` | Update tags/title/collection |
| `bulk-move IDS TARGET [SOURCE]` | Move multiple bookmarks (source defaults to -1/Unsorted) |
| `suggest URL` | Get AI-suggested tags/title |

### Options

| Flag | Description |
|------|-------------|
| `--json` | Raw JSON output |
| `--limit N` | Max results (default: 25) |
| `--page N` | Pagination (0-indexed) |
| `--delay MS` | Delay between API calls (rate limiting) |
| `--token TOKEN` | Override API token |

### Update Options

For the `update` command:

| Flag | Description |
|------|-------------|
| `--tags TAG1,TAG2` | Set tags (comma-separated) |
| `--title TITLE` | Set title |
| `--collection ID` | Move to collection |

### Collection IDs

- `0` = All bookmarks
- `-1` = Unsorted
- `-99` = Trash
- `N` = Specific collection (get IDs from `collections`)

## Examples

```bash
# List unsorted with pagination
{baseDir}/scripts/raindrop.sh list -1 --limit 50 --page 0
{baseDir}/scripts/raindrop.sh list -1 --limit 50 --page 1

# Create collection
{baseDir}/scripts/raindrop.sh create-collection "AI Coding"
# Output: Created: AI Coding / ID: 66016720

# Move single bookmark
{baseDir}/scripts/raindrop.sh move 1234567 66016720

# Update bookmark with tags and move
{baseDir}/scripts/raindrop.sh update 1234567 --tags "claude-code,workflow,tips" --collection 66016720

# Bulk move with rate limiting (100ms between calls)
{baseDir}/scripts/raindrop.sh bulk-move "123,456,789,101112" 66016720 --delay 100

# Find untagged bookmarks in unsorted
{baseDir}/scripts/raindrop.sh list-untagged -1 --limit 100

# Get JSON for scripting
{baseDir}/scripts/raindrop.sh list -1 --json --limit 50 | jq '.items[]._id'

# Count unsorted bookmarks
{baseDir}/scripts/raindrop.sh count -1
```

## Bulk Operations

For large batch operations, use `bulk-move` which uses the Raindrop batch API (up to 100 items per request):

```bash
# Get IDs from unsorted
ids=$({baseDir}/scripts/raindrop.sh list -1 --json --limit 100 | jq -r '[.items[]._id] | join(",")')

# Move all to collection
{baseDir}/scripts/raindrop.sh bulk-move "$ids" 66016720
```

## Rate Limiting

Raindrop API has rate limits. For bulk operations:

1. Use `--delay 100` (100ms between calls)
2. Use `bulk-move` instead of individual `move` calls
3. Process in batches of 50-100

## Direct API

For operations not covered:

```bash
source ~/.config/raindrop.env

# Update tags
curl -X PUT "https://api.raindrop.io/rest/v1/raindrop/ID" \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"tags": ["tag1", "tag2"]}'

# Bulk update (up to 100 IDs)
curl -X PUT "https://api.raindrop.io/rest/v1/raindrops" \
  -H "Authorization: Bearer $RAINDROP_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"ids": [123, 456, 789], "collectionId": 12345}'
```

API docs: https://developer.raindrop.io/
