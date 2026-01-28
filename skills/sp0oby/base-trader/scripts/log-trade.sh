#!/bin/bash
# Log a trade to the trades journal
# Usage: ./log-trade.sh "BUY" "TOKEN" "25" "0.001" "reason" "0xtx..."

ACTION=$1
TOKEN=$2
AMOUNT_USD=$3
PRICE=$4
REASON=$5
TX=$6

TRADES_FILE="$(dirname "$0")/../data/trades.json"

TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

# Create trade entry
TRADE=$(cat <<EOF
{
  "timestamp": "$TIMESTAMP",
  "action": "$ACTION",
  "token": "$TOKEN",
  "amount_usd": $AMOUNT_USD,
  "price": $PRICE,
  "reason": "$REASON",
  "tx": "$TX"
}
EOF
)

# Append to trades file
if [ -f "$TRADES_FILE" ]; then
  # Read existing, append new trade
  jq ". += [$TRADE]" "$TRADES_FILE" > "${TRADES_FILE}.tmp" && mv "${TRADES_FILE}.tmp" "$TRADES_FILE"
else
  echo "[$TRADE]" > "$TRADES_FILE"
fi

echo "Trade logged: $ACTION $TOKEN \$$AMOUNT_USD"
