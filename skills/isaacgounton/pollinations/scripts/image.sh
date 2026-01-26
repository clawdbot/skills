#!/bin/bash
# Pollinations Image/Video Generation
# Usage: ./image.sh "prompt" [--model model] [--width N] [--height N] [--seed N] [--output file] [--duration N]

set -e

PROMPT="$1"
shift

# Defaults
MODEL="${MODEL:-flux}"
WIDTH="${WIDTH:-1024}"
HEIGHT="${HEIGHT:-1024}"
SEED="${SEED:-}"
OUTPUT="${OUTPUT:-}"
DURATION=""
NOLOGO="${NOLOGO:-}"
PRIVATE="${PRIVATE:-}"
SAFE="${SAFE:-}"
ENHANCE="${ENHANCE:-}"
NEGATIVE=""
QUALITY=""
TRANSPARENT=""
IMAGE_URL=""
AUDIO=""
ASPECT_RATIO=""

# URL encode function
urlencode() {
  local string="$1"
  local encoded=""
  local length="${#string}"
  for ((i = 0; i < length; i++)); do
    local c="${string:$i:1}"
    case $c in
      [a-zA-Z0-9.~_-]) encoded+="$c" ;;
      *) encoded+="%$(printf '%X' "'$c")" ;;
    esac
  done
  echo "$encoded"
}

# Parse args
while [[ $# -gt 0 ]]; do
  case "$1" in
    --model)
      MODEL="$2"
      shift 2
      ;;
    --width)
      WIDTH="$2"
      shift 2
      ;;
    --height)
      HEIGHT="$2"
      shift 2
      ;;
    --seed)
      SEED="$2"
      shift 2
      ;;
    --output)
      OUTPUT="$2"
      shift 2
      ;;
    --duration)
      DURATION="$2"
      shift 2
      ;;
    --nologo)
      NOLOGO="true"
      shift
      ;;
    --private)
      PRIVATE="true"
      shift
      ;;
    --safe)
      SAFE="true"
      shift
      ;;
    --enhance)
      ENHANCE="true"
      shift
      ;;
    --negative)
      NEGATIVE="$2"
      shift 2
      ;;
    --quality)
      QUALITY="$2"
      shift 2
      ;;
    --transparent)
      TRANSPARENT="true"
      shift
      ;;
    --audio)
      AUDIO="true"
      shift
      ;;
    --aspect-ratio)
      ASPECT_RATIO="$2"
      shift 2
      ;;
    --image-url)
      IMAGE_URL="$2"
      shift 2
      ;;
    *)
      echo "Unknown option: $1"
      exit 1
      ;;
  esac
done

# Sanitize prompt (replace % with 'percent' to avoid API 400 errors)
SANITIZED_PROMPT=$(echo "$PROMPT" | sed 's/%/percent/g')

# Build query params
PARAMS="model=$MODEL&width=$WIDTH&height=$HEIGHT"

if [[ -n "$SEED" ]]; then
  PARAMS="$PARAMS&seed=$SEED"
fi
if [[ -n "$DURATION" ]]; then
  PARAMS="$PARAMS&duration=$DURATION"
fi
if [[ -n "$NOLOGO" ]]; then
  PARAMS="$PARAMS&nologo=true"
fi
if [[ -n "$PRIVATE" ]]; then
  PARAMS="$PARAMS&private=true"
fi
if [[ -n "$SAFE" ]]; then
  PARAMS="$PARAMS&safe=true"
fi
if [[ -n "$ENHANCE" ]]; then
  PARAMS="$PARAMS&enhance=true"
fi
if [[ -n "$NEGATIVE" ]]; then
  PARAMS="$PARAMS&negative_prompt=$(urlencode "$NEGATIVE")"
fi
if [[ -n "$QUALITY" ]]; then
  PARAMS="$PARAMS&quality=$QUALITY"
fi
if [[ -n "$TRANSPARENT" ]]; then
  PARAMS="$PARAMS&transparent=true"
fi
if [[ -n "$AUDIO" ]]; then
  PARAMS="$PARAMS&audio=true"
fi
if [[ -n "$ASPECT_RATIO" ]]; then
  PARAMS="$PARAMS&aspectRatio=$ASPECT_RATIO"
fi
if [[ -n "$IMAGE_URL" ]]; then
  PARAMS="$PARAMS&image=$(urlencode "$IMAGE_URL")"
fi

# Build URL
ENCODED_PROMPT=$(urlencode "$SANITIZED_PROMPT")
URL="https://gen.pollinations.ai/image/$ENCODED_PROMPT?$PARAMS"

# Determine output filename
if [[ -z "$OUTPUT" ]]; then
  EXT="jpg"
  [[ "$MODEL" =~ (veo|seedance) ]] && EXT="mp4"
  OUTPUT="media_$(date +%s).$EXT"
fi

# Download media
echo "Generating $([[ "$MODEL" =~ (veo|seedance) ]] && echo "video" || echo "image"): $PROMPT"
echo "Model: $MODEL, Size: ${WIDTH}x${HEIGHT}"

if [[ -n "$POLLINATIONS_API_KEY" ]]; then
  curl -s -H "Authorization: Bearer $POLLINATIONS_API_KEY" -o "$OUTPUT" "$URL"
else
  curl -s -o "$OUTPUT" "$URL"
fi

# Check if file was created
if [[ -s "$OUTPUT" ]]; then
  FILE_SIZE=$(ls -lh "$OUTPUT" | awk '{print $5}')
  echo "✓ Saved to: $OUTPUT ($FILE_SIZE)"
else
  echo "✗ Failed to generate media"
  exit 1
fi
