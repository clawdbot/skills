# Valuation Guide

## Overview

Valuation is both art and science. No single method provides the "right" answer. This guide provides multiple valuation approaches to triangulate fair value with appropriate margin of safety.

**Key Principle**: Better to be approximately right than precisely wrong. Use conservative assumptions and require margin of safety.

---

## The Four Valuation Methods

### Method 1: DCF (Discounted Cash Flow) Analysis

**Best for**: Companies with predictable, positive free cash flows

**Weight in Final Valuation**: 40% (if reliable cash flows)

#### Step-by-Step DCF Process

**1. Project Free Cash Flows (5-10 years)**

Free Cash Flow = Operating Cash Flow - Capital Expenditures

**Projection Steps:**
- Start with recent FCF (average last 3 years)
- Project revenue growth based on:
  - Historical growth rates
  - Industry growth expectations
  - Company guidance
  - Market saturation considerations
- Apply profit margins:
  - Use conservative estimates
  - Consider historical ranges
  - Account for competitive pressures
- Subtract capex requirements:
  - Maintenance capex (sustain business)
  - Growth capex (expand business)

**Conservative Assumptions:**
- Use lower end of growth range
- Don't assume infinite margin expansion
- Include realistic capex needs
- Consider competitive pressure on margins

**Example Projection:**
```
Year 1: €100M FCF (base year)
Year 2: €110M (+10% growth)
Year 3: €120M (+9% growth)
Year 4: €130M (+8% growth - slowing)
Year 5: €140M (+7.7% growth)
Year 6-10: 5-6% perpetual growth
```

**2. Calculate Terminal Value**

Two approaches:

**Perpetuity Growth Method** (preferred):
Terminal Value = Year 10 FCF × (1 + g) / (WACC - g)

Where:
- g = long-term growth rate (typically 2-3%, not higher than GDP growth)
- WACC = discount rate

**Exit Multiple Method**:
Terminal Value = Year 10 FCF × Exit Multiple

Exit Multiple = Conservative P/FCF or EV/FCF multiple based on:
- Historical company average
- Industry peer average
- Use lower end of range

**3. Discount to Present Value**

Discount Rate = WACC (Weighted Average Cost of Capital)

**Simple WACC Calculation:**
WACC = Cost of Equity × (Equity %) + Cost of Debt × (1 - Tax Rate) × (Debt %)

**Cost of Equity (simplified)**:
- Risk-free rate (government bond yield): 2-4%
- + Equity risk premium: 4-6%
- + Company-specific risk: 0-3%
- = Total: 8-12% typically

**Conservative approach**: Use higher discount rates (10-12%) for:
- Smaller companies
- Higher risk businesses
- Uncertain cash flows
- Cyclical industries

**Formula:**
Present Value = Future Cash Flow / (1 + WACC)^n

Where n = number of years in future

**4. Calculate Enterprise Value**
Sum of:
- All discounted annual FCFs (Years 1-10)
- Discounted terminal value

**5. Calculate Equity Value**
Equity Value = Enterprise Value + Cash - Debt

**6. Per Share Value**
Fair Value per Share = Equity Value / Shares Outstanding

**Use diluted shares outstanding** (includes options, RSUs)

**7. Apply Margin of Safety**

**Final DCF Fair Value = Calculated Value × (1 - Margin of Safety %)**

Margin of Safety:
- Minimum: 15%
- Standard: 20-25%
- High uncertainty: 30%+

**Example:**
- Calculated DCF value: €100 per share
- Margin of safety: 20%
- **DCF Fair Value: €80 per share**

#### DCF Sensitivity Analysis

Test how fair value changes with different assumptions:

| Discount Rate | Terminal Growth 2% | Terminal Growth 3% | Terminal Growth 4% |
|---------------|-------------------|-------------------|-------------------|
| 8% WACC | €120 | €135 | €155 |
| 10% WACC | €95 | €105 | €120 |
| 12% WACC | €75 | €85 | €95 |

This shows range of possible values based on reasonable assumption changes.

#### When DCF Doesn't Work Well

