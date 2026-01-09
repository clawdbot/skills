#!/bin/bash
# Plan a trip between two stations in Austrian public transport
# Usage: ./route.sh <from-id> <to-id> [results]
#
# Find station IDs with: ./search.sh <name>
# Example: ./route.sh 490132000 490060200     # Stephansplatz → Hauptbahnhof
# Example: ./route.sh 490132000 444130000 5   # Wien → Linz, 5 results

FROM_ID="${1:-}"
TO_ID="${2:-}"
COUNT="${3:-3}"

if [ -z "$FROM_ID" ] || [ -z "$TO_ID" ]; then
    echo "Usage: $0 <from-station-id> <to-station-id> [results]"
    echo ""
    echo "Find station IDs with: ./search.sh <name>"
    echo ""
    echo "Example: $0 490132000 490060200     # Stephansplatz → Hauptbahnhof"
    echo "Example: $0 490132000 444130000 5   # Wien → Linz, 5 results"
    exit 1
fi

curl -s -X POST "https://vao.demo.hafas.de/gate" \
  -H "Content-Type: application/json" \
  -d '{
    "svcReqL": [{
      "req": {
        "depLocL": [{"extId": "'"$FROM_ID"'", "type": "S"}],
        "arrLocL": [{"extId": "'"$TO_ID"'", "type": "S"}],
        "getPasslist": false,
        "maxChg": 5,
        "numF": '"$COUNT"'
      },
      "meth": "TripSearch",
      "id": "1|3|"
    }],
    "client": {"id": "VAO", "v": "1", "type": "AND", "name": "nextgen"},
    "ver": "1.73",
    "lang": "de",
    "auth": {"aid": "nextgen", "type": "AID"}
  }' | jq '
  .svcResL[0].res as $res |
  ($res.common.prodL // []) as $products |
  ($res.common.locL // []) as $locations |
  ($res.common.dirL // []) as $directions |
  
  # Get from/to names
  (($res.outConL // [])[0].dep.locX // 0) as $fromIdx |
  (($res.outConL // [])[0].arr.locX // 0) as $toIdx |
  ($locations[$fromIdx].name // "Unknown") as $fromName |
  ($locations[$toIdx].name // "Unknown") as $toName |
  
  # Helper function to format time
  def formatTime: if . and (. | length) >= 4 then "\(.[0:2]):\(.[2:4])" else . end;
  
  # Helper function to format duration string HHMMSS
  def formatDuration: 
    if . and (. | length) >= 6 then
      (.[0:2] | tonumber) as $h | (.[2:4] | tonumber) as $m |
      if $h > 0 then "\($h)h \($m)min" else "\($m)min" end
    else . end;
  
  {
    from: $fromName,
    to: $toName,
    trips: [
      ($res.outConL // [])[:'"$COUNT"'] | .[] | {
        departure: (.dep.dTimeS // "?") | formatTime,
        arrival: (.arr.aTimeS // "?") | formatTime,
        duration: (.dur // null) | formatDuration,
        changes: (.chg // 0),
        legs: [
          (.secL // []) | .[] | 
          select(.type == "JNY") |
          {
            line: ($products[.jny.prodX // 0].name // "?"),
            direction: (if .jny.dirX != null and $directions[.jny.dirX] != null then $directions[.jny.dirX].txt else null end),
            from: ($locations[.dep.locX // 0].name // "?"),
            departure: (.dep.dTimeS // "?") | formatTime,
            to: ($locations[.arr.locX // 0].name // "?"),
            arrival: (.arr.aTimeS // "?") | formatTime
          }
        ]
      }
    ]
  }
'
