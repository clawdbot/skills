---
name: permission-auditor
description: Generate RBAC permission configs from your routes. Use when you need role-based access control without building it from scratch.
---

# Permission Auditor

Your API has 47 routes and no permission system. This tool scans your route handlers and generates RBAC permission configs automatically. It figures out which endpoints need which roles and outputs a config you can plug right into your middleware.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-permission src/routes/
```

## What It Does

- Scans route handlers and API endpoints to map out your permission surface
- Generates role-based access control configurations
- Detects admin-only routes, public routes, and auth-required routes
- Outputs middleware-ready permission configs
- Identifies routes missing auth checks

## Usage Examples

```bash
npx ai-permission src/routes/
npx ai-permission src/api/
npx ai-permission "src/**/*.controller.ts"
```

## Best Practices

- **Start with least privilege** - Default deny, then explicitly grant access
- **Review generated configs** - The tool suggests roles but you know your business logic
- **Keep permissions close to routes** - Don't scatter permission checks across your codebase

## When to Use This

- Building a new API and need to plan permissions
- Retrofitting RBAC onto an existing app
- Auditing which routes have missing auth checks

## Part of the LXGIC Dev Toolkit

This is one of 110+ free developer tools built by LXGIC Studios. No paywalls, no sign-ups, no API keys on free tiers. Just tools that work.

**Find more:**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- Website: https://lxgic.dev

## Requirements

No install needed. Just run with npx. Node.js 18+ recommended.

## How It Works

Scans your route files to extract endpoint definitions, HTTP methods, and existing auth middleware. AI analyzes the patterns to suggest appropriate role assignments and generates a structured RBAC config.

## License

MIT. Free forever. Use it however you want.