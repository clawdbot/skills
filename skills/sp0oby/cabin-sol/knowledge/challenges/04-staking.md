# Challenge 4: Staking Program

> Lock tokens, earn rewards over time.

## Goal

Build a staking program where users deposit tokens and earn rewards proportional to time staked.

## Key Concepts

- Time-weighted rewards
- Reward rate calculation
- Deposit and withdrawal mechanics
- Claiming accrued rewards

## The Math

```
rewards = staked_amount * time_staked * reward_rate
```

Common approach: track `reward_per_token_stored` globally, update on each action.

## Program Structure

```rust
use anchor_lang::prelude::*;
use anchor_spl::token::{self, Token, TokenAccount, Transfer};

declare_id!("YourProgramId");

#[program]
pub mod staking {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>, reward_rate: u64) -> Result<()> {
        let pool = &mut ctx.accounts.pool;
        pool.authority = ctx.accounts.authority.key();
        pool.staking_mint = ctx.accounts.staking_mint.key();
        pool.reward_mint = ctx.accounts.reward_mint.key();
        pool.reward_rate = reward_rate;
        pool.last_update_time = Clock::get()?.unix_timestamp;
        pool.reward_per_token_stored = 0;
        pool.total_staked = 0;
        pool.bump = ctx.bumps.pool;
        Ok(())
    }

    pub fn stake(ctx: Context<Stake>, amount: u64) -> Result<()> {
        let pool = &mut ctx.accounts.pool;
        let user = &mut ctx.accounts.user_stake;

        // Update rewards before changing state
        update_rewards(pool, user)?;

        // Transfer tokens to vault
        token::transfer(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.user_token.to_account_info(),
                    to: ctx.accounts.vault.to_account_info(),
                    authority: ctx.accounts.owner.to_account_info(),
                },
            ),
            amount,
        )?;

        // Update state
        user.staked_amount = user.staked_amount.checked_add(amount)
            .ok_or(ErrorCode::Overflow)?;
        pool.total_staked = pool.total_staked.checked_add(amount)
            .ok_or(ErrorCode::Overflow)?;

        Ok(())
    }

    pub fn unstake(ctx: Context<Unstake>, amount: u64) -> Result<()> {
        let pool = &mut ctx.accounts.pool;
        let user = &mut ctx.accounts.user_stake;

        require!(user.staked_amount >= amount, ErrorCode::InsufficientStake);

        // Update rewards before changing state
        update_rewards(pool, user)?;

        // Transfer from vault to user
        let seeds = &[b"vault", pool.key().as_ref(), &[pool.vault_bump]];
        let signer = &[&seeds[..]];

        token::transfer(
            CpiContext::new_with_signer(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.vault.to_account_info(),
                    to: ctx.accounts.user_token.to_account_info(),
                    authority: ctx.accounts.vault.to_account_info(),
                },
                signer,
            ),
            amount,
        )?;

        // Update state
        user.staked_amount = user.staked_amount.checked_sub(amount)
            .ok_or(ErrorCode::Underflow)?;
        pool.total_staked = pool.total_staked.checked_sub(amount)
            .ok_or(ErrorCode::Underflow)?;

        Ok(())
    }

    pub fn claim(ctx: Context<Claim>) -> Result<()> {
        let pool = &mut ctx.accounts.pool;
        let user = &mut ctx.accounts.user_stake;

        update_rewards(pool, user)?;

        let reward = user.rewards_earned;
        require!(reward > 0, ErrorCode::NoRewards);

        user.rewards_earned = 0;

        // Transfer rewards
        let seeds = &[b"reward_vault", pool.key().as_ref(), &[pool.reward_vault_bump]];
        let signer = &[&seeds[..]];

        token::transfer(
            CpiContext::new_with_signer(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.reward_vault.to_account_info(),
                    to: ctx.accounts.user_reward_token.to_account_info(),
                    authority: ctx.accounts.reward_vault.to_account_info(),
                },
                signer,
            ),
            reward,
        )?;

        Ok(())
    }
}

fn update_rewards(pool: &mut Account<Pool>, user: &mut Account<UserStake>) -> Result<()> {
    let current_time = Clock::get()?.unix_timestamp;
    
    if pool.total_staked > 0 {
        let time_elapsed = current_time.checked_sub(pool.last_update_time)
            .ok_or(ErrorCode::Overflow)? as u64;
        
        let reward_per_token_delta = time_elapsed
            .checked_mul(pool.reward_rate)
            .ok_or(ErrorCode::Overflow)?
            .checked_mul(1_000_000_000) // Scale for precision
            .ok_or(ErrorCode::Overflow)?
            .checked_div(pool.total_staked)
            .ok_or(ErrorCode::DivisionByZero)?;
        
        pool.reward_per_token_stored = pool.reward_per_token_stored
            .checked_add(reward_per_token_delta)
            .ok_or(ErrorCode::Overflow)?;
    }

    pool.last_update_time = current_time;

    // Update user rewards
    let pending = user.staked_amount
        .checked_mul(pool.reward_per_token_stored.checked_sub(user.reward_per_token_paid).ok_or(ErrorCode::Underflow)?)
        .ok_or(ErrorCode::Overflow)?
        .checked_div(1_000_000_000)
        .ok_or(ErrorCode::DivisionByZero)?;

    user.rewards_earned = user.rewards_earned.checked_add(pending).ok_or(ErrorCode::Overflow)?;
    user.reward_per_token_paid = pool.reward_per_token_stored;

    Ok(())
}

#[account]
pub struct Pool {
    pub authority: Pubkey,
    pub staking_mint: Pubkey,
    pub reward_mint: Pubkey,
    pub reward_rate: u64,
    pub last_update_time: i64,
    pub reward_per_token_stored: u64,
    pub total_staked: u64,
    pub bump: u8,
    pub vault_bump: u8,
    pub reward_vault_bump: u8,
}

#[account]
pub struct UserStake {
    pub owner: Pubkey,
    pub pool: Pubkey,
    pub staked_amount: u64,
    pub reward_per_token_paid: u64,
    pub rewards_earned: u64,
    pub bump: u8,
}

#[error_code]
pub enum ErrorCode {
    #[msg("Overflow")]
    Overflow,
    #[msg("Underflow")]
    Underflow,
    #[msg("Division by zero")]
    DivisionByZero,
    #[msg("Insufficient stake")]
    InsufficientStake,
    #[msg("No rewards to claim")]
    NoRewards,
}
```

