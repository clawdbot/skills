---
name: ynab
description: Manage YNAB budgets, accounts, categories, and transactions via CLI.
metadata: {"clawdbot":{"emoji":"💰","requires":{"bins":["ynab"],"env":["YNAB_API_KEY"]},"primaryEnv":"YNAB_API_KEY","install":[{"id":"node","kind":"node","package":"@stephendolan/ynab-cli","bins":["ynab"],"label":"Install ynab-cli (npm)"}]}}
---

# YNAB CLI

Install
```bash
npm i -g @stephendolan/ynab-cli
```

Auth
```bash
# Get API key from https://app.ynab.com/settings/developer
# Then set YNAB_API_KEY env var, or:
ynab auth login
ynab auth status
```

Budgets
```bash
ynab budgets list
ynab budgets view [id]
ynab budgets set-default <id>
```

Accounts
```bash
ynab accounts list
ynab accounts view <id>
ynab accounts transactions <id>
```

Categories
```bash
ynab categories list
ynab categories view <id>
ynab categories transactions <id>
ynab categories budget <id> --month <YYYY-MM> --amount <amount>
```

Transactions
```bash
ynab transactions list
ynab transactions list --account <id> --since <YYYY-MM-DD>
ynab transactions list --approved=false --min-amount 100
ynab transactions search --memo "coffee"
ynab transactions search --payee-name "Amazon"
ynab transactions view <id>
ynab transactions create --account <id> --amount <amount> --date <YYYY-MM-DD>
ynab transactions update <id> --amount <amount>
ynab transactions delete <id>
ynab transactions split <id> --splits '[{"amount": -50.00, "category_id": "xxx"}]'
```

Payees
```bash
ynab payees list
ynab payees view <id>
ynab payees update <id> --name <name>
ynab payees transactions <id>
```

Months
```bash
ynab months list
ynab months view <YYYY-MM>
```

Scheduled
```bash
ynab scheduled list
ynab scheduled view <id>
ynab scheduled delete <id>
```

Raw API
```bash
ynab api GET /budgets
ynab api POST /budgets/{budget_id}/transactions --data '{"transaction": {...}}'
```

Notes
- Amounts are in your budget's currency, not milliunits
- Use `--compact` for minified JSON
- Rate limit: 200 req/hour
- Cannot create categories/groups/payees via API
