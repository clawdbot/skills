#!/usr/bin/env bash
# Refresh Strava access token using refresh token

set -e

if [ -z "$STRAVA_CLIENT_ID" ] || [ -z "$STRAVA_CLIENT_SECRET" ] || [ -z "$STRAVA_REFRESH_TOKEN" ]; then
  echo "Error: Required environment variables not set"
  echo "Need: STRAVA_CLIENT_ID, STRAVA_CLIENT_SECRET, STRAVA_REFRESH_TOKEN"
  exit 1
fi

RESPONSE=$(curl -s -X POST https://www.strava.com/oauth/token \
  -d client_id="$STRAVA_CLIENT_ID" \
  -d client_secret="$STRAVA_CLIENT_SECRET" \
  -d grant_type=refresh_token \
  -d refresh_token="$STRAVA_REFRESH_TOKEN")

# Extract tokens using grep/sed (works without jq)
NEW_ACCESS_TOKEN=$(echo "$RESPONSE" | grep -o '"access_token":"[^"]*' | cut -d'"' -f4)
NEW_REFRESH_TOKEN=$(echo "$RESPONSE" | grep -o '"refresh_token":"[^"]*' | cut -d'"' -f4)
EXPIRES_AT=$(echo "$RESPONSE" | grep -o '"expires_at":[0-9]*' | cut -d':' -f2)

if [ -n "$NEW_ACCESS_TOKEN" ]; then
  echo "✓ Token refreshed successfully"
  echo "New access token: $NEW_ACCESS_TOKEN"
  echo "New refresh token: $NEW_REFRESH_TOKEN"
  echo "Expires at: $(date -r "$EXPIRES_AT" 2>/dev/null || date -d "@$EXPIRES_AT" 2>/dev/null || echo "$EXPIRES_AT")"
  echo ""
  echo "Update your config with:"
  echo "  STRAVA_ACCESS_TOKEN=\"$NEW_ACCESS_TOKEN\""
  echo "  STRAVA_REFRESH_TOKEN=\"$NEW_REFRESH_TOKEN\""
else
  echo "Error: Token refresh failed"
  echo "$RESPONSE"
  exit 1
fi
