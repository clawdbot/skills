#!/usr/bin/env python3
"""
Setup script for agent-protocol skill.
Creates necessary directories and configuration files.
"""

import json
from pathlib import Path

HOME = Path.home()
SKILL_DIR = Path(__file__).parent.parent

def setup():
    """Initialize agent-protocol directories and config."""
    print("🦎 Setting up Agent Protocol...")
    
    # Create directories
    dirs = [
        HOME / ".clawdbot" / "events" / "queue",
        HOME / ".clawdbot" / "events" / "processed",
        HOME / ".clawdbot" / "events" / "failed",
        HOME / ".clawdbot" / "events" / "log" / "workflows",
        HOME / ".clawdbot" / "workflow_state",
        SKILL_DIR / "config" / "workflows"
    ]
    
    for dir_path in dirs:
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created {dir_path}")
    
    # Copy config if it doesn't exist
    config_src = SKILL_DIR / "config.example.json"
    config_dest = SKILL_DIR / "config" / "protocol.json"
    
    if not config_dest.exists():
        config_dest.parent.mkdir(parents=True, exist_ok=True)
        config_dest.write_text(config_src.read_text())
        print(f"  ✓ Created config: {config_dest}")
    else:
        print(f"  ⊙ Config already exists: {config_dest}")
    
    # Create empty subscriptions file
    subscriptions_file = HOME / ".clawdbot" / "events" / "subscriptions.json"
    if not subscriptions_file.exists():
        subscriptions_file.write_text("[]")
        print(f"  ✓ Created subscriptions file")
    
    print("\n✅ Setup complete!")
    print("\nNext steps:")
    print("  1. Test the event bus:")
    print("     python3 scripts/publish.py --type 'test.hello' --source 'test' --payload '{}'")
    print("  2. Check status:")
    print("     python3 scripts/event_bus.py status")
    print("  3. Create a workflow:")
    print("     cp examples/simple-workflow.json config/workflows/my-workflow.json")
    print("  4. Run workflow engine:")
    print("     python3 scripts/workflow_engine.py --run")

if __name__ == "__main__":
    setup()