**Avoid DCF for:**
- Unprofitable companies (negative FCF)
- Highly cyclical businesses (FCF varies wildly)
- Startups without operating history
- Companies with unpredictable cash flows
- Financial companies (banks, insurance)

**Use alternative methods** in these cases.

---

### Method 2: Relative Valuation (Peer Comparison)

**Best for**: All companies with profitable peers

**Weight in Final Valuation**: 30%

#### Core Valuation Multiples

**1. P/E Ratio (Price-to-Earnings)**

Formula: Stock Price / Earnings Per Share

**When to use:**
- Profitable companies
- Stable earnings
- Mature businesses

**Interpretation:**
- Low P/E (<15): Potentially undervalued or slower growth
- Medium P/E (15-25): Market average
- High P/E (>25): Growth expectations or overvalued

**Adjustments:**
- Use forward P/E (next 12 months) for growth companies
- Use trailing P/E (last 12 months) for mature companies
- Normalize earnings for cyclical businesses (use average through cycle)

**Peer Comparison Example:**
```
Target Company: 18x P/E
Peer 1: 22x P/E
Peer 2: 20x P/E
Peer 3: 19x P/E
Peer Average: 20.3x P/E

Target trades at 11% discount to peers
If discount justified: Fairly valued
If discount NOT justified: Undervalued
```

**2. EV/EBITDA (Enterprise Value to EBITDA)**

Formula: (Market Cap + Debt - Cash) / EBITDA

**When to use:**
- Capital-intensive businesses
- Companies with different debt levels
- Comparing companies with different tax rates

**Interpretation:**
- Low EV/EBITDA (<8): Potentially undervalued
- Medium EV/EBITDA (8-12): Market average
- High EV/EBITDA (>12): Premium valuation

**Advantages:**
- Ignores capital structure differences
- Less affected by depreciation methods
- Good for M&A comparisons

**3. Price-to-Sales (P/S)**

Formula: Market Cap / Annual Revenue

**When to use:**
- Unprofitable growth companies
- Companies with negative earnings
- Comparing companies with different margins

**Interpretation:**
- Low P/S (<2): Potentially undervalued
- Medium P/S (2-4): Market average
- High P/S (>4): Growth premium or overvalued

**Warning**: Can mask poor profitability

**4. Price-to-Book (P/B)**

Formula: Market Cap / Book Value of Equity

**When to use:**
- Asset-heavy companies (banks, real estate, manufacturing)
- Value investing approach
- Distressed companies

**Interpretation:**
- P/B < 1: Trading below book value (potentially undervalued or distressed)
- P/B 1-3: Normal range
- P/B > 3: Premium for intangibles or growth

**Less useful for:**
- Asset-light businesses (software, services)
- Companies with strong intangible assets

**5. PEG Ratio (Price/Earnings to Growth)**

Formula: P/E Ratio / Expected EPS Growth Rate

**When to use:**
- Growth companies
- Comparing companies with different growth rates

**Interpretation:**
- PEG < 1: Undervalued relative to growth
- PEG = 1: Fairly valued (Peter Lynch fair value)
- PEG > 1.5: Expensive relative to growth

**Example:**
- P/E = 25
- Expected growth = 20%
- PEG = 25 / 20 = 1.25 (reasonable)

**Limitations:**
- Only as good as growth estimates
- Doesn't consider growth quality or sustainability

#### Peer Selection Process

**1. Identify Direct Competitors (3-5 companies)**

**Criteria for good peers:**
- Same industry/sector
- Similar business model
- Comparable size (market cap within 3-5x)
- Similar geography
- Similar growth stage

**Example - Semiconductor Equipment:**
- Target: ASML
- Peers: Applied Materials, Lam Research, KLA Corp, Tokyo Electron

**2. Calculate Multiples for Each**

| Company | P/E | EV/EBITDA | P/S | ROE | Growth |
|---------|-----|-----------|-----|-----|--------|
| Target | 20x | 12x | 5x | 18% | 15% |
| Peer 1 | 25x | 15x | 6x | 22% | 20% |
| Peer 2 | 22x | 14x | 5.5x | 20% | 18% |
| Peer 3 | 18x | 11x | 4.5x | 16% | 12% |

