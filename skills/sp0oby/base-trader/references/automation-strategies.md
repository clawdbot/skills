# Automation Strategies

Leverage Bankr's automation features for systematic trading.

## Order Types via Bankr

### Limit Orders
Execute when price reaches target.

```bash
"Set a limit order to buy TOKEN at $0.001 on Base"
"Limit order: sell TOKEN when it hits $0.002"
"Buy $50 of TOKEN if price drops to $X"
```

**Use cases:**
- Buy the dip
- Take profit at target
- Enter at better price
- Scale into positions

### Stop Loss Orders
Automatically sell to limit losses.

```bash
"Set stop loss for my TOKEN at $0.0008"
"Stop loss: sell 50% of TOKEN if it drops 20%"
"Protect all Base positions with -15% stop"
```

**ALWAYS use stop losses. Non-negotiable.**

### DCA (Dollar Cost Averaging)
Fixed amounts at regular intervals.

```bash
"DCA $20 into ETH every week on Base"
"Set up daily $10 USDC purchases"
"Buy $25 of TOKEN every Monday"
```

**Best for:**
- Long-term accumulation
- Reducing timing risk
- Disciplined investing

### TWAP (Time-Weighted Average Price)
Spread large orders over time.

```bash
"TWAP: buy $200 of TOKEN over 24 hours on Base"
"Spread my sell order over 4 hours"
```

**Use for:**
- Large order execution
- Reduce slippage
- Minimize market impact

## Automated Strategy Templates

### Strategy 1: Protected DCA

Build position while protecting downside.

```bash
# Set up weekly buys
"DCA $20 into ETH every week on Base"

# Protect accumulated position
"Set stop loss at -20% for all my ETH"
```

### Strategy 2: Layered Buy Orders

Buy at multiple price levels.

```bash
"Buy $10 of TOKEN if price drops to $0.001"
"Buy $20 of TOKEN if price drops to $0.0008"
"Buy $30 of TOKEN if price drops to $0.0006"
```

### Strategy 3: Scaled Take Profit

Lock in gains progressively.

```bash
"Limit order: sell 25% of TOKEN at $0.002"
"Limit order: sell 25% of TOKEN at $0.003"
"Limit order: sell 25% of TOKEN at $0.005"
# Keep 25% as moonbag
```

### Strategy 4: Range Trading

Buy low, sell high in a range.

```bash
"Buy TOKEN at $0.001 on Base"
"Sell TOKEN when it hits $0.0015"
# Repeat as range continues
```

### Strategy 5: Grid Trading

Multiple buys and sells in a range.

```bash
# Set buy grid
"Limit buy TOKEN at $0.001"
"Limit buy TOKEN at $0.0009"
"Limit buy TOKEN at $0.0008"

# Set sell grid
"Limit sell TOKEN at $0.0012"
"Limit sell TOKEN at $0.0013"
"Limit sell TOKEN at $0.0014"
```

## Managing Automations

### View Active Orders
```bash
"Show my automations"
"What limit orders do I have?"
"List my active DCAs"
```

### Cancel Orders
```bash
"Cancel my TOKEN limit order"
"Stop my DCA into ETH"
"Cancel all my stop losses"
```

## Best Practices

### Setup
1. Start with small amounts to test
2. Be specific about triggers
3. Ensure funds available for execution
4. Set alerts for executions
5. Review orders weekly

### Risk Management
1. Always pair buys with stop losses
2. Don't over-automate
3. Adjust targets as market changes
4. Factor in gas costs
5. Keep some capital in reserve

### Common Mistakes
- Setting orders and forgetting them
- Not accounting for gas
- Overlapping/conflicting orders
- Unrealistic price targets
- No stop loss protection

## Execution Costs

### Base Chain (Low Cost)
- Gas per transaction: ~$0.01-0.05
- DCA monthly cost: ~$0.50
- Very efficient for automation

### Considerations
- Daily DCA = 365 transactions/year
- Weekly DCA = 52 transactions/year
- Factor costs into profit calculations
