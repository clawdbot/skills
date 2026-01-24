---
name: homey-cli
description: Control Homey home automation hub via CLI. Use when you need to control smart home devices (lights, thermostats, sockets, etc.), check device status, list zones, trigger flows, or perform any Homey automation tasks. Supports on/off, dimming, color changes, temperature control, and device inspection. Safe, capability-allowlisted operations only.
---

# Homey CLI

Safe, agent-friendly CLI for controlling Homey home automation hubs.

## What This Skill Provides

- **Device control**: Turn devices on/off, dim lights, change colors, set temperatures
- **Device inspection**: List devices, check status, read capabilities
- **Zone management**: List zones and devices per zone
- **Flow control**: List and trigger flows
- **Inventory**: Get complete hub overview

## Setup

### 1. Install Dependencies

```bash
cd skills/homey-cli
npm install
```

### 2. Create Homey App Credentials

1. Go to https://tools.developer.homey.app/tools/app
2. Create a new app with:
   - **Callback URL**: `http://localhost:8787/callback`
   - Note your **Client ID** and **Client Secret**

### 3. Configure Environment

Create `.env` file:

```bash
export HOMEY_CLIENT_ID="your-client-id"
export HOMEY_CLIENT_SECRET="your-client-secret"
export HOMEY_REDIRECT_URL="http://localhost:8787/callback"
```

### 4. Login

```bash
bash run.sh auth login
```

Follow the OAuth flow in your browser. Tokens are stored in `~/.config/homey-cli/`.

## Usage

### List Homeys

```bash
bash run.sh homey list
```

### Select Active Homey

```bash
bash run.sh homey use <homeyId>
```

### Device Operations

```bash
# List all devices
bash run.sh devices list

# List devices as JSON
bash run.sh devices list --json

# Get specific device
bash run.sh devices get <deviceId>

# Read capability value
bash run.sh devices read <deviceId> onoff

# Control devices
bash run.sh devices on <deviceId>
bash run.sh devices off <deviceId>
bash run.sh devices dim <deviceId> 0.4
bash run.sh devices color <deviceId> #FF8800
bash run.sh devices temperature <deviceId> 21.5
```

### Flow Operations

```bash
# List flows
bash run.sh flows list

# Trigger flow
bash run.sh flows trigger <flowId>
```

### Complete Inventory

```bash
bash run.sh inventory --json
```

## Safety Model

Write operations are **capability-allowlisted** for safety:

- Default allowed: `onoff`, `dim`, `light_hue`, `light_saturation`, `light_temperature`, `target_temperature`
- Override via: `export HOMEY_CLI_ALLOWED_CAPABILITIES=onoff,dim,target_temperature`

Destructive operations (delete devices, modify flows, change app settings) are **not supported**.

## Common Queries

When users ask:
- "Turn on the kitchen lights" → List devices, find match, use `devices on <deviceId>`
- "Dim living room to 50%" → Find device, use `devices dim <deviceId> 0.5`
- "What's the temperature in the bedroom?" → Find device, use `devices read <deviceId> measure_temperature`
- "List all my lights" → Use `devices list --json` and filter by class/capabilities

## Configuration Storage

- **Tokens**: `~/.config/homey-cli/credentials.json`
- **Active Homey**: `~/.config/homey-cli/config.json`

## Troubleshooting

- **Auth errors**: Re-run `bash run.sh auth login`
- **Device not found**: Check device name/ID with `bash run.sh devices list`
- **Capability not allowed**: Add to `HOMEY_CLI_ALLOWED_CAPABILITIES` or check if it's a read-only capability
