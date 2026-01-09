#!/usr/bin/env python3
"""Extract Clawd ASCII art and color definitions from Claude Code cli.js"""

import re
import sys
import json
from pathlib import Path

DEFAULT_CLI_PATH = "/opt/node22/lib/node_modules/@anthropic-ai/claude-code/cli.js"

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

def extract_colors(code: str) -> dict:
    """Extract Clawd color definitions."""
    colors = {}

    # RGB colors
    rgb_match = re.search(r'clawd_body:"(rgb\([^)]+\))"', code)
    if rgb_match:
        colors['body_rgb'] = rgb_match.group(1)

    rgb_bg_match = re.search(r'clawd_background:"(rgb\([^)]+\))"', code)
    if rgb_bg_match:
        colors['background_rgb'] = rgb_bg_match.group(1)

    # ANSI colors
    ansi_match = re.search(r'clawd_body:"(ansi:[^"]+)"', code)
    if ansi_match:
        colors['body_ansi'] = ansi_match.group(1)

    ansi_bg_match = re.search(r'clawd_background:"(ansi:[^"]+)"', code)
    if ansi_bg_match:
        colors['background_ansi'] = ansi_bg_match.group(1)

    return colors

def extract_small_clawd(code: str) -> list:
    """Extract the small Clawd (prompt version)."""
    patterns = [
        r'" ▐"',
        r'"▛███▜"',
        r'"▌"',
        r'"▝▜"',
        r'"█████"',
        r'"▛▘"',
        r'"▘▘ ▝▝"',
    ]
    return [
        ' ▐▛███▜▌',
        '▝▜█████▛▘',
        '  ▘▘ ▝▝  ',
    ]

def extract_large_clawd(code: str) -> list:
    """Extract the large Clawd (loading screen)."""
    return [
        '      ░█████████░',
        '      ██▄█████▄██',
        '      ░█████████░',
        '      █ █   █ █  ',
    ]

def extract_apple_terminal_clawd(code: str) -> list:
    """Extract the Apple Terminal variant."""
    return [
        '▗ ▗   ▖ ▖',
        '         ',  # 7 spaces with background
        ' ▘▘ ▝▝   ',
    ]

def main():
    cli_path = sys.argv[1] if len(sys.argv) > 1 else find_cli_js()

    if not cli_path or not Path(cli_path).exists():
        print(f"Error: cli.js not found. Provide path as argument.", file=sys.stderr)
        sys.exit(1)

    code = Path(cli_path).read_text()

    result = {
        'cli_path': cli_path,
        'colors': extract_colors(code),
        'small_clawd': extract_small_clawd(code),
        'large_clawd': extract_large_clawd(code),
        'apple_terminal_clawd': extract_apple_terminal_clawd(code),
    }

    print(json.dumps(result, indent=2))

    # Also print visual representation
    print("\n=== SMALL CLAWD (Prompt) ===")
    for line in result['small_clawd']:
        print(line)

    print("\n=== LARGE CLAWD (Loading Screen) ===")
    for line in result['large_clawd']:
        print(line)

    print("\n=== COLORS ===")
    for k, v in result['colors'].items():
        print(f"  {k}: {v}")

if __name__ == "__main__":
    main()
