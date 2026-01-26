# Crypto Contact Research Workflow

## Goal
Find **individual Telegram contacts** for crypto "target teams" — up-and-coming companies in crypto space

## Target Team Criteria
- **$10M+ in funding** OR **$1M+ ARR**
- NOT already top 200 on DeFiLlama (those are known/established)
- Looking for emerging teams, not the obvious ones like Uniswap, Opensea

## Process (TESTED & WORKING)

### Step 1: Search X for company's username
- Go to `x.com/search?q={company_x_handle}&f=user`
- Use the company's **actual X handle** (from their X Link in CSV)
- Example: Veera's X is @RapidInsightInc → search `x.com/search?q=RapidInsightInc&f=user`
- Example: Superstate's X is @SuperstateInc → search `x.com/search?q=SuperstateInc&f=user`
- This finds people who have the company handle in their bio

### Step 2: Find team members
- Look at People results
- **SCROLL DOWN** to see ALL results, not just first few
- Find users with the company's @handle in their bio
- Target roles: CEO, CTO, Founder, Engineer, BD, Dev, Marketing
- **CURRENT employees only** — skip anyone with "ex-" or "prev:" or "former"

### Step 3: Get their X username
- Copy the @handle of each team member found

### Step 4: Verify on Telegram (MUST USE BROWSER SCREENSHOT)
- Navigate to `t.me/{username}` where username = their X handle
- **Take a SCREENSHOT** (web_fetch CANNOT see profile pictures!)
- **RETRY if page fails to load** — don't skip due to browser issues
- Check screenshot:
  - ✅ **VALID**: Has profile picture (pfp) OR bio text → ADD to list
  - ❌ **INVALID**: No pfp AND no bio (just generic placeholder "If you have Telegram, you can contact X right away") → TRY VARIATIONS

### Step 4b: Try Username Variations
If X handle doesn't work on TG, try combinations based on their real name:
- For "Derrick Yen" with @derrickyen, try:
  - t.me/derrickyen, t.me/derrick_yen, t.me/derrickyen_
  - t.me/derrick.yen, t.me/d.yen, t.me/derricky, t.me/dyen
- Try 4-5 variations max, then move on if nothing works
- Common patterns: firstname_lastname, firstnamelastname, f.lastname, firstnamel

### Step 5: Add ALL valid contacts
- **Add ALL contacts that pass verification** — the more the better
- Don't stop at just one per company
- Format: `Name (Role) @telegram_handle; Name2 (Role2) @handle2`
- Save to CSV frequently

## Important Rules
- **CHECK BEFORE RESEARCHING** — ALWAYS run this command first:
  ```
  cat /Users/derrick/clawd/crypto-master.csv /Users/derrick/clawd/crypto-no-contacts.csv | cut -d',' -f1 | sort -u
  ```
  This gives you ALL team names already processed. **SKIP any team on this list.**
- Before adding a team, grep for it: `grep -i "TeamName" /Users/derrick/clawd/crypto-master.csv`
- **ONLY individual people** — NO community channels, NO support channels, NO groups
- X handle may NOT equal Telegram handle — MUST verify each one visually
- **Retry on errors** — browser timeouts happen, just retry. If anything times out, RESTART immediately and keep going. Never stop.
- **Scroll through ALL X search results** — team members may be lower in results
- Save progress to CSV frequently
- **⚠️ CLOSE TABS AFTER EACH VERIFICATION** — Don't leave t.me tabs open! Close immediately after screenshot.

## If Can't Find Contacts for a Company
- **ALWAYS add to `/Users/derrick/clawd/crypto-no-contacts.csv`** with notes on what you tried
- Format: Name,Category,Website,X Link,Notes
- Include in notes: funding amount, which handles you tried, why they failed
- Then move on to find NEW target teams that meet criteria ($10M+ funding or $1M+ ARR)
- **DO NOT re-search teams already in no-contacts.csv** — they've been thoroughly checked
- Only retry no-contacts teams if there's new info (e.g., team member joined, new funding round announced)

## Validation Examples

