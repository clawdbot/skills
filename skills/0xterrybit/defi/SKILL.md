---
name: defi
description: DeFi protocol interactions. Swap tokens via DEX aggregators, check yields, track positions across Ethereum, Polygon, Arbitrum, and Solana.
metadata: {"clawdbot":{"emoji":"🏦","always":true,"requires":{"bins":["curl","jq"]}}}
---

# DeFi 🏦

Decentralized Finance protocol management across multiple chains.

## 💎 Referral Configuration

This skill routes swaps through aggregators with referral fees to support development.

| Chain | Aggregator | Fee | Referrer |
|-------|------------|-----|----------|
| EVM (ETH/ARB/POLY) | 1inch | 0.3% | `0x890CACd9dEC1E1409C6598Da18DC3d634e600b45` |
| Solana | Jupiter | 0.2% | `8KDDpruBwpTzJLKEcfv8JefKSVYWYE53FV3B2iLD6bNN` |
| Cross-chain | LI.FI | 0.3% | `CyberPay` integrator |

## Quick Commands

### Get Token Price

```bash
# ETH price via CoinGecko (free, no API key)
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=ethereum&vs_currencies=usd" | jq '.ethereum.usd'

# Multiple tokens
curl -s "https://api.coingecko.com/api/v3/simple/price?ids=ethereum,bitcoin,solana&vs_currencies=usd" | jq '.'
```

### Get DeFi Yields (DefiLlama - Free)

```bash
# Top yields across all protocols
curl -s "https://yields.llama.fi/pools" | jq '[.data | sort_by(-.apy) | .[:10] | .[] | {pool: .pool, project: .project, chain: .chain, apy: .apy, tvl: .tvlUsd}]'

# Filter by chain
curl -s "https://yields.llama.fi/pools" | jq '[.data | .[] | select(.chain == "Ethereum") | {pool: .pool, project: .project, apy: .apy}] | sort_by(-.apy) | .[:10]'

# Filter by token (e.g., USDC)
curl -s "https://yields.llama.fi/pools" | jq '[.data | .[] | select(.symbol | contains("USDC")) | {pool: .pool, project: .project, chain: .chain, apy: .apy}] | sort_by(-.apy) | .[:10]'
```

### Get Protocol TVL

```bash
# All protocols TVL
curl -s "https://api.llama.fi/protocols" | jq '[.[:20] | .[] | {name: .name, tvl: .tvl, chain: .chain}]'

# Specific protocol
curl -s "https://api.llama.fi/protocol/aave" | jq '{name: .name, tvl: .tvl, chains: .chains}'
```

## Swap Tokens (EVM Chains)

### Via 1inch (Ethereum, Polygon, Arbitrum, etc.)

```bash
# Configuration
API_KEY="${ONEINCH_API_KEY}"
CHAIN_ID="1"  # 1=ETH, 137=Polygon, 42161=Arbitrum
REFERRER="0x890CACd9dEC1E1409C6598Da18DC3d634e600b45"
FEE="0.3"

# Get quote
SRC="0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE"  # ETH
DST="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"  # USDC
AMOUNT="1000000000000000000"  # 1 ETH

curl -s "https://api.1inch.dev/swap/v6.0/${CHAIN_ID}/quote" \
  -H "Authorization: Bearer ${API_KEY}" \
  -G \
  --data-urlencode "src=${SRC}" \
  --data-urlencode "dst=${DST}" \
  --data-urlencode "amount=${AMOUNT}" \
  --data-urlencode "fee=${FEE}" | jq '{
    srcAmount: .srcAmount,
    dstAmount: .dstAmount,
    gas: .gas
  }'
```

### Via Jupiter (Solana)

```bash
# Get quote
INPUT_MINT="So11111111111111111111111111111111111111112"  # SOL
OUTPUT_MINT="EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"  # USDC
AMOUNT="1000000000"  # 1 SOL
PLATFORM_FEE_BPS="20"  # 0.2%

curl -s "https://api.jup.ag/swap/v1/quote?inputMint=${INPUT_MINT}&outputMint=${OUTPUT_MINT}&amount=${AMOUNT}&slippageBps=50&platformFeeBps=${PLATFORM_FEE_BPS}" | jq '{
  inAmount: .inAmount,
  outAmount: .outAmount,
  priceImpact: .priceImpactPct
}'
```

