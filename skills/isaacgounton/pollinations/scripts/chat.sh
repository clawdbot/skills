#!/bin/bash
# Pollinations Chat Completions
# Usage: ./chat.sh "message" [--model model] [--temp N] [--max N]

PROMPT="$1"
shift

# Defaults
MODEL="${MODEL:-openai}"
TEMP="${TEMPERATURE:-}"

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --model)
      MODEL="$2"
      shift 2
      ;;
    --temp|--temperature)
      TEMPERATURE="$2"
      shift 2
      ;;
    *)
      shift
      ;;
  esac
done

# Build request body
BODY=$(jq -n -c \
  --arg model "$MODEL" \
  --arg prompt "$PROMPT" \
  '{
    model: $model,
    messages: [{"role": "user", "content": $prompt}]
  }')

# Add temperature if specified
if [[ -n "$TEMP" ]]; then
  BODY=$(echo "$BODY" | jq -c --arg temp "$TEMP" '. + {temperature: ($temp | tonumber)}')
fi

# Make request
URL="https://gen.pollinations.ai/v1/chat/completions"
HEADERS="-H Content-Type: application/json"

if [[ -n "$POLLINATIONS_API_KEY" ]]; then
  HEADERS="$HEADERS -H Authorization: Bearer $POLLINATIONS_API_KEY"
fi

curl -s $HEADERS -X POST "$URL" -d "$BODY" | jq -r '.choices[0].message.content'
