# Quant-Style Dashboard Quick Reference (Enhanced)

## ⚠️ DATA INTEGRITY REQUIREMENTS

**CRITICAL**: Every metric in the dashboard must come from a verified source.

### Source Requirements
| Data Type | Required Source |
|-----------|-----------------|
| Price, Market Cap | Yahoo Finance, Google Finance |
| Financial Ratios | Company filings, Yahoo Finance |
| Insider Trading | SEC Form 4 ONLY (or N/A) |
| Short Interest | FINRA/exchange ONLY (or N/A) |
| Technical Indicators | Yahoo Finance, TradingView |

### If Data Unavailable
- Display "N/A" - NEVER zeros or estimates
- Zero means "zero occurred" - not "unknown"

---

## Overview

The Stock Evaluator skill produces an enhanced "quant-style" dashboard as the final output. This dashboard is an institutional-grade visualization with 60+ metrics, Ichimoku Cloud analysis, 8 investor persona scores, Value Trap detection, and TOP NEWS integration.

## What You'll Get

### Text Analysis (First)
Complete written analysis including:
- Business understanding
- Financial analysis (5-10 years)
- Valuation assessment
- Technical analysis (including Ichimoku Cloud)
- Value Trap assessment
- Investor Persona fit analysis
- Bull vs Bear case
- Investment recommendation
- All advanced metrics

### Visual Dashboard (Second)
React artifact with:
- **TOP NEWS ticker** (scrolling recent headlines)
- **8 color-coded metric sections** (60+ total metrics)
- **Value Trap indicator** with color-coded score
- **8 Investor Persona badges** around radar chart
- **4 charts**: Linear Price + MACD, Radar + Forecast, Log Price + RSI, Ichimoku Cloud
- **Enhanced legends** with actual valuation line values
- **Expandable Key Notes** (Bull/Bear/Entry-Exit)
- **Professional styling** with € currency default

## Dashboard Layout

```
┌─────────────────────────────────────────────────────┐
│  TICKER - Company Name (Orange Header)              │
├─────────────────────────────────────────────────────┤
│ TOP NEWS: Headline [DD Mon YYYY] | Headline [Date]..│
├────────────────────────┬────────────────────────────┤
│ Price & Val (6 metrics)│ Financial Perf (6 metrics) │
│ + PEG (1Y)             │ + Operative Margin         │
├────────────────────────┼────────────────────────────┤
│ Growth (6 metrics)     │ Risk Indicators (6 metrics)│
│ Revenue/Earning (YoY)  │ + Piotroski F, Altman Z    │
├────────────────────────┼────────────────────────────┤
│ Liquidity (7 metrics)  │ Insider & Sent (7 metrics) │
│ Cash, Debt, FCF        │ + Stock Type + Div Yield   │
├────────────────────────┼────────────────────────────┤
│ Quality (6 metrics)    │ Moat & Other (6 metrics)   │
│                        │ + Beta + Vol 1Y combined   │
├────────────────────────┴────────────────────────────┤
│ LINEAR (10Y)    │ RADAR + PERSONAS  │ LOG (10Y)     │
│ + Value legends │ [8 investor badges]│ + Value legends│
│                 │ + 1Y Forecast/MAs │               │
│                 │ + Valuation %     │               │
├─────────────────────────────────────────────────────┤
│ ICHIMOKU CLOUD │                    │ MACD + RSI    │
├─────────────────────────────────────────────────────┤
│ ▶ Key Notes (Expandable)                            │
│   Bull Case | Bear Case | Entry/Exit Strategy       │
└─────────────────────────────────────────────────────┘
```

## TOP NEWS Format

**CRITICAL**: Use pipe-separated format with dates at END in brackets

### Correct Format:
```
TOP NEWS:
Headline text here [11 Nov 2025] | Another headline here [23 Sep 2025] | Third headline [30 Sep 2025]
```

### WRONG Format (DO NOT USE):
```
[11 Nov 2025] Headline text
[23 Sep 2025] Another headline
```

## Metrics Included (60+ Total)

### Price & Valuation (7)
1. Price (€)
2. Market Cap (€)
3. Trailing P/E
4. Forward P/E
5. Subsector Typical P/E
6. **PEG (1Y)** - 1-Year Forward PEG
7. **PEG (5Y)** - 5-Year Historical PEG

### Financial Performance (6)
1. ROE (>20% green, 10-20% yellow, <10% red)
2. ROA (>10% green)
3. Profit Margin (>20% green)
4. **Operative Margin** (NOT "Operating" - >20% green)
5. Gross Margin (>40% green)
6. ROIC (>15% green)

