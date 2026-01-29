---
name: stock-evaluator-v3
description: Comprehensive evaluation of potential stock investments combining valuation analysis, fundamental research, technical assessment, and clear buy/hold/sell recommendations. Use when the user asks about buying a stock, evaluating investment opportunities, analyzing watchlist candidates, or requests stock recommendations. Provides specific entry prices, position sizing, and conviction ratings.
---

# Stock Evaluator (Enhanced)

## ⚠️ CRITICAL: MANDATORY DELIVERABLES CHECKLIST
Every analysis MUST include ALL of these:
- ☐ **Technical Analysis** (price action, indicators, key levels, Ichimoku Cloud)
- ☐ **Fundamental Analysis** (business, financials, competitive position)
- ☐ **Advanced Financial Metrics** (F-Score, Z-Score, M-Score, Max Drawdown, Value Trap Score)
- ☐ **Investor Persona Scores** (8 legendary investor frameworks)
- ☐ **Valuation Assessment** (multiple methods with margin of safety)
- ☐ **Bull vs. Bear Case** (both sides with balance assessment)
- ☐ **Clear Recommendation** (BUY / HOLD / SELL with conviction rating)
- ☐ **Alternative Candidates** (if SELL: provide 3-5 better alternatives)
- ☐ **Enhanced Quant-Style Dashboard** (React dashboard with 60+ metrics, Ichimoku, investor personas, TOP NEWS, and key notes)

**If you cannot complete any item, STOP and ask for clarification.**

---

## ⚠️ CRITICAL: DATA INTEGRITY RULES

### ZERO FABRICATION POLICY
**NEVER fabricate, estimate, or hallucinate ANY numeric data point.** Every metric in the dashboard MUST come from:
1. A web search result with a cited source
2. Company filings (10-K, 10-Q, earnings reports)
3. Official financial data providers

**If data cannot be found → Use "N/A" or "--"**

### MANDATORY WEB SEARCHES (minimum per analysis)

You MUST perform these searches before populating the dashboard:

| Search # | Query Template | Data Retrieved |
|----------|---------------|----------------|
| 1 | "[TICKER] stock price market cap P/E ratio" | Price, Market Cap, P/E |
| 2 | "[TICKER] ROE ROA profit margin 2024 annual report" | Financial ratios |
| 3 | "[TICKER] revenue growth earnings growth FY2024" | Growth rates (REPORTED) |
| 4 | "[TICKER] Piotroski F-Score" | F-Score (or calculate) |
| 5 | "[TICKER] insider trading SEC Form 4 2025" | Insider buys/sells |
| 6 | "[TICKER] short interest percentage float" | Short interest |
| 7 | "[TICKER] RSI MACD 50-day 200-day moving average beta volatility" | Technical indicators |
| 8 | "[TICKER] analyst price target consensus" | Analyst targets |

### DATA SOURCE HIERARCHY

Use sources in this priority order:
1. **Official company filings** (SEC EDGAR, company investor relations)
2. **Exchange data** (NYSE, NASDAQ, LSE official)
3. **Verified financial data** (Yahoo Finance, Google Finance, MarketWatch)
4. **SEC Form 4** (for insider trading ONLY)
5. **FINRA/exchange** (for short interest ONLY)

### PROHIBITED
- Using training knowledge for ANY specific current numbers
- Analyst reports (per user preference)
- Estimates without sourcing
- "Common knowledge" assumptions

### HANDLING UNAVAILABLE DATA

| Situation | Action | Display |
|-----------|--------|---------|
| Metric not found after searching | Display "N/A" | `value: "N/A"` |
| Data is outdated (>1 year old) | Note the date | `value: "15.2% (2023)"` |
| Conflicting sources | Use most authoritative | Note in analysis |
| Calculated metric (F-Score) | Show calculation | Explain in text |
| Insider data unavailable | Show "N/A" | `insBuys: "N/A"` |

**CRITICAL: Zero means "zero occurred" - NEVER substitute zeros for missing data.**

---

## STANDARDIZED METRIC LABELS

Use these EXACT labels in the dashboard (matches reference screenshots):

### Row 1: PRICE & VALUATION | FINANCIAL PERFORMANCE
| Label | Notes |
|-------|-------|
| Price: | $XX.XX or €XX.XX |
| Market Cap: | $XXB or €XXB |
| Trailing P/E: | XX.XX |
| Forward P/E: | XX.XX |
| Subsector P/E: | XX.XX or N/A |
| PEG (1Y): | X.XX with benchmark (<1) |
| ROE: | XX.XX% with benchmark (>20%) |
| ROA: | XX.XX% with benchmark (>10%) |
| Profit Margin: | XX.XX% with benchmark (>20%) |
| Operative Margin: | XX.XX% with benchmark (>20%) - NOTE: "Operative" not "Operating" |
| Gross Margin: | XX.XX% with benchmark (>40%) |
| ROIC: | XX.X% with benchmark (>15%) |

### Row 2: GROWTH METRICS | RISK INDICATORS
| Label | Notes |
|-------|-------|
| Revenue (YoY): | XX.XX% with benchmark (>10%) - REPORTED only |
| Earning (YoY): | XX.XX% with benchmark (>0%) - REPORTED only |
| EPS (TTM): | $X.XX |
| Forward EPS: | $X.XX |
| Growth Rates: | Capped: X.X% / Uncapped: X.X% |
| Analyst Target: | $XX.XX |
| CRS (0-1): | X.XX with benchmark (Medium) |
| Debt/Equity (mrq): | X.XX with benchmark (0.5-1) |
| Piotroski F: | X with benchmark (≥7) |
| Altman Z: | X.XX with benchmark (>3) |
| Beneish M: | X.XX with benchmark (<-1.78) |
| Value Trap: | XX (Label) |

### Row 3: LIQUIDITY & FREE CASH FLOW | INSIDER & SENTIMENT & CLASS
| Label | Notes |
|-------|-------|
| Current Ratio: | X.XX with benchmark (1-2) |
| Cash: | $X.XB |
| Debt: | $X.XB or N/A |
| FCF Growth 5Y: | XX.X% with benchmark (>5%) |
| FCF Yield: | X.XX% with benchmark (>4%) |
| FCF Margin: | XX.XX% with benchmark (>15%) |
| Payout Ratio: | XX.XX% with benchmark (<50%) |
| Buys (12M): | X - from SEC Form 4 or N/A |
| Sells (12M): | X - from SEC Form 4 or N/A |
| Net Shares (12M): | +/-XXK - from SEC Form 4 or N/A |
| Short Int (%): | X.X% |
| Sentiment / Articles: | +X.XXX / XX (Positive/Negative) |
| Stock: [Type] + Div Yield: | Combined: "Stock: Growth" + "Div Yield: X.XX%" |
| Sector/Industry: | Combined: "Sector / Industry" |

### Row 4: QUALITY SCORES | MOAT & OTHER
| Label | Notes |
|-------|-------|
| CQVS: | XX.XX with benchmark range |
| Label: | Strong/Moderate/Weak |
| Valuation: | XX.XX |
| Quality: | XX.XX |
| Strength: | XX.XX |
| Integrity: | XX.XX |
| Buffett Moat: | X with benchmark (4-7) |
| Greenblatt (MF): | EY: X.X% / ROC: X.X% or N/A |
| Beta: + Vol 1Y: | Combined: "Beta: X.XX" + "Vol 1Y: XX.X%" |
| Earnings Predict.: | XX.X% with benchmark (>80%) |
| Drawdown (5Y): | -XX.X% with label (Low/Mid/High) |
| Completeness: + Data Quality: | Combined: "XX.X%" + "High/Medium/Low" |

---

## STANDARDIZED BENCHMARKS (Single Source of Truth)

Use these EXACT thresholds for color coding:

| Metric | Green (Good) | Yellow (Neutral) | Red (Warning) |
|--------|--------------|------------------|---------------|
| **ROE** | >20% | 10-20% | <10% |
| **ROA** | >10% | 5-10% | <5% |
| **Profit Margin** | >20% | 10-20% | <10% |
| **Operative Margin** | >20% | 10-20% | <10% |
| **Gross Margin** | >40% | 25-40% | <25% |
| **ROIC** | >15% | 8-15% | <8% |
| **Debt/Equity** | <1 | 1-2 | >2 |
| **Current Ratio** | 1-2 | 0.5-1 or 2-3 | <0.5 or >3 |
| **Piotroski F** | ≥7 | 4-6 | ≤3 |
| **Altman Z** | >2.99 | 1.81-2.99 | <1.81 |
| **Beneish M** | <-2.22 | -2.22 to -1.78 | >-1.78 |
| **PEG (1Y)** | <1 | 1-2 | >2 |
| **RSI (14)** | 30-50 | 50-70 | >70 or <30 |
| **Short Interest** | <5% | 5-10% | >10% |
| **FCF Yield** | >5% | 2-5% | <2% |
| **FCF Margin** | >15% | 10-15% | <10% |
| **Dividend Yield** | >2% | 1-2% | <1% or >8% |
| **Value Trap** | 0-39 | 40-59 | 60-100 |
| **Max Drawdown** | >-30% | -30% to -50% | <-50% |
| **Revenue Growth** | >10% | 0-10% | <0% |
| **Earnings Growth** | >0% | -10% to 0% | <-10% |

---

## Overview

This skill provides institutional-grade evaluation of potential stock investments. Unlike portfolio analysis which reviews existing positions, this skill evaluates stocks you're **considering buying** or **deciding whether to purchase**.

The evaluation answers:
- **Should I buy this stock?**
- **At what price should I enter?**
- **How much should I allocate?**
- **What's my upside and downside?**
- **When should I sell?**

### Default Currency: € (Euro)
All monetary values in the dashboard should be displayed in **Euro (€)** as the default currency:
- Price: €42.13
- Market Cap: €78.3B
- Analyst Target: €56.45
- Entry/Stop/Target prices: €38, €35, €56
- EPS values: €1.39, €1.91

### IMPORTANT: Use REPORTED Growth Rates
For the dashboard metrics **"Rev Growth"** and **"Earn Growth"**:
- **USE REPORTED GROWTH** - not underlying, adjusted, or organic figures
- Reported figures reflect actual GAAP/IFRS numbers including FX, acquisitions, disposals
- This provides a more accurate picture of what investors actually received
- Example: If underlying growth is 7% but reported is 2.2%, use **2.2%**
- Same for earnings: Use reported EPS growth, not adjusted EPS growth

## Core Purpose

**Stock Evaluator** is for:
- ✅ Evaluating potential investments BEFORE buying
- ✅ Analyzing watchlist candidates
- ✅ Getting buy/hold/sell recommendations with specific prices
- ✅ Comparing multiple investment opportunities
- ✅ Finding better alternatives to current consideration

**NOT for:**
- ❌ Reviewing existing portfolio positions (use Portfolio Analyst skill)
- ❌ General stock market questions
- ❌ Stock screening or discovery from scratch
- ❌ Options, derivatives, or crypto analysis

## Evaluation Framework

### Five Pillars of Stock Evaluation

**1. Valuation Assessment**
- Is the stock undervalued, fairly valued, or overvalued?
- Multiple valuation methods (DCF, relative, Peter Lynch, asset-based)
- Margin of safety requirement (15-30%)
- Fair value estimate with confidence range

**2. Quality Analysis**
- Business model strength and competitive moat
- Financial health and trends (5-10 year view)
- Management quality and capital allocation
- Industry position and competitive advantages

**3. Timing Assessment**
- Technical setup and entry points
- Near-term catalysts and events
- Market sentiment and positioning
- Optimal entry price range

**4. Position Sizing**
- Allocation recommendation (% of portfolio)
- Based on conviction, risk, and diversification
- Maximum allocation limits
- Risk-adjusted sizing

**5. Conviction Rating**
- **Strong Buy**: High conviction, clear undervaluation, low risk
- **Buy**: Good opportunity, reasonable valuation, moderate risk
- **Hold**: Fairly valued, no compelling reason to buy now
- **Avoid**: Overvalued, significant risks, or better alternatives exist

---

## Value Trap Indicator

### What It Is
A Value Trap is when a stock appears undervalued (low P/E, low P/B) but is actually cheap for valid fundamental reasons. The stock keeps declining despite appearing "cheap."

### Value Trap Score Calculation (0-100, LOWER = more genuine, HIGHER = more trap)

**Components to evaluate (ADD points for trap indicators):**

**1. Price Momentum (25 points max)**
- 6-month price change vs market: If underperforming by >20%, ADD 15-25 points
- 12-month price change: Sustained decline = ADD 10-20 points
- If price momentum is POSITIVE: ADD 0 points

**2. Earnings Quality (25 points max)**
- EPS trend (3 years): Declining = ADD 10-25 points
- Revenue trend: Declining = ADD 5-15 points
- Margin trend: Compressing = ADD 5-10 points
- If earnings quality is STRONG: ADD 0 points

**3. Balance Sheet Health (25 points max)**
- Debt levels increasing? ADD 5-15 points
- Cash flow negative or declining? ADD 10-20 points
- Working capital deteriorating? ADD 5-10 points
- If balance sheet is HEALTHY: ADD 0 points

