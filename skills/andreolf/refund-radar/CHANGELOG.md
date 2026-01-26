# Changelog

All notable changes to refund-radar will be documented in this file.

## [1.0.0] - 2026-01-26

### Added

- Initial release
- CSV parser with auto-detection of delimiter, date format, and amount format
- Text parser for pasted transaction data
- Recurring charge detection (frequency, amount similarity, cadence, subscription keywords)
- Unexpected charge detection:
  - New merchant (first time + amount > $30)
  - Amount spike (> 1.8x baseline, delta > $25)
  - Duplicate (same merchant + amount within 2 days)
  - Fee-like (ATM, overdraft, service fees > $3)
  - Currency anomaly (unusual currency or DCC indicator)
  - Missing refund (disputed charge without reversal in 14 days)
- Refund template generation (email, chat, bank dispute)
- Three tone variants (concise, firm, friendly)
- Interactive HTML report with:
  - Dark/light mode toggle
  - Privacy blur toggle
  - Collapsible sections
  - Copy-to-clipboard for templates
  - Auto-hide empty sections
- Persistent state storage (~/.refund_radar/state.json)
- CLI commands: analyze, mark-expected, mark-recurring, expected, reset-state, export
- Local-first, privacy-first: no network calls, no external APIs