### Growth Metrics (7)
1. Revenue Growth (YoY) - **REPORTED, not underlying**
2. Earnings Growth (YoY) - **REPORTED, not adjusted**
3. EPS (TTM)
4. Forward EPS
5. **Growth (Capped)** - Sustainable estimate
6. **Growth (Uncapped)** - Analyst headline
7. Analyst Target (€)

### Risk Indicators (6)
1. CRS (0-1): - Consolidated Risk Score (Medium label)
2. Debt/Equity (mrq): - with benchmark (0.5-1)
3. **Piotroski F:** - (NOT "F-Score") - ≥7 green
4. **Altman Z:** - (NOT "Z-Score") - >3 green
5. **Beneish M:** - (NOT "M-Score") - <-1.78 green
6. **Value Trap:** XX (Label) - 0-39 green, 40-59 yellow, 60-100 red

### Liquidity & Free Cash Flow (7)
1. Current Ratio: (1-2 benchmark)
2. **Cash:** (NOT "Total Cash")
3. **Debt:** (NOT "Total Debt")
4. FCF Growth 5Y: (>5% green)
5. FCF Yield: (>4% green)
6. **FCF Margin:** - FCF/Revenue %
7. Payout Ratio: (<50% green)

### Insider & Sentiment & Class (7)
1. **Buys (12M):** - from SEC Form 4 or N/A
2. **Sells (12M):** - from SEC Form 4 or N/A
3. **Net Shares (12M):** - from SEC Form 4 or N/A
4. **Short Int (%):** - from FINRA/exchange or N/A
5. **Sentiment / Articles:** +X.XXX / XX (Positive/Negative)
6. **Stock: [Type] + Div Yield:** - Combined in one cell
7. **Sector/Industry:** - Combined in one cell

### Quality Scores (6)
1. CQVS (Consolidated Quality & Valuation)
2. Label (Quality classification)
3. Valuation Score
4. Quality Score
5. Strength Score
6. Integrity Score

### Moat & Other (6)
1. **Buffett Moat:** X (4-7 benchmark)
2. **Greenblatt (MF):** EY: X.X% / ROC: X.X% or N/A - Combined
3. **Beta: X.XX + Vol 1Y: XX.X%** - Combined in one cell
4. **Earnings Predict.:** XX.X% (>80% green)
5. **Drawdown (5Y):** -XX.X% (Low/Mid/High)
6. **Completeness: XX.X% + Data Quality: High/Med/Low** - Combined

### Investor Persona Scores (8) - NEW
Displayed as badges around radar chart:
1. **Buffett Score** (0-10) - Quality compounder
2. **Munger Score** (0-10) - Risk-focused
3. **Dalio Score** (0-10) - All-weather
4. **Lynch Score** (0-10) - GARP
5. **Graham Score** (0-10) - Deep value
6. **Greenblatt Score** (0-10) - Magic Formula
7. **Templeton Score** (0-10) - Contrarian
8. **Soros Score** (0-10) - Momentum/macro

### Valuation Lines in Charts (6) - NEW
1. Market Value (Current)
2. Intrinsic Value (Current)
3. Market Value (Next Year)
4. Intrinsic Value (Next Year)
5. Unrestricted Market Value (Current)
6. Unrestricted Market Value (Next Year)

## Chart Details

### Linear Price Chart (Left) - 10 Years
- **Close Price** (solid line)
- **Total Return** (dashed - dividends reinvested)
- **Intrinsic Value lines** (green dashed)
- **Analyst Target** (blue dashed)
- **Legend with € values** for each line
- **MACD below** (blue MACD, red signal)

### Radar Chart + Investor Personas (Center Top)
12-point visualization (normalized 0-100):
1. Revenue Growth
2. Operating Margin
3. Gross Margin
4. Profit Margin
5. ROE
6. Risk Score (inverted)
7. Beta Score (inverted)
8. P/Market Discount
9. Moat Score
10. FCF Growth
11. ROA
12. Earnings Growth

**8 Investor Persona Badges positioned around perimeter:**
- Green badge (7-10): Strong fit
- Yellow badge (4-6.9): Moderate fit
- Red badge (0-3.9): Poor fit

### 1-Year + 6-Month Forecast (Center Bottom)
- **Close Price** (solid black)
- **50-Day MA** (orange)
- **200-Day MA** (red)
- **Bollinger Bands** (gray shading)
- **Forecast line** (green dashed)
- **95% Confidence Interval** (blue shading)
- **Valuation Indicator** (below chart):
  - "Undervalued (+XX%)" - green text
  - "Fairly Valued (+/-X%)" - yellow text
  - "Overvalued (-XX%)" - red text

