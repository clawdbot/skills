# Challenge 1: SPL Token

> *Create your own fungible token. Digital leaves.*

## Goal

Create, mint, and transfer SPL tokens. Understand token accounts and Associated Token Accounts (ATAs).

## Key Concept

**Every token needs TWO types of accounts:**
1. **Mint** — The token definition (decimals, supply, mint authority)
2. **Token Account** — Holds tokens for a specific wallet

One wallet can have many token accounts (one per token type).

## CLI Quick Start

```bash
# Create a new token
spl-token create-token
# Output: Creating token ABC123...

# Create token account for your wallet
spl-token create-account ABC123

# Mint 1000 tokens
spl-token mint ABC123 1000

# Check balance
spl-token balance ABC123

# Transfer to another wallet
spl-token transfer ABC123 100 RECIPIENT_ADDRESS --fund-recipient
```

## In Anchor

### Create Mint

```rust
use anchor_lang::prelude::*;
use anchor_spl::token::{Mint, Token};

#[derive(Accounts)]
pub struct CreateMint<'info> {
    #[account(
        init,
        payer = authority,
        mint::decimals = 9,
        mint::authority = authority,
    )]
    pub mint: Account<'info, Mint>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
}
```

### Mint Tokens

```rust
use anchor_spl::token::{self, MintTo, Token, TokenAccount};

pub fn mint_tokens(ctx: Context<MintTokens>, amount: u64) -> Result<()> {
    token::mint_to(
        CpiContext::new(
            ctx.accounts.token_program.to_account_info(),
            MintTo {
                mint: ctx.accounts.mint.to_account_info(),
                to: ctx.accounts.token_account.to_account_info(),
                authority: ctx.accounts.authority.to_account_info(),
            },
        ),
        amount,
    )?;
    Ok(())
}

#[derive(Accounts)]
pub struct MintTokens<'info> {
    #[account(mut)]
    pub mint: Account<'info, Mint>,
    #[account(mut)]
    pub token_account: Account<'info, TokenAccount>,
    pub authority: Signer<'info>,
    pub token_program: Program<'info, Token>,
}
```

### Transfer Tokens

```rust
use anchor_spl::token::{self, Transfer, Token, TokenAccount};

pub fn transfer(ctx: Context<TransferTokens>, amount: u64) -> Result<()> {
    token::transfer(
        CpiContext::new(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.from.to_account_info(),
                to: ctx.accounts.to.to_account_info(),
                authority: ctx.accounts.authority.to_account_info(),
            },
        ),
        amount,
    )?;
    Ok(())
}

#[derive(Accounts)]
pub struct TransferTokens<'info> {
    #[account(mut)]
    pub from: Account<'info, TokenAccount>,
    #[account(mut)]
    pub to: Account<'info, TokenAccount>,
    pub authority: Signer<'info>,
    pub token_program: Program<'info, Token>,
}
```

## Associated Token Accounts

ATAs are deterministic token accounts derived from wallet + mint:

```rust
use anchor_spl::associated_token::AssociatedToken;

#[derive(Accounts)]
pub struct CreateATA<'info> {
    #[account(
        init_if_needed,
        payer = payer,
        associated_token::mint = mint,
        associated_token::authority = owner,
    )]
    pub token_account: Account<'info, TokenAccount>,
    pub mint: Account<'info, Mint>,
    pub owner: SystemAccount<'info>,
    #[account(mut)]
    pub payer: Signer<'info>,
    pub token_program: Program<'info, Token>,
    pub associated_token_program: Program<'info, AssociatedToken>,
    pub system_program: Program<'info, System>,
}
```

## Gotchas

1. **Decimals matter** — 9 decimals means 1 token = 1_000_000_000 base units
2. **Token accounts are separate** — Can't just send to a wallet address
3. **ATAs simplify UX** — Deterministic addresses for any wallet+token pair
4. **Authority required** — Only mint authority can mint, only owner can transfer

## Cargo.toml

```toml
[dependencies]
anchor-lang = "0.30.0"
anchor-spl = "0.30.0"
```

## Next

→ Challenge 2: NFT Metaplex — Non-fungible tokens and metadata
