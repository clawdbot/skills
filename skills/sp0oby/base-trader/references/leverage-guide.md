# Leverage Trading Guide

⚠️ **HIGH RISK** — Only for experienced traders with strict risk management.

## Overview

Trade with leverage via Avantis perpetuals on Base through Bankr.

**Max Leverage:** 50x crypto, 100x forex/commodities
**Chain:** Base
**Protocol:** Avantis

## When to Use Leverage

### Good Use Cases
- High-conviction directional trades
- Short-term scalps with defined risk
- Hedging spot positions
- Trading both directions (long/short)

### Bad Use Cases
- "Making back losses" (revenge trading)
- Random entries without plan
- Holding through major events
- Using max leverage

## Commands

### Open Position
```bash
"Open a 5x long on ETH with $20"
"Short TOKEN with 3x leverage using $15"
"Long ETH 5x with stop loss at $3000"
```

### With Risk Management
```bash
"Long TOKEN 3x with SL at -15% and TP at +30%"
"5x short ETH with stop loss at $3500"
```

### View Positions
```bash
"Show my Avantis positions"
"What leverage trades do I have?"
"PnL on my ETH long"
```

### Close Positions
```bash
"Close my ETH long"
"Exit all Avantis positions"
"Close 50% of my TOKEN short"
```

## Leverage Guidelines

| Risk Level | Leverage | Position Size | Use Case |
|------------|----------|---------------|----------|
| Conservative | 2-3x | Max $20 | Learning |
| Moderate | 3-5x | Max $30 | Swing trades |
| Aggressive | 5-10x | Max $20 | Scalping |
| DO NOT USE | >10x | — | Too risky |

## Liquidation Math

**Long position liquidation:**
```
Liquidation Price = Entry × (1 - 1/leverage)

Example: 5x long ETH at $3000
Liquidation = $3000 × (1 - 1/5) = $3000 × 0.8 = $2400
(-20% move = total loss)
```

**Short position liquidation:**
```
Liquidation Price = Entry × (1 + 1/leverage)

Example: 5x short ETH at $3000  
Liquidation = $3000 × (1 + 1/5) = $3000 × 1.2 = $3600
(+20% move = total loss)
```

## Risk Rules for Base Trader

### Position Sizing
- Max $30 per leveraged trade
- Max 1-2 leverage trades at a time
- Never more than 10% of portfolio in leverage

### Stop Losses (MANDATORY)
- Always set before entry
- Max -20% of collateral
- Never move stop further away
- Accept the loss when hit

### Take Profits
- Set 2:1 or 3:1 reward:risk minimum
- Scale out: 50% at first target, 50% at second
- Don't be greedy

## Example Trade

```
Portfolio: $100
Leverage trade budget: $10 (10%)

Trade: 5x long ETH at $3000
- Collateral: $10
- Position size: $50 effective
- Stop loss: $2850 (-5% from entry, -25% to collateral)
- Take profit: $3150 (+5% from entry, +25% to collateral)

Risk: $2.50 (25% of $10)
Reward: $2.50 (25% of $10)
R:R = 1:1 (minimum acceptable)
```

## Common Mistakes

1. **No stop loss** → Liquidation
2. **Too much leverage** → Liquidation on small moves
3. **Too large position** → Account blow-up
4. **Holding through news** → Volatile wicks
5. **Revenge trading** → Emotional losses
6. **Moving stop loss** → Larger losses

## When NOT to Trade Leverage

- After a losing streak
- During major news events
- When emotional/tired
- Without a clear plan
- When already have max positions
- In choppy/ranging markets

## Best Practices

1. Paper trade first
2. Start with 2-3x only
3. Use tiny amounts ($10-20)
4. Always have stop loss
5. Take profits, don't hold forever
6. Keep leverage journal
7. Review and learn from every trade

---

**Remember:** Most leverage traders lose money. The edge is in risk management, not prediction. Small losses, occasional big wins.