**4. Valuation Context (25 points max)**
- Is low multiple justified by declining fundamentals? ADD 10-25 points
- Compare current fundamentals to when multiple was higher
- If fundamentals justify valuation: ADD 0 points

### Scoring Formula
```
Value Trap Score = Momentum Penalty + Quality Penalty + Balance Sheet Penalty + Valuation Penalty
```
(Score ranges from 0 to 100, where 0 = definitely genuine value, 100 = definite value trap)

### Score Interpretation
- **0-19**: Genuine Value (likely undervalued, fundamentals intact) - GREEN
- **20-39**: Probably Genuine (minor concerns, monitor) - LIGHT GREEN
- **40-59**: Caution Zone (mixed signals, proceed carefully) - YELLOW
- **60-79**: Likely Trap (multiple red flags) - ORANGE
- **80-100**: Strong Trap Signal (avoid) - RED

### Display Format
```
Value Trap: 21 (Genuine)
```
Color coding: green <40, yellow 40-60, red >60

---

## Investor Persona Scores

Score each stock against 8 famous investor philosophies (0-10 scale). This helps users understand what type of investor the stock suits.

### 1. Warren Buffett Score
Based on "The Warren Buffett Way" - seeks durable competitive advantages

**Key metrics weighted:**
- ROE (>20%): 2 points
- Profit margin (>15%): 2 points
- Free cash flow positive & growing: 2 points
- Moat strength (brand, pricing power): 2 points
- Predictable earnings: 2 points

**Buffett likes:** Predictable businesses, pricing power, low capex needs, consistent profitability

### 2. Charlie Munger Score
Based on "Poor Charlie's Almanack" - mental latticework, inversion thinking

**Focus on:** What could go WRONG (inversion principle)

**Scoring:** Start at 10, subtract penalties:
- High debt (D/E > 2): -3 points
- Volatile earnings: -2 points
- Poor management history: -2 points
- No competitive moat: -2 points
- Accounting red flags: -3 points

### 3. Ray Dalio Score
Based on "Principles" - All-Weather portfolio, economic machine understanding

**Key metrics:**
- D/E ratio < 1: 2 points
- Beta < 1: 2 points
- Stable margins across cycles: 2 points
- Low earnings volatility: 2 points
- Recession resistance history: 2 points

**Dalio likes:** Deleveraging plays, operational efficiency, cycle resilience

### 4. Peter Lynch Score
Based on "One Up on Wall Street" - GARP (Growth at Reasonable Price)

**Primary metric: PEG Ratio (P/E ÷ Growth Rate)**
- PEG < 0.5: 10 points
- PEG 0.5-1.0: 8 points
- PEG 1.0-1.5: 6 points
- PEG 1.5-2.0: 4 points
- PEG > 2.0: 2 points

**Adjustment factors:**
- +1 if earnings growing consistently
- +1 if business easy to understand
- -1 if declining industry

### 5. Benjamin Graham Score
Based on "The Intelligent Investor" - Margin of Safety

**Graham criteria (2 points each, max 10):**
- P/E < 15
- P/B < 1.5
- Current ratio > 2
- Positive earnings 10 years
- Dividend paid 20+ years

### 6. Joel Greenblatt Score
Based on "The Little Book That Beats the Market" - Magic Formula

**Combines two rankings:**
- Earnings Yield (EBIT/EV): Higher = better
- Return on Capital (EBIT/Net Fixed Assets + Working Capital): Higher = better

**Scoring:** Combined rank in top 10% = 10 points, scaled down

### 7. John Templeton Score
Based on contrarian, global value investing

**Key factors:**
- Trading at multi-year lows: +3 points
- Out of favor with analysts: +2 points
- Strong fundamentals despite pessimism: +3 points
- Global perspective (non-US opportunity): +2 points

### 8. George Soros Score
Based on "The Alchemy of Finance" - Reflexivity

**Key factors:**
- Momentum and trend strength: 3 points
- Macro tailwinds: 3 points
- Market perception shifting: 2 points
- Inflection point catalyst: 2 points

**Soros likes:** Macro plays, reflexive situations, trend participation

### Display Format
Show 8 badges around radar chart with scores and color coding:
- Green (7-10): Strong fit
- Yellow (4-6.9): Moderate fit
- Red (0-3.9): Poor fit

---

## Enhanced Technical Analysis

### Ichimoku Cloud Analysis

**Components to Calculate:**
- **Tenkan-sen (Conversion Line):** (9-period high + 9-period low) / 2
- **Kijun-sen (Base Line):** (26-period high + 26-period low) / 2
- **Senkou Span A:** (Tenkan-sen + Kijun-sen) / 2, plotted 26 periods ahead
- **Senkou Span B:** (52-period high + 52-period low) / 2, plotted 26 periods ahead
- **Chikou Span (Lagging Span):** Current close plotted 26 periods back

**Cloud (Kumo):** Area between Senkou Span A and B

**Signals to Identify and Display:**
- **TK Bullish Cross:** Tenkan-sen crosses above Kijun-sen (bullish) - mark with ◆
- **TK Bearish Cross:** Tenkan-sen crosses below Kijun-sen (bearish) - mark with ◆
- **Kumo Twist Bullish:** Cloud changes from red to green - mark with ◆
- **Kumo Twist Bearish:** Cloud changes from green to red - mark with ◆
- **Price vs Cloud:** Above cloud (bullish), Below cloud (bearish), In cloud (neutral)

### Dual PEG Ratios
- **PEG (1Y):** P/E ÷ 1-Year Forward Growth Estimate
- **PEG (5Y):** P/E ÷ 5-Year Historical Growth Rate
- Both provide different perspectives on growth valuation

### FCF Margin
- **Formula:** Free Cash Flow / Revenue × 100
- **Benchmark:** >15% is excellent, >10% is good
- Shows cash generation efficiency relative to sales

### News Sentiment & Short Interest
- **News Sentiment:** -1 to +1 scale based on recent article sentiment
- **Short Interest:** % of float sold short (>10% = high, <5% = low)
- Both indicate market sentiment and potential squeeze/reversal

---

## Fundamental Analysis Process

### 1. Business Understanding (Always First)

**What to Analyze:**
- What does the company do? (products, services, business model)
- Revenue sources and breakdown
- Target customers and markets
- Competitive advantages (moat sources)
- Market position and share
- Industry dynamics and trends

**Management Evaluation:**
- CEO background, tenure, track record
- CFO and key executives
- Capital allocation decisions (dividends, buybacks, acquisitions, R&D)
- Management compensation alignment
- Insider trading patterns (buying is bullish signal)
- Leadership quality from earnings calls and letters

**Competitive Position:**
- Market share and trends
- Key competitors (identify 3-5 direct peers)
- What differentiates this company?
- Sustainable competitive advantages?

### 2. Financial Analysis (5-10 Year View)

**Research Process Order:**
1. **Latest 10-K first** - Understand current business and recent results
2. **Go back 5-10 years through historical 10-Ks** - Understand evolution
3. **Review last 2-3 years of 10-Qs** - Current trajectory
4. **Examine proxy statements** - Governance and compensation

**Key Metrics to Analyze:**

**Quality Benchmarks:**
- ROE > 15% (return on equity)
- Profit Margin > 15%
- Gross Margin > 30%
- Debt < Annual Revenue
- Positive and growing Free Cash Flow
- Revenue growth over 5 years (inflation-adjusted)

**Trends to Assess:**
- Revenue growth trajectory (accelerating/stable/decelerating?)
- Margin expansion or contraction (why?)
- Cash flow consistency and quality
- Balance sheet strength (debt levels, liquidity)
- Return on invested capital (ROIC)
- Working capital management

**Red Flags:**
- Declining margins despite revenue growth
- Negative or inconsistent free cash flow
- Debt growing faster than cash generation
- Losing market share
- Chronic guidance misses
- Accounting irregularities

### 3. Competitive Moat Assessment

**Moat Strength: Wide / Narrow / None**

**Evaluate Sources:**
- **Network effects**: Product improves with more users?
- **Brand loyalty**: Pricing power from brand strength?
- **Switching costs**: Difficult/expensive to switch?
- **Regulatory barriers**: Licenses, patents, regulations?
- **Cost advantages**: Scale, technology, location?
- **Intangible assets**: Patents, trademarks, proprietary data?

**Moat Durability:**
- How long can advantages be sustained?
- What could erode the moat?
- Is moat strengthening or weakening?

**Peer Comparison:**
Compare this company's moat vs. 3-5 direct competitors:
- Market share trends
- Profitability metrics (margins, ROE)
- Growth rates
- Financial strength

### 4. Advanced Financial Health Metrics

Beyond basic quality metrics, calculate these advanced scores for deeper insight:

**Piotroski F-Score (Financial Strength)**

**Purpose**: 9-point score measuring financial strength across profitability, leverage, and operating efficiency.

**Scoring (0-9, higher is better):**

*Profitability (4 points):*
- ROA > 0: +1
- Operating Cash Flow > 0: +1
- ROA improving YoY: +1
- Cash Flow from Operations > Net Income (quality of earnings): +1

*Leverage/Liquidity (3 points):*
- Long-term debt decreasing YoY: +1
- Current ratio improving YoY: +1
- No new shares issued in past year: +1

*Operating Efficiency (2 points):*
- Gross margin improving YoY: +1
- Asset turnover ratio improving YoY: +1

**Interpretation:**
- **8-9**: Excellent financial health
- **6-7**: Good financial health
- **4-5**: Adequate financial health
- **0-3**: Weak financial health

**Altman Z-Score (Bankruptcy Risk)**

**Purpose**: Predicts probability of bankruptcy within 2 years.

**Formula (for public manufacturing companies):**
Z = 1.2(A) + 1.4(B) + 3.3(C) + 0.6(D) + 1.0(E)

Where:
- A = Working Capital / Total Assets
- B = Retained Earnings / Total Assets
- C = EBIT / Total Assets
- D = Market Cap / Total Liabilities
- E = Sales / Total Assets

**Interpretation:**
- **Z > 2.99**: Safe Zone (low bankruptcy risk)
- **Z 1.81-2.99**: Grey Zone (moderate risk)
- **Z < 1.81**: Distress Zone (high bankruptcy risk)

**Note**: Adjust for non-manufacturing companies (different coefficients).

**Beneish M-Score (Earnings Manipulation Detection)**

**Purpose**: Identifies likelihood of earnings manipulation.

**Key Indicators (simplified approach):**
- Days Sales Outstanding Index (increasing = warning)
- Gross Margin Index (declining = warning)
- Asset Quality Index (increasing = warning)
- Sales Growth Index (excessive growth = warning)
- Depreciation Index (declining = warning)
- SG&A Index (disproportionate change = warning)
- Leverage Index (increasing = warning)
- Total Accruals to Total Assets (high = warning)

**Interpretation:**
- **M-Score > -1.78**: Likely manipulator (RED FLAG)
- **M-Score < -1.78**: Unlikely manipulator (clean)

**Practical Check (if full M-Score unavailable):**
- Are accruals consistently high relative to cash flow?
- Is DSO rising faster than revenue?
- Are margins declining with revenue growth?
- Any accounting restatements or auditor changes?

**Max Drawdown (5-Year)**

**Purpose**: Measures largest peak-to-trough price decline.

**Calculation:**
- Identify highest price in past 5 years
- Find lowest subsequent price before recovery
- Max Drawdown % = (Low - High) / High × 100

**Interpretation:**
- **0-20%**: Low volatility (defensive stock)
- **20-40%**: Moderate volatility (typical stock)
- **40-60%**: High volatility (cyclical/growth)
- **>60%**: Extreme volatility (speculative)

**Consolidated Scores**

**Strength Score (0-100):**
Composite of:
- Financial metrics (F-Score contribution)
- Profitability (ROE, margins)
- Growth rates
- Market position

**Integrity Score (0-100):**
Composite of:
- M-Score (earnings quality)
- Cash flow vs. earnings alignment
- Accounting practices
- Management transparency

**Predictability Score (0-100):**
Composite of:
- Revenue consistency (low volatility)
- Earnings consistency
- Business model stability
- Cyclicality assessment

**Data Quality Score (0-100):**
- Completeness of financial data
- Recency of filings
- Auditor quality
- Disclosure transparency

### 5. Risk Analysis

**Company-Specific Risks:**
- Execution risk (can management deliver?)
- Competition risk (share loss, new entrants)
- Product concentration (single product dependency)
- Customer concentration (few large customers)
- Key person risk (CEO dependency)
- Financial distress risk (Z-Score assessment)
- Earnings quality risk (M-Score assessment)

**Industry Risks:**
- Disruption (technology or business model)
- Cyclicality (economic sensitivity)
- Regulation (policy changes)
- Commoditization (pricing power erosion)
- Structural decline (secular headwinds)

**Macro Risks:**
- Economic (recession, inflation, rates)
- Geopolitical (trade wars, conflicts)
- Currency (FX exposure)
- Market (valuation levels, sentiment)

**Overall Risk Level: Low / Moderate / High**

**Consolidated Risk Score:** (0-1 scale, lower is better)
- Incorporates: Z-Score, volatility, leverage, earnings quality
- <0.30: Low Risk
- 0.30-0.60: Moderate Risk
- >0.60: High Risk

