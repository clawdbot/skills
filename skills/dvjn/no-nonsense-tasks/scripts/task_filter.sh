#!/usr/bin/env bash
# Filter tasks by tag

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"

check_db_exists

TAG="$1"

if [ -z "$TAG" ]; then
	echo "Usage: task_filter.sh <tag>"
	exit 1
fi

# Escape for SQL
TAG_ESC=$(sql_escape "$TAG")

# Match exact tags in comma-separated list
# We use a CASE statement to handle exact matching:
# - Match if tags column equals the tag exactly
# - Match if tags starts with "tag,"
# - Match if tags ends with ",tag"
# - Match if tags contains ",tag,"
RESULT=$(
	sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    id as ID,
    status as Status,
    title as Title,
    tags as Tags,
    substr(created_at, 1, 10) as Created
FROM tasks 
WHERE tags = '$TAG_ESC'
   OR tags LIKE '$TAG_ESC,%'
   OR tags LIKE '%,$TAG_ESC'
   OR tags LIKE '%,$TAG_ESC,%'
ORDER BY $STATUS_ORDER_CASE, created_at DESC;
EOF
)

if [ -z "$RESULT" ]; then
	echo "No tasks found with tag: $TAG"
	exit 0
fi

echo "$RESULT"
