#!/bin/bash
# Complete Unraid Monitoring Dashboard (Multi-Server)
# Gets system status, disk health, and resource usage for all configured servers

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
QUERY_SCRIPT="$SCRIPT_DIR/unraid-query.sh"
CONFIG_FILE="$HOME/.clawdbot/credentials/unraid/config.json"
OUTPUT_FILE="$HOME/clawd/memory/bank/unraid-inventory.md"

# Ensure output directory exists
mkdir -p "$(dirname "$OUTPUT_FILE")"

# Start the report
echo "# Unraid Fleet Dashboard" > "$OUTPUT_FILE"
echo "Generated at: $(date)" >> "$OUTPUT_FILE"
echo "" >> "$OUTPUT_FILE"

# Function to process a single server
process_server() {
    local NAME="$1"
    local URL="$2"
    local API_KEY="$3"

    echo "Querying server: $NAME..."
    
    export UNRAID_URL="$URL"
    export UNRAID_API_KEY="$API_KEY"
    export IGNORE_ERRORS="true"

    QUERY='query Dashboard {
      info {
        time
        cpu { model cores threads }
        os { distro release }
        system { manufacturer model }
      }
      metrics {
        cpu { percentTotal }
        memory { total used free percentTotal }
      }
      array {
        state
        capacity { kilobytes { total free used } }
        disks { name device temp status fsSize fsFree fsUsed isSpinning numErrors }
        caches { name device temp status fsSize fsFree fsUsed fsType type }
        parityCheckStatus { status progress errors }
      }
      disks { id name }
      shares { name comment }
      docker {
        containers { names image state status }
      }
      vms { domains { id name state } }
      recentLog: logFile(path: \"syslog\", lines: 100) { content }
      online
      isSSOEnabled
    }'

    RESPONSE=$("$QUERY_SCRIPT" -q "$QUERY" -f json)
    
    # Debug output
    echo "$RESPONSE" > "${NAME}_debug.json"
    
    # Check if response is valid JSON
    if ! echo "$RESPONSE" | jq -e . >/dev/null 2>&1; then
        echo "Error querying $NAME: Invalid response"
        echo "Response saved to ${NAME}_debug.json"
        echo "## Server: $NAME (⚠️ Error)" >> "$OUTPUT_FILE"
        echo "Failed to retrieve data." >> "$OUTPUT_FILE"
        return
    fi

    # Append to report
    echo "## Server: $NAME" >> "$OUTPUT_FILE"
    
    # System Info
    CPU_MODEL=$(echo "$RESPONSE" | jq -r '.data.info.cpu.model')
    OS_REL=$(echo "$RESPONSE" | jq -r '.data.info.os.release')
    UPTIME=$(echo "$RESPONSE" | jq -r '.data.metrics.cpu.percentTotal | tostring + "% CPU Load"')
    
    echo "**OS:** $OS_REL | **CPU:** $CPU_MODEL" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"

    # Array capacity
    ARRAY_TOTAL=$(echo "$RESPONSE" | jq -r '.data.array.capacity.kilobytes.total')
    ARRAY_FREE=$(echo "$RESPONSE" | jq -r '.data.array.capacity.kilobytes.free')
    ARRAY_USED=$(echo "$RESPONSE" | jq -r '.data.array.capacity.kilobytes.used')
    
    if [ "$ARRAY_TOTAL" != "null" ] && [ "$ARRAY_TOTAL" -gt 0 ]; then
        ARRAY_TOTAL_GB=$((ARRAY_TOTAL / 1024 / 1024))
        ARRAY_FREE_GB=$((ARRAY_FREE / 1024 / 1024))
        ARRAY_USED_GB=$((ARRAY_USED / 1024 / 1024))
        ARRAY_USED_PCT=$((ARRAY_USED * 100 / ARRAY_TOTAL))
        echo "### Storage" >> "$OUTPUT_FILE"
        echo "- **Array:** ${ARRAY_USED_GB}GB / ${ARRAY_TOTAL_GB}GB used (${ARRAY_USED_PCT}%)" >> "$OUTPUT_FILE"
    fi

    # Cache pools
    echo "- **Cache Pools:**" >> "$OUTPUT_FILE"
    echo "$RESPONSE" | jq -r '.data.array.caches[] | "  - \(.name) (\(.device)): \(.temp)°C - \(.status) - \(if .fsSize then "\((.fsUsed / 1024 / 1024 | floor))GB / \((.fsSize / 1024 / 1024 | floor))GB used" else "N/A" end)"' >> "$OUTPUT_FILE"
    
    # Docker
    TOTAL_CONTAINERS=$(echo "$RESPONSE" | jq '[.data.docker.containers[]] | length')
    RUNNING_CONTAINERS=$(echo "$RESPONSE" | jq '[.data.docker.containers[] | select(.state == "RUNNING")] | length')
    
    echo "" >> "$OUTPUT_FILE"
    echo "### Workloads" >> "$OUTPUT_FILE"
    echo "- **Docker:** ${TOTAL_CONTAINERS} containers (${RUNNING_CONTAINERS} running)" >> "$OUTPUT_FILE"
    
    # Unhealthy containers
    UNHEALTHY=$(echo "$RESPONSE" | jq -r '.data.docker.containers[] | select(.status | test("unhealthy|restarting"; "i")) | "  - ⚠️  \(.names[0]): \(.status)"')
    if [ -n "$UNHEALTHY" ]; then
        echo "$UNHEALTHY" >> "$OUTPUT_FILE"
    fi

    # VMs
    if [ "$(echo "$RESPONSE" | jq -r '.data.vms.domains')" != "null" ]; then
        TOTAL_VMS=$(echo "$RESPONSE" | jq '[.data.vms.domains[]] | length')
        RUNNING_VMS=$(echo "$RESPONSE" | jq '[.data.vms.domains[] | select(.state == "RUNNING")] | length')
        echo "- **VMs:** ${TOTAL_VMS} VMs (${RUNNING_VMS} running)" >> "$OUTPUT_FILE"
    else
        echo "- **VMs:** Service disabled or no data" >> "$OUTPUT_FILE"
    fi
    
    # Disk Health
    echo "" >> "$OUTPUT_FILE"
    echo "### Health" >> "$OUTPUT_FILE"
    
    HOT_DISKS=$(echo "$RESPONSE" | jq -r '.data.array.disks[] | select(.temp > 45) | "- ⚠️  \(.name): \(.temp)°C (HIGH)"')
    DISK_ERRORS=$(echo "$RESPONSE" | jq -r '.data.array.disks[] | select(.numErrors > 0) | "- ❌ \(.name): \(.numErrors) errors"')
    
    if [ -z "$HOT_DISKS" ] && [ -z "$DISK_ERRORS" ]; then
        echo "- ✅ All disks healthy" >> "$OUTPUT_FILE"
    else
        [ -n "$HOT_DISKS" ] && echo "$HOT_DISKS" >> "$OUTPUT_FILE"
        [ -n "$DISK_ERRORS" ] && echo "$DISK_ERRORS" >> "$OUTPUT_FILE"
    fi
    
    echo "" >> "$OUTPUT_FILE"
    echo "---" >> "$OUTPUT_FILE"
    echo "" >> "$OUTPUT_FILE"
}

# Main loop
if [ -f "$CONFIG_FILE" ]; then
    # Read servers array
    # We use jq -c to output each object on a single line, then read line by line
    jq -c '.servers[]' "$CONFIG_FILE" | while read -r server; do
        NAME=$(echo "$server" | jq -r '.name')
        URL=$(echo "$server" | jq -r '.url')
        KEY=$(echo "$server" | jq -r '.apiKey')
        
        process_server "$NAME" "$URL" "$KEY"
    done
else
    echo "Config file not found: $CONFIG_FILE"
    exit 1
fi

echo "Dashboard saved to: $OUTPUT_FILE"
cat "$OUTPUT_FILE"
