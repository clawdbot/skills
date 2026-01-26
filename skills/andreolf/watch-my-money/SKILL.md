---
name: watch-my-money
description: Analyze bank transactions, categorize spending, track monthly budgets, detect overspending and anomalies. Outputs interactive HTML report.
triggers:
  - "track spending"
  - "check my budget"
  - "analyze transactions"
  - "what did I spend on"
  - "am I overspending"
  - "budget tracker"
  - "spending analysis"
  - "monthly expenses"
formats:
  - CSV bank exports
  - Text transaction lists
outputs:
  - Interactive HTML report
  - JSON data export
  - Console summary
privacy: local-only
---

# watch-my-money

Analyze transactions, categorize spending, track budgets, flag overspending.

## Workflow

### 1. Get Transactions

Ask user for bank/card CSV export OR pasted text.

Common sources:
- Download CSV from your bank's online portal
- Export from budgeting apps
- Copy/paste transactions from statements

Supported formats:
- Any CSV with date, description, amount columns
- Pasted text: "2026-01-03 Starbucks -5.40 CHF"

### 2. Parse & Normalize

Read input, normalize to standard format:
- Auto-detect delimiter (comma, semicolon, tab)
- Parse dates (YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY)
- Normalize amounts (expenses negative, income positive)
- Extract merchant from description
- Detect recurring transactions (subscriptions)

### 3. Categorize Transactions

For each transaction, assign category:

**Categories:**
- rent, utilities, subscriptions, groceries, eating_out
- transport, travel, shopping, health
- income, transfers, other

Categorization order:
1. Check saved merchant overrides
2. Apply deterministic keyword rules (see [common-merchants.md](references/common-merchants.md))
3. Pattern matching (subscriptions, utilities)
4. Heuristic fallback

For ambiguous merchants (batch of 5-10), ask user to confirm.
Save overrides for future runs.

### 4. Check Budgets

Compare spending against user-defined budgets.

Alert thresholds:
- 80% - approaching limit (yellow)
- 100% - at limit (red)
- 120% - over budget (red, urgent)

See [budget-templates.md](references/budget-templates.md) for suggested budgets.

### 5. Detect Anomalies

Flag unusual spending:
- Category spike: spend > 1.5x baseline AND delta > 50
- Subscription growth: subscriptions up > 20%
- New expensive merchant: first appearance AND spend > 30
- Potential subscriptions: recurring same-amount charges

Baseline = previous 3 months average (or current month if no history).

### 6. Generate HTML Report

Create local HTML file with:
- Month summary (income, expenses, net)
- Category breakdown with budget status
- Top merchants
- Alerts section
- Recurring transactions detected
- Privacy toggle (blur amounts/merchants)

Copy [template.html](assets/template.html) and inject data.

### 7. Save State

Persist to `~/.watch_my_money/`:
- `state.json` - budgets, merchant overrides, history
- `reports/YYYY-MM.json` - machine-readable monthly data
- `reports/YYYY-MM.html` - interactive report

## CLI Commands

```bash
# Analyze CSV
python -m watch_my_money analyze --csv path/to/file.csv --month 2026-01

# Analyze from stdin
cat transactions.txt | python -m watch_my_money analyze --stdin --month 2026-01 --default-currency CHF

# Compare months
python -m watch_my_money compare --months 2026-01 2025-12

# Set budget
python -m watch_my_money set-budget --category groceries --amount 500 --currency CHF

# View budgets
python -m watch_my_money budgets

# Export month data
python -m watch_my_money export --month 2026-01 --out summary.json

# Reset all state
python -m watch_my_money reset-state
```

## Output Structure

Console shows:
- Month summary with income/expenses/net
- Category table with spend vs budget
- Recurring transactions detected
- Top 5 merchants
- Alerts as bullet points

Files written:
- `~/.watch_my_money/state.json`
- `~/.watch_my_money/reports/2026-01.json`
- `~/.watch_my_money/reports/2026-01.html`

## HTML Report Features

- Collapsible category sections
- Budget progress bars
- Recurring transaction list
- Month-over-month comparison
- Privacy toggle (blur sensitive data)
- Dark mode (respects system preference)
- Floating action button
- Screenshot-friendly layout
- Auto-hide empty sections

## Privacy

All data stays local. No network calls. No external APIs.
Transaction data is analyzed locally and stored only in `~/.watch_my_money/`.
