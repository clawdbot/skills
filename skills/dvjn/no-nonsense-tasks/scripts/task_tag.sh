#!/usr/bin/env bash
# Add or update tags for a task

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"

check_db_exists

TASK_ID=""
TAGS=""

while [[ $# -gt 0 ]]; do
	case $1 in
	--tags | -t)
		TAGS="$2"
		shift 2
		;;
	--help | -h)
		echo "Usage: task_tag.sh <task_id> <options>"
		echo ""
		echo "Options:"
		echo "  -t, --tags TAGS   Comma-separated tags"
		echo ""
		echo "Examples:"
		echo "  task_tag.sh 1 --tags \"urgent,work,api\""
		echo "  task_tag.sh 8 -t \"bug,frontend\""
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
		elif [ -z "$TAGS" ]; then
			# Support old positional argument for backwards compatibility
			TAGS="$1"
		else
			echo "Error: Unexpected argument: $1"
			exit 1
		fi
		shift
		;;
	esac
done

if [ -z "$TASK_ID" ] || [ -z "$TAGS" ]; then
	echo "Error: Task ID and tags are required"
	echo "Run with --help for usage information"
	exit 1
fi

validate_task_id "$TASK_ID"

TAGS_ESC=$(sql_escape "$TAGS")

# Update tags
RESULT=$(sqlite3 "$DB_PATH" "UPDATE tasks SET tags = '$TAGS_ESC' WHERE id = $TASK_ID; SELECT changes();")

if [ "$RESULT" -eq 0 ]; then
	echo "Error: Task #$TASK_ID not found"
	exit 1
else
	echo "✓ Task #$TASK_ID tags updated: $TAGS"
fi
