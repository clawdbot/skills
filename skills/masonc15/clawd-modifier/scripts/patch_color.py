#!/usr/bin/env python3
"""
Patch Clawd's color in Claude Code cli.js

Usage:
    python patch_color.py <color>              # Use preset color name
    python patch_color.py --rgb R,G,B          # Use custom RGB
    python patch_color.py --restore            # Restore original color
    python patch_color.py --list               # List preset colors

Examples:
    python patch_color.py blue
    python patch_color.py --rgb 100,200,150
    python patch_color.py gold --cli-path /custom/path/cli.js
"""

import argparse
import re
import shutil
import sys
from pathlib import Path
from datetime import datetime

DEFAULT_CLI_PATH = "/opt/node22/lib/node_modules/@anthropic-ai/claude-code/cli.js"

# Original Clawd color
ORIGINAL_COLOR = {
    'rgb': 'rgb(215,119,87)',
    'ansi': 'ansi:redBright',
}

# Preset color palettes
PRESETS = {
    'original': {'rgb': 'rgb(215,119,87)', 'ansi': 'ansi:redBright'},
    'blue': {'rgb': 'rgb(100,149,237)', 'ansi': 'ansi:blueBright'},
    'green': {'rgb': 'rgb(119,215,87)', 'ansi': 'ansi:greenBright'},
    'purple': {'rgb': 'rgb(180,119,215)', 'ansi': 'ansi:magentaBright'},
    'gold': {'rgb': 'rgb(255,215,0)', 'ansi': 'ansi:yellowBright'},
    'cyan': {'rgb': 'rgb(0,215,215)', 'ansi': 'ansi:cyanBright'},
    'pink': {'rgb': 'rgb(255,105,180)', 'ansi': 'ansi:magentaBright'},
    'orange': {'rgb': 'rgb(255,165,0)', 'ansi': 'ansi:yellowBright'},
    'lime': {'rgb': 'rgb(50,205,50)', 'ansi': 'ansi:greenBright'},
    'red': {'rgb': 'rgb(255,69,0)', 'ansi': 'ansi:redBright'},
    'white': {'rgb': 'rgb(255,255,255)', 'ansi': 'ansi:whiteBright'},
    'christmas_red': {'rgb': 'rgb(165,42,42)', 'ansi': 'ansi:red'},
    'christmas_green': {'rgb': 'rgb(34,139,34)', 'ansi': 'ansi:green'},
    'halloween_orange': {'rgb': 'rgb(255,117,24)', 'ansi': 'ansi:yellowBright'},
    'valentines_pink': {'rgb': 'rgb(255,20,147)', 'ansi': 'ansi:magentaBright'},
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

def patch_color(cli_path: str, rgb: str, ansi: str, dry_run: bool = False) -> dict:
    """Patch Clawd's body color in cli.js."""
    code = Path(cli_path).read_text()

    # Find and replace RGB colors (clawd_body only)
    old_rgb_pattern = r'clawd_body:"rgb\([^)]+\)"'
    new_rgb = f'clawd_body:"{rgb}"'

    # Find and replace ANSI colors
    old_ansi_pattern = r'clawd_body:"ansi:[^"]+"'
    new_ansi = f'clawd_body:"{ansi}"'

    rgb_count = len(re.findall(old_rgb_pattern, code))
    ansi_count = len(re.findall(old_ansi_pattern, code))

    if rgb_count == 0 and ansi_count == 0:
        return {'success': False, 'error': 'No clawd_body colors found in cli.js'}

    new_code = re.sub(old_rgb_pattern, new_rgb, code)
    new_code = re.sub(old_ansi_pattern, new_ansi, new_code)

    if not dry_run:
        Path(cli_path).write_text(new_code)

    return {
        'success': True,
        'rgb_replacements': rgb_count,
        'ansi_replacements': ansi_count,
        'new_rgb': rgb,
        'new_ansi': ansi,
        'dry_run': dry_run,
    }

def main():
    parser = argparse.ArgumentParser(description="Modify Clawd's color in Claude Code")
    parser.add_argument('preset', nargs='?', help='Preset color name')
    parser.add_argument('--rgb', help='Custom RGB color (e.g., 100,149,237)')
    parser.add_argument('--ansi', default=None, help='ANSI color override')
    parser.add_argument('--cli-path', default=None, help='Path to cli.js')
    parser.add_argument('--restore', action='store_true', help='Restore original color')
    parser.add_argument('--list', action='store_true', help='List preset colors')
    parser.add_argument('--dry-run', action='store_true', help='Show what would change')
    parser.add_argument('--no-backup', action='store_true', help='Skip backup')

    args = parser.parse_args()

    if args.list:
        print("Available preset colors:")
        for name, colors in PRESETS.items():
            print(f"  {name:20} {colors['rgb']}")
        return

    cli_path = args.cli_path or find_cli_js()
    if not cli_path or not Path(cli_path).exists():
        print(f"Error: cli.js not found. Use --cli-path to specify.", file=sys.stderr)
        sys.exit(1)

    # Determine target color
    if args.restore:
        rgb, ansi = ORIGINAL_COLOR['rgb'], ORIGINAL_COLOR['ansi']
    elif args.rgb:
        parts = args.rgb.split(',')
        if len(parts) != 3:
            print("Error: RGB must be in format R,G,B (e.g., 100,149,237)", file=sys.stderr)
            sys.exit(1)
        rgb = f"rgb({args.rgb})"
        ansi = args.ansi or 'ansi:whiteBright'
    elif args.preset:
        if args.preset not in PRESETS:
            print(f"Error: Unknown preset '{args.preset}'. Use --list to see options.", file=sys.stderr)
            sys.exit(1)
        rgb = PRESETS[args.preset]['rgb']
        ansi = PRESETS[args.preset]['ansi']
    else:
        parser.print_help()
        return

    # Backup unless disabled
    if not args.no_backup and not args.dry_run:
        backup = backup_cli(cli_path)
        print(f"Backup created: {backup}")

    # Apply patch
    result = patch_color(cli_path, rgb, ansi, dry_run=args.dry_run)

    if result['success']:
        action = "Would patch" if args.dry_run else "Patched"
        print(f"{action} {result['rgb_replacements']} RGB and {result['ansi_replacements']} ANSI color definitions")
        print(f"New color: {result['new_rgb']} / {result['new_ansi']}")
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
