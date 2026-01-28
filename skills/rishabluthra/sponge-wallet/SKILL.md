---
name: sponge-wallet
description: Manages crypto wallets, transfers tokens, swaps on DEXes, checks balances, and accesses paid APIs (search, image gen, prediction markets, web scraping, document parsing, sales prospecting) via x402 micropayments. Use when the user asks about wallet balances, token transfers, swaps, blockchain payments, or paid API services.
---

# Sponge Wallet Skill

Multi-chain crypto wallet with transfers, swaps, and paid API access.

## Authentication

**IMPORTANT**: If any tool returns `"Not authenticated"` or `"Invalid API key"`, run the login flow.

Login is two-phase (because Claude Code runs commands non-interactively):

**Phase 1** — Start the device flow (returns a URL and code as JSON):
```bash
node <skill-path>/scripts/wallet.mjs login
```
Show the `verification_url` and `user_code` to the user. Tell them to open the URL in their browser and enter the code.

**Phase 2** — After the user confirms they have approved, poll for the token:
```bash
node <skill-path>/scripts/wallet.mjs login --poll <device_code> <interval> <expires_in>
```
Use the `device_code`, `interval`, and `expires_in` values from Phase 1 output.

Credentials are saved to `~/.spongewallet/credentials.json` automatically.

Credential resolution order:
1. `SPONGE_API_KEY` environment variable (if set, skips stored credentials)
2. `~/.spongewallet/credentials.json` (saved by login)

Other auth commands:
- `node wallet.mjs whoami` — show current auth status
- `node wallet.mjs logout` — remove stored credentials

## How to Execute

```bash
node <skill-path>/scripts/wallet.mjs <tool_name> '<json_args>'
```

Output is JSON with `status: "success"` or `status: "error"`.

## Available Tools

### Wallet & Balance

| Tool | Description | Required | Optional |
|------|-------------|----------|----------|
| `get_balance` | Check balances across chains | — | `chain` |
| `get_solana_tokens` | Discover all SPL tokens in wallet | `chain` | — |
| `search_solana_tokens` | Search Jupiter token database | `query` | `limit` |

### Transfers

| Tool | Description | Required | Optional |
|------|-------------|----------|----------|
| `evm_transfer` | Transfer ETH/USDC on Ethereum/Base | `chain`, `to`, `amount`, `currency` | — |
| `solana_transfer` | Transfer SOL/USDC on Solana | `chain`, `to`, `amount`, `currency` | — |

### Swaps

| Tool | Description | Required | Optional |
|------|-------------|----------|----------|
| `solana_swap` | Swap tokens via Jupiter | `chain`, `input_token`, `output_token`, `amount` | `slippage_bps` |

### Transactions

| Tool | Description | Required | Optional |
|------|-------------|----------|----------|
| `get_transaction_status` | Check tx status | `transaction_hash`, `chain` | — |
| `get_transaction_history` | View past transactions | — | `limit`, `chain` |

### Funding & Withdrawals

| Tool | Description | Required | Optional |
|------|-------------|----------|----------|
| `request_funding` | Request funds from owner | `amount`, `chain`, `currency` | — |
| `withdraw_to_main_wallet` | Return funds to owner | `chain`, `amount` | `currency` |

### Paid APIs (Sponge x402)

| Tool | Description | Required | Optional |
|------|-------------|----------|----------|
| `sponge` | Unified paid API interface | `task` | See [REFERENCE.md](REFERENCE.md) |
| `create_x402_payment` | Create x402 payment payload | `chain`, `to`, `amount` | `token`, `decimals` |

## Chain Reference

**Test keys** (`sponge_test_*`): `sepolia`, `base-sepolia`, `solana-devnet`, `tempo`
**Live keys** (`sponge_live_*`): `ethereum`, `base`, `solana`

## Common Workflows

### Check Balance → Transfer → Verify

```bash
node wallet.mjs get_balance '{"chain":"base"}'
node wallet.mjs evm_transfer '{"chain":"base","to":"0x...","amount":"10","currency":"USDC"}'
node wallet.mjs get_transaction_status '{"transaction_hash":"0x...","chain":"base"}'
```

### Swap Tokens on Solana

```bash
node wallet.mjs search_solana_tokens '{"query":"BONK"}'
node wallet.mjs solana_swap '{"chain":"solana","input_token":"SOL","output_token":"BONK","amount":"0.5"}'
```

### Sponge Paid APIs

```bash
node wallet.mjs sponge '{"task":"search","query":"AI research papers"}'
node wallet.mjs sponge '{"task":"image","prompt":"sunset over mountains"}'
node wallet.mjs sponge '{"task":"predict","semantic_search":"will-trump-win-2028"}'
node wallet.mjs sponge '{"task":"crawl","url":"https://example.com"}'
node wallet.mjs sponge '{"task":"parse","document_url":"https://example.com/doc.pdf"}'
node wallet.mjs sponge '{"task":"prospect","apollo_query":"Stripe","apollo_endpoint":"companies"}'
```

## Error Handling

| Error | Resolution |
|-------|------------|
| `Not authenticated` | Run `node wallet.mjs login` |
| `Invalid API key` | Run `node wallet.mjs login` to re-authenticate |
| `Chain 'X' is not allowed` | Use correct key type (test vs live) for the chain |
| `Insufficient balance` | Use `request_funding` |
| `Address not in allowlist` | Add recipient in the dashboard |

See [REFERENCE.md](REFERENCE.md) for detailed parameter docs.
