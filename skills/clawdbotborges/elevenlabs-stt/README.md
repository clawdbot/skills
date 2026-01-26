# 🎙️ ElevenLabs Speech-to-Text Skill

A [Clawdbot](https://github.com/clawdbot/clawdbot) skill for transcribing audio files using ElevenLabs' Scribe v2 model.

## Features

- 🌍 **90+ languages** supported with automatic detection
- 👥 **Speaker diarization** — identify different speakers
- 🎵 **Audio event tagging** — detect laughter, music, applause, etc.
- 📝 **Word-level timestamps** — precise timing in JSON output
- 🎧 **All major formats** — mp3, m4a, wav, ogg, webm, mp4, and more

## Installation

### For Clawdbot

Add to your `clawdbot.json`:

```json5
{
  skills: {
    entries: {
      "elevenlabs-stt": {
        source: "github:clawdbotborges/elevenlabs-stt",
        apiKey: "sk_your_api_key_here"
      }
    }
  }
}
```

### Standalone

```bash
git clone https://github.com/clawdbotborges/elevenlabs-stt.git
cd elevenlabs-stt
export ELEVENLABS_API_KEY="sk_your_api_key_here"
```

## Usage

```bash
# Basic transcription
./scripts/transcribe.sh audio.mp3

# With speaker diarization
./scripts/transcribe.sh meeting.mp3 --diarize

# Specify language for better accuracy
./scripts/transcribe.sh voice_note.ogg --lang en

# Full JSON with timestamps
./scripts/transcribe.sh podcast.mp3 --json

# Tag audio events (laughter, music, etc.)
./scripts/transcribe.sh recording.wav --events
```

## Options

| Flag | Description |
|------|-------------|
| `--diarize` | Enable speaker diarization |
| `--lang CODE` | ISO language code (e.g., `en`, `pt`, `es`, `fr`) |
| `--json` | Output full JSON response with word timestamps |
| `--events` | Tag audio events like laughter, music, applause |
| `-h, --help` | Show help message |

## Examples

### Transcribe a voice message

```bash
./scripts/transcribe.sh ~/Downloads/voice_note.ogg
# Output: "Hey, just wanted to check in about the meeting tomorrow."
```

### Meeting with multiple speakers

```bash
./scripts/transcribe.sh meeting.mp3 --diarize --lang en --json
```

```json
{
  "text": "Welcome everyone. Let's start with updates.",
  "words": [
    {"text": "Welcome", "start": 0.0, "end": 0.5, "speaker": "speaker_0"},
    {"text": "everyone", "start": 0.5, "end": 1.0, "speaker": "speaker_0"}
  ]
}
```

### Process with jq

```bash
# Get just the text
./scripts/transcribe.sh audio.mp3 --json | jq -r '.text'

# Get word count
./scripts/transcribe.sh audio.mp3 --json | jq '.words | length'
```

## Requirements

- `curl` — for API requests
- `jq` — for JSON parsing (optional, but recommended)
- ElevenLabs API key with Speech-to-Text access

## API Key

Get your API key from [ElevenLabs](https://elevenlabs.io):

1. Sign up or log in
2. Go to Profile → API Keys
3. Create a new key or copy existing one

## License

MIT

## Links

- [ElevenLabs Speech-to-Text](https://elevenlabs.io/speech-to-text)
- [API Documentation](https://elevenlabs.io/docs/api-reference/speech-to-text)
- [Clawdbot](https://github.com/clawdbot/clawdbot)
