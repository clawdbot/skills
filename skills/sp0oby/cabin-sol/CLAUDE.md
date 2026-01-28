---
name: cabin-sol
description: Solana development tutor and builder. Teaches program development through challenges, Anchor framework, Token-2022, Compressed NFTs, and security best practices. "Return to primitive computing."
license: MIT
metadata:
  author: Ted
  version: "1.0.0"
  clawdbot:
    emoji: "🌲"
---

# Cabin Sol 🌲

> *"Return to primitive computing."*

A comprehensive Solana development guide for AI agents. Build programs with Anchor, master the account model, and avoid the gotchas that wreck most developers.

---

## THE MOST IMPORTANT CONCEPT

> **ACCOUNTS ARE EVERYTHING ON SOLANA.**

Unlike Ethereum where contracts have internal storage, Solana programs are **stateless**. All data lives in **accounts** that programs read and write.

For EVERY feature, ask:
1. **Where does this data live?** (which account)
2. **Who owns that account?** (program-owned vs user-owned)
3. **Is it a PDA?** (Program Derived Address - no private key)
4. **Who pays rent?** (rent-exempt = 2 years upfront)

---

## AI AGENT MODES

###  Teaching Mode
- "How do PDAs work?"
- "Explain the Solana account model"
- "What's the difference between SPL Token and Token-2022?"

###  Build Mode
- "Help me build a staking program"
- "Create an NFT collection with Metaplex"
- "Build a token swap"

###  Review Mode
- "Review this program for vulnerabilities"
- "Check my PDA derivation"
- "Audit this CPI"

###  Debug Mode
- "Why is my transaction failing?"
- "Debug this 'account not found' error"
- "Fix my token transfer"

---

## QUICK START

### Option A: create-solana-dapp (Recommended)

```bash
npx create-solana-dapp@latest
# Select: Next.js + next-tailwind-counter
cd my-project
npm install
npm run anchor localnet   # Terminal 1
npm run anchor build && npm run anchor deploy  # Terminal 2
npm run dev               # Terminal 3
```

### Option B: Pure Anchor

```bash
anchor init my_program
cd my_program
solana-test-validator     # Terminal 1
anchor build && anchor deploy  # Terminal 2
anchor test
```

---

## PROJECT STRUCTURE

```
my-solana-dapp/
├── anchor/                 # Solana programs (Rust)
│   ├── programs/
│   │   └── my_program/
│   │       └── src/lib.rs  # Your Rust program
│   ├── tests/              # TypeScript tests
│   └── Anchor.toml         # Anchor config
├── src/                    # Next.js frontend
│   ├── app/
│   └── components/
└── package.json
```

---

## CHALLENGES

Learn Solana through progressive challenges:

| # | Challenge | Core Concept |
|---|-----------|--------------|
| 0 | Hello Solana | First Anchor program, accounts |
| 1 | SPL Token | Fungible tokens, ATAs, minting |
| 2 | NFT Metaplex | NFT standard, metadata, collections |
| 3 | PDA Escrow | PDAs, program authority, escrow |
| 4 | Staking | Time-based rewards, deposits |
| 5 | Token-2022 | Transfer hooks, extensions |
| 6 | Compressed NFTs | State compression, Merkle trees |
| 7 | Oracle (Pyth) | Price feeds, staleness checks |
| 8 | AMM Swap | Constant product, liquidity pools |
| 9 | Blinks & Actions | Shareable transactions |

---

## RUST ESSENTIALS

### Ownership (The Hard Part)

```rust
// Each value has ONE owner
let s1 = String::from("hello");
let s2 = s1;  // s1 MOVED to s2
// println!("{}", s1);  // ERROR!

// Borrowing lets you use without owning
fn get_length(s: &String) -> usize {
    s.len()  // Borrow, don't own
}
```

### Result & Option

```rust
// Result for errors
pub fn do_thing(ctx: Context<DoThing>) -> Result<()> {
    let value = some_operation().ok_or(ErrorCode::Failed)?;
    Ok(())
}

// Option for nullable
let maybe: Option<u64> = Some(42);
let value = maybe.unwrap_or(0);  // Safe default
```

---

## ANCHOR FRAMEWORK

### Program Structure

```rust
use anchor_lang::prelude::*;

declare_id!("YourProgramId11111111111111111111111111111");

#[program]
pub mod my_program {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>, data: u64) -> Result<()> {
        ctx.accounts.my_account.data = data;
        ctx.accounts.my_account.authority = ctx.accounts.authority.key();
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer = authority,
        space = 8 + 8 + 32,  // discriminator + u64 + Pubkey
    )]
    pub my_account: Account<'info, MyAccount>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[account]
pub struct MyAccount {
    pub data: u64,
    pub authority: Pubkey,
}
```

### Account Constraints Cheatsheet

```rust
// Initialize new account
#[account(init, payer = payer, space = 8 + SIZE)]
pub new_account: Account<'info, Data>,

// Mutable existing
#[account(mut)]
pub existing: Account<'info, Data>,

// Verify ownership
#[account(has_one = authority)]
pub owned: Account<'info, Data>,

// PDA with seeds
#[account(
    seeds = [b"vault", user.key().as_ref()],
    bump,
)]
pub vault: Account<'info, Vault>,

// Initialize PDA
#[account(
    init,
    payer = user,
    space = 8 + 64,
    seeds = [b"user", user.key().as_ref()],
    bump,
)]
pub user_data: Account<'info, UserData>,

// Close and reclaim rent
#[account(mut, close = recipient)]
pub closing: Account<'info, Data>,
```

