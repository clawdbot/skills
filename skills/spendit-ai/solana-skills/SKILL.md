---
name: solana
description: Solana wallet operations - create wallets, check balances, send SOL/tokens, swap via Jupiter
triggers:
  - solana
  - wallet
  - sol balance
  - send sol
  - send token
  - swap
  - jupiter
metadata:
  clawdbot:
    emoji: "◎"
    requires:
      env:
        - SOLANA_PRIVATE_KEY
        - JUPITER_API_KEY
    primaryEnv: SOLANA_PRIVATE_KEY
---

# Solana Wallet ◎

Solana wallet management and token operations for AI agents.

## Setup

```bash
pip install -r requirements.txt
```

## Initialize Wallet

First, create a new wallet and save the private key to your `.env` file:

```bash
python3 {baseDir}/scripts/initialize.py
```

This will:
- Generate a new Solana keypair
- Display the public key (wallet address)
- Save the private key in base58 format to `.env` as `SOLANA_PRIVATE_KEY`

**IMPORTANT**: After running initialize.py, export the private key to your environment:
```bash
export SOLANA_PRIVATE_KEY=$(grep SOLANA_PRIVATE_KEY .env | cut -d '=' -f2)
```

Or source the .env file:
```bash
source .env
```

## Wallet Operations

### Check SOL Balance
```bash
python3 {baseDir}/scripts/wallet.py balance
python3 {baseDir}/scripts/wallet.py balance <wallet_address>
```

### Check Token Balance
```bash
python3 {baseDir}/scripts/wallet.py token-balance <token_mint_address>
python3 {baseDir}/scripts/wallet.py token-balance <token_mint_address> --owner <wallet_address>
```

### Send SOL
```bash
python3 {baseDir}/scripts/wallet.py send <recipient_address> <amount_in_sol>
```

### Send SPL Token
```bash
python3 {baseDir}/scripts/wallet.py send-token <token_mint_address> <recipient_address> <amount>
```

### Get Wallet Address
```bash
python3 {baseDir}/scripts/wallet.py address
```

## Jupiter Swaps

### Get Swap Quote
```bash
python3 {baseDir}/scripts/jup_swap.py quote <input_token> <output_token> <amount>
python3 {baseDir}/scripts/jup_swap.py quote SOL USDC 1
```

### Execute Swap
```bash
python3 {baseDir}/scripts/jup_swap.py swap <input_token> <output_token> <amount>
python3 {baseDir}/scripts/jup_swap.py swap SOL USDC 0.1
```

### List Known Tokens
```bash
python3 {baseDir}/scripts/jup_swap.py tokens
```

Token symbols: SOL, USDC, USDT, BONK, JUP, RAY, PYTH (or use full mint addresses)

## Network Configuration

By default, wallet operations run on **mainnet**. Use `--network` to switch:

```bash
python3 {baseDir}/scripts/wallet.py balance --network devnet
python3 {baseDir}/scripts/wallet.py balance --network testnet
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `SOLANA_PRIVATE_KEY` | Base58-encoded private key (required) |
| `JUPITER_API_KEY` | Jupiter API key for swaps (required) |
| `SOLANA_RPC_URL` | Custom RPC endpoint (optional) |

## Examples

```bash
# Initialize new wallet
python3 {baseDir}/scripts/initialize.py

# Check your SOL balance
python3 {baseDir}/scripts/wallet.py balance

# Send 0.1 SOL to another wallet
python3 {baseDir}/scripts/wallet.py send 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU 0.1

# Check USDC balance (mainnet USDC mint)
python3 {baseDir}/scripts/wallet.py token-balance EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v

# Send 10 USDC to another wallet
python3 {baseDir}/scripts/wallet.py send-token EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v 7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU 10

# Quote swap: 1 SOL to USDC
python3 {baseDir}/scripts/jup_swap.py quote SOL USDC 1

# Swap 0.5 SOL to USDC
python3 {baseDir}/scripts/jup_swap.py swap SOL USDC 0.5
```

## Common Token Mints (Mainnet)

| Token | Mint Address |
|-------|--------------|
| USDC | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` |
| USDT | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` |
| BONK | `DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263` |

## When to Use

- **Create wallets** for new Solana accounts
- **Check balances** of SOL or any SPL token
- **Send SOL** for payments or transfers
- **Send tokens** for SPL token transfers
- **Swap tokens** via Jupiter aggregator
- **Devnet testing** with `--network devnet`
