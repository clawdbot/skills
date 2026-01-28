---
name: nginx-gen
description: Generate nginx configs from plain English. Use when you need reverse proxy, SSL, or load balancing setup.
---

# Nginx Gen

Nginx config syntax is cryptic. This tool generates working nginx configurations from plain English descriptions. Reverse proxies, SSL termination, load balancing, caching. All without memorizing directives.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-nginx "reverse proxy to localhost:3000 with SSL"
```

## What It Does

- Generates nginx.conf or site config files
- Handles reverse proxy, load balancing, and static files
- Sets up SSL/TLS with proper security headers
- Includes caching and compression settings
- Adds comments explaining each directive

## Usage Examples

```bash
# Simple reverse proxy
npx ai-nginx "proxy /api to port 3000, serve static from /var/www"

# Load balancer
npx ai-nginx "load balance between 3 backend servers on ports 3001-3003"

# SSL setup
npx ai-nginx "SSL for example.com with redirect from http"

# WebSocket support
npx ai-nginx "proxy websocket connections to port 8080"
```

## Best Practices

- **Test config before reload** - Always nginx -t first
- **Use include for sites** - Keep main config clean
- **Set proper timeouts** - Defaults are often too short
- **Enable gzip** - The generated configs include compression

## When to Use This

- Setting up a new web server
- Don't remember the proxy_pass syntax
- Need to add SSL to an existing site
- Configuring nginx for a Docker container

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
npx ai-nginx --help
```

## How It Works

Takes your description and generates nginx configuration following best practices. Includes security headers, proper SSL settings, and optimization directives. Comments explain each section so you can customize it.

## License

MIT. Free forever. Use it however you want.
