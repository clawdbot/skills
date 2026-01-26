---
name: refund-radar
description: Scan bank statements to detect recurring charges, flag suspicious transactions, and draft refund requests with interactive HTML reports.
---

# refund-radar

Scan bank statements to detect recurring charges, flag suspicious transactions, identify duplicates and fees, draft refund request templates, and generate an interactive HTML audit report.

## Triggers

- "scan my bank statement for refunds"
- "analyze my credit card transactions"
- "find recurring charges in my statement"
- "check for duplicate or suspicious charges"
- "help me dispute a charge"
- "generate a refund request"
- "audit my subscriptions"

## Workflow

### 1. Get Transaction Data

Ask user for bank/card CSV export or pasted text. Common sources:

- Apple Card: Wallet → Card Balance → Export
- Chase: Accounts → Download activity → CSV
- Mint: Transactions → Export
- Any bank: Download as CSV from transaction history

Or accept pasted text format:
```
2026-01-03 Spotify -11.99 USD
2026-01-15 Salary +4500 USD
```

### 2. Parse and Normalize

Run the parser on their data:

```bash
python -m refund_radar analyze --csv statement.csv --month 2026-01
```

Or for pasted text:
```bash
python -m refund_radar analyze --stdin --month 2026-01 --default-currency USD
```

The parser auto-detects:
- Delimiter (comma, semicolon, tab)
- Date format (YYYY-MM-DD, DD/MM/YYYY, MM/DD/YYYY)
- Amount format (single column or debit/credit)
- Currency

### 3. Review Recurring Charges

Tool identifies recurring subscriptions by:
- Same merchant >= 2 times in 90 days
- Similar amounts (within 5% or $2)
- Consistent cadence (weekly, monthly, yearly)
- Known subscription keywords (Netflix, Spotify, etc.)

Output shows:
- Merchant name
- Average amount and cadence
- Last charge date
- Next expected charge

### 4. Flag Suspicious Charges

Tool automatically flags:

| Flag Type | Trigger | Severity |
|-----------|---------|----------|
| Duplicate | Same merchant + amount within 2 days | HIGH |
| Amount Spike | > 1.8x baseline, delta > $25 | HIGH |
| New Merchant | First time + amount > $30 | MEDIUM |
| Fee-like | Keywords (FEE, ATM, OVERDRAFT) + > $3 | LOW |
| Currency Anomaly | Unusual currency or DCC | LOW |

### 5. Clarify with User

For flagged items, ask in batches of 5-10:

- Is this charge legitimate?
- Should I mark this merchant as expected?
- Do you want a refund template for this?

Update state based on answers:
```bash
python -m refund_radar mark-expected --merchant "Costco"
python -m refund_radar mark-recurring --merchant "Netflix"
```

### 6. Generate HTML Report

Report saved to `~/.refund_radar/reports/YYYY-MM.html`

Copy [template.html](assets/template.html) structure. Sections:
- **Summary**: Transaction count, total spent, recurring count, flagged count
- **Recurring Charges**: Table with merchant, amount, cadence, next expected
- **Unexpected Charges**: Flagged items with severity and reason
- **Duplicates**: Same-day duplicate charges
- **Fee-like Charges**: ATM fees, FX fees, service charges
- **Refund Templates**: Ready-to-copy email/chat/dispute messages

Features:
- Privacy toggle (blur merchant names)
- Dark/light mode
- Collapsible sections
- Copy buttons on templates
- Auto-hide empty sections

### 7. Draft Refund Requests

For each flagged charge, generate three template types:
- **Email**: Formal refund request
- **Chat**: Quick message for live support
- **Dispute**: Bank dispute form text

Three tone variants each:
- Concise (default)
- Firm (assertive)
- Friendly (polite)

Templates include:
- Merchant name and date
- Charge amount
- Dispute reason based on flag type
- Placeholders for card last 4, reference number

**Important**: No apostrophes in any generated text.

## CLI Reference

```bash
# Analyze statement
python -m refund_radar analyze --csv file.csv --month 2026-01

# Analyze from stdin
python -m refund_radar analyze --stdin --month 2026-01 --default-currency CHF

# Mark merchant as expected
python -m refund_radar mark-expected --merchant "Amazon"

# Mark merchant as recurring
python -m refund_radar mark-recurring --merchant "Netflix"

# List expected merchants
python -m refund_radar expected

# Reset learned state
python -m refund_radar reset-state

# Export month data
python -m refund_radar export --month 2026-01 --out data.json
```

## Files Written

| Path | Purpose |
|------|---------|
| `~/.refund_radar/state.json` | Learned preferences, merchant history |
| `~/.refund_radar/reports/YYYY-MM.html` | Interactive audit report |
| `~/.refund_radar/reports/YYYY-MM.json` | Raw analysis data |

## Privacy

- **No network calls.** Everything runs locally.
- **No external APIs.** No Plaid, no cloud services.
- **Your data stays on your machine.**
- **Privacy toggle in reports.** Blur merchant names with one click.

## Requirements

- Python 3.9+
- No external dependencies

## Repository

https://github.com/andreolf/refund-radar
