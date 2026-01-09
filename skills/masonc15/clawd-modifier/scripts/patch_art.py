#!/usr/bin/env python3
"""
Patch Clawd's ASCII art in Claude Code cli.js

Usage:
    python patch_art.py --small "line1" "line2" "line3"    # Replace small Clawd
    python patch_art.py --variant robot                     # Use preset variant
    python patch_art.py --add-left-arm                      # Add left arm to Clawd
    python patch_art.py --add-right-arm                     # Add right arm to Clawd
    python patch_art.py --add-hat                           # Add hat to Clawd
    python patch_art.py --restore                           # Restore original

Examples:
    python patch_art.py --add-left-arm --add-right-arm
    python patch_art.py --variant with-arms
"""

import argparse
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime

DEFAULT_CLI_PATH = "/opt/node22/lib/node_modules/@anthropic-ai/claude-code/cli.js"

# Original small Clawd art patterns (what to find in the minified code)
ORIGINAL_SMALL = {
    'top_left': '" ▐"',
    'head': '"▛███▜"',
    'top_right': '"▌"',
    'mid_left': '"▝▜"',
    'body': '"█████"',
    'mid_right': '"▛▘"',
    'feet': '"▘▘ ▝▝"',
}

# Preset variants for small Clawd modifications
VARIANTS = {
    'with-left-arm': {
        'description': 'Clawd with a left arm',
        'replacements': {
            '" ▐"': '"╱▐"',
        }
    },
    'with-right-arm': {
        'description': 'Clawd with a right arm',
        'replacements': {
            '"▌")': '"▌╲")' ,
        }
    },
    'with-arms': {
        'description': 'Clawd with both arms',
        'replacements': {
            '" ▐"': '"╱▐"',
            '"▌")': '"▌╲")',
        }
    },
    'with-hat': {
        'description': 'Clawd wearing a top hat',
        # This requires inserting a new line, which is complex in minified code
        'note': 'Complex modification - requires manual editing',
    },
    'waving': {
        'description': 'Clawd with a waving arm',
        'replacements': {
            '"▌")': '"▌╱")',
        }
    },
    'excited': {
        'description': 'Clawd with arms up',
        'replacements': {
            '" ▐"': '"╲▐"',
            '"▌")': '"▌╱")',
        }
    },
}

def find_cli_js():
    """Find cli.js in common locations."""
    paths = [
        DEFAULT_CLI_PATH,
        Path.home() / ".npm-global/lib/node_modules/@anthropic-ai/claude-code/cli.js",
        "/usr/local/lib/node_modules/@anthropic-ai/claude-code/cli.js",
    ]
    for p in paths:
        if Path(p).exists():
            return str(p)
    return None

def backup_cli(cli_path: str) -> str:
    """Create a backup of cli.js."""
    backup_path = f"{cli_path}.backup.{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    shutil.copy2(cli_path, backup_path)
    return backup_path

def apply_variant(cli_path: str, variant_name: str, dry_run: bool = False) -> dict:
    """Apply a preset variant to Clawd."""
    if variant_name not in VARIANTS:
        return {'success': False, 'error': f'Unknown variant: {variant_name}'}

    variant = VARIANTS[variant_name]
    if 'note' in variant:
        return {'success': False, 'error': variant['note']}

    code = Path(cli_path).read_text()
    total_replacements = 0

    for old, new in variant['replacements'].items():
        count = code.count(old)
        if count > 0:
            code = code.replace(old, new)
            total_replacements += count

    if total_replacements == 0:
        return {'success': False, 'error': 'No matching patterns found (already modified?)'}

    if not dry_run:
        Path(cli_path).write_text(code)

    return {
        'success': True,
        'variant': variant_name,
        'description': variant['description'],
        'replacements': total_replacements,
        'dry_run': dry_run,
    }

def apply_custom_replacements(cli_path: str, replacements: dict, dry_run: bool = False) -> dict:
    """Apply custom string replacements."""
    code = Path(cli_path).read_text()
    total = 0

    for old, new in replacements.items():
        count = code.count(old)
        code = code.replace(old, new)
        total += count

    if total == 0:
        return {'success': False, 'error': 'No matching patterns found'}

    if not dry_run:
        Path(cli_path).write_text(code)

    return {'success': True, 'replacements': total, 'dry_run': dry_run}

def restore_original(cli_path: str, dry_run: bool = False) -> dict:
    """Restore Clawd to original form by reversing known modifications."""
    code = Path(cli_path).read_text()

    # Reverse all known modifications
    reverse_map = {
        '"╱▐"': '" ▐"',
        '"▌╲")': '"▌")',
        '"▌╱")': '"▌")',
        '"╲▐"': '" ▐"',
    }

    total = 0
    for modified, original in reverse_map.items():
        count = code.count(modified)
        code = code.replace(modified, original)
        total += count

    if total == 0:
        return {'success': True, 'message': 'Clawd appears to already be in original form'}

    if not dry_run:
        Path(cli_path).write_text(code)

    return {'success': True, 'reversions': total, 'dry_run': dry_run}

def main():
    parser = argparse.ArgumentParser(description="Modify Clawd's ASCII art")
    parser.add_argument('--variant', help='Apply preset variant')
    parser.add_argument('--add-left-arm', action='store_true', help='Add left arm')
    parser.add_argument('--add-right-arm', action='store_true', help='Add right arm')
    parser.add_argument('--restore', action='store_true', help='Restore original art')
    parser.add_argument('--cli-path', default=None, help='Path to cli.js')
    parser.add_argument('--list', action='store_true', help='List preset variants')
    parser.add_argument('--dry-run', action='store_true', help='Show what would change')
    parser.add_argument('--no-backup', action='store_true', help='Skip backup')

    args = parser.parse_args()

    if args.list:
        print("Available Clawd variants:")
        for name, info in VARIANTS.items():
            note = f" ({info['note']})" if 'note' in info else ""
            print(f"  {name:20} {info['description']}{note}")
        return

    cli_path = args.cli_path or find_cli_js()
    if not cli_path or not Path(cli_path).exists():
        print(f"Error: cli.js not found. Use --cli-path to specify.", file=sys.stderr)
        sys.exit(1)

    # Backup unless disabled
    if not args.no_backup and not args.dry_run:
        backup = backup_cli(cli_path)
        print(f"Backup created: {backup}")

    # Handle restore
    if args.restore:
        result = restore_original(cli_path, dry_run=args.dry_run)
        if result['success']:
            if 'message' in result:
                print(result['message'])
            else:
                action = "Would revert" if args.dry_run else "Reverted"
                print(f"{action} {result['reversions']} modifications")
        return

    # Handle variant
    if args.variant:
        result = apply_variant(cli_path, args.variant, dry_run=args.dry_run)
        if result['success']:
            action = "Would apply" if args.dry_run else "Applied"
            print(f"{action} variant '{result['variant']}': {result['description']}")
            print(f"Modified {result['replacements']} patterns")
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
        return

    # Handle individual modifications
    replacements = {}
    if args.add_left_arm:
        replacements['" ▐"'] = '"╱▐"'
    if args.add_right_arm:
        replacements['"▌")'] = '"▌╲")'

    if replacements:
        result = apply_custom_replacements(cli_path, replacements, dry_run=args.dry_run)
        if result['success']:
            action = "Would modify" if args.dry_run else "Modified"
            print(f"{action} {result['replacements']} patterns")
        else:
            print(f"Error: {result['error']}", file=sys.stderr)
            sys.exit(1)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
