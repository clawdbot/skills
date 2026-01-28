---
name: validator-gen
description: Generate Zod and Yup validation schemas from TypeScript types. Use when you need runtime validation that matches your types.
---

# Validator Gen

Your TypeScript types don't validate at runtime. This tool generates Zod or Yup schemas that match your existing types. Type safety meets runtime validation without writing everything twice.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-validator types.ts
```

## What It Does

- Generates Zod or Yup schemas from TypeScript interfaces and types
- Handles nested objects, arrays, unions, and optional fields
- Adds sensible constraints like email formats, min/max lengths
- Includes error messages that make sense to users
- Outputs ready-to-use validation code

## Usage Examples

```bash
# Generate Zod schemas from your types
npx ai-validator src/types/user.ts

# Use Yup instead
npx ai-validator src/types/user.ts --library yup

# Include custom error messages
npx ai-validator src/types/user.ts --with-messages

# Save to file
npx ai-validator src/types/user.ts > src/validators/user.ts
```

## Best Practices

- **Keep types and validators together** - Put them in the same file or adjacent files
- **Infer types from validators** - Use z.infer<typeof schema> for single source of truth
- **Add custom refinements manually** - AI handles structure but you know your business rules
- **Test edge cases** - Validators catch more than you think, make sure that's what you want

## When to Use This

- Building an API and need request body validation
- Form validation that matches your data types
- Migrating from no validation to typed validation
- Don't want to manually sync types and validators

## Part of the LXGIC Dev Toolkit

This is one of 110+ free developer tools built by LXGIC Studios. No paywalls, no sign-ups, no API keys on free tiers. Just tools that work.

**Find more:**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- Website: https://lxgic.dev

## Requirements

No install needed. Just run with npx. Node.js 18+ recommended. Requires OPENAI_API_KEY environment variable.

```bash
export OPENAI_API_KEY=sk-...
npx ai-validator --help
```

## How It Works

Parses your TypeScript source to extract type definitions. Translates each type into equivalent Zod or Yup schema code with appropriate validators for common patterns like emails, URLs, and dates. Preserves structure and optionality from your original types.

## License

MIT. Free forever. Use it however you want.
