# Solana Trader 🚀

A comprehensive Solana wallet management and trading skill for [Clawdbot](https://clawdbot.com).

## Features

- 💰 **Balance Checking** - View SOL and all SPL token balances
- 📜 **Transaction History** - Browse recent transactions
- 🔄 **Token Swaps** - Swap tokens via Jupiter DEX aggregator
- 💸 **Send Tokens** - Transfer SOL and SPL tokens
- 📊 **Price Checking** - Get real-time token prices

## Installation

```bash
clawdhub install solana-trader
```

Or manually copy to your skills directory:
```bash
cp -r solana-trader ~/.clawdbot/skills/
```

## Configuration

Set the following environment variables:

```bash
# Required: Path to your Solana keypair
export SOLANA_KEYPAIR_PATH="~/.config/solana/id.json"

# Optional: Custom RPC endpoint
export SOLANA_RPC_URL="https://api.mainnet-beta.solana.com"

# Optional: Jupiter API key for better rates
export JUPITER_API_KEY="your-api-key"
```

## Requirements

- [Solana CLI](https://docs.solana.com/cli/install-solana-cli-tools) installed
- `curl` and `jq` available in PATH
- A funded Solana wallet

## Usage Examples

### Check Balance
```
"What's my SOL balance?"
"Show me all my tokens"
"How much USDC do I have?"
```

### Swap Tokens
```
"Swap 1 SOL for USDC"
"Trade 100 USDC for JUP"
"Exchange 0.5 SOL to BONK"
```

### Send Tokens
```
"Send 0.1 SOL to ABC123..."
"Transfer 50 USDC to XYZ789..."
```

### Price Check
```
"What's the price of SOL?"
"How much is JUP worth?"
```

## Security

⚠️ **Important Security Notes:**

1. Your private key stays on your local machine
2. All transactions require explicit confirmation
3. Never share your keypair file
4. Always verify transaction details before confirming

## License

MIT

## Author

Built for the Clawdbot community 🦞
