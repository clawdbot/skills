#!/bin/bash
# phone-call.sh - Make an AI phone call via Bland AI
# Usage: ./phone-call.sh <phone_number> <task> [options]
#
# Examples:
#   ./phone-call.sh "+447123456789" "Book a table for 2 at 7pm"
#   ./phone-call.sh "+14155551234" "Ask about opening hours" --voice josh
#   ./phone-call.sh "+447123456789" "Make appointment" --record --wait

set -e

# Check for help flag first (before API key check)
for arg in "$@"; do
    if [[ "$arg" == "--help" || "$arg" == "-h" ]]; then
        echo "Usage: $0 <phone_number> <task> [options]"
        echo ""
        echo "Arguments:"
        echo "  phone_number    Phone number in E.164 format (+447123456789)"
        echo "  task            Instructions for the AI agent"
        echo ""
        echo "Options:"
        echo "  --voice NAME          Voice to use (default: maya)"
        echo "                        Options: josh, maya, florian, derek, june, nat, paige"
        echo "  --first-sentence STR  Exact first sentence for the AI to say"
        echo "  --record              Record the call"
        echo "  --wait-greeting       Wait for the other party to speak first"
        echo "  --max-duration MIN    Maximum call duration in minutes (default: 30)"
        echo "  --language CODE       Language code (default: en)"
        echo "  --wait                Wait for call to complete and show transcript"
        echo "  --help                Show this help"
        exit 0
    fi
done

# Load API key from environment or secrets file
if [[ -z "$BLAND_API_KEY" ]]; then
    if [[ -f ~/.clawd/secrets.json ]]; then
        BLAND_API_KEY=$(jq -r '.bland_api_key // empty' ~/.clawd/secrets.json 2>/dev/null)
    fi
fi

if [[ -z "$BLAND_API_KEY" ]]; then
    echo "Error: BLAND_API_KEY not set"
    echo "Set it in your environment or in ~/.clawd/secrets.json"
    exit 1
fi

# Parse arguments
PHONE_NUMBER=""
TASK=""
VOICE="maya"
FIRST_SENTENCE=""
RECORD="false"
WAIT_FOR_GREETING="false"
MAX_DURATION="30"
LANGUAGE="en"
WAIT_FOR_COMPLETION="false"

while [[ $# -gt 0 ]]; do
    case $1 in
        --voice)
            VOICE="$2"
            shift 2
            ;;
        --first-sentence)
            FIRST_SENTENCE="$2"
            shift 2
            ;;
        --record)
            RECORD="true"
            shift
            ;;
        --wait-greeting)
            WAIT_FOR_GREETING="true"
            shift
            ;;
        --max-duration)
            MAX_DURATION="$2"
            shift 2
            ;;
        --language)
            LANGUAGE="$2"
            shift 2
            ;;
        --wait)
            WAIT_FOR_COMPLETION="true"
            shift
            ;;
        --help|-h)
            echo "Usage: $0 <phone_number> <task> [options]"
            echo ""
            echo "Arguments:"
            echo "  phone_number    Phone number in E.164 format (+447123456789)"
            echo "  task            Instructions for the AI agent"
            echo ""
            echo "Options:"
            echo "  --voice NAME          Voice to use (default: maya)"
            echo "                        Options: josh, maya, florian, derek, june, nat, paige"
            echo "  --first-sentence STR  Exact first sentence for the AI to say"
            echo "  --record              Record the call"
            echo "  --wait-greeting       Wait for the other party to speak first"
            echo "  --max-duration MIN    Maximum call duration in minutes (default: 30)"
            echo "  --language CODE       Language code (default: en)"
            echo "  --wait                Wait for call to complete and show transcript"
            echo "  --help                Show this help"
            exit 0
            ;;
        *)
            if [[ -z "$PHONE_NUMBER" ]]; then
                PHONE_NUMBER="$1"
            elif [[ -z "$TASK" ]]; then
                TASK="$1"
            fi
            shift
            ;;
    esac
done

if [[ -z "$PHONE_NUMBER" ]] || [[ -z "$TASK" ]]; then
    echo "Error: Phone number and task are required"
    echo "Usage: $0 <phone_number> <task> [options]"
    exit 1
fi

# Validate phone number format (basic check)
if [[ ! "$PHONE_NUMBER" =~ ^\+[0-9]{10,15}$ ]]; then
    echo "Warning: Phone number should be in E.164 format (+447123456789)"
fi

# Build request body
REQUEST_BODY=$(jq -n \
    --arg phone "$PHONE_NUMBER" \
    --arg task "$TASK" \
    --arg voice "$VOICE" \
    --arg first_sentence "$FIRST_SENTENCE" \
    --argjson record "$RECORD" \
    --argjson wait_greeting "$WAIT_FOR_GREETING" \
    --argjson max_duration "$MAX_DURATION" \
    --arg language "$LANGUAGE" \
    '{
        phone_number: $phone,
        task: $task,
        voice: $voice,
        record: $record,
        wait_for_greeting: $wait_greeting,
        max_duration: $max_duration,
        language: $language
    } + (if $first_sentence != "" then {first_sentence: $first_sentence} else {} end)')

# Make the API call
echo "📞 Initiating call to $PHONE_NUMBER..."
echo "📝 Task: $TASK"
echo ""

RESPONSE=$(curl -s -X POST "https://api.bland.ai/v1/calls" \
    -H "Authorization: $BLAND_API_KEY" \
    -H "Content-Type: application/json" \
    -d "$REQUEST_BODY")

# Check for errors
STATUS=$(echo "$RESPONSE" | jq -r '.status // "error"')
if [[ "$STATUS" == "error" ]]; then
    ERROR_MSG=$(echo "$RESPONSE" | jq -r '.message // "Unknown error"')
    echo "❌ Error: $ERROR_MSG"
    exit 1
fi

CALL_ID=$(echo "$RESPONSE" | jq -r '.call_id // empty')

if [[ -z "$CALL_ID" ]]; then
    echo "❌ Error: No call ID returned"
    echo "$RESPONSE" | jq .
    exit 1
fi

echo "✅ Call initiated!"
echo "📱 Call ID: $CALL_ID"
echo ""

# If --wait flag, poll for completion
if [[ "$WAIT_FOR_COMPLETION" == "true" ]]; then
    echo "⏳ Waiting for call to complete..."
    SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
    
    while true; do
        sleep 5
        CALL_STATUS=$("$SCRIPT_DIR/check-call.sh" "$CALL_ID" --json 2>/dev/null || echo '{}')
        COMPLETED=$(echo "$CALL_STATUS" | jq -r '.completed // false')
        
        if [[ "$COMPLETED" == "true" ]]; then
            echo ""
            echo "📋 Call completed!"
            "$SCRIPT_DIR/check-call.sh" "$CALL_ID"
            break
        fi
        
        echo -n "."
    done
else
    echo "💡 Check status with: ./check-call.sh $CALL_ID"
fi
