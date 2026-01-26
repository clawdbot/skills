#!/usr/bin/env python3
"""
Jupiter Swap Operations
Usage: python3 jup_swap.py <command> [args]

Commands:
  quote <input_mint> <output_mint> <amount>   Get swap quote
  swap <input_mint> <output_mint> <amount>    Execute swap
"""

import os
import sys
import asyncio
import argparse
import base64
from decimal import Decimal
from typing import Optional, Dict, Any

try:
    import aiohttp
    import base58
    from solders.keypair import Keypair
    from solders.pubkey import Pubkey
    from solders.transaction import VersionedTransaction
except ImportError as e:
    print(f"Error: Required packages not installed. Missing: {e.name}")
    print("Run: pip install solana solders base58 aiohttp")
    sys.exit(1)


# Jupiter Ultra API
JUPITER_ULTRA_API_URL = os.environ.get(
    "JUPITER_API_URL", "https://api.jup.ag/ultra/v1")

# Common token mints
TOKENS = {
    # Native
    "SOL": "So11111111111111111111111111111111111111112",
    # Stablecoins
    "USDC": "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
    "USDT": "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB",
    "PYUSD": "2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo",
    "USDS": "USDSwr9ApdHk5bvJKMjzff41FfuX8bSxdKcR81vTwcA",
    "USDG": "2u1tszSeqZ3qBWF3uNGPFc8TzMk2tdiwknnRMWGWjGWH",
    "USD1": "USD1ttGY1N17NEEHLmELoaybftRBUSErhqYiQzvEmuB",
    "CASH": "CASHx9KJUStyftLFWGvEVf59SGeG9sh5FfcnZMVPCASH",
    # Wrapped assets
    "ETH": "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs",
    "CBBTC": "cbbtcf3aa214zXHbiAZQwf4122FBYbraNdFqgw4iMij",
    # LST
    "JITOSOL": "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn",
    # DeFi
    "JUP": "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN",
    "JLP": "27G8MtK7VtTcCHkpASjSDdkWWYfoqT6ggEuKidVJidD4",
    "RAY": "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R",
    "PYTH": "HZ1JovNiVvGrGNiiYvEozEVgZ58xaU3RKwX8eACQBCt3",
    # Memes
    "PUMP": "pumpCmXqMfrsAkQ5r49WcJnRayYRqmXz6ae8H7H9Dfn",
    "BONK": "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263",
    "FARTCOIN": "9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump",
    "TRUMP": "6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN",
}

# Token decimals (for display)
TOKEN_DECIMALS = {
    "So11111111111111111111111111111111111111112": 9,   # SOL
    "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": 6,  # USDC
    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": 6,  # USDT
    "2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo": 6,  # PYUSD
    "USDSwr9ApdHk5bvJKMjzff41FfuX8bSxdKcR81vTwcA": 6,   # USDS
    "2u1tszSeqZ3qBWF3uNGPFc8TzMk2tdiwknnRMWGWjGWH": 6,  # USDG
    "USD1ttGY1N17NEEHLmELoaybftRBUSErhqYiQzvEmuB": 6,   # USD1
    "CASHx9KJUStyftLFWGvEVf59SGeG9sh5FfcnZMVPCASH": 6,  # CASH
    "7vfCXTUXx5WJV5JADk17DUJ4ksgau7utNKj4b963voxs": 8,  # ETH
    "cbbtcf3aa214zXHbiAZQwf4122FBYbraNdFqgw4iMij": 8,   # cbBTC
    "J1toso1uCk3RLmjorhTtrVwY9HJ7X8V9yYac6Y7kGCPn": 9,  # JitoSOL
    "JUPyiwrYJFskUPiHa7hkeR8VUtAeFoSYbKedZNsDvCN": 6,   # JUP
    "27G8MtK7VtTcCHkpASjSDdkWWYfoqT6ggEuKidVJidD4": 6,  # JLP
    "4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R": 6,  # RAY
    "HZ1JovNiVvGrGNiiYvEozEVgZ58xaU3RKwX8eACQBCt3": 6,  # PYTH
    "pumpCmXqMfrsAkQ5r49WcJnRayYRqmXz6ae8H7H9Dfn": 6,   # PUMP
    "DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263": 5,  # BONK
    "9BB6NFEcjBCtnNLFko2FqVQBq8HHM13kCyYcdQbgpump": 6,  # Fartcoin
    "6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN": 6,  # TRUMP
}


def check_api_key() -> str:
    """Check Jupiter API key is set."""
    api_key = os.environ.get("JUPITER_API_KEY")
    if not api_key:
        print("Error: JUPITER_API_KEY environment variable not set.")
        print("Get your API key from https://portal.jup.ag/ and export it:")
        print("  export JUPITER_API_KEY=your_api_key_here")
        sys.exit(1)
    return api_key


