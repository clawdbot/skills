# Whale Tracking Strategy

Monitor high-performance wallets to identify smart money movements.

## Concept

Whales = wallets with proven track record of profitable trades. Copy their positioning for edge.

## Data Sources

### Polymarket Leaderboard
```bash
curl "https://gamma-api.polymarket.com/leaderboard"
```
Returns top traders by profit, win rate, volume.

### On-Chain Analysis (Polygon)
- Polygonscan API for transaction history
- Track large position changes (>$5000)
- Monitor wallet clusters (related addresses)

## Tracking Process

### Step 1: Identify Whales

Criteria:
| Metric | Threshold |
|--------|-----------|
| Total Profit | > $50,000 |
| Win Rate | > 60% |
| Trade Count | > 100 |
| Recent Activity | < 7 days |

### Step 2: Monitor Positions

Track via API:
```bash
curl "https://gamma-api.polymarket.com/positions?user={wallet}"
```

Watch for:
- New position entries
- Position size increases
- Exit signals (selling)

### Step 3: Analyze Patterns

- Which market categories do they trade?
- Average hold time?
- Entry timing (early vs late)?
- Position sizing patterns?

## Copy-Trading Logic Types

| Type | Mechanism | Use Case |
|------|-----------|----------|
| PERCENTAGE | Copy X% of whale's position | Proportional risk |
| FIXED | Fixed dollar amount per signal | Strict risk control |
| ADAPTIVE | Scale based on whale's conviction | Optimize risk/reward |

## Signal Interpretation

**Strong Signal:**
- Multiple whales enter same market
- Large position (>10% of their portfolio)
- Early entry (>48h before resolution)

**Weak Signal:**
- Single whale, small position
- Late entry (<12h before resolution)
- Contradicting whale positions

## Risk Factors

- Whales can be wrong
- Front-running risk (others copy too)
- Delayed data = stale signals
- Wash trading / manipulation

## Output Format

```markdown
### Whale Activity Alert

**Market:** [Name]
**Whale:** [Address shortened] | Rank #XX
**Action:** [Buy/Sell] [YES/NO]
**Size:** $X,XXX (X% of their portfolio)
**Their Stats:** XX% win rate | $XXk profit
**Signal Strength:** [Strong/Medium/Weak]
**Other Whales:** [X] in same direction
```
