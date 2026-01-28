#!/bin/bash

# ทำให้ไฟล์ Python สามารถ Execute ได้
chmod +x "$(dirname "$0")/gold-price-mcp.py"

# รัน Python MCP service
"$(dirname "$0")/gold-price-mcp.py" "$@"