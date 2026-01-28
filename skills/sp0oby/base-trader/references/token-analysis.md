# Token Analysis Framework

## Quick Safety Check (< 60 seconds)

### 1. Contract Verification
```bash
# Check on Basescan
https://basescan.org/address/TOKEN_ADDRESS#code
```
✓ Source code visible = Good
✗ Unverified = RED FLAG

### 2. Honeypot Check
Try a small test sell or use honeypot checkers:
- Can you actually sell?
- What's the sell tax?
- Any max transaction limits?

### 3. Liquidity Check
```bash
"What's the liquidity for TOKEN on Base?"
```
- < $5k = Very dangerous
- $5k-$20k = High risk
- $20k-$100k = Medium risk
- > $100k = Lower risk

### 4. Holder Distribution
- Top holder owns > 50%? = RED FLAG
- Team wallet unlocked? = CAUTION
- Many small holders? = Good sign

## Deep Analysis (5-10 minutes)

### Contract Red Flags
- `setFee` function (can change tax)
- `blacklist` function (can block sells)
- Proxy contract (can change logic)
- Mint function without cap
- Owner can pause trading

### Liquidity Analysis
- Is LP locked? For how long?
- Initial liquidity amount
- LP token holder distribution
- Any large LP removals in history?

### Social Signals
- Active Telegram/Discord?
- Team doxxed or anonymous?
- Organic engagement or bots?
- What are influencers saying?

### On-Chain Activity
- Number of holders growing?
- Buy/sell ratio
- Whale movements
- DEX volume trend

## Token Categories

### Blue Chip (Safest)
- ETH, USDC, established tokens
- High liquidity, battle-tested
- Suitable for larger positions

### Mid Cap
- $1M-$100M market cap
- Some track record
- Medium position sizes

### Small Cap / New Launches
- < $1M market cap
- High risk, high reward
- Tiny position sizes only

### Memecoins
- Pure speculation
- 95% go to zero
- Only gamble what you can lose

## Analysis Shortcuts via Bankr

```bash
# Price and basic info
"What's the price of TOKEN on Base?"

# Technical analysis
"Do technical analysis on TOKEN"

# Trending tokens (find opportunities)
"What tokens are trending on Base?"

# Compare tokens
"Compare TOKEN1 vs TOKEN2 on Base"
```

## Decision Matrix

| Factor | Weight | Score (1-5) |
|--------|--------|-------------|
| Contract verified | 20% | |
| Liquidity adequate | 20% | |
| Can sell (not honeypot) | 20% | |
| Team/community trust | 15% | |
| Price action healthy | 15% | |
| Risk:reward ratio | 10% | |

**Total score:**
- 4.0+ = Consider trading
- 3.0-4.0 = Proceed with caution
- < 3.0 = Skip
