#!/bin/bash
# Show status of all tmux agent sessions

echo "🖥️  Tmux Agent Sessions"
echo "========================"
echo ""

SESSIONS=$(tmux list-sessions -F "#{session_name}" 2>/dev/null)

if [ -z "$SESSIONS" ]; then
  echo "No active sessions"
  exit 0
fi

for session in $SESSIONS; do
  echo "📍 Session: $session"
  echo "   Created: $(tmux display-message -t "$session" -p '#{session_created}' | xargs -I{} date -r {} '+%Y-%m-%d %H:%M')"
  
  # Get last few lines to show current state
  LAST_LINE=$(tmux capture-pane -t "$session" -p | grep -v '^$' | tail -1)
  if [ -n "$LAST_LINE" ]; then
    echo "   Status: ${LAST_LINE:0:60}..."
  fi
  echo ""
done

echo "Commands:"
echo "  Check:  ./skills/tmux-agents/scripts/check.sh <name>"
echo "  Attach: tmux attach -t <name>"
echo "  Kill:   tmux kill-session -t <name>"
