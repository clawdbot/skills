#!/bin/bash
# Vision Model Environment Discovery

# Try Clawdbot config first
VISION_URL=$(clawdbot config get skills.screen-monitor.visionUrl 2>/dev/null || echo "")

# Fallback to environment variable
VISION_URL=${VISION_URL:-"http://localhost:8080"}

# Verify service is reachable
if curl -sf "$VISION_URL/v1/models" > /dev/null 2>&1; then
    echo "$VISION_URL"
    exit 0
else
    echo "ERROR: Vision model not reachable at $VISION_URL" >&2
    exit 1
fi
