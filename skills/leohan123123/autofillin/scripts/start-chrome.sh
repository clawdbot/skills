#!/bin/bash
# AutoFillIn - Start Chrome with Debug Mode
# This script launches Chrome with remote debugging enabled
#
# Usage:
#   start-chrome.sh [URL] [--use-default-profile]
#   
# Options:
#   --use-default-profile   Use your existing Chrome profile (keeps login state!)
#   --headless             Run in headless mode

set -e

# Load configuration
CONFIG_DIR="${CHROME_USER_DATA_DIR:-$HOME/.chrome-autofillin}"
CONFIG_FILE="$CONFIG_DIR/autofillin.env"

if [ -f "$CONFIG_FILE" ]; then
    source "$CONFIG_FILE"
fi

# Defaults
CHROME_PATH="${CHROME_PATH:-/Applications/Google Chrome.app/Contents/MacOS/Google Chrome}"
DEBUG_PORT="${CHROME_DEBUG_PORT:-9222}"

# Detect existing Chrome profile directory
DEFAULT_CHROME_PROFILE="$HOME/Library/Application Support/Google/Chrome"
ISOLATED_PROFILE="$HOME/.chrome-autofillin"

# Default: use isolated profile (change to DEFAULT_CHROME_PROFILE to keep logins)
USER_DATA_DIR="${CHROME_USER_DATA_DIR:-$ISOLATED_PROFILE}"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

# Parse arguments
URL="about:blank"
HEADLESS="false"
USE_DEFAULT_PROFILE="false"

for arg in "$@"; do
    case $arg in
        --use-default-profile)
            USE_DEFAULT_PROFILE="true"
            ;;
        --headless)
            HEADLESS="true"
            ;;
        http*|about:*)
            URL="$arg"
            ;;
    esac
done

# Select profile based on flag
if [ "$USE_DEFAULT_PROFILE" = "true" ]; then
    USER_DATA_DIR="$DEFAULT_CHROME_PROFILE"
    echo -e "${GREEN}Using DEFAULT Chrome profile (login state preserved!)${NC}"
else
    USER_DATA_DIR="$ISOLATED_PROFILE"
    echo -e "${YELLOW}Using isolated profile (no login state)${NC}"
fi

echo -e "${CYAN}Starting Chrome with Debug Mode...${NC}"

# IMPORTANT: Must close ALL Chrome instances first to use debug mode
CHROME_RUNNING=$(pgrep -x "Google Chrome" 2>/dev/null || true)
if [ -n "$CHROME_RUNNING" ]; then
    echo -e "${YELLOW}⚠️  Chrome is already running!${NC}"
    echo -e "${YELLOW}   Debug mode requires closing existing Chrome instances.${NC}"
    read -p "Close Chrome and continue? (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        pkill -x "Google Chrome" 2>/dev/null || true
        sleep 2
    else
        echo -e "${RED}Aborted. Please close Chrome manually and retry.${NC}"
        exit 1
    fi
fi

# Kill existing debug port if occupied
if lsof -i:$DEBUG_PORT >/dev/null 2>&1; then
    echo -e "${YELLOW}Killing existing process on port ${DEBUG_PORT}...${NC}"
    pkill -f "remote-debugging-port=${DEBUG_PORT}" 2>/dev/null || true
    sleep 2
fi

# Create user data directory
mkdir -p "$USER_DATA_DIR"

# Build Chrome arguments
CHROME_ARGS=(
    "--remote-debugging-port=${DEBUG_PORT}"
    "--user-data-dir=${USER_DATA_DIR}"
    "--no-first-run"
    "--no-default-browser-check"
    "--disable-background-timer-throttling"
    "--disable-backgrounding-occluded-windows"
    "--disable-renderer-backgrounding"
)

if [ "$HEADLESS" = "true" ]; then
    CHROME_ARGS+=("--headless=new")
fi

# Launch Chrome
echo -e "${GREEN}Launching Chrome...${NC}"
echo -e "  URL: ${URL}"
echo -e "  Debug Port: ${DEBUG_PORT}"
echo -e "  Profile: ${USER_DATA_DIR}"

"$CHROME_PATH" "${CHROME_ARGS[@]}" "$URL" &
CHROME_PID=$!

sleep 2

# Verify Chrome started
if ! kill -0 $CHROME_PID 2>/dev/null; then
    echo -e "${YELLOW}Warning: Chrome may have failed to start${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Chrome running (PID: ${CHROME_PID})${NC}"
echo -e "${GREEN}✓ Debug endpoint: http://localhost:${DEBUG_PORT}${NC}"
echo ""
echo -e "${CYAN}To connect:${NC}"
echo "  - Playwright: browserType.connectOverCDP('http://localhost:${DEBUG_PORT}')"
echo "  - DevTools: Open http://localhost:${DEBUG_PORT} in browser"
echo ""

# Keep script running to show Chrome is active
wait $CHROME_PID 2>/dev/null || true
