#!/bin/bash
# Check disk health and temperatures
# Quick overview of all disks with temperature warnings

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUERY_SCRIPT="$SCRIPT_DIR/../scripts/unraid-query.sh"

QUERY='{ array { disks { name device temp status isSpinning } } }'

echo "=== Disk Health Report ==="
echo ""

RESPONSE=$("$QUERY_SCRIPT" -q "$QUERY" -f raw)

echo "$RESPONSE" | jq -r '.array.disks[] | "\(.name) (\(.device)): \(.temp)°C - \(.status) - \(if .isSpinning then "Spinning" else "Spun down" end)"'

echo ""
echo "Temperature warnings:"
echo "$RESPONSE" | jq -r '.array.disks[] | select(.temp > 45) | "⚠️  \(.name): \(.temp)°C (HIGH)"'

HOTTEST=$(echo "$RESPONSE" | jq -r '[.array.disks[].temp] | max')
echo ""
echo "Hottest disk: ${HOTTEST}°C"
