#!/usr/bin/env bash
# Add a new task

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"

# Parse arguments
TITLE=""
DESCRIPTION=""
TAGS=""
STATUS="backlog"

while [[ $# -gt 0 ]]; do
	case $1 in
	--description | -d)
		DESCRIPTION="$2"
		shift 2
		;;
	--tags | -t)
		TAGS="$2"
		shift 2
		;;
	--status | -s)
		STATUS="$2"
		shift 2
		;;
	--help | -h)
		echo "Usage: task_add.sh <title> [options]"
		echo ""
		echo "Options:"
		echo "  -d, --description TEXT   Task description"
		echo "  -t, --tags TAGS          Comma-separated tags"
		echo "  -s, --status STATUS      Task status (backlog, todo, in-progress, done)"
		echo "                           Default: backlog"
		echo ""
		echo "Examples:"
		echo "  task_add.sh \"Fix bug\""
		echo "  task_add.sh \"Review PR\" --description \"Check auth changes\" --tags \"urgent,review\""
		echo "  task_add.sh \"Deploy\" --status todo --tags \"critical\""
		exit 0
		;;
	-*)
		echo "Error: Unknown option: $1"
		echo "Run with --help for usage information"
		exit 1
		;;
	*)
		if [ -z "$TITLE" ]; then
			TITLE="$1"
		else
			echo "Error: Unexpected argument: $1"
			echo "Run with --help for usage information"
			exit 1
		fi
		shift
		;;
	esac
done

if [ -z "$TITLE" ]; then
	echo "Error: Title is required"
	echo "Run with --help for usage information"
	exit 1
fi

check_db_exists

validate_status "$STATUS"

# Escape for SQL
TITLE_ESC=$(sql_escape "$TITLE")
DESCRIPTION_ESC=$(sql_escape "$DESCRIPTION")
TAGS_ESC=$(sql_escape "$TAGS")

# Insert task
sqlite3 "$DB_PATH" <<EOF
INSERT INTO tasks (title, description, tags, status) 
VALUES ('$TITLE_ESC', '$DESCRIPTION_ESC', '$TAGS_ESC', '$STATUS');
SELECT 'Task added with ID: ' || last_insert_rowid();
EOF