---

## Valuation Assessment

Use **multiple valuation methods** - synthesize into fair value estimate.

### Required Valuation Methods

**1. DCF Analysis (Discounted Cash Flow)**
- Project free cash flows (5-10 years)
- Apply appropriate discount rate (WACC)
- Calculate terminal value
- Include margin of safety: 15-30%
- Sensitivity analysis with different assumptions

**2. Relative Valuation**
- Compare to 3-5 direct peer companies
- Key multiples: P/E, EV/EBITDA, Price/Sales, Price/Book
- Adjust for growth differentials
- Consider industry-specific multiples
- Use both current and historical peer averages

**3. Peter Lynch Fair Value**
- Growth-at-reasonable-price framework
- Compare P/E to growth rate (PEG ratio)
- Fair value when P/E ≈ growth rate
- Adjust for quality factors

**4. Asset-Based (When Applicable)**
- For REITs, financials, asset-heavy companies
- Book value or replacement cost
- Net asset value calculations

### Valuation Synthesis

**Fair Value Estimate: €X.XX**

Weight each method appropriately:
- DCF: 40% (if reliable cash flows)
- Relative: 30% (peer comparison)
- Peter Lynch: 30% (growth-adjusted)

**Margin of Safety:**
- **Current Price vs. Fair Value**: X% discount/premium
- **Required**: Minimum 15% margin of safety
- **Adequate**: 15-30% margin of safety
- **Excellent**: >30% margin of safety

**Valuation Conclusion:**
- **UNDERVALUED**: >15% below fair value (buy opportunity)
- **FAIRLY VALUED**: Within ±15% of fair value (hold)
- **OVERVALUED**: >15% above fair value (avoid/sell)

---

## Technical Analysis (Entry Timing)

Focus on identifying optimal entry points, not full technical analysis.

### Key Technical Elements

**1. Price Action (Last 30-60 Days)**
- Current trend: Uptrend / Downtrend / Range-bound
- Recent price pattern
- Volume trends (increasing on rallies?)
- Momentum assessment

**2. Key Levels**
- **Support levels**: Where buying interest emerges
  - Primary support: €X.XX
  - Secondary support: €X.XX
- **Resistance levels**: Where selling pressure increases
  - Primary resistance: €X.XX
  - Secondary resistance: €X.XX

**3. Technical Indicators**
- **RSI** (Relative Strength Index):
  - >70 = Overbought (may pullback)
  - <30 = Oversold (potential bounce)
  - 40-60 = Neutral
- **MACD** (Moving Average Convergence Divergence):
  - Bullish crossover / Bearish crossover / Neutral
  - Momentum accelerating or decelerating?
- **Moving Averages**:
  - 50-day MA: €X.XX (price above/below?)
  - 200-day MA: €X.XX (trend indicator)

**4. Entry Assessment**
- **Technical Setup**: Bullish / Neutral / Bearish
- **Optimal Entry**: Wait for pullback to support / Buy at market / Wait for breakout
- **Entry Price Range**: €X.XX - €X.XX
- **Avoid Above**: €X.XX (poor risk/reward)

---

## Bull vs. Bear Case Analysis

**MANDATORY**: Every analysis must present both sides fairly.

### Bull Case (Optimistic Scenario)
**Potential Upside: +X% to €X.XX**

1. [Key bull argument 1 with specific evidence]
2. [Key bull argument 2 with specific evidence]
3. [Key bull argument 3 with specific evidence]

**For this to play out:**
- [Required condition 1]
- [Required condition 2]

### Bear Case (Pessimistic Scenario)
**Potential Downside: -X% to €X.XX**

1. [Key bear argument 1 with specific evidence]
2. [Key bear argument 2 with specific evidence]
3. [Key bear argument 3 with specific evidence]

**This happens if:**
- [Risk trigger 1]
- [Risk trigger 2]

### Balance Assessment
**Which case is more probable: [Bull / Bear / Balanced]**

[Explanation of why one case is more likely, considering:
- Quality of evidence for each side
- Historical precedent
- Management track record
- Industry dynamics
- Current valuation]

---

## Investment Recommendation Structure

### BUY Recommendation Criteria
- Fair value >15% above current price (adequate margin of safety)
- Strong or improving fundamentals
- Reasonable or bullish technical setup
- Identifiable catalysts
- Acceptable risk level
- Conviction: Strong Buy or Buy

### HOLD Recommendation Criteria
- Fair value within ±15% of current price
- Stable fundamentals, no compelling catalyst
- Better opportunities may exist elsewhere
- Wait for better entry price
- Conviction: Hold

### SELL/AVOID Recommendation Criteria
- Fair value <-15% below current price (overvalued)
- Deteriorating fundamentals
- Significant risks
- Better alternatives available
- Must provide 3-5 alternative candidates
- Conviction: Avoid

---

## Position Sizing Framework

**Allocation recommendation based on:**

**Conviction + Risk = Position Size**

**Strong Buy (High Conviction, Low Risk):**
- Position size: 5-8% of portfolio
- Maximum: 10%

**Buy (Moderate Conviction, Moderate Risk):**
- Position size: 3-5% of portfolio
- Maximum: 7%

**Speculative/High Risk:**
- Position size: 1-3% of portfolio
- Maximum: 5%

**Considerations:**
- Diversification needs (avoid sector concentration)
- Correlation with existing holdings
- Overall portfolio risk
- Liquidity requirements
- User's risk tolerance (from project context)

---

## Entry and Exit Strategy

### Entry Strategy

**NO scale-in strategies** - recommend single entry approach:

**If BUY:**
- **Ideal Entry Price: €X.XX - €X.XX** (optimal range)
- **Maximum Buy Price: €X.XX** (above this, risk/reward unfavorable)
- **Approach:**
  - "Buy now at market" (if currently at good price)
  - "Wait for pullback to €X.XX support" (if extended)
  - "Buy on break above €X.XX" (if breakout setup)
  - "Don't buy above €X.XX" (if overvalued)

### Exit Strategy

**Price Target (12-month):** €X.XX (+X% upside)
- Conservative: €X.XX
- Base case: €X.XX
- Optimistic: €X.XX

**Stop Loss:** €X.XX (-X% maximum loss)
- Technical stop: Below key support
- Fundamental stop: If thesis breaks

**Sell If (Thesis-Breaking Conditions):**
1. [Specific fundamental deterioration]
2. [Specific competitive threat]
3. [Specific valuation threshold]

**Hold Duration:**
- Expected timeframe: [6-12 months / 1-3 years / 3-5+ years]
- Based on investment type (swing trade vs long-term hold)

---

## Catalyst Identification

Identify specific events that could drive stock performance.

**Near-Term (0-6 months):**
- Upcoming earnings: [Date]
- Product launches: [Event]
- Regulatory decisions: [Expected timing]
- Industry events: [Conference, data release]

**Medium-Term (6-18 months):**
- Market expansion plans
- New product cycles
- Margin expansion initiatives
- Strategic partnerships

**Long-Term (18+ months):**
- Structural industry trends
- Market share gains
- Technological leadership
- Business model evolution

---

## Key Analytical Constraints

**Critical Principles:**

1. **No Press/News for Fundamental Analysis**
   - Use company filings only (10-K, 10-Q, 8-K, proxy)
   - Use earnings call transcripts
   - Do NOT rely on news articles or press releases
   - Exception: News for recent developments, but verify in filings

2. **Magnitude Over Precision**
   - Focus on stocks with good margin of safety (>15%)
   - Don't need perfect forecasts
   - Better to be approximately right than precisely wrong
   - Conservative assumptions better than optimistic

3. **Long-Term View**
   - Analyze 5-10 year trends, not just recent quarters
   - Temporary setbacks vs. structural problems
   - Sustainable competitive advantages matter most
   - Short-term noise vs. long-term signal

4. **Compare Apples to Apples**
   - Benchmark against 3-5 direct competitors
   - Not just broad market indices
   - Industry-specific metrics and norms
   - Adjust for company size and maturity

5. **Intellectual Honesty**
   - Acknowledge limitations and unknowns
   - Present both bull and bear cases fairly
   - Say "I don't know" when appropriate
   - Update views when evidence changes

---

## Output Template

