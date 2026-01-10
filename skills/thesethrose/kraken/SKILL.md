---
name: kraken
description: Query Kraken crypto account balances, portfolio, trades, and staking positions.
metadata: {"clawdbot":{"emoji":"🐍","requires":{"bins":["python3"]},"env":{"KRAKEN_API_KEY":"Kraken API key","KRAKEN_API_SECRET":"Kraken API secret"}}}
---

# Kraken Crypto Skill

Query your Kraken account using the `kraken_cli.py` tool.

## Setup

Export your Kraken API credentials:
```bash
export KRAKEN_API_KEY="your_api_key"
export KRAKEN_API_SECRET="your_api_secret"
```

## Commands

### Account Balances
- `balance` - Get all account balances
- `portfolio` - Get trade balance summary (equity, PnL, cost basis)

### History
- `ledger` - Get ledger entries (transaction history)
- `ledger --asset BTC` - Filter ledger by specific asset
- `trades` - Get trade history
- `trades --pair BTC/USD` - Filter trades by trading pair

### Staking
- `earn` - Show stakeable assets and APY rates
- `earn positions` - Show current staking positions

### Deposits
- `deposits methods` - Show available deposit methods
- `deposits address BTC` - Get deposit address for an asset

---

## Example Usage

```
You: What's my Kraken balance?
Bot: Runs kraken_cli.py balance → Shows all crypto balances

You: Show my trades
Bot: Runs kraken_cli.py trades → Shows recent trade history

You: What are my staking positions?
Bot: Runs kraken_cli.py earn positions → Shows staked assets
```

**Note:** Requires `KRAKEN_API_KEY` and `KRAKEN_API_SECRET` environment variables.
