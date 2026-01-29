#!/usr/bin/env python3
"""Enable personal analytics tracking."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import load_config, save_config

def main():
    try:
        config = load_config()
    except FileNotFoundError:
        print("❌ Config file not found. Run: cp config.example.json config.json", file=sys.stderr)
        sys.exit(1)
    
    config["enabled"] = True
    save_config(config)
    
    print("✅ Personal analytics tracking enabled")
    print("\nTracking:")
    tracking = config.get("tracking", {})
    for key, value in tracking.items():
        status = "✓" if value else "✗"
        print(f"  {status} {key}")
    
    print("\nPrivacy:")
    privacy = config.get("privacy", {})
    print(f"  Auto-delete after: {privacy.get('auto_delete_after_days', 90)} days")
    print(f"  Exclude patterns: {len(privacy.get('exclude_patterns', []))} configured")
    
    print("\n💡 Run 'python3 scripts/analyze.py' to see your patterns")

if __name__ == "__main__":
    main()