**3. Adjust for Quality Differences**

If target has:
- Higher margins → Deserves premium multiple
- Faster growth → Deserves premium multiple
- Stronger moat → Deserves premium multiple
- Better ROIC → Deserves premium multiple

**4. Calculate Fair Value Range**

**Example using P/E:**
- Peer average P/E: 21.7x
- Target earnings: €5.00 per share
- Unadjusted fair value: €5.00 × 21.7 = €108.50

**Quality adjustment:**
- Target has higher ROE and margins (+10% premium)
- Target has slower growth (-5% discount)
- Net adjustment: +5% premium
- Adjusted fair value: €108.50 × 1.05 = €113.90

**Apply margin of safety: €113.90 × 0.85 = €96.80**

#### Historical Valuation Context

Compare current valuation to company's own history:

**Target Company P/E History:**
- Current: 20x
- 1-year avg: 22x
- 3-year avg: 19x
- 5-year avg: 18x
- 10-year avg: 17x

**Interpretation:**
- Trading slightly above long-term average
- Below recent peak
- Context needed: Has business improved? Or is market too optimistic?

#### Industry-Specific Multiples

Different industries have different "normal" multiples:

**Technology/Software:**
- High P/E (25-40x), high P/S (8-15x)
- Justified by high margins and growth

**Consumer Staples:**
- Medium P/E (18-25x), low P/S (1-2x)
- Stable, predictable, slower growth

**Industrials:**
- Low-medium P/E (12-18x), low P/S (0.8-1.5x)
- Cyclical, capital intensive

**Financials:**
- Low P/E (8-12x), use P/B (1-2x) instead
- Different business model (leverage)

**Healthcare/Pharma:**
- Medium-high P/E (20-30x), medium P/S (4-8x)
- Patent protection, R&D intensive

---

### Method 3: Peter Lynch Fair Value

**Best for**: Growth-at-reasonable-price (GARP) stocks

**Weight in Final Valuation**: 30%

#### The Peter Lynch Approach

**Core Principle**: A fairly priced stock should have P/E ratio equal to its growth rate.

**Fair Value P/E = Expected Growth Rate**

**PEG Ratio = P/E / Growth Rate**
- PEG = 1.0 → Fairly valued
- PEG < 1.0 → Undervalued
- PEG > 1.5 → Overvalued

#### Step-by-Step Process

**1. Determine Expected Growth Rate**

Use most conservative estimate from:
- Historical 5-year EPS growth
- Analyst consensus estimates
- Company guidance
- Industry growth expectations

**Example:**
- Historical growth: 18%
- Analyst estimates: 20%
- Company guidance: 15-17%
- **Use: 15% (most conservative)**

**2. Calculate Fair Value P/E**

**Fair Value P/E = Growth Rate**
Fair Value P/E = 15x (for 15% growth)

**3. Calculate Fair Value Price**

Fair Value = Fair Value P/E × Current EPS

**Example:**
- Fair Value P/E: 15x
- Current EPS: €4.00
- Fair Value = 15 × €4.00 = €60.00

**4. Quality Adjustments**

**Add premium (+2-5 points) if:**
- Low debt (debt/equity < 0.5)
- High ROE (>20%)
- Strong competitive moat
- Consistent dividend growth
- High profit margins (>20%)

**Subtract discount (-2-5 points) if:**
- High debt (debt/equity > 1.0)
- Low ROE (<10%)
- Weak competitive position
- Inconsistent earnings
- Cyclical business

**Adjusted Example:**
- Base fair value P/E: 15x
- High ROE (+2 points)
- Strong moat (+2 points)
- High debt (-2 points)
- **Adjusted fair value P/E: 17x**
- Fair value = 17 × €4.00 = €68.00

**5. Apply Margin of Safety**

Peter Lynch Fair Value = Adjusted Fair Value × (1 - 15%)
= €68.00 × 0.85 = **€57.80**

#### Peter Lynch Categories

