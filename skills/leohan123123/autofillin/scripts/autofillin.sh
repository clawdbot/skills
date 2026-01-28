#!/bin/bash
# AutoFillIn - Form Filling Orchestrator
# Coordinates the form filling process with validation

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m'

# Configuration
DEBUG_PORT="${CHROME_DEBUG_PORT:-9222}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"

show_help() {
    echo -e "${BLUE}AutoFillIn - Automated Form Filling Tool${NC}"
    echo ""
    echo "Usage: $0 [OPTIONS] <URL>"
    echo ""
    echo "Options:"
    echo "  -h, --help           Show this help message"
    echo "  -c, --check          Check environment only"
    echo "  -s, --setup          Run setup script"
    echo "  --start-chrome       Start Chrome with debug mode"
    echo "  --port PORT          Use custom debug port (default: 9222)"
    echo ""
    echo "Examples:"
    echo "  $0 https://example.com/form"
    echo "  $0 --check"
    echo "  $0 --start-chrome https://clawdhub.com/upload"
    echo ""
}

check_environment() {
    echo -e "${CYAN}Checking AutoFillIn Environment...${NC}"
    echo ""
    
    local all_ok=true
    
    # Check Chrome
    echo -n "  Chrome: "
    if [ -x "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" ] || command -v google-chrome &>/dev/null; then
        echo -e "${GREEN}✓ Found${NC}"
    else
        echo -e "${RED}✗ Not found${NC}"
        all_ok=false
    fi
    
    # Check Node.js
    echo -n "  Node.js: "
    if command -v node &>/dev/null; then
        echo -e "${GREEN}✓ $(node -v)${NC}"
    else
        echo -e "${RED}✗ Not found${NC}"
        all_ok=false
    fi
    
    # Check debug port
    echo -n "  Debug Port ${DEBUG_PORT}: "
    if lsof -i:$DEBUG_PORT >/dev/null 2>&1; then
        echo -e "${GREEN}✓ Active${NC}"
    else
        echo -e "${YELLOW}○ Not active (start Chrome first)${NC}"
    fi
    
    # Check config directory
    echo -n "  Config Directory: "
    if [ -d "$HOME/.chrome-autofillin" ]; then
        echo -e "${GREEN}✓ Exists${NC}"
    else
        echo -e "${YELLOW}○ Will be created on setup${NC}"
    fi
    
    echo ""
    
    if [ "$all_ok" = true ]; then
        echo -e "${GREEN}Environment OK${NC}"
        return 0
    else
        echo -e "${RED}Environment issues detected. Run: $0 --setup${NC}"
        return 1
    fi
}

# Parse arguments
ACTION=""
URL=""
CUSTOM_PORT=""

while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            show_help
            exit 0
            ;;
        -c|--check)
            ACTION="check"
            shift
            ;;
        -s|--setup)
            ACTION="setup"
            shift
            ;;
        --start-chrome)
            ACTION="start-chrome"
            shift
            ;;
        --port)
            CUSTOM_PORT="$2"
            shift 2
            ;;
        *)
            URL="$1"
            shift
            ;;
    esac
done

# Apply custom port if specified
if [ -n "$CUSTOM_PORT" ]; then
    DEBUG_PORT="$CUSTOM_PORT"
    export CHROME_DEBUG_PORT="$DEBUG_PORT"
fi

# Execute action
case "$ACTION" in
    check)
        check_environment
        ;;
    setup)
        echo -e "${CYAN}Running environment setup...${NC}"
        bash "$SCRIPT_DIR/setup-env.sh"
        ;;
    start-chrome)
        if [ -z "$URL" ]; then
            URL="about:blank"
        fi
        echo -e "${CYAN}Starting Chrome...${NC}"
        bash "$SCRIPT_DIR/start-chrome.sh" "$URL"
        ;;
    *)
        if [ -z "$URL" ]; then
            show_help
            exit 1
        fi
        
        echo -e "${BLUE}╔══════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${BLUE}║                    AutoFillIn                                ║${NC}"
        echo -e "${BLUE}╚══════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        echo -e "${CYAN}Target URL: ${URL}${NC}"
        echo ""
        
        # Check if Chrome is running with debug port
        if ! lsof -i:$DEBUG_PORT >/dev/null 2>&1; then
            echo -e "${YELLOW}Chrome debug mode not detected.${NC}"
            echo -e "${CYAN}Starting Chrome...${NC}"
            bash "$SCRIPT_DIR/start-chrome.sh" "$URL" &
            sleep 3
        fi
        
        echo -e "${GREEN}Ready for form filling operations.${NC}"
        echo ""
        echo -e "${CYAN}Use browser automation tools to:${NC}"
        echo "  1. Navigate to: ${URL}"
        echo "  2. Use browser_snapshot to analyze page"
        echo "  3. Use browser_type to fill fields"
        echo "  4. Use browser_file_upload to upload files"
        echo "  5. Wait for manual confirmation before submit"
        echo ""
        ;;
esac
