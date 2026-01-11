---
name: voicemonkey
description: Control Alexa devices via VoiceMonkey API v2 - make announcements, trigger routines, start flows, and display media.
homepage: https://voicemonkey.io
metadata: {"clawdbot":{"emoji":"🐒","requires":{"env":["VOICEMONKEY_TOKEN"]},"primaryEnv":"VOICEMONKEY_TOKEN"}}
---

# VoiceMonkey

Control Alexa/Echo devices via VoiceMonkey API v2. Make TTS announcements, trigger Alexa routines, start flows, and display images/videos on Echo Show devices.

## Setup

1. Get your secret token from [Voice Monkey Console](https://console.voicemonkey.io) → Settings → API Credentials
2. Set environment variable:
   ```bash
   export VOICEMONKEY_TOKEN="your-secret-token"
   ```
   Or add to `~/.clawdbot/clawdbot.json`:
   ```json
   {
     "skills": {
       "entries": {
         "voicemonkey": {
           "env": { "VOICEMONKEY_TOKEN": "your-secret-token" }
         }
       }
     }
   }
   ```
3. Find your Device IDs in the Voice Monkey Console → Settings → Devices

## API Base URL

```
https://api-v2.voicemonkey.io
```

## Announcement API

Make TTS announcements, play audio/video, or display images on Alexa devices.

**Endpoint:** `https://api-v2.voicemonkey.io/announcement`

### Basic TTS Announcement

```bash
curl -X GET "https://api-v2.voicemonkey.io/announcement?token=$VOICEMONKEY_TOKEN&device=YOUR_DEVICE_ID&text=Hello%20from%20Echo"
```

### With Authorization Header (recommended)

```bash
curl -X POST "https://api-v2.voicemonkey.io/announcement" \
  -H "Authorization: $VOICEMONKEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "YOUR_DEVICE_ID",
    "text": "Hello from Echo the Fox!"
  }'
```

### With Voice and Chime

```bash
curl -X POST "https://api-v2.voicemonkey.io/announcement" \
  -H "Authorization: $VOICEMONKEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "YOUR_DEVICE_ID",
    "text": "Dinner is ready!",
    "voice": "Brian",
    "chime": "soundbank://soundlibrary/alarms/beeps_and_bloops/bell_02"
  }'
```

### Display Image on Echo Show

```bash
curl -X POST "https://api-v2.voicemonkey.io/announcement" \
  -H "Authorization: $VOICEMONKEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "YOUR_DEVICE_ID",
    "text": "Check out this image",
    "image": "https://example.com/image.jpg",
    "media_width": "100",
    "media_height": "100",
    "media_scaling": "best-fit"
  }'
```

### Play Audio File

```bash
curl -X POST "https://api-v2.voicemonkey.io/announcement" \
  -H "Authorization: $VOICEMONKEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "YOUR_DEVICE_ID",
    "audio": "https://example.com/sound.mp3"
  }'
```

### Play Video on Echo Show

```bash
curl -X POST "https://api-v2.voicemonkey.io/announcement" \
  -H "Authorization: $VOICEMONKEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "YOUR_DEVICE_ID",
    "video": "https://example.com/video.mp4",
    "video_repeat": 1
  }'
```

### Open Website on Echo Show

```bash
curl -X POST "https://api-v2.voicemonkey.io/announcement" \
  -H "Authorization: $VOICEMONKEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "YOUR_DEVICE_ID",
    "website": "https://example.com",
    "no_bg": "true"
  }'
```

### Announcement Parameters

| Parameter | Required | Description |
|-----------|----------|-------------|
| `token` | Yes* | Secret token (*or use Authorization header) |
| `device` | Yes | Device ID from Voice Monkey console |
| `text` | No | TTS text (supports SSML) |
| `voice` | No | Voice for TTS (see API Playground for options) |
| `language` | No | Language code for better pronunciation |
| `chime` | No | Sound URL or Alexa sound library reference |
| `audio` | No | HTTPS URL of audio file to play |
| `background_audio` | No | Audio to play behind TTS |
| `image` | No | HTTPS URL of image for Echo Show |
| `video` | No | HTTPS URL of MP4 video for Echo Show |
| `video_repeat` | No | Number of times to loop video |
| `website` | No | URL to open on Echo Show |
| `no_bg` | No | Set "true" to hide Voice Monkey branding |
| `media_width` | No | Image width |
| `media_height` | No | Image height |
| `media_scaling` | No | Image scaling mode |
| `media_align` | No | Image alignment |
| `media_radius` | No | Corner radius for image clipping |
| `var-[name]` | No | Update Voice Monkey variables |

## Routine Trigger API

Trigger Voice Monkey devices to start Alexa Routines.

**Endpoint:** `https://api-v2.voicemonkey.io/trigger`

```bash
curl -X POST "https://api-v2.voicemonkey.io/trigger" \
  -H "Authorization: $VOICEMONKEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "YOUR_TRIGGER_DEVICE_ID"
  }'
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `token` | Yes* | Secret token (*or use Authorization header) |
| `device` | Yes | Trigger Device ID from Voice Monkey console |

## Flows Trigger API

Start Voice Monkey Flows.

**Endpoint:** `https://api-v2.voicemonkey.io/flows`

```bash
curl -X POST "https://api-v2.voicemonkey.io/flows" \
  -H "Authorization: $VOICEMONKEY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "device": "YOUR_DEVICE_ID",
    "flow": 12345
  }'
```

| Parameter | Required | Description |
|-----------|----------|-------------|
| `token` | Yes* | Secret token (*or use Authorization header) |
| `device` | Yes | Device ID |
| `flow` | Yes | Numeric Flow ID from Voice Monkey console |

## Media Requirements

### Images
- Most common formats supported (JPG, PNG, etc.)
- **No animated GIFs**
- Optimize file size for faster loading
- Must be hosted at HTTPS URL with valid SSL
- CORS must allow wildcard: `Access-Control-Allow-Origin: *`

### Videos
- **MP4 format only** (MPEG-4 Part-14)
- Audio codecs: AAC, MP3
- Max resolution: 1080p @30fps or @60fps
- Must be hosted at HTTPS URL with valid SSL

### Audio
- Formats: AAC, MP3, OGG, Opus, WAV
- Bit rate: ≤ 1411.20 kbps
- Sample rate: ≤ 48kHz
- File size: ≤ 10MB
- Total response length: ≤ 240 seconds

## SSML Examples

Use SSML in the `text` parameter for richer announcements:

```xml
<speak>
  <amazon:emotion name="excited" intensity="high">
    This is exciting news!
  </amazon:emotion>
</speak>
```

```xml
<speak>
  The time is <say-as interpret-as="time">3:30pm</say-as>
</speak>
```

## Notes

- Keep your token secure; rotate via Console → Settings → API Credentials if compromised
- Use the [API Playground](https://console.voicemonkey.io) to test and explore options
- Premium members can upload media directly in the Voice Monkey console
- Always confirm before sending announcements to avoid unexpected noise
