#!/usr/bin/env bash
# Show details of a specific task

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"

check_db_exists

TASK_ID="$1"

if [ -z "$TASK_ID" ]; then
	echo "Usage: task_show.sh <task_id>"
	exit 1
fi

validate_task_id "$TASK_ID"

RESULT=$(
	sqlite3 "$DB_PATH" <<EOF
.mode line
SELECT 
    id as 'ID',
    title as 'Title',
    description as 'Description',
    tags as 'Tags',
    status as 'Status',
    created_at as 'Created',
    updated_at as 'Updated'
FROM tasks 
WHERE id = $TASK_ID;
EOF
)

if [ -z "$RESULT" ]; then
	echo "Error: Task #$TASK_ID not found"
	exit 1
fi

echo "$RESULT"