## Account Contexts (Abbreviated)

```rust
#[derive(Accounts)]
pub struct Stake<'info> {
    #[account(mut, seeds = [b"pool", pool.staking_mint.as_ref()], bump = pool.bump)]
    pub pool: Account<'info, Pool>,
    
    #[account(
        init_if_needed,
        payer = owner,
        space = 8 + 32 + 32 + 8 + 8 + 8 + 1,
        seeds = [b"user", pool.key().as_ref(), owner.key().as_ref()],
        bump
    )]
    pub user_stake: Account<'info, UserStake>,
    
    #[account(mut)]
    pub vault: Account<'info, TokenAccount>,
    
    #[account(mut)]
    pub user_token: Account<'info, TokenAccount>,
    
    #[account(mut)]
    pub owner: Signer<'info>,
    
    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
}
```

## Key Points

1. Always update rewards BEFORE changing staked amounts
2. Use scaled integers for precision (multiply by 1e9, divide later)
3. Handle the zero-staked case (avoid division by zero)
4. Store all bumps to avoid recalculation

## Gotchas

- Reward calculation must happen before any state change
- Integer division loses precision - scale up first
- Time-based rewards need `Clock::get()?`
- Ensure reward vault has sufficient tokens

## Next

Challenge 5: Token-2022
