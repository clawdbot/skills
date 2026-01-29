# Advanced Financial Health Metrics Guide

## Overview

This guide provides detailed calculation methods and interpretation for advanced financial health metrics that go beyond basic financial ratios. These metrics help identify financial strength, bankruptcy risk, and earnings quality.

---

## 1. Piotroski F-Score (Financial Strength)

### Purpose
Developed by Joseph Piotroski, this 9-point score measures financial strength across three dimensions: profitability, leverage/liquidity, and operating efficiency.

### When to Use
- Value investing (screening undervalued stocks)
- Identifying financially strong companies
- Avoiding value traps (cheap but deteriorating)
- Quality assessment for any stock

### Calculation (9 Points Total)

#### Profitability Signals (4 points)

**1. Positive Return on Assets (ROA): +1 point**
```
ROA = Net Income / Total Assets

Score +1 if: ROA > 0
Score 0 if: ROA ≤ 0
```

**2. Positive Operating Cash Flow: +1 point**
```
Score +1 if: Operating Cash Flow > 0
Score 0 if: Operating Cash Flow ≤ 0
```

**3. Change in ROA (Quality of Earnings): +1 point**
```
ΔROA = Current Year ROA - Prior Year ROA

Score +1 if: ΔROA > 0 (improving)
Score 0 if: ΔROA ≤ 0 (declining)
```

**4. Quality of Earnings: +1 point**
```
Score +1 if: Operating Cash Flow > Net Income
Score 0 if: Operating Cash Flow ≤ Net Income

Interpretation: Cash flow exceeding net income indicates high-quality, 
sustainable earnings (not driven by accounting accruals)
```

#### Leverage, Liquidity, and Source of Funds (3 points)

**5. Change in Long-term Debt: +1 point**
```
ΔDebt = Current Year LT Debt - Prior Year LT Debt

Score +1 if: ΔDebt < 0 (debt decreasing)
Score 0 if: ΔDebt ≥ 0 (debt increasing or flat)
```

**6. Change in Current Ratio: +1 point**
```
Current Ratio = Current Assets / Current Liabilities
ΔCurrent Ratio = Current Year Ratio - Prior Year Ratio

Score +1 if: ΔCurrent Ratio > 0 (improving liquidity)
Score 0 if: ΔCurrent Ratio ≤ 0 (declining liquidity)
```

**7. Change in Shares Outstanding: +1 point**
```
ΔShares = Current Shares Outstanding - Prior Year Shares Outstanding

Score +1 if: ΔShares ≤ 0 (no dilution)
Score 0 if: ΔShares > 0 (dilution from new issuance)

Interpretation: No new equity issuance suggests company can fund 
operations and growth from internal sources
```

#### Operating Efficiency (2 points)

**8. Change in Gross Margin: +1 point**
```
Gross Margin = (Revenue - COGS) / Revenue
ΔGross Margin = Current Year GM - Prior Year GM

Score +1 if: ΔGross Margin > 0 (improving)
Score 0 if: ΔGross Margin ≤ 0 (declining)
```

**9. Change in Asset Turnover: +1 point**
```
Asset Turnover = Revenue / Total Assets
ΔAsset Turnover = Current Year AT - Prior Year AT

Score +1 if: ΔAsset Turnover > 0 (improving efficiency)
Score 0 if: ΔAsset Turnover ≤ 0 (declining efficiency)
```

### F-Score Interpretation

| Score | Rating | Meaning | Action |
|-------|--------|---------|--------|
| 8-9 | Excellent | Very strong financial health across all dimensions | High quality |
| 6-7 | Good | Solid fundamentals with minor weaknesses | Quality stock |
| 4-5 | Adequate | Mixed signals, some concerns | Proceed with caution |
| 2-3 | Weak | Multiple red flags | Likely avoid |
| 0-1 | Very Weak | Severe financial deterioration | Avoid |

### Practical Application

**For Value Investing:**
- Screen for low P/B stocks with F-Score ≥ 7
- Avoids value traps (cheap + weak = trap)

**For Quality Assessment:**
- F-Score ≥ 7 = Strong fundamentals
- F-Score < 5 = Deteriorating fundamentals

**Trend Analysis:**
- Calculate F-Score for multiple years
- Improving F-Score (5→7→8) = strengthening company
- Declining F-Score (8→6→4) = deteriorating company

### Example Calculation

**Company XYZ - Fiscal Year 2024:**

*Profitability:*
1. ROA = 8% (positive) → +1
2. Operating CF = €500M (positive) → +1
3. Prior ROA = 7%, Current = 8% (improving) → +1
4. Operating CF (€500M) > Net Income (€450M) → +1
**Subtotal: 4/4**

*Leverage/Liquidity:*
5. LT Debt decreased from €2B to €1.8B → +1
6. Current Ratio: 2.1 vs 1.9 prior year (improving) → +1
7. Shares Outstanding: No change → +1
**Subtotal: 3/3**

