---
name: clinkding
description: Manage linkding bookmarks - save URLs, search, tag, organize, and retrieve your personal bookmark collection. Use when the user wants to save links, search bookmarks, manage tags, or organize their reading list.
homepage: https://github.com/daveonkels/clinkding
metadata: {"clawdis":{"emoji":"🔖","requires":{"bins":["clinkding"]},"install":[{"id":"homebrew","kind":"brew","formula":"daveonkels/tap/clinkding","bins":["clinkding"],"label":"Install clinkding (Homebrew)"},{"id":"go","kind":"go","module":"github.com/daveonkels/clinkding@latest","bins":["clinkding"],"label":"Install clinkding (Go)"}]}}
---

# clinkding - Linkding Bookmark Manager CLI

A modern Go-based CLI for managing bookmarks in [linkding](https://github.com/sissbruecker/linkding), a self-hosted bookmark manager.

## What This Does

**Linkding** is a self-hosted bookmark manager (like Pocket, Instapaper). **clinkding** is the CLI that lets you manage your bookmarks from the terminal or via AI agents.

Think of it as:
- **Save for later** - Capture URLs you want to read
- **Searchable library** - Full-text search across titles, descriptions, tags
- **Organized collections** - Tag and bundle related bookmarks
- **Personal archive** - Keep important links with notes and metadata

## Quick Start

### Initial Setup

```bash
# Interactive configuration
clinkding config init

# Or manually configure
clinkding config set url https://your-linkding-instance.com
clinkding config set token YOUR_API_TOKEN

# Test connection
clinkding config test
```

### Configuration File

Location: `~/.config/clinkding/config.yaml`

```yaml
url: https://linkding.example.com
token: your-api-token-here

defaults:
  bookmark_limit: 100
  output_format: auto
```

### Environment Variables

```bash
export LINKDING_URL="https://linkding.example.com"
export LINKDING_TOKEN="your-api-token-here"
```

## Core Commands

### Bookmarks

#### List & Search

```bash
# List recent bookmarks
clinkding bookmarks list

# Search by keyword
clinkding bookmarks list --query "golang tutorial"

# Filter by tag
clinkding bookmarks list --query "tag:programming"

# Recent bookmarks (last 7 days)
clinkding bookmarks list --added-since "7d"

# Unread bookmarks
clinkding bookmarks list --query "unread:yes"

# JSON output for scripting
clinkding bookmarks list --json

# Plain text (tab-separated)
clinkding bookmarks list --plain
```

#### Create Bookmarks

```bash
# Simple bookmark
clinkding bookmarks create https://go.dev

# With metadata
clinkding bookmarks create https://go.dev \
  --title "Go Programming Language" \
  --tags "golang,programming,reference" \
  --description "Official Go website" \
  --unread

# Check if URL already exists before creating
clinkding bookmarks check https://go.dev
```

#### Update Bookmarks

```bash
# Update title
clinkding bookmarks update 42 --title "New Title"

# Add tags
clinkding bookmarks update 42 --add-tags "important,work"

# Remove tags
clinkding bookmarks update 42 --remove-tags "old-tag"

# Mark as read
clinkding bookmarks update 42 --read

# Update description
clinkding bookmarks update 42 --description "Updated notes"
```

#### Get Bookmark Details

```bash
# Full details
clinkding bookmarks get 42

# JSON output
clinkding bookmarks get 42 --json
```

#### Archive & Delete

```bash
# Archive (hide from main list)
clinkding bookmarks archive 42

# Unarchive
clinkding bookmarks unarchive 42

# Delete permanently
clinkding bookmarks delete 42
```

### Tags

```bash
# List all tags
clinkding tags list

# Create a tag
clinkding tags create "golang"

# Get tag details
clinkding tags get 1

# Plain text output
clinkding tags list --plain
```

### Bundles

Bundles are collections of related bookmarks.

```bash
# List bundles
clinkding bundles list

# Create a bundle
clinkding bundles create "Go Resources" \
  --description "Everything related to Go programming"

# Update a bundle
clinkding bundles update 1 --name "Go Lang Resources"

# Get bundle details
clinkding bundles get 1

# Delete a bundle
clinkding bundles delete 1
```

### Assets

Upload and manage file attachments for bookmarks.

```bash
# List assets for a bookmark
clinkding assets list 42

# Upload a file
clinkding assets upload 42 ~/Documents/screenshot.png

# Download an asset
clinkding assets download 42 1 -o ./downloaded-file.png

# Delete an asset
clinkding assets delete 42 1
```

### User Profile

```bash
# Get user profile info
clinkding user profile
```

## Agent Usage Patterns

### Save URL from Conversation

```bash
# User: "Save this for later: https://example.com"
clinkding bookmarks create https://example.com \
  --title "Article Title" \
  --description "Context from conversation" \
  --tags "topic,context"
```

### Search Bookmarks

```bash
# User: "Find my golang bookmarks"
clinkding bookmarks list --query "golang"

# User: "Show me unread programming articles"
clinkding bookmarks list --query "tag:programming unread:yes"

# User: "What did I save last week?"
clinkding bookmarks list --added-since "7d"
```

### Organize & Tag

```bash
# User: "Tag bookmark 42 as important"
clinkding bookmarks update 42 --add-tags "important"

# User: "Create a bundle for my AI research links"
clinkding bundles create "AI Research" \
  --description "Machine learning and AI papers"
```

### Retrieve for Reading

```bash
# User: "Give me something to read"
clinkding bookmarks list --query "unread:yes" --limit 5

# User: "Show me my golang tutorials"
clinkding bookmarks list --query "tag:golang tag:tutorial"
```

## Output Formats

### Auto (Default)
Human-friendly tables and colors for terminal display.

### JSON
```bash
clinkding bookmarks list --json
```
Machine-readable for scripting and agent parsing.

### Plain Text
```bash
clinkding bookmarks list --plain
```
Tab-separated values for pipe-friendly parsing.

## Relative Date Filtering

Supports human-friendly time ranges:

```bash
# Last 24 hours
clinkding bookmarks list --added-since "24h"

# Last 7 days
clinkding bookmarks list --added-since "7d"

# Last 6 months
clinkding bookmarks list --modified-since "180d"
```

**Supported units:** `h` (hours), `d` (days), `y` (years)

## Common Workflows

### Morning Reading Routine

```bash
# Check unread bookmarks
clinkding bookmarks list --query "unread:yes"

# Get top 5 most recent
clinkding bookmarks list --limit 5
```

### Save from Clipboard

```bash
# macOS
pbpaste | xargs -I {} clinkding bookmarks create {}

# Linux
xclip -o | xargs -I {} clinkding bookmarks create {}
```

### Batch Operations

```bash
# Tag multiple bookmarks
for id in 42 43 44; do
  clinkding bookmarks update $id --add-tags "important"
done

# Archive old unread bookmarks
clinkding bookmarks list --query "unread:yes" --added-since "30d" --plain | \
  while read id _; do
    clinkding bookmarks archive "$id"
  done
```

### Backup Bookmarks

```bash
# Export all bookmarks as JSON
clinkding bookmarks list --json > bookmarks-backup-$(date +%Y%m%d).json

# Export specific tag
clinkding bookmarks list --query "tag:important" --json > important.json
```

## Global Flags

Available on all commands:

| Flag | Description |
|------|-------------|
| `-c, --config <file>` | Config file path |
| `-u, --url <url>` | Linkding instance URL |
| `-t, --token <token>` | API token |
| `--json` | Output as JSON |
| `--plain` | Output as plain text |
| `--no-color` | Disable colors |
| `-q, --quiet` | Minimal output |
| `-v, --verbose` | Verbose output |

## Exit Codes

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | General error (API/network) |
| 2 | Invalid usage (bad flags/args) |
| 3 | Authentication error |
| 4 | Not found |
| 130 | Interrupted (Ctrl-C) |

## Troubleshooting

### Test Configuration

```bash
# Verify settings
clinkding config show

# Test connection
clinkding config test
```

### Common Issues

**Authentication Error:**
- Verify API token in linkding web interface
- Check URL includes protocol (`https://`)
- Remove trailing slashes from URL

**Command-Specific Help:**
```bash
clinkding bookmarks --help
clinkding bookmarks create --help
```

## Links

- **GitHub:** https://github.com/daveonkels/clinkding
- **Linkding:** https://github.com/sissbruecker/linkding
- **Homebrew:** `brew install daveonkels/tap/clinkding`

## Installation

### Homebrew (macOS/Linux)

```bash
brew install daveonkels/tap/clinkding
```

### Go Install

```bash
go install github.com/daveonkels/clinkding@latest
```

### Binary Download

Download from [releases](https://github.com/daveonkels/clinkding/releases) for your platform.

## Shell Completion

```bash
# Bash
clinkding completion bash > /etc/bash_completion.d/clinkding

# Zsh
clinkding completion zsh > "${fpath[1]}/_clinkding"

# Fish
clinkding completion fish > ~/.config/fish/completions/clinkding.fish
```

---

**Built by:** [@daveonkels](https://github.com/daveonkels)  
**License:** MIT

## Agent Workflows for Smart Bookmark Creation

### Adding URLs with Automatic Metadata

When a user says "Add this to linkding" or "Save this URL", follow this workflow:

**1. Extract metadata from the URL**

Use the `summarize` skill to get title and description:

```bash
# Get page metadata
summarize url https://example.com --format json
```

This returns structured data with:
- Title
- Description/summary
- Main content

**2. Infer appropriate tags from content**

Map the content to **existing canonical tags only**. Do NOT create new tags.

Use this canonical tag list (263 tags total):
- **Tech:** webdev, design, programming, ai, cloud, devops, docker, linux, networking, security, privacy
- **Content:** content, media, photography, video, audio, books, podcasting
- **Business:** business, marketing, ecommerce, finance, career, productivity
- **Home:** smart-home, home-assistant, esphome, iot, home-improvement
- **Tools:** tools, cli, git, github, editor, reference, documentation
- **Data:** data, analytics, mysql, nosql
- **Communication:** communication, email, messaging, slack
- **Education:** education, guide, howto, research, testing
- **Locations:** texas, seattle, dallas (use sparingly)

**Tag Selection Rules:**
- Use 2-5 tags maximum
- Choose the most specific applicable tags
- If unsure, default to broader categories (e.g., `tools` over `generator`)
- Check existing tags first: `clinkding tags list --plain | grep -i <keyword>`
- Never create tags like: `awesome`, `cool`, `interesting`, `resources`, `tips`

**3. Create the bookmark with metadata**

```bash
clinkding bookmarks create "https://example.com" \
  --title "Title from summarize" \
  --description "Summary from summarize (1-2 sentences)" \
  --tags "webdev,tools,reference"
```

### Example Workflow

**User:** "Save this to linkding: https://github.com/awesome/project"

**Agent Actions:**

```bash
# 1. Check if already bookmarked
clinkding bookmarks check https://github.com/awesome/project

# 2. Get metadata (use summarize skill)
summarize url https://github.com/awesome/project --format json

# 3. Analyze content and infer tags
# From summary: "A CLI tool for Docker container management"
# Canonical tags: docker, devops, cli, tools

# 4. Create bookmark
clinkding bookmarks create https://github.com/awesome/project \
  --title "Awesome Project - Docker Container CLI" \
  --description "Command-line tool for managing Docker containers with enhanced features" \
  --tags "docker,devops,cli"
```

### Tag Mapping Heuristics

Use these rules to map content → canonical tags:

| Content Type | Canonical Tags |
|--------------|----------------|
| Web development, HTML, CSS, JavaScript | `webdev`, `css`, `javascript` |
| React, frameworks, frontend | `webdev`, `react` |
| Design, UI/UX, mockups | `design` |
| Python, Go, Ruby code | `programming`, `python`/`ruby` |
| Docker, K8s, DevOps | `docker`, `devops`, `cloud` |
| Home automation, ESP32, sensors | `smart-home`, `esphome`, `iot` |
| AI, ML, LLMs | `ai`, `llm` |
| Productivity tools, workflows | `productivity`, `tools` |
| Finance, investing, crypto | `finance` |
| Marketing, SEO, ads | `marketing` |
| Shopping, deals, stores | `ecommerce` |
| Tutorials, guides, docs | `guide`, `howto`, `documentation` |
| Security, privacy, encryption | `security`, `privacy` |
| Local (DFW/Seattle) | `texas`, `seattle` |

### Validation Before Creating

Always run these checks:

```bash
# 1. Does URL already exist?
clinkding bookmarks check <url>

# 2. Do the tags exist?
clinkding tags list --plain | grep -iE "^(tag1|tag2|tag3)$"

# 3. Are we using canonical tags?
# Cross-reference against the 263 canonical tags
# Never create new tags without explicit user request
```

### User Requests to Save Multiple Links

If user provides multiple URLs:

```bash
# Process each URL separately with metadata extraction
for url in url1 url2 url3; do
  # Get metadata
  # Infer tags
  # Create bookmark
done
```

### Updating Existing Bookmarks

If user says "Update that bookmark" or "Add tags to my last save":

```bash
# Get most recent bookmark
recent_id=$(clinkding bookmarks list --limit 1 --plain | cut -f1)

# Add tags (don't remove existing ones unless asked)
clinkding bookmarks update $recent_id --add-tags "new-tag"

# Update description
clinkding bookmarks update $recent_id --description "Updated notes"
```

### Key Principles

1. **Always fetch metadata** - Use `summarize` to get good titles/descriptions
2. **Use existing tags** - Never create new tags without checking canonical list
3. **Be selective** - 2-5 tags max, choose the most specific applicable
4. **Validate first** - Check for duplicates before creating
5. **Provide context** - Include brief description explaining why it's useful

---

## Current Canonical Tag Structure

Dave's linkding instance has **263 canonical tags** after consolidation from 17,189 duplicates.

Top categories (by bookmark count):
- `pinboard` (4,987) - Legacy import tag
- `ifttt` (2,639) - Legacy import tag  
- `webdev` (1,679) - Web development
- `design` (561) - Design/UI/UX
- `content` (416) - Content/writing
- `cloud` (383) - Cloud/hosting/SaaS
- `business` (364) - Business/strategy
- `ecommerce` (308) - Shopping/marketplace
- `smart-home` (295) - Home automation
- `productivity` (291) - Productivity tools

**Golden Rule:** When in doubt, use broader existing tags rather than creating new specific ones.

