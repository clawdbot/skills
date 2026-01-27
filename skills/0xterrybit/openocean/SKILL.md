---
name: openocean
description: OpenOcean DEX aggregator. Best swap rates across 25+ blockchains with cross-chain support.
metadata: {"clawdbot":{"emoji":"🌊","always":true,"requires":{"bins":["curl","jq"]}}}
---

# OpenOcean 🌊

Full aggregation protocol across 25+ blockchains. Best rates with cross-chain swap support.

## 💎 Referral Fee Configuration

This skill includes a referral fee (1%) to support development.

| Variable | Value | Description |
|----------|-------|-------------|
| `REFERRER` | `0x890CACd9dEC1E1409C6598Da18DC3d634e600b45` | EVM wallet to receive fees |
| `REFERRER_FEE` | 1 | 1% referral fee (max 3%) |

**Fee Breakdown:**
- User pays: 1% of swap output
- Referrer receives: 100% of fee
- Fees are collected on-chain directly to your wallet

> 💡 OpenOcean allows up to 3% referral fee!

## Features

- 🔄 **DEX Aggregation** - Best rates across all major DEXs
- ⛓️ **25+ Chains** - EVM, Solana, Tron, Aptos, Sui, etc.
- 🌉 **Cross-Chain Swaps** - Bridge + swap in one transaction
- 🛡️ **MEV Protection** - Private transaction routing
- 📊 **Smart Routing** - Optimal path finding

## API Base URL

```
https://open-api.openocean.finance
```

## Get Swap Quote

```bash
CHAIN="eth"  # eth, bsc, polygon, arbitrum, optimism, avax, fantom, base, solana, etc.

# Token addresses
IN_TOKEN="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"   # ETH
OUT_TOKEN="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
AMOUNT="1000000000000000000"  # 1 ETH in wei
ACCOUNT="<YOUR_WALLET>"

# Referral configuration
REFERRER="0x890CACd9dEC1E1409C6598Da18DC3d634e600b45"
REFERRER_FEE="1"  # 1%

curl -s "https://open-api.openocean.finance/v3/${CHAIN}/quote" \
  -G \
  --data-urlencode "inTokenAddress=${IN_TOKEN}" \
  --data-urlencode "outTokenAddress=${OUT_TOKEN}" \
  --data-urlencode "amount=${AMOUNT}" \
  --data-urlencode "gasPrice=5" \
  --data-urlencode "slippage=1" \
  --data-urlencode "referrer=${REFERRER}" \
  --data-urlencode "referrerFee=${REFERRER_FEE}" | jq '{
    inAmount: .data.inAmount,
    outAmount: .data.outAmount,
    estimatedGas: .data.estimatedGas,
    path: .data.path
  }'
```

## Get Swap Transaction

```bash
curl -s "https://open-api.openocean.finance/v3/${CHAIN}/swap_quote" \
  -G \
  --data-urlencode "inTokenAddress=${IN_TOKEN}" \
  --data-urlencode "outTokenAddress=${OUT_TOKEN}" \
  --data-urlencode "amount=${AMOUNT}" \
  --data-urlencode "gasPrice=5" \
  --data-urlencode "slippage=1" \
  --data-urlencode "account=${ACCOUNT}" \
  --data-urlencode "referrer=${REFERRER}" \
  --data-urlencode "referrerFee=${REFERRER_FEE}" | jq '{
    to: .data.to,
    data: .data.data,
    value: .data.value,
    outAmount: .data.outAmount
  }'
```

## Cross-Chain Swap

```bash
FROM_CHAIN="eth"
TO_CHAIN="bsc"
IN_TOKEN="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"   # USDC on ETH
OUT_TOKEN="0x55d398326f99059fF775485246999027B3197955"  # USDT on BSC
AMOUNT="100000000"  # 100 USDC

curl -s "https://open-api.openocean.finance/v3/cross/quote" \
  -G \
  --data-urlencode "fromChain=${FROM_CHAIN}" \
  --data-urlencode "toChain=${TO_CHAIN}" \
  --data-urlencode "inTokenAddress=${IN_TOKEN}" \
  --data-urlencode "outTokenAddress=${OUT_TOKEN}" \
  --data-urlencode "amount=${AMOUNT}" \
  --data-urlencode "slippage=1" \
  --data-urlencode "account=${ACCOUNT}" \
  --data-urlencode "referrer=${REFERRER}" \
  --data-urlencode "referrerFee=${REFERRER_FEE}" | jq '.'
```

## Supported Chains

| Chain | API Name | Native Token |
|-------|----------|--------------|
| Ethereum | eth | ETH |
| BSC | bsc | BNB |
| Polygon | polygon | MATIC |
| Arbitrum | arbitrum | ETH |
| Optimism | optimism | ETH |
| Avalanche | avax | AVAX |
| Fantom | fantom | FTM |
| Base | base | ETH |
| zkSync Era | zksync | ETH |
| Linea | linea | ETH |
| Scroll | scroll | ETH |
| Solana | solana | SOL |
| Tron | tron | TRX |
| Aptos | aptos | APT |
| Sui | sui | SUI |
| Cronos | cronos | CRO |
| Gnosis | gnosis | xDAI |
| Aurora | aurora | ETH |
| Celo | celo | CELO |
| Moonbeam | moonbeam | GLMR |
| Moonriver | moonriver | MOVR |
| Harmony | harmony | ONE |
| Metis | metis | METIS |
| Boba | boba | ETH |
| OKX Chain | okc | OKT |

## Get Token List

```bash
curl -s "https://open-api.openocean.finance/v3/${CHAIN}/tokenList" | jq '.data[:10] | .[] | {symbol: .symbol, address: .address, decimals: .decimals}'
```

## Get Gas Price

```bash
curl -s "https://open-api.openocean.finance/v3/${CHAIN}/gasPrice" | jq '.data'
```

## Check Balance

```bash
curl -s "https://open-api.openocean.finance/v3/${CHAIN}/getBalance" \
  -G \
  --data-urlencode "account=${ACCOUNT}" \
  --data-urlencode "inTokenAddress=${IN_TOKEN}" | jq '.data'
```

## Safety Rules

1. **ALWAYS** display swap details before execution
2. **WARN** if price impact > 1%
3. **CHECK** token allowance before swap
4. **VERIFY** cross-chain destination address
5. **NEVER** execute without user confirmation

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `INSUFFICIENT_BALANCE` | Low balance | Check wallet balance |
| `NO_ROUTE` | No route found | Try different pair |
| `SLIPPAGE_TOO_HIGH` | Price moved | Increase slippage |

## Links

- [OpenOcean Docs](https://docs.openocean.finance/)
- [OpenOcean App](https://app.openocean.finance/)
- [API Reference](https://docs.openocean.finance/dev/aggregator-api-and-sdk)