def get_keypair() -> Keypair:
    """Load keypair from environment variable."""
    private_key = os.environ.get("SOLANA_PRIVATE_KEY")

    if not private_key:
        print("Error: SOLANA_PRIVATE_KEY environment variable not set.")
        print("Run initialize.py first to create a wallet, then export the key:")
        print(
            "  export SOLANA_PRIVATE_KEY=$(grep SOLANA_PRIVATE_KEY .env | cut -d '=' -f2)")
        sys.exit(1)

    try:
        key_bytes = base58.b58decode(private_key)
        return Keypair.from_bytes(key_bytes)
    except Exception as e:
        print(f"Error: Invalid private key format: {e}")
        sys.exit(1)


def resolve_mint(mint_or_symbol: str) -> str:
    """Resolve token symbol to mint address."""
    upper = mint_or_symbol.upper()
    if upper in TOKENS:
        return TOKENS[upper]
    return mint_or_symbol


def get_token_name(mint: str) -> str:
    """Get token symbol from mint address."""
    for symbol, address in TOKENS.items():
        if address == mint:
            return symbol
    return mint[:8] + "..."


def format_amount(amount: int, mint: str) -> str:
    """Format raw amount to human-readable."""
    decimals = TOKEN_DECIMALS.get(mint, 9)
    value = Decimal(amount) / Decimal(10 ** decimals)
    return f"{value:.{decimals}f}".rstrip('0').rstrip('.')


def parse_amount(amount: str, mint: str) -> int:
    """Parse human-readable amount to raw units."""
    decimals = TOKEN_DECIMALS.get(mint, 9)
    value = Decimal(amount)
    return int(value * Decimal(10 ** decimals))


async def get_quote(
    input_mint: str,
    output_mint: str,
    amount: int,
    taker: str
) -> Optional[Dict[str, Any]]:
    """Get swap quote from Jupiter Ultra API."""
    api_key = check_api_key()

    headers = {
        "Accept": "application/json",
        "x-api-key": api_key,
    }

    params = {
        "inputMint": input_mint,
        "outputMint": output_mint,
        "amount": str(amount),
        "taker": taker,
        "swapMode": "ExactIn",
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{JUPITER_ULTRA_API_URL}/order",
                params=params,
                headers=headers
            ) as response:
                if response.status != 200:
                    error_data = await response.text()
                    print(
                        f"Error: Jupiter API error ({response.status}): {error_data}")
                    return None

                data = await response.json()

                if data.get('error') or data.get('errorMessage'):
                    print(
                        f"Error: {data.get('error') or data.get('errorMessage')}")
                    return None

                return data
    except Exception as e:
        print(f"Error: Failed to get quote: {e}")
        return None


async def execute_swap(
    signed_tx: VersionedTransaction,
    request_id: str
) -> Optional[Dict[str, Any]]:
    """Execute signed transaction via Jupiter Ultra API."""
    api_key = check_api_key()

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "x-api-key": api_key,
    }

    serialized_tx = base64.b64encode(bytes(signed_tx)).decode('utf-8')

    payload = {
        "signedTransaction": serialized_tx,
        "requestId": request_id
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{JUPITER_ULTRA_API_URL}/execute",
                json=payload,
                headers=headers
            ) as response:
                if response.status != 200:
                    error_data = await response.text()
                    print(
                        f"Error: Execute failed ({response.status}): {error_data}")
                    return None

                result = await response.json()
                return result
    except Exception as e:
        print(f"Error: Failed to execute: {e}")
        return None


def cmd_quote(args):
    """Get swap quote."""
    input_mint = resolve_mint(args.input_mint)
    output_mint = resolve_mint(args.output_mint)

    # Parse amount
    amount = parse_amount(args.amount, input_mint)

    # Need a taker address for quote
    keypair = get_keypair()
    taker = str(keypair.pubkey())

    print(f"◎ Getting quote...")
    print(f"  Input: {get_token_name(input_mint)}")
    print(f"  Output: {get_token_name(output_mint)}")
    print(f"  Amount: {args.amount}")

    result = asyncio.run(get_quote(input_mint, output_mint, amount, taker))

    if not result:
        sys.exit(1)

    in_amount = int(result.get("inAmount", 0))
    out_amount = int(result.get("outAmount", 0))
    price_impact = result.get("priceImpactPct", "0")

    print(f"\n◎ Quote:")
    print(
        f"  You pay: {format_amount(in_amount, input_mint)} {get_token_name(input_mint)}")
    print(
        f"  You get: {format_amount(out_amount, output_mint)} {get_token_name(output_mint)}")
    print(f"  Price impact: {price_impact}%")
    print(f"  Router: {result.get('router', 'N/A')}")

    # Calculate rate
    if in_amount > 0 and out_amount > 0:
        in_dec = TOKEN_DECIMALS.get(input_mint, 9)
        out_dec = TOKEN_DECIMALS.get(output_mint, 9)
        rate = (Decimal(out_amount) / Decimal(10 ** out_dec)) / \
            (Decimal(in_amount) / Decimal(10 ** in_dec))
        print(
            f"  Rate: 1 {get_token_name(input_mint)} = {rate:.6f} {get_token_name(output_mint)}")


