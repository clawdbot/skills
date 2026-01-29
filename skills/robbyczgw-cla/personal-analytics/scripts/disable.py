#!/usr/bin/env python3
"""Disable personal analytics tracking."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import load_config, save_config

def main():
    try:
        config = load_config()
    except FileNotFoundError:
        print("❌ Config file not found", file=sys.stderr)
        sys.exit(1)
    
    config["enabled"] = False
    save_config(config)
    
    print("✅ Personal analytics tracking disabled")
    print("\n⚠️ Existing data is preserved.")
    print("To delete all data, run: python3 scripts/delete_data.py --all")

if __name__ == "__main__":
    main()
