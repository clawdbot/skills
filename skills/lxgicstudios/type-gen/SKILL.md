---
name: type-gen
description: Generate TypeScript interfaces from JSON. Use when typing API responses.
---

# Type Generator

You have a JSON response and need TypeScript types. Paste in a JSON file and get clean interfaces back.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-type-gen response.json --name UserResponse
```

## What It Does

- Reads JSON files and generates TypeScript
- Handles nested objects and arrays
- Infers optional fields
- Adds JSDoc comments

## Usage Examples

```bash
# Generate from JSON
npx ai-type-gen response.json --name UserResponse

# Save to file
npx ai-type-gen data.json --name Product --output types/product.ts
```

## Best Practices

- **Name interfaces clearly** - UserResponse, not Data
- **Check optional fields** - JSON can be misleading
- **Handle nulls** - undefined vs null matters
- **Group related types** - keep them together

## When to Use This

- Typing API responses
- Working with external data
- Reverse engineering APIs
- Learning from real data

## Part of the LXGIC Dev Toolkit

This is one of 110+ free developer tools built by LXGIC Studios. No paywalls, no sign-ups, no API keys on free tiers. Just tools that work.

**Find more:**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- Website: https://lxgic.dev

## Requirements

No install needed. Just run with npx. Node.js 18+ recommended. Needs OPENAI_API_KEY environment variable.

```bash
npx ai-type-gen --help
```

## How It Works

Parses your JSON file, analyzes the structure including nested objects and arrays, and generates TypeScript interfaces with proper types and optional fields.

## License

MIT. Free forever. Use it however you want.
