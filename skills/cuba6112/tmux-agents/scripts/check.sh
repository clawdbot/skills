#!/bin/bash
# Check on a tmux agent session

SESSION_NAME="$1"
LINES="${2:-50}"

if [ -z "$SESSION_NAME" ]; then
  echo "Active sessions:"
  tmux list-sessions 2>/dev/null || echo "No sessions running"
  exit 0
fi

if ! tmux has-session -t "$SESSION_NAME" 2>/dev/null; then
  echo "Session '$SESSION_NAME' not found"
  echo ""
  echo "Active sessions:"
  tmux list-sessions 2>/dev/null || echo "No sessions running"
  exit 1
fi

echo "=== Session: $SESSION_NAME (last $LINES lines) ==="
echo ""
tmux capture-pane -t "$SESSION_NAME" -p -S -$LINES
