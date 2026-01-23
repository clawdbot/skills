# Unraid API Skill

Query and monitor Unraid servers via the GraphQL API.

## What's Included

This skill provides complete access to all 27 read-only Unraid GraphQL API endpoints.

### Files

```
skills/unraid/
├── SKILL.md                           # Main skill documentation
├── README.md                          # This file
├── scripts/
│   └── unraid-query.sh               # GraphQL query helper script
├── examples/
│   ├── monitoring-dashboard.sh       # Complete system dashboard
│   ├── disk-health.sh                # Disk temperature & health check
│   └── read-logs.sh                  # Log file reader
└── references/
    ├── api-reference.md              # Complete API documentation
    └── quick-reference.md            # Common queries cheat sheet
```

## Quick Start

1. **Set your credentials:**
   ```bash
   export UNRAID_URL="https://your-unraid-server/graphql"
   export UNRAID_API_KEY="your-api-key"
   ```

2. **Run a query:**
   ```bash
   cd skills/unraid
   ./scripts/unraid-query.sh -q "{ online }"
   ```

3. **Run examples:**
   ```bash
   ./examples/monitoring-dashboard.sh
   ./examples/disk-health.sh
   ```

## Triggers

This skill activates when you mention:
- "check Unraid"
- "monitor Unraid"
- "Unraid API"
- "Unraid disk temperatures"
- "Unraid array status"
- "read Unraid logs"
- And more Unraid-related monitoring tasks

## Features

- **27 working endpoints** - All read-only queries documented
- **Helper script** - Easy CLI interface for GraphQL queries
- **Example scripts** - Ready-to-use monitoring scripts
- **Complete reference** - Detailed documentation with examples
- **Quick reference** - Common queries cheat sheet

## Endpoints Covered

### System & Monitoring
- System info (CPU, OS, hardware)
- Real-time metrics (CPU %, memory %)
- Configuration & settings
- Log files (list & read)

### Storage
- Array status & disks
- All physical disks (including cache/USB)
- Network shares
- Parity check status

### Virtualization
- Docker containers
- Virtual machines

### Power & Alerts
- UPS devices
- System notifications

### Administration
- API key management
- User & authentication
- Server registration
- UI customization

## Requirements

- **Unraid 7.2+** (GraphQL API)
- **API Key** with Viewer role
- **jq** for JSON parsing (usually pre-installed)
- **curl** for HTTP requests

## Getting an API Key

1. Log in to Unraid WebGUI
2. Settings → Management Access → API Keys
3. Click "Create API Key"
4. Name: "monitoring" (or whatever you like)
5. Role: Select "Viewer" (read-only)
6. Copy the generated key

## Documentation

- **SKILL.md** - Start here for task-oriented guidance
- **references/api-reference.md** - Complete endpoint reference
- **references/quick-reference.md** - Quick query examples

## Examples

### System Status
```bash
./scripts/unraid-query.sh -q "{ online metrics { cpu { percentTotal } } }"
```

### Disk Health
```bash
./examples/disk-health.sh
```

### Complete Dashboard
```bash
./examples/monitoring-dashboard.sh
```

### Read Logs
```bash
./examples/read-logs.sh syslog 20
```

## Notes

- All sizes are in **kilobytes**
- Temperatures are in **Celsius**
- Docker container logs are **not accessible** via API (use SSH)
- Poll no faster than every **5 seconds** to avoid server load

## Version

- **Skill Version:** 1.0.0
- **API Version:** Unraid 7.2 GraphQL
- **Tested:** 2026-01-21
- **Endpoints:** 27 working read-only queries
