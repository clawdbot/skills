---
name: prisma-gen
description: Generate Prisma schema from plain English. Use when you need database models fast without writing boilerplate.
---

# Prisma Gen

Stop hand-writing Prisma schemas. Just describe your data model in plain English and get a complete, production-ready schema.prisma file in seconds. No more googling relation syntax or forgetting @unique decorators.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-prisma-gen "a blog with users, posts, comments, and tags"
```

## What It Does

- Generates complete Prisma schema from natural language descriptions
- Handles relations automatically (one-to-many, many-to-many, self-referential)
- Adds proper indexes, constraints, and default values
- Supports all Prisma field types and decorators
- Outputs clean, formatted schema ready to use

## Usage Examples

```bash
# E-commerce database
npx ai-prisma-gen "e-commerce with products, categories, orders, and user reviews"

# SaaS multi-tenant
npx ai-prisma-gen "multi-tenant saas with organizations, teams, users, and role-based permissions"

# Social app
npx ai-prisma-gen "social network with users, friendships, posts, likes, and direct messages"

# Save to file
npx ai-prisma-gen "task management with projects and assignees" > prisma/schema.prisma
```

## Best Practices

- **Be specific about relations** - Say "users have many posts" instead of just "users and posts"
- **Mention unique fields** - Include "email should be unique" if that's what you need
- **Include edge cases** - Soft deletes, timestamps, status enums. Mention them upfront.
- **Review before migrating** - The schema is a starting point. Always check the output matches your needs.

## When to Use This

- Starting a new project and need a database schema fast
- Prototyping an idea and don't want to waste time on boilerplate
- Learning Prisma and want to see how complex relations should look
- Converting a mental model into actual schema code

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
npx ai-prisma-gen --help
```

## How It Works

Takes your plain English description, sends it to GPT with Prisma-specific prompting, and returns a properly formatted schema.prisma file. The AI understands Prisma conventions like @@index, @relation, and common patterns like soft deletes and timestamps.

## License

MIT. Free forever. Use it however you want.
