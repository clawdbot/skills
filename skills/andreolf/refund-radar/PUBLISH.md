# refund-radar

## Metadata

- **Name**: refund-radar
- **Version**: 1.0.0
- **Author**: andreolf
- **Repository**: https://github.com/andreolf/refund-radar
- **License**: MIT

## Description

Local-first bank statement auditor that detects recurring charges, flags suspicious transactions, and drafts ready-to-send refund request templates. Generates interactive HTML reports with privacy toggle.

## Tags

- finance
- bank
- statement
- refund
- subscription
- audit
- privacy
- local-first

## Features

- Parse CSV and text bank statements with auto-detection
- Detect recurring subscriptions with cadence estimation
- Flag duplicates, amount spikes, new merchants, fees
- Generate ready-to-send refund templates (email, chat, dispute)
- Interactive HTML reports with dark/light mode
- Privacy toggle to blur merchant names
- Persistent state for learning preferences
- Zero external dependencies

## Workflow Summary

1. User provides bank statement (CSV or pasted text)
2. Tool parses and normalizes transactions
3. Detects recurring charges automatically
4. Flags suspicious/unexpected charges
5. Asks clarifying questions in batches
6. Generates interactive HTML report
7. Drafts refund request templates
8. Learns from user decisions for future runs

## Requirements

- Python 3.9+
- No external packages required

## Privacy

All processing happens locally. No network calls. No external APIs.

## Screenshots

Report shows:
- Summary cards with totals
- Recurring charges table with next expected dates
- Flagged transactions with severity badges
- Copy-to-clipboard refund templates
- Dark mode and privacy blur toggle
