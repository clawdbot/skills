---
name: query-optimizer
description: Optimize SQL and Prisma queries using AI. Use when your queries are slow and you need performance help.
---

# Query Optimizer

Slow queries killing your app? Paste your SQL or Prisma code and get optimization suggestions. Index recommendations, query rewrites, N+1 detection. The stuff that takes hours to figure out manually.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-query-optimize "SELECT * FROM users WHERE email LIKE '%@gmail.com'"
```

## What It Does

- Analyzes SQL and Prisma queries for performance issues
- Suggests missing indexes with CREATE INDEX statements
- Rewrites queries to avoid common antipatterns
- Detects N+1 problems in ORM code
- Explains why changes improve performance

## Usage Examples

```bash
# Optimize a SQL query
npx ai-query-optimize "SELECT * FROM orders WHERE created_at > NOW() - INTERVAL '30 days'"

# Analyze a Prisma query file
npx ai-query-optimize queries.ts

# Check for N+1 issues
npx ai-query-optimize src/api/users.ts --check-n-plus-one

# Get index recommendations
npx ai-query-optimize schema.sql --suggest-indexes
```

## Best Practices

- **Include your schema** - Context about tables and existing indexes helps a lot
- **Measure before and after** - EXPLAIN ANALYZE doesn't lie
- **Test with real data** - Optimizations that work on 100 rows might fail on 1M
- **Don't optimize prematurely** - Fix actual slow queries, not theoretical ones

## When to Use This

- Database queries are showing up in your APM as slow
- Users are complaining about loading times
- You inherited a codebase with questionable query patterns
- Learning SQL optimization and want to understand the patterns

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
npx ai-query-optimize --help
```

## How It Works

Parses your query or code file to understand the data access patterns. Applies database optimization knowledge to identify issues like missing indexes, expensive operations (LIKE with leading wildcards), and ORM antipatterns. Provides specific, actionable fixes.

## License

MIT. Free forever. Use it however you want.