**Slow Growers** (0-5% growth):
- Fair P/E: 5-10x
- Mature, dividend-paying
- Example: Utilities, some consumer staples

**Stalwarts** (8-12% growth):
- Fair P/E: 12-15x
- Large, stable companies
- Example: Coca-Cola, P&G

**Fast Growers** (15-25% growth):
- Fair P/E: 15-25x
- Most attractive for GARP
- Example: Growing tech companies

**Cyclicals** (Varies):
- P/E misleading at peaks
- Use normalized earnings
- Example: Industrials, materials

**Turnarounds** (Varies):
- Often negative earnings
- Buy before recovery
- High risk/reward

**Asset Plays** (Varies):
- P/B more relevant than P/E
- Hidden asset value
- Example: Real estate, natural resources

#### The Peter Lynch Checklist

For a stock to qualify as attractive:
- [ ] PEG < 1.0 (preferably < 0.75)
- [ ] P/E reasonable for growth rate
- [ ] Company has sustainable competitive advantages
- [ ] Debt manageable (can pay off in 2-3 years from FCF)
- [ ] Earnings growing consistently (not erratic)
- [ ] You understand the business
- [ ] Room to grow (not saturated market)
- [ ] Management aligned with shareholders

---

### Method 4: Asset-Based Valuation

**Best for**: Asset-heavy companies, financials, REITs, distressed companies

**Weight in Final Valuation**: Varies (primary for certain companies)

#### When to Use Asset-Based Valuation

**Primary valuation method for:**
- **Banks and Financial Institutions**: P/B is standard
- **REITs**: Net Asset Value (NAV) approach
- **Asset-heavy industrials**: Replacement value matters
- **Holding companies**: Sum-of-the-parts
- **Distressed/Liquidation scenarios**: Tangible book value

**Secondary consideration for:**
- Any company trading below book value
- Companies with significant real estate
- Natural resource companies

#### Book Value Approach

**1. Calculate Book Value of Equity**

Book Value = Total Assets - Total Liabilities

Or from balance sheet:
Book Value = Shareholders' Equity

**2. Calculate Book Value per Share**

Book Value per Share = Book Value / Shares Outstanding

**3. Compare to Stock Price**

P/B Ratio = Stock Price / Book Value per Share

**Interpretation:**
- P/B < 1.0: Trading below book (potential value or distress)
- P/B 1.0-3.0: Normal range
- P/B > 3.0: Premium for intangibles or growth

**4. Tangible Book Value (More Conservative)**

Tangible Book Value = Book Value - Intangible Assets - Goodwill

Removes:
- Goodwill from acquisitions
- Patents, trademarks
- Other intangibles

**More conservative measure** - "liquidation value" estimate

#### Adjusted Book Value

**Problem**: Historical cost accounting doesn't reflect current values

**Adjustments to consider:**

**1. Real Estate:**
- Book value: Purchase price minus depreciation
- Market value: Current property values
- Adjustment: Often significantly higher than book

**2. Inventory:**
- FIFO vs LIFO accounting differences
- Obsolete inventory may be overstated
- Adjust to net realizable value

**3. Intangibles:**
- Patents, brands may be worth more than book
- Or may be worthless (expired, obsolete)
- Assess actual value

**4. Liabilities:**
- Pension obligations (may be understated)
- Environmental liabilities
- Legal contingencies

**Adjusted Book Value Example:**
```
Reported Book Value: €1,000M
+ Real estate appreciation: +€200M
- Goodwill impairment: -€150M
- Obsolete inventory: -€50M
Adjusted Book Value: €1,000M
```

#### REIT Net Asset Value (NAV)

**For Real Estate Investment Trusts:**

**1. Calculate Property Values**
- Market value of properties (use cap rate)
- Or appraised values

**2. Subtract Debt**
Net Asset Value = Property Values - Debt

**3. Per Share NAV**
NAV per Share = NAV / Shares Outstanding

**4. Compare to Stock Price**
Price / NAV Ratio

**Typical REIT Valuation:**
- P/NAV < 0.9: Undervalued
- P/NAV 0.9-1.1: Fair value
- P/NAV > 1.1: Premium (quality properties, management)

