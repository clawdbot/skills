#!/usr/bin/env python3
"""
Solana Wallet Operations
Usage: python3 wallet.py <command> [args]

Commands:
  address                          Show wallet address
  balance [address]                Check SOL balance
  token-balance <mint> [--owner]   Check SPL token balance
  send <recipient> <amount>        Send SOL
  send-token <mint> <to> <amount>  Send SPL token
"""

import os
import sys
import argparse
from decimal import Decimal

try:
    import base58
    from solders.keypair import Keypair
    from solders.pubkey import Pubkey
    from solders.system_program import TransferParams, transfer
    from solders.transaction import Transaction
    from solders.message import Message
    from solana.rpc.api import Client
    from solana.rpc.commitment import Confirmed
    from solana.rpc.types import TxOpts, TokenAccountOpts
    from spl.token.client import Token
    from spl.token.constants import TOKEN_PROGRAM_ID, ASSOCIATED_TOKEN_PROGRAM_ID, TOKEN_2022_PROGRAM_ID
    from spl.token.instructions import get_associated_token_address, create_associated_token_account
except ImportError as e:
    print(f"Error: Required packages not installed. Missing: {e.name}")
    print("Run: pip install solana solders spl-token base58")
    sys.exit(1)


# Network RPC endpoints
NETWORKS = {
    "mainnet": "https://api.mainnet-beta.solana.com",
    "devnet": "https://api.devnet.solana.com",
    "testnet": "https://api.testnet.solana.com",
}

LAMPORTS_PER_SOL = 1_000_000_000


def get_keypair() -> Keypair:
    """Load keypair from environment variable."""
    private_key = os.environ.get("SOLANA_PRIVATE_KEY")
    
    if not private_key:
        print("Error: SOLANA_PRIVATE_KEY environment variable not set.")
        print("Run initialize.py first to create a wallet, then export the key:")
        print("  export SOLANA_PRIVATE_KEY=$(grep SOLANA_PRIVATE_KEY .env | cut -d '=' -f2)")
        sys.exit(1)
    
    try:
        # Decode base58 private key
        key_bytes = base58.b58decode(private_key)
        return Keypair.from_bytes(key_bytes)
    except Exception as e:
        print(f"Error: Invalid private key format: {e}")
        sys.exit(1)


def get_client(network: str = "mainnet") -> Client:
    """Get Solana RPC client."""
    rpc_url = os.environ.get("SOLANA_RPC_URL") or NETWORKS.get(network, NETWORKS["mainnet"])
    return Client(rpc_url)


def cmd_address(args):
    """Show wallet address."""
    keypair = get_keypair()
    print(f"◎ Wallet Address: {keypair.pubkey()}")


def cmd_balance(args):
    """Check SOL balance."""
    client = get_client(args.network)
    
    if args.address:
        try:
            pubkey = Pubkey.from_string(args.address)
        except Exception as e:
            print(f"Error: Invalid address: {e}")
            sys.exit(1)
    else:
        keypair = get_keypair()
        pubkey = keypair.pubkey()
    
    try:
        response = client.get_balance(pubkey, commitment=Confirmed)
        lamports = response.value
        sol = Decimal(lamports) / Decimal(LAMPORTS_PER_SOL)
        
        print(f"◎ Address: {pubkey}")
        print(f"◎ Balance: {sol:.9f} SOL")
        print(f"◎ Network: {args.network}")
    except Exception as e:
        print(f"Error fetching balance: {e}")
        sys.exit(1)


def cmd_token_balance(args):
    """Check SPL token balance."""
    client = get_client(args.network)
    
    try:
        mint_pubkey = Pubkey.from_string(args.mint)
    except Exception as e:
        print(f"Error: Invalid mint address: {e}")
        sys.exit(1)
    
    if args.owner:
        try:
            owner_pubkey = Pubkey.from_string(args.owner)
        except Exception as e:
            print(f"Error: Invalid owner address: {e}")
            sys.exit(1)
    else:
        keypair = get_keypair()
        owner_pubkey = keypair.pubkey()
    
    try:
        # Get token accounts by owner
        response = client.get_token_accounts_by_owner_json_parsed(
            owner_pubkey,
            TokenAccountOpts(mint=mint_pubkey),
            commitment=Confirmed
        )
        
        if response.value:
            for account in response.value:
                parsed = account.account.data.parsed
                info = parsed["info"]
                amount = info["tokenAmount"]
                
                print(f"◎ Token Mint: {args.mint}")
                print(f"◎ Owner: {owner_pubkey}")
                print(f"◎ Balance: {amount['uiAmountString']} ({amount['amount']} raw)")
                print(f"◎ Decimals: {amount['decimals']}")
                print(f"◎ Network: {args.network}")
        else:
            print(f"◎ Token Mint: {args.mint}")
            print(f"◎ Owner: {owner_pubkey}")
            print(f"◎ Balance: 0 (no token account)")
            print(f"◎ Network: {args.network}")
    except Exception as e:
        print(f"Error fetching token balance: {e}")
        sys.exit(1)