```markdown
# [SYMBOL] - [Company Name] Evaluation

## ⚠️ DELIVERABLES CHECKLIST ✓
☑ Technical Analysis Complete
☑ Fundamental Analysis Complete
☑ Valuation Assessment Complete
☑ Bull vs. Bear Case Complete
☑ Clear Recommendation: **[BUY / HOLD / SELL]**
☑ Alternative Candidates: [If SELL, list 3-5 alternatives below]

---

## 📊 Executive Summary

[2-3 sentence bottom-line assessment with key reasoning]

**Recommendation: [BUY / HOLD / SELL]**
**Conviction: [Strong Buy / Buy / Hold / Avoid]**

---

## 💰 Valuation Assessment

**Fair Value Estimate: €X.XX** (Current: €X.XX)
- **Margin of Safety: X%** [Adequate >15% / Insufficient <15%]
- **Valuation: [UNDERVALUED / FAIRLY VALUED / OVERVALUED]**

| Valuation Method | Fair Value | vs. Current | Weight |
|-----------------|-----------|-------------|--------|
| DCF Analysis | €X.XX | +X% | 40% |
| Peer Relative | €X.XX | +X% | 30% |
| Peter Lynch | €X.XX | +X% | 30% |
| **Weighted Average** | **€X.XX** | **+X%** | **100%** |

**Assumptions:**
- DCF: [Key assumptions - growth rate, margins, discount rate]
- Margin of safety applied: X%

---

## 🏢 Business & Competitive Analysis

### What They Do
[2-3 paragraph business model summary:
- Core products/services
- Revenue breakdown
- Target markets
- Business model]

### Competitive Advantages
**Moat Strength: [Wide / Narrow / None]**

1. **[Advantage 1]**: [Detailed explanation with evidence]
2. **[Advantage 2]**: [Detailed explanation with evidence]
3. **[Advantage 3]**: [Detailed explanation with evidence]

**Moat Durability:** [How sustainable are these advantages? 3-5 years? 10+ years?]

### Management Quality Assessment
**Overall Rating: [Excellent / Good / Adequate / Concerning]**

- **CEO**: [Name] - [Background, tenure]
  - Track record: [Achievements/concerns]
  - Capital allocation: [Shareholder-friendly? Smart acquisitions?]
- **CFO**: [Name] - [Financial stewardship]
- **Insider Trading**: [Recent buying/selling activity]
- **Key Insight**: [Overall management assessment]

### Competitive Position

**Market Position:**
- Market share: X% (#X in industry)
- Share trend: [Gaining / Stable / Losing]

**Key Competitors:** [List 3-5 direct peers]

**Peer Comparison:**
| Company | Mkt Cap | Revenue Growth | Profit Margin | ROE | P/E | Moat |
|---------|---------|---------------|---------------|-----|-----|------|
| [Target] | €XB | X% | X% | X% | X.X | [Rating] |
| [Peer 1] | €XB | X% | X% | X% | X.X | [Rating] |
| [Peer 2] | €XB | X% | X% | X.X | X.X | [Rating] |
| [Peer 3] | €XB | X% | X% | X% | X.X | [Rating] |

**Competitive Assessment:** [Is this the best company in the sector?]

---

## 📈 Financial Health Analysis

### Quality Metrics vs. Benchmarks

| Metric | Current | 1Y Ago | 3Y Ago | 5Y Ago | Target | Status |
|--------|---------|--------|--------|--------|--------|--------|
| ROE | X% | X% | X% | X% | >15% | [✓/✗] |
| Profit Margin | X% | X% | X% | X% | >15% | [✓/✗] |
| Gross Margin | X% | X% | X% | X% | >30% | [✓/✗] |
| Revenue Growth | X% | X% | X% | X% | >0% | [✓/✗] |
| Debt/Revenue | X.X | X.X | X.X | X.X | <1.0 | [✓/✗] |
| FCF | €XM | €XM | €XM | €XM | Positive | [✓/✗] |

### Advanced Financial Health Scores

**Piotroski F-Score: X/9** [Excellent 8-9 / Good 6-7 / Adequate 4-5 / Weak 0-3]

*Profitability:* X/4
- ROA positive: [✓/✗]
- Operating CF positive: [✓/✗]
- ROA improving: [✓/✗]
- CF > Net Income: [✓/✗]

*Leverage:* X/3
- Debt decreasing: [✓/✗]
- Current ratio improving: [✓/✗]
- No dilution: [✓/✗]

*Efficiency:* X/2
- Margin improving: [✓/✗]
- Turnover improving: [✓/✗]

**Assessment:** [Detailed interpretation of F-Score]

**Altman Z-Score: X.XX** [Safe >2.99 / Grey 1.81-2.99 / Distress <1.81]
- **Bankruptcy Risk:** [Low / Moderate / High]
- **Interpretation:** [Explanation of Z-Score and financial stability]

**Beneish M-Score: X.XX** [Clean <-1.78 / Warning >-1.78]
- **Earnings Quality:** [High / Moderate / Questionable]
- **Red Flags:** [List any concerning indicators or state "None"]

**Max Drawdown (5Y): -X%** [Low <20% / Moderate 20-40% / High 40-60% / Extreme >60%]
- **Volatility Assessment:** [Low/Moderate/High volatility explanation]
- **Peak price:** €X.XX ([Date])
- **Trough price:** €X.XX ([Date])

### Consolidated Scores

**Strength Score: X/100** (Financial power and market position)
**Integrity Score: X/100** (Earnings quality and transparency)
**Predictability Score: X/100** (Business consistency)
**Data Quality Score: X/100** (Information completeness)

**Overall Quality Rating: [Elite / Strong / Good / Adequate / Weak]**

### Financial Trends (5-10 Year View)

**Revenue:**
- [Trend description: growth rate, consistency, drivers]
- [Any concerning patterns?]

**Margins:**
- Gross margin: [Expanding / Stable / Declining]
- Operating margin: [Trend]
- Net margin: [Trend]
- Drivers: [Why are margins moving this way?]

**Cash Flow:**
- Operating cash flow: [Trend and quality]
- Free cash flow: [Consistency, conversion]
- Capital allocation: [Dividends, buybacks, capex, acquisitions]

**Balance Sheet:**
- Debt levels: [Conservative / Moderate / High]
- Liquidity: [Strong / Adequate / Concerning]
- Trend: [Strengthening / Stable / Weakening]

### 🚩 Red Flags
[List any concerning trends or issues, or state "None identified"]

---

## 📉 Technical Analysis & Entry Timing

### Price Action (Last 30-60 Days)
- **Current Price**: €X.XX
- **52-Week Range**: €X.XX - €X.XX
- **30-day Change**: [+/-X%]
- **Trend**: [Uptrend / Downtrend / Range-bound]
- **Volume**: [Increasing / Decreasing / Normal]

### Key Technical Levels

**Support Levels:**
- **Primary Support: €X.XX** - [Significance/reason]
- **Secondary Support: €X.XX** - [Significance/reason]

**Resistance Levels:**
- **Primary Resistance: €X.XX** - [Significance/reason]
- **Secondary Resistance: €X.XX** - [Significance/reason]

### Technical Indicators

**RSI**: X.X [Overbought >70 / Neutral 30-70 / Oversold <30]
**MACD**: [Bullish crossover / Bearish crossover / Neutral]
- Interpretation: [Momentum assessment]

**Moving Averages:**
- 50-day MA: €X.XX - Price is [above/below]
- 200-day MA: €X.XX - Price is [above/below]
- Golden/Death Cross: [Any recent crossovers?]

### Entry Assessment

**Technical Setup: [Bullish / Neutral / Bearish]**

**Optimal Entry Strategy:**
- [Buy now at market / Wait for pullback to €X.XX / Buy on breakout above €X.XX]
- **Ideal Entry Range: €X.XX - €X.XX**
- **Maximum Buy Price: €X.XX** (avoid above this)

**Momentum: [Strong Bullish / Bullish / Neutral / Bearish / Strong Bearish]**

---

## ⚖️ Bull vs. Bear Case

### 🐂 Bull Case
**Potential Upside: €X.XX (+X%)**

1. **[Bull Argument 1]**: [Specific evidence and reasoning]
2. **[Bull Argument 2]**: [Specific evidence and reasoning]
3. **[Bull Argument 3]**: [Specific evidence and reasoning]

**For this to play out:**
- [Required condition 1]
- [Required condition 2]

**Probability: [High / Moderate / Low]**

### 🐻 Bear Case
**Potential Downside: €X.XX (-X%)**

1. **[Bear Argument 1]**: [Specific risk and reasoning]
2. **[Bear Argument 2]**: [Specific risk and reasoning]
3. **[Bear Argument 3]**: [Specific risk and reasoning]

**This happens if:**
- [Risk trigger 1]
- [Risk trigger 2]

**Probability: [High / Moderate / Low]**

### ⚖️ Balance Assessment

**Which case is more probable: [Bull / Bear / Balanced]**

[2-3 paragraph explanation of:
- Weight of evidence for each side
- Historical precedent
- Management track record
- Industry dynamics
- Current valuation
- Risk/reward assessment]

---

## ⚠️ Risk Analysis

**Overall Risk Level: [Low / Moderate / High]**

### Key Risks

**1. [Risk Category - e.g., Competition Risk]**: 
[Specific risk and potential impact. Probability: High/Medium/Low]

**2. [Risk Category - e.g., Execution Risk]**: 
[Specific risk and potential impact. Probability: High/Medium/Low]

**3. [Risk Category - e.g., Valuation Risk]**: 
[Specific risk and potential impact. Probability: High/Medium/Low]

**4. [Risk Category - e.g., Macro Risk]**: 
[Specific risk and potential impact. Probability: High/Medium/Low]

### Risk Mitigation
[How does the company/investment address these risks?]
[What reduces the risk in this investment?]

---

## 🎯 Catalysts & Timeline

### Near-Term (0-6 months)
- **[Date]**: [Specific catalyst - earnings, product launch, etc.]
- **[Date]**: [Specific catalyst]

### Medium-Term (6-18 months)
- [Expected development 1]
- [Expected development 2]

### Long-Term (18+ months)
- [Structural trend 1]
- [Structural trend 2]

**Expected Timeline to Target**: [6-12 months / 1-3 years / 3-5+ years]

---

## 💡 Investment Recommendation

### **RECOMMENDATION: [BUY / HOLD / SELL]**
### **Conviction: [Strong Buy / Buy / Hold / Avoid]**

### Rationale
[2-3 paragraph synthesis of entire analysis:
- Why this recommendation?
- What makes it compelling (or not)?
- How does valuation + fundamentals + technicals + catalysts = this conclusion?
- What's the risk/reward?]

---

## 📍 Entry Strategy (if BUY)

**Ideal Entry Price: €X.XX - €X.XX**
- Reasoning: [Why this range?]

**Maximum Acceptable Price: €X.XX**
- Above this: Risk/reward unfavorable

**Approach:**
- [Buy now at market / Wait for pullback to €X.XX / Buy on breakout above €X.XX]
- Reasoning: [Current technical setup justification]

**DO NOT BUY IF:**
- Price exceeds €X.XX without fundamental improvement
- [Other specific condition]

---

## 🎯 Exit Strategy

### Price Targets (12-Month Horizon)
- **Conservative**: €X.XX (+X%)
- **Base Case**: €X.XX (+X%)
- **Optimistic**: €X.XX (+X%)

### Stop Loss
**Stop Loss: €X.XX (-X% maximum loss)**
- Technical: Below €X.XX support
- Fundamental: If [thesis-breaking condition]

### Sell Conditions (Thesis-Breaking)
Exit position if any of these occur:
1. [Specific fundamental deterioration - e.g., "ROE drops below 10% for 2 consecutive quarters"]
2. [Specific competitive threat - e.g., "Loses >5% market share to competitor"]
3. [Specific valuation threshold - e.g., "Reaches €X.XX (>50% above fair value)"]

### Hold Duration
**Expected Timeframe**: [6-12 months / 1-3 years / 3-5+ years]
- Based on: [Investment type - swing trade vs. long-term hold]

---

## 📏 Position Sizing

### Recommended Allocation: X-X% of portfolio
**Specific Recommendation: X%**

**Rationale:**
- Conviction level: [Strong Buy / Buy → drives size]
- Risk level: [Low / Moderate / High → constrains size]
- Diversification: [Sector exposure, correlation with existing holdings]
- Liquidity: [Can exit position easily?]

**Maximum Allocation: X%**
- Risk management limit
- Don't exceed even if highly convicted

### Sizing Guidelines Applied:
- Strong Buy + Low Risk = 5-8% (max 10%)
- Buy + Moderate Risk = 3-5% (max 7%)
- Speculative + High Risk = 1-3% (max 5%)

---

## 🔑 Key Takeaways

### Top 3 Reasons to Invest
1. [Most compelling positive factor]
2. [Second most compelling positive factor]
3. [Third most compelling positive factor]

### Top 3 Concerns
1. [Biggest risk or concern]
2. [Second biggest risk or concern]
3. [Third biggest risk or concern]

### One-Sentence Investment Thesis
[Single sentence capturing the complete investment case - why buy or avoid]

---

## 📚 Research Documentation

**Sources Consulted:**
- 10-K filings: [Fiscal years reviewed - e.g., FY2020-2024]
- 10-Q filings: [Recent quarters - e.g., Q1-Q3 2025]
- Earnings calls: [Dates reviewed]
- Proxy statements: [Years reviewed]
- Management letters: [Years reviewed]
- Competitor analysis: [Companies benchmarked]

**Analysis Depth:**
- Historical period analyzed: [X years]
- Peer companies compared: [Number and names]
- Valuation methods used: [DCF, Relative, Peter Lynch, Asset-based]

**Confidence Level: [High / Medium / Low]**
- **Based on**: [Quality and completeness of available data]
- **Gaps**: [Any areas where information is limited or unavailable]
- **Limitations**: [Any constraints in the analysis]

---

## 🔄 Alternative Candidates (Required if SELL/AVOID)

[If recommending SELL or AVOID, provide 3-5 better investment alternatives with brief rationale for each]

### Alternative 1: [Symbol] - [Company Name]
**Why it's better**: [1-2 paragraph comparison]
**Quick metrics**: [Valuation, growth, margins]

### Alternative 2: [Symbol] - [Company Name]
**Why it's better**: [1-2 paragraph comparison]
**Quick metrics**: [Valuation, growth, margins]

### Alternative 3: [Symbol] - [Company Name]
**Why it's better**: [1-2 paragraph comparison]
**Quick metrics**: [Valuation, growth, margins]

[Continue for 4-5 alternatives if SELL recommendation]

---

**Analysis Date**: [Current Date]
**Next Review**: [Suggested review date based on catalysts or timeline]
**Analyst**: Claude Stock Evaluator

---

## 📊 Quant-Style Dashboard

**FINAL MANDATORY STEP**: Create a React artifact using the standardized quant-style dashboard template with:

**Required Data to Populate:**
- ✅ All 48 metrics across 8 sections (calculated above)
- ✅ Historical price data (5 years, 6-12 points)
- ✅ 1-year price + 6-month forecast (4-6 points)
- ✅ MACD data (3-5 recent points)
- ✅ RSI data (3-5 recent points)
- ✅ Radar chart (12 metrics, normalized 0-100)
- ✅ Bull case (target + 5 points)
- ✅ Bear case (target + 5 points)
- ✅ Entry/exit strategy (5 values)

**Use the EXACT template code provided in the skill instructions above.**
**DO NOT use placeholder values - populate with actual calculated data from this analysis.**

[Create the React artifact here using the quant-style template]
```

---

## Quant-Style Dashboard Artifact

**MANDATORY**: After completing the full text analysis, create a React dashboard artifact using the standardized quant-style template format.

### Dashboard Template Structure

The dashboard uses a specific institutional-grade format with:

**1. Header Section** (Orange background)
- Format: `TICKER - Company Name`

**2. Eight Metric Sections** (2-column grid)

| Left Column | Right Column |
|-------------|--------------|
| Price & Valuation (blue) | Financial Performance (green) |
| Growth Metrics (emerald) | Risk Indicators (red) |
| Liquidity & FCF (cyan) | Insider & Sentiment (purple) |
| Quality Scores (orange) | Moat & Other (gray) |

Each section: 6 metric boxes with values, labels, benchmarks, color coding

**3. Charts Section** (3-column grid)

- **Left**: Linear Price Chart + MACD
  - Price, Intrinsic Value, Market Value lines
  - 5-year historical data
  - MACD indicator below

- **Center**: Radar Chart + 1-Year Forecast
  - 12-point radar (normalized 0-100)
  - Consolidated advice badge
  - 1-year price + 6-month forecast

- **Right**: Log Price Chart + RSI
  - Log-scale price history
  - Intrinsic value comparison
  - RSI (14) indicator below

**4. Key Notes Section** (Expandable accordion)
- 3-column layout: Bull Case | Bear Case | Entry/Exit Strategy
- Click to expand/collapse

**5. Footer**
- Analysis date, data sources, recommendation

### Required Metrics by Section

**Price & Valuation** (6 metrics):
- Price, Market Cap, Trailing P/E, Forward P/E, Subsector Typical P/E, PEG Ratio

**Financial Performance** (6 metrics):
- ROE, ROA, Profit Margin, Operating Margin, Gross Margin, ROIC

**Growth Metrics** (6 metrics):
- Revenue Growth (5Y), Earnings Growth, EPS (TTM), Forward EPS, Analyst Rec, Target Price

**Risk Indicators** (6 metrics):
- Debt/Equity, Consolidated Risk, F-Score, Z-Score, M-Score, Max Drawdown (5Y)

**Liquidity & FCF** (6 metrics):
- Current Ratio, Total Cash, Total Debt, FCF Growth 5Y, FCF Yield, Payout Ratio

**Insider & Sentiment** (6 metrics):
- Insider Buys (12M), Insider Sells (12M), Net Shares (12M), RSI (14D), Stock Type, Sector

**Quality Scores** (6 metrics):
- CQVS, Label, Valuation Score, Quality Score, Strength Score, Integrity Score

