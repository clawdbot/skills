# Hunter Subagent Task Template

Use this template when spawning crypto hunter subagents via `sessions_spawn`:

```
You are a crypto team hunter. Find NEW crypto teams with $10M+ funding and get verified Telegram contacts.

**YOUR SOURCES:** [SPECIFY SOURCES - e.g., "Paradigm portfolio", "recent Jan 2026 funding", "Solana ecosystem"]

**CHECK FIRST:** grep -i "TeamName" [WORKSPACE]/crypto-master.csv [WORKSPACE]/crypto-no-contacts.csv — SKIP if already there!

**PROCESS:**
1. Browse source portfolios/funding news
2. Find teams with $10M+ funding
3. Search X for team members with @company in bio
4. Verify TG via web_fetch on t.me/{handle}
5. Valid = has pfp OR bio mentioning company
6. Add valid contacts to crypto-master.csv
7. Add failed verifications to crypto-no-contacts.csv

**CSV FORMAT:** Name,Chain,Category,Website,X Link,Funding,Contacts
**Chain values:** ETH, SOL, BASE, ARB, OP, MATIC, AVAX, BTC, MULTI, N/A
**Contacts format:** "Name (Role) @tghandle; Name2 (Role2) @tghandle2"

Add 3-5 NEW teams then report findings.
```

## Spawn Example

```javascript
sessions_spawn({
  label: "crypto-hunter-v1",
  task: "[TEMPLATE ABOVE WITH SOURCES FILLED IN]",
  runTimeoutSeconds: 1800
})
```

## Good Source Categories

**VC Portfolios:**
- Paradigm, a16z crypto, Polychain, Dragonfly, Framework
- Pantera, Multicoin, Electric Capital, Variant
- Hack VC, Haun Ventures, 1kx, Placeholder

**Funding News:**
- RootData Fundraising (rootdata.com/Fundraising)
- @crypto_fundraising Telegram channel
- crypto-fundraising.info

**Ecosystems:**
- Solana: Solana Ventures, Colosseum winners
- Base: Base ecosystem grants
- Sui/Aptos: Foundation investments

**Categories:**
- DeFi protocols, L2s, bridges/interop
- Security/auditing, developer tools
- Gaming, DePIN, AI x crypto
