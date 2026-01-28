---
name: serpapi
description: Search Google via SerpAPI (Google Search, Google News, Google Local). Use when you need to search the web, find news articles, or look up local businesses. Supports country/language targeting for region-specific results.
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["curl","python3"],"env":["SERPAPI_API_KEY"]},"primaryEnv":"SERPAPI_API_KEY"}}
---

# SerpAPI Search

Search Google via SerpAPI with country/language targeting.

## Quick start

```bash
# Google Search
{baseDir}/scripts/search.sh "artificial intelligence B2B" --country br --lang pt

# Google News
{baseDir}/scripts/search.sh "inteligência artificial" --engine google_news --country br --lang pt

# Google Local
{baseDir}/scripts/search.sh "AI companies" --engine google_local --country us --location "San Francisco, California"
```

## Engines

| Engine | Use case | Key results field |
|--------|----------|-------------------|
| `google` | Web search (default) | `organic_results` |
| `google_news` | News articles | `news_results` |
| `google_local` | Local businesses/places | `local_results` |

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--engine` | `google`, `google_news`, `google_local` | `google` |
| `--country` | 2-letter country code (`br`, `us`, `de`, etc.) | `us` |
| `--lang` | Language code (`pt`, `en`, `es`, etc.) | `en` |
| `--location` | Location string (e.g. `"São Paulo, Brazil"`) | — |
| `--num` | Number of results | `10` |
| `--json` | Raw JSON output | off |

## API key

Set `SERPAPI_API_KEY` env var, or store it:
```bash
mkdir -p ~/.config/serpapi
echo "your_key_here" > ~/.config/serpapi/api_key
chmod 600 ~/.config/serpapi/api_key
```

## Common country codes

`br` (Brazil), `us` (USA), `pt` (Portugal), `de` (Germany), `fr` (France), `es` (Spain), `gb` (UK), `jp` (Japan), `in` (India).
