---
name: discord-voice
description: Real-time voice conversations in Discord voice channels with Claude AI
metadata:
  clawdbot:
    config:
      requiredEnv:
        - DISCORD_TOKEN
        - OPENAI_API_KEY
      optionalEnv:
        - ELEVENLABS_API_KEY
        - DEEPGRAM_API_KEY
      systemDependencies:
        - ffmpeg
        - build-essential
      example: |
        {
          "plugins": {
            "entries": {
              "discord-voice": {
                "enabled": true,
                "config": {
                  "sttProvider": "whisper",
                  "ttsProvider": "openai",
                  "ttsVoice": "nova",
                  "vadSensitivity": "medium",
                  "streamingSTT": true,
                  "bargeIn": true,
                  "allowedUsers": []
                }
              }
            }
          }
        }
---

# Discord Voice Plugin for Clawdbot

Real-time voice conversations in Discord voice channels. Join a voice channel, speak, and have your words transcribed, processed by Claude, and spoken back.

## Features

- **Join/Leave Voice Channels**: Via slash commands, CLI, or agent tool
- **Voice Activity Detection (VAD)**: Automatically detects when users are speaking
- **Speech-to-Text**: Whisper API (OpenAI) or Deepgram
- **Streaming STT**: Real-time transcription with Deepgram WebSocket (~1s latency reduction)
- **Agent Integration**: Transcribed speech is routed through the Clawdbot agent
- **Text-to-Speech**: OpenAI TTS or ElevenLabs
- **Audio Playback**: Responses are spoken back in the voice channel
- **Barge-in Support**: Stops speaking immediately when user starts talking
- **Auto-reconnect**: Automatic heartbeat monitoring and reconnection on disconnect

## Requirements

- Discord bot with voice permissions (Connect, Speak, Use Voice Activity)
- API keys for STT and TTS providers
- System dependencies for voice:
  - `ffmpeg` (audio processing)
  - Native build tools for `@discordjs/opus` and `sodium-native`

## Installation

### 1. Install System Dependencies

```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg build-essential python3

# Fedora/RHEL
sudo dnf install ffmpeg gcc-c++ make python3

# macOS
brew install ffmpeg
```

### 2. Install via ClawdHub

```bash
clawdhub install discord-voice
```

Or manually:

```bash
cd ~/.clawdbot/extensions
git clone <repository-url> discord-voice
cd discord-voice
npm install
```

### 3. Configure in clawdbot.json

```json5
{
  "plugins": {
    "entries": {
      "discord-voice": {
        "enabled": true,
        "config": {
          "sttProvider": "whisper",
          "ttsProvider": "openai",
          "ttsVoice": "nova",
          "vadSensitivity": "medium",
          "allowedUsers": [],  // Empty = allow all users
          "silenceThresholdMs": 1500,
          "maxRecordingMs": 30000,
          "openai": {
            "apiKey": "sk-..."  // Or use OPENAI_API_KEY env var
          }
        }
      }
    }
  }
}
```

### 4. Discord Bot Setup

Ensure your Discord bot has these permissions:
- **Connect** - Join voice channels
- **Speak** - Play audio
- **Use Voice Activity** - Detect when users speak

Add these to your bot's OAuth2 URL or configure in Discord Developer Portal.

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `enabled` | boolean | `true` | Enable/disable the plugin |
| `sttProvider` | string | `"whisper"` | `"whisper"` or `"deepgram"` |
| `streamingSTT` | boolean | `true` | Use streaming STT (Deepgram only, ~1s faster) |
| `ttsProvider` | string | `"openai"` | `"openai"` or `"elevenlabs"` |
| `ttsVoice` | string | `"nova"` | Voice ID for TTS |
| `vadSensitivity` | string | `"medium"` | `"low"`, `"medium"`, or `"high"` |
| `bargeIn` | boolean | `true` | Stop speaking when user talks |
| `allowedUsers` | string[] | `[]` | User IDs allowed (empty = all) |
| `silenceThresholdMs` | number | `1500` | Silence before processing (ms) |
| `maxRecordingMs` | number | `30000` | Max recording length (ms) |
| `heartbeatIntervalMs` | number | `30000` | Connection health check interval |
| `autoJoinChannel` | string | `undefined` | Channel ID to auto-join on startup |

