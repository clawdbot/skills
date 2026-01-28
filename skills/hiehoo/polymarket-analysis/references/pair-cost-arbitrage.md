# Pair Cost Arbitrage Strategy

Exploit pricing inefficiencies where YES + NO shares cost less than guaranteed $1.00 payout.

## Mathematical Foundation

```
Pair Cost = (Total_Cost_YES / Qty_YES) + (Total_Cost_NO / Qty_NO)

If Pair Cost < 1.00:
  Guaranteed Profit = min(Qty_YES, Qty_NO) - (Cost_YES + Cost_NO)
```

## Detection Process

### Step 1: Fetch Order Book
```bash
curl "https://gamma-api.polymarket.com/markets/{market_id}"
```

Extract: `outcomePrices`, `bestBid`, `bestAsk` for both outcomes.

### Step 2: Calculate Pair Cost

```
YES_price + NO_price = Pair Cost
Target: Pair Cost < 0.99 (1% margin minimum)
```

### Step 3: Simulate Fill

Account for slippage across order book depth:
- Small orders (<$500): Use best bid/ask
- Large orders (>$500): Walk the book, calculate avg fill price

### Step 4: Profit Calculation

```
Example:
- Buy 1000 YES @ $0.52 = $520
- Buy 1000 NO @ $0.47 = $470
- Total Cost = $990
- Pair Cost = 0.52 + 0.47 = 0.99
- Guaranteed Payout = $1000
- Profit = $10 (1.01% return)
```

## Opportunity Criteria

| Metric | Threshold | Rationale |
|--------|-----------|-----------|
| Pair Cost | < 0.99 | Minimum 1% gross margin |
| Liquidity | > $1000 each side | Ensure executable size |
| Time to Resolution | < 24h preferred | Faster capital turnover |
| Spread | < 3% | Avoid illiquid markets |

## Risk Factors

- **Slippage:** Large orders move price; simulate book depth
- **Timing:** Prices change rapidly; stale data = failed arb
- **Resolution Risk:** Market cancelled/voided = funds locked
- **Gas Fees:** MATIC network fees reduce thin margins

## Output Format

```markdown
### Pair Cost Opportunity

**Market:** [Name]
**Pair Cost:** $X.XX (X.X% below $1.00)
**Max Size:** $X,XXX (based on book depth)
**Est. Profit:** $XX.XX
**Confidence:** [High/Med/Low]
**Risk:** [Key concern]
```

## API Endpoints

- Markets list: `GET /markets`
- Market details: `GET /markets/{id}`
- Order book: `GET /book/{token_id}`