def cmd_swap(args):
    """Execute swap."""
    input_mint = resolve_mint(args.input_mint)
    output_mint = resolve_mint(args.output_mint)

    # Parse amount
    amount = parse_amount(args.amount, input_mint)

    keypair = get_keypair()
    taker = str(keypair.pubkey())

    print(f"◎ Preparing swap...")
    print(f"  From: {keypair.pubkey()}")
    print(f"  Input: {args.amount} {get_token_name(input_mint)}")
    print(f"  Output: {get_token_name(output_mint)}")

    # Get quote and transaction
    result = asyncio.run(get_quote(input_mint, output_mint, amount, taker))

    if not result:
        sys.exit(1)

    if not result.get("transaction"):
        print("Error: No transaction returned from API")
        sys.exit(1)

    out_amount = int(result.get("outAmount", 0))
    price_impact = result.get("priceImpactPct", "0")
    request_id = result.get("requestId")

    print(f"\n◎ Quote:")
    print(
        f"  You get: ~{format_amount(out_amount, output_mint)} {get_token_name(output_mint)}")
    print(f"  Price impact: {price_impact}%")

    # Decode and sign transaction
    try:
        tx_bytes = base64.b64decode(result["transaction"])
        unsigned_tx = VersionedTransaction.from_bytes(tx_bytes)
        signed_tx = VersionedTransaction(unsigned_tx.message, [keypair])
    except Exception as e:
        print(f"Error: Failed to sign transaction: {e}")
        sys.exit(1)

    print("\n◎ Executing swap...")

    # Execute via Jupiter API
    exec_result = asyncio.run(execute_swap(signed_tx, request_id))

    if exec_result and exec_result.get("status") == "Success":
        signature = exec_result.get("signature")
        print(f"\n✅ Swap successful!")
        print(f"◎ Signature: {signature}")
        print(f"◎ Explorer: https://solscan.io/tx/{signature}")
    else:
        error = exec_result.get("error") if exec_result else "Unknown error"
        print(f"\n❌ Swap failed: {error}")
        sys.exit(1)


def cmd_tokens(args):
    """List known tokens."""
    print("◎ Known Tokens:\n")
    print(f"  {'Symbol':<8} {'Mint Address':<50} {'Decimals'}")
    print(f"  {'-'*8} {'-'*50} {'-'*8}")
    for symbol, mint in TOKENS.items():
        decimals = TOKEN_DECIMALS.get(mint, "?")
        print(f"  {symbol:<8} {mint:<50} {decimals}")


def main():
    parser = argparse.ArgumentParser(
        description="Jupiter Swap Operations",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  jup_swap.py quote SOL USDC 1           Quote swapping 1 SOL to USDC
  jup_swap.py quote USDC SOL 100         Quote swapping 100 USDC to SOL
  jup_swap.py swap SOL USDC 0.1          Swap 0.1 SOL to USDC
  jup_swap.py tokens                     List known tokens

Token symbols: SOL, USDC, USDT, ETH, CBBTC, JUP, BONK, TRUMP, etc.
Or use full mint addresses. Run 'tokens' to see all.

Environment variables (required):
  SOLANA_PRIVATE_KEY    Base58 private key
  JUPITER_API_KEY       Jupiter API key (get from https://portal.jup.ag/)
        """
    )

    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # quote command
    quote_parser = subparsers.add_parser("quote", help="Get swap quote")
    quote_parser.add_argument(
        "input_mint", help="Input token (symbol or mint)")
    quote_parser.add_argument(
        "output_mint", help="Output token (symbol or mint)")
    quote_parser.add_argument("amount", help="Amount to swap")
    quote_parser.set_defaults(func=cmd_quote)

    # swap command
    swap_parser = subparsers.add_parser("swap", help="Execute swap")
    swap_parser.add_argument("input_mint", help="Input token (symbol or mint)")
    swap_parser.add_argument(
        "output_mint", help="Output token (symbol or mint)")
    swap_parser.add_argument("amount", help="Amount to swap")
    swap_parser.set_defaults(func=cmd_swap)

    # tokens command
    tokens_parser = subparsers.add_parser("tokens", help="List known tokens")
    tokens_parser.set_defaults(func=cmd_tokens)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    args.func(args)


if __name__ == "__main__":
    main()
