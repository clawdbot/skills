# Program Derived Addresses (PDAs)

> *Addresses without private keys. Your program's vaults.*

## What Is a PDA?

A PDA is an address that:
1. Is derived deterministically from **seeds** + **program ID**
2. Has **no private key** (can't sign normally)
3. Only the **deriving program** can sign for it

## Why PDAs Exist

Programs need to own assets. But programs can't hold private keys.

Solution: PDAs. Addresses that only the program can authorize.

```
Regular Address: Has private key → Owner signs
PDA:             No private key  → Program signs via CPI
```

## Deriving PDAs

```rust
// In Rust
let (pda, bump) = Pubkey::find_program_address(
    &[b"vault", user.key().as_ref()],
    &program_id,
);

// In TypeScript
const [pda, bump] = PublicKey.findProgramAddressSync(
    [Buffer.from("vault"), user.toBuffer()],
    programId
);
```

## The Bump

Not all seed combinations produce valid PDAs. The `bump` is a number (0-255) that makes the address fall "off the curve" (no corresponding private key).

`find_program_address` tries bump=255, then 254, etc. until it finds a valid PDA.

**Always store the bump** to avoid recomputation:

```rust
#[account]
pub struct Vault {
    pub bump: u8,  // Store it!
}
```

## Using PDAs in Anchor

### Creating a PDA Account

```rust
#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer = user,
        space = 8 + 32 + 8 + 1,
        seeds = [b"vault", user.key().as_ref()],
        bump
    )]
    pub vault: Account<'info, Vault>,
    
    #[account(mut)]
    pub user: Signer<'info>,
    pub system_program: Program<'info, System>,
}
```

### Reading a PDA Account

```rust
#[derive(Accounts)]
pub struct DoSomething<'info> {
    #[account(
        seeds = [b"vault", user.key().as_ref()],
        bump = vault.bump  // Use stored bump
    )]
    pub vault: Account<'info, Vault>,
    pub user: Signer<'info>,
}
```

### PDA Signs a CPI

```rust
pub fn withdraw(ctx: Context<Withdraw>, amount: u64) -> Result<()> {
    let vault = &ctx.accounts.vault;
    
    // Build signer seeds
    let seeds = &[
        b"vault",
        ctx.accounts.user.key.as_ref(),
        &[vault.bump],
    ];
    let signer = &[&seeds[..]];
    
    // PDA signs the transfer
    token::transfer(
        CpiContext::new_with_signer(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.vault_token.to_account_info(),
                to: ctx.accounts.user_token.to_account_info(),
                authority: ctx.accounts.vault.to_account_info(),
            },
            signer,  // PDA signs!
        ),
        amount,
    )?;
    
    Ok(())
}
```

## Common Seed Patterns

```rust
// User-specific PDA
seeds = [b"user", user.key().as_ref()]

// Global singleton
seeds = [b"config"]

// User + token specific
seeds = [b"stake", user.key().as_ref(), mint.key().as_ref()]

// Counter-based (for multiple per user)
seeds = [b"order", user.key().as_ref(), &order_id.to_le_bytes()]
```

## Gotchas

### 1. Seeds Must Match Exactly
```rust
// Creation
seeds = [b"vault", user.key().as_ref()]

// Access - MUST be identical
seeds = [b"vault", user.key().as_ref()]  // 
seeds = [b"Vault", user.key().as_ref()]  //  Different!
```

### 2. Store the Bump
```rust
//  Recalculating is expensive and can fail
let (_, bump) = Pubkey::find_program_address(...);

//  Store at creation, use stored value
bump = vault.bump
```

### 3. Bump Is Part of Seeds for Signing
```rust
// When signing, include bump in seeds
let seeds = &[b"vault", user.as_ref(), &[bump]];
//                                      ^^^^^^^ Don't forget!
```

### 4. PDA ≠ Keypair
```rust
//  Can't do this
let pda = Keypair::new();  // PDAs aren't keypairs

//  Derive from seeds
let (pda, bump) = Pubkey::find_program_address(&seeds, &program_id);
```
