---
name: logger-gen
description: Set up structured logging for any framework. Use when configuring logging.
---

# Logger Generator

Structured logging is important but setting it up right takes time. This tool generates production-ready logging config for pino, winston, or bunyan.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-logger pino
```

## What It Does

- Generates logging setup for popular libraries
- Includes request tracking and correlation IDs
- Sets up log rotation and formatting
- Pretty output for development, JSON for production

## Usage Examples

```bash
# Pino setup
npx ai-logger pino

# Winston to file
npx ai-logger winston -o lib/logger.ts

# Edge runtime compatible
npx ai-logger bunyan -e edge
```

## Best Practices

- **Use structured logs** - JSON is searchable
- **Include request IDs** - trace requests across services
- **Log at the right level** - don't info log everything
- **Redact sensitive data** - never log passwords or tokens

## When to Use This

- Starting a new project with proper logging
- Replacing console.log with real logging
- Setting up log aggregation
- Debugging production issues

## Part of the LXGIC Dev Toolkit

This is one of 110+ free developer tools built by LXGIC Studios. No paywalls, no sign-ups, no API keys on free tiers. Just tools that work.

**Find more:**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- Website: https://lxgicstudios.com

## Requirements

No install needed. Just run with npx. Node.js 18+ recommended. Needs OPENAI_API_KEY environment variable.

```bash
npx ai-logger --help
```

## How It Works

Generates complete logging configuration for your chosen library including transports, formatters, and middleware for request logging. Handles environment-specific settings automatically.

## License

MIT. Free forever. Use it however you want.
