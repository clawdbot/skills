#!/bin/sh
set -eu

OUT_PATH="$1"
TOPIC="${2:-tech}"
COUNT="${3:-5}"
OFFSET="${4:-0}"

# Ensure we have a venv with dependencies (avoid touching system python).
VENV_DIR="./tmp/hn-venv"
PY="$VENV_DIR/bin/python"

if [ ! -x "$PY" ]; then
  python3 -m venv "$VENV_DIR"
  "$PY" -m pip install --quiet --disable-pip-version-check google-genai pillow
fi

JSON="$(node skills/hn-digest/scripts/hn.mjs --count "$COUNT" --offset "$OFFSET" --topic "$TOPIC" --format json)"
PROMPT="$(printf "%s" "$JSON" | node skills/hn-digest/scripts/mood_prompt.mjs --topic "$TOPIC")"

"$PY" skills/hn-digest/scripts/nano_banana_mood.py --out "$OUT_PATH" --resolution 1K --prompt "$PROMPT"
