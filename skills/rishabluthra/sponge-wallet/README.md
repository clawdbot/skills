# Sponge Wallet — Claude Skill

A Claude Code skill for managing crypto wallets, transferring tokens, swapping on DEXes, and accessing paid APIs via x402 micropayments.

## Install

```bash
git clone https://github.com/paysponge/wallet-skills.git ~/.claude/skills/sponge-wallet
```

That's it. No dependencies — just needs Node.js 18+.

## Login

On first use, Claude will prompt you to log in. Or run manually:

```bash
node ~/.claude/skills/sponge-wallet/scripts/wallet.mjs login
```

This opens a browser for OAuth authentication. Credentials are saved to `~/.spongewallet/credentials.json`.

## What it can do

- **Check balances** across Ethereum, Base, and Solana
- **Transfer** ETH, SOL, and USDC
- **Swap tokens** on Solana via Jupiter
- **View transaction** status and history
- **Request funding** from your main wallet
- **Search the web** via Exa (x402)
- **Generate images** via Gemini (x402)
- **Query prediction markets** via Dome (x402)
- **Scrape web pages** via Firecrawl (x402)
- **Parse documents** via Reducto (x402)
- **Find sales prospects** via Apollo (x402)

## Usage

Just ask Claude naturally:

- "Check my wallet balance"
- "Transfer 10 USDC to 0x..."
- "Swap 1 SOL for USDC"
- "Search for AI research papers"
- "What are the odds on the next election?"

## Supported chains

| Key type | Chains |
|----------|--------|
| `sponge_test_*` | sepolia, base-sepolia, solana-devnet, tempo |
| `sponge_live_*` | ethereum, base, solana |

## Docs

- [SKILL.md](SKILL.md) — Tool catalog and workflows
- [REFERENCE.md](REFERENCE.md) — Detailed parameter reference
