#!/usr/bin/env python3
"""Show personal analytics status."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import load_config, load_data, is_enabled

def main():
    try:
        config = load_config()
        data = load_data()
    except FileNotFoundError as e:
        print(f"❌ {e}", file=sys.stderr)
        sys.exit(1)
    
    enabled = is_enabled()
    
    print("\n📊 Personal Analytics Status\n")
    print(f"Status: {'✅ Enabled' if enabled else '❌ Disabled'}")
    
    # Data summary
    sessions = data.get("sessions", [])
    topics = data.get("topic_stats", {})
    
    print(f"\nData:")
    print(f"  Sessions tracked: {len(sessions)}")
    print(f"  Unique topics: {len(topics)}")
    
    if sessions:
        first_session = sessions[0].get("start", "Unknown")
        last_session = sessions[-1].get("end", "Unknown")
        print(f"  First session: {first_session}")
        print(f"  Last session: {last_session}")
    
    # Tracking settings
    tracking = config.get("tracking", {})
    print(f"\nTracking:")
    for key, value in tracking.items():
        status = "✓" if value else "✗"
        print(f"  {status} {key}")
    
    # Privacy settings
    privacy = config.get("privacy", {})
    print(f"\nPrivacy:")
    print(f"  Auto-delete after: {privacy.get('auto_delete_after_days', 90)} days")
    print(f"  Exclude patterns: {len(privacy.get('exclude_patterns', []))} configured")
    
    # Integration
    integrations = config.get("integrations", {})
    pr_integration = integrations.get("proactive_research", {})
    
    if pr_integration.get("enabled", False):
        print(f"\nIntegrations:")
        print(f"  ✓ Proactive Research (auto-suggest: {pr_integration.get('auto_suggest_topics', False)})")
    
    print()

if __name__ == "__main__":
    main()
