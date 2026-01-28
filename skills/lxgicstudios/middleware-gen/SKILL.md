---
name: middleware-gen
description: Generate Express middleware from plain English. Use when building API middleware.
---

# Middleware Generator

Writing middleware means handling edge cases, async errors, and weird Express patterns. Describe what you need and get production-ready middleware.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-middleware "rate limit 100 req/min per IP"
```

## What It Does

- Generates Express middleware from descriptions
- Handles rate limiting, auth, logging, and more
- Includes proper error handling
- TypeScript support built in

## Usage Examples

```bash
# Rate limiting
npx ai-middleware "rate limit 100 req/min per IP"

# JWT auth
npx ai-middleware "JWT auth with role-based access" -t

# Request logging
npx ai-middleware "request logging with response time" -o logger.ts -t

# API key validation
npx ai-middleware "validate API key from header"
```

## Best Practices

- **Order matters** - put auth before route handlers
- **Handle errors** - don't let middleware crash the server
- **Keep it focused** - one middleware, one job
- **Test thoroughly** - middleware affects every request

## When to Use This

- Adding new middleware to an API
- Need common patterns like rate limiting
- Learning middleware best practices
- Prototyping API features quickly

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
npx ai-middleware --help
```

## How It Works

Takes your plain English description and generates Express-compatible middleware code. The AI knows common patterns and includes proper async handling, error handling, and TypeScript types.

## License

MIT. Free forever. Use it however you want.
