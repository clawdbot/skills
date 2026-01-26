---
name: elevenlabs-stt
description: Transcribe audio files using ElevenLabs Speech-to-Text (Scribe v2).
homepage: https://elevenlabs.io/speech-to-text
metadata: {"clawdbot":{"emoji":"🎙️","requires":{"bins":["curl"],"env":["ELEVENLABS_API_KEY"]},"primaryEnv":"ELEVENLABS_API_KEY"}}
---

# ElevenLabs Speech-to-Text

Transcribe audio files using ElevenLabs' Scribe v2 model. Supports 90+ languages with speaker diarization.

## Quick Start

```bash
# Basic transcription
{baseDir}/scripts/transcribe.sh /path/to/audio.mp3

# With speaker diarization
{baseDir}/scripts/transcribe.sh /path/to/audio.mp3 --diarize

# Specify language (improves accuracy)
{baseDir}/scripts/transcribe.sh /path/to/audio.mp3 --lang en

# Full JSON output with timestamps
{baseDir}/scripts/transcribe.sh /path/to/audio.mp3 --json
```

## Options

| Flag | Description |
|------|-------------|
| `--diarize` | Identify different speakers |
| `--lang CODE` | ISO language code (e.g., en, pt, es) |
| `--json` | Output full JSON with word timestamps |
| `--events` | Tag audio events (laughter, music, etc.) |

## Supported Formats

All major audio/video formats: mp3, m4a, wav, ogg, webm, mp4, etc.

## API Key

Set `ELEVENLABS_API_KEY` environment variable, or configure in clawdbot.json:

```json5
{
  skills: {
    entries: {
      "elevenlabs-stt": {
        apiKey: "sk_..."
      }
    }
  }
}
```

## Examples

```bash
# Transcribe a WhatsApp voice note
{baseDir}/scripts/transcribe.sh ~/Downloads/voice_note.ogg

# Meeting recording with multiple speakers
{baseDir}/scripts/transcribe.sh meeting.mp3 --diarize --lang en

# Get JSON for processing
{baseDir}/scripts/transcribe.sh podcast.mp3 --json > transcript.json
```
