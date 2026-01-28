# Challenge 3: PDA Escrow

> *Trust the program, not the person.*

## Goal

Build an escrow that holds tokens until conditions are met. Master PDAs as program-controlled vaults.

## Key Concept

**PDAs can hold assets** because they have no private key — only your program can sign for them.

```
User deposits → PDA holds → Conditions met → PDA releases
```

## The Escrow Pattern

```rust
use anchor_lang::prelude::*;
use anchor_spl::token::{self, Token, TokenAccount, Transfer};

declare_id!("YourProgramId");

#[program]
pub mod escrow {
    use super::*;

    pub fn create_escrow(
        ctx: Context<CreateEscrow>,
        amount: u64,
        unlock_time: i64,
    ) -> Result<()> {
        let escrow = &mut ctx.accounts.escrow;
        escrow.depositor = ctx.accounts.depositor.key();
        escrow.recipient = ctx.accounts.recipient.key();
        escrow.amount = amount;
        escrow.unlock_time = unlock_time;
        escrow.bump = ctx.bumps.escrow;
        escrow.vault_bump = ctx.bumps.vault;

        // Transfer tokens to vault PDA
        token::transfer(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.depositor_token.to_account_info(),
                    to: ctx.accounts.vault.to_account_info(),
                    authority: ctx.accounts.depositor.to_account_info(),
                },
            ),
            amount,
        )?;

        Ok(())
    }

    pub fn release(ctx: Context<Release>) -> Result<()> {
        let escrow = &ctx.accounts.escrow;
        
        // Check unlock time
        let clock = Clock::get()?;
        require!(
            clock.unix_timestamp >= escrow.unlock_time,
            EscrowError::TooEarly
        );

        // Transfer from vault to recipient
        let seeds = &[
            b"vault",
            escrow.depositor.as_ref(),
            &[escrow.vault_bump],
        ];
        let signer = &[&seeds[..]];

        token::transfer(
            CpiContext::new_with_signer(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.vault.to_account_info(),
                    to: ctx.accounts.recipient_token.to_account_info(),
                    authority: ctx.accounts.vault.to_account_info(),
                },
                signer,
            ),
            escrow.amount,
        )?;

        Ok(())
    }
}

#[derive(Accounts)]
pub struct CreateEscrow<'info> {
    #[account(
        init,
        payer = depositor,
        space = 8 + 32 + 32 + 8 + 8 + 1 + 1,
        seeds = [b"escrow", depositor.key().as_ref()],
        bump
    )]
    pub escrow: Account<'info, Escrow>,

    #[account(
        init,
        payer = depositor,
        token::mint = mint,
        token::authority = vault,
        seeds = [b"vault", depositor.key().as_ref()],
        bump
    )]
    pub vault: Account<'info, TokenAccount>,

    #[account(mut)]
    pub depositor_token: Account<'info, TokenAccount>,
    
    pub mint: Account<'info, token::Mint>,
    
    /// CHECK: Just storing the pubkey
    pub recipient: UncheckedAccount<'info>,

    #[account(mut)]
    pub depositor: Signer<'info>,
    
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Release<'info> {
    #[account(
        mut,
        seeds = [b"escrow", escrow.depositor.as_ref()],
        bump = escrow.bump,
        close = depositor
    )]
    pub escrow: Account<'info, Escrow>,

    #[account(
        mut,
        seeds = [b"vault", escrow.depositor.as_ref()],
        bump = escrow.vault_bump
    )]
    pub vault: Account<'info, TokenAccount>,

    #[account(
        mut,
        constraint = recipient_token.owner == escrow.recipient
    )]
    pub recipient_token: Account<'info, TokenAccount>,

    /// CHECK: Rent refund destination
    #[account(mut)]
    pub depositor: UncheckedAccount<'info>,

    pub token_program: Program<'info, Token>,
}

#[account]
pub struct Escrow {
    pub depositor: Pubkey,   // 32
    pub recipient: Pubkey,   // 32
    pub amount: u64,         // 8
    pub unlock_time: i64,    // 8
    pub bump: u8,            // 1
    pub vault_bump: u8,      // 1
}

#[error_code]
pub enum EscrowError {
    #[msg("Cannot release before unlock time")]
    TooEarly,
}
```

## PDA Signing Pattern

```rust
// The vault PDA signs the transfer
let seeds = &[
    b"vault",
    escrow.depositor.as_ref(),
    &[escrow.vault_bump],  // MUST include bump!
];
let signer = &[&seeds[..]];

token::transfer(
    CpiContext::new_with_signer(..., signer),
    amount,
)?;
```

**Always store and use the bump.** Recalculating can fail if the canonical bump wasn't found.

## Security Notes

1. **Store bumps** — Don't recalculate, store at creation
2. **Validate recipient** — Ensure tokens go to the right place
3. **Close accounts** — Reclaim rent when done (`close = depositor`)
4. **Time checks** — Use `Clock::get()?.unix_timestamp`

## Next

→ Challenge 4: Staking — Time-weighted rewards
