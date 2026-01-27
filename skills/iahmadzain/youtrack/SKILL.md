---
name: youtrack
description: Manage YouTrack issues, projects, and workflows via CLI. Use when creating, updating, searching, or commenting on YouTrack issues, listing projects, checking issue states, or automating issue workflows.
metadata: {"clawdbot":{"emoji":"🎫","requires":{"bins":["jq","curl"]}}}
---

# YouTrack CLI

Use `ytctl` (in `scripts/`) for YouTrack issue tracking.

## Setup

Credentials stored in `~/.config/youtrack/config.json`:
```json
{
  "url": "https://your-instance.youtrack.cloud",
  "token": "perm:xxx"
}
```

Or set env vars: `YOUTRACK_URL`, `YOUTRACK_TOKEN`

Generate token: YouTrack → Profile → Account Security → New Token

## Commands

```bash
# List projects
ytctl projects

# List issues (with optional filters)
ytctl issues                           # all issues
ytctl issues SP                        # issues in project SP
ytctl issues SP --query "state: Open"  # filtered
ytctl issues --max 50                  # limit results

# Get issue details
ytctl issue SP-123

# Create issue
ytctl create SP "Bug: Login fails"
ytctl create SP "Feature request" "Detailed description here"

# Update issue
ytctl update SP-123 state "In Progress"
ytctl update SP-123 assignee john.doe
ytctl update SP-123 priority Critical

# Add comment
ytctl comment SP-123 "Investigating this now"

# Search with YouTrack query syntax
ytctl search "project: SP state: Open assignee: me"
ytctl search "created: today"
ytctl search "#unresolved sort by: priority"

# List workflow states for project
ytctl states SP

# List users
ytctl users
ytctl users --query "john"
```

## Query Syntax

YouTrack query examples:
- `state: Open` — by state
- `assignee: me` — assigned to current user
- `created: today` — created today
- `updated: {last week}` — updated in last week
- `#unresolved` — all unresolved
- `has: attachments` — with attachments
- `sort by: priority desc` — sorted

Combine: `project: SP state: Open assignee: me sort by: updated`

## Output

Default: table format. Add `--json` for raw JSON output:
```bash
ytctl issues SP --json
ytctl issue SP-123  # always JSON for single issue
```

## Bulk Operations

```bash
# Update all matching issues (with dry-run preview)
ytctl bulk-update "project: SP state: Open" state "In Progress" --dry-run
ytctl bulk-update "project: SP state: Open" state "In Progress"

# Comment on all matching issues
ytctl bulk-comment "project: SP state: Open" "Batch update notice"

# Assign all matching issues
ytctl bulk-assign "project: SP #unresolved" john.doe --dry-run
```

## Reports

```bash
# Project summary (default 7 days)
ytctl report SP
ytctl report SP --days 14

# User activity report
ytctl report-user zain
ytctl report-user zain --days 30

# State distribution with bar chart
ytctl report-states SP
```

## Notes

- Project can be shortName (SP) or full name
- Fields: state, summary, description, assignee, priority
- Use `ytctl states PROJECT` to see valid state names
- Bulk operations support `--dry-run` to preview before executing
