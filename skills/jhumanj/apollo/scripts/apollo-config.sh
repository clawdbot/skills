#!/bin/bash
set -euo pipefail

# Loads config for Apollo API scripts.
# Expected file: /Users/jhumanj/clawd/config/apollo.env

CONFIG_FILE="/Users/jhumanj/clawd/config/apollo.env"

if [ -f "$CONFIG_FILE" ]; then
  # shellcheck disable=SC1090
  source "$CONFIG_FILE"
fi

if [ -z "${APOLLO_BASE_URL:-}" ]; then
  echo "Missing APOLLO_BASE_URL. Create $CONFIG_FILE (see /Users/jhumanj/clawd/config/apollo.env.example)." >&2
  exit 1
fi

if [ -z "${APOLLO_API_KEY:-}" ]; then
  echo "Missing APOLLO_API_KEY. Create $CONFIG_FILE (see /Users/jhumanj/clawd/config/apollo.env.example)." >&2
  exit 1
fi

APOLLO_BASE_URL="${APOLLO_BASE_URL%/}"

export APOLLO_BASE_URL
export APOLLO_API_KEY
