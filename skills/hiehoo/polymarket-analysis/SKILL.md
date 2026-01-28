---
name: polymarket-analysis
description: Analyze Polymarket prediction markets for trading edges. Pair Cost arbitrage, whale tracking, sentiment analysis, momentum signals. No execution.
version: 2.0.0
---

# Polymarket Analysis

Identify trading advantages in Polymarket prediction markets through multi-modal analysis.

**Scope:** Analysis and opportunity identification only. No trade execution.

## Modes

| Mode | Description | Reference |
|------|-------------|-----------|
| **Analyze** | One-time analysis of a market | This file |
| **Monitor** | 24/7 market monitoring via cron | `references/market-monitoring-setup.md` |

## Quick Start

### Step 1: Get Market Link
Use `AskUserQuestion` to request market URL:
```
"Please provide the Polymarket URL you want to analyze/monitor"
```

### Step 2: Extract Market ID
From URL like `polymarket.com/event/{slug}/{condition-id}`:
- Event slug: `{slug}`
- Condition ID: `{condition-id}` (for API calls)

### Step 3: Fetch Market Data
```bash
curl "https://gamma-api.polymarket.com/markets/{condition-id}"
```

### Step 4: Run Analysis or Setup Monitoring
- **Analyze:** Run multi-strategy analysis (see Core Strategies)
- **Monitor:** Setup cron job (see `references/market-monitoring-setup.md`)

## Core Strategies

| Strategy | Description | Reference |
|----------|-------------|-----------|
| Pair Cost Arbitrage | YES+NO pricing < $1.00 | `references/pair-cost-arbitrage.md` |
| Momentum Analysis | RSI, MA on binary prices | `references/momentum-analysis.md` |
| Whale Tracking | Large trade detection | `references/whale-tracking.md` |
| Sentiment | News/social aggregation | `references/sentiment-analysis.md` |

## Alert Thresholds

| Event | Threshold | Action |
|-------|-----------|--------|
| Price change | ±5% in 1h | Notify user |
| Large trade | >$5,000 single order | Whale alert |
| Pair cost drop | <$0.98 | Arbitrage opportunity |
| Volume spike | >2x 24h average | Market activity alert |

## Output Format

```markdown
## Polymarket Analysis: [Market Name]

**Market:** [URL]
**Prices:** YES $X.XX | NO $X.XX | Pair Cost: $X.XX

### Opportunities
1. [Strategy]: [Description] | Confidence: [H/M/L]

### Alerts (if monitoring)
- [Timestamp]: [Alert type] - [Details]

### Risk Assessment
- [Key risks]
```

## References

- `references/market-monitoring-setup.md` - 24/7 cron monitoring
- `references/pair-cost-arbitrage.md` - Arbitrage detection
- `references/momentum-analysis.md` - Technical analysis
- `references/whale-tracking.md` - Smart money tracking
- `references/sentiment-analysis.md` - Sentiment aggregation
- `references/polymarket-api.md` - API endpoints
