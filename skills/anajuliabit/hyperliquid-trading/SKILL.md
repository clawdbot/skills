---
name: hyperliquid
description: Trade and monitor Hyperliquid perpetual futures. Check balances, view positions with P&L, place/cancel orders, execute market trades. Use when the user asks about Hyperliquid trading, portfolio status, crypto positions, or wants to execute trades on Hyperliquid.
---

# Hyperliquid Trading Skill

Full trading and portfolio management for Hyperliquid perpetual futures exchange.

## Prerequisites

Install dependencies once:

```bash
cd skills/hyperliquid/scripts && npm install
```

## Authentication

**For read-only operations (balance, positions, prices):**
- Set `HYPERLIQUID_ADDRESS` environment variable
- No private key needed

**For trading operations:**
- Set `HYPERLIQUID_PRIVATE_KEY` environment variable
- Address derived automatically from private key

**Testnet:**
- Set `HYPERLIQUID_TESTNET=1` to use testnet

## Core Operations

### Portfolio Monitoring

**Check balance:**
```bash
HYPERLIQUID_ADDRESS=0x... node scripts/hyperliquid.mjs balance
```

**View positions with P&L:**
```bash
HYPERLIQUID_ADDRESS=0x... node scripts/hyperliquid.mjs positions
```

**Check open orders:**
```bash
HYPERLIQUID_ADDRESS=0x... node scripts/hyperliquid.mjs orders
```

**View trade history:**
```bash
HYPERLIQUID_ADDRESS=0x... node scripts/hyperliquid.mjs fills
```

**Get price for a coin:**
```bash
node scripts/hyperliquid.mjs price BTC
```

### Trading Operations

All trading commands require `HYPERLIQUID_PRIVATE_KEY`.

**Place limit orders:**
```bash
# Buy 0.1 BTC at $45,000
HYPERLIQUID_PRIVATE_KEY=0x... node scripts/hyperliquid.mjs buy BTC 0.1 45000

# Sell 1 ETH at $3,000
HYPERLIQUID_PRIVATE_KEY=0x... node scripts/hyperliquid.mjs sell ETH 1 3000
```

**Market orders (with 5% slippage protection):**
```bash
# Market buy 0.5 BTC
HYPERLIQUID_PRIVATE_KEY=0x... node scripts/hyperliquid.mjs market-buy BTC 0.5

# Market sell 2 ETH
HYPERLIQUID_PRIVATE_KEY=0x... node scripts/hyperliquid.mjs market-sell ETH 2
```

**Cancel orders:**
```bash
# Cancel specific order
HYPERLIQUID_PRIVATE_KEY=0x... node scripts/hyperliquid.mjs cancel BTC 12345

# Cancel all orders
HYPERLIQUID_PRIVATE_KEY=0x... node scripts/hyperliquid.mjs cancel-all

# Cancel all orders for specific coin
HYPERLIQUID_PRIVATE_KEY=0x... node scripts/hyperliquid.mjs cancel-all BTC
```

## Output Formatting

All commands output JSON. Parse and format for chat display:

**For balance/portfolio:**
- Show total equity, available balance
- List positions with size, entry price, unrealized P&L
- Summarize open orders

**For trade execution:**
- Confirm order details before executing
- Report order ID and status after execution
- Show filled price if immediately executed

## Safety Guidelines

**Before executing trades:**
1. Confirm trade parameters with user (coin, size, direction, price)
2. Show current price and position for context
3. Calculate estimated cost/proceeds

**Position sizing:**
- Warn if trade is >20% of account equity
- Suggest appropriate sizes based on account balance

**Price checks:**
- For limit orders, compare limit price to current market price
- Warn if limit price is >5% away from market (likely mistake)

## Error Handling

**Common errors:**
- "Address required" → Set HYPERLIQUID_ADDRESS or HYPERLIQUID_PRIVATE_KEY
- "Private key required" → Trading needs HYPERLIQUID_PRIVATE_KEY
- "Unknown coin" → Check available coins with `meta` command
- HTTP errors → Check network connection and API status

**When errors occur:**
- Show the error message to user
- Suggest fixes (set env vars, check coin names, verify balance)
- Don't retry trades automatically

## Workflow Examples

**"How's my Hyperliquid portfolio?"**
1. Run `balance` to get total equity
2. Run `positions` to get open positions
3. Format summary: equity, positions with P&L, total unrealized P&L

**"Buy 0.5 BTC on Hyperliquid"**
1. Run `price BTC` to get current price
2. Run `balance` to verify sufficient funds
3. Confirm with user: "Buy 0.5 BTC at market? Current price: $X. Estimated cost: $Y"
4. Execute `market-buy BTC 0.5`
5. Report order result

**"What's the current BTC price on Hyperliquid?"**
1. Run `price BTC`
2. Format response: "BTC: $X on Hyperliquid"

**"Close my ETH position"**
1. Run `positions` to get current ETH position size
2. If long → market-sell, if short → market-buy
3. Execute with position size
4. Report result

## Advanced Features

**List all available coins:**
```bash
node scripts/hyperliquid.mjs meta
```

**Query other addresses:**
```bash
# Check someone else's positions (read-only, public data)
node scripts/hyperliquid.mjs positions 0x1234...
```

## Notes

- All sizes are in base currency (BTC, ETH, etc.)
- Prices are in USD
- Market orders use limit orders with 5% slippage protection
- Hyperliquid uses perpetual futures, not spot trading
- Check references/api.md for full API documentation
