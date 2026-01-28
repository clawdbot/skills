#!/usr/bin/env bash
# List tasks with optional status filter

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"

check_db_exists

STATUS_FILTER=""

while [[ $# -gt 0 ]]; do
	case $1 in
	--status | -s)
		STATUS_FILTER="$2"
		shift 2
		;;
	--help | -h)
		echo "Usage: task_list.sh [options]"
		echo ""
		echo "Options:"
		echo "  -s, --status STATUS   Filter by status (backlog, todo, in-progress, done)"
		echo ""
		echo "Examples:"
		echo "  task_list.sh                    # List all tasks"
		echo "  task_list.sh --status todo      # List only todo tasks"
		echo "  task_list.sh -s in-progress     # List in-progress tasks"
		exit 0
		;;
	-*)
		echo "Error: Unknown option: $1"
		echo "Run with --help for usage information"
		exit 1
		;;
	*)
		# Support old positional argument style for backwards compatibility
		if [ -z "$STATUS_FILTER" ]; then
			STATUS_FILTER="$1"
		else
			echo "Error: Unexpected argument: $1"
			exit 1
		fi
		shift
		;;
	esac
done

if [ -z "$STATUS_FILTER" ]; then
	# List all tasks
	RESULT=$(
		sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    id as ID,
    status as Status,
    title as Title,
    tags as Tags,
    substr(created_at, 1, 10) as Created
FROM tasks 
ORDER BY $STATUS_ORDER_CASE, created_at DESC;
EOF
	)
	if [ -z "$RESULT" ]; then
		echo "No tasks found. Add one with task_add.sh"
		exit 0
	fi
	echo "$RESULT"
else
	# Escape for SQL
	STATUS_FILTER_ESC=$(sql_escape "$STATUS_FILTER")

	# List tasks by status
	RESULT=$(
		sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    id as ID,
    title as Title,
    tags as Tags,
    substr(created_at, 1, 10) as Created
FROM tasks 
WHERE status = '$STATUS_FILTER_ESC'
ORDER BY created_at DESC;
EOF
	)
	if [ -z "$RESULT" ]; then
		echo "No tasks found with status: $STATUS_FILTER"
		exit 0
	fi
	echo "$RESULT"
fi
