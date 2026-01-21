#!/usr/bin/env bash
# Telegram slash command wrapper for task-tracker skill
# Usage: telegram-commands.sh {daily|weekly|done24h|done7d}

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

case "$1" in
  daily)
    python3 "$SCRIPT_DIR/standup.py"
    ;;
  weekly)
    # Show high priority tasks, then medium priority tasks
    echo "📋 Weekly Priorities"
    echo ""
    echo "### High Priority"
    python3 "$SCRIPT_DIR/tasks.py" list --priority high --status todo
    echo ""
    echo "### Medium Priority"
    python3 "$SCRIPT_DIR/tasks.py" list --priority medium --status todo
    ;;
  done24h)
    # Show completed tasks from last 24 hours
    python3 "$SCRIPT_DIR/tasks.py" list --status done --completed-since 24h
    ;;
  done7d)
    # Show completed tasks from last 7 days
    python3 "$SCRIPT_DIR/tasks.py" list --status done --completed-since 7d
    ;;
  *)
    echo "Usage: $0 {daily|weekly|done24h|done7d}"
    exit 1
    ;;
esac