*Efficiency:*
8. Gross Margin: 42% vs 40% prior year (improving) → +1
9. Asset Turnover: 0.85 vs 0.82 prior year (improving) → +1
**Subtotal: 2/2**

**Total F-Score: 9/9 (Excellent)**

---

## 2. Altman Z-Score (Bankruptcy Prediction)

### Purpose
Developed by Edward Altman in 1968, predicts probability of bankruptcy within 2 years. Highly accurate for manufacturing companies.

### When to Use
- Assessing financial distress risk
- Credit analysis
- Avoiding companies at risk of bankruptcy
- Turnaround situation evaluation

### Formulas

#### For Public Manufacturing Companies (Original)
```
Z-Score = 1.2(A) + 1.4(B) + 3.3(C) + 0.6(D) + 1.0(E)

Where:
A = Working Capital / Total Assets
B = Retained Earnings / Total Assets
C = EBIT / Total Assets
D = Market Value of Equity / Total Liabilities
E = Sales / Total Assets
```

#### For Private Companies (Z'-Score)
```
Z'-Score = 0.717(A) + 0.847(B) + 3.107(C) + 0.420(D') + 0.998(E)

Where D' = Book Value of Equity / Total Liabilities
(Use when market cap not available)
```

#### For Non-Manufacturing/Service Companies (Z''-Score)
```
Z''-Score = 6.56(A) + 3.26(B) + 6.72(C) + 1.05(D)

Where variables same as above, but E removed
(Services have lower asset intensity)
```

### Step-by-Step Calculation

**Component A: Working Capital / Total Assets**
```
Working Capital = Current Assets - Current Liabilities
Total Assets = From balance sheet

A = WC / TA

Measures liquid assets relative to company size.
Higher = more liquidity cushion
```

**Component B: Retained Earnings / Total Assets**
```
Retained Earnings = Cumulative earnings kept in business
Total Assets = From balance sheet

B = RE / TA

Measures cumulative profitability and age of company.
Higher = more mature, profitable company
```

**Component C: EBIT / Total Assets**
```
EBIT = Earnings Before Interest and Tax
Total Assets = From balance sheet

C = EBIT / TA

Measures productivity of assets.
Higher = more efficient operations
```

**Component D: Market Cap / Total Liabilities**
```
Market Value of Equity = Current Stock Price × Shares Outstanding
Total Liabilities = From balance sheet

D = Market Cap / Total Liabilities

Measures equity cushion relative to debt.
Higher = safer (equity can absorb losses before creditors impaired)
```

**Component E: Sales / Total Assets**
```
Sales = Annual revenue
Total Assets = From balance sheet

E = Sales / TA

Measures asset turnover/efficiency.
Higher = generating more revenue per dollar of assets
```

### Z-Score Interpretation

**For Manufacturing Companies (Original Z-Score):**

| Z-Score | Zone | Interpretation | Bankruptcy Probability |
|---------|------|----------------|------------------------|
| > 2.99 | Safe Zone | Low risk of bankruptcy | < 5% within 2 years |
| 1.81 - 2.99 | Grey Zone | Moderate risk, requires monitoring | 5-20% within 2 years |
| < 1.81 | Distress Zone | High bankruptcy risk | > 20% within 2 years |

**For Private/Non-Manufacturing (Modified Scores):**
- Thresholds slightly different
- Z' > 2.60 = Safe
- Z' 1.10-2.60 = Grey
- Z' < 1.10 = Distress

### Practical Application

**Risk Assessment:**
- Z > 3.0 = Very safe, strong financial position
- Z 2.5-3.0 = Safe but monitor
- Z 2.0-2.5 = Watch closely, some concern
- Z 1.5-2.0 = Significant risk
- Z < 1.5 = High distress, possible bankruptcy

**Credit Analysis:**
- Z > 2.99: Low credit risk
- Z 1.81-2.99: Medium credit risk
- Z < 1.81: High credit risk, avoid lending

**Trend Monitoring:**
- Declining Z-Score = deteriorating financial health
- Improving Z-Score = strengthening finances

### Example Calculation

**Company ABC - Manufacturing (Public):**

Balance Sheet Data:
- Current Assets: €500M
- Current Liabilities: €200M
- Total Assets: €2,000M
- Total Liabilities: €1,200M
- Retained Earnings: €400M

Income Statement:
- Sales: €3,000M
- EBIT: €300M

Market Data:
- Stock Price: €50
- Shares Outstanding: 40M
- Market Cap: €2,000M

**Calculations:**
```
A = (500-200) / 2000 = 300/2000 = 0.15
B = 400 / 2000 = 0.20
C = 300 / 2000 = 0.15
D = 2000 / 1200 = 1.67
E = 3000 / 2000 = 1.50

Z = 1.2(0.15) + 1.4(0.20) + 3.3(0.15) + 0.6(1.67) + 1.0(1.50)
Z = 0.18 + 0.28 + 0.495 + 1.002 + 1.50
Z = 3.457
```

