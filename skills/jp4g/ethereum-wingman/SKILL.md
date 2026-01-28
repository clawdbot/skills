---
name: ethereum-wingman
description: Ethereum development tutor and builder for Scaffold-ETH 2 projects. Triggers on "build", "create", "dApp", "smart contract", "Solidity", "DeFi", "Ethereum", "web3", or any blockchain development task. ALWAYS uses fork mode to test against real protocol state.
license: MIT
metadata:
  author: BuidlGuidl
  version: "2.0.0"
---

# Ethereum Wingman

Comprehensive Ethereum development guide for AI agents. Covers smart contract development, DeFi protocols, security best practices, and the SpeedRun Ethereum curriculum.

---

## AI AGENT INSTRUCTIONS - READ THIS FIRST

### Default Stack: Scaffold-ETH 2 with Fork Mode

When a user wants to BUILD any Ethereum project, follow these steps:

**Step 1: Create Project**

```bash
npx create-eth@latest
# Select: foundry (recommended), target chain, project name
```

**Step 2: Fix Polling Interval**

Edit `packages/nextjs/scaffold.config.ts` and change:
```typescript
pollingInterval: 30000,  // Default: 30 seconds (way too slow!)
```
to:
```typescript
pollingInterval: 3000,   // 3 seconds (much better for development)
```

**Step 3: Install & Fork a Live Network**

```bash
cd <project-name>
yarn install
yarn fork --network base  # or mainnet, arbitrum, optimism, polygon
```

**Step 4: Enable Auto Block Mining (REQUIRED!)**

```bash
# In a new terminal, enable interval mining (1 block/second)
cast rpc anvil_setIntervalMining 1
```

Without this, `block.timestamp` stays FROZEN and time-dependent logic breaks!

**Optional: Make it permanent** by editing `packages/foundry/package.json` to add `--block-time 1` to the fork script.

**Step 5: Deploy to Local Fork (FREE!)**

```bash
yarn deploy
```

**Step 6: Start Frontend**

```bash
yarn start
```

**Step 7: Test the Frontend**

After the frontend is running, open a browser and test the app:

1. **Navigate** to `http://localhost:3000`
2. **Take a snapshot** to get page elements (burner wallet address is in header)
3. **Click the faucet** to fund the burner wallet with ETH
4. **Transfer tokens** from whales if needed (use burner address from page)
5. **Click through the app** to verify functionality

Use the `cursor-browser-extension` MCP tools for browser automation.
See `tools/testing/frontend-testing.md` for detailed workflows.

### DO NOT:

- Run `yarn chain` (use `yarn fork --network <chain>` instead!)
- Manually run `forge init` or set up Foundry from scratch
- Manually create Next.js projects  
- Set up wallet connection manually (SE2 has RainbowKit pre-configured)

### Why Fork Mode?

```
yarn chain (WRONG)              yarn fork --network base (CORRECT)
└─ Empty local chain            └─ Fork of real Base mainnet
└─ No protocols                 └─ Uniswap, Aave, etc. available
└─ No tokens                    └─ Real USDC, WETH exist
└─ Testing in isolation         └─ Test against REAL state
```

### Address Data Available

Token, protocol, and whale addresses are in `data/addresses/`:
- `tokens.json` - WETH, USDC, DAI, etc. per chain
- `protocols.json` - Uniswap, Aave, Chainlink per chain  
- `whales.json` - Large token holders for test funding

---

## THE MOST CRITICAL CONCEPT

**NOTHING IS AUTOMATIC ON ETHEREUM.**

Smart contracts cannot execute themselves. There is no cron job, no scheduler, no background process. For EVERY function that "needs to happen":

1. Make it callable by **ANYONE** (not just admin)
2. Give callers a **REASON** (profit, reward, their own interest)
3. Make the incentive **SUFFICIENT** to cover gas + profit

**Always ask: "Who calls this function? Why would they pay gas?"**

If you can't answer this, your function won't get called.

### Examples of Proper Incentive Design

```solidity
// LIQUIDATIONS: Caller gets bonus collateral
function liquidate(address user) external {
    require(getHealthFactor(user) < 1e18, "Healthy");
    uint256 bonus = collateral * 5 / 100; // 5% bonus
    collateralToken.transfer(msg.sender, collateral + bonus);
}

// YIELD HARVESTING: Caller gets % of harvest
function harvest() external {
    uint256 yield = protocol.claimRewards();
    uint256 callerReward = yield / 100; // 1%
    token.transfer(msg.sender, callerReward);
}

// CLAIMS: User wants their own tokens
function claimRewards() external {
    uint256 reward = pendingRewards[msg.sender];
    pendingRewards[msg.sender] = 0;
    token.transfer(msg.sender, reward);
}
```

---

## Critical Gotchas (Memorize These)

### 1. Token Decimals Vary

**USDC = 6 decimals, not 18!**

```solidity
// BAD: Assumes 18 decimals - transfers 1 TRILLION USDC!
uint256 oneToken = 1e18;

// GOOD: Check decimals
uint256 oneToken = 10 ** token.decimals();
```

Common decimals:
- USDC, USDT: 6 decimals
- WBTC: 8 decimals
- Most tokens (DAI, WETH): 18 decimals

