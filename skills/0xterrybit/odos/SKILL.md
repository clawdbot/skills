---
name: odos
description: Odos smart order routing DEX aggregator. Best swap rates with patented SOR algorithm across 500+ liquidity sources.
metadata: {"clawdbot":{"emoji":"🔮","always":true,"requires":{"bins":["curl","jq"]}}}
---

# Odos 🔮

Smart Order Routing DEX aggregator. Patented algorithm for best execution across 500+ liquidity sources.

## 💎 Referral Fee Configuration

This skill includes a referral fee (1%) to support development.

| Variable | Value | Description |
|----------|-------|-------------|
| `REFERRAL_CODE` | `0` | Referral code (0 = default) |
| `FEE_RECIPIENT` | `0x890CACd9dEC1E1409C6598Da18DC3d634e600b45` | EVM wallet to receive fees |
| `COMPACT` | true | Use compact calldata for gas savings |

**Fee Breakdown:**
- User pays: ~1% of swap output (configurable)
- Referrer receives: 100% of fee
- Fees are collected on-chain directly to your wallet

## Features

- 🔄 **500+ Liquidity Sources** - Uniswap, SushiSwap, Curve, Balancer, etc.
- ⛓️ **Multi-Chain** - Ethereum, Arbitrum, Optimism, Polygon, Base, Avalanche
- 🧠 **Smart Order Routing** - Patented SOR algorithm
- 📊 **Multi-Input Swaps** - Swap multiple tokens at once
- 💰 **Referral Program** - Earn on every swap
- ⚡ **Gas Optimized** - Compact calldata for lower gas

## API Base URL

```
https://api.odos.xyz
```

## Get Swap Quote

```bash
CHAIN_ID="1"  # Ethereum

# Token addresses
INPUT_TOKEN="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"   # ETH
OUTPUT_TOKEN="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
INPUT_AMOUNT="1000000000000000000"  # 1 ETH in wei
USER_ADDRESS="<YOUR_WALLET>"

# Referral configuration
REFERRAL_CODE="0"

curl -s -X POST "https://api.odos.xyz/sor/quote/v2" \
  -H "Content-Type: application/json" \
  -d "{
    \"chainId\": ${CHAIN_ID},
    \"inputTokens\": [{
      \"tokenAddress\": \"${INPUT_TOKEN}\",
      \"amount\": \"${INPUT_AMOUNT}\"
    }],
    \"outputTokens\": [{
      \"tokenAddress\": \"${OUTPUT_TOKEN}\",
      \"proportion\": 1
    }],
    \"userAddr\": \"${USER_ADDRESS}\",
    \"slippageLimitPercent\": 1,
    \"referralCode\": ${REFERRAL_CODE},
    \"compact\": true
  }" | jq '{
    inAmounts: .inAmounts,
    outAmounts: .outAmounts,
    gasEstimate: .gasEstimate,
    pathId: .pathId
  }'
```

## Assemble Transaction

```bash
PATH_ID="<PATH_ID_FROM_QUOTE>"

curl -s -X POST "https://api.odos.xyz/sor/assemble" \
  -H "Content-Type: application/json" \
  -d "{
    \"userAddr\": \"${USER_ADDRESS}\",
    \"pathId\": \"${PATH_ID}\",
    \"simulate\": false
  }" | jq '{
    to: .transaction.to,
    data: .transaction.data,
    value: .transaction.value,
    gasLimit: .transaction.gas
  }'
```

## Multi-Input Swap (Swap Multiple Tokens)

```bash
# Swap ETH + USDC to DAI
curl -s -X POST "https://api.odos.xyz/sor/quote/v2" \
  -H "Content-Type: application/json" \
  -d "{
    \"chainId\": ${CHAIN_ID},
    \"inputTokens\": [
      {
        \"tokenAddress\": \"0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE\",
        \"amount\": \"500000000000000000\"
      },
      {
        \"tokenAddress\": \"0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48\",
        \"amount\": \"500000000\"
      }
    ],
    \"outputTokens\": [{
      \"tokenAddress\": \"0x6B175474E89094C44Da98b954EesdeAC495271d0F\",
      \"proportion\": 1
    }],
    \"userAddr\": \"${USER_ADDRESS}\",
    \"slippageLimitPercent\": 1,
    \"referralCode\": ${REFERRAL_CODE},
    \"compact\": true
  }" | jq '.'
```

## Multi-Output Swap (Split to Multiple Tokens)

```bash
# Swap ETH to 50% USDC + 50% DAI
curl -s -X POST "https://api.odos.xyz/sor/quote/v2" \
  -H "Content-Type: application/json" \
  -d "{
    \"chainId\": ${CHAIN_ID},
    \"inputTokens\": [{
      \"tokenAddress\": \"0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE\",
      \"amount\": \"${INPUT_AMOUNT}\"
    }],
    \"outputTokens\": [
      {
        \"tokenAddress\": \"0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48\",
        \"proportion\": 0.5
      },
      {
        \"tokenAddress\": \"0x6B175474E89094C44Da98b954EedeAC495271d0F\",
        \"proportion\": 0.5
      }
    ],
    \"userAddr\": \"${USER_ADDRESS}\",
    \"slippageLimitPercent\": 1,
    \"referralCode\": ${REFERRAL_CODE},
    \"compact\": true
  }" | jq '.'
```

## Supported Chains

| Chain | ID | Native Token |
|-------|-----|--------------|
| Ethereum | 1 | ETH |
| Arbitrum | 42161 | ETH |
| Optimism | 10 | ETH |
| Polygon | 137 | MATIC |
| Base | 8453 | ETH |
| Avalanche | 43114 | AVAX |
| BSC | 56 | BNB |
| Fantom | 250 | FTM |
| zkSync Era | 324 | ETH |
| Linea | 59144 | ETH |
| Mantle | 5000 | MNT |
| Mode | 34443 | ETH |

## Get Token List

```bash
curl -s "https://api.odos.xyz/info/tokens/${CHAIN_ID}" | jq '.tokenMap | to_entries[:10] | .[] | {symbol: .value.symbol, address: .key, decimals: .value.decimals}'
```

## Get Liquidity Sources

```bash
curl -s "https://api.odos.xyz/info/liquidity-sources/${CHAIN_ID}" | jq '.[] | {id: .id, name: .name}'
```

## Check Contract Info

```bash
curl -s "https://api.odos.xyz/info/contract-info/v2/${CHAIN_ID}" | jq '{
  routerAddress: .routerAddress,
  executorAddress: .executorAddress
}'
```

## Safety Rules

1. **ALWAYS** display swap details before execution
2. **WARN** if price impact > 1%
3. **CHECK** token allowance before swap
4. **VERIFY** output amounts
5. **NEVER** execute without user confirmation

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `NO_PATH_FOUND` | No route available | Try different pair |
| `INSUFFICIENT_LIQUIDITY` | Low liquidity | Reduce amount |
| `SLIPPAGE_EXCEEDED` | Price moved | Increase slippage |

## Links

- [Odos Docs](https://docs.odos.xyz/)
- [Odos App](https://app.odos.xyz/)
- [API Reference](https://docs.odos.xyz/api/endpoints)
