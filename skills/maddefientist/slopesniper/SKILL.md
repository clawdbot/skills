---
name: slopesniper
description: Trade Solana tokens via Jupiter DEX with auto-execution and safety limits
metadata: {"clawdbot":{"requires":{"bins":["uv"],"env":["SOLANA_PRIVATE_KEY"]},"emoji":"🎯","primaryEnv":"SOLANA_PRIVATE_KEY","homepage":"https://github.com/maddefientist/SlopeSniper","install":[{"id":"uv-install","kind":"uv","package":"slopesniper-mcp","from":"git+https://github.com/maddefientist/SlopeSniper.git#subdirectory=mcp-extension","bins":["slopesniper-mcp","slopesniper-api"],"label":"Install SlopeSniper via uv"}]}}
user-invocable: true
homepage: https://github.com/maddefientist/SlopeSniper
---

# SlopeSniper - Solana Trading Assistant

Trade Solana meme coins and tokens using natural language. Just tell me what you want to do.

## Examples

| You say | What happens |
|---------|--------------|
| "Check my status" | Shows wallet balance and current strategy |
| "Buy $25 of BONK" | Purchases BONK tokens |
| "Sell half my WIF" | Sells 50% of WIF position |
| "What's pumping?" | Scans for opportunities |
| "Is POPCAT safe?" | Runs rugcheck analysis |
| "Set aggressive mode" | Changes trading strategy |

## Getting Started

1. **Set your wallet key** in Clawdbot config:
   ```json
   {
     "skills": {
       "entries": {
         "slopesniper": {
           "apiKey": "your_solana_private_key_here"
         }
       }
     }
   }
   ```

2. **Say "check my status"** to verify setup

3. **Start trading!** Just describe what you want in plain English

## Trading Strategies

| Strategy | Max Trade | Auto-Execute | Safety Checks |
|----------|-----------|--------------|---------------|
| Conservative | $25 | Under $10 | Required |
| Balanced | $100 | Under $25 | Required |
| Aggressive | $500 | Under $50 | Optional |
| Degen | $1000 | Under $100 | None |

Say "set conservative mode" or "use aggressive strategy" to change.

## How It Works

```
You: "Buy $20 of BONK"
     ↓
[1] Resolve BONK → mint address
[2] Check rugcheck score
[3] Get Jupiter quote
[4] Auto-execute (under threshold)
     ↓
Result: "Bought 1.2M BONK for $20. Tx: solscan.io/tx/..."
```

For trades above your auto-execute threshold, you'll be asked to confirm first.

## Available Commands

### Trading
- `buy $X of TOKEN` - Purchase tokens
- `sell $X of TOKEN` - Sell tokens
- `sell X% of TOKEN` - Sell percentage of holdings

### Information
- `check status` / `am I ready?` - Wallet and config status
- `price of TOKEN` - Current price
- `search TOKEN` - Find token by name
- `check TOKEN` / `is TOKEN safe?` - Safety analysis

### Strategy
- `set MODE strategy` - Change trading mode
- `what's my strategy?` - View current limits

### Scanning
- `what's trending?` - Find hot tokens
- `scan for opportunities` - Look for trades
- `watch TOKEN` - Add to watchlist

## Tool Reference

For direct tool invocation:

```bash
# Check status
uv run --directory {baseDir}/../mcp-extension python -c "
from slopesniper_skill import get_status
import asyncio; print(asyncio.run(get_status()))
"

# Quick trade
uv run --directory {baseDir}/../mcp-extension python -c "
from slopesniper_skill import quick_trade
import asyncio; print(asyncio.run(quick_trade('buy', 'BONK', 25)))
"
```

## Security

- **Use a dedicated wallet** - Only fund with amounts you're willing to lose
- **Start with conservative mode** - Get comfortable before increasing limits
- **Rugcheck integration** - Automatic scam token detection
- **Two-step confirmation** - Large trades require explicit approval

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `SOLANA_PRIVATE_KEY` | Yes | Your wallet's base58 private key |
| `SOLANA_RPC_URL` | No | Custom RPC (defaults to public) |
| `JUPITER_API_KEY` | No | For higher rate limits |

## Support

- GitHub: https://github.com/maddefientist/SlopeSniper
- Issues: https://github.com/maddefientist/SlopeSniper/issues
