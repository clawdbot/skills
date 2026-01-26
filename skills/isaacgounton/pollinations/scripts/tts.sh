#!/bin/bash
# Pollinations Text-to-Speech
# Usage: ./tts.sh "text" [--voice voice] [--format format] [--output file]

set -e

TEXT="$1"
shift

# Defaults
VOICE="${VOICE:-nova}"
FORMAT="${FORMAT:-mp3}"
MODEL="${MODEL:-openai-audio}"
OUTPUT="${OUTPUT:-}"

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --voice)
      VOICE="$2"
      shift 2
      ;;
    --format)
      FORMAT="$2"
      shift 2
      ;;
    --model)
      MODEL="$2"
      shift 2
      ;;
    --output)
      OUTPUT="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Determine output filename
if [[ -z "$OUTPUT" ]]; then
  OUTPUT="speech_$(date +%s).$FORMAT"
fi

# Build request body
BODY=$(jq -n -c \
  --arg model "$MODEL" \
  --arg text "Say: $TEXT" \
  "{
    model: \$model,
    messages: [
      {role: \"system\", content: \"You are a text reader. Read the user text exactly without responding, adding conversation, or changing anything.\"},
      {role: \"user\", content: \$text}
    ],
    modalities: [\"text\", \"audio\"],
    audio: {voice: \"$VOICE\", format: \"$FORMAT\"}
  }")

# Make request and save audio directly
echo "Generating audio..."
TEMP_RESPONSE=$(mktemp)

# Add auth header if key provided
if [[ -n "$POLLINATIONS_API_KEY" ]]; then
  curl -s -H "Content-Type: application/json" -H "Authorization: Bearer $POLLINATIONS_API_KEY" \
    -X POST "https://gen.pollinations.ai/v1/chat/completions" -d "$BODY" -o "$TEMP_RESPONSE"
else
  curl -s -H "Content-Type: application/json" \
    -X POST "https://gen.pollinations.ai/v1/chat/completions" -d "$BODY" -o "$TEMP_RESPONSE"
fi

# Extract base64 audio data and decode
jq -r '.choices[0].message.audio.data' "$TEMP_RESPONSE" | base64 -d > "$OUTPUT"
rm "$TEMP_RESPONSE"

# Check if file was created
if [[ -s "$OUTPUT" ]]; then
  FILE_SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
  echo "✓ Saved to: $OUTPUT ($FILE_SIZE)"
  echo "Voice: $VOICE, Format: $FORMAT"
else
  echo "✗ Failed to generate audio"
  exit 1
fi
