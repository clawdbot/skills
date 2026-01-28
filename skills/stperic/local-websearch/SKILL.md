---
name: searxng
description: Search the web using a self-hosted SearXNG metasearch engine. Aggregates Google, Brave, DuckDuckGo, and more without API keys.
homepage: https://docs.searxng.org
metadata: {"moltbot":{"emoji":"🔍","requires":{"bins":["python3"],"env":["SEARXNG_URL"]}}}
---

# SearXNG Web Search

Privacy-respecting metasearch via your self-hosted SearXNG instance.

## When to use (trigger phrases)

Use this skill when the user asks:
- "search the web for..."
- "look up..." / "find information about..."
- "what is..." (when current info needed)
- "research..." / "search for..."
- "google..." (redirect to privacy-respecting search)

## Quick start

```bash
python3 ~/.clawdbot/skills/searxng/scripts/searxng_search.py "your query"
python3 ~/.clawdbot/skills/searxng/scripts/searxng_search.py "query" --count 10
python3 ~/.clawdbot/skills/searxng/scripts/searxng_search.py "query" --lang de
```

## Setup

Set `SEARXNG_URL` environment variable:
```bash
export SEARXNG_URL="http://your-searxng-host:8888"
```

## Flags

| Flag | Default | Description |
|------|---------|-------------|
| `-n`, `--count` | 5 | Results to return (1-20) |
| `-l`, `--lang` | auto | Language code (en, de, fr, es, etc.) |

## Output

Returns JSON:
```json
{
  "query": "search terms",
  "count": 5,
  "results": [
    {"title": "...", "url": "...", "description": "...", "engines": ["google", "brave"], "score": 1.5}
  ]
}
```

## Notes

- No API keys needed—SearXNG aggregates upstream engines
- Results include source engines for transparency
- Scores indicate relevance (higher = better)
- For news, add "news" to query or use `--lang` for regional results