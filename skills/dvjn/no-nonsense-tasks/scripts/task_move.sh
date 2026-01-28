#!/usr/bin/env bash
# Move task to a different status

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"

check_db_exists

TASK_ID=""
NEW_STATUS=""

while [[ $# -gt 0 ]]; do
	case $1 in
	--status | -s)
		NEW_STATUS="$2"
		shift 2
		;;
	--help | -h)
		echo "Usage: task_move.sh <task_id> <options>"
		echo ""
		echo "Options:"
		echo "  -s, --status STATUS   New status (backlog, todo, in-progress, done)"
		echo ""
		echo "Examples:"
		echo "  task_move.sh 3 --status todo"
		echo "  task_move.sh 7 -s in-progress"
		echo "  task_move.sh 12 --status done"
		exit 0
		;;
	-*)
		echo "Error: Unknown option: $1"
		echo "Run with --help for usage information"
		exit 1
		;;
	*)
		if [ -z "$TASK_ID" ]; then
			TASK_ID="$1"
		elif [ -z "$NEW_STATUS" ]; then
			# Support old positional argument for backwards compatibility
			NEW_STATUS="$1"
		else
			echo "Error: Unexpected argument: $1"
			exit 1
		fi
		shift
		;;
	esac
done

if [ -z "$TASK_ID" ] || [ -z "$NEW_STATUS" ]; then
	echo "Error: Task ID and status are required"
	echo "Run with --help for usage information"
	exit 1
fi

validate_task_id "$TASK_ID"
validate_status "$NEW_STATUS"

# Update status (NEW_STATUS is validated, so safe to use)
RESULT=$(sqlite3 "$DB_PATH" "UPDATE tasks SET status = '$NEW_STATUS' WHERE id = $TASK_ID; SELECT changes();")

if [ "$RESULT" -eq 0 ]; then
	echo "Error: Task #$TASK_ID not found"
	exit 1
else
	echo "✓ Task #$TASK_ID moved to '$NEW_STATUS'"
fi
