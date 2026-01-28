# AGENT.md - Development Guide

This file is for AI agents and developers working on the no-nonsense-tasks skill.

## Architecture

**Components:**

- `scripts/lib.sh` - Common functions and variables
- `scripts/*.sh` - Individual command scripts
- `migrations/*.sql` - Database schema migrations

**Database:**

- SQLite3 at `~/.no-nonsense/tasks.db` (default)
- Override with `NO_NONSENSE_DB` environment variable

## Code Standards

**Shell scripts:**

- Use `#!/usr/bin/env bash` shebang
- Source `lib.sh` for common functions
- All user input must be validated/escaped before SQL use

**SQL Injection Protection:**

- Use `sql_escape()` for string inputs
- Use `validate_task_id()` for numeric IDs
- Use `validate_status()` for status enums

**Error Handling:**

- Always check if DB exists with `check_db_exists()`
- Handle zero-result cases with friendly messages
- Validate all user input before processing

**Common Functions (lib.sh):**

- `check_db_exists()` - Verify DB file exists
- `sql_escape()` - Escape single quotes for SQL
- `validate_task_id()` - Ensure ID is numeric
- `validate_status()` - Validate status enum
- `STATUS_ORDER_CASE` - Standard status sorting

## Migrations

**How it works:**

1. Migrations live in `migrations/*.sql`
2. Named with format: `001_description.sql`, `002_another.sql`, etc.
3. `init_db.sh` tracks which migrations have been applied
4. Safe to run `init_db.sh` multiple times - skips already-applied migrations

**Adding a new migration:**

1. Create `migrations/00X_description.sql` (next number in sequence)
2. Write SQL schema changes
3. Run `./scripts/init_db.sh` to apply
4. Migration is tracked in `schema_migrations` table

**Example migration:**

```sql
-- migrations/002_add_priority.sql
ALTER TABLE tasks ADD COLUMN priority TEXT DEFAULT 'medium' 
    CHECK(priority IN ('low', 'medium', 'high'));
CREATE INDEX IF NOT EXISTS idx_priority ON tasks(priority);
```

**Important:**

- Migrations are forward-only (no rollback mechanism)
- Test migrations on a copy of the DB first
- Use `IF NOT EXISTS` for idempotent operations when possible

## Environment Variables

- `NO_NONSENSE_TASKS_DB` - Database file path (default: `~/.no-nonsense/tasks.db`)

## Testing

**Manual testing checklist:**

- [ ] Add task with quotes/special chars in title
- [ ] List with zero tasks
- [ ] Filter by non-existent tag
- [ ] Show non-existent task ID
- [ ] Move task with invalid status
- [ ] Update with invalid field name
- [ ] Delete non-existent task

**SQL injection test cases:**

```bash
# These should NOT break or execute arbitrary SQL
./scripts/task_add.sh "'; DROP TABLE tasks; --"
./scripts/task_tag.sh 1 "'; DELETE FROM tasks; --"
./scripts/task_filter.sh "' OR '1'='1"
```

## Common Patterns

**Adding a new command:**

1. Create `scripts/task_newcmd.sh`
2. Start with standard template:

```bash
#!/usr/bin/env bash
# Description of command

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/lib.sh"

check_db_exists

# Your logic here
```

3. Validate inputs
4. Escape SQL strings
5. Handle zero-result cases
6. Update SKILL.md with usage examples

## Known Limitations

- Tag search uses LIKE pattern (matches partial strings)
- No task archiving/soft delete
- No due dates or priorities (yet - see migration example)
- No multi-user support
- No task dependencies or subtasks
