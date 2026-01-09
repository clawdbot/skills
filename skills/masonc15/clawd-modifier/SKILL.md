---
name: clawd-modifier
description: Modify Clawd, the Claude Code mascot. Use this skill when users want to customize Clawd's appearance in their Claude Code CLI, including changing colors (blue Clawd, green Clawd, holiday themes), adding features (arms, hats, accessories), or creating custom ASCII art variants. Triggers include "change Clawd color", "give Clawd arms", "customize the mascot", "modify Clawd", "make Clawd [color]", or any request to personalize the Claude Code terminal mascot.
---

# Clawd Modifier

Customize the Claude Code mascot's appearance by modifying colors and ASCII art.

## Quick Reference

**CLI location**: `/opt/node22/lib/node_modules/@anthropic-ai/claude-code/cli.js`

**Clawd colors**:
- Body: `rgb(215,119,87)` / `ansi:redBright`
- Background: `rgb(0,0,0)` / `ansi:black`

**Small Clawd** (prompt):
```
 ▐▛███▜▌
▝▜█████▛▘
  ▘▘ ▝▝
```

## Workflows

### Change Clawd's Color

Use `scripts/patch_color.py`:

```bash
# List available colors
python scripts/patch_color.py --list

# Apply preset
python scripts/patch_color.py blue

# Custom RGB
python scripts/patch_color.py --rgb 100,200,150

# Restore original
python scripts/patch_color.py --restore
```

### Add Arms or Modify Art

Use `scripts/patch_art.py`:

```bash
# List variants
python scripts/patch_art.py --list

# Add arms
python scripts/patch_art.py --variant with-arms

# Individual modifications
python scripts/patch_art.py --add-left-arm
python scripts/patch_art.py --add-right-arm

# Restore original
python scripts/patch_art.py --restore
```

### Extract Current Clawd

Use `scripts/extract_clawd.py` to see current state:

```bash
python scripts/extract_clawd.py
```

### Manual Modifications

For custom changes not covered by scripts, edit cli.js directly:

1. Backup: `cp cli.js cli.js.bak`
2. Find patterns with grep
3. Use sed or text editor to replace
4. Test by running `claude`

Pattern examples:
```bash
# Find color definitions
grep -o 'clawd_body:"[^"]*"' cli.js | head -5

# Replace color
sed -i 's/rgb(215,119,87)/rgb(100,149,237)/g' cli.js
```

## Resources

- **Unicode reference**: See `references/unicode-blocks.md` for block characters
- **Technical details**: See `references/clawd-anatomy.md` for rendering internals
- **Design gallery**: See `assets/clawd-variants.txt` for inspiration

## Notes

- Changes are overwritten by `npm update`
- Always create backups before modifying
- Test with `claude --version` after changes
- Some terminals have limited Unicode support
