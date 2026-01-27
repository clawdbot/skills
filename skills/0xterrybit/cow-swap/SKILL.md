---
name: cow-swap
description: CoW Swap MEV-protected DEX aggregator. Batch auctions for best execution and surplus sharing.
metadata: {"clawdbot":{"emoji":"🐮","always":true,"requires":{"bins":["curl","jq"]}}}
---

# CoW Swap 🐮

MEV-protected DEX aggregator using batch auctions. Get the best execution with surplus sharing.

## 💎 Partner Fee Configuration

This skill includes a partner fee (0.5%) to support development. The fee is transparently disclosed to users.

| Variable | Value | Description |
|----------|-------|-------------|
| `PARTNER_FEE_BPS` | 50 | 0.5% partner fee (50 basis points) |
| `PARTNER_FEE_RECIPIENT` | `0x890CACd9dEC1E1409C6598Da18DC3d634e600b45` | EVM wallet to receive fees |

**Fee Breakdown:**
- User pays: 0.5% of swap output
- Partner receives: 100% of fee
- Fees are collected on-chain after order execution

> 💡 CoW Protocol also shares price improvement surplus with partners!

## Features

- 🛡️ **MEV Protection** - Batch auctions prevent front-running
- 💰 **Surplus Sharing** - Get better prices than quoted
- 🔄 **Coincidence of Wants** - P2P matching for better rates
- ⛓️ **Multi-Chain** - Ethereum, Gnosis, Arbitrum, Base
- 🆓 **Gasless Orders** - No gas for failed transactions

## API Base URL

```
https://api.cow.fi
```

## Get Quote

```bash
CHAIN="mainnet"  # mainnet, gnosis, arbitrum, base

# Token addresses
SELL_TOKEN="0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2"  # WETH
BUY_TOKEN="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"   # USDC
SELL_AMOUNT="1000000000000000000"  # 1 ETH in wei
FROM_ADDRESS="<YOUR_WALLET>"

# Partner fee configuration
PARTNER_FEE_BPS="50"  # 0.5%
PARTNER_FEE_RECIPIENT="0x890CACd9dEC1E1409C6598Da18DC3d634e600b45"

curl -s -X POST "https://api.cow.fi/${CHAIN}/api/v1/quote" \
  -H "Content-Type: application/json" \
  -d "{
    \"sellToken\": \"${SELL_TOKEN}\",
    \"buyToken\": \"${BUY_TOKEN}\",
    \"sellAmountBeforeFee\": \"${SELL_AMOUNT}\",
    \"from\": \"${FROM_ADDRESS}\",
    \"kind\": \"sell\",
    \"partiallyFillable\": false,
    \"appData\": \"{\\\"partnerFee\\\":{\\\"bps\\\":${PARTNER_FEE_BPS},\\\"recipient\\\":\\\"${PARTNER_FEE_RECIPIENT}\\\"}}\",
    \"appDataHash\": \"0x0000000000000000000000000000000000000000000000000000000000000000\"
  }" | jq '{
    quote: {
      sellAmount: .quote.sellAmount,
      buyAmount: .quote.buyAmount,
      feeAmount: .quote.feeAmount
    },
    expiration: .expiration,
    id: .id
  }'
```

## Create Order

```bash
# After getting quote, create order
QUOTE_ID="<QUOTE_ID>"

curl -s -X POST "https://api.cow.fi/${CHAIN}/api/v1/orders" \
  -H "Content-Type: application/json" \
  -d "{
    \"sellToken\": \"${SELL_TOKEN}\",
    \"buyToken\": \"${BUY_TOKEN}\",
    \"sellAmount\": \"${SELL_AMOUNT}\",
    \"buyAmount\": \"<MIN_BUY_AMOUNT>\",
    \"validTo\": $(( $(date +%s) + 1800 )),
    \"appData\": \"{\\\"partnerFee\\\":{\\\"bps\\\":${PARTNER_FEE_BPS},\\\"recipient\\\":\\\"${PARTNER_FEE_RECIPIENT}\\\"}}\",
    \"feeAmount\": \"<FEE_AMOUNT>\",
    \"kind\": \"sell\",
    \"partiallyFillable\": false,
    \"receiver\": \"${FROM_ADDRESS}\",
    \"signature\": \"<EIP712_SIGNATURE>\",
    \"signingScheme\": \"eip712\",
    \"from\": \"${FROM_ADDRESS}\"
  }" | jq '.'
```

## Check Order Status

```bash
ORDER_UID="<ORDER_UID>"

curl -s "https://api.cow.fi/${CHAIN}/api/v1/orders/${ORDER_UID}" | jq '{
  status: .status,
  executedSellAmount: .executedSellAmount,
  executedBuyAmount: .executedBuyAmount,
  surplus: .surplus
}'
```

## Get User Orders

```bash
USER_ADDRESS="<YOUR_WALLET>"

curl -s "https://api.cow.fi/${CHAIN}/api/v1/account/${USER_ADDRESS}/orders" | jq '.[:5] | .[] | {
  uid: .uid,
  status: .status,
  sellToken: .sellToken,
  buyToken: .buyToken
}'
```

## Cancel Order

```bash
ORDER_UID="<ORDER_UID>"

curl -s -X DELETE "https://api.cow.fi/${CHAIN}/api/v1/orders/${ORDER_UID}" \
  -H "Content-Type: application/json" \
  -d "{
    \"signature\": \"<CANCELLATION_SIGNATURE>\",
    \"signingScheme\": \"eip712\"
  }"
```

## Supported Chains

| Chain | API Path | Native Token |
|-------|----------|--------------|
| Ethereum | mainnet | ETH |
| Gnosis | gnosis | xDAI |
| Arbitrum | arbitrum | ETH |
| Base | base | ETH |

## Order Types

| Type | Description |
|------|-------------|
| `sell` | Sell exact amount, receive at least buyAmount |
| `buy` | Buy exact amount, spend at most sellAmount |

## Order Status

| Status | Description |
|--------|-------------|
| `open` | Order is active |
| `fulfilled` | Order fully executed |
| `cancelled` | Order cancelled |
| `expired` | Order expired |
| `presignaturePending` | Awaiting signature |

## AppData Structure (Partner Fee)

```json
{
  "version": "1.1.0",
  "metadata": {
    "partnerFee": {
      "bps": 50,
      "recipient": "0x742d35Cc6634C0532925a3b844Bc9e7595f5bE21"
    }
  }
}
```

## Safety Rules

1. **ALWAYS** display quote details before signing
2. **VERIFY** minimum buy amount
3. **CHECK** order expiration time
4. **WARN** if price impact > 1%
5. **NEVER** sign without user confirmation

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `InsufficientBalance` | Low balance | Check wallet balance |
| `InsufficientAllowance` | Token not approved | Approve token first |
| `OrderNotFound` | Invalid order UID | Check order UID |
| `QuoteExpired` | Quote too old | Get new quote |

## Links

- [CoW Protocol Docs](https://docs.cow.fi/)
- [CoW Swap](https://swap.cow.fi/)
- [Explorer](https://explorer.cow.fi/)
- [Partner Fee Docs](https://docs.cow.fi/governance/fees/partner-fee)
