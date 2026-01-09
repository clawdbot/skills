#!/bin/bash
# Get current service disruptions in Austrian public transport
# Usage: ./disruptions.sh [max-results]
#
# Example: ./disruptions.sh       # Get up to 20 disruptions
# Example: ./disruptions.sh 50    # Get up to 50 disruptions

MAX_RESULTS="${1:-20}"

curl -s -X POST "https://vao.demo.hafas.de/gate" \
  -H "Content-Type: application/json" \
  -d '{
    "svcReqL": [{
      "req": {
        "maxNum": '"$MAX_RESULTS"',
        "himFltrL": [{"mode": "INC", "type": "HIMCAT", "value": "*"}]
      },
      "meth": "HimSearch",
      "id": "1|4|"
    }],
    "client": {"id": "VAO", "v": "1", "type": "AND", "name": "nextgen"},
    "ver": "1.73",
    "lang": "de",
    "auth": {"aid": "nextgen", "type": "AID"}
  }' | jq '
  .svcResL[0].res as $res |
  ($res.common.himL // []) as $messages |
  
  if ($messages | length) == 0 then
    {
      status: "ok",
      message: "No disruptions currently reported",
      count: 0,
      disruptions: []
    }
  else
    {
      count: ($messages | length),
      disruptions: [
        $messages[] | {
          id: .hid,
          category: .cat,
          priority: .prio,
          head: .head,
          text: .text,
          validFrom: .sDate,
          validTo: .eDate,
          affectedLines: ((.affProdRefL // []) | map(.name) | if . == [] then null else . end)
        }
      ]
    }
  end
'
