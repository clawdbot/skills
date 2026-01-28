# Hyperliquid Trading Skill for Clawdbot

Full-featured Clawdbot skill for trading Hyperliquid perpetual futures. Monitor your portfolio, analyze markets with charts/volume, and execute trades with AI assistance.

## Features

### Core Trading
- **Portfolio Monitoring**: Balance, positions, P&L tracking
- **Order Execution**: Market and limit orders (long & short)
- **Order Management**: Cancel specific orders or all at once
- **Trade History**: View recent fills
- **Security**: Read-only mode by default, trading requires explicit private key

### Market Analysis Tools 🆕
- **Chart Data with Volume**: Historical price action via CoinGecko
- **Momentum Detection**: Automated signal generation (strong bull/bear/neutral)
- **Volume Analysis**: Compare current volume vs average
- **Multi-timeframe**: 1-hour and 6-hour trend analysis
- **228+ Assets**: Trade any perpetual on Hyperliquid

### Strategy Support 🆕
- **Position Monitoring**: Check P&L with automated alerts
- **Risk Management**: 10% position size, stop losses, profit targets
- **Market Scanner**: Quick overview of all major assets
- **Decision Support**: Wait for high-probability setups

## Installation

```bash
# Install via ClawdHub (recommended)
clawdhub install hyperliquid

# Or install manually in your Clawdbot workspace
cd skills
# Clone or copy the hyperliquid skill folder here

# Install dependencies
cd hyperliquid/scripts
npm install
```

## Configuration

### Read-Only (Portfolio Monitoring)

Set your Hyperliquid address to check balances and positions without private key access:

```bash
export HYPERLIQUID_ADDRESS=0xYourAddress
```

### Trading (Requires Private Key)

For executing trades, set your private key:

```bash
export HYPERLIQUID_PRIVATE_KEY=0xYourPrivateKey
```

**Or use `.env` file** (recommended for security):
```bash
cd hyperliquid
cp .env.example .env
# Edit .env with your credentials
nano .env
```

⚠️ **Security**: Never commit your `.env` file. It's already in `.gitignore`.

### Testnet

To use Hyperliquid testnet:

```bash
export HYPERLIQUID_TESTNET=1
```

## Usage

### Market Analysis (New!)

**Analyze market with charts and volume:**
```bash
cd scripts
./analyze-coingecko.mjs

# Output includes:
# - Recent price action (last 10 hours)
# - Volume analysis vs average
# - Momentum signals (strong/weak bull/bear)
# - 6-hour trend direction
# - Trading recommendation
```

**Quick market scan:**
```bash
./scan-market.mjs

# Shows current prices for:
# - BTC, ETH, SOL, AVAX, DOGE, ARB
# - First 20 available perpetuals
```

**Check your positions:**
```bash
./check-positions.mjs

# Shows:
# - Account equity and available balance
# - Open positions with P&L
# - Profit target/stop loss alerts
# - Current BTC/ETH/SOL prices
```

### Direct CLI Trading

```bash
# Check balance
node scripts/hyperliquid.mjs balance

# View positions with P&L
node scripts/hyperliquid.mjs positions

# Get current BTC price
node scripts/hyperliquid.mjs price BTC

# Place market orders
node scripts/hyperliquid.mjs market-buy SOL 0.1
node scripts/hyperliquid.mjs market-sell ETH 0.5

# Place limit orders
node scripts/hyperliquid.mjs limit-buy BTC 0.001 88000
node scripts/hyperliquid.mjs limit-sell ETH 1 3100

# Cancel all orders
node scripts/hyperliquid.mjs cancel-all
```

### Through Clawdbot

Once installed, interact naturally:

- "Analyze the crypto market on Hyperliquid"
- "What's the momentum on BTC right now?"
- "Check my Hyperliquid positions"
- "Show me current SOL price and volume"
- "Enter a BTC long position"
- "Close my ETH position"

## Commands Reference

### Read Operations (No Private Key Needed)

- `balance [address]` - Show account balance and equity
- `positions [address]` - Show open positions with P&L
- `price <coin>` - Get current price (auto-adds -PERP)
- `meta` - List all available coins

### Trading Operations (Requires HYPERLIQUID_PRIVATE_KEY)