def cmd_send(args):
    """Send SOL to another wallet."""
    client = get_client(args.network)
    keypair = get_keypair()
    
    try:
        recipient = Pubkey.from_string(args.recipient)
    except Exception as e:
        print(f"Error: Invalid recipient address: {e}")
        sys.exit(1)
    
    try:
        amount_sol = Decimal(args.amount)
        if amount_sol <= 0:
            print("Error: Amount must be positive")
            sys.exit(1)
        lamports = int(amount_sol * LAMPORTS_PER_SOL)
    except Exception as e:
        print(f"Error: Invalid amount: {e}")
        sys.exit(1)
    
    print(f"◎ Sending {amount_sol} SOL...")
    print(f"  From: {keypair.pubkey()}")
    print(f"  To: {recipient}")
    print(f"  Network: {args.network}")
    
    try:
        # Get recent blockhash
        blockhash_resp = client.get_latest_blockhash(commitment=Confirmed)
        recent_blockhash = blockhash_resp.value.blockhash
        
        # Create transfer instruction
        transfer_ix = transfer(
            TransferParams(
                from_pubkey=keypair.pubkey(),
                to_pubkey=recipient,
                lamports=lamports
            )
        )
        
        # Create, sign and send transaction using VersionedTransaction
        from solders.transaction import VersionedTransaction
        from solders.message import MessageV0
        
        msg = MessageV0.try_compile(
            payer=keypair.pubkey(),
            instructions=[transfer_ix],
            address_lookup_table_accounts=[],
            recent_blockhash=recent_blockhash,
        )
        tx = VersionedTransaction(msg, [keypair])
        
        # Send transaction (skip preflight to avoid blockhash timing issues)
        opts = TxOpts(skip_preflight=True, preflight_commitment=Confirmed)
        result = client.send_transaction(tx, opts=opts)
        signature = result.value
        
        print(f"\n✅ Transaction sent!")
        print(f"◎ Signature: {signature}")
        print(f"◎ Explorer: https://solscan.io/tx/{signature}" + ("?cluster=devnet" if args.network == "devnet" else ""))
        
    except Exception as e:
        print(f"\n❌ Transaction failed: {e}")
        sys.exit(1)


