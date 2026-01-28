# Challenge 8: AMM Swap

> Build a constant product market maker.

## Goal

Create a simple AMM (Automated Market Maker) using the x*y=k formula.

## The Math

Constant product formula:
```
x * y = k

Where:
  x = reserve of token A
  y = reserve of token B
  k = constant (invariant)
```

When swapping:
```
(x + dx) * (y - dy) = k

Solving for dy:
dy = (y * dx) / (x + dx)
```

## Program Structure

```rust
use anchor_lang::prelude::*;
use anchor_spl::token::{self, Token, TokenAccount, Transfer};

declare_id!("YourProgramId");

#[program]
pub mod amm {
    use super::*;

    pub fn initialize_pool(ctx: Context<InitializePool>) -> Result<()> {
        let pool = &mut ctx.accounts.pool;
        pool.token_a_mint = ctx.accounts.token_a_mint.key();
        pool.token_b_mint = ctx.accounts.token_b_mint.key();
        pool.token_a_reserve = ctx.accounts.token_a_reserve.key();
        pool.token_b_reserve = ctx.accounts.token_b_reserve.key();
        pool.lp_mint = ctx.accounts.lp_mint.key();
        pool.bump = ctx.bumps.pool;
        Ok(())
    }

    pub fn add_liquidity(
        ctx: Context<AddLiquidity>,
        amount_a: u64,
        amount_b: u64,
    ) -> Result<()> {
        let pool = &ctx.accounts.pool;

        // Transfer tokens to reserves
        token::transfer(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.user_token_a.to_account_info(),
                    to: ctx.accounts.token_a_reserve.to_account_info(),
                    authority: ctx.accounts.user.to_account_info(),
                },
            ),
            amount_a,
        )?;

        token::transfer(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.user_token_b.to_account_info(),
                    to: ctx.accounts.token_b_reserve.to_account_info(),
                    authority: ctx.accounts.user.to_account_info(),
                },
            ),
            amount_b,
        )?;

        // Mint LP tokens
        // LP tokens = sqrt(amount_a * amount_b) for first deposit
        // Or proportional to existing reserves for subsequent
        let lp_amount = calculate_lp_tokens(
            amount_a,
            amount_b,
            ctx.accounts.token_a_reserve.amount,
            ctx.accounts.token_b_reserve.amount,
            ctx.accounts.lp_mint.supply,
        )?;

        let seeds = &[b"pool", pool.token_a_mint.as_ref(), pool.token_b_mint.as_ref(), &[pool.bump]];
        let signer = &[&seeds[..]];

        token::mint_to(
            CpiContext::new_with_signer(
                ctx.accounts.token_program.to_account_info(),
                token::MintTo {
                    mint: ctx.accounts.lp_mint.to_account_info(),
                    to: ctx.accounts.user_lp.to_account_info(),
                    authority: ctx.accounts.pool.to_account_info(),
                },
                signer,
            ),
            lp_amount,
        )?;

        Ok(())
    }

    pub fn swap(
        ctx: Context<Swap>,
        amount_in: u64,
        minimum_out: u64,
    ) -> Result<()> {
        let reserve_in = ctx.accounts.reserve_in.amount;
        let reserve_out = ctx.accounts.reserve_out.amount;

        // Calculate output: dy = (y * dx) / (x + dx)
        // With 0.3% fee: dx_after_fee = dx * 997 / 1000
        let amount_in_with_fee = (amount_in as u128)
            .checked_mul(997)
            .ok_or(ErrorCode::Overflow)?;
        
        let numerator = amount_in_with_fee
            .checked_mul(reserve_out as u128)
            .ok_or(ErrorCode::Overflow)?;
        
        let denominator = (reserve_in as u128)
            .checked_mul(1000)
            .ok_or(ErrorCode::Overflow)?
            .checked_add(amount_in_with_fee)
            .ok_or(ErrorCode::Overflow)?;
        
        let amount_out = numerator
            .checked_div(denominator)
            .ok_or(ErrorCode::DivisionByZero)? as u64;

        // Slippage check
        require!(amount_out >= minimum_out, ErrorCode::SlippageExceeded);

        // Transfer in
        token::transfer(
            CpiContext::new(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.user_token_in.to_account_info(),
                    to: ctx.accounts.reserve_in.to_account_info(),
                    authority: ctx.accounts.user.to_account_info(),
                },
            ),
            amount_in,
        )?;

        // Transfer out (PDA signs)
        let pool = &ctx.accounts.pool;
        let seeds = &[b"pool", pool.token_a_mint.as_ref(), pool.token_b_mint.as_ref(), &[pool.bump]];
        let signer = &[&seeds[..]];

        token::transfer(
            CpiContext::new_with_signer(
                ctx.accounts.token_program.to_account_info(),
                Transfer {
                    from: ctx.accounts.reserve_out.to_account_info(),
                    to: ctx.accounts.user_token_out.to_account_info(),
                    authority: ctx.accounts.pool.to_account_info(),
                },
                signer,
            ),
            amount_out,
        )?;

        Ok(())
    }
}

fn calculate_lp_tokens(
    amount_a: u64,
    amount_b: u64,
    reserve_a: u64,
    reserve_b: u64,
    lp_supply: u64,
) -> Result<u64> {
    if lp_supply == 0 {
        // First deposit: LP = sqrt(a * b)
        let product = (amount_a as u128)
            .checked_mul(amount_b as u128)
            .ok_or(ErrorCode::Overflow)?;
        Ok(integer_sqrt(product) as u64)
    } else {
        // Subsequent: proportional to smaller ratio
        let lp_a = (amount_a as u128)
            .checked_mul(lp_supply as u128)
            .ok_or(ErrorCode::Overflow)?
            .checked_div(reserve_a as u128)
            .ok_or(ErrorCode::DivisionByZero)?;
        
        let lp_b = (amount_b as u128)
            .checked_mul(lp_supply as u128)
            .ok_or(ErrorCode::Overflow)?
            .checked_div(reserve_b as u128)
            .ok_or(ErrorCode::DivisionByZero)?;
        
        Ok(std::cmp::min(lp_a, lp_b) as u64)
    }
}

fn integer_sqrt(n: u128) -> u128 {
    if n == 0 { return 0; }
    let mut x = n;
    let mut y = (x + 1) / 2;
    while y < x {
        x = y;
        y = (x + n / x) / 2;
    }
    x
}

#[account]
pub struct Pool {
    pub token_a_mint: Pubkey,
    pub token_b_mint: Pubkey,
    pub token_a_reserve: Pubkey,
    pub token_b_reserve: Pubkey,
    pub lp_mint: Pubkey,
    pub bump: u8,
}

#[error_code]
pub enum ErrorCode {
    #[msg("Overflow")]
    Overflow,
    #[msg("Division by zero")]
    DivisionByZero,
    #[msg("Slippage exceeded")]
    SlippageExceeded,
}
```

## Key Concepts

1. Constant product invariant must hold after every trade
2. LP tokens represent share of pool
3. Slippage protection is essential
4. Fees (0.3%) go to LP providers

## Price Impact

Larger trades = more price impact:
```
Small trade:  1 ETH for ~3000 USDC
Large trade:  100 ETH for ~290,000 USDC (not 300,000!)
```

The curve provides infinite liquidity but at increasingly worse prices.

## Gotchas

1. First depositor sets the price ratio
2. Use u128 for intermediate calculations to avoid overflow
3. Always implement slippage protection
4. LP token calculation differs for first vs subsequent deposits
5. Front-running is a real risk - use private mempools or slippage limits

## Next

Challenge 9: Blinks and Actions