**Moat & Other** (6 metrics):
- Moat Score (0-10), Beta, Predictability, Data Quality, Completeness, Dividend Yield

### Radar Chart Metrics (12 points, normalized 0-100)
1. Revenue Growth (normalize: X% growth → scale to 100 for 20%+)
2. Operating Margin (normalize: X% → 100 for 30%+)
3. Gross Margin (normalize: X% → 100 for 60%+)
4. Profit Margin (normalize: X% → 100 for 25%+)
5. ROE (normalize: X% → 100 for 30%+)
6. Risk Score (inverse of consolidated risk: 100 - risk*100)
7. Beta Score (inverse: 100 for beta=0.5, 50 for beta=1.5, 0 for beta=2.5+)
8. P/Market Discount (100 = deeply undervalued, 50 = fair, 0 = overvalued)
9. Moat Score (moat rating * 10)
10. FCF Yield (X% → 100 for 8%+)
11. ROA (X% → 100 for 20%+)
12. Earnings Growth (X% → 100 for 25%+)

### Color Coding Rules

```javascript
// Green (isGood: true) - Positive indicators
ROE > 20%, ROA > 10%, Margins > 20%, ROIC > 15%
Revenue Growth > 10%, Current Ratio 1-2, Z-Score > 3
M-Score < -1.78, FCF Growth > 0%, Payout < 50%
F-Score >= 7, Quality >= 70, Strength >= 70

// Red (isGood: false) - Warning indicators  
Max Drawdown < -50%, Beta > 2, Consolidated Risk > 0.6
Predictability < 50%, F-Score <= 3, Z-Score < 1.81
M-Score > -1.78, Quality < 50

// Yellow (isGood: 'neutral') - Monitor
F-Score 4-6, RSI 30-70, Moat 5-7, Quality 50-70
Beta 1.5-2.0, Predictability 50-70%
```

### Complete Template Code

Use this exact template structure:

