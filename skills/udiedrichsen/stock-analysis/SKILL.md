---
name: stock-analysis
description: Analyze stocks and cryptocurrencies using Yahoo Finance data. Supports portfolio management (create, add, remove assets), crypto analysis (Top 20 by market cap), and periodic performance reports (daily/weekly/monthly/quarterly/yearly). 8 analysis dimensions for stocks, 3 for crypto. Use for stock analysis, portfolio tracking, earnings reactions, or crypto monitoring.
homepage: https://finance.yahoo.com
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["uv"],"env":[]},"install":[{"id":"uv-brew","kind":"brew","formula":"uv","bins":["uv"],"label":"Install uv (brew)"}]}}
---

# Stock Analysis (v5.0)

Analyze US stocks and cryptocurrencies using Yahoo Finance data. Includes portfolio management, crypto support, and periodic analysis.

## Quick Start

**IMPORTANT:** Pass ONLY the stock ticker symbol(s) as arguments. Do NOT add extra text, headers, or formatting in the command.

Analyze a single ticker:

```bash
uv run {baseDir}/scripts/analyze_stock.py AAPL
uv run {baseDir}/scripts/analyze_stock.py MSFT --output json
```

Compare multiple tickers:

```bash
uv run {baseDir}/scripts/analyze_stock.py AAPL MSFT GOOGL
```

## Cryptocurrency Analysis (v5.0)

Analyze top 20 cryptocurrencies by market cap:

```bash
uv run {baseDir}/scripts/analyze_stock.py BTC-USD
uv run {baseDir}/scripts/analyze_stock.py ETH-USD SOL-USD
```

**Supported Cryptos:**
BTC-USD, ETH-USD, BNB-USD, SOL-USD, XRP-USD, ADA-USD, DOGE-USD, AVAX-USD, DOT-USD, MATIC-USD, LINK-USD, ATOM-USD, UNI-USD, LTC-USD, BCH-USD, XLM-USD, ALGO-USD, VET-USD, FIL-USD, NEAR-USD

**Crypto Analysis Dimensions:**
- Market cap (large/mid/small classification)
- Category (Smart Contract L1, DeFi, Payment, etc.)
- BTC correlation (30-day)
- Momentum (RSI, price range)
- Market context (VIX, general market regime)

## Portfolio Management (v5.0)

Create and manage portfolios with mixed assets (stocks + crypto):

```bash
# Create portfolio
uv run {baseDir}/scripts/portfolio.py create "My Portfolio"

# Add assets
uv run {baseDir}/scripts/portfolio.py add AAPL --quantity 100 --cost 150.00
uv run {baseDir}/scripts/portfolio.py add BTC-USD --quantity 0.5 --cost 40000 --portfolio "My Portfolio"

# View holdings with current P&L
uv run {baseDir}/scripts/portfolio.py show

# Update/remove assets
uv run {baseDir}/scripts/portfolio.py update AAPL --quantity 150
uv run {baseDir}/scripts/portfolio.py remove BTC-USD

# List/delete portfolios
uv run {baseDir}/scripts/portfolio.py list
uv run {baseDir}/scripts/portfolio.py delete "My Portfolio"
```

**Portfolio Storage:** `~/.clawdbot/skills/stock-analysis/portfolios.json`

## Portfolio Analysis (v5.0)

Analyze all assets in a portfolio with optional period returns:

```bash
# Analyze portfolio
uv run {baseDir}/scripts/analyze_stock.py --portfolio "My Portfolio"

# With period returns (daily/weekly/monthly/quarterly/yearly)
uv run {baseDir}/scripts/analyze_stock.py --portfolio "My Portfolio" --period weekly
uv run {baseDir}/scripts/analyze_stock.py -p "My Portfolio" --period monthly
```

**Portfolio Summary includes:**
- Total cost, current value, P&L
- Period return (if specified)
- Concentration warnings (>30% in single asset)
- Recommendation summary (BUY/HOLD/SELL counts)

**Examples:**
- ✅ CORRECT: `uv run {baseDir}/scripts/analyze_stock.py BAC`
- ✅ CORRECT: `uv run {baseDir}/scripts/analyze_stock.py BTC-USD`
- ❌ WRONG: `uv run {baseDir}/scripts/analyze_stock.py === BANK OF AMERICA (BAC) - Q4 2025 EARNINGS ===`
- ❌ WRONG: `uv run {baseDir}/scripts/analyze_stock.py "Bank of America"`

Use the ticker symbol only (e.g., BAC, not "Bank of America"). For crypto, use the -USD suffix (e.g., BTC-USD).

## Analysis Components

The script evaluates eight key dimensions:

