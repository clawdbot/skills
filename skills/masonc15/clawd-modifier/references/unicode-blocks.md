# Unicode Block Drawing Characters

Quick reference for characters used in Clawd and terminal ASCII art.

## Block Elements (U+2580-U+259F)

| Char | Code | Name | Use |
|------|------|------|-----|
| █ | 2588 | Full Block | Solid fill |
| ▀ | 2580 | Upper Half | Top edge |
| ▄ | 2584 | Lower Half | Bottom edge, ears |
| ▌ | 258C | Left Half | Left edge |
| ▐ | 2590 | Right Half | Right edge |
| ▖ | 2596 | Lower Left Quadrant | Corners |
| ▗ | 2597 | Lower Right Quadrant | Corners |
| ▘ | 2598 | Upper Left Quadrant | Feet |
| ▝ | 259D | Upper Right Quadrant | Feet |
| ▛ | 259B | Upper Left + Upper Right + Lower Left | Rounded corners |
| ▜ | 259C | Upper Left + Upper Right + Lower Right | Rounded corners |
| ░ | 2591 | Light Shade | Background texture |
| ▒ | 2592 | Medium Shade | Medium fill |
| ▓ | 2593 | Dark Shade | Dense fill |

## Box Drawing (U+2500-U+257F)

| Char | Code | Name |
|------|------|------|
| ─ | 2500 | Horizontal |
| │ | 2502 | Vertical |
| ┌ | 250C | Down and Right |
| ┐ | 2510 | Down and Left |
| └ | 2514 | Up and Right |
| ┘ | 2518 | Up and Left |
| ╱ | 2571 | Light Diagonal Upper Right to Lower Left |
| ╲ | 2572 | Light Diagonal Upper Left to Lower Right |

## Clawd Character Map

```
Small Clawd (standard terminals):
 ▐▛███▜▌   ← ▐ (right half), ▛ (3-quarter), █ (full), ▜ (3-quarter), ▌ (left half)
▝▜█████▛▘  ← ▝ (upper-right), ▜, █████, ▛, ▘ (upper-left)
  ▘▘ ▝▝    ← feet using upper quadrants

Small Clawd (Apple Terminal - simpler charset):
▗ ▗   ▖ ▖  ← lower quadrants for outline
           ← solid background row
 ▘▘ ▝▝     ← upper quadrants for feet

Large Clawd (loading screen):
 █████████   ← head
██▄█████▄██  ← ears (▄ = lower half blocks)
 █████████   ← body
█ █   █ █    ← eyes/feet pattern
```

## Combining Characters for Arms

```
Original:     With arms:
 ▐▛███▜▌     ╱▐▛███▜▌╲
▝▜█████▛▘   ▝▜█████▛▘

╱ = left arm raised
╲ = right arm
```
