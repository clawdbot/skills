# Challenge 0: Hello Solana

> *Your first program. Welcome to the forest.*

## Goal

Build an Anchor program that stores a message. Learn how accounts work by doing.

## What You'll Learn

- Programs are stateless (data lives in accounts)
- Account creation and ownership
- PDA derivation
- Anchor's constraint system

## Setup

```bash
anchor init hello_cabin
cd hello_cabin
solana-test-validator  # Terminal 1
anchor build && anchor test  # Terminal 2
```

## The Program

```rust
use anchor_lang::prelude::*;

declare_id!("YourProgramId");

#[program]
pub mod hello_cabin {
    use super::*;

    pub fn initialize(ctx: Context<Initialize>, message: String) -> Result<()> {
        let cabin = &mut ctx.accounts.cabin;
        cabin.message = message;
        cabin.owner = ctx.accounts.owner.key();
        cabin.bump = ctx.bumps.cabin;
        Ok(())
    }

    pub fn update(ctx: Context<Update>, message: String) -> Result<()> {
        ctx.accounts.cabin.message = message;
        Ok(())
    }
}

#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(
        init,
        payer = owner,
        space = 8 + 32 + 4 + 280 + 1,
        seeds = [b"cabin", owner.key().as_ref()],
        bump
    )]
    pub cabin: Account<'info, Cabin>,
    #[account(mut)]
    pub owner: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct Update<'info> {
    #[account(
        mut,
        seeds = [b"cabin", owner.key().as_ref()],
        bump = cabin.bump,
        has_one = owner
    )]
    pub cabin: Account<'info, Cabin>,
    pub owner: Signer<'info>,
}

#[account]
pub struct Cabin {
    pub owner: Pubkey,      // 32 bytes
    pub message: String,    // 4 + 280 bytes
    pub bump: u8,           // 1 byte
}
```

## Space Breakdown

```
8   discriminator (Anchor adds this)
32  owner (Pubkey)
4   message length prefix
280 message content (max)
1   bump
---
325 total bytes
```

**Never forget the 8-byte discriminator.**

## The Test

```typescript
import * as anchor from "@coral-xyz/anchor";
import { Program } from "@coral-xyz/anchor";
import { HelloCabin } from "../target/types/hello_cabin";
import { expect } from "chai";

describe("hello_cabin", () => {
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);
  const program = anchor.workspace.HelloCabin as Program<HelloCabin>;

  const [cabinPda] = anchor.web3.PublicKey.findProgramAddressSync(
    [Buffer.from("cabin"), provider.wallet.publicKey.toBuffer()],
    program.programId
  );

  it("creates a cabin", async () => {
    await program.methods
      .initialize("The forest does not have a sell button")
      .accounts({
        cabin: cabinPda,
        owner: provider.wallet.publicKey,
        systemProgram: anchor.web3.SystemProgram.programId,
      })
      .rpc();

    const cabin = await program.account.cabin.fetch(cabinPda);
    expect(cabin.message).to.equal("The forest does not have a sell button");
  });

  it("updates the message", async () => {
    await program.methods
      .update("Return to primitive computing")
      .accounts({
        cabin: cabinPda,
        owner: provider.wallet.publicKey,
      })
      .rpc();

    const cabin = await program.account.cabin.fetch(cabinPda);
    expect(cabin.message).to.equal("Return to primitive computing");
  });
});
```

## Key Takeaways

1. **Data lives in accounts**, not in the program
2. **PDAs** are deterministic addresses your program controls
3. **Space must be pre-allocated** — you can't resize easily
4. **Anchor validates** constraints automatically

## Next

→ Challenge 1: SPL Token — Create fungible tokens