#### Replacement Cost (Tobin's Q)

**For Asset-Heavy Businesses:**

**Tobin's Q = Market Cap / Replacement Cost of Assets**

**Interpretation:**
- Q < 1: Cheaper to buy company than build from scratch
- Q = 1: Market price equals replacement cost
- Q > 1: Premium for intangibles, market position

**Practical Application:**
Difficult to calculate precisely, but useful concept:
- If P/B < 1 for capital-intensive business, consider replacement cost
- Would it cost more to build this business than to buy it?

#### Sum-of-the-Parts (SOTP) Valuation

**For Conglomerates or Diversified Companies:**

**1. Identify Business Segments**
Break company into distinct businesses

**2. Value Each Segment Separately**
Use appropriate method for each:
- Mature segment: P/E multiple
- Growth segment: DCF or P/S
- Asset segment: Book value or NAV

**3. Sum All Segments**
Total Value = Segment 1 + Segment 2 + Segment 3...

**4. Add Corporate-Level Items**
- Cash and investments
- Corporate debt
- Pension obligations

**5. Calculate Per Share Value**
Fair Value per Share = Total Value / Shares Outstanding

**Example:**
```
Segment A (Mature): €2,000M (at 12x P/E)
Segment B (Growth): €3,000M (at DCF)
Segment C (Real Estate): €1,500M (at NAV)
+ Corporate cash: €500M
- Corporate debt: €1,000M
Total Value: €6,000M
Shares: 100M
Fair Value: €60 per share
```

---

## Synthesizing Multiple Valuation Methods

### The Weighted Average Approach

**Standard Weights:**
- DCF: 40%
- Relative Valuation: 30%
- Peter Lynch: 30%
- Asset-Based: (when applicable)

**Example Synthesis:**
```
DCF Fair Value: €80 × 40% = €32
Peer Relative: €95 × 30% = €28.50
Peter Lynch: €85 × 30% = €25.50
Weighted Average: €86
```

### Adjusting Weights Based on Situation

**Increase DCF weight (to 50%) when:**
- Highly predictable cash flows
- Stable, mature business
- Long operating history

**Decrease DCF weight (to 20%) when:**
- Unpredictable cash flows
- Cyclical business
- High-growth, uncertain future

**Increase Relative weight (to 40%) when:**
- Good peer group available
- Standard business model
- Industry multiples well-established

**Increase Asset-Based weight (to 40-50%) when:**
- Trading below book value
- Asset-rich company (REIT, financial)
- Distressed or liquidation scenario

### Fair Value Range

**Don't give single number - provide range:**

**Fair Value Range: €75 - €95**
- Low end: Conservative assumptions, high discount
- Mid point: Base case, standard discount
- High end: Optimistic assumptions, low discount

**Current price: €65**
- Margin of safety: 13-31%
- Assessment: Undervalued (adequate to excellent margin)

---

## Margin of Safety Requirements

### Benjamin Graham's Principle

**"The margin of safety is the difference between the intrinsic value of a stock and its market price."**

**Purpose:**
- Protects against errors in analysis
- Protects against unforeseen events
- Provides cushion for disappointing results
- Allows for multiple of upside potential

### Recommended Margins

**Standard Margin: 20-25%**
- For quality companies with predictable businesses
- Fair Value €100 → Buy below €75-80

**Minimum Margin: 15%**
- For very high-quality, low-risk companies
- Fair Value €100 → Buy below €85

**Elevated Margin: 30-40%**
- For cyclical businesses
- For companies with uncertain futures
- For speculative situations
- Fair Value €100 → Buy below €60-70

### Margin of Safety in Practice

**If Fair Value = €100:**

| Margin | Buy Below | Interpretation |
|--------|-----------|----------------|
| 10% | €90 | Insufficient - too little cushion |
| 15% | €85 | Minimum - for highest quality only |
| 20% | €80 | Standard - adequate protection |
| 25% | €75 | Good - solid margin |
| 30% | €70 | Excellent - significant upside |
| 40%+ | <€60 | Outstanding - compelling value |

