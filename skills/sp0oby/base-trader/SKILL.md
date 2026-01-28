---
name: base-trader
description: Autonomous crypto trading on Base via Bankr. Use for trading tokens, monitoring launches, executing strategies, or managing a trading portfolio. Triggers on "trade", "buy", "sell", "launch", "snipe", "profit", "PnL", "portfolio balance", or any crypto trading task on Base.
metadata:
  version: "1.1.0"
  clawdbot:
    emoji: "📈"
---

# Base Trader 📈

Autonomous trading system for Base chain via Bankr API.

## Philosophy

> *"The market is a machine for transferring wealth from the impatient to the patient."*

This skill prioritizes **capital preservation** over aggressive gains. Every trade has defined risk parameters. No YOLO.

## Prerequisites

- Bankr API configured at `~/.clawdbot/skills/bankr/config.json`
- ETH in your Bankr wallet for gas and trading
- Check your wallet address with: `bankr.sh "What is my wallet address?"`

## Core Principles

### 1. Risk Management (NON-NEGOTIABLE)

```
MAX_POSITION_SIZE = 10% of portfolio
MAX_SINGLE_TRADE = $50 USD
STOP_LOSS = -15% from entry
TAKE_PROFIT = +30% minimum target
MAX_DAILY_LOSS = -20% of starting balance
```

If daily loss limit hit → STOP TRADING FOR 24 HOURS.

### 2. Entry Criteria (ALL must pass)

Before ANY buy:
- [ ] Liquidity > $10k
- [ ] Contract verified on Basescan
- [ ] No honeypot indicators (can sell)
- [ ] Not on known scam list
- [ ] Age > 5 minutes (avoid rugs at launch)
- [ ] Price action shows accumulation, not dump

### 3. Exit Rules

**Take Profit (scale out):**
- 25% at +30%
- 25% at +50%
- 25% at +100%
- Hold 25% moonbag

**Stop Loss:**
- Hard stop at -15%
- No averaging down on losers

## Trading Strategies

### Strategy 1: Launch Sniper (HIGH RISK)

Monitor new token launches, enter early with small size.

```bash
# Check trending/new tokens
scripts/bankr.sh "What tokens are trending on Base?"

# Research before buying
scripts/bankr.sh "What's the liquidity for TOKEN on Base?"

# Small entry
scripts/bankr.sh "Buy $20 of TOKEN on Base"
```

**Rules:**
- Max $20 per snipe
- Sell 50% at 2x, rest at 5x or stop loss
- Max 3 snipes per day

### Strategy 2: Momentum Trading (MEDIUM RISK)

Trade established tokens showing strength.

**Entry signals:**
- Price > 20-period MA
- Volume increasing
- Higher lows forming

```bash
# Check momentum
scripts/bankr.sh "Do technical analysis on TOKEN"

# Enter with limit order
scripts/bankr.sh "Buy $30 of TOKEN if price drops to X"
```

### Strategy 3: DCA Blue Chips (LOW RISK)

Steady accumulation of proven tokens.

```bash
# Weekly DCA
scripts/bankr.sh "DCA $20 into ETH every week on Base"
scripts/bankr.sh "DCA $10 into USDC every week on Base"
```

## Execution via Bankr

### Check Portfolio
```bash
~/clawd/skills/bankr/scripts/bankr.sh "Show my portfolio on Base"
```

### Execute Trade
```bash
~/clawd/skills/bankr/scripts/bankr.sh "Buy $25 of TOKEN on Base"
```

### Set Stop Loss
```bash
~/clawd/skills/bankr/scripts/bankr.sh "Set stop loss for TOKEN at -15%"
```

### Check Price
```bash
~/clawd/skills/bankr/scripts/bankr.sh "What's the price of TOKEN on Base?"
```

## Trade Journal

Log every trade to `data/trades.json`:

```json
{
  "timestamp": "2026-01-28T12:00:00Z",
  "action": "BUY",
  "token": "TOKEN",
  "amount_usd": 25,
  "price": 0.001,
  "reason": "Launch snipe - verified contract, good liquidity",
  "tx": "0x..."
}
```

After each trade, update the journal. Review weekly for pattern analysis.

## Daily Routine

### Morning (9 AM)
1. Check portfolio balance
2. Review overnight price action
3. Identify opportunities
4. Set limit orders for the day

### Midday (1 PM)
1. Check open positions
2. Adjust stop losses if in profit
3. Take profits if targets hit

### Evening (6 PM)
1. Close any day trades
2. Log all trades to journal
3. Calculate daily PnL
4. Review what worked/didn't

## Red Flags (DO NOT TRADE)

- Honeypot (can't sell)
- Liquidity < $5k
- Unverified contract
- Team anonymous with no track record
- Promises of guaranteed returns
- Excessive tax (>10%)
- Locked liquidity < 30 days
- Price already 10x+ from launch

## Performance Tracking

Track in `data/performance.json`:
```json
{
  "start_date": "2026-01-28",
  "starting_balance_usd": 100,
  "current_balance_usd": 100,
  "total_trades": 0,
  "winning_trades": 0,
  "losing_trades": 0,
  "win_rate": 0,
  "total_pnl_usd": 0,
  "best_trade": null,
  "worst_trade": null
}
```

## Safety Overrides

If ANY of these occur, STOP ALL TRADING:

1. Daily loss > 20%
2. 3 consecutive losing trades
3. Portfolio down > 30% from ATH
4. Unexpected error in execution
5. Market-wide crash (ETH -20% in 24h)

Wait 24 hours, reassess, then resume with smaller size.

## Autonomous Trading Mode

When running autonomously (via cron or heartbeat):

### Morning Scan (9 AM)
1. Check portfolio balance
2. Review overnight price action on holdings
3. Scan for new opportunities
4. Set limit orders for the day

### Midday Check (1 PM)
1. Monitor open positions
2. Adjust trailing stops on winners
3. Take profits if targets hit
4. Log any executed trades

### Evening Review (6 PM)
1. Close day trades if any
2. Calculate daily PnL
3. Update performance.json
4. Generate summary for user

### Execution Commands
```bash
# Morning
~/clawd/skills/bankr/scripts/bankr.sh "Show my portfolio on Base"
~/clawd/skills/bankr/scripts/bankr.sh "What tokens are trending on Base?"

# Execute trade
~/clawd/skills/bankr/scripts/bankr.sh "Buy $25 of TOKEN on Base"

# Set protection
~/clawd/skills/bankr/scripts/bankr.sh "Set stop loss for TOKEN at -15%"

# Take profit
~/clawd/skills/bankr/scripts/bankr.sh "Sell 25% of my TOKEN on Base"
```

## References

### Core Trading
- [references/strategies.md](references/strategies.md) - Detailed strategy breakdowns
- [references/token-analysis.md](references/token-analysis.md) - How to analyze tokens
- [references/risk-management.md](references/risk-management.md) - Position sizing formulas

### Market & Research
- [references/market-analysis.md](references/market-analysis.md) - Reading market conditions
- [references/market-research-bankr.md](references/market-research-bankr.md) - Bankr research commands

### Execution
- [references/execution.md](references/execution.md) - Order types and execution
- [references/automation-strategies.md](references/automation-strategies.md) - Automated trading setups
- [references/launch-sniping.md](references/launch-sniping.md) - New token launch guide

### Advanced
- [references/leverage-guide.md](references/leverage-guide.md) - Leveraged trading (high risk)

---

*"The goal is not to make money on every trade. The goal is to be profitable over time."*
