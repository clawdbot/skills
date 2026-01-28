#!/usr/bin/env bash
# Show task statistics

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/lib.sh
source "$SCRIPT_DIR/lib.sh"

check_db_exists

echo "=== Task Statistics ==="
echo ""

TOTAL=$(sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM tasks;")

if [ "$TOTAL" -eq 0 ]; then
	echo "No tasks found."
	echo ""
	echo "Total tasks: 0"
	exit 0
fi

sqlite3 -header -column "$DB_PATH" <<EOF
SELECT 
    status as Status,
    COUNT(*) as Count
FROM tasks 
GROUP BY status
ORDER BY $STATUS_ORDER_CASE;
EOF

echo ""
echo "Total tasks: $TOTAL"