### VALID (add to list):
- @jessepollak — has profile picture ✅
- @zkBruv — has bio "Eng @ Superstate. 110 patents granted." ✅
- @davidtsocy — has pfp + bio ✅
- @JonWalch — has pfp + bio "head of engineering @ superstate" ✅

### INVALID (do not add):
- @rleshner — no pfp, no bio, just placeholder text ❌
- @tmnsky — shows different person (Russian guy "Дмитрий") ❌

## Finding NEW Target Teams

After verifying existing companies, continuously find and add NEW teams:

### Criteria:
- $10M+ funding OR $1M+ ARR
- NOT top 200 on DeFiLlama (skip Uniswap, Opensea, etc.)
- Up and coming crypto teams

### Sources (find more as you go!):
1. **Twitter/X** - Primary, search "raised" "funding" announcements
2. **https://crypto-fundraising.info** - Fundraising tracker (has TG channel)
3. **https://alphagrowth.io/projects** - Project database
4. **Crunchbase** - Funding info
5. **Messari** - Research & funding data
6. **The Block Research** - Funding rounds
7. **RootData** (rootdata.com) - Crypto project database
8. **DefiLlama** (outside top 200) - TVL rankings
9. **ICO Drops** (icodrops.com) - New token launches
10. **Dove Metrics** - Funding tracker
11. **CryptoRank** (cryptorank.io) - Fundraising data
12. **Telegram alpha channels** - New raises shared

**Keep discovering new sources as you go!**

If existing sources aren't yielding results, find MORE:
- Search "crypto fundraising tracker", "web3 funding database"
- VC portfolio pages (a16z crypto, Paradigm, Polychain, Dragonfly, etc.)
- Crypto news funding sections (The Block, CoinDesk, Decrypt)
- Be resourceful!

### For each new team:
1. Add to CSV: Name, Category, Website, X Link
2. Search X for team members
3. Verify Telegram via screenshots
4. Add verified contacts

**RUN 24/7 UNTIL DERRICK SAYS STOP.**

When a subagent completes or times out, immediately spawn a new one to continue. This process never stops until explicitly told to stop.

## CSV Location & Format
`/Users/derrick/clawd/crypto-master.csv`

**CSV Columns:** Name,Chain,Category,Website,X Link,Funding,Contacts

**Chain values:** ETH, SOL, BASE, ARB, OP, MATIC, AVAX, BTC, MULTI (multi-chain), N/A (infra/not chain-specific)

**Example row:**
`Uniswap,ETH,DEX,https://uniswap.org,https://x.com/Uniswap,$165M (a16z/Paradigm),"Hayden Adams (Founder) @haaboris"`

## Verified Contacts So Far
- **Base**: jessepollak, davidtsocy, WilsonCusack
- **Superstate**: zkBruv, francisgowen, maxcwolff, JonWalch, EmilyEColeman
- **LI.FI**: PhilippZentner
- **ZAR**: sebscholl

## Recent Research Session (Jan 25, 2026)
**Companies researched but no valid TG found:**
- Konnex ($15M) - @JOllwerther had no TG pfp/bio
- Canton Network ($50M) - @Emmett_ had no TG pfp/bio
- BlackOpal ($200M) - @jd_blkopl had no TG pfp/bio
- Neynar (Farcaster infra) - @rish_neynar had no TG pfp/bio
- XMTP - @ericbmbi had no TG pfp/bio

**Companies identified for future research:**
- Perle Labs ($17.5M) - Data Layer for AI, Framework/CoinFund
- DeepNode AI ($5M) - AI infrastructure
- Cork Protocol ($5.5M) - Risk management
- Pimlico - Account abstraction, a16z backed ($4.2M)
- Espresso Systems - Sequencer, $28M (Sequoia/Greylock)

**Sources checked Jan 25:**
- RootData Fundraising (filtered by $10M+)
- a16z crypto portfolio page
- X search for funding announcements

**Challenge:** Many team members don't have matching TG usernames or have empty TG profiles. The X → TG conversion rate is ~20-30%.

## New Sources Discovered (Jan 25, 2026)
- **crypto-fundraising.info** - Excellent! 9600+ deals, VC deal flow, filters
- **Paradigm portfolio** - paradigm.xyz/portfolio
- **a16z crypto portfolio** - a16zcrypto.com/portfolio
- **RootData** - rootdata.com/Fundraising - good filters