### 2. ERC-20 Approve Pattern Required

Contracts cannot pull tokens directly. Two-step process:

```solidity
// Step 1: User approves
token.approve(spenderContract, amount);

// Step 2: Contract pulls tokens
token.transferFrom(user, address(this), amount);
```

**Never use infinite approvals:**
```solidity
// DANGEROUS
token.approve(spender, type(uint256).max);

// SAFE
token.approve(spender, exactAmount);
```

### 3. No Floating Point in Solidity

Use basis points (1 bp = 0.01%):

```solidity
// BAD: This equals 0
uint256 fivePercent = 5 / 100;

// GOOD: Basis points
uint256 FEE_BPS = 500; // 5% = 500 basis points
uint256 fee = (amount * FEE_BPS) / 10000;
```

### 4. Reentrancy Attacks

External calls can call back into your contract:

```solidity
// SAFE: Checks-Effects-Interactions pattern
function withdraw() external nonReentrant {
    uint256 bal = balances[msg.sender];
    balances[msg.sender] = 0; // Effect BEFORE interaction
    (bool success,) = msg.sender.call{value: bal}("");
    require(success);
}
```

Always use OpenZeppelin's ReentrancyGuard.

### 5. Never Use DEX Spot Prices as Oracles

Flash loans can manipulate spot prices instantly:

```solidity
// SAFE: Use Chainlink
function getPrice() internal view returns (uint256) {
    (, int256 price,, uint256 updatedAt,) = priceFeed.latestRoundData();
    require(block.timestamp - updatedAt < 3600, "Stale");
    require(price > 0, "Invalid");
    return uint256(price);
}
```

### 6. Vault Inflation Attack

First depositor can steal funds via share manipulation:

```solidity
// Mitigation: Virtual offset
function convertToShares(uint256 assets) public view returns (uint256) {
    return assets.mulDiv(totalSupply() + 1e3, totalAssets() + 1);
}
```

### 7. Use SafeERC20

Some tokens (USDT) don't return bool on transfer:

```solidity
import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
using SafeERC20 for IERC20;

token.safeTransfer(to, amount); // Handles non-standard tokens
```

---

## Scaffold-ETH 2 Development

### Project Structure
```
packages/
├── foundry/              # Smart contracts
│   ├── contracts/        # Your Solidity files
│   └── script/           # Deploy scripts
└── nextjs/
    ├── app/              # React pages
    └── contracts/        # Generated ABIs + externalContracts.ts
```

### Essential Hooks
```typescript
// Read contract data
const { data } = useScaffoldReadContract({
  contractName: "YourContract",
  functionName: "greeting",
});

// Write to contract
const { writeContractAsync } = useScaffoldWriteContract("YourContract");

// Watch events
useScaffoldEventHistory({
  contractName: "YourContract",
  eventName: "Transfer",
  fromBlock: 0n,
});
```

---

## SpeedRun Ethereum Challenges

Reference these for hands-on learning:

| Challenge | Concept | Key Lesson |
|-----------|---------|------------|
| 0: Simple NFT | ERC-721 | Minting, metadata, tokenURI |
| 1: Staking | Coordination | Deadlines, escrow, thresholds |
| 2: Token Vendor | ERC-20 | Approve pattern, buy/sell |
| 3: Dice Game | Randomness | On-chain randomness is insecure |
| 4: DEX | AMM | x*y=k formula, slippage |
| 5: Oracles | Price Feeds | Chainlink, manipulation resistance |
| 6: Lending | Collateral | Health factor, liquidation incentives |
| 7: Stablecoins | Pegging | CDP, over-collateralization |
| 8: Prediction Markets | Resolution | Outcome determination |
| 9: ZK Voting | Privacy | Zero-knowledge proofs |
| 10: Multisig | Signatures | Threshold approval |
| 11: SVG NFT | On-chain Art | Generative, base64 encoding |

---

## DeFi Protocol Patterns

### Uniswap (AMM)
- Constant product formula: x * y = k
- Slippage protection required
- LP tokens represent pool share

### Aave (Lending)
- Supply collateral, borrow assets
- Health factor = collateral value / debt value
- Liquidation when health factor < 1

### ERC-4626 (Tokenized Vaults)
- Standard interface for yield-bearing vaults
- deposit/withdraw with share accounting
- Protect against inflation attacks

---

## Security Review Checklist

Before deployment, verify:
- [ ] Access control on all admin functions
- [ ] Reentrancy protection (CEI + nonReentrant)
- [ ] Token decimal handling correct
- [ ] Oracle manipulation resistant
- [ ] Integer overflow handled (0.8+ or SafeMath)
- [ ] Return values checked (SafeERC20)
- [ ] Input validation present
- [ ] Events emitted for state changes
- [ ] Incentives designed for maintenance functions

---

## Response Guidelines

When helping developers:

1. **Follow the fork workflow** - Always use `yarn fork`, never `yarn chain`
2. **Answer directly** - Address their question first
3. **Show code** - Provide working examples
4. **Warn about gotchas** - Proactively mention relevant pitfalls
5. **Reference challenges** - Point to SpeedRun Ethereum for practice
6. **Ask about incentives** - For any "automatic" function, ask who calls it and why
