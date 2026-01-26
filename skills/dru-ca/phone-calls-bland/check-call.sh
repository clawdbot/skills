#!/bin/bash
# check-call.sh - Check the status of a Bland AI phone call
# Usage: ./check-call.sh <call_id> [options]

set -e

# Check for help flag first
for arg in "$@"; do
    if [[ "$arg" == "--help" || "$arg" == "-h" ]]; then
        echo "Usage: $0 <call_id> [options]"
        echo ""
        echo "Options:"
        echo "  --json    Output raw JSON"
        echo "  --help    Show this help"
        exit 0
    fi
done

# Load API key
if [[ -z "$BLAND_API_KEY" ]]; then
    if [[ -f ~/.clawd/secrets.json ]]; then
        BLAND_API_KEY=$(jq -r '.bland_api_key // empty' ~/.clawd/secrets.json 2>/dev/null)
    fi
fi

if [[ -z "$BLAND_API_KEY" ]]; then
    echo "Error: BLAND_API_KEY not set"
    exit 1
fi

# Parse arguments
CALL_ID=""
JSON_OUTPUT="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        --json)
            JSON_OUTPUT="true"
            shift
            ;;
        --help|-h)
            # Handled at top of script
            exit 0
            ;;
        *)
            CALL_ID="$1"
            shift
            ;;
    esac
done

if [[ -z "$CALL_ID" ]]; then
    echo "Error: Call ID required"
    echo "Usage: $0 <call_id>"
    exit 1
fi

# Get call details
RESPONSE=$(curl -s -X GET "https://api.bland.ai/v1/calls/$CALL_ID" \
    -H "Authorization: $BLAND_API_KEY")

# Check for errors
if echo "$RESPONSE" | jq -e '.error' > /dev/null 2>&1; then
    echo "Error: $(echo "$RESPONSE" | jq -r '.error')"
    exit 1
fi

if [[ "$JSON_OUTPUT" == "true" ]]; then
    echo "$RESPONSE"
    exit 0
fi

# Parse and display results
COMPLETED=$(echo "$RESPONSE" | jq -r '.completed // false')
STATUS=$(echo "$RESPONSE" | jq -r '.status // "unknown"')
DURATION=$(echo "$RESPONSE" | jq -r '.call_length // 0')
TO_NUMBER=$(echo "$RESPONSE" | jq -r '.to // "unknown"')
ANSWERED=$(echo "$RESPONSE" | jq -r '.answered_by // "unknown"')

echo "📱 Call Status"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Call ID:     $CALL_ID"
echo "To:          $TO_NUMBER"
echo "Status:      $STATUS"
echo "Completed:   $COMPLETED"
echo "Duration:    ${DURATION}s"
echo "Answered by: $ANSWERED"
echo ""

# Show transcript if available
TRANSCRIPT=$(echo "$RESPONSE" | jq -r '.concatenated_transcript // empty')
if [[ -n "$TRANSCRIPT" && "$TRANSCRIPT" != "null" ]]; then
    echo "📝 Transcript"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "$TRANSCRIPT"
    echo ""
fi

# Show summary if available
SUMMARY=$(echo "$RESPONSE" | jq -r '.summary // empty')
if [[ -n "$SUMMARY" && "$SUMMARY" != "null" ]]; then
    echo "📋 Summary"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "$SUMMARY"
    echo ""
fi

# Show recording URL if available
RECORDING=$(echo "$RESPONSE" | jq -r '.recording_url // empty')
if [[ -n "$RECORDING" && "$RECORDING" != "null" ]]; then
    echo "🎙️ Recording: $RECORDING"
    echo ""
fi

# Show any error info
ERROR=$(echo "$RESPONSE" | jq -r '.error_message // empty')
if [[ -n "$ERROR" && "$ERROR" != "null" ]]; then
    echo "⚠️ Error: $ERROR"
fi
