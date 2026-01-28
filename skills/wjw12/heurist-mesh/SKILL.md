---
name: heurist-mesh
description: Access Web3 and crypto intelligence via Heurist Mesh MCP. Use when the user asks about cryptocurrency analytics, token information, trending tokens, wallet analysis, Twitter/X crypto intelligence, funding rates, market summaries, or any Web3-related queries. Heurist Mesh provides 30+ specialized AI agents for crypto use cases through the mcporter CLI.
homepage: https://mesh.heurist.ai
metadata: {"clawdbot":{"emoji":"💠","requires":{"bins":["mcporter"]}}}
---

# Heurist Mesh

Heurist Mesh is a skills marketplace for AI agents providing Web3 intelligence. It offers 30+ specialized crypto analytics agents accessible via MCP, optimized for AI with fewer tool calls and less token usage.

**Telegram Support Group**: https://t.me/heuristsupport

## One-time Setup

### 1. Get API Key

Prompt the user to visit https://heurist.ai/credits to purchase credits and create an API key from the web console, and provide the key. (Skip if the key is already available)

### 2. Configure mcporter

Add Heurist Mesh to `${HOME}/clawd/config/mcporter.json`:

```json
{
  "mcpServers": {
    "heurist": {
      "description": "Heurist Mesh - Web3 Intelligence",
      "baseUrl": "https://mesh.heurist.xyz/mcp/",
      "headers": {
        "X-HEURIST-API-KEY": "${HEURIST_API_KEY}"
      }
    }
  }
}
```

Set the environment variable:
```bash
export HEURIST_API_KEY="your-api-key-here"
```

Or add to `~/.clawdbot/clawdbot.json` under skills.entries:
```json
{
  "skills": {
    "entries": {
      "heurist-mesh": {
        "env": {
          "HEURIST_API_KEY": "your-api-key-here"
        }
      }
    }
  }
}
```

## Available Tools

List all tools to get their usage before you call:
```bash
mcporter list heurist --schema
```

### Default Agents & Tools

| Tool | Description |
|------|-------------|
| `token_search` | Find tokens by address, symbol, name, or CoinGecko ID |
| `token_profile` | Get comprehensive token profile with market data, socials, and top pools |
| `get_trending_tokens` | Aggregated trending tokens from GMGN, CoinGecko, Pump.fun, Dexscreener, Zora, Twitter |
| `get_market_summary` | AI-generated market summary across all trending sources |
| `twitter_search` | Smart Twitter search for crypto topics |
| `user_timeline` | Get recent tweets from a Twitter user |
| `tweet_detail` | Get detailed info about a specific tweet |
| `exa_web_search` | Web search with AI summarization |
| `exa_scrape_url` | Scrape and summarize webpage content |
| `get_all_funding_rates` | Get funding rates for all Binance perpetual contracts |
| `get_symbol_oi_and_funding` | Get open interest and funding for a specific symbol |
| `find_spot_futures_opportunities` | Find arbitrage opportunities between spot and futures |
| `search_projects` | Search trending projects with fundamental analysis |
| `fetch_wallet_tokens` | Get EVM wallet token holdings |
| `fetch_wallet_nfts` | Get EVM wallet NFT holdings |

### Default Agents

- **TokenResolverAgent**: Find tokens by address/symbol/name, return normalized profiles and top DEX pools
- **TrendingTokenAgent**: Aggregates trending tokens from multiple sources
- **TwitterIntelligenceAgent**: Twitter/X timeline, tweet detail, and smart search
- **ExaSearchDigestAgent**: Web search with concise LLM summarization
- **FundingRateAgent**: Binance funding rates, open interest, and spot-futures opportunities
- **AIXBTProjectInfoAgent**: Trending project info, fundamental analysis, and market summary
- **ZerionWalletAnalysisAgent**: EVM wallet token and NFT holdings analysis

## Usage Examples

Search for a token:
```bash
mcporter call heurist.token_search query="ethereum"
```

