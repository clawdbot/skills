# Clawd Anatomy

Technical breakdown of Clawd's structure in Claude Code.

## Rendering Technology

- **Framework**: Ink (React for command-line interfaces)
- **Components**: `$` = styled Text component with color/backgroundColor props
- **File**: `cli.js` (~10.7MB bundled JavaScript)
- **Location**: `/opt/node22/lib/node_modules/@anthropic-ai/claude-code/cli.js`

## Color System

Clawd uses two color keys defined in theme objects:

```javascript
// True-color terminals (24-bit RGB)
clawd_body: "rgb(215,119,87)"      // Coral/terracotta
clawd_background: "rgb(0,0,0)"     // Black

// ANSI fallback (8/16-color terminals)
clawd_body: "ansi:redBright"
clawd_background: "ansi:black"
```

There are 4+ theme definitions in cli.js (light mode, dark mode, etc.), each containing these color keys.

## Small Clawd (Prompt Icon)

Rendered by function `gZ0()` (standard terminals) and `vz3()` (Apple Terminal).

### Standard Terminal Version
```
 ▐▛███▜▌
▝▜█████▛▘
  ▘▘ ▝▝
```

**JSX structure** (simplified):
```jsx
<Box flexDirection="column">
  <Text>
    <Text color="clawd_body"> ▐</Text>
    <Text color="clawd_body" backgroundColor="clawd_background">▛███▜</Text>
    <Text color="clawd_body">▌</Text>
  </Text>
  <Text>
    <Text color="clawd_body">▝▜</Text>
    <Text color="clawd_body" backgroundColor="clawd_background">█████</Text>
    <Text color="clawd_body">▛▘</Text>
  </Text>
  <Text color="clawd_body">  ▘▘ ▝▝  </Text>
</Box>
```

### Apple Terminal Version
```
▗ ▗   ▖ ▖
         (7 spaces with background)
▘▘ ▝▝
```

Uses inverted colors (background as foreground) for compatibility.

## Large Clawd (Loading Screen)

Appears on the welcome/loading screen with stars animation.

```
      ░█████████░
      ██▄█████▄██    ← ears (▄ lower half blocks)
      ░█████████░
      █ █   █ █      ← eyes/feet
```

Integrated into a larger scene with:
- Animated stars (`*` characters that move)
- Light shade characters (`░▒▓`) for atmosphere
- Dotted lines (`…………`) for ground

## Pattern Locations in cli.js

Search patterns to find Clawd code:
```bash
# Color definitions
grep -o 'clawd_body:"[^"]*"' cli.js

# Small Clawd patterns
grep -o '"▛███▜"' cli.js
grep -o '"▘▘ ▝▝"' cli.js

# Large Clawd patterns
grep -o '"██▄█████▄██"' cli.js
grep -o '"█ █   █ █"' cli.js

# Rendering functions
grep -o 'function [a-zA-Z0-9_]*().*clawd' cli.js
```

## Modification Points

| What to change | Pattern to find | Example replacement |
|---------------|-----------------|---------------------|
| Body color (RGB) | `clawd_body:"rgb(215,119,87)"` | `clawd_body:"rgb(100,149,237)"` |
| Body color (ANSI) | `clawd_body:"ansi:redBright"` | `clawd_body:"ansi:blueBright"` |
| Add left arm | `" ▐"` | `"╱▐"` |
| Add right arm | `"▌")` | `"▌╲")` |
| Modify head | `"▛███▜"` | Custom pattern |
| Modify feet | `"▘▘ ▝▝"` | Custom pattern |

## Ink ANSI Color Reference

Available ANSI colors for `clawd_body`:
- `ansi:black`, `ansi:red`, `ansi:green`, `ansi:yellow`
- `ansi:blue`, `ansi:magenta`, `ansi:cyan`, `ansi:white`
- Bright variants: `ansi:blackBright`, `ansi:redBright`, etc.
