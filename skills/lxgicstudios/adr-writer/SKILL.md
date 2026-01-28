---
name: adr-writer
description: Generate Architecture Decision Records with AI. Use when documenting technical decisions.
---

# ADR Writer

Writing Architecture Decision Records is one of those things everyone knows they should do but nobody actually does. Too much boilerplate, too much thinking about format when you should be thinking about the decision itself. This tool fixes that.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-adr "switch from REST to GraphQL"
```

## What It Does

- Generates complete ADRs in standard format (title, context, decision, consequences)
- Handles the boring structure so you focus on the actual decision
- Creates consistent documentation your team can actually reference later
- Works with any architectural decision from database choices to framework migrations

## Usage Examples

```bash
# Database decision
npx ai-adr "use PostgreSQL over MongoDB for transactional data"

# Architecture pattern
npx ai-adr "adopt microservices instead of monolith"

# Framework choice
npx ai-adr "migrate from Express to Fastify"

# Infrastructure
npx ai-adr "move to Kubernetes from Docker Compose"
```

## Best Practices

- **Be specific** - "switch to GraphQL for mobile clients" beats "change API"
- **Include context** - mention why you're making this decision in your description
- **Review the output** - AI gets you 80% there, but add your team's specific context
- **Keep them versioned** - commit ADRs alongside the code they document

## When to Use This

- Starting a new project and need to document initial tech choices
- Making a significant architectural change that future devs will question
- Onboarding new team members who need to understand past decisions
- Satisfying compliance requirements for decision documentation

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
npx ai-adr --help
```

## How It Works

Takes your plain English description of an architectural decision, sends it to GPT-4o-mini with a prompt optimized for ADR format, and returns a complete, well-structured document. The output follows the standard ADR template used by most engineering teams.

## License

MIT. Free forever. Use it however you want.
