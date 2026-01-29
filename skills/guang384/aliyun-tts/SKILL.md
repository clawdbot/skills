---
name: aliyun-tts
description: Alibaba Cloud Text-to-Speech synthesis service.
metadata: {"clawdbot":{"emoji":"🔊"}}
---

# aliyun-tts

Alibaba Cloud Text-to-Speech synthesis service.

## Configuration

Set the following environment variables:
- `ALIYUN_APP_KEY` - Application Key
- `ALIYUN_ACCESS_KEY_ID` - Access Key ID
- `ALIYUN_ACCESS_KEY_SECRET` - Access Key Secret (sensitive)

### Option 1: CLI configuration (recommended)

```bash
# Configure App Key
clawdbot skills config aliyun-tts ALIYUN_APP_KEY "your-app-key"

# Configure Access Key ID
clawdbot skills config aliyun-tts ALIYUN_ACCESS_KEY_ID "your-access-key-id"

# Configure Access Key Secret (sensitive)
clawdbot skills config aliyun-tts ALIYUN_ACCESS_KEY_SECRET "your-access-key-secret"
```

### Option 2: Manual configuration

Edit `~/.clawdbot/clawdbot.json`:

```json5
{
  skills: {
    entries: {
      "aliyun-tts": {
        env: {
          ALIYUN_APP_KEY: "your-app-key",
          ALIYUN_ACCESS_KEY_ID: "your-access-key-id",
          ALIYUN_ACCESS_KEY_SECRET: "your-access-key-secret"
        }
      }
    }
  }
}
```

## Usage

```bash
# Basic usage
{baseDir}/bin/aliyun-tts "Hello, this is Aliyun TTS"

# Specify output file
{baseDir}/bin/aliyun-tts -o /tmp/voice.mp3 "Hello"

# Specify voice
{baseDir}/bin/aliyun-tts -v siyue "Use siyue voice"

# Specify format and sample rate
{baseDir}/bin/aliyun-tts -f mp3 -r 16000 "Audio parameters"
```

## Options

| Flag | Description | Default |
|------|-------------|---------|
| `-o, --output` | Output file path | tts.mp3 |
| `-v, --voice` | Voice name | siyue |
| `-f, --format` | Audio format | mp3 |
| `-r, --sample-rate` | Sample rate | 16000 |

## Available Voices

Common voices: `siyue`, `xiaoxuan`, `xiaoyun`, etc. See Alibaba Cloud documentation for the full list.

## Chat Voice Replies

When a user requests a voice reply:

```bash
# Generate audio
{baseDir}/bin/aliyun-tts -o /tmp/voice-reply.mp3 "Your reply content"

# Include in your response:
# MEDIA:/tmp/voice-reply.mp3
```
