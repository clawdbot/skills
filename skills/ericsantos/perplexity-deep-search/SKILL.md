---
name: perplexity
description: "Deep search via Perplexity API. Three modes: search (quick facts), reason (complex analysis), research (in-depth reports). Returns AI-grounded answers with citations."
homepage: https://docs.perplexity.ai
metadata: {"clawdbot":{"emoji":"🔮","requires":{"bins":["curl","jq"]},"primaryEnv":"PERPLEXITY_API_KEY"}}
---

# Perplexity Deep Search

AI-powered web search with three modes for different depth levels.

## Quick Start

```bash
# Quick search (sonar) - facts, summaries, current events
{baseDir}/scripts/search.sh "latest AI news"

# Reasoning (sonar-reasoning-pro) - complex analysis, multi-step
{baseDir}/scripts/search.sh --mode reason "compare React vs Vue for enterprise apps"

# Deep Research (sonar-deep-research) - full reports, exhaustive analysis
{baseDir}/scripts/search.sh --mode research "market analysis of AI in healthcare 2025"
```

## Modes

| Mode | Model | Best For | Cost |
|------|-------|----------|------|
| `search` (default) | `sonar-pro` | Quick facts, summaries, current events | Low |
| `reason` | `sonar-reasoning-pro` | Complex analysis, comparisons, problem-solving | Medium |
| `research` | `sonar-deep-research` | In-depth reports, market analysis, literature reviews | High |

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `--mode` | `search`, `reason`, `research` | `search` |
| `--recency` | `hour`, `day`, `week`, `month` | — |
| `--domains` | Comma-separated domain filter | — |
| `--lang` | Language code (`pt`, `en`, `es`, etc.) | — |
| `--json` | Raw JSON output | off |

## Examples

```bash
# Search with recency filter
{baseDir}/scripts/search.sh --recency week "OpenAI latest announcements"

# Search restricted to specific domains
{baseDir}/scripts/search.sh --domains "arxiv.org,nature.com" "transformer architecture advances"

# Search in Portuguese
{baseDir}/scripts/search.sh --lang pt "inteligência artificial no Brasil"

# Deep research with JSON output
{baseDir}/scripts/search.sh --mode research --json "enterprise AI adoption trends"
```

## API Key

Set `PERPLEXITY_API_KEY` env var:
```bash
export PERPLEXITY_API_KEY="pplx-..."
```

## Pricing Reference

- **Search (sonar-pro):** ~$0.01/query
- **Reasoning (sonar-reasoning-pro):** ~$0.02/query
- **Deep Research (sonar-deep-research):** ~$0.40/query (uses many searches + reasoning)

Use `search` for everyday queries. Reserve `research` for when you truly need exhaustive analysis.