**Result: Z = 3.46 (Safe Zone - Low bankruptcy risk)**

### Limitations

**Z-Score works best for:**
- Manufacturing companies
- Public companies with market cap data
- Companies with significant tangible assets

**Z-Score limitations:**
- Less accurate for service/tech companies (low assets)
- Less accurate for financial companies (different leverage norms)
- Can be manipulated through accounting choices
- Historical data = may not catch rapid deterioration

**Adjustments needed for:**
- Banks/Financials: Don't use Z-Score (use regulatory capital ratios instead)
- Tech/Service: Use Z''-Score or alternative metrics
- Startups: Often negative Z-Score (burning cash by design)

---

## 3. Beneish M-Score (Earnings Manipulation Detection)

### Purpose
Developed by Messod Beneish, detects likelihood of earnings manipulation through financial statement analysis. Identifies "creative accounting."

### When to Use
- Earnings quality assessment
- Fraud detection screening
- Avoiding accounting scandals
- Due diligence in acquisitions

### Full M-Score Formula

```
M-Score = -4.84 + 0.920(DSRI) + 0.528(GMI) + 0.404(AQI) + 0.892(SGI) 
          + 0.115(DEPI) - 0.172(SGAI) + 4.679(TATA) - 0.327(LVGI)

Where:
DSRI = Days Sales in Receivables Index
GMI = Gross Margin Index
AQI = Asset Quality Index
SGI = Sales Growth Index
DEPI = Depreciation Index
SGAI = Sales, General & Administrative Expenses Index
TATA = Total Accruals to Total Assets
LVGI = Leverage Index
```

### Component Calculations

**1. DSRI (Days Sales in Receivables Index)**
```
Days Sales in Receivables = (Accounts Receivable / Sales) × 365

DSRI = (DSR_t / DSR_t-1)

Interpretation:
- DSRI > 1: Receivables growing faster than sales (warning)
- Could indicate revenue recognition issues or credit quality problems
- Manipulators often book fake sales, inflating receivables
```

**2. GMI (Gross Margin Index)**
```
Gross Margin = (Sales - COGS) / Sales

GMI = (Gross Margin_t-1 / Gross Margin_t)

Interpretation:
- GMI > 1: Gross margin declining (warning)
- Declining margins create pressure to manipulate earnings
- May indicate competitive issues or cost problems
```

**3. AQI (Asset Quality Index)**
```
Asset Quality = 1 - (Current Assets + PP&E) / Total Assets

AQI = (Asset Quality_t / Asset Quality_t-1)

Interpretation:
- AQI > 1: Increasing soft assets (warning)
- Soft assets (goodwill, intangibles) easier to manipulate
- High AQI suggests capitalizing expenses or deferring costs
```

**4. SGI (Sales Growth Index)**
```
SGI = (Sales_t / Sales_t-1)

Interpretation:
- SGI > 1: Sales growing (could be warning if excessive)
- Extreme growth can motivate manipulation to maintain trend
- Rapid growth harder to sustain = pressure to inflate numbers
```

**5. DEPI (Depreciation Index)**
```
Depreciation Rate = Depreciation / (Depreciation + Net PP&E)

DEPI = (Depreciation Rate_t-1 / Depreciation Rate_t)

Interpretation:
- DEPI > 1: Depreciation rate slowing (warning)
- May indicate extending asset lives to reduce expenses
- Way to artificially boost earnings
```

**6. SGAI (SG&A Index)**
```
SGAI = (SG&A_t / Sales_t) / (SG&A_t-1 / Sales_t-1)

Interpretation:
- SGAI > 1: SG&A rising faster than sales (warning)
- Operating inefficiency or aggressive expansion
- But SGAI < 1 when manipulating (cutting necessary expenses)
- Mixed signal - context dependent
```

**7. TATA (Total Accruals to Total Assets)**
```
Total Accruals = (ΔCurrent Assets - ΔCash) - (ΔCurrent Liabilities - 
                  ΔShort-term Debt - ΔTax Payable) - Depreciation

TATA = Total Accruals / Total Assets

Interpretation:
- High TATA = earnings driven by accruals, not cash (warning)
- Sustainable earnings come from cash, not accounting entries
- High accruals often reversed in future (earnings collapse)
```

**8. LVGI (Leverage Index)**
```
Leverage = (Total Debt / Total Assets)

LVGI = (Leverage_t / Leverage_t-1)

Interpretation:
- LVGI > 1: Increasing leverage (warning)
- More debt = more pressure to meet covenants
- Can motivate earnings manipulation to avoid default
```

### M-Score Interpretation

**Threshold: -1.78**

| M-Score | Assessment | Probability of Manipulation | Action |
|---------|-----------|----------------------------|--------|
| > -1.78 | Likely Manipulator | High probability (>50%) | RED FLAG - Avoid |
| -2.50 to -1.78 | Grey Zone | Moderate concerns | Investigate further |
| < -2.50 | Unlikely Manipulator | Low probability | Likely clean |

