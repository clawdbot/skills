#!/usr/bin/env python3
"""
Solana Wallet Initialization
Creates a new wallet and saves the private key to .env file
"""

import os
import sys
from pathlib import Path

try:
    from solders.keypair import Keypair
    import base58
except ImportError:
    print("Error: Required packages not installed.")
    print("Run: pip install solana solders base58")
    sys.exit(1)


def create_wallet():
    """Generate a new Solana keypair."""
    keypair = Keypair()
    return keypair


def save_to_env(private_key_base58: str, env_path: Path = None):
    """Save private key to .env file."""
    if env_path is None:
        env_path = Path.cwd() / ".env"
    
    env_content = {}
    
    # Read existing .env if it exists
    if env_path.exists():
        with open(env_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    key, value = line.split("=", 1)
                    env_content[key] = value
    
    # Update or add SOLANA_PRIVATE_KEY
    env_content["SOLANA_PRIVATE_KEY"] = private_key_base58
    
    # Write back to .env
    with open(env_path, "w") as f:
        for key, value in env_content.items():
            f.write(f"{key}={value}\n")
    
    return env_path


def main():
    print("◎ Solana Wallet Initialization\n")
    
    # Check if wallet already exists
    existing_key = os.environ.get("SOLANA_PRIVATE_KEY")
    env_path = Path.cwd() / ".env"
    
    if env_path.exists():
        with open(env_path, "r") as f:
            content = f.read()
            if "SOLANA_PRIVATE_KEY=" in content:
                print("⚠️  Warning: SOLANA_PRIVATE_KEY already exists in .env")
                response = input("Do you want to create a new wallet? This will overwrite the existing key. (y/N): ")
                if response.lower() != "y":
                    print("Aborted.")
                    sys.exit(0)
    
    # Create new wallet
    keypair = create_wallet()
    
    # Get public key (wallet address)
    public_key = str(keypair.pubkey())
    
    # Get private key as bytes and encode to base58
    # The keypair's secret() returns the full 64-byte secret (32-byte seed + 32-byte public key)
    private_key_bytes = bytes(keypair)
    private_key_base58 = base58.b58encode(private_key_bytes).decode("utf-8")
    
    # Save to .env
    saved_path = save_to_env(private_key_base58, env_path)
    
    print("✅ New wallet created!\n")
    print(f"📍 Public Key (Address): {public_key}")
    print(f"💾 Private key saved to: {saved_path}")
    print()
    print("⚠️  IMPORTANT: Keep your private key safe! Never share it.")
    print()
    print("To use the wallet, export the private key to your environment:")
    print()
    print("  export SOLANA_PRIVATE_KEY=$(grep SOLANA_PRIVATE_KEY .env | cut -d '=' -f2)")
    print()
    print("Or source the .env file:")
    print()
    print("  source .env")
    print()
    print(f"Fund your wallet by sending SOL to: {public_key}")


if __name__ == "__main__":
    main()
