# Challenge 7: Oracle Integration (Pyth)

> Get real-world price data on-chain.

## Goal

Integrate Pyth price feeds to get reliable, manipulation-resistant price data.

## Why Oracles?

On-chain programs cannot access off-chain data. Oracles bridge this gap.

Never use DEX spot prices as oracles - they can be manipulated with flash loans.

## Pyth Network

Pyth provides high-fidelity price feeds from institutional sources:
- Sub-second updates
- Confidence intervals
- Multiple asset classes (crypto, forex, commodities)

## Setup

```toml
[dependencies]
pyth-sdk-solana = "0.10.0"
```

## Reading Price Feeds

```rust
use anchor_lang::prelude::*;
use pyth_sdk_solana::load_price_feed_from_account_info;

#[derive(Accounts)]
pub struct GetPrice<'info> {
    /// CHECK: Pyth price feed account
    pub price_feed: AccountInfo<'info>,
}

pub fn get_price(ctx: Context<GetPrice>) -> Result<i64> {
    let price_feed = load_price_feed_from_account_info(
        &ctx.accounts.price_feed
    ).map_err(|_| ErrorCode::InvalidPriceFeed)?;

    let current_price = price_feed
        .get_price_no_older_than(
            Clock::get()?.unix_timestamp,
            60  // Max age in seconds
        )
        .ok_or(ErrorCode::StalePrice)?;

    // Price is in fixed-point format
    // price.price is the value
    // price.expo is the exponent (usually negative)
    // actual_price = price.price * 10^price.expo

    msg!("Price: {} x 10^{}", current_price.price, current_price.expo);
    msg!("Confidence: +/- {}", current_price.conf);

    Ok(current_price.price)
}

#[error_code]
pub enum ErrorCode {
    #[msg("Invalid price feed")]
    InvalidPriceFeed,
    #[msg("Price is stale")]
    StalePrice,
}
```

## Price Feed Addresses

Mainnet feeds: https://pyth.network/developers/price-feed-ids

Common feeds:
```
SOL/USD:  H6ARHf6YXhGYeQfUzQNGk6rDNnLBQKrenN712K4AQJEG
BTC/USD:  GVXRSBjFk6e6J3NbVPXohDJetcTjaeeuykUpbQF8UoMU
ETH/USD:  JBu1AL4obBcCMqKBBxhpWCNUt136ijcuMZLFvTP7iWdB
USDC/USD: Gnt27xtC473ZT2Mw5u8wZ68Z3gULkSTb5DuxJy7eJotD
```

## Handling Price Data

```rust
pub fn use_price(ctx: Context<UsePrice>, amount: u64) -> Result<()> {
    let price_feed = load_price_feed_from_account_info(
        &ctx.accounts.price_feed
    )?;

    let price = price_feed
        .get_price_no_older_than(Clock::get()?.unix_timestamp, 60)
        .ok_or(ErrorCode::StalePrice)?;

    // Convert to usable format
    // Example: price.price = 12345, price.expo = -2
    // Means $123.45

    let price_in_cents: u64 = if price.expo >= 0 {
        (price.price as u64) * 10u64.pow(price.expo as u32)
    } else {
        (price.price as u64) / 10u64.pow((-price.expo) as u32)
    };

    // Use confidence interval for safety
    let confidence = price.conf;
    
    // Reject if confidence is too wide (>1% of price)
    require!(
        confidence * 100 < price.price.unsigned_abs(),
        ErrorCode::PriceTooUncertain
    );

    Ok(())
}
```

## TypeScript Client

```typescript
import { PythSolanaReceiver } from '@pythnetwork/pyth-solana-receiver';

const pythSolanaReceiver = new PythSolanaReceiver({
  connection,
  wallet,
});

// Get price feed account
const priceFeedAccount = pythSolanaReceiver.getPriceFeedAccountAddress(
  0, // shard
  'e62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43' // SOL/USD
);
```

## Best Practices

1. Always check staleness
```rust
get_price_no_older_than(timestamp, max_age_seconds)
```

2. Use confidence intervals
```rust
// Wider confidence = less reliable
if price.conf > acceptable_threshold {
    return Err(ErrorCode::PriceTooUncertain);
}
```

3. Handle negative exponents correctly
```rust
// Price is fixed-point: actual = price * 10^expo
// expo is usually -8 for crypto prices
```

4. Validate the price feed account
```rust
// Ensure it's the expected feed, not a fake
require!(
    ctx.accounts.price_feed.key() == EXPECTED_SOL_USD_FEED,
    ErrorCode::WrongPriceFeed
);
```

## Gotchas

1. Prices can be stale during network congestion
2. Confidence intervals widen during volatility
3. Different feeds have different update frequencies
4. Always validate the price feed pubkey
5. Handle the exponent correctly (usually negative)

## Next

Challenge 8: AMM Swap
