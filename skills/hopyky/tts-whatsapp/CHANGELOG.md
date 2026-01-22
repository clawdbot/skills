# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-22

### Added
- 🎙️ High-quality text-to-speech using Piper TTS
- 🌍 Support for 40+ languages (French, English, Spanish, German, and more)
- 📤 Automatic WhatsApp message sending via Clawdbot
- 👥 Support for WhatsApp groups (use group ID as target)
- 🎛️ Multiple quality levels (x_low, low, medium, high)
- 🎵 Automatic conversion to OGG/Opus format for WhatsApp
- 🧹 Smart file cleanup:
  - Auto-delete files after successful send
  - Auto-cleanup files older than 24 hours
  - Keep files on send error for manual retry
- ⚙️ Flexible configuration via environment variables
- 🚫 `--no-send` option to generate audio without sending
- 🎚️ `--speed` option to adjust playback speed
- 💬 `--message` option to add text caption with audio
- 📊 Clear progress logging and error messages
- 🔍 Model existence validation with helpful error messages

### Features
- **Multi-language support**: Switch between 40+ languages with `--lang`
- **Voice selection**: Choose specific voices with `--voice`
- **Quality control**: Adjust quality/size trade-off with `--quality`
- **Group messaging**: Send to WhatsApp groups using group IDs
- **Environment-based defaults**: Set preferences via environment variables
- **Fast generation**: ~2-3s from command to WhatsApp delivery

### Technical Details
- Node.js script with minimal dependencies
- Integration with Piper TTS for speech synthesis
- FFmpeg for audio format conversion
- Clawdbot CLI for WhatsApp delivery
- Automatic cleanup of temporary files
- Comprehensive error handling

[1.0.0]: https://github.com/clawdbot/clawdhub/releases/tag/tts-whatsapp-v1.0.0
