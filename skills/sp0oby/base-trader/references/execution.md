# Trade Execution

## Order Types via Bankr

### Market Orders (Immediate)
```bash
"Buy $25 of TOKEN on Base"
"Sell all my TOKEN on Base"
"Sell 50% of my TOKEN"
```

Best for:
- Fast-moving opportunities
- Exiting positions quickly
- When slippage is acceptable

### Limit Orders (Price-specific)
```bash
"Buy TOKEN at $0.001 on Base"
"Set limit order to buy TOKEN if price drops to $0.0008"
"Sell TOKEN when it hits $0.002"
```

Best for:
- Better entry prices
- Automated exits
- Not watching charts

### Stop Loss Orders
```bash
"Set stop loss for TOKEN at $0.0007"
"Set stop loss for all holdings at -15%"
```

Essential for:
- Every single trade
- Protecting capital
- Sleeping at night

### DCA Orders
```bash
"DCA $20 into ETH every week on Base"
"Set up weekly buy of $10 USDC"
```

Best for:
- Long-term accumulation
- Reducing timing risk
- Building positions

## Execution Checklist

### Before Entry
- [ ] Portfolio checked
- [ ] Position size calculated
- [ ] Stop loss level defined
- [ ] Take profit targets set
- [ ] Within daily risk budget
- [ ] Token analysis complete

### Entry Execution
```bash
# 1. Final price check
"What's the current price of TOKEN on Base?"

# 2. Execute buy
"Buy $25 of TOKEN on Base"

# 3. Verify execution
"Show my TOKEN balance on Base"

# 4. Log the trade
./scripts/log-trade.sh "BUY" "TOKEN" "25" "0.001" "momentum entry" "0x..."
```

### After Entry
- [ ] Stop loss set
- [ ] Trade logged
- [ ] Alerts configured
- [ ] Position monitored

## Slippage Management

### What Is Slippage
Difference between expected and actual execution price.

### Minimizing Slippage
1. Use limit orders when possible
2. Trade tokens with deep liquidity
3. Avoid large orders relative to liquidity
4. Trade during active hours

### Acceptable Slippage
- Large cap: < 0.5%
- Mid cap: < 1%
- Small cap: < 2%
- New launches: < 5% (expected)

## Partial Execution

### Scaling In
Instead of one large buy:
```bash
"Buy $10 of TOKEN on Base"  # First entry
# Wait for confirmation
"Buy $10 of TOKEN on Base"  # Add if thesis holds
# Wait for confirmation  
"Buy $10 of TOKEN on Base"  # Final position
```

### Scaling Out
```bash
"Sell 25% of my TOKEN"  # At +30%
"Sell 25% of my TOKEN"  # At +50%
"Sell 25% of my TOKEN"  # At +100%
# Hold 25% moonbag
```

## Error Handling

### Transaction Failed
1. Check wallet balance (gas)
2. Verify token address
3. Check if token is tradeable
4. Try smaller amount
5. Wait and retry

### Unexpected Price
1. Verify current price
2. Check for recent news
3. Review liquidity
4. Decide: abort or adjust

### Partial Fill
1. Check how much filled
2. Decide: wait or cancel remainder
3. Adjust position tracking