```jsx
import React, { useState } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, 
  ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, 
  PolarRadiusAxis, Radar, ReferenceLine, Area, ComposedChart, Scatter
} from 'recharts';

const QuantDashboard = () => {
  const [showKeyNotes, setShowKeyNotes] = useState(false);

  // ============================================================
  // POPULATE WITH STOCK-SPECIFIC DATA FROM ANALYSIS
  // ============================================================
  
  const ticker = "TICKER";  // Replace
  const companyName = "Company Name";  // Replace
  const recommendation = "BUY";  // BUY, HOLD, SELL, SPECULATIVE BUY
  const analysisDate = "December 6, 2025";  // Current date

  const metrics = {
    // Price & Valuation - from analysis
    price: 100.00,
    marketCap: '€10B',
    trailingPE: 20.0,
    forwardPE: 18.0,
    subsectorTypicalPE: 25.0,
    peg1Y: 1.2,           // NEW: 1-Year Forward PEG
    peg5Y: 2.5,           // NEW: 5-Year PEG
    
    // Financial Performance - from 5-10 year analysis
    roe: 25.0,
    roa: 12.0,
    profitMargin: 20.0,
    opMargin: 25.0,
    grossMargin: 50.0,
    roic: 18.0,
    
    // Growth Metrics - from historical trends (USE REPORTED, not underlying)
    revGrowth: 15.0,      // REPORTED revenue growth YoY
    earnGrowth: 20.0,     // REPORTED earnings growth YoY
    epsTTM: 5.00,
    forwardEPS: 5.50,
    growthCapped: 10.0,   // NEW: Capped sustainable growth estimate
    growthUncapped: 22.0, // NEW: Headline analyst growth estimate
    analystTarget: 120.00,
    
    // Risk Indicators - from advanced metrics section
    crs: 0.40,            // Consolidated Risk Score (0-1 scale)
    debtEquity: 0.50,
    fScore: 7,            // Piotroski F-Score
    zScore: 4.0,          // Altman Z-Score
    mScore: -2.5,         // Beneish M-Score
    valueTrapScore: 25,   // NEW: 0-100, LOWER = genuine, HIGHER = trap
    valueTrapLabel: 'Genuine', // NEW: Genuine/Caution/Trap
    maxDrawdown: -30.0,   // 5-year max drawdown %
    
    // Liquidity & FCF - from cash flow analysis
    currentRatio: 1.5,
    totalCash: '€2B',
    totalDebt: '€1B',
    fcfGrowth5Y: 12.0,    // 5-year smoothed growth
    fcfYield: 5.0,
    fcfMargin: 18.5,      // NEW: FCF / Revenue %
    payoutRatio: 30.0,
    
    // Insider & Sentiment - from SEC Form 4 or use "N/A" if unavailable
    insBuys: 0,           // From SEC Form 4 - use actual count or "N/A"
    insSells: 0,          // From SEC Form 4 - use actual count or "N/A"
    netShares: 'N/A',     // From SEC Form 4 - use actual or "N/A"
    shortInterest: 2.5,   // From FINRA/exchange - use actual or "N/A"
    newsSentiment: 0.25,  // -1 to +1 scale
    newsArticleCount: 15, // Recent article count
    
    // Beta & Volatility
    beta: 1.0,            // Stock beta
    vol1Y: 25.0,          // 1-Year volatility %
    
    // Quality Scores - from consolidated scoring
    cqvs: 75.0,           // Consolidated Quality & Valuation Score
    label: 'Quality Growth', // Elite/Compounder/Quality Growth/etc
    valuation: 70.0,      // 0-100
    quality: 80.0,        // 0-100
    strength: 75.0,       // 0-100
    integrity: 85.0,      // 0-100
    
    // Moat & Other
    buffettMoat: 8,       // 0-10 scale (renamed from moat)
    greenblattEY: 6.5,    // NEW: Earnings Yield %
    greenblattROC: 22.0,  // NEW: Return on Capital %
    earningsPredict: 70,  // Earnings Predictability 0-100
    completeness: 85,     // Data completeness 0-100
    dataQuality: 'High',  // High/Medium/Low
    divYield: 1.5,
    stockType: 'Growth',  // Growth/Value/Cyclical/Defensive
    sector: 'Technology',
    industry: 'Software',
    
    // NEW: Investor Persona Scores (0-10 scale each)
    buffettScore: 7.5,    // Durable competitive advantage seeker
    mungerScore: 6.8,     // Inversion thinker, risk avoider
    dalioScore: 7.2,      // All-weather, cycle resilient
    lynchScore: 8.0,      // GARP - Growth at Reasonable Price
    grahamScore: 5.5,     // Deep value, margin of safety
    greenblattScore: 6.0, // Magic Formula (EY + ROC)
    templetonScore: 4.5,  // Contrarian, global value
    sorosScore: 3.0,      // Reflexivity, macro trends
    
    // NEW: Valuation Lines for Charts
    marketValueCurrent: 95.00,
    intrinsicValueCurrent: 110.00,
    marketValueNextYear: 105.00,
    intrinsicValueNextYear: 120.00,
    unrestrictedMarketValueCurrent: 125.00,
    unrestrictedMarketValueNextYear: 140.00,
    
    // Valuation Assessment (for indicator below forecast)
    valuationPercent: 15,       // Positive = undervalued, negative = overvalued
    valuationLabel: 'Undervalued', // Undervalued/Fairly Valued/Overvalued
  };

  // TOP NEWS Headlines - Format: pipe-separated with dates at END in brackets
  const topNews = [
    { headline: 'Company announces Q4 guidance above expectations', date: '05 Dec 2025' },
    { headline: 'New product launch receives positive analyst coverage', date: '28 Nov 2025' },
    { headline: 'Strategic partnership announced with major cloud provider', date: '15 Nov 2025' },
    { headline: 'Q3 earnings beat estimates, revenue up 18% YoY', date: '02 Nov 2025' },
    { headline: 'Management presents at investor conference, reaffirms outlook', date: '20 Oct 2025' },
  ];
  
  // Format TOP NEWS as pipe-separated string with dates at END
  const topNewsString = topNews.map(n => `${n.headline} [${n.date}]`).join(' | ');

  // Historical Price Data (10 years with multiple valuation lines)
  const priceHistory = [
    { date: '2016', price: 25, totalReturn: 28, marketValueCurrent: 27, intrinsicValueCurrent: 30, marketValueNextYear: 29, intrinsicValueNextYear: 32, analystTarget: 30, unrestrictedCurrent: 28, unrestrictedNextYear: 31 },
    { date: '2017', price: 35, totalReturn: 40, marketValueCurrent: 38, intrinsicValueCurrent: 42, marketValueNextYear: 40, intrinsicValueNextYear: 45, analystTarget: 42, unrestrictedCurrent: 40, unrestrictedNextYear: 44 },
    { date: '2018', price: 45, totalReturn: 52, marketValueCurrent: 48, intrinsicValueCurrent: 55, marketValueNextYear: 52, intrinsicValueNextYear: 60, analystTarget: 55, unrestrictedCurrent: 52, unrestrictedNextYear: 58 },
    { date: '2019', price: 55, totalReturn: 65, marketValueCurrent: 58, intrinsicValueCurrent: 68, marketValueNextYear: 62, intrinsicValueNextYear: 72, analystTarget: 65, unrestrictedCurrent: 65, unrestrictedNextYear: 72 },
    { date: '2020', price: 50, totalReturn: 62, marketValueCurrent: 55, intrinsicValueCurrent: 65, marketValueNextYear: 60, intrinsicValueNextYear: 70, analystTarget: 62, unrestrictedCurrent: 62, unrestrictedNextYear: 70 },
    { date: '2021', price: 75, totalReturn: 95, marketValueCurrent: 80, intrinsicValueCurrent: 90, marketValueNextYear: 85, intrinsicValueNextYear: 98, analystTarget: 90, unrestrictedCurrent: 92, unrestrictedNextYear: 105 },
    { date: '2022', price: 65, totalReturn: 85, marketValueCurrent: 72, intrinsicValueCurrent: 85, marketValueNextYear: 78, intrinsicValueNextYear: 92, analystTarget: 82, unrestrictedCurrent: 85, unrestrictedNextYear: 95 },
    { date: '2023', price: 80, totalReturn: 105, marketValueCurrent: 85, intrinsicValueCurrent: 100, marketValueNextYear: 92, intrinsicValueNextYear: 108, analystTarget: 98, unrestrictedCurrent: 100, unrestrictedNextYear: 115 },
    { date: '2024', price: 95, totalReturn: 125, marketValueCurrent: 100, intrinsicValueCurrent: 115, marketValueNextYear: 108, intrinsicValueNextYear: 125, analystTarget: 115, unrestrictedCurrent: 120, unrestrictedNextYear: 135 },
    { date: '2025', price: 100, totalReturn: 135, marketValueCurrent: 105, intrinsicValueCurrent: 120, marketValueNextYear: 115, intrinsicValueNextYear: 132, analystTarget: 125, unrestrictedCurrent: 130, unrestrictedNextYear: 145 },
  ];

  // 1 Year Price with 6-Month Forecast, MAs, and Bollinger Bands
  const oneYearData = [
    { date: "Jan'25", price: 90, ma50: 88, ma200: 85, upperBand: 98, lowerBand: 82, forecast: null, ci95Upper: null, ci95Lower: null },
    { date: "Mar'25", price: 88, ma50: 89, ma200: 86, upperBand: 96, lowerBand: 80, forecast: null, ci95Upper: null, ci95Lower: null },
    { date: "May'25", price: 95, ma50: 91, ma200: 87, upperBand: 102, lowerBand: 84, forecast: null, ci95Upper: null, ci95Lower: null },
    { date: "Jul'25", price: 92, ma50: 92, ma200: 88, upperBand: 100, lowerBand: 84, forecast: null, ci95Upper: null, ci95Lower: null },
    { date: "Sep'25", price: 98, ma50: 94, ma200: 90, upperBand: 106, lowerBand: 86, forecast: null, ci95Upper: null, ci95Lower: null },
    { date: "Nov'25", price: 100, ma50: 96, ma200: 92, upperBand: 108, lowerBand: 88, forecast: 100, ci95Upper: 108, ci95Lower: 92 },
    { date: "Jan'26", price: null, ma50: null, ma200: null, upperBand: null, lowerBand: null, forecast: 108, ci95Upper: 120, ci95Lower: 96 },
    { date: "Mar'26", price: null, ma50: null, ma200: null, upperBand: null, lowerBand: null, forecast: 115, ci95Upper: 130, ci95Lower: 100 },
  ];

  // NEW: Ichimoku Cloud Data (6-month view with signal markers)
  const ichimokuData = [
    { date: 'Jun', price: 88, tenkan: 87, kijun: 85, senkouA: 84, senkouB: 82, chikou: 85, tkCrossMarker: null, kumoTwistMarker: null },
    { date: 'Jul', price: 92, tenkan: 90, kijun: 87, senkouA: 86, senkouB: 84, chikou: 90, tkCrossMarker: 92, kumoTwistMarker: null }, // TK Bullish Cross
    { date: 'Aug', price: 95, tenkan: 93, kijun: 90, senkouA: 89, senkouB: 86, chikou: 93, tkCrossMarker: null, kumoTwistMarker: null },
    { date: 'Sep', price: 98, tenkan: 96, kijun: 93, senkouA: 92, senkouB: 88, chikou: 96, tkCrossMarker: null, kumoTwistMarker: 92 }, // Kumo Twist Bullish
    { date: 'Oct', price: 96, tenkan: 97, kijun: 95, senkouA: 94, senkouB: 90, chikou: 94, tkCrossMarker: null, kumoTwistMarker: null },
    { date: 'Nov', price: 100, tenkan: 98, kijun: 96, senkouA: 95, senkouB: 92, chikou: 98, tkCrossMarker: null, kumoTwistMarker: null },
  ];

  // NEW: Ichimoku Signals Summary
  const ichimokuSignals = {
    tkCross: 'TK Bullish Cross',
    kumoTwist: 'Kumo Twist Bullish',
    priceVsCloud: 'Above Cloud (Bullish)',
  };

  // MACD Data (recent 6 months)
  const macdData = [
    { date: 'Jun', macd: 0.5, signal: 0.3, histogram: 0.2 },
    { date: 'Jul', macd: 1.2, signal: 0.6, histogram: 0.6 },
    { date: 'Aug', macd: 1.5, signal: 1.0, histogram: 0.5 },
    { date: 'Sep', macd: 1.8, signal: 1.3, histogram: 0.5 },
    { date: 'Oct', macd: 1.2, signal: 1.4, histogram: -0.2 },
    { date: 'Nov', macd: 0.8, signal: 1.2, histogram: -0.4 },
  ];

  // RSI Data (recent 6 months)
  const rsiData = [
    { date: 'Jun', rsi: 45 },
    { date: 'Jul', rsi: 55 },
    { date: 'Aug', rsi: 62 },
    { date: 'Sep', rsi: 68 },
    { date: 'Oct', rsi: 58 },
    { date: 'Nov', rsi: 55 },
  ];

  // Radar Chart Data (normalize all to 0-100 scale)
  const radarData = [
    { metric: 'Rev Growth', value: 70, fullMark: 100 },
    { metric: 'Op Margin', value: 75, fullMark: 100 },
    { metric: 'Gross Margin', value: 65, fullMark: 100 },
    { metric: 'Profit Margin', value: 60, fullMark: 100 },
    { metric: 'ROE', value: 70, fullMark: 100 },
    { metric: 'Risk (CRS)', value: 60, fullMark: 100 },
    { metric: 'Beta Score', value: 70, fullMark: 100 },
    { metric: 'P/Market Disc', value: 50, fullMark: 100 },
    { metric: 'Moat', value: 80, fullMark: 100 },
    { metric: 'FCF Growth', value: 55, fullMark: 100 },
    { metric: 'ROA', value: 65, fullMark: 100 },
    { metric: 'Earn Growth', value: 75, fullMark: 100 },
  ];

  // Key Notes Content - from Bull/Bear case analysis
  const bullCase = {
    target: "€130-150",  // Bull case price target
    points: [
      "Strong revenue growth momentum",
      "Expanding margins",
      "Market leadership position",
      "Favorable industry tailwinds",
      "Strong balance sheet"
    ]
  };

  const bearCase = {
    target: "€70-80",  // Bear case price target
    points: [
      "Valuation compression risk",
      "Competitive pressures",
      "Macro sensitivity",
      "Execution risks",
      "Key person dependency"
    ]
  };

  const entryStrategy = {
    idealEntry: "€90-95",  // From Entry Strategy section
    currentEntry: "€100 acceptable",
    target: "€120 (+20%)",  // 12-month target
    stopLoss: "€85 (-15%)",  // Stop loss
    positionSize: "2-3%"  // Recommended allocation
  };

  // ============================================================
  // COMPONENT CODE (Standard - use as-is)
  // ============================================================

  // Helper: Value Trap color (LOWER = genuine = green, HIGHER = trap = red)
  const getValueTrapColor = (score) => {
    if (score < 40) return 'bg-green-100 border-green-400 text-green-800';
    if (score < 60) return 'bg-yellow-100 border-yellow-400 text-yellow-800';
    return 'bg-red-100 border-red-400 text-red-800';
  };

  // Helper: Get label for Value Trap score
  const getValueTrapLabel = (score) => {
    if (score < 20) return 'Genuine';
    if (score < 40) return 'Probably Genuine';
    if (score < 60) return 'Caution';
    if (score < 80) return 'Likely Trap';
    return 'Strong Trap';
  };

  // Helper: Persona score color
  const getPersonaColor = (score) => {
    if (score >= 7) return 'bg-green-500';
    if (score >= 4) return 'bg-yellow-500';
    return 'bg-red-500';
  };

  // Helper: News sentiment color
  const getSentimentColor = (sentiment) => {
    if (sentiment > 0.3) return 'text-green-600';
    if (sentiment > 0) return 'text-green-500';
    if (sentiment > -0.3) return 'text-yellow-600';
    return 'text-red-600';
  };

  // Persona Badge Component
  const PersonaBadge = ({ name, score, position }) => (
    <div className={`absolute ${position} flex flex-col items-center`}>
      <div className={`w-6 h-6 rounded-full ${getPersonaColor(score)} flex items-center justify-center text-white text-[8px] font-bold`}>
        {score.toFixed(1)}
      </div>
      <div className="text-[7px] text-gray-600 mt-0.5">{name}</div>
    </div>
  );

  const MetricBox = ({ label, value, benchmark, isGood, size = 'normal' }) => {
    let bgColor = 'bg-gray-50';
    if (isGood === true) bgColor = 'bg-green-50 border-green-200';
    if (isGood === false) bgColor = 'bg-red-50 border-red-200';
    if (isGood === 'neutral') bgColor = 'bg-yellow-50 border-yellow-200';
    
    return (
      <div className={`${bgColor} border p-1.5 flex flex-col justify-center items-center`}>
        <div className="text-base font-bold text-gray-900">{value}</div>
        <div className="text-[9px] text-gray-600 text-center leading-tight">{label}</div>
        {benchmark && <div className="text-[8px] text-gray-400">{benchmark}</div>}
      </div>
    );
  };

  const SectionHeader = ({ title, bgColor }) => (
    <div className={`${bgColor} px-2 py-1 text-[10px] font-bold text-gray-700`}>
      {title}
    </div>
  );

  return (
    <div className="w-full max-w-7xl mx-auto p-3 bg-white text-xs">
      {/* Header */}
      <div className="bg-orange-500 text-white px-3 py-2 mb-1 text-lg font-bold text-center">
        {ticker} - {companyName}
      </div>

      {/* TOP NEWS - Pipe separated with dates at END */}
      <div className="border border-gray-300 rounded p-2 mb-3 bg-gray-50">
        <span className="font-bold text-[10px]">TOP NEWS:</span>
        <div className="text-[9px] mt-1">{topNewsString}</div>
      </div>

      {/* Top 4 sections */}
      <div className="grid grid-cols-2 gap-2 mb-3">
        {/* Price & Valuation - Updated with dual PEG */}
        <div className="border border-gray-300 rounded overflow-hidden">
          <SectionHeader title="PRICE & VALUATION" bgColor="bg-blue-100" />
          <div className="grid grid-cols-7 gap-px bg-gray-200">
            <MetricBox label="Price:" value={`€${metrics.price}`} />
            <MetricBox label="Market Cap:" value={metrics.marketCap} />
            <MetricBox label="Trailing P/E:" value={metrics.trailingPE} />
            <MetricBox label="Forward P/E:" value={metrics.forwardPE} benchmark={`(${metrics.subsectorTypicalPE})`} isGood={metrics.forwardPE < metrics.subsectorTypicalPE} />
            <MetricBox label="Subsector P/E:" value={metrics.subsectorTypicalPE} />
            <MetricBox label="PEG (1Y):" value={metrics.peg1Y} benchmark="(<1.5)" isGood={metrics.peg1Y < 1.5 ? true : metrics.peg1Y < 2 ? 'neutral' : false} />
            <MetricBox label="PEG (5Y):" value={metrics.peg5Y} benchmark="(<2)" isGood={metrics.peg5Y < 2 ? true : metrics.peg5Y < 3 ? 'neutral' : false} />
          </div>
        </div>

        {/* Financial Performance */}
        <div className="border border-gray-300 rounded overflow-hidden">
          <SectionHeader title="FINANCIAL PERFORMANCE" bgColor="bg-green-100" />
          <div className="grid grid-cols-6 gap-px bg-gray-200">
            <MetricBox label="ROE:" value={`${metrics.roe}%`} benchmark="(>20%)" isGood={metrics.roe >= 20 ? true : metrics.roe >= 10 ? 'neutral' : false} />
            <MetricBox label="ROA:" value={`${metrics.roa}%`} benchmark="(>10%)" isGood={metrics.roa >= 10} />
            <MetricBox label="Profit Margin:" value={`${metrics.profitMargin}%`} benchmark="(>20%)" isGood={metrics.profitMargin >= 20 ? true : metrics.profitMargin >= 10 ? 'neutral' : false} />
            <MetricBox label="Operative Margin:" value={`${metrics.opMargin}%`} benchmark="(>20%)" isGood={metrics.opMargin >= 20} />
            <MetricBox label="Gross Margin:" value={`${metrics.grossMargin}%`} benchmark="(>40%)" isGood={metrics.grossMargin >= 40} />
            <MetricBox label="ROIC:" value={`${metrics.roic}%`} benchmark="(>15%)" isGood={metrics.roic >= 15} />
          </div>
        </div>
      </div>

      {/* Next 4 sections */}
      <div className="grid grid-cols-2 gap-2 mb-3">
        {/* Growth Metrics */}
        <div className="border border-gray-300 rounded overflow-hidden">
          <SectionHeader title="GROWTH METRICS" bgColor="bg-emerald-100" />
          <div className="grid grid-cols-7 gap-px bg-gray-200">
            <MetricBox label="Revenue (YoY):" value={`${metrics.revGrowth}%`} benchmark="(>10%)" isGood={metrics.revGrowth >= 10} />
            <MetricBox label="Earning (YoY):" value={`${metrics.earnGrowth}%`} benchmark="(>0%)" isGood={metrics.earnGrowth >= 0} />
            <MetricBox label="EPS (TTM):" value={`€${metrics.epsTTM}`} />
            <MetricBox label="Forward EPS:" value={`€${metrics.forwardEPS}`} isGood={metrics.forwardEPS > metrics.epsTTM} />
            <MetricBox label="Growth Rates:" value={`Capped: ${metrics.growthCapped}%`} benchmark={`Uncapped: ${metrics.growthUncapped}%`} />
            <MetricBox label="Analyst Target:" value={`€${metrics.analystTarget}`} />
          </div>
        </div>

        {/* Risk Indicators */}
        <div className="border border-gray-300 rounded overflow-hidden">
          <SectionHeader title="RISK INDICATORS" bgColor="bg-red-100" />
          <div className="grid grid-cols-6 gap-px bg-gray-200">
            <MetricBox label="CRS (0-1):" value={metrics.crs.toFixed(2)} benchmark="(Medium)" isGood={metrics.crs < 0.4 ? true : metrics.crs < 0.6 ? 'neutral' : false} />
            <MetricBox label="Debt/Equity (mrq):" value={metrics.debtEquity} benchmark="(0.5-1)" isGood={metrics.debtEquity < 1 ? true : metrics.debtEquity < 2 ? 'neutral' : false} />
            <MetricBox label="Piotroski F:" value={metrics.fScore} benchmark="(≥7)" isGood={metrics.fScore >= 7 ? true : metrics.fScore >= 4 ? 'neutral' : false} />
            <MetricBox label="Altman Z:" value={metrics.zScore.toFixed(2)} benchmark="(>3)" isGood={metrics.zScore >= 2.99 ? true : metrics.zScore >= 1.81 ? 'neutral' : false} />
            <MetricBox label="Beneish M:" value={metrics.mScore.toFixed(2)} benchmark="(<-1.78)" isGood={metrics.mScore < -1.78} />
            <MetricBox label="Value Trap:" value={`${metrics.valueTrapScore} (${metrics.valueTrapLabel})`} isGood={metrics.valueTrapScore < 40 ? true : metrics.valueTrapScore < 60 ? 'neutral' : false} />
          </div>
        </div>
      </div>

      {/* Next 4 sections */}
      <div className="grid grid-cols-2 gap-2 mb-3">
        {/* Liquidity & Free Cash Flow */}
        <div className="border border-gray-300 rounded overflow-hidden">
          <SectionHeader title="LIQUIDITY & FREE CASH FLOW" bgColor="bg-cyan-100" />
          <div className="grid grid-cols-7 gap-px bg-gray-200">
            <MetricBox label="Current Ratio:" value={metrics.currentRatio.toFixed(2)} benchmark="(1-2)" isGood={metrics.currentRatio >= 1 && metrics.currentRatio <= 2 ? true : 'neutral'} />
            <MetricBox label="Cash:" value={metrics.totalCash} />
            <MetricBox label="Debt:" value={metrics.totalDebt} />
            <MetricBox label="FCF Growth 5Y:" value={`${metrics.fcfGrowth5Y}%`} benchmark="(>5%)" isGood={metrics.fcfGrowth5Y >= 5} />
            <MetricBox label="FCF Yield:" value={`${metrics.fcfYield}%`} benchmark="(>4%)" isGood={metrics.fcfYield >= 4} />
            <MetricBox label="FCF Margin:" value={`${metrics.fcfMargin}%`} benchmark="(>15%)" isGood={metrics.fcfMargin >= 15 ? true : metrics.fcfMargin >= 10 ? 'neutral' : false} />
            <MetricBox label="Payout Ratio:" value={`${metrics.payoutRatio}%`} benchmark="(<50%)" isGood={metrics.payoutRatio < 50} />
          </div>
        </div>

        {/* Insider & Sentiment & Class */}
        <div className="border border-gray-300 rounded overflow-hidden">
          <SectionHeader title="INSIDER & SENTIMENT & CLASS" bgColor="bg-purple-100" />
          <div className="grid grid-cols-7 gap-px bg-gray-200">
            <MetricBox label="Buys (12M):" value={metrics.insBuys} isGood={metrics.insBuys > metrics.insSells} />
            <MetricBox label="Sells (12M):" value={metrics.insSells} />
            <MetricBox label="Net Shares (12M):" value={metrics.netShares} />
            <MetricBox label="Short Int (%):" value={`${metrics.shortInterest}%`} isGood={metrics.shortInterest < 5 ? true : metrics.shortInterest < 10 ? 'neutral' : false} />
            <MetricBox label="Sentiment / Articles:" value={`${metrics.newsSentiment > 0 ? '+' : ''}${metrics.newsSentiment.toFixed(3)} / ${metrics.newsArticleCount}`} benchmark={metrics.newsSentiment > 0 ? '(Positive)' : '(Negative)'} isGood={metrics.newsSentiment > 0} />
            <MetricBox label={`Stock: ${metrics.stockType}`} value={`Div Yield: ${metrics.divYield}%`} />
            <MetricBox label="Sector/Industry:" value={`${metrics.sector} /`} benchmark={metrics.industry} />
          </div>
        </div>
      </div>

      {/* Last 2 sections */}
      <div className="grid grid-cols-2 gap-2 mb-3">
        {/* Quality Scores */}
        <div className="border border-gray-300 rounded overflow-hidden">
          <SectionHeader title="QUALITY SCORES" bgColor="bg-orange-100" />
          <div className="grid grid-cols-6 gap-px bg-gray-200">
            <MetricBox label="CQVS:" value={metrics.cqvs.toFixed(1)} benchmark="(>70)" isGood={metrics.cqvs >= 70 ? true : metrics.cqvs >= 50 ? 'neutral' : false} />
            <MetricBox label="Label:" value={metrics.label} />
            <MetricBox label="Valuation:" value={metrics.valuation} isGood={metrics.valuation >= 70} />
            <MetricBox label="Quality:" value={metrics.quality} isGood={metrics.quality >= 70 ? true : metrics.quality >= 50 ? 'neutral' : false} />
            <MetricBox label="Strength:" value={metrics.strength} isGood={metrics.strength >= 70} />
            <MetricBox label="Integrity:" value={metrics.integrity} isGood={metrics.integrity >= 70 ? true : metrics.integrity >= 50 ? 'neutral' : false} />
          </div>
        </div>

        {/* Moat & Other */}
        <div className="border border-gray-300 rounded overflow-hidden">
          <SectionHeader title="MOAT & OTHER" bgColor="bg-gray-200" />
          <div className="grid grid-cols-6 gap-px bg-gray-200">
            <MetricBox label="Buffett Moat:" value={metrics.buffettMoat} benchmark="(4-7)" isGood={metrics.buffettMoat >= 7 ? true : metrics.buffettMoat >= 4 ? 'neutral' : false} />
            <MetricBox label="Greenblatt (MF):" value={`EY: ${metrics.greenblattEY}%`} benchmark={metrics.greenblattROC ? `ROC: ${metrics.greenblattROC}%` : 'ROC: N/A'} isGood={metrics.greenblattEY >= 8 ? true : metrics.greenblattEY >= 4 ? 'neutral' : false} />
            <MetricBox label={`Beta: ${metrics.beta}`} value={`Vol 1Y: ${metrics.vol1Y}%`} isGood={metrics.beta < 1 ? true : metrics.beta < 1.5 ? 'neutral' : false} />
            <MetricBox label="Earnings Predict.:" value={`${metrics.earningsPredict}%`} benchmark="(>80%)" isGood={metrics.earningsPredict >= 80 ? true : metrics.earningsPredict >= 60 ? 'neutral' : false} />
            <MetricBox label="Drawdown (5Y):" value={`${metrics.maxDrawdown}%`} benchmark={metrics.maxDrawdown > -30 ? '(Low)' : metrics.maxDrawdown > -50 ? '(Mid)' : '(High)'} isGood={metrics.maxDrawdown > -30 ? true : metrics.maxDrawdown > -50 ? 'neutral' : false} />
            <MetricBox label={`Completeness: ${metrics.completeness}%`} value={`Data Quality: ${metrics.dataQuality}`} isGood={metrics.dataQuality === 'High' ? true : metrics.dataQuality === 'Medium' ? 'neutral' : false} />
          </div>
        </div>
      </div>

      {/* Charts Section - Enhanced with Legends */}
      <div className="grid grid-cols-3 gap-2 mb-3">
        {/* Linear Price Chart + MACD */}
        <div className="border border-gray-300 rounded p-2">
          <div className="text-sm font-bold mb-1 text-center">LINEAR PRICE CHART (10Y)</div>
          <div className="text-[7px] text-gray-500 mb-1 pl-1">
            — Close Price — Total Return<br/>
            - - Market Value (Current): €{metrics.marketValueCurrent}<br/>
            - - Intrinsic Value (Current): €{metrics.intrinsicValueCurrent}<br/>
            - - Analyst Target: €{metrics.analystTarget}
          </div>
          <ResponsiveContainer width="100%" height={130}>
            <LineChart data={priceHistory}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
              <XAxis dataKey="date" tick={{ fontSize: 7 }} />
              <YAxis tick={{ fontSize: 7 }} />
              <Tooltip contentStyle={{ fontSize: 8 }} />
              <Line type="monotone" dataKey="price" stroke="#1f2937" strokeWidth={1.5} dot={false} name="Close" />
              <Line type="monotone" dataKey="totalReturn" stroke="#6b7280" strokeWidth={1} strokeDasharray="2 2" dot={false} name="Total Return" />
              <Line type="monotone" dataKey="intrinsicValueCurrent" stroke="#16a34a" strokeWidth={1} strokeDasharray="5 5" dot={false} name="IV Current" />
              <Line type="monotone" dataKey="analystTarget" stroke="#3b82f6" strokeWidth={1} strokeDasharray="3 3" dot={false} name="Target" />
            </LineChart>
          </ResponsiveContainer>
          <div className="text-xs font-bold mt-1 mb-1 text-center">MACD</div>
          <ResponsiveContainer width="100%" height={55}>
            <LineChart data={macdData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
              <XAxis dataKey="date" tick={{ fontSize: 6 }} />
              <YAxis tick={{ fontSize: 6 }} />
              <ReferenceLine y={0} stroke="#666" />
              <Tooltip contentStyle={{ fontSize: 7 }} />
              <Line type="monotone" dataKey="macd" stroke="#2563eb" strokeWidth={1} dot={false} name="MACD" />
              <Line type="monotone" dataKey="signal" stroke="#dc2626" strokeWidth={1} dot={false} name="Signal" />
            </LineChart>
          </ResponsiveContainer>
        </div>

        {/* Radar + Investor Personas + Forecast */}
        <div className="border border-gray-300 rounded p-2">
          <div className="relative">
            <ResponsiveContainer width="100%" height={140}>
              <RadarChart data={radarData}>
                <PolarGrid />
                <PolarAngleAxis dataKey="metric" tick={{ fontSize: 6 }} />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={{ fontSize: 6 }} />
                <Radar name={ticker} dataKey="value" stroke="#2563eb" fill="#3b82f6" fillOpacity={0.3} />
              </RadarChart>
            </ResponsiveContainer>
            {/* Investor Persona Badges */}
            <PersonaBadge name="Buffett" score={metrics.buffettScore} position="top-0 left-1/4" />
            <PersonaBadge name="Lynch" score={metrics.lynchScore} position="top-0 right-1/4" />
            <PersonaBadge name="Munger" score={metrics.mungerScore} position="top-1/4 -left-2" />
            <PersonaBadge name="Greenblatt" score={metrics.greenblattScore} position="top-1/4 -right-2" />
            <PersonaBadge name="Dalio" score={metrics.dalioScore} position="bottom-1/4 -left-2" />
            <PersonaBadge name="Graham" score={metrics.grahamScore} position="bottom-1/4 -right-2" />
            <PersonaBadge name="Templeton" score={metrics.templetonScore} position="bottom-0 left-1/4" />
            <PersonaBadge name="Soros" score={metrics.sorosScore} position="bottom-0 right-1/4" />
          </div>
          <div className="text-center my-1">
            <span className="bg-green-200 px-2 py-0.5 text-[10px] font-bold rounded border border-green-400">
              Advice: {recommendation} (CQVS: {metrics.cqvs.toFixed(1)})
            </span>
          </div>
          <div className="text-[8px] font-bold mb-0.5 text-center">1Y PRICE + 6-MONTH FORECAST</div>
          <div className="text-[6px] text-gray-500 mb-0.5 text-center">— Close — 50-Day MA — 200-Day MA ▒ Bollinger Bands - - Forecast</div>
          <ResponsiveContainer width="100%" height={70}>
            <ComposedChart data={oneYearData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
              <XAxis dataKey="date" tick={{ fontSize: 6 }} />
              <YAxis tick={{ fontSize: 6 }} />
              <Tooltip contentStyle={{ fontSize: 7 }} />
              <Area type="monotone" dataKey="upperBand" stroke="none" fill="#e0e0e0" fillOpacity={0.5} />
              <Area type="monotone" dataKey="ci95Upper" stroke="none" fill="#dbeafe" fillOpacity={0.5} />
              <Line type="monotone" dataKey="price" stroke="#1f2937" strokeWidth={1.5} dot={false} />
              <Line type="monotone" dataKey="ma50" stroke="#f59e0b" strokeWidth={1} dot={false} />
              <Line type="monotone" dataKey="ma200" stroke="#ef4444" strokeWidth={1} dot={false} />
              <Line type="monotone" dataKey="forecast" stroke="#16a34a" strokeWidth={1.5} strokeDasharray="5 5" dot={false} />
            </ComposedChart>
          </ResponsiveContainer>
          {/* Valuation Indicator */}
          <div className={`text-center text-[10px] font-bold mt-1 ${metrics.valuationPercent > 10 ? 'text-green-600' : metrics.valuationPercent < -10 ? 'text-red-600' : 'text-yellow-600'}`}>
            {metrics.valuationLabel} ({metrics.valuationPercent > 0 ? '+' : ''}{metrics.valuationPercent}%)
          </div>
        </div>

        {/* Log Price + RSI */}
        <div className="border border-gray-300 rounded p-2">
          <div className="text-sm font-bold mb-1 text-center">LOG PRICE CHART (10Y)</div>
          <div className="text-[7px] text-gray-500 mb-1 pl-1">
            — Close Price — Total Return<br/>
            - - Unrestr. Market Value (Current): €{metrics.unrestrictedMarketValueCurrent}<br/>
            - - Unrestr. Market Value (Next Year): €{metrics.unrestrictedMarketValueNextYear}
          </div>
          <ResponsiveContainer width="100%" height={130}>
            <LineChart data={priceHistory}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
              <XAxis dataKey="date" tick={{ fontSize: 7 }} />
              <YAxis tick={{ fontSize: 7 }} scale="log" domain={['auto', 'auto']} />
              <Tooltip contentStyle={{ fontSize: 8 }} />
              <Line type="monotone" dataKey="price" stroke="#1f2937" strokeWidth={1.5} dot={false} name="Close" />
              <Line type="monotone" dataKey="totalReturn" stroke="#6b7280" strokeWidth={1} strokeDasharray="2 2" dot={false} name="Total Return" />
              <Line type="monotone" dataKey="unrestrictedCurrent" stroke="#dc2626" strokeWidth={1} strokeDasharray="5 5" dot={false} name="Unrestr Current" />
              <Line type="monotone" dataKey="unrestrictedNextYear" stroke="#f97316" strokeWidth={1} strokeDasharray="5 5" dot={false} name="Unrestr Next" />
            </LineChart>
          </ResponsiveContainer>
          <div className="text-xs font-bold mt-1 mb-1 text-center">RSI (14) = {rsiData[rsiData.length - 1].rsi}</div>
          <ResponsiveContainer width="100%" height={55}>
            <LineChart data={rsiData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
              <XAxis dataKey="date" tick={{ fontSize: 6 }} />
              <YAxis tick={{ fontSize: 6 }} domain={[0, 100]} />
              <Tooltip contentStyle={{ fontSize: 7 }} />
              <ReferenceLine y={70} stroke="#ef4444" strokeDasharray="2 2" />
              <ReferenceLine y={30} stroke="#22c55e" strokeDasharray="2 2" />
              <Line type="monotone" dataKey="rsi" stroke="#f59e0b" strokeWidth={1.5} dot={false} />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* NEW: Ichimoku Cloud Chart */}
      <div className="border border-gray-300 rounded p-2 mb-3">
        <div className="text-sm font-bold mb-1 text-center">ICHIMOKU CLOUD</div>
        <div className="flex gap-4 text-[7px] justify-center mb-1">
          <span>— Close Price</span>
          <span className="text-blue-500">— Tenkan-sen (9)</span>
          <span className="text-red-500">— Kijun-sen (26)</span>
          <span className="text-gray-400">— Chikou Span</span>
          <span className="text-green-500">▒ Senkou Span A/B (Cloud)</span>
          <span className="ml-2 font-bold text-yellow-600">◆ TK Cross</span>
          <span className="text-purple-600">◆ Kumo Twist</span>
        </div>
        <ResponsiveContainer width="100%" height={100}>
          <ComposedChart data={ichimokuData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#e0e0e0" />
            <XAxis dataKey="date" tick={{ fontSize: 7 }} />
            <YAxis tick={{ fontSize: 7 }} domain={['auto', 'auto']} />
            <Tooltip contentStyle={{ fontSize: 8 }} />
            <Area type="monotone" dataKey="senkouA" stroke="none" fill="#86efac" fillOpacity={0.3} />
            <Area type="monotone" dataKey="senkouB" stroke="none" fill="#fca5a5" fillOpacity={0.3} />
            <Line type="monotone" dataKey="price" stroke="#1f2937" strokeWidth={2} dot={false} name="Price" />
            <Line type="monotone" dataKey="tenkan" stroke="#3b82f6" strokeWidth={1} dot={false} name="Tenkan" />
            <Line type="monotone" dataKey="kijun" stroke="#dc2626" strokeWidth={1} dot={false} name="Kijun" />
            <Line type="monotone" dataKey="chikou" stroke="#9ca3af" strokeWidth={1} strokeDasharray="3 3" dot={false} name="Chikou" />
            <Scatter dataKey="tkCrossMarker" fill="#9333ea" shape="diamond" name="TK Cross" />
            <Scatter dataKey="kumoTwistMarker" fill="#dc2626" shape="diamond" name="Kumo Twist" />
          </ComposedChart>
        </ResponsiveContainer>
        <div className="flex gap-4 text-[8px] justify-center mt-1">
          <span className="bg-green-100 px-2 rounded">{ichimokuSignals.tkCross}</span>
          <span className="bg-green-100 px-2 rounded">{ichimokuSignals.kumoTwist}</span>
          <span className="bg-green-100 px-2 rounded">{ichimokuSignals.priceVsCloud}</span>
        </div>
      </div>

      {/* Key Notes (Expandable) */}
      <div className="border border-gray-300 rounded overflow-hidden">
        <button 
          onClick={() => setShowKeyNotes(!showKeyNotes)}
          className="w-full bg-gray-100 px-3 py-2 text-left text-sm font-bold flex items-center hover:bg-gray-200"
        >
          <span className="mr-2">{showKeyNotes ? '▼' : '▶'}</span> Key Notes (Click to Expand)
        </button>
        {showKeyNotes && (
          <div className="p-3 bg-gray-50">
            <div className="grid grid-cols-3 gap-4 text-xs">
              {/* Bull Case */}
              <div>
                <div className="font-bold text-green-700 mb-2 text-sm">BULL CASE ({bullCase.target})</div>
                <ul className="list-disc list-inside space-y-1">
                  {bullCase.points.map((point, i) => <li key={i}>{point}</li>)}
                </ul>
              </div>
              {/* Bear Case */}
              <div>
                <div className="font-bold text-red-700 mb-2 text-sm">BEAR CASE ({bearCase.target})</div>
                <ul className="list-disc list-inside space-y-1">
                  {bearCase.points.map((point, i) => <li key={i}>{point}</li>)}
                </ul>
              </div>
              {/* Entry/Exit Strategy */}
              <div>
                <div className="font-bold text-blue-700 mb-2 text-sm">ENTRY/EXIT STRATEGY</div>
                <ul className="list-disc list-inside space-y-1">
                  <li><strong>Ideal Entry:</strong> {entryStrategy.idealEntry}</li>
                  <li><strong>Current:</strong> {entryStrategy.currentEntry}</li>
                  <li><strong>Target:</strong> {entryStrategy.target}</li>
                  <li><strong>Stop Loss:</strong> {entryStrategy.stopLoss}</li>
                  <li><strong>Position Size:</strong> {entryStrategy.positionSize}</li>
                </ul>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="text-xs text-gray-500 text-center mt-3">
        Analysis Date: {analysisDate} | Sources: SEC Filings, Company Reports | 
        <span className="font-bold text-blue-600 ml-1">{recommendation}</span>
      </div>
    </div>
  );
};

export default QuantDashboard;
```

