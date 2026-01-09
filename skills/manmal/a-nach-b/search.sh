#!/bin/bash
# Search for stations/stops in Austrian public transport
# Usage: ./search.sh <name>
#
# Returns: Station name, ID, type, and coordinates

QUERY="${1:-}"

if [ -z "$QUERY" ]; then
    echo "Usage: $0 <station-name>"
    echo "Example: $0 Stephansplatz"
    echo "Example: $0 \"Wien Hauptbahnhof\""
    exit 1
fi

curl -s -X POST "https://vao.demo.hafas.de/gate" \
  -H "Content-Type: application/json" \
  -d '{
    "svcReqL": [{
      "req": {
        "input": {
          "loc": {"name": "'"$QUERY"'"},
          "field": "S"
        }
      },
      "meth": "LocMatch",
      "id": "1|1|"
    }],
    "client": {"id": "VAO", "v": "1", "type": "AND", "name": "nextgen"},
    "ver": "1.73",
    "lang": "de",
    "auth": {"aid": "nextgen", "type": "AID"}
  }' | jq -r '
  .svcResL[0].res.match.locL // [] | 
  map(select(.type == "S" or .type == "A")) |
  .[:15] |
  map({
    name: .name,
    id: .extId,
    type: (if .type == "S" then "Station" elif .type == "A" then "Address" else .type end),
    coordinates: (if .crd then "\(.crd.y / 1000000), \(.crd.x / 1000000)" else null end)
  })
'
