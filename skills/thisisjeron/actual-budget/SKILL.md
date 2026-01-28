---
name: actual-budget
description: Query and manage personal finances via the official Actual Budget Node.js API. Use for budget queries, transaction imports/exports, account management, categorization, rules, schedules, and bank sync with self-hosted Actual Budget instances.
---

# Actual Budget API

Official Node.js API for [Actual Budget](https://actualbudget.org). Runs headless — works on local budget data synced from your server.

## Installation

```bash
npm install @actual-app/api
```

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `ACTUAL_SERVER_URL` | Yes | Server URL (e.g., `https://actual.example.com`) |
| `ACTUAL_PASSWORD` | Yes | Server password |
| `ACTUAL_SYNC_ID` | Yes | Budget Sync ID (Settings → Advanced → Sync ID) |
| `ACTUAL_DATA_DIR` | No | Local cache directory for budget data (defaults to cwd) |
| `ACTUAL_ENCRYPTION_PASSWORD` | No | E2E encryption password, if enabled |
| `NODE_TLS_REJECT_UNAUTHORIZED` | No | Set to `0` for self-signed certs |

## Quick Start

```javascript
const api = require('@actual-app/api');

await api.init({
  dataDir: process.env.ACTUAL_DATA_DIR || '/tmp/actual-cache',
  serverURL: process.env.ACTUAL_SERVER_URL,
  password: process.env.ACTUAL_PASSWORD,
});

await api.downloadBudget(
  process.env.ACTUAL_SYNC_ID,
  process.env.ACTUAL_ENCRYPTION_PASSWORD ? { password: process.env.ACTUAL_ENCRYPTION_PASSWORD } : undefined
);

// ... do work ...

await api.shutdown();
```

## Core Concepts

- **Amounts** are integers in cents: `$50.00` = `5000`, `-1200` = expense of $12.00
- **Dates** use `YYYY-MM-DD`, months use `YYYY-MM`
- **IDs** are UUIDs — use `getIDByName(type, name)` to look up by name
- Convert with `api.utils.amountToInteger(123.45)` → `12345`

## Common Operations

### Get Budget Overview
```javascript
const months = await api.getBudgetMonths();        // ['2026-01', '2026-02', ...]
const jan = await api.getBudgetMonth('2026-01');   // { categoryGroups, incomeAvailable, ... }
```

### Accounts
```javascript
const accounts = await api.getAccounts();
const balance = await api.getAccountBalance(accountId);
const newId = await api.createAccount({ name: 'Checking', type: 'checking' }, 50000); // $500 initial
await api.closeAccount(id, transferToAccountId);  // transfer remaining balance
```

### Transactions
```javascript
// Get transactions for date range
const txns = await api.getTransactions(accountId, '2026-01-01', '2026-01-31');

// Import with deduplication + rules (preferred for bank imports)
const { added, updated } = await api.importTransactions(accountId, [
  { date: '2026-01-15', amount: -2500, payee_name: 'Grocery Store', notes: 'Weekly run' },
  { date: '2026-01-16', amount: -1200, payee_name: 'Coffee Shop', imported_id: 'bank-123' },
]);

// Update a transaction
await api.updateTransaction(txnId, { category: categoryId, cleared: true });
```

### Categories & Payees
```javascript
const categories = await api.getCategories();
const groups = await api.getCategoryGroups();
const payees = await api.getPayees();

// Create
const catId = await api.createCategory({ name: 'Subscriptions', group_id: groupId });
const payeeId = await api.createPayee({ name: 'Netflix', category: catId });
```

### Budget Amounts
```javascript
await api.setBudgetAmount('2026-01', categoryId, 30000);  // budget $300
await api.setBudgetCarryover('2026-01', categoryId, true);
```

### Rules
```javascript
const rules = await api.getRules();
await api.createRule({
  stage: 'pre',
  conditionsOp: 'and',
  conditions: [{ field: 'payee', op: 'is', value: payeeId }],
  actions: [{ op: 'set', field: 'category', value: categoryId }],
});
```

### Schedules
```javascript
const schedules = await api.getSchedules();
await api.createSchedule({
  payee: payeeId,
  account: accountId,
  amount: -1500,
  date: { frequency: 'monthly', start: '2026-01-01', interval: 1, endMode: 'never' },
});
```

### Bank Sync
```javascript
await api.runBankSync({ accountId });  // GoCardless/SimpleFIN
```

### Sync & Shutdown
```javascript
await api.sync();      // push/pull changes to server
await api.shutdown();  // always call when done
```

## ActualQL Queries

For complex queries, use ActualQL:

```javascript
const { q, runQuery } = require('@actual-app/api');

// Sum expenses by category this month
const { data } = await runQuery(
  q('transactions')
    .filter({
      date: [{ $gte: '2026-01-01' }, { $lte: '2026-01-31' }],
      amount: { $lt: 0 },
    })
    .groupBy('category.name')
    .select(['category.name', { total: { $sum: '$amount' } }])
);

// Search transactions
const { data } = await runQuery(
  q('transactions')
    .filter({ 'payee.name': { $like: '%grocery%' } })
    .select(['date', 'amount', 'payee.name', 'category.name'])
    .orderBy({ date: 'desc' })
    .limit(20)
);
```

**Operators:** `$eq`, `$lt`, `$lte`, `$gt`, `$gte`, `$ne`, `$oneof`, `$regex`, `$like`, `$notlike`
**Splits:** `.options({ splits: 'inline' | 'grouped' | 'all' })`

## Helpers

```javascript
// Look up ID by name
const acctId = await api.getIDByName('accounts', 'Checking');
const catId = await api.getIDByName('categories', 'Food');
const payeeId = await api.getIDByName('payees', 'Amazon');

// List budgets
const budgets = await api.getBudgets();  // local + remote files
```

## Transfers

Transfers use special payees. Find transfer payee by `transfer_acct` field:
```javascript
const payees = await api.getPayees();
const transferPayee = payees.find(p => p.transfer_acct === targetAccountId);
await api.importTransactions(fromAccountId, [
  { date: '2026-01-15', amount: -10000, payee: transferPayee.id }
]);
```

## Split Transactions

```javascript
await api.importTransactions(accountId, [{
  date: '2026-01-15',
  amount: -5000,
  payee_name: 'Costco',
  subtransactions: [
    { amount: -3000, category: groceryCatId },
    { amount: -2000, category: householdCatId },
  ]
}]);
```

## Bulk Import (New Budget)

For migrating from another app:
```javascript
await api.runImport('My-New-Budget', async () => {
  for (const acct of myData.accounts) {
    const id = await api.createAccount(acct);
    await api.addTransactions(id, myData.transactions.filter(t => t.acctId === id));
  }
});
```

## Reference

Full API: https://actualbudget.org/docs/api/reference
ActualQL: https://actualbudget.org/docs/api/actual-ql