#!/bin/bash
# AutoFillIn Environment Setup Script
# Configures Chrome, Playwright, and MCP for automated form filling

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
CHROME_DEBUG_PORT="${CHROME_DEBUG_PORT:-9222}"
CHROME_USER_DATA_DIR="${CHROME_USER_DATA_DIR:-$HOME/.chrome-autofillin}"
CHROME_PATH="${CHROME_PATH:-}"

echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║           AutoFillIn Environment Setup                       ║${NC}"
echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""

# Detect OS
detect_os() {
    case "$(uname -s)" in
        Darwin*)    echo "macos" ;;
        Linux*)     echo "linux" ;;
        MINGW*|MSYS*|CYGWIN*) echo "windows" ;;
        *)          echo "unknown" ;;
    esac
}

OS=$(detect_os)
echo -e "${CYAN}[1/6] Detected OS: ${OS}${NC}"

# Find Chrome
find_chrome() {
    if [ -n "$CHROME_PATH" ] && [ -x "$CHROME_PATH" ]; then
        echo "$CHROME_PATH"
        return 0
    fi
    
    case "$OS" in
        macos)
            local paths=(
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
                "/Applications/Chromium.app/Contents/MacOS/Chromium"
                "$HOME/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
            )
            ;;
        linux)
            local paths=(
                "/usr/bin/google-chrome"
                "/usr/bin/google-chrome-stable"
                "/usr/bin/chromium"
                "/usr/bin/chromium-browser"
                "/snap/bin/chromium"
            )
            ;;
        windows)
            local paths=(
                "/c/Program Files/Google/Chrome/Application/chrome.exe"
                "/c/Program Files (x86)/Google/Chrome/Application/chrome.exe"
            )
            ;;
    esac
    
    for path in "${paths[@]}"; do
        if [ -x "$path" ]; then
            echo "$path"
            return 0
        fi
    done
    
    # Try which command
    which google-chrome 2>/dev/null || which chromium 2>/dev/null || echo ""
}

CHROME_EXECUTABLE=$(find_chrome)
if [ -z "$CHROME_EXECUTABLE" ]; then
    echo -e "${RED}[ERROR] Chrome not found!${NC}"
    echo -e "${YELLOW}Please install Google Chrome:${NC}"
    case "$OS" in
        macos)
            echo "  brew install --cask google-chrome"
            echo "  OR download from: https://www.google.com/chrome/"
            ;;
        linux)
            echo "  sudo apt install google-chrome-stable"
            echo "  OR sudo dnf install google-chrome-stable"
            ;;
    esac
    exit 1
fi
echo -e "${GREEN}[2/6] Chrome found: ${CHROME_EXECUTABLE}${NC}"

# Create user data directory
echo -e "${CYAN}[3/6] Creating Chrome profile directory...${NC}"
mkdir -p "$CHROME_USER_DATA_DIR"
echo -e "${GREEN}  ✓ Profile directory: ${CHROME_USER_DATA_DIR}${NC}"

# Check if port is available
check_port() {
    local port=$1
    if lsof -i:$port >/dev/null 2>&1; then
        return 1  # Port in use
    fi
    return 0  # Port available
}

echo -e "${CYAN}[4/6] Checking debug port ${CHROME_DEBUG_PORT}...${NC}"
if ! check_port $CHROME_DEBUG_PORT; then
    echo -e "${YELLOW}  ⚠ Port ${CHROME_DEBUG_PORT} is in use${NC}"
    
    # Check if it's Chrome using the port
    CHROME_PID=$(lsof -t -i:$CHROME_DEBUG_PORT 2>/dev/null || true)
    if [ -n "$CHROME_PID" ]; then
        echo -e "${YELLOW}  Killing existing process on port ${CHROME_DEBUG_PORT}...${NC}"
        kill $CHROME_PID 2>/dev/null || true
        sleep 2
    fi
fi
echo -e "${GREEN}  ✓ Port ${CHROME_DEBUG_PORT} ready${NC}"

# Check Node.js and npm
echo -e "${CYAN}[5/6] Checking Node.js environment...${NC}"
if ! command -v node &>/dev/null; then
    echo -e "${RED}[ERROR] Node.js not found!${NC}"
    echo -e "${YELLOW}Please install Node.js:${NC}"
    echo "  brew install node"
    echo "  OR use nvm: curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash"
    exit 1
fi

NODE_VERSION=$(node -v)
echo -e "${GREEN}  ✓ Node.js: ${NODE_VERSION}${NC}"

# Check/Install Playwright
echo -e "${CYAN}[6/6] Checking Playwright...${NC}"
if ! npm list -g @playwright/test &>/dev/null 2>&1; then
    echo -e "${YELLOW}  Installing Playwright globally...${NC}"
    npm install -g @playwright/test 2>/dev/null || true
fi

# Install Playwright browsers if needed
if ! npx playwright install chromium --dry-run &>/dev/null 2>&1; then
    echo -e "${YELLOW}  Installing Playwright Chromium browser...${NC}"
    npx playwright install chromium 2>/dev/null || true
fi
echo -e "${GREEN}  ✓ Playwright ready${NC}"

# Generate launch script
LAUNCH_SCRIPT="$CHROME_USER_DATA_DIR/launch-chrome.sh"
cat > "$LAUNCH_SCRIPT" << EOF
#!/bin/bash
# Auto-generated Chrome launch script for AutoFillIn

CHROME_PATH="$CHROME_EXECUTABLE"
DEBUG_PORT="${CHROME_DEBUG_PORT}"
USER_DATA_DIR="${CHROME_USER_DATA_DIR}"

# Kill any existing Chrome with debug port
pkill -f "remote-debugging-port=\${DEBUG_PORT}" 2>/dev/null || true
sleep 1

# Launch Chrome with debug port
"\$CHROME_PATH" \\
    --remote-debugging-port=\${DEBUG_PORT} \\
    --user-data-dir="\${USER_DATA_DIR}" \\
    --no-first-run \\
    --no-default-browser-check \\
    "\$@" &

echo "Chrome launched with debug port \${DEBUG_PORT}"
echo "Connect via: http://localhost:\${DEBUG_PORT}"
EOF

chmod +x "$LAUNCH_SCRIPT"

# Generate environment config
CONFIG_FILE="$CHROME_USER_DATA_DIR/autofillin.env"
cat > "$CONFIG_FILE" << EOF
# AutoFillIn Environment Configuration
# Generated: $(date)

CHROME_PATH="$CHROME_EXECUTABLE"
CHROME_DEBUG_PORT=$CHROME_DEBUG_PORT
CHROME_USER_DATA_DIR="$CHROME_USER_DATA_DIR"
LAUNCH_SCRIPT="$LAUNCH_SCRIPT"
OS="$OS"
NODE_VERSION="$NODE_VERSION"
EOF

echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║           Setup Complete!                                     ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${CYAN}Configuration:${NC}"
echo -e "  Chrome: ${CHROME_EXECUTABLE}"
echo -e "  Debug Port: ${CHROME_DEBUG_PORT}"
echo -e "  Profile Dir: ${CHROME_USER_DATA_DIR}"
echo -e "  Launch Script: ${LAUNCH_SCRIPT}"
echo ""
echo -e "${CYAN}To start Chrome with debug mode:${NC}"
echo -e "  ${LAUNCH_SCRIPT} https://example.com"
echo ""
echo -e "${CYAN}Or manually:${NC}"
echo -e "  \"${CHROME_EXECUTABLE}\" --remote-debugging-port=${CHROME_DEBUG_PORT} --user-data-dir=\"${CHROME_USER_DATA_DIR}\" URL"
echo ""
