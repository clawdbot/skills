---
name: enzoldhazam
description: Control NGBS iCON Smart Home thermostats. Use when the user asks about home temperature, heating, thermostat control, or wants to adjust room temperatures.
---

# enzoldhazam

Control NGBS iCON Smart Home thermostats via enzoldhazam.hu.

## Setup

1. Install the CLI:
```bash
git clone https://github.com/daniel-laszlo/enzoldhazam.git
cd enzoldhazam
go build -o enzoldhazam ./cmd/enzoldhazam
sudo mv enzoldhazam /usr/local/bin/
```

2. Login (credentials stored in macOS Keychain):
```bash
enzoldhazam login
```

Or set environment variables:
```bash
export ENZOLDHAZAM_USER="your-email"
export ENZOLDHAZAM_PASS="your-password"
```

## Commands

| Command | Description |
|---------|-------------|
| `enzoldhazam status` | Show all rooms with temperatures |
| `enzoldhazam status --json` | JSON output for parsing |
| `enzoldhazam get <room>` | Get specific room details |
| `enzoldhazam set <room> <temp>` | Set target temperature |
| `enzoldhazam login` | Save credentials to Keychain |
| `enzoldhazam logout` | Clear stored credentials |

## Examples

```bash
# Check current temperatures
enzoldhazam status

# Set a room to 22°C
enzoldhazam set "Living Room" 22

# Get room info as JSON
enzoldhazam get "Bedroom" --json
```

## Instructions

When the user asks about home temperature, heating, or thermostats:

1. Use `enzoldhazam status` to check current state
2. Use `enzoldhazam set <room> <temp>` to change temperature
3. Parse `--json` output when you need to process the data

Always confirm temperature changes with the user before executing.
