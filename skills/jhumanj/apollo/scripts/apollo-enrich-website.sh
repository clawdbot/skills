#!/bin/bash
set -euo pipefail

# Usage: apollo-enrich-website.sh "domain.com"
# Calls: GET /api/v1/organizations/enrich?domain=...

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}" )" && pwd)"

DOMAIN="${1:-}"
if [ -z "$DOMAIN" ]; then
  echo "Usage: apollo-enrich-website.sh \"domain.com\"" >&2
  exit 1
fi

# Try the commonly documented enrichment endpoint.
"$SCRIPT_DIR/apollo-get.sh" "/api/v1/organizations/enrich" "domain=$DOMAIN"
