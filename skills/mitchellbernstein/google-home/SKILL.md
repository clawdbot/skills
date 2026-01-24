---
name: google-home
description: Control Google Nest devices (thermostats, cameras, doorbells) via the Google Smart Device Management API using curl and jq.
metadata: {"clawdbot":{"emoji":"🏠","requires":{"bins":["curl","jq"]}}
---

# Google Home / Nest CLI

Control Google Nest devices via the Smart Device Management (SDM) API using curl + jq.

## Setup (Required)

1. **Create a Google Cloud Project**
   - Go to https://console.cloud.google.com
   - Create a new project

2. **Enable the SDM API**
   - APIs & Services → Library
   - Search "Smart Device Management"
   - Enable it

3. **Create OAuth Credentials**
   - APIs & Services → Credentials
   - Create OAuth 2.0 Client ID
   - Download the JSON file
   - Extract `client_id` and `client_secret`

4. **Register Your Devices**
   - Visit https://nests.google.com/frame/register-user
   - Accept the terms

5. **Get Access Token**
   ```bash
   # Replace with your values
   curl -s \
     -d "client_id=YOUR_CLIENT_ID" \
     -d "client_secret=YOUR_CLIENT_SECRET" \
     -d "refresh_token=YOUR_REFRESH_TOKEN" \
     -d "grant_type=refresh_token" \
     https://www.googleapis.com/oauth2/v4/token
   ```

## Quick Start

```bash
# List devices
google-home-cli devices

# Get thermostat info
google-home-cli thermostat "Living Room" --info

# Set temperature (heat/cool/auto)
google-home-cli thermostat "Living Room" --temp 72

# Query camera
google-home-cli camera "Front Door" --status
```

## Device Commands

### Thermostats
- `google-home-cli thermostat <name>` — show current temp/humidity
- `--temp <degrees>` — set target temperature
- `--mode heat|cool|auto` — set HVAC mode
- `--fan on|auto` — control fan

### Cameras & Doorbells
- `google-home-cli camera <name>` — get stream/status
- `--snapshot` — download current image
- `--stream` — start live stream URL

### Speakers & Displays
- `google-home-cli speaker <name>` — device info
- `--volume 0-100` — set volume
- `--stop` — stop playback

## Environment Variables

```bash
export GOOGLE_HOME_CLIENT_ID="your-client-id"
export GOOGLE_HOME_CLIENT_SECRET="your-client-secret"
export GOOGLE_HOME_ACCESS_TOKEN="your-access-token"
```

## Alternative: Direct API Calls

```bash
# List all devices
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://smartdevicemanagement.googleapis.com/v1/enterprises/YOUR_PROJECT_ID/devices"

# Get device traits
curl -s -H "Authorization: Bearer $ACCESS_TOKEN" \
  "https://smartdevicemanagement.googleapis.com/v1/enterprises/YOUR_PROJECT_ID/devices/YOUR_DEVICE_ID"
```

## Helper Script

A `nest` CLI helper is included at `scripts/nest`:

```bash
# Make it available globally
ln -sf /Users/mitchellbernstein/clawd/skills/google-home/scripts/nest /usr/local/bin/nest

# List devices
nest list

# Get thermostat status
nest status "enterprises/PROJECT_ID/devices/DEVICE_ID"

# Set temperature (Celsius)
nest temp "enterprises/PROJECT_ID/devices/DEVICE_ID" 22

# Set mode
nest mode "enterprises/PROJECT_ID/devices/DEVICE_ID" HEAT
```

## Configuration

Create `~/.config/google-home/config.json`:

```json
{
  "project_id": "your-google-cloud-project-id",
  "access_token": "your-oauth-access-token"
}
```

## Notes

- Tokens expire; refresh them periodically
- Device names use full path: `enterprises/PROJECT_ID/devices/DEVICE_ID`
- Temperature is in Celsius (convert from Fahrenheit if needed)
- Camera streams require additional permissions
