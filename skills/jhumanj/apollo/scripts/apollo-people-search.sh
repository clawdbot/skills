#!/bin/bash
set -euo pipefail

# Usage: apollo-people-search.sh "keywords" [page] [perPage]
# Uses POST /api/v1/mixed_people/api_search (new endpoint).

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"

KEYWORDS="${1:-}"
PAGE="${2:-1}"
PER_PAGE="${3:-5}"

if [ -z "$KEYWORDS" ]; then
  echo "Usage: apollo-people-search.sh \"keywords\" [page] [perPage]" >&2
  exit 1
fi

BODY=$(python3 - <<'PY' "$KEYWORDS" "$PAGE" "$PER_PAGE"
import json,sys
keywords=sys.argv[1]
page=int(sys.argv[2])
per_page=int(sys.argv[3])
print(json.dumps({"q_keywords": keywords, "page": page, "per_page": per_page}))
PY
)

"$SCRIPT_DIR/apollo-post.sh" "/api/v1/mixed_people/api_search" "$BODY"
