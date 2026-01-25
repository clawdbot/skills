---
name: nest-devices
description: Control Nest smart home devices (thermostat, cameras, doorbell) via the Device Access API. Use when asked to check or adjust home temperature, view camera feeds, check who's at the door, monitor rooms, or set up temperature schedules.
metadata:
  clawdbot:
    emoji: "🏠"
---

# Nest Device Access

Control Nest devices via Google's Smart Device Management API.

## Setup

### 1. Google Cloud & Device Access

1. Create a Google Cloud project at [console.cloud.google.com](https://console.cloud.google.com)
2. Pay the $5 fee and create a Device Access project at [console.nest.google.com/device-access](https://console.nest.google.com/device-access)
3. Create OAuth 2.0 credentials (Web application type)
4. Add `https://www.google.com` as an authorized redirect URI
5. Link your Nest account to the Device Access project

### 2. Get Refresh Token

Run the OAuth flow to get a refresh token:

```bash
# 1. Open this URL in browser (replace CLIENT_ID and PROJECT_ID):
https://nestservices.google.com/partnerconnections/PROJECT_ID/auth?redirect_uri=https://www.google.com&access_type=offline&prompt=consent&client_id=CLIENT_ID&response_type=code&scope=https://www.googleapis.com/auth/sdm.service

# 2. Authorize and copy the 'code' parameter from the redirect URL

# 3. Exchange code for tokens:
curl -X POST https://oauth2.googleapis.com/token \
  -d "client_id=CLIENT_ID" \
  -d "client_secret=CLIENT_SECRET" \
  -d "code=AUTH_CODE" \
  -d "grant_type=authorization_code" \
  -d "redirect_uri=https://www.google.com"
```

### 3. Store Credentials

Store in 1Password or environment variables:

**1Password** (recommended):
Create an item with fields: `project_id`, `client_id`, `client_secret`, `refresh_token`

**Environment variables:**
```bash
export NEST_PROJECT_ID="your-project-id"
export NEST_CLIENT_ID="your-client-id"
export NEST_CLIENT_SECRET="your-client-secret"
export NEST_REFRESH_TOKEN="your-refresh-token"
```

## Usage

### List devices
```bash
python3 scripts/nest.py list
```

### Thermostat

```bash
# Get status
python3 scripts/nest.py get <device_id>

# Set temperature (Celsius)
python3 scripts/nest.py set-temp <device_id> 21 --unit c --type heat

# Set temperature (Fahrenheit)
python3 scripts/nest.py set-temp <device_id> 70 --unit f --type heat

# Change mode (HEAT, COOL, HEATCOOL, OFF)
python3 scripts/nest.py set-mode <device_id> HEAT

# Eco mode
python3 scripts/nest.py set-eco <device_id> MANUAL_ECO
```

### Cameras

```bash
# Generate live stream URL (RTSP, valid ~5 min)
python3 scripts/nest.py stream <device_id>
```

## Python API

```python
from nest import NestClient

client = NestClient()

# List devices
devices = client.list_devices()

# Thermostat control
client.set_heat_temperature(device_id, 21.0)  # Celsius
client.set_thermostat_mode(device_id, 'HEAT')
client.set_eco_mode(device_id, 'MANUAL_ECO')

# Camera stream
result = client.generate_stream(device_id)
rtsp_url = result['results']['streamUrls']['rtspUrl']
```

## Configuration

The script checks for credentials in this order:

1. **1Password**: Set `NEST_OP_VAULT` and `NEST_OP_ITEM` (or use defaults: vault "Alfred", item "Nest Device Access API")
2. **Environment variables**: `NEST_PROJECT_ID`, `NEST_CLIENT_ID`, `NEST_CLIENT_SECRET`, `NEST_REFRESH_TOKEN`

## Temperature Reference

| Setting | Celsius | Fahrenheit |
|---------|---------|------------|
| Eco (away) | 15-17°C | 59-63°F |
| Comfortable | 19-21°C | 66-70°F |
| Warm | 22-23°C | 72-73°F |
| Night | 17-18°C | 63-65°F |

---

## Real-Time Events (Doorbell, Motion, etc.)

For instant alerts when someone rings the doorbell or motion is detected, you need to set up Google Cloud Pub/Sub with a webhook.

### Prerequisites

- Google Cloud CLI (`gcloud`) installed and authenticated
- Cloudflare account (free tier works) for the tunnel
- Clawdbot hooks enabled in config

### 1. Enable Clawdbot Hooks

Add to your `clawdbot.json`:

```json
{
  "hooks": {
    "enabled": true,
    "token": "your-secret-token-here"
  }
}
```

Generate a token: `openssl rand -hex 24`

### 2. Create Pub/Sub Topic

```bash
gcloud config set project YOUR_GCP_PROJECT_ID

# Create topic
gcloud pubsub topics create nest-events

# Grant SDM permission to publish
gcloud pubsub topics add-iam-policy-binding nest-events \
  --member="serviceAccount:sdm-prod@sdm-prod.iam.gserviceaccount.com" \
  --role="roles/pubsub.publisher"
```

### 3. Link Topic to Device Access

Go to [console.nest.google.com/device-access](https://console.nest.google.com/device-access) → Your Project → Edit → Set Pub/Sub topic to:

```
projects/YOUR_GCP_PROJECT_ID/topics/nest-events
```

### 4. Set Up Cloudflare Tunnel

```bash
# Install cloudflared
curl -L -o ~/.local/bin/cloudflared https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64
chmod +x ~/.local/bin/cloudflared

# Authenticate (opens browser)
~/.local/bin/cloudflared tunnel login

# Create named tunnel
~/.local/bin/cloudflared tunnel create nest-webhook

# Note the Tunnel ID (UUID) from output
```

Create `~/.cloudflared/config.yml`:

```yaml
tunnel: nest-webhook
credentials-file: /home/YOUR_USER/.cloudflared/TUNNEL_ID.json

ingress:
  - hostname: nest.yourdomain.com
    service: http://localhost:8420
  - service: http_status:404
```

Create DNS route:

```bash
~/.local/bin/cloudflared tunnel route dns nest-webhook nest.yourdomain.com
```

### 5. Create Systemd Services

**Webhook server** (`/etc/systemd/system/nest-webhook.service`):

```ini
[Unit]
Description=Nest Pub/Sub Webhook Server
After=network.target

[Service]
Type=simple
User=YOUR_USER
Environment=CLAWDBOT_GATEWAY_URL=http://localhost:18789
Environment=CLAWDBOT_HOOKS_TOKEN=your-hooks-token-here
ExecStart=/usr/bin/python3 /path/to/skills/nest-devices/scripts/nest-webhook.py
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

**Cloudflare tunnel** (`/etc/systemd/system/cloudflared-nest.service`):

```ini
[Unit]
Description=Cloudflare Tunnel for Nest Webhook
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
User=YOUR_USER
ExecStart=/home/YOUR_USER/.local/bin/cloudflared tunnel run nest-webhook
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
```

Enable and start:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now nest-webhook cloudflared-nest
```

### 6. Create Pub/Sub Push Subscription

```bash
gcloud pubsub subscriptions create nest-events-sub \
  --topic=nest-events \
  --push-endpoint="https://nest.yourdomain.com/nest/events" \
  --ack-deadline=30
```

### 7. Test

```bash
# Test webhook endpoint
curl https://nest.yourdomain.com/health

# Simulate doorbell event
curl -X POST http://localhost:8420/nest/events \
  -H "Content-Type: application/json" \
  -d '{"message":{"data":"eyJyZXNvdXJjZVVwZGF0ZSI6eyJuYW1lIjoiZW50ZXJwcmlzZXMvdGVzdC9kZXZpY2VzL0RPT1JCRUxMLTAxIiwiZXZlbnRzIjp7InNkbS5kZXZpY2VzLmV2ZW50cy5Eb29yYmVsbENoaW1lLkNoaW1lIjp7ImV2ZW50SWQiOiJ0ZXN0In19fX0="}}'
```

### Supported Events

| Event | Alert |
|-------|-------|
| `DoorbellChime.Chime` | 🔔 Doorbell rang! |
| `CameraMotion.Motion` | 📹 Motion detected |
| `CameraPerson.Person` | 🚶 Person detected |
| `CameraSound.Sound` | 🔊 Sound detected |
| `CameraClipPreview.ClipPreview` | 🎬 Clip ready |

---

## Limitations

- Camera streams expire after ~5 minutes
- Real-time events require Pub/Sub setup (see above)
- Quick tunnels (without Cloudflare account) have no uptime guarantee
- Some older Nest devices may not support all features
