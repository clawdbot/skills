# Polymarket API Reference

Gamma API endpoints for market data retrieval.

## Base URL

```
https://gamma-api.polymarket.com
```

## Endpoints

### List Markets
```bash
GET /markets
GET /markets?closed=false&active=true
```

Response fields:
- `id`: Market identifier
- `question`: Market question text
- `outcomes`: ["Yes", "No"] or multi-outcome
- `outcomePrices`: Current prices array
- `volume`: Total traded volume
- `liquidity`: Current liquidity
- `endDate`: Resolution date

### Market Details
```bash
GET /markets/{market_id}
```

Additional fields:
- `description`: Full market description
- `resolutionSource`: Oracle/resolution info
- `tags`: Category tags
- `conditionId`: On-chain condition ID

### Order Book
```bash
GET /book/{token_id}
```

Returns:
- `bids`: Buy orders [price, size]
- `asks`: Sell orders [price, size]
- `spread`: Current bid-ask spread

### Price History
```bash
GET /prices/{token_id}?interval=1h&fidelity=1
```

Intervals: `1m`, `5m`, `15m`, `1h`, `4h`, `1d`

### User Positions
```bash
GET /positions?user={wallet_address}
```

### Leaderboard
```bash
GET /leaderboard?window=all
```

Windows: `daily`, `weekly`, `monthly`, `all`

## Token IDs

Each outcome has unique token ID:
- YES token: `{condition_id}_0`
- NO token: `{condition_id}_1`

Find via market details endpoint.

## Rate Limits

- Public endpoints: ~100 req/min
- No auth required for read-only
- WebSocket available for real-time

## WebSocket

```
wss://ws-subscriptions-clob.polymarket.com/ws/market
```

Subscribe to order book updates, trades, price changes.

## Example: Fetch Market Data

```bash
# Get active markets
curl "https://gamma-api.polymarket.com/markets?active=true&closed=false"

# Get specific market
curl "https://gamma-api.polymarket.com/markets/0x..."

# Get order book depth
curl "https://gamma-api.polymarket.com/book/{token_id}"
```
