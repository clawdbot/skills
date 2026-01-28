---
name: sql-writer
description: Convert natural language to SQL queries. Use when you need to write SQL fast.
---

# SQL Writer

Nobody memorizes SQL syntax. You know what data you want, you just can't remember if it's LEFT JOIN or INNER JOIN or whether the WHERE clause goes before GROUP BY. This tool takes plain English and gives you the exact SQL query you need.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-sql "get all users who signed up this month"
```

## What It Does

- Converts plain English descriptions to working SQL queries
- Supports multiple SQL dialects including PostgreSQL, MySQL, and SQLite
- Accepts table schema context for more accurate queries
- Outputs clean, properly formatted SQL ready to run

## Usage Examples

```bash
# Simple query
npx ai-sql "get all users who signed up this month"

# Specify dialect
npx ai-sql "top 10 products by revenue" -d MySQL

# With schema context
npx ai-sql "users who ordered in the last 90 days" -s "users(id,name,email) orders(id,user_id,created_at)"
```

## Best Practices

- **Include your table schema** - Pass table names and columns with --schema for better results
- **Specify your dialect** - PostgreSQL and MySQL have subtle differences
- **Start simple then refine** - Get the basic query right first
- **Review before running** - Always read the generated SQL before running it on production

## When to Use This

- You know what data you want but can't remember the SQL syntax
- Building a quick report
- Learning SQL and want to see how queries should look
- Prototyping database queries before writing them into your app

## Part of the LXGIC Dev Toolkit

This is one of 110+ free developer tools built by LXGIC Studios. No paywalls, no sign-ups, no API keys on free tiers. Just tools that work.

**Find more:**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- Website: https://lxgic.dev

## Requirements

No install needed. Just run with npx. Node.js 18+ recommended.

```bash
npx ai-sql --help
```

## How It Works

The tool sends your natural language description to an AI model that understands SQL. It outputs a properly formatted query in your chosen dialect.

## License

MIT. Free forever. Use it however you want.