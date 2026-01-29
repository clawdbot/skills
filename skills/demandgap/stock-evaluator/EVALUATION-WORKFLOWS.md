# Stock Evaluation Workflows

## Overview

This guide provides step-by-step workflows for the two primary use cases:
1. **Single Stock Evaluation** - Deep analysis of one potential investment
2. **Watchlist Analysis** - Comparative analysis of multiple candidates

---

## Workflow 1: Single Stock Evaluation

### Use Case
User asks: "Should I buy [TICKER]?" or "Analyze [TICKER] as a potential investment"

### Complete Step-by-Step Process

#### Phase 1: Initial Research & Context (5-10 minutes)

**Step 1: Gather Basic Information**
- Search: "[TICKER] investor relations"
- Search: "[TICKER] latest 10-K"
- Search: "[TICKER] latest earnings call"

**Collect:**
- Company name and business description
- Current stock price
- Market capitalization
- Recent stock performance (52-week range)
- Latest earnings date

**Step 2: Check Portfolio Context**
- Review project knowledge for existing portfolio
- Is this stock already owned?
  - **If YES**: Suggest using Portfolio Analyst instead
  - **If NO**: Proceed with evaluation
- Check sector exposure (avoid over-concentration)

**Step 3: Quick Quality Screen**
Verify company meets minimum quality thresholds:
- [ ] Profitable? (Positive net income)
- [ ] Positive free cash flow?
- [ ] Debt < Annual Revenue?
- [ ] 5+ years of operating history?

**If fails multiple criteria**: Flag as speculative/high-risk upfront

---

#### Phase 2: Business Understanding (15-20 minutes)

**Step 4: Read Latest 10-K**

**Research Order (Critical):**
1. **Latest 10-K first** - Start with "Business" and "Management's Discussion" sections
2. **Go back 5-10 years** - Skim historical 10-Ks to understand evolution
3. **Recent 10-Qs** - Last 2-3 quarters for current trajectory

**Extract:**
- **Business model**: How do they make money?
- **Products/services**: What do they sell?
- **Revenue breakdown**: Geographic and segment mix
- **Customers**: Who buys from them? Any concentration?
- **Competition**: Who are the main competitors?

**Step 5: Identify Competitive Advantages (Moat)**

**Assess each potential moat source:**
- **Network effects**: Product gets better with more users?
- **Brand power**: Can charge premium prices?
- **Switching costs**: Hard for customers to leave?
- **Regulatory barriers**: Patents, licenses, regulations?
- **Cost advantages**: Scale, technology, location?
- **Intangible assets**: Patents, trade secrets, data?

**Moat Classification:**
- **Wide**: Multiple strong moat sources, sustainable 10+ years
- **Narrow**: One or two moat sources, sustainable 5-10 years
- **None**: Commodity business, competitive market

**Step 6: Evaluate Management**

**Read/Listen to:**
- CEO letter in latest annual report
- Recent earnings call transcript (management Q&A)
- Investor presentation

**Assess:**
- **Competence**: Track record of execution?
- **Transparency**: Honest about challenges?
- **Capital allocation**: Smart use of cash (dividends, buybacks, acquisitions, R&D)?
- **Alignment**: Management compensation tied to long-term value?

**Check insider trading:**
- Search: "[TICKER] insider transactions"
- Buying = bullish signal
- Selling = neutral (could be personal reasons)

**Management Rating: Excellent / Good / Adequate / Concerning**

**Step 7: Identify Direct Competitors (3-5 companies)**

**Selection criteria:**
- Same industry
- Similar business model
- Comparable size (within 3-5x market cap)
- Similar geography

**Example - Payment Processor:**
- Target: Square (SQ)
- Peers: PayPal, Stripe, Adyen, Fiserv

**Document for later peer comparison**

---

#### Phase 3: Financial Analysis (20-30 minutes)

**Step 8: Analyze Financial Trends (5-10 Year View)**

**Revenue Growth:**
| Year | Revenue | YoY Growth | 5-Yr CAGR |
|------|---------|-----------|-----------|
| 2020 | €XM | | |
| 2021 | €XM | X% | |
| 2022 | €XM | X% | |
| 2023 | €XM | X% | |
| 2024 | €XM | X% | X% |