def cmd_send_token(args):
    """Send SPL token to another wallet."""
    from solders.transaction import VersionedTransaction
    from solders.message import MessageV0
    from spl.token.instructions import transfer_checked, TransferCheckedParams
    
    client = get_client(args.network)
    keypair = get_keypair()
    
    try:
        mint_pubkey = Pubkey.from_string(args.mint)
    except Exception as e:
        print(f"Error: Invalid mint address: {e}")
        sys.exit(1)
    
    try:
        recipient = Pubkey.from_string(args.recipient)
    except Exception as e:
        print(f"Error: Invalid recipient address: {e}")
        sys.exit(1)
    
    try:
        amount = Decimal(args.amount)
        if amount <= 0:
            print("Error: Amount must be positive")
            sys.exit(1)
    except Exception as e:
        print(f"Error: Invalid amount: {e}")
        sys.exit(1)
    
    print(f"◎ Sending {amount} tokens...")
    print(f"  Token: {mint_pubkey}")
    print(f"  From: {keypair.pubkey()}")
    print(f"  To: {recipient}")
    print(f"  Network: {args.network}")
    
    try:
        # Get mint account to determine token program (Token vs Token-2022)
        mint_account = client.get_account_info(mint_pubkey, commitment=Confirmed)
        if not mint_account.value:
            print("Error: Token mint not found")
            sys.exit(1)
        
        # Detect token program from mint account owner
        mint_owner = mint_account.value.owner
        if mint_owner == TOKEN_2022_PROGRAM_ID:
            token_program_id = TOKEN_2022_PROGRAM_ID
            print("  Token type: Token-2022")
        else:
            token_program_id = TOKEN_PROGRAM_ID
            print("  Token type: SPL Token")
        
        # Get mint info for decimals
        mint_info = client.get_account_info_json_parsed(mint_pubkey, commitment=Confirmed)
        decimals = mint_info.value.data.parsed["info"]["decimals"]
        
        # Convert amount to raw units
        raw_amount = int(amount * (10 ** decimals))
        
        # Find sender's token account for this mint
        source_accounts = client.get_token_accounts_by_owner_json_parsed(
            keypair.pubkey(),
            TokenAccountOpts(mint=mint_pubkey, program_id=token_program_id),
            commitment=Confirmed
        )
        
        if not source_accounts.value:
            print("Error: You don't have a token account for this token")
            sys.exit(1)
        
        # Use the first token account found (could be ATA or regular)
        source_ata = source_accounts.value[0].pubkey
        
        # Get destination ATA (recipient's token account) - with correct program ID
        dest_ata = get_associated_token_address(recipient, mint_pubkey, token_program_id)
        
        # Check if destination ATA exists
        dest_info = client.get_account_info(dest_ata, commitment=Confirmed)
        
        # Build instructions
        instructions = []
        
        # If dest ATA doesn't exist, create it
        if not dest_info.value:
            print("  Creating token account for recipient...")
            create_ata_ix = create_associated_token_account(
                payer=keypair.pubkey(),
                owner=recipient,
                mint=mint_pubkey,
                token_program_id=token_program_id
            )
            instructions.append(create_ata_ix)
        
        # Add transfer instruction
        transfer_ix = transfer_checked(
            TransferCheckedParams(
                program_id=token_program_id,
                source=source_ata,
                mint=mint_pubkey,
                dest=dest_ata,
                owner=keypair.pubkey(),
                amount=raw_amount,
                decimals=decimals
            )
        )
        instructions.append(transfer_ix)
        
        # Get recent blockhash
        blockhash_resp = client.get_latest_blockhash(commitment=Confirmed)
        recent_blockhash = blockhash_resp.value.blockhash
        
        # Create, sign and send transaction
        msg = MessageV0.try_compile(
            payer=keypair.pubkey(),
            instructions=instructions,
            address_lookup_table_accounts=[],
            recent_blockhash=recent_blockhash,
        )
        tx = VersionedTransaction(msg, [keypair])
        
        # Send transaction
        opts = TxOpts(skip_preflight=True, preflight_commitment=Confirmed)
        result = client.send_transaction(tx, opts=opts)
        signature = result.value
        
        print(f"\n✅ Token transfer sent!")
        print(f"◎ Signature: {signature}")
        print(f"◎ Explorer: https://solscan.io/tx/{signature}" + ("?cluster=devnet" if args.network == "devnet" else ""))
        
    except Exception as e:
        print(f"\n❌ Transaction failed: {e}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="Solana Wallet Operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  wallet.py address                     Show your wallet address
  wallet.py balance                     Check SOL balance
  wallet.py balance <address>           Check another wallet's balance
  wallet.py token-balance <mint>        Check token balance
  wallet.py send <recipient> 0.1        Send 0.1 SOL
  wallet.py send-token <mint> <to> 10   Send 10 tokens
        """
    )
    
    parser.add_argument(
        "--network", "-n",
        choices=["mainnet", "devnet", "testnet"],
        default="mainnet",
        help="Solana network (default: mainnet)"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # address command
    addr_parser = subparsers.add_parser("address", help="Show wallet address")
    addr_parser.set_defaults(func=cmd_address)
    
    # balance command
    bal_parser = subparsers.add_parser("balance", help="Check SOL balance")
    bal_parser.add_argument("address", nargs="?", help="Address to check (default: your wallet)")
    bal_parser.set_defaults(func=cmd_balance)
    
    # token-balance command
    tok_parser = subparsers.add_parser("token-balance", help="Check SPL token balance")
    tok_parser.add_argument("mint", help="Token mint address")
    tok_parser.add_argument("--owner", "-o", help="Owner address (default: your wallet)")
    tok_parser.set_defaults(func=cmd_token_balance)
    
    # send command
    send_parser = subparsers.add_parser("send", help="Send SOL")
    send_parser.add_argument("recipient", help="Recipient address")
    send_parser.add_argument("amount", help="Amount in SOL")
    send_parser.set_defaults(func=cmd_send)
    
    # send-token command
    send_tok_parser = subparsers.add_parser("send-token", help="Send SPL token")
    send_tok_parser.add_argument("mint", help="Token mint address")
    send_tok_parser.add_argument("recipient", help="Recipient address")
    send_tok_parser.add_argument("amount", help="Amount of tokens")
    send_tok_parser.set_defaults(func=cmd_send_token)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    args.func(args)


if __name__ == "__main__":
    main()
