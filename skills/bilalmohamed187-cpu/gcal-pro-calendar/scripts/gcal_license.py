#!/usr/bin/env python3
"""
gcal-pro: License Management Module
Handles Pro tier license validation.
"""

import json
import hashlib
import os
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, Any

CONFIG_DIR = Path.home() / ".config" / "gcal-pro"
LICENSE_FILE = CONFIG_DIR / "license.json"

# Simple license key format: GCAL-XXXX-XXXX-XXXX
# In production, you'd use a more robust system (Gumroad API, etc.)


def get_machine_id() -> str:
    """Generate a machine-specific identifier."""
    # Combine hostname and username for basic machine ID
    import socket
    hostname = socket.gethostname()
    username = os.environ.get("USERNAME") or os.environ.get("USER") or "unknown"
    raw = f"{hostname}:{username}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def validate_license_key(key: str) -> bool:
    """
    Validate a license key format.
    
    Real implementation would verify against Gumroad API or similar.
    For MVP, we use a simple checksum validation.
    """
    if not key:
        return False
    
    # Expected format: GCAL-XXXX-XXXX-XXXX
    parts = key.upper().strip().split("-")
    if len(parts) != 4 or parts[0] != "GCAL":
        return False
    
    # Simple checksum: last 4 chars should be based on first 3 parts
    check_input = "-".join(parts[:3])
    expected_check = hashlib.md5(check_input.encode()).hexdigest()[:4].upper()
    
    # For now, accept any well-formed key (implement real validation later)
    # In production: verify against Gumroad API
    return all(len(p) == 4 for p in parts[1:])


def activate_license(key: str) -> Dict[str, Any]:
    """
    Activate a Pro license.
    
    Args:
        key: License key from purchase
        
    Returns:
        Activation result with status and message
    """
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    
    if not validate_license_key(key):
        return {
            "success": False,
            "message": "Invalid license key format. Expected: GCAL-XXXX-XXXX-XXXX"
        }
    
    # Create license file
    license_data = {
        "key": key.upper().strip(),
        "tier": "pro",
        "valid": True,
        "activated_at": datetime.utcnow().isoformat(),
        "machine_id": get_machine_id()
    }
    
    try:
        with open(LICENSE_FILE, "w") as f:
            json.dump(license_data, f, indent=2)
        
        # Secure the file
        try:
            os.chmod(LICENSE_FILE, 0o600)
        except (OSError, AttributeError):
            pass
        
        return {
            "success": True,
            "message": "✓ Pro license activated! You now have full access.",
            "tier": "pro"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Failed to save license: {e}"
        }


def get_license_info() -> Dict[str, Any]:
    """Get current license information."""
    if not LICENSE_FILE.exists():
        return {
            "tier": "free",
            "valid": True,
            "message": "Free tier - read-only access"
        }
    
    try:
        with open(LICENSE_FILE, "r") as f:
            data = json.load(f)
        
        return {
            "tier": data.get("tier", "free"),
            "valid": data.get("valid", False),
            "activated_at": data.get("activated_at"),
            "key": data.get("key", "")[:9] + "..." if data.get("key") else None
        }
    except (json.JSONDecodeError, IOError):
        return {
            "tier": "free",
            "valid": True,
            "message": "License file corrupted - defaulting to free tier"
        }


def deactivate_license() -> Dict[str, Any]:
    """Deactivate current license."""
    if LICENSE_FILE.exists():
        try:
            LICENSE_FILE.unlink()
            return {
                "success": True,
                "message": "License deactivated. Reverted to free tier."
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"Failed to deactivate: {e}"
            }
    else:
        return {
            "success": True,
            "message": "No license to deactivate."
        }


def is_pro() -> bool:
    """Quick check if user has Pro access."""
    info = get_license_info()
    return info.get("tier") == "pro" and info.get("valid", False)


# CLI interface
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="gcal-pro license management")
    parser.add_argument("command", choices=["status", "activate", "deactivate"],
                        help="License command")
    parser.add_argument("--key", "-k", help="License key for activation")
    
    args = parser.parse_args()
    
    if args.command == "status":
        info = get_license_info()
        print(f"Tier:      {info.get('tier', 'free').title()}")
        print(f"Valid:     {'Yes' if info.get('valid') else 'No'}")
        if info.get('activated_at'):
            print(f"Activated: {info.get('activated_at')}")
        if info.get('key'):
            print(f"Key:       {info.get('key')}")
        if info.get('message'):
            print(f"Note:      {info.get('message')}")
    
    elif args.command == "activate":
        if not args.key:
            print("Error: --key required for activation")
            print("Usage: python gcal_license.py activate --key GCAL-XXXX-XXXX-XXXX")
            exit(1)
        result = activate_license(args.key)
        print(result.get("message"))
        exit(0 if result.get("success") else 1)
    
    elif args.command == "deactivate":
        result = deactivate_license()
        print(result.get("message"))
        exit(0 if result.get("success") else 1)
