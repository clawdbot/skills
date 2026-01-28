#!/bin/bash
# Check portfolio balance via Bankr

BANKR_SCRIPT="$HOME/clawd/skills/bankr/scripts/bankr.sh"

if [ ! -f "$BANKR_SCRIPT" ]; then
  echo "Error: Bankr script not found at $BANKR_SCRIPT"
  exit 1
fi

echo "Checking portfolio on Base..."
"$BANKR_SCRIPT" "Show my complete portfolio on Base"
