#!/usr/bin/env python3
"""
Patch Clawd's appearance directly in the compiled Claude Code binary.

This script modifies specific byte sequences in the Bun-compiled binary
to change Clawd's ASCII art (e.g., adding arms, changing poses).

Usage:
    python patch_binary.py --variant excited
    python patch_binary.py --restore
    python patch_binary.py --list

WARNING: This modifies a compiled binary. Always backup first!
"""

import argparse
import shutil
import sys
from pathlib import Path
from datetime import datetime

# Default binary locations
DEFAULT_PATHS = [
    Path.home() / ".local/bin/claude",
    "/usr/local/bin/claude",
    "/opt/homebrew/bin/claude",
]

# Patch definitions
# Format: (search_bytes, replace_bytes, description)
# All strings are UTF-16LE encoded

PATCHES = {
    'excited': {
        'description': 'Clawd with arms up (excited pose) - LARGE startup Clawd',
        'patches': [
            # LARGE CLAWD (startup screen)
            # The body line: body"}," \u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588\u2588 ")
            # Change first \u2588 to \u2572 (left arm): 5c7532353838 -> 5c7532353732
            # Change last \u2588 to \u2571 (right arm): 5c7532353838 -> 5c7532353731
            {
                # Pattern: body"}," \u2588 (start of body line, first block)
                'search': b'body"}," \\u2588',
                'replace': b'body"}," \\u2572',  # ╲ left arm up
                'description': 'Large Clawd left arm up'
            },
            {
                # Pattern: \u2588 ") at end of body line (last block before space and close)
                'search': b'\\u2588 ")',
                'replace': b'\\u2571 ")',  # ╱ right arm up
                'description': 'Large Clawd right arm up'
            },
        ]
    },
    'excited-small': {
        'description': 'Clawd with arms up - SMALL prompt Clawd only',
        'patches': [
            # SMALL CLAWD (prompt icon) - UTF-16LE in constant pool
            {
                'search': b'\x20\x00\x90\x25',  # " ▐" in UTF-16LE
                'replace': b'\x72\x25\x90\x25', # "╲▐" in UTF-16LE
                'context': b'clawd_body',
                'max_distance': 50,
                'description': 'Small Clawd left arm up'
            },
        ]
    },
    'excited-both': {
        'description': 'Clawd with arms up - BOTH large and small',
        'patches': [
            # Large Clawd
            {
                'search': b'body"}," \\u2588',
                'replace': b'body"}," \\u2572',
                'description': 'Large Clawd left arm up'
            },
            {
                'search': b'\\u2588 ")',
                'replace': b'\\u2571 ")',
                'description': 'Large Clawd right arm up'
            },
            # Small Clawd
            {
                'search': b'\x20\x00\x90\x25',
                'replace': b'\x72\x25\x90\x25',
                'context': b'clawd_body',
                'max_distance': 50,
                'description': 'Small Clawd left arm up'
            },
        ]
    },
    'waving': {
        'description': 'Clawd waving (one arm up)',
        'patches': [
            {
                'search': b'\\u2588 ")',
                'replace': b'\\u2571 ")',
                'description': 'Large Clawd right arm waving'
            },
        ]
    },
    'original': {
        'description': 'Restore original Clawd',
        'patches': [
            # Restore large Clawd
            {
                'search': b'body"}," \\u2572',
                'replace': b'body"}," \\u2588',
                'description': 'Remove large Clawd left arm'
            },
            {
                'search': b'\\u2571 ")',
                'replace': b'\\u2588 ")',
                'description': 'Remove large Clawd right arm'
            },
            # Restore small Clawd
            {
                'search': b'\x72\x25\x90\x25',
                'replace': b'\x20\x00\x90\x25',
                'context': b'clawd_body',
                'max_distance': 50,
                'description': 'Remove small Clawd left arm'
            },
        ]
    }
}


def find_binary():
    """Find the Claude Code binary."""
    for path in DEFAULT_PATHS:
        if path.exists():
            return path
    return None


def backup_binary(binary_path: Path) -> Path:
    """Create a timestamped backup of the binary."""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_path = binary_path.parent / f"{binary_path.name}.backup.{timestamp}"
    shutil.copy2(binary_path, backup_path)
    return backup_path


