#!/usr/bin/env bash
# Common functions and variables for no-nonsense-tasks

# Database configuration
DB_PATH="${NO_NONSENSE_TASKS_DB:-$HOME/.no-nonsense/tasks.db}"

# Check if database exists
check_db_exists() {
	if [ ! -f "$DB_PATH" ]; then
		echo "Error: Database not initialized. Run init_db.sh first."
		exit 1
	fi
}

# Escape single quotes for SQL
sql_escape() {
	local input="$1"
	echo "${input//\'/\'\'}"
}

# Validate task ID is numeric
validate_task_id() {
	local task_id="$1"
	if ! [[ "$task_id" =~ ^[0-9]+$ ]]; then
		echo "Error: Task ID must be a number"
		exit 1
	fi
}

# Validate status
validate_status() {
	local status="$1"
	case "$status" in
	backlog | todo | in-progress | done)
		return 0
		;;
	*)
		echo "Error: Invalid status '$status'. Must be: backlog, todo, in-progress, or done"
		exit 1
		;;
	esac
}

# Standard status ordering for queries (used in SQL ORDER BY clauses)
# shellcheck disable=SC2034
STATUS_ORDER_CASE="
    CASE status
        WHEN 'in-progress' THEN 1
        WHEN 'todo' THEN 2
        WHEN 'backlog' THEN 3
        WHEN 'done' THEN 4
    END
"
