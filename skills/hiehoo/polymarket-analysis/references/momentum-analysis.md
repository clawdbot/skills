# Momentum Analysis Strategy

Technical analysis on binary outcome price movements to identify directional trades.

## Indicators

### RSI (Relative Strength Index)
```
RSI = 100 - (100 / (1 + RS))
RS = Avg Gain / Avg Loss (14 periods)

Signals:
- RSI > 70: Overbought (potential YES→NO rotation)
- RSI < 30: Oversold (potential NO→YES rotation)
```

### Moving Averages
```
Short MA: 5-period (fast signal)
Long MA: 20-period (trend confirmation)

Signals:
- Short > Long: Bullish momentum
- Short < Long: Bearish momentum
- Crossover: Trend reversal signal
```

### Price Action Patterns
- **Breakout:** Price exceeds recent range with volume
- **Consolidation:** Tight range before resolution catalyst
- **Divergence:** Price vs RSI disagreement

## Data Collection

### Historical Prices
```bash
# Fetch price history via Gamma API
curl "https://gamma-api.polymarket.com/prices/{token_id}?interval=1h"
```

### Volume Analysis
- Track 24h volume changes
- Compare to 7d average
- Spike detection: Volume > 2x average

## Analysis Process

1. **Fetch 50+ intervals** (15m for short-term, 1h for swing)
2. **Calculate RSI** on YES outcome price
3. **Plot MAs** (5 and 20 period)
4. **Identify signals** (oversold/overbought, crossovers)
5. **Correlate with events** (news, resolution date)

## Signal Strength

| Signal | Strength | Action |
|--------|----------|--------|
| RSI < 30 + MA crossover up | Strong | Consider YES |
| RSI > 70 + MA crossover down | Strong | Consider NO |
| Single indicator only | Weak | Wait for confirmation |
| Divergence present | Caution | Potential reversal |

## Limitations

- Binary markets != traditional assets (bounded 0-1)
- Event-driven; technicals secondary to fundamentals
- Low liquidity distorts indicators
- Resolution date creates time decay dynamics

## Output Format

```markdown
### Momentum Analysis

**Market:** [Name]
**Current Price:** YES $X.XX | NO $X.XX
**RSI (14):** XX.X [Overbought/Oversold/Neutral]
**MA Signal:** [Bullish/Bearish/Neutral]
**Volume:** [Above/Below] average
**Confidence:** [High/Med/Low]
**Note:** [Key observation]
```
