#!/bin/bash
set -euo pipefail

# Usage: apollo-orgs-bulk.sh "id1" [id2] [id3...]
# Calls: GET /organizations/bulk?organization_ids=...
# Note: Often requires master API key.

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"

if [ $# -lt 1 ]; then
  echo "Usage: apollo-orgs-bulk.sh \"orgId1\" [orgId2] ..." >&2
  exit 1
fi

IDS=$(python3 - <<'PY' "$@"
import sys
print(','.join(sys.argv[1:]))
PY
)

"$SCRIPT_DIR/apollo-get.sh" "/organizations/bulk" "organization_ids=$IDS"
