#!/bin/bash
# Get real-time departures from an Austrian public transport station
# Usage: ./departures.sh <station-id> [count]
#
# Find station IDs with: ./search.sh <name>
# Example: ./departures.sh 490132000        # Wien Stephansplatz
# Example: ./departures.sh 490060200 20     # Wien Hauptbahnhof, 20 results

STATION_ID="${1:-}"
COUNT="${2:-10}"

if [ -z "$STATION_ID" ]; then
    echo "Usage: $0 <station-id> [count]"
    echo ""
    echo "Find station IDs with: ./search.sh <name>"
    echo ""
    echo "Common station IDs:"
    echo "  490132000 - Wien Stephansplatz"
    echo "  490134900 - Wien Hauptbahnhof"
    echo "  490024300 - Wien Westbahnhof"
    echo "  444116400 - Linz Hbf"
    echo "  455000200 - Salzburg Hbf"
    echo "  460086000 - Graz Hbf"
    exit 1
fi

curl -s -X POST "https://vao.demo.hafas.de/gate" \
  -H "Content-Type: application/json" \
  -d '{
    "svcReqL": [{
      "req": {
        "stbLoc": {"extId": "'"$STATION_ID"'", "type": "S"},
        "type": "DEP",
        "maxJny": '"$COUNT"'
      },
      "meth": "StationBoard",
      "id": "1|2|"
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
  
  # Get station name
  ($locations[0].name // "Unknown") as $stationName |
  
  # Helper to format time
  def formatTime: if . and (. | length) >= 4 then "\(.[0:2]):\(.[2:4])" else null end;
  
  # Helper to calculate delay
  def calcDelay(real; sched):
    if real and sched and (real | length) >= 4 and (sched | length) >= 4 then
      ((real[0:2] | tonumber) * 60 + (real[2:4] | tonumber)) -
      ((sched[0:2] | tonumber) * 60 + (sched[2:4] | tonumber))
    else null end;
  
  {
    station: $stationName,
    departures: [
      ($res.jnyL // [])[:'"$COUNT"'] | .[] | 
      (if .dirX != null and $directions[.dirX] != null then $directions[.dirX].txt else .dirTxt end) as $dir |
      calcDelay(.stbStop.dTimeR; .stbStop.dTimeS) as $delayMin |
      {
        line: ($products[.prodX // 0].name // "?"),
        direction: ($dir // null),
        departure: ((.stbStop.dTimeR // .stbStop.dTimeS) | formatTime),
        scheduled: (.stbStop.dTimeS | formatTime),
        delay: (if $delayMin != null and $delayMin > 0 then "+\($delayMin)min" elif $delayMin != null and $delayMin < 0 then "\($delayMin)min" else null end),
        platform: (.stbStop.dPlatfS // .stbStop.dPlatfR // null),
        cancelled: (if .stbStop.dCncl == true then true else null end)
      }
    ]
  }
'