1. **Earnings Surprise (30% weight)**: Actual vs expected EPS, revenue beats/misses
2. **Fundamentals (20% weight)**: P/E ratio, profit margins, revenue growth, debt levels
3. **Analyst Sentiment (20% weight)**: Consensus ratings, price target vs current price
4. **Historical Patterns (10% weight)**: Past earnings reactions, volatility
5. **Market Context (10% weight)**: VIX, SPY/QQQ trends, market regime
6. **Sector Performance (15% weight)**: Stock vs sector comparison, sector trends
7. **Momentum (15% weight)**: RSI, 52-week range, volume, relative strength
8. **Sentiment Analysis (10% weight)**: Fear/Greed Index, short interest, VIX term structure, insider trading, put/call ratio

**Sentiment Sub-Indicators:**
- **Fear & Greed Index (CNN)**: Contrarian signal (extreme fear = buy opportunity, extreme greed = caution)
- **Short Interest**: High shorts + squeeze potential = bullish; justified shorts = bearish
- **VIX Term Structure**: Contango = complacency/bullish; backwardation = stress/bearish
- **Insider Activity**: Net buying/selling from SEC Form 4 filings (90-day window)
- **Put/Call Ratio**: High ratio = excessive fear/bullish; low ratio = complacency/bearish

Weights auto-normalize if some components unavailable.

**Special Timing Checks:**
- Pre-earnings warning (< 14 days): Recommends HOLD instead of BUY
- Post-earnings spike detection (> 15% in 5 days): Flags "gains priced in"
- Overbought conditions (RSI > 70 + near 52w high): Reduces confidence

## Timing Warnings & Risk Flags

The script detects high-risk scenarios:

### Earnings Timing
- **Pre-Earnings Period**: If earnings < 14 days away, BUY signals become HOLD
- **Post-Earnings Spike**: If stock up > 15% in 5 days after earnings, warns "gains may be priced in"

### Technical Risk
- **Overbought Conditions**: RSI > 70 + near 52-week high = high-risk entry

### Market Risk
- **High VIX**: Market fear (VIX > 30) reduces confidence in BUY signals
- **Risk-Off Mode (v4.0.0)**: When safe-havens (GLD, TLT, UUP) rise together, reduces BUY confidence by 30%
  - Detects flight to safety across gold, treasuries, and USD
  - Triggers when GLD ≥ +2%, TLT ≥ +1%, UUP ≥ +1% (5-day change)

### Sector Risk
- **Sector Weakness**: Stock may look good but sector is rotating out

### Geopolitical Risk (v4.0.0)
The script now scans breaking news (last 24h) for crisis keywords and automatically flags affected stocks:

- **Taiwan Conflict**: Semiconductors (NVDA, AMD, TSM, INTC, etc.) → 30% confidence penalty
- **China Tensions**: Tech/Consumer (AAPL, QCOM, NKE, SBUX, etc.) → 30% confidence penalty
- **Russia-Ukraine**: Energy/Materials (XOM, CVX, MOS, CF, etc.) → 30% confidence penalty
- **Middle East**: Oil/Defense (XOM, LMT, RTX, etc.) → 30% confidence penalty
- **Banking Crisis**: Financials (JPM, BAC, WFC, C, etc.) → 30% confidence penalty

If a ticker is not in the affected list but its sector is exposed, applies a 15% confidence penalty.

**Example Alert:**
```
⚠️ SECTOR RISK: Tech supply chain and consumer market exposure (detected: china, tariff)
```

### Breaking News Alerts (v4.0.0)
- Scans Google News RSS for crisis keywords (war, recession, sanctions, disasters, etc.)
- Displays up to 2 breaking news alerts in caveats (last 24 hours)
- Uses 1-hour cache to avoid excessive API calls

## Output Format

**Default (text)**: Concise buy/hold/sell signal with 3-5 bullet points and caveats

**JSON**: Structured data with scores, metrics, and raw data for further analysis

## Limitations

- **Data freshness**: Yahoo Finance may lag 15-20 minutes
- **Sentiment data staleness**:
  - Short interest data lags ~2 weeks (FINRA reporting schedule)
  - Insider trades may lag filing by 2-3 days
  - VIX term structure only updates during futures trading hours
- **Breaking news limitations (v4.0.0)**:
  - Google News RSS may lag by 15-60 minutes
  - Keyword matching may have false positives/negatives
  - Does not analyze sentiment, only detects keywords
  - 1-hour cache means alerts may be slightly stale
- **Missing data**: Not all stocks have analyst coverage, options chains, or complete fundamentals
- **Execution time**: 3-5s per stock with async parallel fetching and caching (shared indicators cached for 1h)
- **Disclaimer**: All outputs include prominent "not financial advice" warning
- **US markets only**: Non-US tickers may have incomplete data

## Error Handling

The script gracefully handles:
- Invalid tickers → Clear error message
- Missing analyst data → Signal based on available metrics only
- API failures → Retry with exponential backoff, fail after 3 attempts
