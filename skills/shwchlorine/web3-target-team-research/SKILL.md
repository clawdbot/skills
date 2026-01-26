---
name: web3-target-team-research
description: Find crypto/web3 teams with $10M+ funding and verified Telegram contacts. Use when hunting for crypto leads, building contact lists, researching funded startups, or prospecting web3 companies. Spawns parallel subagent hunters to search VC portfolios and verify TG handles.
---

# Web3 Target Team Research

Find well-funded crypto teams ($10M+) with verified Telegram contacts for outreach.

## Quick Start

```
Hunt for crypto teams from [SOURCE]
```

Example sources: Paradigm portfolio, recent funding news, Solana ecosystem, DeFi protocols

## How It Works

1. **Spawn hunters** - Parallel subagents search different VC portfolios/sources
2. **Find teams** - Filter for $10M+ funding, check if already tracked
3. **Verify TG** - Screenshot t.me/{handle}, require pfp OR bio with company affiliation
4. **Add to CSV** - Append verified contacts to master CSV

## Commands

### Start Hunting
```
Start crypto hunters targeting [SOURCES]
```
Spawns 3 hunters with specified focus areas.

### Check Status
```
How many teams do we have?
```
Returns count from crypto-master.csv.

### Stop Hunting
```
Stop the crypto hunters
```
Removes the auto-respawn cron job.

## CSV Format

**Master CSV:** `crypto-master.csv`
```
Name,Chain,Category,Website,X Link,Funding,Contacts
Uniswap,ETH,DEX,https://uniswap.org,https://x.com/Uniswap,$165M,"Hayden Adams (Founder) @haaboris"
```

**No-Contacts CSV:** `crypto-no-contacts.csv` (teams researched but no valid TG found)

**Chain values:** ETH, SOL, BASE, ARB, OP, MATIC, AVAX, BTC, MULTI, N/A

## TG Verification Rules

A TG handle is **valid** if the profile has:
- Profile picture (pfp), OR
- Bio mentioning the company/role

**Invalid:** Empty profiles, wrong person, channels instead of personal accounts

## Hunter Task Template

See [references/hunter-task.md](references/hunter-task.md) for the full subagent task template.

## Auto-Hunting Setup

To run hunters continuously:

1. Create a cron job that checks hunter count every 10 minutes
2. Add to HEARTBEAT.md to auto-respawn if < 3 hunters active

See [references/auto-hunt-setup.md](references/auto-hunt-setup.md) for cron configuration.

## Best Sources (by success rate)

**High yield (~40%+ TG conversion):**
- Consumer/DeFi protocols (Paradigm, Dragonfly, Framework)
- Bridge/interop projects
- Security/auditing firms

**Medium yield (~20-30%):**
- Gaming/NFT (Animoca, Immutable)
- L2s and infrastructure
- Asia-focused VCs (Hashed, OKX Ventures)

**Low yield (<20%):**
- Enterprise/institutional (Point72, Tiger Global)
- Oracles and data providers
- Social/community platforms

## Tips

- Always `grep -i "TeamName"` both CSVs before adding
- Team members often have different X vs TG handles
- Founders have lower TG presence than BD/marketing roles
- Recent funding announcements = fresher, more findable contacts
