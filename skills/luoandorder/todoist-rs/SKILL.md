---
name: todoist
description: Manage Todoist tasks. Use when the user mentions "todoist", "my tasks", "task list", "add a task", "complete task", or wants to interact with their Todoist account.
homepage: https://github.com/LuoAndOrder/todoist-rs
metadata: {"clawdbot":{"emoji":"✅","requires":{"bins":["td"]},"install":[{"id":"brew","kind":"brew","formula":"LuoAndOrder/tap/todoist-cli","bins":["td"],"label":"Install todoist-cli via Homebrew"}]}}
---

# Todoist Integration

Manage tasks via `td` CLI (todoist-rs).

## Installation

```bash
brew install LuoAndOrder/tap/todoist-cli
```

Or install via Cargo: `cargo install todoist-cli-rs`

## Sync Behavior

- **Writes auto-sync**: `add`, `done`, `edit`, `delete` hit the API directly
- **Reads use cache**: `list`, `today`, `show` read from local cache
- **Sync when needed**: Use `--sync` flag or `td sync` for fresh data

```bash
td sync              # Incremental sync (fast)
td sync --full       # Full rebuild if cache seems off
```

## Common Operations

### List Tasks

```bash
# Today's agenda (includes overdue)
td today --sync

# Today only (no overdue)
td today --no-overdue

# All tasks
td list --sync

# By project
td list -p "Inbox" --sync
td list -p "Work" --sync

# High priority
td list -f "p1 | p2" --sync

# By label
td list -l "urgent" --sync

# Complex filters
td list -f "today & p1" --sync
td list -f "(today | overdue) & !@waiting_on" --sync
```

### Add Tasks

Quick add (natural language):
```bash
td quick "Buy milk tomorrow @errands #Personal"
td quick "Review PR tomorrow" --note "Check the auth changes carefully"
```

Structured add:
```bash
td add "Task content" \
  -p "Inbox" \
  -P 2 \
  -d "today" \
  -l "urgent"

# With description
td add "Prepare quarterly report" -P 1 -d "friday" \
  --description "Include sales metrics and customer feedback summary"
```

Options:
- `-P, --priority` - 1 (highest) to 4 (lowest, default)
- `-p, --project` - project name
- `-d, --due` - due date ("today", "tomorrow", "2026-01-30", "next monday")
- `-l, --label` - label (repeat for multiple)
- `--description` - task description/notes (shown below task title)
- `--section` - target section within project
- `--parent` - parent task ID (creates subtask)

### Complete Tasks

```bash
td done <task-id>
td done <id1> <id2> <id3>              # Multiple at once
td done <id> --all-occurrences         # End recurring task permanently
```

### Modify Tasks

```bash
td edit <task-id> -c "New content"
td edit <task-id> --description "Additional notes here"
td edit <task-id> -P 1
td edit <task-id> -d "tomorrow"
td edit <task-id> --add-label "urgent"
td edit <task-id> --remove-label "next"
td edit <task-id> --no-due             # Remove due date
td edit <task-id> --section "Next Actions"
td edit <task-id> -p "Work"            # Move to different project
```

Edit options:
- `-c, --content` - update task title
- `--description` - update task description/notes
- `-P, --priority` - change priority (1-4)
- `-d, --due` - change due date
- `--no-due` - remove due date
- `-l, --label` - replace all labels
- `--add-label` - add a label
- `--remove-label` - remove a label
- `-p, --project` - move to different project
- `--section` - move to section within project

### Show Task Details

```bash
td show <task-id>
td show <task-id> --comments
```

### Delete Tasks

```bash
td delete <task-id>
```

### Reopen Completed Tasks

```bash
td reopen <task-id>
```

## Project & Label Management

```bash
# Projects
td projects                            # List all
td projects add "New Project"
td projects show <id>

# Labels
td labels                              # List all
td labels add "urgent"
```

## Filter Syntax

Use with `-f/--filter`:
- `|` for OR: `today | overdue`
- `&` for AND: `@next & #Personal`
- Parentheses: `(today | overdue) & p1`
- Negation: `!@waiting_on`
- Priority: `p1`, `p2`, `p3`, `p4`
- Dates: `today`, `tomorrow`, `overdue`, `no date`, `7 days`

## Workflow Tips

1. **Morning review**: `td today --sync`
2. **Quick capture**: `td quick "thing to do"`
3. **Focus list**: `td list -f "@next" --sync`
4. **Waiting on**: `td list -f "@waiting_on" --sync`
5. **End of day**: `td today` (cache is fine, already synced)