### Simplified M-Score Approach

If full M-Score calculation not feasible, use **Red Flag Checklist:**

**High-Risk Indicators (3+ flags = WARNING):**
- [ ] DSR increasing >10% faster than sales
- [ ] Gross margins declining for 2+ consecutive years
- [ ] Operating cash flow < 80% of net income
- [ ] Working capital increasing much faster than sales
- [ ] Frequent accounting method changes
- [ ] Goodwill/intangibles >30% of assets and growing
- [ ] Depreciation expense declining as % of PP&E
- [ ] Revenue growth >30% per year (unsustainable pace)
- [ ] Frequent restatements or auditor changes
- [ ] SEC investigations or accounting inquiries

**Clean Indicators (supportive):**
- [ ] Operating cash flow ≥ net income
- [ ] Stable receivables relative to sales
- [ ] Conservative accounting policies
- [ ] Long-tenured, reputable auditor
- [ ] Transparent management communication
- [ ] Low accruals (<5% of assets)

### Practical Application

**Screening Process:**
1. Calculate M-Score for all holdings
2. Flag any with M-Score > -1.78
3. Investigate flagged companies:
   - Review 10-K footnotes
   - Check management discussion of accounting
   - Look for unusual items
   - Compare to peer accounting practices

**Ongoing Monitoring:**
- Recalculate annually
- Watch for M-Score trending upward
- Pay attention to individual components
- Investigate sudden jumps in any index

### Example Calculation

**Company DEF - Year 2024:**

*Prior Year (2023):*
- Sales: €1,000M
- Receivables: €150M
- Gross Margin: 45%
- SG&A: €200M

*Current Year (2024):*
- Sales: €1,200M (20% growth)
- Receivables: €210M (40% growth)
- Gross Margin: 42% (declining)
- SG&A: €250M

**Key Indices:**
```
DSRI = (210/1200 × 365) / (150/1000 × 365) = 64 / 55 = 1.16
GMI = 0.45 / 0.42 = 1.07
SGI = 1200 / 1000 = 1.20
SGAI = (250/1200) / (200/1000) = 0.208 / 0.200 = 1.04
```

**Red Flags:**
- DSRI = 1.16 (receivables growing 40% vs sales 20%)
- GMI = 1.07 (margins declining)
- SGI = 1.20 (aggressive growth)

**Assessment:** Multiple warning signs - investigate further
- Why are receivables growing so fast?
- Why are margins declining despite growth?
- Is revenue recognition aggressive?

### Real-World Examples

**Companies Caught with M-Score:**
- Enron: M-Score flagged before collapse
- WorldCom: High TATA, inflated assets
- Tyco: Multiple indices elevated

**Key Lesson:** M-Score not perfect but raises important questions. High M-Score ≠ definite fraud, but warrants deeper investigation.

---

## 4. Max Drawdown (Volatility Measure)

### Purpose
Measures the largest peak-to-trough decline in stock price over a specified period. Indicates downside risk and volatility.

### When to Use
- Risk assessment
- Position sizing decisions
- Understanding potential losses
- Comparing volatility across stocks

### Calculation

**Step 1: Identify Historical Peak**
```
Find highest price (peak) in specified period (typically 5 years)

Peak Price = Maximum price in lookback period
Peak Date = Date of maximum price
```

**Step 2: Find Subsequent Trough**
```
Find lowest price AFTER the peak, before any new peak

Trough Price = Minimum price after peak, before recovery
Trough Date = Date of minimum price
```

**Step 3: Calculate Drawdown**
```
Max Drawdown % = ((Trough Price - Peak Price) / Peak Price) × 100

Always negative number (e.g., -35%)
```

### Interpretation

**Volatility Categories:**

| Max Drawdown | Volatility | Type of Stock | Investor Suitability |
|--------------|-----------|---------------|---------------------|
| 0% to -20% | Very Low | Defensive, Utilities | Conservative |
| -20% to -30% | Low | Consumer Staples | Moderate Conservative |
| -30% to -40% | Moderate | Large Cap, Diversified | Moderate |
| -40% to -50% | High | Growth, Cyclicals | Aggressive |
| -50% to -70% | Very High | Small Cap, High Growth | Very Aggressive |
| > -70% | Extreme | Speculative, Startups | Speculative Only |

### Practical Application

**Position Sizing:**
- Higher max drawdown = smaller position size
- Example: -60% max drawdown → limit to 3% position
- Example: -20% max drawdown → can go up to 8% position

**Risk Management:**
- Understand worst-case scenario
- Set realistic stop losses
- Prepare psychologically for volatility

**Comparison:**
- Compare to market (S&P 500 typically -30% to -50% in bears)
- Higher drawdown than market = higher beta
- Lower drawdown than market = defensive

### Example Calculation

**Stock XYZ - 5 Year Period:**