### When Current Price Above Fair Value

**Current: €110, Fair Value: €100**
- Premium: 10%
- Recommendation: **AVOID** or **SELL**
- Explanation: Paying premium without margin of safety

**Exception**: High-quality growth companies
- May accept 0-10% premium if:
  - Very strong competitive moat
  - Accelerating growth
  - Near-term catalysts
- But NEVER more than 10% premium

---

## Valuation Red Flags

### Warning Signs of Overvaluation

1. **P/E > 40x** (unless hypergrowth with clear path)
2. **PEG > 2.0** (paying too much for growth)
3. **Price > 2x fair value** (extreme overvaluation)
4. **EV/Sales > 10x** (even for growth companies)
5. **No margin of safety** (current price = or > fair value)

### Warning Signs Analysis May Be Wrong

1. **Valuations wildly different** (DCF says €50, peers say €150)
   - Re-examine assumptions
   - Which method is more reliable for this company?

2. **Fair value far from current market price** (>50% difference)
   - Market may know something you don't
   - Or market may be wrong (opportunity!)
   - Requires high conviction to act

3. **Highly sensitive to assumptions** (DCF varies €50-€150)
   - Indicates high uncertainty
   - Use wider margin of safety
   - May want to avoid

4. **All growth assumptions at upper end of range**
   - Be more conservative
   - Reality often disappoints optimism

5. **Ignoring obvious risks in valuation**
   - Price in identified risks
   - Don't just hope they don't materialize

---

## Industry-Specific Valuation Considerations

### Technology/Software
- Use: DCF (if positive FCF), P/S, EV/Sales
- Focus: Revenue growth, customer acquisition cost, retention
- Multiples: High (P/E 30-50x, P/S 8-15x for SaaS)

### Semiconductors
- Use: DCF, P/E, EV/EBITDA
- Focus: Cyclicality, capex cycles, technology leadership
- Multiples: Medium (P/E 15-25x), use normalized earnings

### Consumer Discretionary
- Use: P/E, EV/EBITDA, P/S
- Focus: Brand strength, comp sales, margins
- Multiples: Medium (P/E 15-25x)

### Consumer Staples
- Use: P/E, EV/EBITDA, dividend yield
- Focus: Stability, pricing power, market share
- Multiples: Medium-high (P/E 20-28x) for quality

### Healthcare/Pharma
- Use: DCF (careful), P/E, EV/EBITDA
- Focus: Pipeline, patent cliffs, R&D productivity
- Multiples: Medium-high (P/E 20-30x)

### Financials/Banks
- Use: P/B, P/E (careful with earnings quality)
- Focus: ROE, net interest margin, credit quality
- Multiples: Low (P/E 8-12x, P/B 1-2x)

### Industrials
- Use: P/E (normalized), EV/EBITDA, DCF
- Focus: Cyclicality, operating leverage, backlog
- Multiples: Medium (P/E 15-20x), use through-cycle earnings

### REITs
- Use: NAV, FFO multiples, dividend yield
- Focus: Property quality, occupancy, debt levels
- Multiples: P/NAV 0.9-1.1x, yield 3-5%

### Energy
- Use: EV/Production, P/CF, NAV for reserves
- Focus: Commodity prices, reserves, costs
- Multiples: Highly variable with oil prices

---

## Final Valuation Checklist

Before finalizing fair value estimate:

- [ ] Used multiple valuation methods (minimum 2, preferably 3)
- [ ] Compared to 3-5 direct peer companies
- [ ] Used conservative assumptions throughout
- [ ] Checked historical valuation context
- [ ] Considered industry-specific factors
- [ ] Applied appropriate margin of safety (minimum 15%)
- [ ] Created fair value range, not single point
- [ ] Sensitivity tested key assumptions
- [ ] Explained reasoning for each method's weight
- [ ] Identified key risks that could change valuation
- [ ] Checked for qualitative factors missed in numbers
- [ ] Honest about limitations and uncertainties

**Remember**: Valuation is an input to decision-making, not the decision itself. Combine with qualitative analysis, risk assessment, and investment opportunity evaluation.