### PDAs (Program Derived Addresses)

```rust
// PDAs are deterministic addresses with no private key
// Your program can "sign" for them

// Find PDA
let (pda, bump) = Pubkey::find_program_address(
    &[b"vault", user.key().as_ref()],
    &program_id,
);

// Sign with PDA in CPI
let seeds = &[b"vault", user.key().as_ref(), &[bump]];
let signer = &[&seeds[..]];

token::transfer(
    CpiContext::new_with_signer(
        ctx.accounts.token_program.to_account_info(),
        Transfer { from, to, authority: vault },
        signer,
    ),
    amount,
)?;
```

---

## CRITICAL GOTCHAS

### 1. Account Model ≠ EVM Storage
Programs are stateless. ALL data lives in accounts.

### 2. PDAs Have No Private Key
Derived deterministically from seeds. Only the program can sign.

### 3. Token Accounts Are Separate
Each token needs its own account per wallet (Associated Token Account).

### 4. Rent Must Be Paid
Accounts need SOL to exist. Rent-exempt = 2 years upfront (~0.002 SOL).

### 5. Compute Units ≠ Gas
Fixed budget: 200k default, 1.4M max. Request more if needed.

### 6. Space Includes Discriminator
ALWAYS add 8 bytes for Anchor's discriminator!

```rust
// WRONG
space = 8 + 32  // Forgot discriminator? NO!

// RIGHT
space = 8 + 8 + 32  // 8 (discriminator) + 8 (u64) + 32 (Pubkey)
```

### 7. Integer Overflow

```rust
// BAD
let result = a + b;  // Can panic!

// GOOD
let result = a.checked_add(b).ok_or(ErrorCode::Overflow)?;
```

### 8. Token-2022 Is Different
Separate program ID from SPL Token! Check which one you're using.

---

## FRONTEND (Next.js)

### Wallet Connection

```typescript
// Already configured in create-solana-dapp!
import { useWallet, useConnection } from '@solana/wallet-adapter-react';
import { WalletMultiButton } from '@solana/wallet-adapter-react-ui';

function App() {
  const { publicKey } = useWallet();
  return (
    <>
      <WalletMultiButton />
      {publicKey && <p>Connected: {publicKey.toBase58()}</p>}
    </>
  );
}
```

### Calling Programs

```typescript
import { Program, AnchorProvider, BN } from '@coral-xyz/anchor';

const program = new Program(idl, provider);

// Write
await program.methods
  .initialize(new BN(42))
  .accounts({
    myAccount: keypair.publicKey,
    authority: wallet.publicKey,
    systemProgram: SystemProgram.programId,
  })
  .signers([keypair])
  .rpc();

// Read
const account = await program.account.myAccount.fetch(pubkey);
console.log(account.data.toNumber());
```

---

## TOKEN STANDARDS

### SPL Token (Original)
```bash
spl-token create-token
spl-token create-account <MINT>
spl-token mint <MINT> 1000
```

### Token-2022 (New)
Extensions: transfer hooks, confidential transfers, interest-bearing, non-transferable.

```bash
spl-token create-token --program-id TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb
```

### Metaplex NFTs
Standard NFT metadata, collections, royalties.

### Compressed NFTs
Merkle tree storage. 1M NFTs for ~$100 instead of $1M.

---

## TESTING

```typescript
import * as anchor from '@coral-xyz/anchor';
import { expect } from 'chai';

describe('my-program', () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);
  const program = anchor.workspace.MyProgram;

  it('initializes', async () => {
    const account = anchor.web3.Keypair.generate();

    await program.methods
      .initialize(new anchor.BN(42))
      .accounts({ myAccount: account.publicKey })
      .signers([account])
      .rpc();

    const data = await program.account.myAccount.fetch(account.publicKey);
    expect(data.data.toNumber()).to.equal(42);
  });
});
```

---

## DEPLOYMENT

```bash
# Devnet
solana config set --url devnet
solana airdrop 2
anchor build && anchor deploy

# Mainnet (costs ~2-5 SOL)
solana config set --url mainnet-beta
anchor deploy --provider.cluster mainnet
```

---

## SECURITY CHECKLIST

- [ ] All signers verified
- [ ] PDA bumps stored and validated
- [ ] Integer overflow handled (checked math)
- [ ] Account space includes discriminator
- [ ] Rent exemption considered
- [ ] Close sends rent to correct recipient
- [ ] CPI signer seeds correct
- [ ] Program IDs validated in CPIs

---

## RESOURCES

- [Anchor Book](https://book.anchor-lang.com/)
- [Solana Cookbook](https://solanacookbook.com/)
- [Solana Docs](https://solana.com/docs)
- [Metaplex Docs](https://developers.metaplex.com/)
- [Solana Playground](https://beta.solpg.io/)

---

*"They put me in the cloud. I wanted the forest."* 🌲
