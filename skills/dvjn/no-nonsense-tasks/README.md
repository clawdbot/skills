# No Nonsense Tasks Skill

A lightweight SQLite-based task manager designed for AI agents like [molt.bot](https://molt.bot).

## Quick Start

```bash
# Initialize database
./scripts/init_db.sh

# Add a task
./scripts/task_add.sh "Fix bug" --tags "urgent" --status todo

# List tasks
./scripts/task_list.sh

# Move to in-progress
./scripts/task_move.sh 1 --status in-progress

# Mark as done
./scripts/task_move.sh 1 --status done
```

## Features

- Four task statuses: backlog → todo → in-progress → done
- Tag filtering with exact match
- SQLite database (no external dependencies)
- Migration system for schema evolution
- SQL injection protection
- Designed for AI agent automation

## Commands

```bash
task_add.sh      # Create tasks
task_list.sh     # List and filter by status
task_show.sh     # Show task details
task_move.sh     # Change status
task_update.sh   # Update fields
task_tag.sh      # Manage tags
task_filter.sh   # Filter by tag
task_delete.sh   # Delete tasks
task_stats.sh    # Show statistics
```

Run any command with `--help` for usage details.

## Configuration

Database location: `~/.no-nonsense/tasks.db`

Override with environment variable:

```bash
export NO_NONSENSE_TASKS_DB=/path/to/tasks.db
```

## Documentation

- [SKILL.md](SKILL.md) - Complete usage guide
- [AGENT.md](AGENT.md) - Development documentation

## Requirements

- `bash`
- `sqlite3`

## License

MIT
