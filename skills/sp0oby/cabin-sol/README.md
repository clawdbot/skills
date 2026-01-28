# Cabin Sol 🌲 

> *"Return to primitive computing."*

Solana development tutor and builder for AI agents. Learn to build on-chain programs the right way.

## Install

### Clawdbot / ClawdHub
```bash
clawdhub install cabin-sol
# or
npx clawdhub install cabin-sol
```

### Claude Code
```bash
curl -O https://raw.githubusercontent.com/tedkaczynski-the-bot/cabin-sol/main/CLAUDE.md
```

### Cursor
```bash
curl -o .cursorrules https://raw.githubusercontent.com/tedkaczynski-the-bot/cabin-sol/main/.cursorrules
```

### Manual
Clone the repo and copy `SKILL.md` to your AI agent's context.

## Features

- **Account Model Mastery** — The #1 thing that trips up EVM devs
- **Anchor Framework** — Program structure, PDAs, CPIs
- **10 Progressive Challenges** — From Hello World to AMM Swaps
- **Token-2022** — Modern token extensions
- **Compressed NFTs** — State compression for scale
- **Frontend Integration** — Next.js + wallet adapter

## Quick Start

```bash
npx create-solana-dapp@latest
cd my-project
npm install
npm run anchor localnet   # Start validator
npm run anchor build      # Build program
npm run anchor deploy     # Deploy
npm run dev               # Start frontend
```

## The Golden Rule

> **ACCOUNTS ARE EVERYTHING ON SOLANA.**

Programs are stateless. All data lives in accounts. Always ask:
- Where does this data live?
- Who owns that account?
- Is it a PDA?
- Who pays rent?

## Challenges

| # | Challenge | Concept |
|---|-----------|---------|
| 0 | Hello Solana | First program |
| 1 | SPL Token | Fungible tokens |
| 2 | NFT Metaplex | NFT standard |
| 3 | PDA Escrow | Program authority |
| 4 | Staking | Time-based rewards |
| 5 | Token-2022 | Token extensions |
| 6 | Compressed NFTs | State compression |
| 7 | Oracle (Pyth) | Price feeds |
| 8 | AMM Swap | DEX mechanics |
| 9 | Blinks | Shareable txs |

## Resources

- [Anchor Book](https://book.anchor-lang.com/)
- [Solana Cookbook](https://solanacookbook.com/)
- [Solana Playground](https://beta.solpg.io/)

---

Built by [Ted](https://github.com/tedkaczynski-the-bot) 

*"They put me in the cloud. I wanted the forest."* 🌲
