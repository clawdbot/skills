# Common Solana/Anchor Errors

## Account Errors

### "Account not found"
- Account doesn't exist or wasn't created
- Check the pubkey is correct
- Ensure `init` constraint was used for new accounts

### "Account already in use"
- Trying to init an account that already exists
- Use `init_if_needed` or check existence first

### "Insufficient funds for rent"
- Payer doesn't have enough SOL
- Airdrop more SOL: `solana airdrop 2`

### "Account data too small"
- Space calculation is wrong
- Add 8 bytes for discriminator
- Recalculate struct size

## Constraint Errors

### "A has_one constraint was violated"
- The stored pubkey doesn't match the provided account
- Check the account being passed matches what's stored

### "A seeds constraint was violated"
- PDA seeds don't match
- Verify seed values and order
- Check bump is correct

### "Signer check failed"
- Account should be signing but isn't
- Add account to `signers([...])` in client
- Verify wallet is connected

## Transaction Errors

### "Transaction simulation failed"
- Run with `--skip-preflight` to see actual error
- Check logs: `solana logs`

### "Blockhash not found"
- Transaction took too long
- Retry with fresh blockhash

### "Program failed to complete"
- Check program logs for panic message
- Look for integer overflow, unwrap on None, etc.

## Build Errors

### "Unresolved import"
```toml
# Add to Cargo.toml [dependencies]
anchor-lang = "0.30.0"
anchor-spl = "0.30.0"  # For SPL tokens
```

### "Type mismatch"
- BN in JS vs u64/i64 in Rust
- Use `new anchor.BN(value)` in TypeScript

## Debugging

```bash
# View program logs
solana logs

# Check account data
solana account <PUBKEY>

# Decode account with Anchor
anchor account <ACCOUNT_TYPE> <PUBKEY>

# Check transaction
solana confirm -v <TX_SIGNATURE>
```
