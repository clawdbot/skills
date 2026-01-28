# Account Space Calculation

## Always Include Discriminator

Anchor uses an 8-byte discriminator at the start of every account. This is the SHA256 hash of the account name.

```
Total Space = 8 (discriminator) + your data
```

## Type Sizes

| Type | Size (bytes) |
|------|--------------|
| bool | 1 |
| u8 / i8 | 1 |
| u16 / i16 | 2 |
| u32 / i32 | 4 |
| u64 / i64 | 8 |
| u128 / i128 | 16 |
| Pubkey | 32 |
| Option<T> | 1 + size(T) |
| Vec<T> | 4 + (n * size(T)) |
| String | 4 + length |
| [T; n] | n * size(T) |

## Examples

```rust
// Simple struct: 8 + 8 + 32 = 48 bytes
#[account]
pub struct Counter {
    pub count: u64,      // 8 bytes
    pub authority: Pubkey, // 32 bytes
}

// With optional: 8 + 8 + 32 + (1 + 32) = 81 bytes
#[account]
pub struct WithOption {
    pub count: u64,
    pub authority: Pubkey,
    pub delegate: Option<Pubkey>,
}

// With vec (max 10 items): 8 + 4 + (10 * 32) = 332 bytes
#[account]
pub struct WithVec {
    pub owners: Vec<Pubkey>,  // Must allocate max size upfront
}
```

## Using INIT_SPACE Macro

```rust
use anchor_lang::prelude::*;

#[account]
#[derive(InitSpace)]  // Automatically calculates space
pub struct MyAccount {
    pub count: u64,
    pub authority: Pubkey,
    #[max_len(50)]  // Required for String/Vec
    pub name: String,
}

// Then use:
#[account(init, payer = payer, space = 8 + MyAccount::INIT_SPACE)]
pub my_account: Account<'info, MyAccount>,
```
