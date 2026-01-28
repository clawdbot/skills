#!/usr/bin/env bash
# Delete a task

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"

check_db_exists

TASK_ID="$1"

if [ -z "$TASK_ID" ]; then
	echo "Usage: task_delete.sh <task_id>"
	exit 1
fi

validate_task_id "$TASK_ID"

# Get task title before deleting
TITLE=$(sqlite3 "$DB_PATH" "SELECT title FROM tasks WHERE id = $TASK_ID;")

if [ -z "$TITLE" ]; then
	echo "Error: Task #$TASK_ID not found"
	exit 1
fi

# Delete task
sqlite3 "$DB_PATH" "DELETE FROM tasks WHERE id = $TASK_ID;"
echo "✓ Task #$TASK_ID deleted: $TITLE"