### Provider Configuration

#### OpenAI (Whisper + TTS)
```json5
{
  "openai": {
    "apiKey": "sk-...",
    "whisperModel": "whisper-1",
    "ttsModel": "tts-1"
  }
}
```

#### ElevenLabs (TTS only)
```json5
{
  "elevenlabs": {
    "apiKey": "...",
    "voiceId": "21m00Tcm4TlvDq8ikWAM",  // Rachel
    "modelId": "eleven_multilingual_v2"
  }
}
```

#### Deepgram (STT only)
```json5
{
  "deepgram": {
    "apiKey": "...",
    "model": "nova-2"
  }
}
```

## Usage

### Slash Commands (Discord)

Once registered with Discord, use these commands:
- `/voice join <channel>` - Join a voice channel
- `/voice leave` - Leave the current voice channel
- `/voice status` - Show voice connection status

### CLI Commands

```bash
# Join a voice channel
clawdbot voice join <channelId>

# Leave voice
clawdbot voice leave --guild <guildId>

# Check status
clawdbot voice status
```

### Agent Tool

The agent can use the `discord_voice` tool:
```
Join voice channel 1234567890
```

The tool supports actions:
- `join` - Join a voice channel (requires channelId)
- `leave` - Leave voice channel
- `speak` - Speak text in the voice channel
- `status` - Get current voice status

## How It Works

1. **Join**: Bot joins the specified voice channel
2. **Listen**: VAD detects when users start/stop speaking
3. **Record**: Audio is buffered while user speaks
4. **Transcribe**: On silence, audio is sent to STT provider
5. **Process**: Transcribed text is sent to Clawdbot agent
6. **Synthesize**: Agent response is converted to audio via TTS
7. **Play**: Audio is played back in the voice channel

## Streaming STT (Deepgram)

When using Deepgram as your STT provider, streaming mode is enabled by default. This provides:

- **~1 second faster** end-to-end latency
- **Real-time feedback** with interim transcription results
- **Automatic keep-alive** to prevent connection timeouts
- **Fallback** to batch transcription if streaming fails

To use streaming STT:
```json5
{
  "sttProvider": "deepgram",
  "streamingSTT": true,  // default
  "deepgram": {
    "apiKey": "...",
    "model": "nova-2"
  }
}
```

## Barge-in Support

When enabled (default), the bot will immediately stop speaking if a user starts talking. This creates a more natural conversational flow where you can interrupt the bot.

To disable (let the bot finish speaking):
```json5
{
  "bargeIn": false
}
```

## Auto-reconnect

The plugin includes automatic connection health monitoring:

- **Heartbeat checks** every 30 seconds (configurable)
- **Auto-reconnect** on disconnect with exponential backoff
- **Max 3 attempts** before giving up

If the connection drops, you'll see logs like:
```
[discord-voice] Disconnected from voice channel
[discord-voice] Reconnection attempt 1/3
[discord-voice] Reconnected successfully
```

## VAD Sensitivity

- **low**: Picks up quiet speech, may trigger on background noise
- **medium**: Balanced (recommended)
- **high**: Requires louder, clearer speech

## Troubleshooting

### "Discord client not available"
Ensure the Discord channel is configured and the bot is connected before using voice.

### Opus/Sodium build errors
Install build tools:
```bash
npm install -g node-gyp
npm rebuild @discordjs/opus sodium-native
```

### No audio heard
1. Check bot has Connect + Speak permissions
2. Check bot isn't server muted
3. Verify TTS API key is valid

### Transcription not working
1. Check STT API key is valid
2. Check audio is being recorded (see debug logs)
3. Try adjusting VAD sensitivity

### Enable debug logging
```bash
DEBUG=discord-voice clawdbot gateway start
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `DISCORD_TOKEN` | Discord bot token (required) |
| `OPENAI_API_KEY` | OpenAI API key (Whisper + TTS) |
| `ELEVENLABS_API_KEY` | ElevenLabs API key |
| `DEEPGRAM_API_KEY` | Deepgram API key |

## Limitations

- Only one voice channel per guild at a time
- Maximum recording length: 30 seconds (configurable)
- Requires stable network for real-time audio
- TTS output may have slight delay due to synthesis

## License

MIT