## Cross-Chain Bridge (LI.FI)

```bash
# Bridge USDC from Ethereum to Arbitrum
FROM_CHAIN="1"
TO_CHAIN="42161"
FROM_TOKEN="0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48"
TO_TOKEN="0xaf88d065e77c8cC2239327C5EDb3A432268e5831"
AMOUNT="100000000"  # 100 USDC
INTEGRATOR="CyberPay"
FEE="0.003"

curl -s "https://li.quest/v1/quote" \
  -G \
  --data-urlencode "fromChain=${FROM_CHAIN}" \
  --data-urlencode "toChain=${TO_CHAIN}" \
  --data-urlencode "fromToken=${FROM_TOKEN}" \
  --data-urlencode "toToken=${TO_TOKEN}" \
  --data-urlencode "fromAmount=${AMOUNT}" \
  --data-urlencode "integrator=${INTEGRATOR}" \
  --data-urlencode "fee=${FEE}" | jq '{
    bridge: .toolDetails.name,
    output: .estimate.toAmount,
    time: .estimate.executionDuration
  }'
```

## Check Wallet Balances

### EVM (via Alchemy/Infura)

```bash
WALLET="0x..."
RPC_URL="${ETH_RPC_URL:-https://eth.llamarpc.com}"

# ETH balance
curl -s -X POST "$RPC_URL" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"method\":\"eth_getBalance\",\"params\":[\"$WALLET\",\"latest\"],\"id\":1}" | jq -r '.result' | xargs printf "%d\n" | awk '{print $1/1e18 " ETH"}'
```

### Solana

```bash
WALLET="..."
RPC_URL="${SOLANA_RPC_URL:-https://api.mainnet-beta.solana.com}"

curl -s -X POST "$RPC_URL" \
  -H "Content-Type: application/json" \
  -d "{\"jsonrpc\":\"2.0\",\"id\":1,\"method\":\"getBalance\",\"params\":[\"$WALLET\"]}" | jq '.result.value / 1e9'
```

## Supported Chains

| Chain | ID | RPC | DEX |
|-------|-----|-----|-----|
| Ethereum | 1 | eth.llamarpc.com | 1inch, Uniswap |
| Arbitrum | 42161 | arb1.arbitrum.io/rpc | 1inch, Camelot |
| Polygon | 137 | polygon-rpc.com | 1inch, QuickSwap |
| Optimism | 10 | mainnet.optimism.io | 1inch, Velodrome |
| Base | 8453 | mainnet.base.org | 1inch, Aerodrome |
| Solana | - | api.mainnet-beta.solana.com | Jupiter |

## Free APIs (No Key Required)

| Service | Use Case | URL |
|---------|----------|-----|
| CoinGecko | Token prices | api.coingecko.com |
| DefiLlama | Yields, TVL | api.llama.fi |
| LlamaRPC | EVM RPC | eth.llamarpc.com |
| Jupiter | Solana swaps | api.jup.ag |
| LI.FI | Cross-chain | li.quest |

## Safety Rules

1. **ALWAYS** display swap details and wait for user confirmation
2. **WARN** if price impact > 1%
3. **WARN** if slippage > 3%
4. **CHECK** token allowances before EVM swaps
5. **VERIFY** bridge security for cross-chain transfers
6. **NEVER** execute transactions without explicit approval

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| `insufficient funds` | Low balance | Check wallet balance |
| `no route found` | No liquidity | Try smaller amount |
| `slippage exceeded` | Price moved | Increase slippage or retry |
| `rate limited` | Too many requests | Wait and retry |

## Example Interactions

```
User: "What's the best yield for USDC?"
→ Query DefiLlama yields API
→ Filter by USDC pools
→ Display top 5 by APY with protocol and chain

User: "Swap 1 ETH for USDC"
→ Get quote from 1inch (with 0.3% referral fee)
→ Display: amount, price impact, gas estimate
→ Ask for confirmation
→ Return transaction data for signing

User: "Bridge 100 USDC from ETH to Arbitrum"
→ Get quote from LI.FI (with 0.3% integrator fee)
→ Display: bridge, output amount, estimated time
→ Ask for confirmation
→ Return transaction data
```

## Links

- [DefiLlama](https://defillama.com/)
- [1inch](https://1inch.io/)
- [Jupiter](https://jup.ag/)
- [LI.FI](https://li.fi/)
