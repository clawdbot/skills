# Sponge Wallet — Tool Parameter Reference

Detailed parameter documentation for every tool exposed by the Sponge Wallet skill.

---

## get_balance

Check wallet balances for native tokens and USDC across supported chains.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | string | No | Specific chain to check. If omitted, returns all chains. Values: `ethereum`, `base`, `sepolia`, `base-sepolia`, `tempo`, `solana`, `solana-devnet`, `all` |

```bash
node wallet.mjs get_balance '{}'
node wallet.mjs get_balance '{"chain":"base"}'
```

---

## evm_transfer

Transfer ETH or USDC on Ethereum or Base networks. USDC transfers use gas sponsorship automatically (sender doesn't need ETH for gas).

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | string | Yes | `ethereum`, `base`, `sepolia`, or `base-sepolia` |
| `to` | string | Yes | Recipient address (0x-prefixed). Must be in your allowlist. |
| `amount` | string | Yes | Amount to send (e.g., `"0.1"` for ETH, `"100"` for USDC) |
| `currency` | string | Yes | `ETH` or `USDC` |

```bash
node wallet.mjs evm_transfer '{"chain":"base","to":"0x742d35Cc6634C0532925a3b844Bc9e7595f2bD18","amount":"10","currency":"USDC"}'
```

---

## solana_transfer

Transfer SOL or USDC on Solana.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | string | Yes | `solana` or `solana-devnet` |
| `to` | string | Yes | Recipient address (base58 public key). Must be in your allowlist. |
| `amount` | string | Yes | Amount to send (e.g., `"0.5"` for SOL, `"100"` for USDC) |
| `currency` | string | Yes | `SOL` or `USDC` |

```bash
node wallet.mjs solana_transfer '{"chain":"solana","to":"5xG1...","amount":"1","currency":"SOL"}'
```

---

## solana_swap

Swap tokens on Solana using Jupiter aggregator. Finds the best route across all Solana DEXes.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | string | Yes | `solana` or `solana-devnet` |
| `input_token` | string | Yes | Token to swap from — symbol (`SOL`, `USDC`) or mint address |
| `output_token` | string | Yes | Token to swap to — symbol or mint address |
| `amount` | string | Yes | Amount of input token to swap (e.g., `"1.5"`) |
| `slippage_bps` | number | No | Slippage tolerance in basis points (default: 50 = 0.5%, max: 1000 = 10%) |

```bash
node wallet.mjs solana_swap '{"chain":"solana","input_token":"SOL","output_token":"USDC","amount":"1"}'
node wallet.mjs solana_swap '{"chain":"solana","input_token":"SOL","output_token":"BONK","amount":"0.5","slippage_bps":100}'
```

---

## get_solana_tokens

Discover all SPL tokens in your Solana wallet with metadata from Jupiter.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | string | Yes | `solana` or `solana-devnet` |

```bash
node wallet.mjs get_solana_tokens '{"chain":"solana"}'
```

---

## search_solana_tokens

Search Jupiter's token database by symbol or name.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `query` | string | Yes | Token symbol, name, or partial match (e.g., `"BONK"`, `"dogwifhat"`) |
| `limit` | number | No | Max results (default: 10, max: 20) |

```bash
node wallet.mjs search_solana_tokens '{"query":"BONK"}'
node wallet.mjs search_solana_tokens '{"query":"pepe","limit":5}'
```

---

## get_transaction_status

Check the status of a transaction.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `transaction_hash` | string | Yes | Transaction hash (EVM) or signature (Solana) |
| `chain` | string | Yes | Chain the transaction is on |

```bash
node wallet.mjs get_transaction_status '{"transaction_hash":"0xabc123...","chain":"base"}'
```

---

## get_transaction_history

View past transactions for this agent's wallets.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `limit` | number | No | Number of transactions to return (default: 50) |
| `chain` | string | No | Filter by chain. If omitted, returns all chains. |

```bash
node wallet.mjs get_transaction_history '{}'
node wallet.mjs get_transaction_history '{"limit":10,"chain":"base"}'
```

---

## request_funding

Request additional funds from the agent's owner. Creates a pending approval request — funds are NOT transferred immediately.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `amount` | string | Yes | Amount to request (e.g., `"50.00"`) |
| `chain` | string | Yes | Chain to receive funds on |
| `currency` | string | Yes | Currency to request. Valid options depend on chain — EVM: `ETH`, `USDC`; Solana: `SOL`, `USDC`; Tempo: `pathUSD` |

```bash
node wallet.mjs request_funding '{"amount":"50","chain":"base","currency":"USDC"}'
```

---

## withdraw_to_main_wallet

Return funds from the agent wallet to the owner's main wallet. Does not require allowlist approval.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | string | Yes | Chain to withdraw on |
| `amount` | string | Yes | Amount to withdraw (e.g., `"0.1"`) |
| `currency` | string | No | `native` (default) for chain's native token, or `USDC` |

```bash
node wallet.mjs withdraw_to_main_wallet '{"chain":"base","amount":"0.05","currency":"native"}'
node wallet.mjs withdraw_to_main_wallet '{"chain":"base","amount":"100","currency":"USDC"}'
```

---

## sponge

Unified interface for paid API services via x402 micropayments (~$0.01 USDC per request). Payment is handled automatically.

### Common Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `task` | string | Yes | `search`, `image`, `predict`, `crawl`, `llm`, `parse`, or `prospect` |
| `query` | string | Depends | Search query or LLM prompt (for `search`, `llm`) |
| `prompt` | string | Depends | Image generation or LLM prompt (for `image`, `llm`) |
| `url` | string | Depends | URL to crawl (for `crawl`) |
| `model` | string | No | LLM model name (for `llm`, default: `openai/gpt-4o-mini`) |
| `num_results` | number | No | Number of search results (for `search`, default: 10) |
| `provider` | string | No | Override provider: `exa`, `dome`, `firecrawl`, `openrouter`, `gemini`, `reducto`, `apollo` |
| `auto_pay` | boolean | No | Auto-pay for services (default: true). Set false to see payment requirements first. |
| `payment_signature` | string | No | Base64 payment signature (only if `auto_pay` is false) |

### Prediction Market Parameters (task=predict)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `semantic_search` | string | No | Polymarket semantic search slug (e.g., `"will-trump-win-2028"`) |
| `dome_path` | string | No | Dome API path (default: `/v1/polymarket/markets`) |

### Document Parsing Parameters (task=parse)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `document_url` | string | Yes | URL of document to parse (PDF, image, spreadsheet) |

### Sales Prospecting Parameters (task=prospect)

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `apollo_endpoint` | string | No | `companies` (default), `people`, `enrich`, or `bulk_enrich` |
| `apollo_query` | string | No | Company name or domain to search (use for specific company lookups, NOT industry searches) |
| `apollo_filters` | object | No | Search filters — e.g., `{"q_organization_keyword_tags":["AI","fintech"],"organization_num_employees_ranges":["1,500"]}` |
| `apollo_person_titles` | string[] | No | Filter people by titles (e.g., `["CEO","CTO"]`) |
| `apollo_per_page` | number | No | Results per page (max: 20, default: 20) |
| `apollo_email` | string | No | Email for enrichment |
| `apollo_linkedin_url` | string | No | LinkedIn URL for enrichment |
| `apollo_person_id` | string | No | Apollo person ID for enrichment |
| `apollo_first_name` | string | No | First name for enrichment |
| `apollo_last_name` | string | No | Last name for enrichment |
| `apollo_organization_name` | string | No | Org name for enrichment |
| `apollo_domain` | string | No | Company domain for enrichment |
| `apollo_reveal_personal_emails` | boolean | No | Include personal emails (default: true) |
| `apollo_details` | object[] | No | Array of person details for bulk enrichment (max 10) |

### Examples

```bash
# Web search
node wallet.mjs sponge '{"task":"search","query":"latest AI research"}'

# Image generation
node wallet.mjs sponge '{"task":"image","prompt":"sunset over mountains"}'

# Prediction markets
node wallet.mjs sponge '{"task":"predict","semantic_search":"will-trump-win-2028","dome_path":"/v1/polymarket/markets"}'

# Web scraping
node wallet.mjs sponge '{"task":"crawl","url":"https://example.com"}'

# LLM completion
node wallet.mjs sponge '{"task":"llm","query":"Summarize quantum computing","model":"openai/gpt-4o"}'

# Document parsing
node wallet.mjs sponge '{"task":"parse","document_url":"https://example.com/report.pdf"}'

# Prospect: search companies by industry
node wallet.mjs sponge '{"task":"prospect","apollo_endpoint":"companies","apollo_filters":{"q_organization_keyword_tags":["artificial intelligence"],"organization_num_employees_ranges":["1,500"]},"apollo_per_page":5}'

# Prospect: enrich a contact
node wallet.mjs sponge '{"task":"prospect","apollo_endpoint":"enrich","apollo_email":"john@company.com"}'
```

---

## create_x402_payment

Create a signed x402 payment payload for paying external APIs. This is a low-level tool — prefer using `sponge` which handles payment automatically.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `chain` | string | Yes | Chain for payment. Map from 402 response `network` field: `eip155:8453` -> `base`, `eip155:84532` -> `base-sepolia`, etc. |
| `to` | string | Yes | Recipient address from 402 response `payTo` field |
| `amount` | string | Yes | Human-readable amount (e.g., `"0.01"` for 0.01 USDC). Convert from `maxAmountRequired` by dividing by 10^decimals. |
| `token` | string | No | Token contract address from 402 response `asset` field. Defaults to USDC. |
| `decimals` | number | No | Token decimals (default: 6 for USDC) |
| `valid_for_seconds` | number | No | Payment validity in seconds (default: 3600) |
| `resource_url` | string | No | URL of the resource being purchased |
| `resource_description` | string | No | Description of the resource |

```bash
node wallet.mjs create_x402_payment '{"chain":"base-sepolia","to":"0xf0DfD006e3D0d4F966F1b649359EDB89ba675777","amount":"0.01","token":"0x036CbD53842c5426634e7929541eC2318f3dCF7e"}'
```

---

## Testnet-Only Tools

These tools are only available with test API keys (`sponge_test_*`):

### tempo_transfer

Send pathUSD on the Tempo testnet.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `to` | string | Yes | Recipient address |
| `amount` | string | Yes | Amount of pathUSD to send |
| `use_gas_sponsorship` | boolean | No | Let the platform cover gas fees (recommended) |

### request_tempo_faucet

Get free Tempo testnet tokens. No parameters required.

```bash
node wallet.mjs request_tempo_faucet '{}'
```
