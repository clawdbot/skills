---
name: swagger-gen
description: Generate OpenAPI specs from Express routes. Use when documenting APIs.
---

# Swagger Generator

Your API has no documentation. This reads your Express routes and generates a complete OpenAPI 3.0 spec.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-swagger ./src/routes/
```

## What It Does

- Reads your Express route files
- Generates OpenAPI 3.0 specification
- Documents request/response shapes
- Ready for Swagger UI

## Usage Examples

```bash
# Generate from routes
npx ai-swagger ./src/routes/

# Single file
npx ai-swagger ./src/routes/users.ts -o docs/api.yaml
```

## Best Practices

- **Keep it updated** - regenerate when routes change
- **Add descriptions** - explain what endpoints do
- **Include examples** - show sample requests
- **Document errors** - not just happy paths

## When to Use This

- Creating API documentation
- Setting up Swagger UI
- Onboarding API consumers
- API-first design

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
npx ai-swagger --help
```

## How It Works

Parses your Express route definitions to extract endpoints, methods, and handler code. Then generates OpenAPI spec with proper types and descriptions.

## License

MIT. Free forever. Use it however you want.
