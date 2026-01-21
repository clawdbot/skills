#!/usr/bin/env python3
"""
Initialize Task Tracker - Create TASKS.md from template.
"""

import sys
from pathlib import Path

SKILL_DIR = Path(__file__).parent.parent
TEMPLATE_FILE = SKILL_DIR / "assets" / "templates" / "TASKS.md"
TARGET_FILE = Path.home() / "clawd" / "memory" / "work" / "TASKS.md"


def init():
    """Create TASKS.md from template."""
    if TARGET_FILE.exists():
        print(f"\n⚠️ Tasks file already exists: {TARGET_FILE}")
        print("Delete it first if you want to recreate from template.\n")
        sys.exit(1)
    
    if not TEMPLATE_FILE.exists():
        print(f"\n❌ Template not found: {TEMPLATE_FILE}")
        sys.exit(1)
    
    # Ensure directory exists
    TARGET_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Copy template
    content = TEMPLATE_FILE.read_text()
    TARGET_FILE.write_text(content)
    
    print(f"\n✅ Created tasks file: {TARGET_FILE}\n")
    print("Next steps:")
    print("  python3 scripts/tasks.py list\n")


if __name__ == '__main__':
    init()
