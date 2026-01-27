---
name: transak
description: Transak fiat-to-crypto on-ramp for Web3. Buy and sell crypto with 100+ payment methods across 170+ countries.
metadata: {"clawdbot":{"emoji":"🚀","always":true,"requires":{"bins":["curl","jq"]}}}
---

# Transak 🚀

Web3 payment infrastructure. Fiat on/off-ramp trusted by 600+ DeFi, NFT, and wallet projects.

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `TRANSAK_API_KEY` | API Key | Yes |
| `TRANSAK_SECRET` | Secret for webhooks | No |
| `TRANSAK_ENV` | `STAGING` or `PRODUCTION` | No |

## Features

- 🌍 **170+ Countries** - Global coverage
- 💳 **100+ Payment Methods** - Cards, bank, mobile
- ⛓️ **75+ Blockchains** - EVM, Solana, Bitcoin, etc.
- 🔄 **Off-Ramp** - Sell crypto to fiat
- 🎨 **NFT Checkout** - Direct NFT purchases
- 🔌 **Widget SDK** - Easy integration

## API Base URLs

- Staging: `https://api-stg.transak.com`
- Production: `https://api.transak.com`

## Get Supported Cryptocurrencies

```bash
API_KEY="${TRANSAK_API_KEY}"
ENV="${TRANSAK_ENV:-STAGING}"
[[ "$ENV" == "PRODUCTION" ]] && BASE_URL="https://api.transak.com" || BASE_URL="https://api-stg.transak.com"

curl -s "${BASE_URL}/api/v2/currencies/crypto-currencies" | jq '.response[:10] | .[] | {symbol: .symbol, name: .name, network: .network.name}'
```

## Get Supported Fiat Currencies

```bash
curl -s "${BASE_URL}/api/v2/currencies/fiat-currencies" | jq '.response[:10] | .[] | {symbol: .symbol, name: .name, paymentOptions: .paymentOptions}'
```

## Get Price Quote

```bash
FIAT="USD"
CRYPTO="ETH"
FIAT_AMOUNT="100"
NETWORK="ethereum"
PAYMENT_METHOD="credit_debit_card"

curl -s "${BASE_URL}/api/v2/currencies/price" \
  -G \
  --data-urlencode "fiatCurrency=${FIAT}" \
  --data-urlencode "cryptoCurrency=${CRYPTO}" \
  --data-urlencode "fiatAmount=${FIAT_AMOUNT}" \
  --data-urlencode "network=${NETWORK}" \
  --data-urlencode "paymentMethod=${PAYMENT_METHOD}" \
  --data-urlencode "isBuyOrSell=BUY" | jq '{
    cryptoAmount: .response.cryptoAmount,
    fiatAmount: .response.fiatAmount,
    totalFee: .response.totalFee,
    conversionPrice: .response.conversionPrice
  }'
```

## Generate Widget URL

```bash
API_KEY="${TRANSAK_API_KEY}"
WALLET_ADDRESS="<USER_WALLET>"
CRYPTO="ETH"
NETWORK="ethereum"
FIAT_AMOUNT="100"
FIAT_CURRENCY="USD"

# Build widget URL
WIDGET_URL="https://global.transak.com/?apiKey=${API_KEY}"
WIDGET_URL+="&walletAddress=${WALLET_ADDRESS}"
WIDGET_URL+="&cryptoCurrencyCode=${CRYPTO}"
WIDGET_URL+="&network=${NETWORK}"
WIDGET_URL+="&fiatAmount=${FIAT_AMOUNT}"
WIDGET_URL+="&fiatCurrency=${FIAT_CURRENCY}"
WIDGET_URL+="&productsAvailed=BUY"

echo "Widget URL: $WIDGET_URL"
```

## Get Order Status

```bash
ORDER_ID="<ORDER_ID>"

curl -s "${BASE_URL}/api/v2/partners/order/${ORDER_ID}" \
  -H "api-key: ${API_KEY}" | jq '{
    status: .response.status,
    cryptoAmount: .response.cryptoAmount,
    transactionHash: .response.transactionHash,
    walletAddress: .response.walletAddress
  }'
```

## Supported Networks

| Network | ID | Tokens |
|---------|-----|--------|
| Ethereum | ethereum | ETH, USDT, USDC, DAI |
| Polygon | polygon | MATIC, USDT, USDC |
| Arbitrum | arbitrum | ETH, ARB, USDC |
| Optimism | optimism | ETH, OP, USDC |
| BSC | bsc | BNB, BUSD, USDT |
| Solana | solana | SOL, USDC |
| Avalanche | avaxcchain | AVAX, USDC |
| Base | base | ETH, USDC |
| Bitcoin | bitcoin | BTC |

## Payment Methods

| Method | Regions | Speed |
|--------|---------|-------|
| Credit/Debit Card | Global | Instant |
| Apple Pay | Global | Instant |
| Google Pay | Global | Instant |
| Bank Transfer | Global | 1-3 days |
| SEPA | Europe | 1-2 days |
| PIX | Brazil | Instant |
| UPI | India | Instant |
| GCash | Philippines | Instant |
| GrabPay | SEA | Instant |

## Order Status Codes

| Status | Description |
|--------|-------------|
| `AWAITING_PAYMENT_FROM_USER` | Waiting for payment |
| `PAYMENT_DONE_MARKED_BY_USER` | Payment submitted |
| `PROCESSING` | Processing order |
| `PENDING_DELIVERY_FROM_TRANSAK` | Sending crypto |
| `COMPLETED` | Order completed |
| `CANCELLED` | Order cancelled |
| `FAILED` | Order failed |
| `REFUNDED` | Payment refunded |
| `EXPIRED` | Order expired |

## Webhook Events

```bash
# Webhook payload
{
  "eventID": "ORDER_COMPLETED",
  "webhookData": {
    "id": "order-123",
    "status": "COMPLETED",
    "cryptoAmount": 0.05,
    "cryptoCurrency": "ETH",
    "transactionHash": "0x...",
    "walletAddress": "0x..."
  }
}
```

## Verify Webhook

```bash
verify_webhook() {
  local payload="$1"
  local signature="$2"
  
  local expected=$(echo -n "$payload" | openssl dgst -sha256 -hmac "$TRANSAK_SECRET" | cut -d' ' -f2)
  
  [[ "$signature" == "$expected" ]]
}
```

## Widget Customization

```bash
# Additional widget parameters
WIDGET_URL+="&themeColor=0066FF"           # Custom color
WIDGET_URL+="&hideMenu=true"               # Hide menu
WIDGET_URL+="&disableWalletAddressForm=true"  # Lock wallet
WIDGET_URL+="&exchangeScreenTitle=Buy%20Crypto"  # Custom title
WIDGET_URL+="&defaultPaymentMethod=credit_debit_card"
```

## Safety Rules

1. **VERIFY** webhook signatures
2. **NEVER** expose API keys client-side
3. **CHECK** order status before fulfilling
4. **VALIDATE** wallet addresses

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `INVALID_API_KEY` | Bad API key | Check credentials |
| `UNSUPPORTED_CRYPTO` | Currency unavailable | Check supported list |
| `AMOUNT_TOO_LOW` | Below minimum | Increase amount |
| `AMOUNT_TOO_HIGH` | Above maximum | Decrease amount |

## Links

- [Transak Docs](https://docs.transak.com/)
- [Dashboard](https://dashboard.transak.com/)
- [Widget Demo](https://global.transak.com/)
