#!/bin/bash
# Logic to choose between Portal frame or OS screenshot
FRAME_PATH="/tmp/clawdbot-screen-latest.png"

if [ -f "$FRAME_PATH" ]; then
    echo "📸 Found active WebRTC frame. Analyzing..."
    SCREENSHOT="$FRAME_PATH"
else
    echo "📸 No portal active. Taking OS screenshot..."
    SCREENSHOT="/tmp/screenshot_$(date +%s).png"
    if command -v import &>/dev/null; then
        import -window root "$SCREENSHOT"
    elif command -v screencapture &>/dev/null; then
        screencapture -x "$SCREENSHOT"
    else
        echo "Error: No capture method found."
        exit 1
    fi
fi

# Call the internal agent vision analysis
clawdbot agent --message "Read the image at $SCREENSHOT and describe the main content clearly."