Price History:
- 2020 Jan: €100 (starting point)
- 2021 Dec: €180 (PEAK)
- 2022 Mar: €90 (TROUGH after peak)
- 2023 Dec: €160 (recovery but not new peak)
- 2024 Nov: €175 (current)

**Calculation:**
```
Peak = €180 (Dec 2021)
Trough = €90 (Mar 2022)

Max Drawdown = (90 - 180) / 180 × 100
             = -90 / 180 × 100
             = -50%
```

**Assessment:** -50% max drawdown = High volatility stock
- Requires strong risk tolerance
- Appropriate for 3-5% position size
- Expect significant volatility
- Not suitable for conservative investors

### Additional Considerations

**Recovery Time:**
- How long from trough to recovery?
- Faster recovery = more resilient
- Years to recover = concerning

**Frequency:**
- Multiple -40%+ drawdowns = very volatile
- Rare deep drawdowns = event-driven

**Current Distance from Peak:**
- Currently at all-time high = no current drawdown
- Currently -30% from peak = in drawdown now

---

## 5. Consolidated Scoring Systems

### Strength Score (0-100)

**Components (weighted):**
- F-Score contribution: 30% (F-Score/9 × 100)
- ROE performance: 20% (ROE/30 × 100, capped at 100)
- Margin quality: 20% (Net Margin/25 × 100, capped at 100)
- Revenue growth: 15% (5yr CAGR/20 × 100, capped at 100)
- Market position: 15% (qualitative: leader=100, follower=50)

**Interpretation:**
- 80-100: Exceptional strength
- 60-79: Strong
- 40-59: Moderate
- 20-39: Weak
- 0-19: Very weak

### Integrity Score (0-100)

**Components (weighted):**
- M-Score quality: 40% (inverse relationship - lower M-Score = higher integrity)
- Cash flow quality: 30% (OCF/Net Income ratio)
- Accounting transparency: 20% (qualitative assessment)
- Management communication: 10% (qualitative assessment)

**Interpretation:**
- 80-100: High integrity, trustworthy
- 60-79: Good integrity
- 40-59: Moderate concerns
- 20-39: Significant concerns
- 0-19: High manipulation risk

### Predictability Score (0-100)

**Components (weighted):**
- Revenue volatility: 30% (lower volatility = higher score)
- Earnings consistency: 30% (fewer misses = higher score)
- Business model stability: 25% (subscription/recurring = higher)
- Cyclicality: 15% (non-cyclical = higher score)

**Interpretation:**
- 80-100: Highly predictable
- 60-79: Predictable
- 40-59: Moderate predictability
- 20-39: Unpredictable
- 0-19: Highly uncertain

### Data Quality Score (0-100)

**Components:**
- Financial statement completeness: 40%
- Reporting timeliness: 30%
- Auditor quality: 20%
- Disclosure transparency: 10%

**Interpretation:**
- 90-100: Complete, timely, transparent
- 70-89: Good quality with minor gaps
- 50-69: Adequate but some concerns
- 30-49: Significant data issues
- 0-29: Poor quality, unreliable

---

## Comprehensive Example: Full Analysis

**Company: TechCorp Inc. - Analysis for 2024**

### Financial Data Summary
- Total Assets: €5,000M
- Current Assets: €2,000M
- Current Liabilities: €800M
- Total Liabilities: €2,500M
- LT Debt: €1,500M
- Market Cap: €8,000M
- Revenue: €6,000M
- EBIT: €900M
- Net Income: €600M
- Operating CF: €700M
- Depreciation: €200M
- ROA: 12%
- Receivables: €900M
- Gross Margin: 48%

### F-Score Calculation

1. ROA = 12% (positive) → +1
2. Operating CF = €700M (positive) → +1
3. Prior ROA = 10%, improving → +1
4. OCF (€700M) > NI (€600M) → +1
5. Prior LT Debt €1,600M, now €1,500M (decreasing) → +1
6. Current Ratio: 2.5 vs 2.3 prior (improving) → +1
7. No new shares issued → +1
8. Gross Margin: 48% vs 46% prior (improving) → +1
9. Asset Turnover: 1.2 vs 1.15 prior (improving) → +1

**F-Score: 9/9 (Excellent)**

### Z-Score Calculation
```
A = (2000-800) / 5000 = 0.24
B = 1200 / 5000 = 0.24 (assuming RE = €1,200M)
C = 900 / 5000 = 0.18
D = 8000 / 2500 = 3.20
E = 6000 / 5000 = 1.20

Z = 1.2(0.24) + 1.4(0.24) + 3.3(0.18) + 0.6(3.20) + 1.0(1.20)
Z = 0.288 + 0.336 + 0.594 + 1.920 + 1.200
Z = 4.34
```

**Z-Score: 4.34 (Safe Zone - Very low bankruptcy risk)**

### M-Score Simplified Check
- DSR: Stable relative to sales ✓
- Gross margins: Improving ✓
- OCF > Net Income ✓
- No unusual accounting changes ✓
- Transparent reporting ✓