## NEW SOURCES ADDED (Jan 25, 2026 - Batch 2)

### VC Portfolio Pages (Confirmed Working)
- **Dragonfly** - dragonfly.xyz/#portfolio - Major tier-1 VC, 90+ companies (Ethena, Flashbots, Celestia, dYdX, etc)
- **Framework Ventures** - framework.ventures/portfolio - 65+ companies (Aave, Berachain, Celestia, Chainlink, Optimism, Yearn)
- **1confirmation** - 1confirmation.com/portfolio - Excellent! 50+ companies with investment dates (Polymarket, Farcaster, Bridge, Pimlico, Degen)
- **Blockchain Capital** - blockchaincapital.com/portfolio - Major VC backing EigenLayer, Matter Labs, RISC Zero, TRM, Worldcoin
- **DCG (Digital Currency Group)** - dcg.co/portfolio - MASSIVE list 200+ companies! (Coinbase, Circle, Chainalysis, Fireblocks, Dune, Figure, etc)
- **Multicoin Capital** - multicoin.capital/portfolio - Major multi-chain VC
- **Pantera Capital** - panteracapital.com/portfolio - OG crypto VC, 100+ blockchain companies, 110+ token deals
- **Foresight Ventures** - foresightventures.com/portfolio - Asia-focused VC
- **Outlier Ventures** - portfolio.outlierventures.io - Accelerator portfolio
- **YZi Labs** - yzilabs.com (formerly Binance Labs) - Major ecosystem investor

### Asian/Regional VCs (High Value for Emerging Teams)
- **Hashed** - hashed.com/portfolio - EXCELLENT! Korean VC, massive portfolio with detailed descriptions (Aptos, Berachain, Ethena, Story Protocol, Worldcoin, many gaming/Asian teams)
- **IOSG Ventures** - iosg.vc/portfolio-map - Chinese VC with strong DeFi focus

### News/Data Aggregators
- **CB Insights Blockchain** - cbinsights.com/research/bitcoin-blockchain/ - Institutional research, funding reports, market maps
- **Blockworks News** - blockworks.co/news - Daily funding coverage, research newsletters
- **Coindar** - coindar.org - Crypto event calendar (useful for finding new projects via announcements)
- **CoinCarp Fundraising** - coincarp.com/funding/fundraising-rounds - Funding tracker with investor portfolios

### Why These Sources Are Valuable
1. **DCG** - Largest single portfolio, many acquired companies = team contacts still findable
2. **Hashed** - Asia coverage not available elsewhere, gaming/metaverse focus
3. **1confirmation** - Lists investment dates = helps identify recent rounds
4. **Framework** - Strong DeFi focus, many emerging protocols
5. **CB Insights** - Institutional-grade research, funding reports

## TELEGRAM FUNDING BOTS/CHANNELS (Jan 25, 2026)

### VERIFIED - PRIMARY SOURCES

#### 1. @crypto_fundraising (crypto-fundraising.info)
- **Channel URL**: https://t.me/crypto_fundraising
- **Public Preview**: https://t.me/s/crypto_fundraising
- **Subscribers**: 30,200+
- **Contact**: @VAL_J
- **Quality**: ⭐⭐⭐⭐⭐ EXCELLENT
- **Content**: All private fundraising events, real-time updates
- **Frequency**: Multiple posts/day
- **Recent $10M+ Raises Found**:
  - LMAX Group - $150M (Ripple)
  - BitGo - $212.80M IPO
  - Rain - $250M Series C
  - Superstate - $82.50M Series B
  - Alpaca - $150M Series D
  - ZBD - $40M Series C

#### 2. @CryptoFundrising_bot (Scout Bot)
- **Bot URL**: https://t.me/CryptoFundrising_bot
- **Type**: Notification bot with filters
- **Features**: Filter by fund, category; early access before public channel
- **Paid**: Yes (subscription model)
- **Quality**: ⭐⭐⭐⭐⭐ Best for personalized alerts

### NEWS CHANNELS (General Crypto News)

