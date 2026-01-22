---
name: tts-whatsapp
version: 1.0.0
description: Send high-quality text-to-speech voice messages on WhatsApp in 40+ languages with automatic delivery
user-invocable: true
disable-model-invocation: false
tags:
  - whatsapp
  - tts
  - voice
  - messaging
  - multilingual
  - audio
author: Community
repository: https://github.com/clawdbot/clawdhub
---

# 🎙️ TTS WhatsApp - Voice Messages in 40+ Languages

Send high-quality text-to-speech voice messages on WhatsApp with automatic delivery. Supports 40+ languages, personal messages, and group broadcasts.

## ✨ Features

- 🎙️ **High-quality TTS** powered by Piper (40+ languages)
- 🎵 **Automatic conversion** to OGG/Opus (WhatsApp format)
- 📤 **Automatic sending** via Clawdbot
- 👥 **Group support** - Send to individuals or WhatsApp groups
- 🌍 **Multi-language** - French, English, Spanish, German, and 40+ more
- 🧹 **Smart cleanup** - Auto-delete files after successful send
- ⚡ **Fast** - ~2-3s from command to delivery

## 📦 Prerequisites

1. **Piper TTS**: `pip3 install --user piper-tts`
2. **FFmpeg**: `brew install ffmpeg` (macOS) or `apt install ffmpeg` (Linux)
3. **Voice models**: Download from [Hugging Face](https://huggingface.co/rhasspy/piper-voices)
   - Place in `~/.clawdbot/skills/piper-tts/models/`
   - Example: `fr_FR-siwis-medium.onnx`

## 🚀 Quick Start

### Basic usage
```bash
tts-whatsapp "Hello, this is a test" --target "+15555550123"
```

### Send to WhatsApp group
```bash
tts-whatsapp "Hello everyone" --target "120363257357161211@g.us"
```

### Change language
```bash
tts-whatsapp "Hola mundo" --lang es_ES --voice carlfm --target "+34..."
```

### Different quality levels
```bash
tts-whatsapp "High quality" --quality high --target "+1..."
```

## 🌍 Supported Languages

- 🇫🇷 French (`fr_FR`): siwis, upmc, tom
- 🇬🇧 English GB (`en_GB`): alan, alba
- 🇺🇸 English US (`en_US`): lessac, amy, joe
- 🇪🇸 Spanish (`es_ES`, `es_MX`): carlfm, davefx
- 🇩🇪 German (`de_DE`): thorsten, eva_k
- 🇮🇹 Italian (`it_IT`): riccardo
- 🇵🇹 Portuguese (`pt_BR`, `pt_PT`): faber
- 🇳🇱 Dutch (`nl_NL`): mls, rdh
- 🇷🇺 Russian (`ru_RU`): dmitri, irina
- And 30+ more!

[Full voice list →](https://rhasspy.github.io/piper-samples/)

## 🔧 Configuration

Configure in `~/.clawdbot/clawdbot.json`:

```json
{
  "skills": {
    "entries": {
      "tts_whatsapp": {
        "enabled": true,
        "env": {
          "WHATSAPP_DEFAULT_TARGET": "+15555550123",
          "PIPER_DEFAULT_LANG": "en_US",
          "PIPER_DEFAULT_VOICE": "lessac",
          "PIPER_DEFAULT_QUALITY": "medium"
        }
      }
    }
  }
}
```

## 🎛️ All Options

```
--target NUMBER       WhatsApp number or group ID
--message TEXT        Text message with audio
--lang LANGUAGE       Language (default: fr_FR)
--voice VOICE         Voice name (default: auto)
--quality QUALITY     x_low, low, medium, high
--speed SPEED         Playback speed (default: 1.0)
--no-send            Don't send automatically
```

## 📊 Performance

~2.3s total for a 10-second message:
- TTS generation: ~1s
- Format conversion: ~0.2s
- WhatsApp delivery: ~1s

## 📚 Full Documentation

See [README.md](README.md) for complete documentation, examples, and troubleshooting.