**Assessment:**
- Accelerating / Stable / Decelerating?
- Consistent or erratic?
- How does it compare to industry?

**Profitability Margins:**
| Year | Gross Margin | Operating Margin | Net Margin |
|------|--------------|------------------|------------|
| 2020 | X% | X% | X% |
| 2024 | X% | X% | X% |

**Trend:** Expanding / Stable / Declining
**Driver:** Scale / Pricing / Cost management / Competition

**Cash Flow Quality:**
| Year | Op. Cash Flow | Capex | Free Cash Flow |
|------|---------------|-------|----------------|
| 2020 | €XM | €XM | €XM |
| 2024 | €XM | €XM | €XM |

**Assessment:**
- Consistently positive?
- Growing with revenue?
- FCF conversion (FCF / Net Income): >80% is good

**Balance Sheet Strength:**
- Cash & Equivalents: €XM
- Total Debt: €XM
- Net Debt (Debt - Cash): €XM
- Debt/Revenue ratio: X.X (<1.0 is good)

**Assessment:** Strong / Adequate / Concerning

**Step 9: Calculate Quality Metrics**

| Metric | Current | Target | Pass? |
|--------|---------|--------|-------|
| ROE | X% | >15% | ✓/✗ |
| Profit Margin | X% | >15% | ✓/✗ |
| Gross Margin | X% | >30% | ✓/✗ |
| Debt/Revenue | X.X | <1.0 | ✓/✗ |
| FCF Positive | Yes/No | Yes | ✓/✗ |
| Revenue Growth (5yr) | X% | >0% | ✓/✗ |

**Quality Score: X/6 criteria passed**
- 5-6: High quality
- 3-4: Moderate quality
- 0-2: Low quality (proceed with caution)

**Step 10: Identify Red Flags**

**Warning signs to check:**
- [ ] Declining margins despite revenue growth
- [ ] Negative or inconsistent free cash flow
- [ ] Debt growing faster than revenue
- [ ] Losing market share to competitors
- [ ] Frequent guidance misses
- [ ] Accounting irregularities
- [ ] High customer/supplier concentration (>50%)
- [ ] Key person dependency (founder-led with no succession)

**Document any red flags found**

---

#### Phase 4: Peer Comparison (15-20 minutes)

**Step 11: Research Peer Companies**

For each of 3-5 competitors:
- Search: "[PEER] latest 10-K"
- Extract key metrics
- Read analyst reports if available

**Step 12: Build Comparison Table**

| Company | Mkt Cap | Rev Growth | Gross Margin | Net Margin | ROE | P/E | EV/EBITDA | P/S | Moat |
|---------|---------|-----------|--------------|------------|-----|-----|-----------|-----|------|
| Target | €XB | X% | X% | X% | X% | X.X | X.X | X.X | [Rating] |
| Peer 1 | €XB | X% | X% | X% | X% | X.X | X.X | X.X | [Rating] |
| Peer 2 | €XB | X% | X% | X% | X% | X.X | X.X | X.X | [Rating] |
| Peer 3 | €XB | X% | X% | X% | X% | X.X | X.X | X.X | [Rating] |
| Average | | X% | X% | X% | X% | X.X | X.X | X.X | |

**Step 13: Assess Relative Position**

