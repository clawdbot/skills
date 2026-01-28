---
name: aluvia-brave-search
description: Web search and content extraction via Brave Search API, with unblockable access using Aluvia mobile proxy. Use for searching documentation, facts, or any web content. No browser required; bypasses blocks and CAPTCHAs.
---

# Aluvia Brave Search

Headless web search and content extraction using Brave Search, with unblockable access via Aluvia mobile proxy. No browser required; bypasses blocks and CAPTCHAs.

## Setup

Run once before first use:

```bash
cd ~/Projects/agent-scripts/skills/aluvia-brave-search
npm ci
```

# Set your API keys (required for all features):

export ALUVIA_API_KEY=your_aluvia_key
export BRAVE_API_KEY=your_brave_key

# Optional: reuse a specific Aluvia connection

export ALUVIA_CONNECTION_ID=your_connection_id

Both `ALUVIA_API_KEY` and `BRAVE_API_KEY` are required. If `ALUVIA_CONNECTION_ID` is set, it will be used to reuse an existing Aluvia connection for proxying requests.

## Search

```bash
./search.js "query"                    # Basic search (5 results)
./search.js "query" -n 10              # More results
./search.js "query" --content          # Include page content as markdown
./search.js "query" -n 3 --content     # Combined
```

## Extract Page Content

```bash
./content.js https://example.com/article
```

Fetches a URL and extracts readable content as markdown.

## Output Format

```
--- Result 1 ---
Title: Page Title
Link: https://example.com/page
Snippet: Description from search results
Content: (if --content flag used)
  Markdown content extracted from the page...

--- Result 2 ---
...
```

## When to Use

- Searching for documentation or API references
- Looking up facts or current information
- Fetching content from specific URLs
- Any task requiring web search without interactive browsing
