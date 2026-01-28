# Hyperliquid API Reference

## Base URLs

- **Mainnet:** `https://api.hyperliquid.xyz`
- **Testnet:** `https://api.hyperliquid-testnet.xyz`

## Authentication

Trading operations require signing with your Ethereum private key:

1. Create action object (e.g., order, cancel)
2. Add timestamp
3. Sign message with ethers.js `wallet.signMessage()`
4. Send signed action to `/exchange` endpoint

Read-only operations require no authentication.

## Information Endpoints

All use POST to `/info` with JSON body specifying `type`.

### Clearinghouse State

Get account balance, positions, and margin info:

```json
{
  "type": "clearinghouseState",
  "user": "0x..."
}
```

**Response:**
```json
{
  "assetPositions": [
    {
      "position": {
        "coin": "BTC",
        "szi": "0.5",           // Position size
        "entryPx": "45000.0",   // Entry price
        "positionValue": "22500.0",
        "unrealizedPnl": "500.0"
      },
      "type": "oneWay"
    }
  ],
  "crossMarginSummary": {
    "accountValue": "50000.0",
    "totalMarginUsed": "5000.0"
  }
}
```

### Open Orders

```json
{
  "type": "openOrders",
  "user": "0x..."
}
```

### User Fills (Trade History)

```json
{
  "type": "userFills",
  "user": "0x..."
}
```

### Market Data

**All mid prices:**
```json
{ "type": "allMids" }
```

Returns: `{ "BTC": "45123.5", "ETH": "3021.2", ... }`

**Meta (available coins):**
```json
{ "type": "meta" }
```

Returns universe of tradeable assets with specs.

## Trading Endpoints

All use POST to `/exchange` with signed action.

### Place Order

```json
{
  "type": "order",
  "orders": [{
    "a": 0,              // Asset index (from meta)
    "b": true,           // true = buy, false = sell
    "p": "45000.0",      // Limit price
    "s": "0.5",          // Size
    "r": false,          // Reduce-only
    "t": {
      "limit": { "tif": "Gtc" }  // Time-in-force
    }
  }],
  "grouping": "na",
  "signature": "0x...",
  "timestamp": 1234567890
}
```

### Cancel Order

```json
{
  "type": "cancel",
  "cancels": [{
    "a": 0,              // Asset index
    "o": 12345           // Order ID
  }],
  "signature": "0x...",
  "timestamp": 1234567890
}
```

### Cancel All Orders

```json
{
  "type": "cancel",
  "cancels": [],
  "signature": "0x...",
  "timestamp": 1234567890
}
```

## Order Types

- **Limit:** Standard limit order with price
- **Market:** Achieved via limit order with aggressive price and slippage buffer
- **Post-only:** `"t": { "limit": { "tif": "Alo" } }` (add liquidity only)

## Asset Indexing

Assets referenced by index (0, 1, 2...). Get mapping from `meta` endpoint:
- BTC is typically index 0
- ETH is typically index 1
- Query meta to get current mapping

## Position Size Convention

- Positive size = long position
- Negative size = short position
- Size in base currency (e.g., BTC, ETH)

## Error Responses

HTTP 200 with error object:
```json
{
  "status": "err",
  "response": {
    "type": "error",
    "message": "Insufficient margin"
  }
}
```

Common errors:
- Insufficient margin
- Invalid signature
- Unknown coin
- Order size too small/large
- Price precision error

## Rate Limits

Hyperliquid has rate limits. Space out requests, especially in loops.

## Documentation

Official docs: https://hyperliquid.gitbook.io/hyperliquid-docs/
