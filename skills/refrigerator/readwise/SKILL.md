---
name: readwise
description: Access Readwise highlights and Reader saved articles
homepage: https://readwise.io
metadata: {"clawdbot":{"emoji":"📚","requires":{"bins":["node"],"env":["READWISE_TOKEN"]},"primaryEnv":"READWISE_TOKEN"}}
---

# Readwise & Reader Skill

Access your Readwise highlights and Reader saved articles.

## Setup

Get your API token from: https://readwise.io/access_token

Set the environment variable:
```bash
export READWISE_TOKEN="your_token_here"
```

Or add to ~/.clawdbot/clawdbot.json under "env".

## Readwise (Highlights)

### List books/sources
```bash
node {baseDir}/scripts/readwise.mjs books [--limit 20]
```

### Get highlights from a book
```bash
node {baseDir}/scripts/readwise.mjs highlights [--book-id 123] [--limit 20]
```

### Search highlights
```bash
node {baseDir}/scripts/readwise.mjs search "query"
```

### Export all highlights (paginated)
```bash
node {baseDir}/scripts/readwise.mjs export [--updated-after 2024-01-01]
```

## Reader (Saved Articles)

### List documents
```bash
node {baseDir}/scripts/reader.mjs list [--location new|later|archive|feed] [--category article|book|podcast|...] [--limit 20]
```

### Get document details
```bash
node {baseDir}/scripts/reader.mjs get <document_id>
```

### Save a URL to Reader
```bash
node {baseDir}/scripts/reader.mjs save "https://example.com/article" [--location later]
```

### Search Reader
```bash
node {baseDir}/scripts/reader.mjs search "query"
```

## Notes
- Rate limits: 20 requests/minute for Readwise, varies for Reader
- All commands output JSON for easy parsing
- Use `--help` on any command for options
