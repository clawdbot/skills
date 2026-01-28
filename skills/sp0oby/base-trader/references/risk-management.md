# Risk Management

> *"Rule #1: Don't lose money. Rule #2: Don't forget Rule #1."*

## Position Sizing

### The 2% Rule
Never risk more than 2% of portfolio on a single trade.

```
Portfolio: $100
Max risk per trade: $2
If stop loss is -20%: Max position = $10
If stop loss is -10%: Max position = $20
```

### Kelly Criterion (Advanced)
```
Optimal bet size = (Win% × Avg Win - Loss% × Avg Loss) / Avg Win

Example:
- Win rate: 40%
- Average win: +50%
- Average loss: -15%

Kelly = (0.40 × 0.50 - 0.60 × 0.15) / 0.50
Kelly = (0.20 - 0.09) / 0.50 = 22%

Use half-Kelly (11%) for safety.
```

## Stop Loss Strategies

### Fixed Percentage Stop
Set stop at fixed % below entry.
- Aggressive: -10%
- Normal: -15%
- Conservative: -20%

### Support-Based Stop
Place stop just below key support level.
More precise but requires chart analysis.

### Trailing Stop
Move stop up as price rises.
```
Entry: $1.00
Price hits $1.30: Move stop to $1.10
Price hits $1.50: Move stop to $1.25
```

### Time-Based Stop
Exit if no movement after X hours/days.
Frees capital for better opportunities.

## Take Profit Strategy

### Scaled Exit (Recommended)
```
Entry: $1.00
TP1 (25%): $1.30 (+30%)
TP2 (25%): $1.50 (+50%)
TP3 (25%): $2.00 (+100%)
TP4 (25%): Let ride with trailing stop
```

### Why Scale Out?
- Locks in profits
- Reduces regret
- Keeps exposure to big moves
- Psychological benefit

## Portfolio Allocation

### Conservative
- 70% Stablecoins/ETH
- 20% Blue chips
- 10% Speculation

### Moderate
- 50% Stablecoins/ETH
- 30% Blue chips
- 20% Speculation

### Aggressive
- 30% Stablecoins/ETH
- 40% Blue chips
- 30% Speculation

## Daily/Weekly Limits

### Daily Loss Limit: -20%
If hit: Stop trading for 24 hours.

### Weekly Loss Limit: -30%
If hit: Stop trading until Monday.

### Consecutive Loss Limit: 3 trades
After 3 losses in a row: Take a break, reassess.

## Emotional Management

### FOMO (Fear of Missing Out)
- There's always another trade
- Missing a winner beats catching a loser
- If you feel FOMO, wait 10 minutes

### Revenge Trading
- After a loss, do NOT immediately trade again
- Take a 1-hour break minimum
- Losses happen; revenge makes them worse

### Overconfidence
- After big wins, reduce size
- Winners often give back gains
- Stay humble, stay sized

## Risk Checklist Before Every Trade

- [ ] Position size within limits?
- [ ] Stop loss defined?
- [ ] Take profit targets set?
- [ ] Within daily loss budget?
- [ ] Not revenge trading?
- [ ] Not FOMO buying?
- [ ] Risk:reward at least 1:2?

If any NO → Don't trade.

## Emergency Procedures

### Market Crash
1. Don't panic sell
2. Check if positions have stops
3. If no stops, assess damage
4. Decide: Hold or cut losses
5. Don't try to catch falling knives

### Rug Pull
1. Accept the loss immediately
2. Don't try to recover by trading more
3. Document what happened
4. Learn from the mistake
5. Move on

### Technical Issues
1. Don't trade if systems are failing
2. Document any failed transactions
3. Wait for systems to stabilize
4. Verify wallet state before resuming
