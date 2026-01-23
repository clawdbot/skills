#!/bin/bash
# Read Unraid system logs
# Usage: ./read-logs.sh [log-name] [lines]

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUERY_SCRIPT="$SCRIPT_DIR/../scripts/unraid-query.sh"

LOG_NAME="${1:-syslog}"
LINES="${2:-20}"

echo "=== Reading $LOG_NAME (last $LINES lines) ==="
echo ""

QUERY="{ logFile(path: \"$LOG_NAME\", lines: $LINES) { path totalLines startLine content } }"

RESPONSE=$("$QUERY_SCRIPT" -q "$QUERY" -f raw)

echo "$RESPONSE" | jq -r '.logFile.content'

echo ""
echo "---"
echo "Total lines in log: $(echo "$RESPONSE" | jq -r '.logFile.totalLines')"
echo "Showing from line: $(echo "$RESPONSE" | jq -r '.logFile.startLine')"
