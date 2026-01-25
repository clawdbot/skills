---
name: omnifocus
description: Manage OmniFocus tasks, projects, and folders via Omni Automation. Use for task management, to-do lists, project tracking, GTD workflows, adding/completing/editing tasks, setting due dates, managing tags, and recurring tasks. Requires OmniFocus installed on macOS.
---

# OmniFocus

Control OmniFocus via JXA (JavaScript for Automation).

## Requirements

- macOS with OmniFocus 3 or 4 installed
- OmniFocus must be running (or will auto-launch)

## Quick Reference

```bash
# Run via the wrapper script
./scripts/of <command> [args...]

# Or directly
osascript -l JavaScript ./scripts/omnifocus.js <command> [args...]
```

## Commands

### List/Query

| Command | Description |
|---------|-------------|
| `inbox` | List inbox tasks |
| `folders` | List all folders |
| `projects [folder]` | List projects, optionally filtered by folder |
| `tasks <project>` | List tasks in a project |
| `tags` | List all tags |
| `today` | Tasks due today or overdue |
| `flagged` | Flagged incomplete tasks |
| `search <query>` | Search tasks by name |
| `info <taskId>` | Full task details |

### Create

| Command | Description |
|---------|-------------|
| `add <name> [project]` | Add task to inbox or project |
| `newproject <name> [folder]` | Create project |
| `newfolder <name>` | Create top-level folder |
| `newtag <name>` | Create or get tag |

### Modify

| Command | Description |
|---------|-------------|
| `complete <taskId>` | Mark complete |
| `uncomplete <taskId>` | Mark incomplete |
| `delete <taskId>` | Permanently delete |
| `rename <taskId> <name>` | Rename task |
| `note <taskId> <text>` | Append to note |
| `setnote <taskId> <text>` | Replace note |
| `defer <taskId> <date>` | Set defer date (YYYY-MM-DD) |
| `due <taskId> <date>` | Set due date |
| `flag <taskId> [true\|false]` | Set flagged |
| `tag <taskId> <tag>` | Add tag (creates if needed) |
| `untag <taskId> <tag>` | Remove tag |
| `move <taskId> <project>` | Move to project |

### Repeat

```bash
# repeat <taskId> <method> <interval> <unit>
of repeat abc123 fixed 1 weeks
of repeat abc123 due-after-completion 2 days
of repeat abc123 defer-after-completion 1 months
of unrepeat abc123
```

Methods: `fixed`, `due-after-completion`, `defer-after-completion`  
Units: `days`, `weeks`, `months`, `years`

## Output Format

All commands return JSON. Success responses include `"success": true`. Errors include `"error": "message"`.

```json
{
  "success": true,
  "task": {
    "id": "abc123",
    "name": "Task name",
    "note": "Notes here",
    "flagged": false,
    "completed": false,
    "deferDate": "2026-01-30",
    "dueDate": "2026-02-01",
    "project": "Project Name",
    "tags": ["tag1", "tag2"],
    "repeat": {"method": "fixed", "rule": "RRULE:FREQ=WEEKLY;INTERVAL=1"}
  }
}
```

## Examples

```bash
# Add task to inbox
of add "Buy groceries"

# Add task to specific project
of add "Review docs" "Work Projects"

# Set due date and flag
of due abc123 2026-02-01
of flag abc123 true

# Add tags
of tag abc123 "urgent"
of tag abc123 "home"

# Create recurring task
of add "Weekly review" "Habits"
of repeat xyz789 fixed 1 weeks

# Search and complete
of search "groceries"
of complete abc123

# Get today's tasks
of today
```

## Notes

- Task IDs are OmniFocus internal IDs (returned in all task responses)
- Dates use ISO format: YYYY-MM-DD
- Project and folder names are case-sensitive
- Tags are created automatically if they don't exist when using `tag` command
- All output is JSON for easy parsing

## Technical Details

This skill uses JavaScript for Automation (JXA) for most operations, with AppleScript fallbacks for tag and repeat operations (due to known JXA type conversion bugs with these specific OmniFocus APIs).

The hybrid approach provides:
- JSON output for easy parsing
- Robust escaping for special characters in tag names
- Error handling with clear messages

**First run:** OmniFocus may prompt to allow automation access. Enable this in System Settings > Privacy & Security > Automation.
