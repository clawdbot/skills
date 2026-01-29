---
name: naming-gen
description: Suggest better variable and function names in your code. Use when improving code readability.
---

# Naming Gen

You have a variable called "data2" and a function called "processStuff". This tool analyzes your code and suggests better names. Clear, descriptive names that tell you what things actually do. Because naming is hard and you shouldn't have to suffer.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-naming ./src/utils.ts
```

## What It Does

- Analyzes variable and function names in your code
- Suggests clearer, more descriptive alternatives
- Identifies vague names like "temp", "data", "result"
- Respects your project's naming conventions
- Shows context for why each suggestion is better

## Usage Examples

```bash
# Analyze a single file
npx ai-naming ./src/processor.ts

# Analyze all files in a directory
npx ai-naming ./src/

# Only flag the worst offenders
npx ai-naming ./src --threshold 3

# Output suggestions as a checklist
npx ai-naming ./src --format checklist
```

## Best Practices

- **Fix the vague ones first** - "data", "temp", "result" are the worst offenders
- **Consider the scope** - Short names are fine for tiny scopes. Long names for wide scopes.
- **Be consistent** - If you call it "user" somewhere, don't call it "customer" elsewhere
- **Don't over-abbreviate** - "usr" doesn't save enough characters to justify the confusion

## When to Use This

- Reviewing code before a PR
- Refactoring legacy code with cryptic variable names
- Learning to write more readable code
- Code review prep when you know your names are lazy

## Part of the LXGIC Dev Toolkit

This is one of 110+ free developer tools built by LXGIC Studios. No paywalls, no sign-ups, no API keys on free tiers. Just tools that work.

**Find more:**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- Website: https://lxgicstudios.com

## Requirements

No install needed. Just run with npx. Node.js 18+ recommended.

```bash
npx ai-naming --help
```

## How It Works

The tool parses your source code, identifies all variable and function names, analyzes what each one actually does by looking at how it's used, then suggests names that better describe the purpose and content.

## License

MIT. Free forever. Use it however you want.
