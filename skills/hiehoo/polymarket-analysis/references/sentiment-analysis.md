# Sentiment Analysis Strategy

Aggregate sentiment from multiple sources to anticipate market movements.

## Data Sources

| Source | Type | Use Case |
|--------|------|----------|
| X/Twitter | Social | Real-time sentiment, breaking news |
| News APIs | Media | Institutional coverage, announcements |
| On-Chain | Flow | Liquidity movements, whale activity |
| Google Trends | Search | Public interest proxy |

## Collection Process

### Twitter/X Sentiment
```
Search queries:
- "[Market topic] polymarket"
- "$[relevant ticker]"
- Key influencer accounts

Analyze:
- Volume of mentions (spike detection)
- Sentiment polarity (positive/negative/neutral)
- Influencer positioning
```

### News Aggregation
```
Sources:
- CoinDesk, CoinTelegraph (crypto)
- Reuters, Bloomberg (macro)
- Polymarket blog/announcements

Track:
- Headlines mentioning market topic
- Institutional announcements
- Regulatory news
```

### On-Chain Flow
```
Monitor:
- Large USDC inflows to Polymarket
- Position concentration changes
- New wallet activity spikes
```

## Sentiment Scoring

```
Score Range: -100 to +100

+100: Extreme bullish (YES favored)
+50: Moderately bullish
0: Neutral
-50: Moderately bearish
-100: Extreme bearish (NO favored)
```

### Scoring Factors

| Factor | Weight | Signal |
|--------|--------|--------|
| News sentiment | 30% | Headlines tone |
| Social volume | 25% | Mention spike |
| Influencer bias | 20% | Key account positions |
| On-chain flow | 25% | Money movement |

## Timing Considerations

**Session Volatility:**
- Asia/Europe transition: High volatility
- US market open: News catalyst
- Weekend: Lower liquidity, higher spreads

**Event-Driven:**
- Pre-announcement: Sentiment builds
- Post-announcement: Rapid price adjustment
- Resolution approach: Sentiment converges to outcome

## Contrarian Signals

When to fade sentiment:
- Extreme readings (>80 or <-80)
- Sentiment/price divergence
- "Everyone agrees" scenarios
- Late-stage hype

## Output Format

```markdown
### Sentiment Analysis

**Market:** [Name]
**Overall Score:** XX/100 [Bullish/Bearish/Neutral]

**Breakdown:**
- News: [XX] - [Key headline]
- Social: [XX] - [Volume trend]
- On-Chain: [XX] - [Flow direction]

**Key Catalysts:**
- [Upcoming event/date]
- [Relevant news item]

**Confidence:** [High/Med/Low]
**Contrarian Alert:** [Yes/No] - [Reason if yes]
```
