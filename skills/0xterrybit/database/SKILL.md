---
name: database
description: Database management and queries. Connect to SQL and NoSQL databases, run queries, and manage schemas.
metadata: {"clawdbot":{"emoji":"🗄️","always":true,"requires":{"bins":["curl","jq"]}}}
---

# Database 🗄️

Database management and queries.

## Supported Databases

- PostgreSQL
- MySQL
- SQLite
- MongoDB
- Redis

## Features

- Run SQL queries
- Schema management
- Data export/import
- Backup and restore
- Performance monitoring

## Usage Examples

```
"Show all tables in database"
"Run query: SELECT * FROM users LIMIT 10"
"Export table to CSV"
```

## Safety Rules

1. **ALWAYS** confirm before DELETE/DROP operations
2. **WARN** about queries without WHERE clause
