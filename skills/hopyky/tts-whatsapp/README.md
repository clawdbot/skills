# 🎙️ TTS WhatsApp - Text-to-Speech Voice Messages

Send voice messages on WhatsApp with high-quality text-to-speech in 40+ languages.

## ✨ Features

- 🎙️ **High-quality TTS** powered by Piper (40+ languages)
- 🎵 **Automatic conversion** to OGG/Opus (WhatsApp format)
- 📤 **Automatic sending** via Clawdbot
- 👥 **Group support** - Send to individuals or WhatsApp groups
- 🌍 **Multi-language** - French, English, Spanish, German, and 40+ more
- 🧹 **Smart cleanup** - Auto-delete files after successful send
- ⚡ **Fast** - ~2-3s from command to delivery

## 📦 Prerequisites

1. **Piper TTS** installed:
   ```bash
   pip3 install --user piper-tts
   ```

2. **FFmpeg** installed:
   ```bash
   # macOS
   brew install ffmpeg

   # Linux
   apt install ffmpeg  # or yum, pacman, etc.
   ```

3. **Piper voice models** downloaded:
   - Download from [Hugging Face](https://huggingface.co/rhasspy/piper-voices)
   - Place in `~/.clawdbot/skills/piper-tts/models/`
   - Default: `fr_FR-siwis-medium.onnx`

## 🚀 Quick Start

### Basic usage (with environment variables)

```bash
tts-whatsapp "Hello, this is a test message"
```

### Specify recipient

```bash
tts-whatsapp "Hello" --target "+15555550123"
```

### Send to a WhatsApp group

```bash
tts-whatsapp "Hello everyone" --target "120363257357161211@g.us"
```

### Change language

```bash
# English
tts-whatsapp "Hello world" --lang en_US --voice lessac

# Spanish
tts-whatsapp "Hola mundo" --lang es_ES --voice carlfm

# German
tts-whatsapp "Guten Tag" --lang de_DE --voice thorsten
```

### Adjust voice quality

```bash
tts-whatsapp "High quality audio" --quality high
```

### Generate without sending

```bash
tts-whatsapp "Test" --no-send
```

## 🔧 Configuration

### Environment Variables

Set these in `~/.clawdbot/clawdbot.json` under the skill configuration:

```json
{
  "skills": {
    "entries": {
      "tts_whatsapp": {
        "enabled": true,
        "env": {
          "PIPER_BIN_PATH": "/path/to/piper",
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

### Available Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `PIPER_BIN_PATH` | Path to piper executable | `~/Library/Python/3.9/bin/piper` |
| `WHATSAPP_DEFAULT_TARGET` | Default recipient phone number or group ID | None (required) |
| `PIPER_DEFAULT_LANG` | Default language code | `fr_FR` |
| `PIPER_DEFAULT_VOICE` | Default voice name | `siwis` |
| `PIPER_DEFAULT_QUALITY` | Default quality level | `medium` |

## 🌍 Supported Languages

Piper supports 40+ languages. Here are some examples:

| Language | Code | Example Voices |
|----------|------|----------------|
| 🇫🇷 French | `fr_FR` | `siwis`, `upmc`, `tom` |
| 🇬🇧 English (GB) | `en_GB` | `alan`, `alba`, `northern_english_male` |
| 🇺🇸 English (US) | `en_US` | `lessac`, `libritts`, `amy`, `joe` |
| 🇪🇸 Spanish | `es_ES` | `carlfm`, `davefx` |
| 🇲🇽 Spanish (MX) | `es_MX` | `claude` |
| 🇩🇪 German | `de_DE` | `thorsten`, `eva_k`, `karlsson` |
| 🇮🇹 Italian | `it_IT` | `riccardo` |
| 🇵🇹 Portuguese (BR) | `pt_BR` | `faber` |
| 🇵🇹 Portuguese (PT) | `pt_PT` | `tugão` |
| 🇳🇱 Dutch | `nl_NL` | `mls`, `rdh` |
| 🇷🇺 Russian | `ru_RU` | `dmitri`, `irina` |
| 🇨🇳 Chinese | `zh_CN` | `huayan` |

**Full list:** [Piper Voice Samples](https://rhasspy.github.io/piper-samples/)

## 🎛️ All Options

```bash
tts-whatsapp "text to speak" [OPTIONS]

Options:
  --target NUMBER       WhatsApp number or group ID
                        Examples: +15555550123, 120363257357161211@g.us

  --message TEXT        Text message accompanying the audio

  --lang LANGUAGE       Language code (default: fr_FR)
                        Examples: en_US, es_ES, de_DE, it_IT

  --voice VOICE         Specific voice name (default: auto per language)
                        Examples: lessac, siwis, thorsten

  --quality QUALITY     Audio quality: x_low, low, medium, high
                        Default: medium

  --speed SPEED         Playback speed (default: 1.0)
                        Examples: 0.8 (slower), 1.2 (faster)

  --no-send            Generate audio file without sending
```

## 📊 How It Works

1. **Text → Speech** - Piper generates high-quality audio (~1s)
2. **Convert** - FFmpeg converts to OGG/Opus format (~0.2s)
3. **Send** - Clawdbot sends to WhatsApp (~1s)
4. **Cleanup** - File deleted after successful send

**Total time: ~2.3s** for a 10-second message

## 🗑️ File Management

- **Auto-delete after send** - Files removed after successful WhatsApp delivery
- **Auto-cleanup old files** - Files older than 24h are deleted on next run
- **Keep on error** - Files preserved if sending fails

## 💡 Examples

### Personal message

```bash
tts-whatsapp "Don't forget the meeting at 3pm" --target "+15555550123"
```

### Group announcement

```bash
tts-whatsapp "Meeting in 5 minutes!" --target "120363257357161211@g.us"
```

### With text caption

```bash
tts-whatsapp "Important update" --message "📢 Please listen"
```

### Different language and voice

```bash
tts-whatsapp "Guten Morgen" --lang de_DE --voice thorsten --target "+491234567890"
```

### Slow speech for learning

```bash
tts-whatsapp "Practice your pronunciation" --speed 0.7 --lang en_US
```

### High quality for music/podcast

```bash
tts-whatsapp "Welcome to my podcast" --quality high --lang en_US --voice lessac
```

## 🔍 Troubleshooting

### Model not found error

```
ERROR: Modèle introuvable: ~/.clawdbot/skills/piper-tts/models/en_US-lessac-medium.onnx
```

**Solution:** Download the model from [Hugging Face](https://huggingface.co/rhasspy/piper-voices/tree/main/en/en_US/lessac/medium)

### No default target error

```
⚠️  Erreur: Aucun destinataire défini
```

**Solution:** Either set `WHATSAPP_DEFAULT_TARGET` in your config or use `--target`

### Clawdbot not found

**Solution:** Make sure Clawdbot is installed and in your PATH

## 📄 License

MIT License - Feel free to use and modify

## 🙏 Credits

- **Piper TTS** by [Rhasspy](https://github.com/rhasspy/piper)
- **Clawdbot** by [clawdbot team](https://github.com/clawdbot/clawdbot)
- **FFmpeg** by the FFmpeg team

## 🔗 Links

- [Piper Voice Samples](https://rhasspy.github.io/piper-samples/)
- [Download Voice Models](https://huggingface.co/rhasspy/piper-voices)
- [Clawdbot Documentation](https://docs.clawd.bot)
- [ClawdHub](https://clawdhub.com)