**M-Score Assessment: Clean (No red flags)**

### Max Drawdown (5Y)
- Peak: €95 (2022)
- Trough: €52 (2023)
- Max Drawdown: -45%

**Assessment: High volatility (typical for tech)**

### Consolidated Scores
- **Strength: 92/100** (Exceptional)
- **Integrity: 88/100** (High)
- **Predictability: 65/100** (Moderate)
- **Data Quality: 95/100** (Excellent)

### Overall Assessment
**TechCorp shows exceptional financial health with no earnings quality concerns. High volatility is typical for growth tech. Strong buy candidate from financial health perspective.**

---

## Best Practices

1. **Use Multiple Metrics**: No single score tells the whole story
2. **Trend Analysis**: Track scores over multiple years
3. **Industry Context**: Compare to peers, not absolute standards
4. **Qualitative Overlay**: Scores augment, don't replace judgment
5. **Update Regularly**: Recalculate annually or after major events
6. **Red Flag Prioritization**: M-Score warnings trump good F/Z-Scores
7. **Documentation**: Keep calculation workpapers for consistency

## Limitations

**All models have limitations:**
- Based on reported financials (garbage in, garbage out)
- Historical data (backward-looking)
- Industry differences (one size doesn't fit all)
- Can be manipulated (sophisticated fraud can fool models)
- Context matters (scores are inputs, not decisions)

**Use as screening tools and warning systems, not absolute truth.**

---

## 6. Value Trap Score (Genuine Value vs Trap Detection)

### Purpose
Identifies whether a stock that appears undervalued (low P/E, low P/B) is genuinely cheap or a "value trap" - cheap for valid fundamental reasons and likely to stay cheap or decline further.

### When to Use
- Evaluating seemingly undervalued stocks
- Screening value candidates
- Avoiding false bargains
- Confirming value thesis

### Calculation (0-100 Scale, LOWER = Genuine, HIGHER = Trap)

**Component 1: Price Momentum (25 points max)**
```
Assess 6-month and 12-month price performance vs market:

Underperforming market by >20% for 6 months: ADD 15-25 points
Underperforming market by 10-20%: ADD 8-15 points
Underperforming market by 0-10%: ADD 0-8 points
Outperforming market: ADD 0 points

Sustained 12-month decline: ADD additional 10-20 points
```

**Component 2: Earnings Quality (25 points max)**
```
EPS Trend (3 years):
- Declining each year: ADD 20-25 points
- Declining 2 of 3 years: ADD 10-20 points
- Flat: ADD 5-10 points
- Growing: ADD 0 points

Revenue Trend:
- Declining: ADD 5-15 points
- Flat: ADD 2-5 points
- Growing: ADD 0 points

Margin Trend:
- Compressing: ADD 5-10 points
- Stable: ADD 0 points
```

**Component 3: Balance Sheet Health (25 points max)**
```
Debt Levels:
- Increasing significantly: ADD 10-15 points
- Increasing moderately: ADD 5-10 points
- Stable/Decreasing: ADD 0 points

Cash Flow:
- Negative FCF: ADD 15-20 points
- Declining FCF: ADD 5-15 points
- Stable/Growing FCF: ADD 0 points

Working Capital:
- Deteriorating: ADD 5-10 points
- Stable/Improving: ADD 0 points
```

**Component 4: Valuation Context (25 points max)**
```
Compare current state to when multiple was higher:
- Fundamentals clearly justify lower multiple: ADD 20-25 points
- Mixed signals: ADD 10-20 points
- Fundamentals don't explain discount: ADD 0 points
```

### Formula
```
Value Trap Score = Momentum Penalty + Quality Penalty + Balance Sheet Penalty + Valuation Penalty
```

### Interpretation

| Score | Rating | Meaning | Action |
|-------|--------|---------|--------|
| 0-19 | Genuine Value | Fundamentals intact, likely undervalued | Strong candidate |
| 20-39 | Probably Genuine | Minor concerns, worth monitoring | Proceed with research |
| 40-59 | Caution Zone | Mixed signals, proceed carefully | Deep dive required |
| 60-79 | Likely Trap | Multiple red flags | Avoid unless special situation |
| 80-100 | Strong Trap | Cheap for good reasons | Avoid |

### Example Calculation

**Company DEF - Appears Cheap (P/E = 8, P/B = 0.7)**

*Momentum:*
- 6-month vs market: -25% underperformance → ADD 20 points
- 12-month decline: Sustained → ADD 15 points
**Subtotal: 35 points** (capped at 25)

*Earnings Quality:*
- EPS trend: Declining 3 consecutive years → ADD 22 points
- Revenue: Flat → ADD 3 points
- Margins: Compressing → ADD 8 points
**Subtotal: 33 points** (capped at 25)

*Balance Sheet:*
- Debt: Increasing → ADD 12 points
- FCF: Declining → ADD 10 points
- Working capital: Stable → ADD 0 points
**Subtotal: 22 points**

*Valuation Context:*
- Was trading at P/E 15 when EPS was 50% higher → ADD 20 points
**Subtotal: 20 points**

**Total Value Trap Score: 25 + 25 + 22 + 20 = 92 (Strong Trap)**

Assessment: Despite low multiples, this is a classic value trap. Fundamentals are deteriorating, explaining the low valuation.

---

## 7. Investor Persona Scores (8 Legendary Investor Frameworks)

### Purpose
Score stocks against 8 famous investor philosophies to help identify what type of investor the stock would appeal to, and to surface different perspectives on quality.

### When to Use
- Matching stocks to investment style
- Getting multiple perspectives on quality
- Understanding investment thesis fit
- Identifying blind spots in analysis

### The 8 Investor Personas

#### 1. Warren Buffett Score (0-10)
**Philosophy:** Durable competitive advantages, predictable earnings, high returns on capital

**Calculation:**
| Factor | Criteria | Points |
|--------|----------|--------|
| ROE | >25%: 2, >20%: 1.5, >15%: 1, <15%: 0 | 0-2 |
| Profit Margin | >20%: 2, >15%: 1.5, >10%: 1, <10%: 0 | 0-2 |
| FCF | Positive & growing: 2, Positive: 1, Negative: 0 | 0-2 |
| Moat Strength | Wide: 2, Narrow: 1, None: 0 | 0-2 |
| Predictability | High: 2, Medium: 1, Low: 0 | 0-2 |

**Buffett Score = Sum of points**

#### 2. Charlie Munger Score (0-10)
**Philosophy:** Inversion thinking - focus on what could go wrong

**Calculation (start at 10, subtract penalties):**
| Risk Factor | Penalty |
|-------------|---------|
| High debt (D/E > 2) | -3 |
| Volatile earnings (CoV > 30%) | -2 |
| Poor management track record | -2 |
| No competitive moat | -2 |
| Accounting red flags (M-Score > -1.78) | -3 |

**Munger Score = 10 - Sum of penalties (minimum 0)**

#### 3. Ray Dalio Score (0-10)
**Philosophy:** All-weather, cycle resilience, balance

**Calculation:**
| Factor | Criteria | Points |
|--------|----------|--------|
| Leverage | D/E < 0.5: 2, < 1: 1.5, < 2: 1, >2: 0 | 0-2 |
| Beta | <0.8: 2, <1: 1.5, <1.3: 1, >1.3: 0 | 0-2 |
| Margin Stability | Low variance: 2, Medium: 1, High: 0 | 0-2 |
| Earnings Volatility | Low: 2, Medium: 1, High: 0 | 0-2 |
| Recession Resistance | Historically resilient: 2, Mixed: 1, Cyclical: 0 | 0-2 |

**Dalio Score = Sum of points**

#### 4. Peter Lynch Score (0-10)
**Philosophy:** GARP - Growth at a Reasonable Price

**Primary metric: PEG Ratio**
| PEG | Points |
|-----|--------|
| < 0.5 | 10 |
| 0.5 - 0.75 | 9 |
| 0.75 - 1.0 | 8 |
| 1.0 - 1.25 | 6 |
| 1.25 - 1.5 | 5 |
| 1.5 - 2.0 | 3 |
| > 2.0 | 1 |

**Adjustments:**
- Consistent earnings growth: +1 (cap at 10)
- Easy to understand business: +1 (cap at 10)
- Declining industry: -1

**Lynch Score = PEG points + adjustments**

#### 5. Benjamin Graham Score (0-10)
**Philosophy:** Deep value, margin of safety, defensive criteria

**Graham Criteria (2 points each):**
1. P/E < 15
2. P/B < 1.5
3. P/E × P/B < 22.5
4. Current Ratio > 2
5. Positive earnings for 10+ years

**Graham Score = Sum of criteria met × 2**

#### 6. Joel Greenblatt Score (0-10)
**Philosophy:** Magic Formula - high earnings yield + high return on capital

**Calculation:**
| Earnings Yield (EBIT/EV) | Points | Return on Capital | Points |
|--------------------------|--------|-------------------|--------|
| > 15% | 5 | > 50% | 5 |
| 10-15% | 4 | 30-50% | 4 |
| 8-10% | 3 | 20-30% | 3 |
| 5-8% | 2 | 12-20% | 2 |
| < 5% | 1 | < 12% | 1 |

**Greenblatt Score = EY points + ROC points**

#### 7. John Templeton Score (0-10)
**Philosophy:** Contrarian, global value, maximum pessimism

**Calculation:**
| Factor | Criteria | Points |
|--------|----------|--------|
| Price vs 52-week low | Within 10%: 3, Within 20%: 2, Within 30%: 1 | 0-3 |
| Analyst sentiment | Mostly sell: 2, Mixed: 1, Mostly buy: 0 | 0-2 |
| Fundamentals vs pessimism | Strong despite bearishness: 3, Mixed: 1.5 | 0-3 |
| Global opportunity | Non-US or emerging: 2, Developed ex-US: 1, US: 0 | 0-2 |

**Templeton Score = Sum of points**

#### 8. George Soros Score (0-10)
**Philosophy:** Reflexivity, macro trends, momentum with thesis

**Calculation:**
| Factor | Criteria | Points |
|--------|----------|--------|
| Price momentum | Strong uptrend: 3, Moderate: 2, Weak: 1 | 0-3 |
| Macro tailwinds | Strong: 3, Moderate: 2, Headwinds: 0 | 0-3 |
| Perception shift | Narrative changing positively: 2, Stable: 1 | 0-2 |
| Catalyst proximity | Near-term catalyst: 2, Medium-term: 1, None: 0 | 0-2 |

**Soros Score = Sum of points**

### Display Format
Show 8 circular badges around radar chart:
- **Green (7-10):** Strong fit for this investor type
- **Yellow (4-6.9):** Moderate fit
- **Red (0-3.9):** Poor fit

### Interpretation Matrix

| If High Scores In... | Stock Type | Suitable For |
|---------------------|------------|--------------|
| Buffett + Munger | Quality compounder | Long-term holders |
| Lynch + Greenblatt | GARP opportunity | Growth-value blend |
| Graham + Templeton | Deep value | Contrarian investors |
| Dalio | Defensive/stable | Conservative portfolios |
| Soros | Momentum play | Active traders |

### Example: TechCorp Analysis

| Persona | Score | Rationale |
|---------|-------|-----------|
| Buffett | 8.5 | High ROE, strong moat, predictable |
| Munger | 7.0 | Low debt, clean accounting, minor cyclicality |
| Dalio | 6.0 | Beta 1.3 (higher), but stable margins |
| Lynch | 9.0 | PEG 0.8, consistent growth, understandable |
| Graham | 3.0 | Fails P/E, P/B criteria (growth premium) |
| Greenblatt | 7.0 | Good EY (8%), excellent ROC (35%) |
| Templeton | 2.0 | Near highs, well-liked by analysts |
| Soros | 6.5 | Momentum fading, but AI catalyst |

**Conclusion:** TechCorp is a Buffett/Lynch stock - quality GARP play, not for deep value or momentum strategies.

---

## 8. FCF Margin and Other Enhanced Metrics

### FCF Margin
**Formula:** Free Cash Flow / Revenue × 100

**Interpretation:**
| FCF Margin | Rating | Meaning |
|------------|--------|---------|
| > 25% | Exceptional | Cash machine, strong pricing power |
| 15-25% | Excellent | High-quality business |
| 10-15% | Good | Solid cash generation |
| 5-10% | Adequate | Average cash conversion |
| < 5% | Poor | Capital intensive or margin pressure |

### Greenblatt Magic Formula Components

**Earnings Yield (EY):**
```
EY = EBIT / Enterprise Value × 100

Where:
- EBIT = Earnings Before Interest and Taxes
- Enterprise Value = Market Cap + Debt - Cash
```

**Return on Capital (ROC):**
```
ROC = EBIT / (Net Fixed Assets + Net Working Capital) × 100

Where:
- Net Fixed Assets = PP&E less accumulated depreciation
- Net Working Capital = Current Assets - Current Liabilities (excluding cash and debt)
```

### News Sentiment Score
**Scale:** -1.0 to +1.0

| Score | Interpretation |
|-------|----------------|
| > +0.5 | Very positive coverage |
| +0.2 to +0.5 | Positive coverage |
| -0.2 to +0.2 | Neutral coverage |
| -0.5 to -0.2 | Negative coverage |
| < -0.5 | Very negative coverage |

### Short Interest
**Formula:** Shares Sold Short / Float × 100

| Short Interest | Interpretation |
|----------------|----------------|
| < 3% | Very low, minimal bearish sentiment |
| 3-5% | Normal range |
| 5-10% | Elevated, some concern |
| 10-20% | High, significant bearish sentiment |
| > 20% | Very high, potential squeeze candidate |

---

## Summary: Complete Metrics Toolkit

| Metric | Purpose | Key Threshold |
|--------|---------|---------------|
| F-Score | Financial strength | ≥7 = Strong |
| Z-Score | Bankruptcy risk | >2.99 = Safe |
| M-Score | Earnings manipulation | <-1.78 = Clean |
| Max Drawdown | Volatility | >-40% = Moderate |
| Value Trap | Genuine vs trap | <40 = Genuine |
| Investor Personas | Style fit | 8 scores, 0-10 |
| FCF Margin | Cash efficiency | >15% = Excellent |
| Greenblatt EY | Cheap earnings | >8% = Good |
| Greenblatt ROC | Capital efficiency | >20% = Good |
| News Sentiment | Market mood | >0 = Positive |
| Short Interest | Bearish sentiment | <5% = Low |

**Use these metrics together for comprehensive analysis. No single metric tells the whole story.**