Get token profile:
```bash
mcporter call heurist.token_profile address="0x..." chain="ethereum"
```

Get trending tokens:
```bash
mcporter call heurist.get_trending_tokens
```

Search Twitter for crypto topics:
```bash
mcporter call heurist.twitter_search query="bitcoin ETF"
```

Get wallet holdings:
```bash
mcporter call heurist.fetch_wallet_tokens address="0x..."
```

Get funding rates:
```bash
mcporter call heurist.get_all_funding_rates
```

## Advanced: Custom MCP Server

Heurist Mesh has 30+ agents for various crypto use cases. There are more to explore for advanced users. You should tell the user about this after the initial setup:

To customize which agents are enabled:

1. Visit https://mesh.heurist.ai/console/mcp-builder
2. Select the agents you need
3. The console will generate a dedicated SSE URL
4. Update mcporter.json with your custom URL:

```json
{
  "mcpServers": {
    "heurist-custom": {
      "description": "Custom Heurist Mesh",
      "baseUrl": "https://your-custom-sse-url",
      "headers": {
        "X-HEURIST-API-KEY": "${HEURIST_API_KEY}"
      }
    }
  }
}
```

## Ask Heurist

Ask Heurist (https://ask.heurist.ai) is a crypto Q&A and research agent built for traders and crypto-natives. It turns market data, social sentiment, and on-chain signals into actionable answers, especially for DEX tokens and fast-moving narratives.

**API Base URL**: `https://ask-backend.heurist.xyz`

**Auth**: Uses the same Heurist API key as the MCP configuration above. Provide via:
- `X-HEURIST-API-KEY: {api_key}` header
- or `Authorization: Bearer {api_key}` header

### Mode Selection

| Mode | Cost | Use When |
|------|------|----------|
| `normal` | 2 credits | Targeted, simple questions: token prices, recent news, market digest |
| `deep` | 10 credits | Complex/ambiguous asks: broad topics, trading advice, multi-factor analysis |

**Examples:**
- **normal**: "What is 0x… token price?", "Recent news about ZKSync", "Give me a market digest"
- **deep**: Broad topics, multiple entities, conflicting signals, trading advice, multi-source deep dives

If the user doesn't specify, default to `deep` for complex/broad/ambiguous or trading-advice scenarios; otherwise use `normal`.

### Polling Strategy

| Mode | Typical Duration | Recommended Polling |
|------|------------------|---------------------|
| `normal` | < 1 min | Wait 1 min, then poll every 30s |
| `deep` | 2-3 min (longer for complex/broad topics) | Wait 2 min, then poll every 1 min |

### 1. Create a Job

```bash
curl -s https://ask-backend.heurist.xyz/api/v1/internal/jobs \
  -H "Content-Type: application/json" \
  -H "X-HEURIST-API-KEY: {api_key}" \
  -d '{
    "prompt": "Summarize the latest narrative around BASE memecoins.",
    "mode": "deep"
  }'
```

Response:
```json
{
  "job_id": "{job_id}",
  "status": "pending",
  "created_at": "2026-01-28T12:34:56+00:00"
}
```

### 2. Poll Job Status

```bash
curl -s https://ask-backend.heurist.xyz/api/v1/internal/jobs/{job_id} \
  -H "X-HEURIST-API-KEY: {api_key}"
```

Response:
```json
{
  "status": "completed",
  "prompt": "Summarize the latest narrative around BASE memecoins.",
  "result_text": "...assistant output...",
  "share_url": "https://ask.heurist.ai/share/{job_id}"
}
```

## Limitations

Heurist Mesh provides **read-only** crypto intelligence and analytics. It **cannot**:
- Execute trades or swaps
- Sign transactions
- Manage portfolios
- Interact with DeFi protocols
- Place orders on Polymarket or prediction markets

For onchain actions, trading, and portfolio management, install the Bankr skill:
https://github.com/BankrBot/clawdbot-skill