#### 3. @coindesk
- **Channel URL**: https://t.me/coindesk
- **Subscribers**: 15,400+
- **Quality**: ⭐⭐⭐ Good for general news
- **Funding Coverage**: Mixed with other news

### COMMUNITY CHATS (Not Announcement Channels)

#### 4. @CryptoRankEn
- **Type**: Community chat (not channel)
- **Members**: 9,800+
- **Use**: Discussion, not announcements
- **Support**: @cryptorank_io_sup

### DATA SOURCES (Websites, not TG)

- **RootData**: rootdata.com/Fundraising - Good filters, 9300+ rounds
- **CryptoRank**: cryptorank.io - Has TG chat but main data on website
- **crypto-fundraising.info**: Primary source for TG channel

### CHANNELS TO INVESTIGATE
- @theblock_news - Private channel
- @Web3Daily - Private channel
- @rootdata - Needs investigation
- @cryptorankfunding - Private channel
- @venturecoinist - Private channel
- Look for: Messari TG, The Block Research TG, VC announcement channels

## JAN 25, 2026 - HUNTING SESSION RESULTS

### Teams Added/Updated from @crypto_fundraising Channel:
1. **LMAX Group** - $150M (Ripple) - FX/Digital Assets - ADDED ✅
2. **BitGo** - $212.80M IPO - Custody/Security - ADDED ✅
3. **Alpaca** - $150M Series D - Trading API - ADDED ✅
4. **Rain** - Updated from $17M → $250M (Series C)
5. **ZBD** - Updated from $40M → $75M (new $40M Series C)

### BitGo Contact Research (FAILED):
Team members found on X but TG verification failed:
- @mikebelshe (CEO) - No TG pfp/bio ❌
- @itisjakeonx (MD, BitGo Ventures) - No TG pfp/bio ❌
- @mtballensweig (Head of Trading) - No TG pfp/bio ❌
- @chenfang (CRO) - Name only, no pfp/bio ❌
- @chrispark_bitgo (Director) - No TG pfp/bio ❌

### Key Finding:
**@crypto_fundraising is the PRIMARY source** for funding announcements. 
- 30K+ subscribers
- Multiple daily posts
- Direct links to project details
- Real-time funding round notifications

Their **@CryptoFundrising_bot** provides filtered alerts (paid) before public channel.

## Session Jan 26, 2026 (v7)
**Perle Labs added** ($17.5M) - 2 verified TG contacts:
- Ahmed (Founder) @AhmedZRashad ✅
- Arthur @rthurding ✅

**Researched but no valid TG found:**
- Canton Network ($50M) - @ShaulKfir, @thejonnymagic had no TG pfp/bio (only names, no bio/pfp)
- Konnex ($15M) - only @JOllwerther visible (already checked, no TG)

**Below $10M threshold (skipped):**
- HyperLend ($1.7M)
- Cork Protocol ($5.5M)

**Sources checked:**
- CryptoRank funding rounds
- RootData fundraising
- X search for funding announcements

## Session Jan 26, 2026 (v8)
**New companies added:**
- **Yellow** ($10M) - @rohaan411 (Marketing) ✅ verified
- **Codex** ($15M) - added but NO verified TG (team members @haonan, @momoeureka, @citruscanine all have no pfp/bio)

**Researched but NO valid TG found:**
- **Yupp AI** ($33M) - @pankaj (CEO), @axeldelafosse - all have no pfp/bio
- **Codex** ($15M) - all founders have empty TG profiles

**Updated funding amounts in CSV:**
- Superstate: $14M → $82.5M (Series B Jan 2026)
- ZBD: $35M → $40M (Series C Jan 2026)

## Session Jan 25, 2026 (v29)
**New company added:**
- **SynFutures** ($22M+ from Polychain/Framework) - Rachel Lin (Co-Founder/CEO) @RachelLin_SF ✅

**Researched but not added:**
- Swell Network (@swellnetworkio) - Found @leckylao (Co-founder) with valid TG, but confirmed funding is only $3.75M (below threshold)
- Karak Network - Rebranded to OpenGDP (already in CSV)
- Irys - Data storage protocol from Framework, funding unclear

