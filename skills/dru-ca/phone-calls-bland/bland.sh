#!/bin/bash
# bland.sh - Low-level Bland AI API wrapper
# Usage: ./bland.sh <command> [options]
#
# Commands:
#   call      - Make a call (raw JSON body)
#   status    - Get call status
#   list      - List recent calls
#   analyze   - Analyze a completed call
#   voices    - List available voices
#   balance   - Check account balance

set -e

# Check for help first
COMMAND="${1:-help}"
if [[ "$COMMAND" == "help" || "$COMMAND" == "--help" || "$COMMAND" == "-h" || "$COMMAND" == "voices" || "$COMMAND" == "balance" || "$COMMAND" == "credits" ]]; then
    # These commands don't need API key
    :
else
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
fi

API_BASE="https://api.bland.ai/v1"

# Helper function for API calls
api_call() {
    local method="$1"
    local endpoint="$2"
    local data="$3"
    
    if [[ -n "$data" ]]; then
        curl -s -X "$method" "$API_BASE$endpoint" \
            -H "Authorization: $BLAND_API_KEY" \
            -H "Content-Type: application/json" \
            -d "$data"
    else
        curl -s -X "$method" "$API_BASE$endpoint" \
            -H "Authorization: $BLAND_API_KEY"
    fi
}

shift || true

case "$COMMAND" in
    call)
        # Make a call with raw JSON
        if [[ -z "$1" ]]; then
            echo "Usage: $0 call '<json_body>'"
            echo ""
            echo "Example:"
            echo '  ./bland.sh call '"'"'{"phone_number": "+447123456789", "task": "Say hello"}'"'"
            exit 1
        fi
        api_call POST "/calls" "$1" | jq .
        ;;
        
    status|get)
        # Get call status
        if [[ -z "$1" ]]; then
            echo "Usage: $0 status <call_id>"
            exit 1
        fi
        api_call GET "/calls/$1" | jq .
        ;;
        
    list)
        # List recent calls
        LIMIT="${1:-10}"
        api_call GET "/calls?limit=$LIMIT" | jq .
        ;;
        
    analyze)
        # Analyze a call with custom prompt
        if [[ -z "$1" ]]; then
            echo "Usage: $0 analyze <call_id> [prompt]"
            exit 1
        fi
        CALL_ID="$1"
        PROMPT="${2:-Summarize this call and extract any important information like dates, times, names, or action items.}"
        
        DATA=$(jq -n --arg prompt "$PROMPT" '{goal: $prompt}')
        api_call POST "/calls/$CALL_ID/analyze" "$DATA" | jq .
        ;;
        
    stop)
        # Stop an ongoing call
        if [[ -z "$1" ]]; then
            echo "Usage: $0 stop <call_id>"
            exit 1
        fi
        api_call POST "/calls/$1/stop" | jq .
        ;;
        
    voices)
        # List available voices (built-in)
        echo "Built-in Voices:"
        echo "  josh     - Male, professional"
        echo "  maya     - Female, friendly (default)"
        echo "  florian  - Male, European accent"
        echo "  derek    - Male, casual"
        echo "  june     - Female, professional"
        echo "  nat      - Male, natural"
        echo "  paige    - Female, upbeat"
        echo ""
        echo "Note: Custom voices can be created in the Bland dashboard"
        ;;
        
    balance|credits)
        # This endpoint may not exist - placeholder
        echo "Check your balance at: https://app.bland.ai/dashboard/billing"
        ;;
        
    help|--help|-h)
        echo "Bland AI API Wrapper"
        echo ""
        echo "Usage: $0 <command> [options]"
        echo ""
        echo "Commands:"
        echo "  call <json>           Make a call with raw JSON body"
        echo "  status <call_id>      Get call status and transcript"
        echo "  list [limit]          List recent calls (default: 10)"
        echo "  analyze <call_id> [prompt]  Analyze a call with AI"
        echo "  stop <call_id>        Stop an ongoing call"
        echo "  voices                List available voices"
        echo "  balance               Check account balance"
        echo "  help                  Show this help"
        ;;
        
    *)
        echo "Unknown command: $COMMAND"
        echo "Run '$0 help' for usage"
        exit 1
        ;;
esac
