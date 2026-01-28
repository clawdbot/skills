# Launch Sniping Guide

> *High risk, high reward. Most launches fail. Size accordingly.*

## What Is Launch Sniping

Buying tokens very early (minutes to hours) after launch to capture initial price appreciation.

## Why It Works (Sometimes)

- Early liquidity is thin → small buys move price
- Genuine projects often 5-10x from launch
- FOMO cycle attracts more buyers
- First-mover advantage is real

## Why It Fails (Often)

- 90%+ of launches are scams/rugs
- Honeypots trap buyers
- Dev dumps immediately
- No real utility or community
- Liquidity pulled

## Risk Management

### Position Sizing
```
Max per snipe: $20
Max snipes per day: 3
Total daily snipe risk: $60
```

### Expected Outcomes
- 8 out of 10 snipes: Lose 50-100%
- 1 out of 10 snipes: Break even or small profit
- 1 out of 10 snipes: 5-20x gain

The winners must pay for the losers.

## Finding Launches

### Methods
1. **Bankr Trending**: "What tokens are trending on Base?"
2. **CT (Crypto Twitter)**: Follow alpha callers
3. **Telegram Groups**: Launch announcement channels
4. **On-chain Monitoring**: Watch deployer addresses

### Red Flags to Skip
- Team fully anonymous, no track record
- No liquidity lock
- Excessive taxes (>5%)
- Copy-paste contract
- No website/social presence
- Promises of guaranteed gains

## 60-Second Analysis

When you find a potential snipe, you have ~60 seconds:

### Second 0-20: Contract Check
```bash
# Is contract verified?
# Check Basescan: https://basescan.org/address/CONTRACT
```

### Second 20-40: Liquidity Check
```bash
"What's the liquidity for TOKEN on Base?"
# Need > $5k minimum
# Prefer > $10k
```

### Second 40-50: Quick Social Check
- Telegram exists and active?
- Twitter account?
- Website?

### Second 50-60: Decision
- All green? → Snipe with $15-20
- Any red flags? → Skip
- Unsure? → Skip (plenty more launches)

## Execution

### Entry
```bash
"Buy $20 of TOKEN on Base"
```

### Immediate Actions
1. Verify you can sell (small test if unsure)
2. Set mental stop at -50%
3. Set alert at 2x

### Exit Strategy
```
At 2x: Sell 50% → Recovered cost
At 5x: Sell remaining or trail
At -50%: Cut loss, no questions
```

## Post-Trade

### If Winner
- Log the trade
- Note what made it work
- Don't get overconfident
- Stick to position sizes

### If Loser
- Log the trade
- Note what went wrong
- Don't revenge trade
- Move on immediately

## Example Snipe Flow

```
1. See "New token FOREST launching on Base" on CT
2. Check contract: Verified ✓
3. Check liquidity: $15k ✓
4. Check: Can sell? Quick look at recent txs ✓
5. Check: Telegram? Active, 200 members ✓
6. Decision: Green lights → Execute

7. "Buy $20 of FOREST on Base"
8. Log: ./scripts/log-trade.sh "BUY" "FOREST" "20" "0.0001" "launch snipe" "0x..."

9. Monitor:
   - At 2x ($0.0002): "Sell 50% of my FOREST"
   - Trail rest with mental stop at entry
   - At 5x or stop: Exit remainder

10. Log exit and calculate P&L
```

## Common Mistakes

1. **Oversizing**: Putting too much into one snipe
2. **FOMO**: Buying after 5x already happened
3. **No Stop**: Hoping a loser recovers
4. **Revenge**: Immediately sniping after a loss
5. **Overtrading**: Taking every launch instead of selecting

## Mental Game

- Accept most snipes will lose
- Focus on process, not outcomes
- One big winner covers many losers
- Patience > aggression
- Skip more than you take