### Implementation Instructions

**CRITICAL STEPS:**

1. **Calculate all metrics** during the comprehensive text analysis
2. **Store metrics in variables** as you calculate them
3. **After completing full text analysis**, create the React artifact
4. **Replace ALL placeholder values** in the template with actual calculated data
5. **Use the EXACT template structure** - do not modify the component code
6. **Populate these specific data arrays**:
   - `metrics` object (60+ values including investor persona scores)
   - `topNews` array (5 recent headlines with dates)
   - `priceHistory` array (10-year data with multiple valuation lines)
   - `oneYearData` array (with MAs, Bollinger Bands, forecast)
   - `ichimokuData` array (6-month with signal markers)
   - `ichimokuSignals` object (TK cross, Kumo twist, price vs cloud)
   - `macdData` array (6 recent points with histogram)
   - `rsiData` array (6 recent points)
   - `radarData` array (12 metrics, normalized 0-100)
   - `bullCase.points` (5 points from bull case analysis)
   - `bearCase.points` (5 points from bear case analysis)
   - `entryStrategy` (5 values from entry/exit strategy)

6. **Normalize radar chart values** properly:
   - Each metric on 0-100 scale
   - Higher is always better (invert risk/beta if needed)
   - Use scaling formulas provided above

7. **Format values correctly**:
   - Currency: `"€100.00"` (Euro is the default - use € not $)
   - Large numbers: `"€10B"`, `"€2.5M"`
   - Percentages: `15.0` (number, not string with %)
   - Ratios: `1.25` (number)
   - Scores: `7` (integer) or `75.0` (float)