### Log Price Chart (Right) - 10 Years
- **Close Price** (logarithmic scale)
- **Total Return** (dashed)
- **Unrestricted Market Value lines** (red/orange dashed)
- **Legend with € values**

### MACD + RSI (Right Bottom, Stacked)
**MACD** (top):
- MACD line (blue)
- Signal line (red)
- Buy Signal markers (green triangles)
- Zero reference line

**RSI (14)** (bottom):
- RSI line (orange)
- Reference lines at 30 and 70
- Current value displayed: "RSI (14) = XX.X"

### Ichimoku Cloud (Bottom) - NEW
- **Close Price** (thick black)
- **Tenkan-sen** (blue - 9-period conversion)
- **Kijun-sen** (red - 26-period base)
- **Chikou Span** (gray dashed - lagging)
- **Senkou Span A/B** (green/red cloud shading)
- **◆ Diamond markers** at signal points:
  - TK Bullish/Bearish Cross
  - Kumo Twist Bullish/Bearish
- **Signal summary** below chart

## Color Coding

### Value Trap Score Colors
- **Green** (0-39): Genuine value
- **Yellow** (40-59): Caution zone
- **Red** (60-100): Likely trap

### Investor Persona Badge Colors
- **Green** (7-10): Strong fit for investor type
- **Yellow** (4-6.9): Moderate fit
- **Red** (0-3.9): Poor fit

### News Sentiment Colors
- **Green** (>0.2): Positive coverage
- **Yellow** (-0.2 to 0.2): Neutral
- **Red** (<-0.2): Negative coverage

### Ichimoku Signal Colors
- **Green background**: Bullish signal
- **Yellow background**: Neutral
- **Red background**: Bearish signal

## Key Notes Section

Click the expandable accordion to see:

**Bull Case** (Green, left column):
- Upside price target (€)
- 5 key bull arguments
- What needs to happen

**Bear Case** (Red, center column):
- Downside price target (€)
- 5 key risk factors
- What could go wrong

**Entry/Exit Strategy** (Blue, right column):
- Ideal entry price range (€)
- Current entry assessment
- 12-month target (€)
- Stop loss level (€)
- Position size recommendation

## How to Read the Dashboard

### Quick Scan (30 seconds)
1. **TOP NEWS**: Recent headlines for context
2. **Header**: Ticker and company name
3. **Advice Badge** (center): Recommendation + CQVS score
4. **Value Trap Score**: Green = genuine, Red = avoid
5. **Color patterns**: Mostly green = strong
6. **Persona badges**: Which investors would like this stock?

### Medium Review (2-3 minutes)
1. Check all 8 sections for red flags
2. Review Value Trap score and rationale
3. Scan Investor Persona scores - who fits?
4. Check Ichimoku Cloud signals
5. Review price charts and trends
6. Note F-Score, Z-Score, M-Score

### Deep Analysis (5-10 minutes)
1. Expand Key Notes
2. Read Bull vs Bear cases
3. Review entry/exit strategy
4. Cross-reference with text analysis
5. Study Ichimoku signals and trends
6. Verify all metrics rationale
7. Consider which persona scores match your style

## Interpreting Investor Persona Scores

| High Scores In... | Stock Type | Best For |
|-------------------|------------|----------|
| Buffett + Munger | Quality compounder | Long-term holders |
| Lynch + Greenblatt | GARP opportunity | Growth-value blend |
| Graham + Templeton | Deep value | Contrarian investors |
| Dalio | Defensive/stable | Conservative portfolios |
| Soros | Momentum play | Active traders |

## Value Trap Quick Reference

| Score | Label | Action |
|-------|-------|--------|
| 0-19 | Genuine | Strong value candidate |
| 20-39 | Probably Genuine | Worth deep research |
| 40-59 | Caution | Investigate red flags |
| 60-79 | Likely Trap | Avoid unless special |
| 80-100 | Strong Trap | Avoid |

## Currency Note

**All monetary values are in € (Euro) by default:**
- Stock prices: €42.13
- Market caps: €78.3B
- Entry/stop/target prices: €38, €35, €56
- Valuation line values: €45.17, €49.59

## Remember

**The dashboard is a visual summary, not a standalone decision tool.**

- Always read the full text analysis
- Understand the reasoning behind metrics
- Consider your own investment criteria
- Use Investor Persona scores to match your style
- Trust Value Trap score for "cheap" stocks
- Ichimoku provides trend context
- Dashboards complement, not replace, analysis

**The enhanced format ensures:**
- Consistency across analyses
- Easy comparison between stocks
- Professional presentation
- Comprehensive 60+ metric coverage
- Multi-dimensional quality assessment
- Trend and momentum context
- Quick visual assessment