def find_context_matches(data: bytes, context: bytes, max_occurrences: int = 200) -> list:
    """Find all positions where context string appears."""
    positions = []
    start = 0
    while len(positions) < max_occurrences:
        pos = data.find(context, start)
        if pos == -1:
            break
        positions.append(pos)
        start = pos + 1
    return positions


def apply_patch(binary_path: Path, variant: str, dry_run: bool = False) -> dict:
    """Apply a patch variant to the binary."""
    if variant not in PATCHES:
        return {'success': False, 'error': f'Unknown variant: {variant}'}

    patch_def = PATCHES[variant]
    data = binary_path.read_bytes()

    total_patches = 0
    patch_details = []

    for patch in patch_def['patches']:
        if not patch.get('search') or not patch.get('replace'):
            continue

        search = patch['search']
        replace = patch['replace']
        context = patch.get('context', b'')
        max_dist = patch.get('max_distance', 100)

        if context:
            # Find patches only near context strings
            context_positions = find_context_matches(data, context)

            for ctx_pos in context_positions:
                # Search in the region after the context
                region_start = ctx_pos
                region_end = min(ctx_pos + max_dist + len(search), len(data))
                region = data[region_start:region_end]

                local_pos = region.find(search)
                if local_pos != -1:
                    abs_pos = region_start + local_pos
                    # Verify it's the right pattern
                    if data[abs_pos:abs_pos + len(search)] == search:
                        if not dry_run:
                            data = data[:abs_pos] + replace + data[abs_pos + len(search):]
                        total_patches += 1
                        patch_details.append({
                            'offset': abs_pos,
                            'description': patch.get('description', 'Unknown'),
                            'context_offset': ctx_pos
                        })
        else:
            # Global search and replace
            count = data.count(search)
            if count > 0:
                if not dry_run:
                    data = data.replace(search, replace)
                total_patches += count
                patch_details.append({
                    'count': count,
                    'description': patch.get('description', 'Unknown')
                })

    if total_patches == 0:
        return {
            'success': False,
            'error': 'No matching patterns found (already patched or different binary version?)'
        }

    if not dry_run:
        binary_path.write_bytes(data)

    return {
        'success': True,
        'patches_applied': total_patches,
        'details': patch_details,
        'dry_run': dry_run,
        'variant': variant,
        'description': patch_def['description']
    }


def main():
    parser = argparse.ArgumentParser(
        description="Patch Clawd's appearance in compiled Claude Code binary"
    )
    parser.add_argument('--variant', '-v', help='Variant to apply (excited, waving, original)')
    parser.add_argument('--binary', '-b', help='Path to Claude binary')
    parser.add_argument('--list', '-l', action='store_true', help='List available variants')
    parser.add_argument('--dry-run', '-n', action='store_true', help='Show what would be changed')
    parser.add_argument('--no-backup', action='store_true', help='Skip creating backup')
    parser.add_argument('--restore', '-r', action='store_true', help='Restore to original')

    args = parser.parse_args()

    if args.list:
        print("Available Clawd variants:")
        for name, info in PATCHES.items():
            patches_count = len([p for p in info.get('patches', []) if p.get('search')])
            print(f"  {name:15} {info['description']} ({patches_count} patches)")
        return

    if args.restore:
        args.variant = 'original'

    if not args.variant:
        parser.print_help()
        return

    # Find binary
    binary_path = Path(args.binary) if args.binary else find_binary()
    if not binary_path or not binary_path.exists():
        print(f"Error: Claude binary not found. Use --binary to specify path.", file=sys.stderr)
        sys.exit(1)

    print(f"Binary: {binary_path}")

    # Backup
    if not args.no_backup and not args.dry_run:
        backup = backup_binary(binary_path)
        print(f"Backup: {backup}")

    # Apply patch
    result = apply_patch(binary_path, args.variant, dry_run=args.dry_run)

    if result['success']:
        action = "Would apply" if args.dry_run else "Applied"
        print(f"\n{action} variant '{result['variant']}': {result['description']}")
        print(f"Total patches: {result['patches_applied']}")

        if result.get('details'):
            print("\nDetails:")
            for detail in result['details']:
                if 'offset' in detail:
                    print(f"  - {detail['description']} at offset {detail['offset']}")
                elif 'count' in detail:
                    print(f"  - {detail['description']}: {detail['count']} occurrences")

        if not args.dry_run:
            print("\nRestart Claude Code to see changes.")
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