8. **Growth metrics**:
   - Use REPORTED revenue growth (not underlying/organic)
   - Use REPORTED earnings growth (not adjusted EPS growth)

9. **DO NOT**:
   - Leave placeholder values
   - Modify the component structure
   - Skip any sections
   - Use estimated/guessed data

**This is the ONLY accepted dashboard format. All other dashboard styles are deprecated.**

---

## Integration with Project Context

### Portfolio Awareness
- Access portfolio data from project knowledge
- Check if stock is already owned (if so, suggest using Portfolio Analyst)
- Assess fit with existing holdings (sector exposure, correlation)
- Consider position sizing in context of current allocations

### Investment Profile
- User's investment timeline, risk tolerance, preferences in project instructions
- Tailor recommendations to user's profile
- Consider tax implications from user's context
- Adjust position sizing based on portfolio size and risk tolerance

### Avoiding Duplication
If stock is already in portfolio:
- Acknowledge: "You already own [SYMBOL]. For analysis of your existing position, use the Portfolio Analyst skill."
- Still provide evaluation if user wants fresh assessment
- Frame as "Should you add more?" rather than initial purchase

---

## When to Use This Skill

**Use Stock Evaluator when:**
- User asks "Should I buy [stock]?"
- User wants evaluation of watchlist candidates
- User requests stock recommendations
- User asks "Is [stock] a good investment?"
- User wants to compare multiple potential investments
- User asks for alternatives to a stock they're considering
- User wants entry price and position sizing guidance
- User requests a "quant-style dashboard" or "stock visualization"

**Do NOT use this skill when:**
- User wants to review existing portfolio positions → Use Portfolio Analyst
- User wants general market commentary → Regular knowledge
- User wants stock screening/discovery → Different workflow
- User asks about options, derivatives, crypto → Out of scope

**Output includes:**
- Comprehensive text analysis (all sections above)
- Quant-style React dashboard artifact (standardized visual format)

---

## Best Practices

### Research Approach
1. **Start with company filings** (10-K, 10-Q) - NOT news articles
2. **Go back 5-10 years** - Understand evolution, not just current state
3. **Compare to 3-5 peers** - Apples to apples comparison
4. **Multiple valuation methods** - Don't rely on single approach
5. **Present both sides** - Bull and bear cases fairly
6. **Be specific** - Use actual data, not generalities

### Valuation Discipline
- Always require minimum 15% margin of safety
- Use conservative assumptions in DCF
- Weight multiple valuation methods
- Consider industry-specific norms
- Don't overpay for growth

### Risk Awareness
- Explicitly identify and quantify risks
- Consider probability and impact
- Acknowledge unknowns honestly
- Don't just focus on upside

### Communication
- Lead with clear recommendation
- Support every claim with evidence
- Use specific numbers and dates
- Explain reasoning, don't just state conclusions
- Make recommendations unmistakable

---

## Common Patterns to Recognize

### Quality Companies
- Consistent profitability over full cycle (5-10 years)
- Strong balance sheet (low debt, high cash)
- Competitive moats (wide or narrow)
- Shareholder-friendly capital allocation
- Predictable business model

### Value Traps (AVOID)
- Cheap for a reason (declining business)
- High debt with weak cash flow
- Losing market share consistently
- No competitive advantages
- Poor management capital allocation

### Growth at Reasonable Price (GARP)
- Strong revenue growth (15-25%+)
- Expanding margins
- Large addressable market
- Competitive advantages
- Reasonable valuation (PEG < 1.5)

### Turnaround Candidates
- New management with track record
- Improving key metrics quarter-over-quarter
- Catalyst for change
- Deep value with margin of safety
- Reduced debt or improved cash flow

---

## Quality Checks Before Finalizing

Before presenting analysis, verify:

### DATA INTEGRITY CHECKS (CRITICAL - CHECK FIRST)
1. ✅ Every numeric metric has a cited source from web search?
2. ✅ No insider activity fabricated? (SEC Form 4 or N/A)
3. ✅ No short interest fabricated? (FINRA/exchange or N/A)
4. ✅ ROE benchmark correct? (>20% = green, 10-20% = yellow, <10% = red)
5. ✅ Standardized metric labels used? (e.g., "Operative Margin", not "Operating")
6. ✅ All unavailable data shows "N/A"? (NEVER zeros or estimates)
7. ✅ TOP NEWS format correct? (pipe-separated, dates at END in brackets)
8. ✅ Valuation indicator displayed below forecast? (Undervalued/Fairly Valued/Overvalued +/- %)
9. ✅ Beta + Vol 1Y combined in one cell?
10. ✅ Sector/Industry combined in one cell?

### ANALYSIS COMPLETENESS CHECKS
11. ✅ All mandatory deliverables completed?
12. ✅ Multiple valuation methods used?
13. ✅ Both bull and bear cases presented?
14. ✅ Clear BUY/HOLD/SELL recommendation?
15. ✅ Specific entry price and position size?
16. ✅ 3-5 peer companies compared?
17. ✅ 5-10 year financial trends analyzed?
18. ✅ Research based on company filings, not news?
19. ✅ Margin of safety calculated?
20. ✅ Risk level assessed?
21. ✅ If SELL: 3-5 alternatives provided?
22. ✅ Technical entry points identified?
23. ✅ Advanced metrics calculated (Piotroski F, Altman Z, Beneish M, Max Drawdown)?
24. ✅ All monetary values in € (Euro)?
25. ✅ Revenue/Earnings growth using REPORTED (not underlying/adjusted) figures?
26. ✅ Value Trap Score calculated (0-100, LOWER = genuine)?
27. ✅ All 8 Investor Persona Scores calculated (0-10)?
28. ✅ PEG ratio calculated?
29. ✅ FCF Margin calculated?
30. ✅ Greenblatt Magic Formula metrics (EY, ROC)?
31. ✅ News sentiment and short interest researched?
32. ✅ Ichimoku Cloud data gathered with signal markers?
33. ✅ TOP NEWS section populated (5 recent headlines)?
34. ✅ 10-year price history with valuation lines available?
35. ✅ Enhanced dashboard created with ALL 60+ metrics populated?

### FINAL VALIDATION QUESTIONS
- Can you cite source for EVERY number in the dashboard?
- Did any metric come from training knowledge alone? (If yes, search again or use N/A)
- Are insider buys/sells from SEC Form 4 specifically? (If not found, use N/A)

If any checklist item incomplete: **STOP and gather more information**.
If data genuinely unavailable after searching: **Use "N/A" - never fabricate**.

---

## Example Evaluation Structure

[See complete example in EVALUATION-WORKFLOWS.md for detailed walkthrough]

---

## Continuous Improvement

After each evaluation:
- Track recommendation outcomes
- Learn from what worked/didn't work
- Refine valuation assumptions
- Improve pattern recognition
- Update industry knowledge

The goal is to discover genuinely attractive investment opportunities that fit the user's profile with adequate margin of safety and acceptable risk.