**Questions to answer:**
1. Is target the best company in the group? (highest margins, ROE, growth)
2. Does target's valuation reflect its quality? (better = higher multiple justified)
3. Is there a clear winner among peers? (buy the best, avoid the rest)
4. Where does target rank? (#1, #2, #3...)

**Comparative Assessment:**
- Best-in-class / Above average / Average / Below average

---

#### Phase 5: Valuation Analysis (30-40 minutes)

**Step 14: DCF Valuation** (See VALUATION-GUIDE.md for details)

**Quick DCF Steps:**
1. Project FCF for 5-10 years (use conservative growth)
2. Calculate terminal value (use 2-3% perpetual growth)
3. Discount to present (use 10-12% WACC typically)
4. Add cash, subtract debt
5. Divide by diluted shares
6. Apply 15-30% margin of safety

**DCF Fair Value: €X.XX**
**Sensitivity Range: €X.XX - €X.XX** (with different assumptions)

**Step 15: Relative Valuation**

**Calculate target's fair value using peer multiples:**

**P/E Method:**
- Peer average P/E: X.X
- Target EPS: €X.XX
- Unadjusted fair value: €X.XX
- Quality adjustment: [+/-X%]
- Adjusted fair value: €X.XX

**Repeat for:**
- EV/EBITDA method
- P/S method (if growth company)
- P/B method (if asset-heavy)

**Relative Fair Value Range: €X.XX - €X.XX**

**Step 16: Peter Lynch Fair Value**

1. Expected growth rate (use conservative estimate): X%
2. Fair value P/E = Growth rate = X
3. Current EPS: €X.XX
4. Base fair value: €X.XX
5. Quality adjustments: [+/- points for moat, debt, margins]
6. Adjusted P/E: X
7. Peter Lynch fair value: €X.XX

**Step 17: Synthesize Valuation**

| Method | Fair Value | Weight | Weighted Value |
|--------|-----------|--------|----------------|
| DCF | €X.XX | 40% | €X.XX |
| Peer Relative | €X.XX | 30% | €X.XX |
| Peter Lynch | €X.XX | 30% | €X.XX |
| **Weighted Average** | | **100%** | **€X.XX** |

**Fair Value Estimate: €X.XX**
**Fair Value Range: €X.XX - €X.XX** (Conservative to Optimistic)

**Current Price: €X.XX**
**Margin of Safety: X%** (Excellent >30% / Good 20-30% / Adequate 15-20% / Insufficient <15%)

**Valuation Conclusion: UNDERVALUED / FAIRLY VALUED / OVERVALUED**

---

#### Phase 6: Technical Analysis (10-15 minutes)

**Step 18: Analyze Price Action**

**Chart Review (Last 60 days):**
- Trend: Uptrend / Downtrend / Range-bound
- Recent high: €X.XX
- Recent low: €X.XX
- Current: €X.XX
- Volume: Increasing on rallies? / Declining?

**Step 19: Identify Key Levels**

**Support Levels** (where buying interest emerges):
- Primary support: €X.XX (recent low / moving average / prior breakout level)
- Secondary support: €X.XX

**Resistance Levels** (where selling pressure increases):
- Primary resistance: €X.XX (recent high / round number / prior breakdown level)
- Secondary resistance: €X.XX

**Step 20: Check Technical Indicators**

**RSI (Relative Strength Index):**
- Current: X
- Interpretation: Overbought (>70) / Neutral (30-70) / Oversold (<30)

**MACD:**
- Position: Above signal line / Below signal line
- Recent crossover: Bullish / Bearish / None
- Momentum: Accelerating / Decelerating / Neutral

**Moving Averages:**
- 50-day MA: €X.XX - Price is [above/below]
- 200-day MA: €X.XX - Price is [above/below]
- Trend: [Golden cross / Death cross / Neutral]

**Step 21: Determine Entry Strategy**

**Technical Setup: Bullish / Neutral / Bearish**

**If Bullish Setup:**
- "Buy now at market (€X.XX)"
- Ideal entry: €X.XX - €X.XX

**If Neutral Setup:**
- "Wait for pullback to €X.XX support"
- Or "Buy on breakout above €X.XX resistance"

**If Bearish Setup:**
- "Wait - avoid until setup improves"
- "Requires break above €X.XX to turn bullish"

**Entry Price Range: €X.XX - €X.XX**
**Maximum Buy Price: €X.XX** (above this, risk/reward unfavorable)

---

#### Phase 7: Risk & Catalyst Assessment (10-15 minutes)

**Step 22: Identify Key Risks**

**Company-Specific Risks:**
1. [Risk]: [Description and potential impact] - Probability: High/Med/Low
2. [Risk]: [Description and potential impact] - Probability: High/Med/Low
3. [Risk]: [Description and potential impact] - Probability: High/Med/Low

**Industry Risks:**
1. [Risk]: [Description] - Probability: High/Med/Low

**Macro Risks:**
1. [Risk]: [Description] - Probability: High/Med/Low

**Overall Risk Level: Low / Moderate / High**

**Step 23: Identify Catalysts**

**Near-Term (0-6 months):**
- [Date]: Earnings announcement
- [Date]: Product launch / event
- [Timeframe]: Regulatory decision

**Medium-Term (6-18 months):**
- Market expansion
- New product cycle
- Margin improvement initiatives

**Long-Term (18+ months):**
- Structural industry trend
- Technology leadership
- Market share gains

**Expected Timeline to Target: [6-12 months / 1-3 years / 3-5+ years]**

---

#### Phase 8: Bull vs. Bear Case (15-20 minutes)

**Step 24: Build Bull Case**

**Potential Upside: €X.XX (+X%)**

**Three strongest bull arguments:**
1. [Argument with specific evidence]
2. [Argument with specific evidence]
3. [Argument with specific evidence]

**For this to happen:**
- [Required condition]
- [Required condition]

**Step 25: Build Bear Case**

**Potential Downside: €X.XX (-X%)**

**Three strongest bear arguments:**
1. [Risk with specific reasoning]
2. [Risk with specific reasoning]
3. [Risk with specific reasoning]

**This happens if:**
- [Risk trigger]
- [Risk trigger]

**Step 26: Balance Assessment**

**Which case is more probable: Bull / Bear / Balanced**

**Reasoning:**
[2-3 paragraphs weighing evidence:
- Quality and quantity of evidence for each side
- Historical precedent and company track record
- Management competence and execution ability
- Industry dynamics (tailwinds vs headwinds)
- Current valuation (does price reflect risks?)
- Risk/reward assessment]

---

#### Phase 9: Investment Decision (10 minutes)

**Step 27: Determine Recommendation**

**Decision Matrix:**

| Valuation | Fundamentals | Technicals | Risk | → Recommendation |
|-----------|-------------|-----------|------|------------------|
| Undervalued (>15%) | Strong | Bullish/Neutral | Low-Mod | **BUY** |
| Undervalued (>15%) | Strong | Bearish | Moderate | **HOLD** (wait for setup) |
| Fairly Valued (±15%) | Strong | Any | Low-Mod | **HOLD** |
| Overvalued (>15%) | Any | Any | Any | **SELL/AVOID** |
| Any | Weak | Any | High | **AVOID** |

**Final Recommendation: BUY / HOLD / SELL/AVOID**
**Conviction: Strong Buy / Buy / Hold / Avoid**

**Step 28: Define Entry/Exit Strategy**

**If BUY:**
- **Ideal Entry: €X.XX - €X.XX**
- **Maximum Buy Price: €X.XX**
- **Approach**: [Buy now / Wait for pullback / Buy on breakout]

**Exit Strategy:**
- **12-Month Target: €X.XX** (+X%)
- **Stop Loss: €X.XX** (-X%)
- **Sell If**: [Thesis-breaking conditions]

**Step 29: Determine Position Sizing**

**Allocation Guidance:**
- Strong Buy + Low Risk = 5-8% position (max 10%)
- Buy + Moderate Risk = 3-5% position (max 7%)
- Speculative + High Risk = 1-3% position (max 5%)

**Recommended Allocation: X-X%**
**Specific: X%**

**Rationale:**
- Conviction: [Strong Buy / Buy]
- Risk: [Low / Moderate / High]
- Diversification: [Sector exposure check]
- Liquidity: [Can exit easily?]

---

#### Phase 10: Documentation & Deliverables (10 minutes)

**Step 30: Final Checklist Verification**

- ☐ Technical Analysis Complete
- ☐ Fundamental Analysis Complete
- ☐ Valuation Assessment Complete (multiple methods)
- ☐ Bull vs. Bear Case Complete
- ☐ Clear Recommendation (BUY/HOLD/SELL)
- ☐ Alternative Candidates (if SELL - provide 3-5)

**Step 31: Write Executive Summary**

**2-3 sentence bottom-line:**
- Recommendation + Conviction
- Key reason supporting the recommendation
- Most important risk or opportunity

**Step 32: Compile Research Sources**

**Document:**
- 10-K filings reviewed (years)
- 10-Q filings reviewed (quarters)
- Earnings calls listened to (dates)
- Competitor research conducted
- Confidence level (High/Medium/Low)

**Step 33: Provide Alternative Candidates (if SELL)**

If recommending SELL/AVOID, provide 3-5 better alternatives:
- Similar sector/industry
- Better fundamentals or valuation
- 1-2 paragraph rationale each

---

### Single Stock Evaluation Timeline

**Total Time: 2.5-3.5 hours for thorough analysis**

- Initial Research: 10 min
- Business Understanding: 20 min
- Financial Analysis: 30 min
- Peer Comparison: 20 min
- Valuation: 40 min
- Technical Analysis: 15 min
- Risk/Catalysts: 15 min
- Bull/Bear Case: 20 min
- Decision & Sizing: 10 min
- Documentation: 10 min

**For experienced analyst**: Can be done in 2 hours
**For complex company**: May take 4-5 hours

---

## Workflow 2: Watchlist Analysis

### Use Case
User provides list of 5-15 stocks they're considering and wants comparative analysis to identify best opportunities.

### Streamlined Process (Per Stock)

#### Phase 1: Quick Quality Screen (10 min per stock)

**For each stock:**

**Step 1: Basic Research**
- Search: "[TICKER] latest 10-K"
- Current price and market cap
- Recent performance

**Step 2: Quality Metrics Check**

| Ticker | Profitable? | Positive FCF? | Debt<Revenue? | ROE>15%? | Quality Score |
|--------|------------|--------------|--------------|----------|---------------|
| Stock 1 | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | X/4 |
| Stock 2 | ✓/✗ | ✓/✗ | ✓/✗ | ✓/✗ | X/4 |
| ... | | | | | |

**Step 3: Initial Triage**

**Eliminate immediately:**
- Quality score 0-1 (multiple failures)
- Recent accounting issues
- Severe financial distress
- Complete lack of moat

**Advance to Phase 2:**
- Quality score 2-4
- Reasonable fundamentals
- Some competitive advantage

**Result: Narrow list from 10-15 to 5-8 candidates**

---

#### Phase 2: Comparative Business Analysis (15 min per stock)

**Step 4: Business Model Summary**

For each remaining candidate:

| Ticker | Business Model | Revenue | Moat | Management | Industry |
|--------|---------------|---------|------|------------|----------|
| Stock 1 | [1 sentence] | €XB | Wide/Narrow/None | Good/Adequate | [Sector] |
| Stock 2 | [1 sentence] | €XB | Wide/Narrow/None | Good/Adequate | [Sector] |
| ... | | | | | |

**Step 5: Identify Best-in-Class**

**Within each sector represented:**
- Who has widest moat?
- Who has best management?
- Who has strongest financials?

**Result: Rank candidates within sectors**

---

#### Phase 3: Financial Comparison (10 min per stock)

**Step 6: Build Financial Comparison Table**

| Ticker | Rev Growth (5yr) | Gross Margin | Net Margin | ROE | Debt/Rev | FCF (TTM) |
|--------|-----------------|--------------|------------|-----|----------|-----------|
| Stock 1 | X% | X% | X% | X% | X.X | €XM |
| Stock 2 | X% | X% | X% | X% | X.X | €XM |
| Stock 3 | X% | X% | X% | X% | X.X | €XM |
| ... | | | | | | |
| Best | [Ticker] | [Ticker] | [Ticker] | [Ticker] | [Ticker] | [Ticker] |

**Step 7: Score Each Stock**

**Quality Score (0-10 points):**
- Rev growth >15%: +2
- Gross margin >40%: +2
- Net margin >20%: +2
- ROE >20%: +2
- Debt/Rev <0.5: +2

| Ticker | Quality Score | Ranking |
|--------|--------------|---------|
| Stock 1 | 8/10 | #1 |
| Stock 2 | 6/10 | #2 |
| ... | | |

---

#### Phase 4: Valuation Comparison (20 min per stock)

**Step 8: Quick Valuation for Each**

**Simplified approach for watchlist:**
- Primary method: Peer relative valuation (fastest)
- Secondary: Peter Lynch (if growth company)
- Skip full DCF (too time-intensive for multiple stocks)

**For each stock:**

| Ticker | Current Price | P/E | Peer Avg P/E | PEG | Fair Value Est. | Margin of Safety |
|--------|--------------|-----|--------------|-----|-----------------|------------------|
| Stock 1 | €X.XX | X.X | X.X | X.X | €X.XX | X% |
| Stock 2 | €X.XX | X.X | X.X | X.X | €X.XX | X% |
| ... | | | | | | |

**Step 9: Identify Best Values**

**Sort by margin of safety (highest first):**
1. Stock X: X% undervalued
2. Stock Y: Y% undervalued
3. Stock Z: Z% undervalued

**Eliminate:**
- Stocks with <10% margin of safety (not compelling)
- Stocks >20% overvalued (avoid)

---

#### Phase 5: Risk-Adjusted Ranking (10 min per stock)

**Step 10: Quick Risk Assessment**

| Ticker | Quality Score | Margin of Safety | Risk Level | Risk-Adj. Rank |
|--------|--------------|-----------------|------------|----------------|
| Stock 1 | 8/10 | 25% | Low | #1 |
| Stock 2 | 6/10 | 30% | Moderate | #2 |
| Stock 3 | 7/10 | 15% | Moderate | #3 |

**Risk-Adjusted Ranking Formula:**
- High quality + High margin + Low risk = Top rank
- Lower quality or higher risk = Lower rank even with good margin

**Step 11: Final Triage to Top 3-5**

**Criteria for Top 5:**
- Quality score ≥6/10
- Margin of safety ≥15%
- Risk level ≤ Moderate
- No significant red flags

---

#### Phase 6: Deep Dive on Top 3-5 (Follow Single Stock Workflow)

**Step 12: Full Analysis on Finalists**

For the top 3-5 candidates, perform **full single stock evaluation**:
- Complete business analysis
- Detailed financial analysis
- Comprehensive valuation (all methods)
- Technical analysis
- Bull/Bear case
- Entry/exit strategy
- Position sizing

**Time per stock: 2.5-3 hours**
**Total for top 5: 12-15 hours**

---

#### Phase 7: Final Ranking & Recommendations (30 min)

**Step 13: Create Final Comparison**

| Rank | Ticker | Conviction | Fair Value | Upside | Risk | Rec Allocation | Rationale |
|------|--------|-----------|-----------|--------|------|----------------|-----------|
| #1 | [TICK] | Strong Buy | €XX | +X% | Low | 5-8% | [1 sentence] |
| #2 | [TICK] | Buy | €XX | +X% | Mod | 3-5% | [1 sentence] |
| #3 | [TICK] | Buy | €XX | +X% | Mod | 3-5% | [1 sentence] |

**Step 14: Portfolio Construction Recommendation**

**Suggested approach:**
- **Buy immediately**: Top 1-2 with best setups
- **Buy on pullback**: #3-4 if technically extended
- **Monitor closely**: #5+ for future opportunities

**Total allocation**: X-X% across top 3-5 picks

**Diversification check:**
- Multiple sectors represented?
- Different risk profiles?
- Different time horizons?

---

### Watchlist Analysis Timeline

**For 10-stock watchlist:**

- Quick Screen (10 stocks × 10 min): 1.5-2 hours
- Comparative Analysis (8 stocks × 15 min): 2 hours
- Valuation (8 stocks × 20 min): 2.5 hours
- Risk Ranking: 1.5 hours
- Deep Dive (top 5 × 2.5 hours): 12-15 hours
- Final Ranking: 30 min

**Total: 20-25 hours for comprehensive watchlist analysis**

**Streamlined version (top 3 only): 12-15 hours**

---

## Efficiency Tips for Both Workflows

### Research Shortcuts

**Use AI to Speed Up:**
- Summarize 10-K filings
- Extract key metrics from multiple years
- Identify main competitors
- Flag red flags in financial statements

**But always:**
- Verify AI summaries against original documents
- Use own judgment for interpretation
- Don't let AI make valuation decisions

### Template Usage

**Create reusable templates for:**
- Financial trend analysis tables
- Peer comparison tables
- Valuation synthesis tables
- Risk assessment checklists

**Saves 20-30% of time**

### Focus Areas

**Spend more time on:**
- Valuation (most critical)
- Competitive moat assessment
- Risk identification

**Spend less time on:**
- Overly precise financial projections
- Excessive peer research (3-5 is enough)
- Historical analysis >10 years old

### Red Flag Triggers

**Stop immediately and reassess if:**
- Multiple quality criteria failures
- Obvious red flags emerge (fraud, insolvency)
- Better alternatives clearly available
- Analysis becomes too uncertain (>50% variation in fair value)

**Don't waste time on obvious passes**

---

## Quality Control Checklist

### Before Finalizing Any Recommendation

**Completeness:**
- [ ] All mandatory deliverables completed
- [ ] Both bull and bear cases presented
- [ ] Multiple valuation methods used
- [ ] Specific entry/exit prices provided
- [ ] Position sizing recommendation included
- [ ] Risk level assessed
- [ ] Alternative candidates provided (if SELL)

**Accuracy:**
- [ ] Numbers verified against source documents
- [ ] Calculations double-checked
- [ ] Peer comparisons use correct data
- [ ] Industry context considered

**Clarity:**
- [ ] Recommendation is unmistakable (BUY/HOLD/SELL)
- [ ] Conviction level clear (Strong Buy/Buy/Hold/Avoid)
- [ ] Reasoning is specific with evidence
- [ ] Technical jargon explained
- [ ] Executive summary captures key points

**Objectivity:**
- [ ] Confirmation bias checked (considered contrary evidence)
- [ ] Both sides presented fairly
- [ ] Risks explicitly acknowledged
- [ ] Limitations stated clearly
- [ ] No unsupported claims

---

## Common Pitfalls to Avoid

### Analysis Pitfalls

**❌ Anchoring bias**: Don't fixate on current price
- Evaluate based on intrinsic value, not price paid or current quote

**❌ Recency bias**: Don't overweight recent quarters
- Look at 5-10 year trends, not just last quarter

**❌ Confirmation bias**: Don't seek only supporting evidence
- Actively seek contrary evidence and risks

**❌ Complexity bias**: Don't assume complex = better
- Simple businesses often best investments

**❌ Precision illusion**: Don't confuse precision with accuracy
- Better approximately right than precisely wrong

### Valuation Pitfalls

**❌ Single method reliance**: Don't use only DCF or only P/E
- Use multiple methods and synthesize

**❌ Heroic assumptions**: Don't project 30% growth forever
- Use conservative, realistic assumptions

**❌ Ignoring margin of safety**: Don't buy at fair value
- Require minimum 15% margin of safety

**❌ Paying for hope**: Don't overpay for growth that may not materialize
- Growth must be probable, not just possible

### Recommendation Pitfalls

**❌ Vague recommendations**: Don't say "interesting opportunity"
- Say BUY at €X.XX or below, position size X%

**❌ Missing downside**: Don't present only bull case
- Always show what could go wrong

**❌ No risk management**: Don't recommend buying without stop loss
- Define clear exit conditions

**❌ Ignoring portfolio context**: Don't recommend in vacuum
- Consider sector concentration and diversification

---

## Continuous Improvement

### Track Record

**For each recommendation:**
- Document recommendation date and price
- Track subsequent price movement
- Note if thesis played out or not
- Learn from successes and failures

### Pattern Recognition

**Over time, identify:**
- Which valuation methods work best for which industries
- Which quality metrics most predictive
- Which risks most important to monitor
- Which technical setups most reliable

### Skill Development

**Improve through:**
- Reading great investor letters (Buffett, Munger, Klarman)
- Studying past successful analyses
- Learning from mistakes (write post-mortems)
- Building industry expertise over time

**Goal**: Get better at identifying quality businesses, estimating fair value, and timing entries to generate superior returns.
