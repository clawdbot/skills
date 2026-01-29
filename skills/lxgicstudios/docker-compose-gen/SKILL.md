---
name: compose-gen
description: Generate docker-compose.yml by scanning your project. Use when containerizing an existing app.
---

# Compose Gen

Writing docker-compose from scratch is tedious. This tool scans your project, detects services, and generates a working docker-compose.yml. Database, cache, your app, all wired up correctly.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-docker-compose
```

## What It Does

- Scans your project to detect services needed
- Generates docker-compose.yml with proper networking
- Includes database, cache, and queue services as needed
- Sets up volumes for persistence
- Adds health checks and depends_on

## Usage Examples

```bash
# Generate for current project
npx ai-docker-compose

# Specify services manually
npx ai-docker-compose --services postgres,redis,app

# Include development overrides
npx ai-docker-compose --with-dev

# Output to specific file
npx ai-docker-compose > docker-compose.yml
```

## Best Practices

- **Use named volumes** - Don't lose your data on container restart
- **Add health checks** - Make depends_on actually wait for services
- **Separate dev and prod** - Use docker-compose.override.yml for dev settings
- **Pin image versions** - postgres:latest will break eventually

## When to Use This

- Containerizing an existing application
- Don't remember the docker-compose syntax
- Need a quick local development environment
- Setting up a new service and need the boilerplate

## Part of the LXGIC Dev Toolkit

This is one of 110+ free developer tools built by LXGIC Studios. No paywalls, no sign-ups, no API keys on free tiers. Just tools that work.

**Find more:**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- Website: https://lxgicstudios.com

## Requirements

No install needed. Just run with npx. Node.js 18+ recommended. Requires OPENAI_API_KEY environment variable.

```bash
export OPENAI_API_KEY=sk-...
npx ai-docker-compose --help
```

## How It Works

Scans package.json, requirements.txt, or other config files to detect your stack. Identifies database connections, cache usage, and external service dependencies. Generates docker-compose.yml with appropriate services, networks, and volumes.

## License

MIT. Free forever. Use it however you want.
