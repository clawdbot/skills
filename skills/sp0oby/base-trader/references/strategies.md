# Trading Strategies Deep Dive

## Launch Sniping

### What It Is
Buying tokens very early after launch to capture initial price appreciation.

### The Edge
- Early liquidity providers often sell quickly
- Genuine projects often 5-10x from launch
- Small capital can generate outsized returns

### The Risk
- 90%+ of launches are rugs or scams
- Extreme volatility
- Liquidity can disappear instantly

### Execution Checklist

1. **Find the launch**
   - Monitor Base token deployers
   - Watch crypto Twitter for calls
   - Use Bankr: "What tokens are trending on Base?"

2. **Verify contract (60 seconds)**
   - Check Basescan verification
   - Look for honeypot functions
   - Check tax rates
   - Verify liquidity lock

3. **Size appropriately**
   - Never more than $20 per snipe
   - Expect 80% to lose
   - The 20% winners must cover losses

4. **Exit fast**
   - Take 50% at 2x
   - Move stop to breakeven
   - Let rest ride to 5x or stop out

### Example Flow
```
1. See new token CABIN on Base
2. Check: "What's the liquidity for CABIN on Base?"
3. Check: Contract verified? ✓
4. Check: Can sell? (small test sell)
5. Buy: "Buy $15 of CABIN on Base"
6. Set alert at 2x
7. At 2x: "Sell 50% of my CABIN"
8. Move mental stop to entry
9. At 5x or stop: Sell rest
```

## Momentum Trading

### What It Is
Trading tokens already showing upward momentum, riding the trend.

### Indicators to Watch
- Price above moving averages
- Increasing volume
- Higher highs, higher lows
- Social sentiment positive

### Entry Criteria
1. Token up 20%+ in 24h with volume
2. Not already extended (avoid buying tops)
3. Clear support level to place stop
4. Risk:reward at least 1:2

### Position Sizing
```
Risk per trade = 2% of portfolio
Stop distance = Entry - Stop price
Position size = Risk / Stop distance
```

### Example
```
Portfolio: $100
Risk (2%): $2
Entry: $0.10
Stop: $0.085 (15% below)
Position size: $2 / $0.015 = $13.33 worth
```

## DCA (Dollar Cost Averaging)

### What It Is
Buying fixed amounts at regular intervals regardless of price.

### Why It Works
- Removes emotion from trading
- Averages out volatility
- Builds positions over time
- No timing required

### Best For
- ETH, major tokens
- Long-term accumulation
- Reducing average entry

### Setup via Bankr
```bash
"DCA $20 into ETH every week on Base"
"DCA $10 into USDC every week on Base"
```

## Grid Trading

### What It Is
Placing buy and sell orders at regular intervals.

### Setup
```
Token range: $0.08 - $0.12
Grid levels: 5
Buy at: $0.08, $0.085, $0.09, $0.095, $0.10
Sell at: $0.10, $0.105, $0.11, $0.115, $0.12
```

### Benefits
- Profits from volatility
- Automatic execution
- Works in ranging markets

### Via Bankr
```bash
"Set limit buy for TOKEN at $0.08"
"Set limit sell for TOKEN at $0.12"
```
