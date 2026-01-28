---
name: next-config-gen
description: Generate Next.js config with best practices. Use when configuring Next.js.
---

# Next Config Generator

next.config.js has a million options. This tool reads your project and generates a config with sensible defaults and the features you actually need.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-next-config
```

## What It Does

- Analyzes your Next.js project
- Generates optimized next.config.mjs
- Includes image domains, rewrites, and headers
- Sets up best practice defaults

## Usage Examples

```bash
# Generate from current project
npx ai-next-config

# Output as CommonJS
npx ai-next-config -o next.config.js
```

## Best Practices

- **Enable strict mode** - catch issues early
- **Configure image domains** - external images need allowlisting
- **Set security headers** - HTTPS, CSP, etc.
- **Use rewrites carefully** - they can affect caching

## When to Use This

- Starting a new Next.js project
- Upgrading to latest Next.js version
- Adding features like image optimization
- Cleaning up messy config

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
npx ai-next-config --help
```

## How It Works

Reads your package.json and project structure to understand what features you're using. Then generates a next.config with appropriate settings for images, headers, redirects, and experimental features.

## License

MIT. Free forever. Use it however you want.
