# Challenge 2: NFT with Metaplex

> Non-fungible tokens on Solana.

## Goal

Create an NFT with metadata using Metaplex standards. Understand the relationship between mint, metadata, and master edition accounts.

## Key Concepts

NFTs on Solana are SPL tokens with:
- Supply of 1
- 0 decimals
- Metadata account (name, symbol, URI)
- Master Edition account (proves uniqueness)

## Account Structure

```
Mint Account (SPL Token)
    |
    +-- Metadata Account (Metaplex)
    |       - name
    |       - symbol  
    |       - uri (points to JSON)
    |       - creators
    |       - seller_fee_basis_points
    |
    +-- Master Edition Account (Metaplex)
            - proves max supply = 1
            - enables prints (editions)
```

## Dependencies

```toml
[dependencies]
anchor-lang = "0.30.0"
anchor-spl = "0.30.0"
mpl-token-metadata = "4.1.2"
```

## Create NFT

```rust
use anchor_lang::prelude::*;
use anchor_spl::token::{Mint, Token, TokenAccount};
use mpl_token_metadata::{
    instructions::{CreateV1Builder, MintV1Builder},
    types::{Creator, TokenStandard},
};

#[derive(Accounts)]
pub struct CreateNft<'info> {
    #[account(
        init,
        payer = payer,
        mint::decimals = 0,
        mint::authority = payer,
        mint::freeze_authority = payer,
    )]
    pub mint: Account<'info, Mint>,

    #[account(
        init,
        payer = payer,
        associated_token::mint = mint,
        associated_token::authority = payer,
    )]
    pub token_account: Account<'info, TokenAccount>,

    /// CHECK: Validated by Metaplex
    #[account(mut)]
    pub metadata: UncheckedAccount<'info>,

    /// CHECK: Validated by Metaplex
    #[account(mut)]
    pub master_edition: UncheckedAccount<'info>,

    #[account(mut)]
    pub payer: Signer<'info>,

    pub token_program: Program<'info, Token>,
    pub system_program: Program<'info, System>,
    pub rent: Sysvar<'info, Rent>,

    /// CHECK: Metaplex program
    pub token_metadata_program: UncheckedAccount<'info>,
}

pub fn create_nft(
    ctx: Context<CreateNft>,
    name: String,
    symbol: String,
    uri: String,
) -> Result<()> {
    // Build create instruction
    let create_ix = CreateV1Builder::new()
        .metadata(ctx.accounts.metadata.key())
        .master_edition(Some(ctx.accounts.master_edition.key()))
        .mint(ctx.accounts.mint.key(), true)
        .authority(ctx.accounts.payer.key())
        .payer(ctx.accounts.payer.key())
        .update_authority(ctx.accounts.payer.key(), true)
        .name(name)
        .symbol(symbol)
        .uri(uri)
        .seller_fee_basis_points(500) // 5% royalty
        .token_standard(TokenStandard::NonFungible)
        .instruction();

    // Invoke Metaplex
    anchor_lang::solana_program::program::invoke(
        &create_ix,
        &[
            ctx.accounts.metadata.to_account_info(),
            ctx.accounts.master_edition.to_account_info(),
            ctx.accounts.mint.to_account_info(),
            ctx.accounts.payer.to_account_info(),
            ctx.accounts.system_program.to_account_info(),
        ],
    )?;

    // Mint 1 token
    let mint_ix = MintV1Builder::new()
        .token(ctx.accounts.token_account.key())
        .token_owner(Some(ctx.accounts.payer.key()))
        .metadata(ctx.accounts.metadata.key())
        .master_edition(Some(ctx.accounts.master_edition.key()))
        .mint(ctx.accounts.mint.key())
        .authority(ctx.accounts.payer.key())
        .payer(ctx.accounts.payer.key())
        .amount(1)
        .instruction();

    anchor_lang::solana_program::program::invoke(
        &mint_ix,
        &[
            ctx.accounts.token_account.to_account_info(),
            ctx.accounts.metadata.to_account_info(),
            ctx.accounts.master_edition.to_account_info(),
            ctx.accounts.mint.to_account_info(),
            ctx.accounts.payer.to_account_info(),
        ],
    )?;

    Ok(())
}
```

## Metadata JSON Format

The `uri` points to a JSON file:

```json
{
  "name": "My NFT #1",
  "symbol": "MNFT",
  "description": "A unique digital asset",
  "image": "https://arweave.net/xxx",
  "attributes": [
    { "trait_type": "Background", "value": "Blue" },
    { "trait_type": "Rarity", "value": "Rare" }
  ],
  "properties": {
    "files": [
      { "uri": "https://arweave.net/xxx", "type": "image/png" }
    ],
    "creators": [
      { "address": "...", "share": 100 }
    ]
  }
}
```

## PDA Derivation

Metadata and Master Edition are PDAs:

```rust
// Metadata PDA
seeds = ["metadata", token_metadata_program_id, mint]

// Master Edition PDA  
seeds = ["metadata", token_metadata_program_id, mint, "edition"]
```

## Using Metaplex CLI

```bash
# Install Sugar (Metaplex CLI)
bash <(curl -sSf https://sugar.metaplex.com/install.sh)

# Create collection
sugar launch

# Upload assets
sugar upload

# Deploy candy machine
sugar deploy
```

## Gotchas

1. Metadata account is a PDA owned by Metaplex, not your program
2. URI should point to immutable storage (Arweave, IPFS)
3. Royalties are enforced by marketplaces, not on-chain
4. Master Edition prevents additional minting

## Next

Challenge 3: PDA Escrow (already complete)
Challenge 4: Staking Program
