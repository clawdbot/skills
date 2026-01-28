# The Solana Account Model

> *Everything is an account. This is the way.*

## The Core Truth

**Solana programs are stateless.** They contain only code, no data.

All data — balances, state, configuration — lives in **accounts**.

```
Ethereum: Contract has code + storage
Solana:   Program has code, Accounts have data
```

## Account Anatomy

Every account has:

| Field | Description |
|-------|-------------|
| `lamports` | Balance in lamports (1 SOL = 1B lamports) |
| `data` | Arbitrary bytes (your state lives here) |
| `owner` | Program that can modify this account |
| `executable` | Is this account a program? |
| `rent_epoch` | When rent was last paid |

## Ownership Rules

1. **Only the owner can modify `data`**
2. **Only the owner can debit `lamports`**
3. **Anyone can credit `lamports`**
4. **System Program owns new accounts**

```rust
// Your program owns accounts it creates
#[account(init, ...)]
pub my_account: Account<'info, MyData>,
// owner = YOUR_PROGRAM_ID

// User wallets are owned by System Program
pub user: Signer<'info>,
// owner = 11111111111111111111111111111111
```

## Program-Owned vs System-Owned

| Type | Owner | Can Hold SOL | Can Hold Data |
|------|-------|--------------|---------------|
| Wallet | System Program |  |  |
| Program Account | BPF Loader |  |  (code) |
| Data Account | Your Program |  |  |
| Token Account | Token Program |  |  (balance) |

## Reading Accounts in Instructions

Every instruction receives accounts as a list:

```rust
#[derive(Accounts)]
pub struct MyInstruction<'info> {
    // These accounts are passed by the client
    pub account_a: Account<'info, DataA>,
    pub account_b: Account<'info, DataB>,
    pub signer: Signer<'info>,
}
```

The client must pass all required accounts:

```typescript
await program.methods
  .myInstruction()
  .accounts({
    accountA: pubkeyA,
    accountB: pubkeyB,
    signer: wallet.publicKey,
  })
  .rpc();
```

## Why This Matters

1. **Parallel execution** — Solana knows which accounts each tx touches, can run non-overlapping txs in parallel

2. **Explicit dependencies** — No hidden state reads, everything is declared

3. **Rent model** — Accounts pay for their storage space

4. **Composability** — Any program can read any account (but only owner can write)

## Mental Model

Think of Solana as a database where:
- Programs = stored procedures
- Accounts = rows in tables
- Instructions = function calls that must declare which rows they touch

## Common Patterns

### Config Account
```rust
#[account]
pub struct Config {
    pub admin: Pubkey,
    pub fee_bps: u16,
    pub paused: bool,
}
```

### User State Account
```rust
#[account]
pub struct UserState {
    pub owner: Pubkey,
    pub balance: u64,
    pub last_action: i64,
}
```

### PDA for Deterministic Addresses
```rust
#[account(
    seeds = [b"user", owner.key().as_ref()],
    bump
)]
pub user_state: Account<'info, UserState>,
```
