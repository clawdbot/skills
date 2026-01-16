# Stock Analysis v5.0

Analyze stocks and cryptocurrencies with portfolio management, periodic reports, and 8-dimension analysis.

## Features

| Feature | Description |
|---------|-------------|
| **Stock Analysis** | 8 dimensions: earnings, fundamentals, analysts, historical, market, sector, momentum, sentiment |
| **Crypto Analysis** | Top 20 cryptos: market cap, category, BTC correlation, momentum |
| **Portfolio Management** | Create portfolios, add/remove assets, track P&L |
| **Periodic Reports** | Daily, weekly, monthly, quarterly, yearly returns |
| **Risk Detection** | Geopolitical risk, breaking news alerts, concentration warnings |

## Quick Start

### Analyze Stocks
```bash
uv run scripts/analyze_stock.py AAPL
uv run scripts/analyze_stock.py AAPL MSFT GOOGL
```

### Analyze Crypto
```bash
uv run scripts/analyze_stock.py BTC-USD
uv run scripts/analyze_stock.py ETH-USD SOL-USD
```

### Portfolio Management
```bash
# Create and manage portfolios
uv run scripts/portfolio.py create "My Portfolio"
uv run scripts/portfolio.py add AAPL --quantity 100 --cost 150
uv run scripts/portfolio.py add BTC-USD --quantity 0.5 --cost 40000
uv run scripts/portfolio.py show

# Analyze portfolio
uv run scripts/analyze_stock.py --portfolio "My Portfolio"
uv run scripts/analyze_stock.py --portfolio "My Portfolio" --period weekly
```

## Supported Cryptocurrencies (Top 20)

BTC, ETH, BNB, SOL, XRP, ADA, DOGE, AVAX, DOT, MATIC, LINK, ATOM, UNI, LTC, BCH, XLM, ALGO, VET, FIL, NEAR

## Analysis Dimensions

### Stocks (8 dimensions)
1. **Earnings Surprise** - EPS beats/misses
2. **Fundamentals** - P/E, margins, growth, debt
3. **Analyst Sentiment** - Ratings, price targets
4. **Historical Patterns** - Past earnings reactions
5. **Market Context** - VIX, SPY/QQQ trends
6. **Sector Performance** - Relative strength
7. **Momentum** - RSI, 52-week range
8. **Sentiment** - Fear/Greed, short interest, insider trading

### Crypto (3 dimensions)
1. **Crypto Fundamentals** - Market cap, category, BTC correlation
2. **Momentum** - RSI, price range
3. **Market Context** - General market regime

## Risk Features

- **Breaking News Alerts** - Scans for crisis keywords (war, recession, sanctions)
- **Geopolitical Risk** - Taiwan, China, Russia, Middle East, banking crisis detection
- **Safe-Haven Tracking** - GLD, TLT, UUP for risk-off detection
- **Concentration Warnings** - Alerts when >30% in single asset

## Portfolio Storage

Portfolios stored at: `~/.clawdbot/skills/stock-analysis/portfolios.json`

## Version History

- **v5.0.0** - Portfolio management, crypto support, periodic analysis
- **v4.1.0** - Insider trading via edgartools, market context caching
- **v4.0.0** - Geopolitical risk, breaking news, safe-haven detection
- **v3.0.0** - Sentiment analysis (5 indicators)
- **v2.0.0** - Market context, sector, momentum
- **v1.0.0** - Initial release

## Data Sources

- [Yahoo Finance](https://finance.yahoo.com) - Price, fundamentals, earnings
- [CNN Fear & Greed](https://money.cnn.com/data/fear-and-greed/) - Market sentiment
- [SEC EDGAR](https://www.sec.gov/edgar) - Insider trading (Form 4)
- [Google News RSS](https://news.google.com) - Breaking news

---

**Disclaimer:** This tool is for informational purposes only and does NOT constitute financial advice.