- `market-buy <coin> <size>` - Market buy (5% slippage protection)
- `market-sell <coin> <size>` - Market sell (5% slippage protection)
- `limit-buy <coin> <size> <price>` - Place limit buy order
- `limit-sell <coin> <size> <price>` - Place limit sell order
- `cancel-all [coin]` - Cancel all orders (optionally for one coin)

### Analysis Scripts

- `analyze-coingecko.mjs` - Full market analysis with charts/volume
- `check-positions.mjs` - Monitor open positions and P&L
- `scan-market.mjs` - Quick price overview

## Strategy Examples

### Momentum Scalping (Recommended for Small Accounts)

```bash
# 1. Analyze market conditions
./analyze-coingecko.mjs

# 2. If signal is "STRONG BULLISH" or "STRONG BEARISH", check position size
# Account: $100, 10% position = $10

# 3. Enter trade
node hyperliquid.mjs market-buy ETH 0.0033  # ~$10 position

# 4. Monitor position every 30-60 minutes
./check-positions.mjs

# 5. Exit at +2% profit target or -1% stop loss
node hyperliquid.mjs market-sell ETH 0.0033
```

### Risk Parameters (Example)

- **Position Size**: 10% of account per trade
- **Max Loss**: 1% per trade (stop loss)
- **Profit Target**: 2% per trade
- **Max Positions**: 1 at a time (focus)
- **Entry Signal**: Volume >1.5x average + price move >0.5%

## Architecture

- **CLI Client**: `scripts/hyperliquid.mjs` - Official Hyperliquid SDK wrapper
- **Market Analysis**: `scripts/analyze-coingecko.mjs` - CoinGecko API integration
- **Position Monitor**: `scripts/check-positions.mjs` - Real-time P&L tracking
- **Market Scanner**: `scripts/scan-market.mjs` - Quick price overview
- **Skill Definition**: `SKILL.md` - Instructions for Clawdbot
- **API Reference**: `references/api.md` - Hyperliquid API docs
- **Dependencies**: Official `hyperliquid` npm package, `node-fetch`

## API & Data Sources

**Trading**: 
- Hyperliquid API (mainnet: `https://api.hyperliquid.xyz`)
- Official SDK: `hyperliquid` npm package

**Market Data**:
- CoinGecko Free API (no auth required)
- 24-hour historical data with volume
- Automatic momentum signal generation

## Safety Features

- **Read-only by default**: No private key needed for monitoring
- **Slippage protection**: Market orders use 5% limit buffer
- **Position size validation**: Checks minimum order size ($10)
- **Stop loss alerts**: Automated notifications when hit
- **Profit target tracking**: Know when to take gains
- **Clear signal thresholds**: Only trade strong momentum (>0.5% + volume)

## Trading Strategy Support

The skill includes a complete momentum scalping strategy:

**Entry Criteria**:
- Price move >0.5% in 15-30 minutes
- Volume >1.5x average (confirms momentum)
- Clear directional bias (not choppy)

**Position Management**:
- Set 2% profit target
- Set 1% stop loss
- Monitor every 30-60 minutes
- Max hold time: 4 hours

**Exit Rules**:
- Hit profit target → Close immediately
- Hit stop loss → Close immediately  
- No momentum → Close at breakeven
- Max time reached → Close position

## Development

Built with:
- Node.js (ES modules)
- Official Hyperliquid SDK for trading
- CoinGecko API for market analysis
- node-fetch for HTTP requests

## Updates

**v2.0.0** (2026-01-27)
- 🎉 Integrated official Hyperliquid SDK
- 📊 Added chart/volume analysis via CoinGecko
- 🎯 Automated momentum signal detection
- 📈 Position monitoring with P&L alerts
- 🔧 Fixed all trading operations
- 📝 Complete strategy documentation

**v1.0.0** (2026-01-27)
- Initial release
- Basic trading functionality
- Portfolio monitoring

## License

MIT

## About Clawdbot

Clawdbot is an AI assistant framework with extensible skills. Learn more at https://clawd.bot

---

**Disclaimer**: This is unofficial software. Use at your own risk. Trading cryptocurrency perpetual futures is high risk. Always verify trades before execution. The automated signals are for informational purposes only and not financial advice.
