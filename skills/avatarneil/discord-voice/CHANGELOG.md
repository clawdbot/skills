# Changelog

All notable changes to the Discord Voice Plugin for Clawdbot will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-26

### Added
- Initial release of Discord Voice Plugin
- Voice Activity Detection (VAD) for automatic speech detection
- Speech-to-Text support with Whisper (OpenAI) and Deepgram
- Streaming STT with Deepgram WebSocket for ~1s latency reduction
- Text-to-Speech support with OpenAI TTS and ElevenLabs
- Streaming TTS for real-time audio playback
- Barge-in support to interrupt bot responses
- Auto-reconnect with heartbeat monitoring
- Discord slash commands: `/voice join`, `/voice leave`, `/voice status`
- CLI commands for voice management
- Agent tool `discord_voice` for programmatic control
- Configurable VAD sensitivity (low/medium/high)
- User allowlist support for restricted access
- Automatic audio buffering during STT connection setup
- Processing lock to prevent duplicate/racing responses
- Thinking sound indicator during agent processing

### Fixed
- Buffer audio during streaming STT connection setup
- Move processing lock after audio filters to prevent permanent lock
- Always stop thinking sound even if agent call fails
- Remove lane restriction to allow full tool access

### Security
- API key validation for STT/TTS providers
- User permission checks for allowed users
- Environment variable support for sensitive credentials