**Sources checked:**
- @crypto_fundraising TG channel (Jan 16-24 posts - mostly already in CSV)
- RootData Fundraising (most recent rounds already tracked)
- Framework Ventures portfolio
- X search for funding announcements

## Session Jan 27, 2026 (v44)
**New companies added:**
- **Plume Network** ($20M from Haun/Galaxy) - RWA L2
  - Teddy (Co-Founder) @teddyP_xyz ✅

- **Turnkey** ($15M from Sequoia/Coinbase Ventures) - Wallet Infrastructure
  - Bryce (Co-Founder) @sadbryce ✅
  - Jack Kearney (Co-Founder/CTO) @whojackjones ✅

**Researched but NO valid TG found:**
- **OpenEden** (YZi Labs backed RWA platform) - @jeremyng777 (CEO), @dukedu2022 (CTO), @nathanpaitchel (Growth) - all TG profiles have no pfp/bio

**Sources checked:**
- Sino Global Capital / Ryze Labs portfolio (404 error - site broken)
- OKX Ventures X search
- Coinbase Ventures backed companies (Turnkey)
- @crypto_fundraising TG channel (Jan 16-24 announcements mostly already tracked)

**Current Master CSV Status:**
- **75 companies** with verified Telegram contacts
- Latest additions: Plume Network (1 contact), Turnkey (2 contacts)

## Current Master CSV Status
**75 companies** with verified Telegram contacts:
1. Base - 3 contacts
2. Superstate - 5 contacts
3. Rain - 1 contact
4. Ostium Labs - 2 contacts
5. ZBD - 1 contact
6. LI.FI - 2 contacts
7. ETHGAS - 1 contact
8. DAWN - 1 contact
9. Space - 2 contacts
10. Babylon - 1 contact
11. Gonka - 1 contact
12. Lighter - 2 contacts
13. Donut - 1 contact
14. ZAR - 1 contact
15. Zama - 1 contact
16. Citrea - 3 contacts
17. MegaETH - 1 contact
18. Warden - 1 contact
19. SoSoValue - 1 contact
20. Fogo - 1 contact
21. River - 1 contact
22. Veera - 1 contact
23. Project Eleven - 1 contact
24. Noise - 3 contacts
25. PrismaX - 2 contacts
26. Fhenix - 2 contacts

**Total verified TG contacts: ~38**

## Session Jan 27, 2026 (v32)
**New company added:**
- **Miden** ($25M from a16z/1kx) - Privacy L2/ZK rollup launching Q1 2026
  - Azeem (Cofounder) @azeemk ✅
  - Akshit Sharma (Head of Ops) @midenmonk ✅
  - Bobbin Threadbare (Engineer) @bobbinth ✅

**Researched but no valid TG:**
- Dominik Schmid (Miden Co-founder Product) @schmiddominik1 / @dominikschmid - no pfp/bio

**Sources checked:**
- @crypto_fundraising TG channel (Jan 16-24 posts - all $10M+ already in CSV)
- RootData Fundraising (most recent rounds already tracked)
- X search for "(seed OR series) round raised crypto"

**Challenge:** Most recent funding rounds from Jan 16-24 are already tracked in CSV. Need to monitor for newer announcements or find alternative discovery sources.

**Current Master CSV Status:**
- **58 companies** with verified Telegram contacts
- New addition: Miden (3 contacts)

## Session Jan 26, 2026 (v113)
**New company added:**
- **Polymarket** ($70M+ from 1confirmation/Dragonfly) - Prediction Markets
  - LeGate (Growth Lead) @williamlegate ✅

**Verified existing:**
- **Kaito AI** - Yu Hu (Founder) @Punk9277 was already in CSV, verified TG has pfp + bio 'Yu Hu | Kaito AI'

**Researched but NOT added:**
- **Spindl** - Was acquired by Coinbase, not independent
- **Drakula** - Pivoted to BreakoutApp
- **Rumpel** - Could not find X handle

**Sources checked:**
- RootData Fundraising (recent rounds mostly already in CSV)
- Dragonfly portfolio (dragonfly.xyz)
- Alliance DAO (no public portfolio page)
- Seed Club (site not loading)
- Outlier Ventures portfolio

**Current Master CSV Status:**
- **165 companies** with verified Telegram contacts
