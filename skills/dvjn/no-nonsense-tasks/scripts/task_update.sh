#!/usr/bin/env bash
# Update task fields

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"

check_db_exists

TASK_ID=""
FIELD=""
VALUE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
	case $1 in
	--title)
		FIELD="title"
		VALUE="$2"
		shift 2
		;;
	--description | -d)
		FIELD="description"
		VALUE="$2"
		shift 2
		;;
	--tags | -t)
		FIELD="tags"
		VALUE="$2"
		shift 2
		;;
	--status | -s)
		FIELD="status"
		VALUE="$2"
		shift 2
		;;
	--help | -h)
		echo "Usage: task_update.sh <task_id> <options>"
		echo ""
		echo "Options:"
		echo "  --title TEXT           Update title"
		echo "  -d, --description TEXT Update description"
		echo "  -t, --tags TAGS        Update tags (comma-separated)"
		echo "  -s, --status STATUS    Update status (backlog, todo, in-progress, done)"
		echo ""
		echo "Examples:"
		echo "  task_update.sh 5 --title \"New title\""
		echo "  task_update.sh 5 --description \"Updated description\""
		echo "  task_update.sh 5 --tags \"urgent,bug\""
		echo "  task_update.sh 5 --status in-progress"
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
		else
			echo "Error: Unexpected argument: $1"
			echo "Run with --help for usage information"
			exit 1
		fi
		shift
		;;
	esac
done

if [ -z "$TASK_ID" ] || [ -z "$FIELD" ] || [ -z "$VALUE" ]; then
	echo "Error: Task ID and at least one field to update are required"
	echo "Run with --help for usage information"
	exit 1
fi

validate_task_id "$TASK_ID"

# Validate and escape based on field type
case "$FIELD" in
title | description | tags)
	VALUE_ESC=$(sql_escape "$VALUE")
	;;
status)
	validate_status "$VALUE"
	VALUE_ESC="$VALUE" # Status is validated, safe to use
	;;
*)
	echo "Error: Invalid field '$FIELD'. Must be: title, description, tags, or status"
	exit 1
	;;
esac

# Update field
RESULT=$(sqlite3 "$DB_PATH" "UPDATE tasks SET $FIELD = '$VALUE_ESC' WHERE id = $TASK_ID; SELECT changes();")

if [ "$RESULT" -eq 0 ]; then
	echo "Error: Task #$TASK_ID not found"
	exit 1
else
	echo "✓ Task #$TASK_ID updated: $FIELD = '$VALUE'"
fi
