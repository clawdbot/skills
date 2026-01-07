# Pocket Transcripts Skill

A Claude Code skill for reading transcripts and summaries from [Pocket AI](https://heypocket.com) recording devices.

## What is Pocket?

Pocket is an AI-powered wearable device that records conversations and generates transcripts, summaries, and action items. This skill provides programmatic access to your Pocket data via their unofficial API.

## Features

- **List recordings** with metadata (title, duration, date, speakers)
- **Get full transcripts** of recorded conversations (50k+ characters)
- **Get AI summaries** in markdown format
- **Extract action items** from recordings
- **Search recordings** by text

## Installation

### For Claude Code Users

Download the `.skill` file from [Releases](../../releases) and add it to your Claude Code skills.

### Manual Installation

```bash
# Clone to your skills directory
git clone https://github.com/YOUR_USERNAME/pocket-transcripts-skill.git ~/.claude/skills/pocket-transcripts
```

## Setup

### Prerequisites

1. A Pocket account with recordings
2. The [browser skill](https://github.com/anthropics/skills/tree/main/skills/browser) installed
3. Chrome browser

### Authentication

Pocket uses Firebase authentication. To extract your token:

1. Start Chrome with your profile:
   ```bash
   ~/.claude/skills/browser/start.js --profile
   ```

2. Navigate to Pocket and log in:
   ```bash
   ~/.claude/skills/browser/nav.js https://app.heypocket.com
   ```

3. Extract the token:
   ```bash
   python3 ~/.claude/skills/pocket-transcripts/scripts/reader.py extract
   ```

The token is saved to `~/.pocket_token.json` and expires in 1 hour.

## Usage

### CLI

```bash
# List recent recordings
python3 scripts/reader.py

# List recordings from last 7 days
python3 scripts/reader.py 7
```

### Python

```python
from reader import get_recordings, get_recording_full, search_recordings

# List recordings
recordings = get_recordings(days=30, limit=20)
for r in recordings:
    print(f"{r.recorded_at:%Y-%m-%d} | {r.duration_str} | {r.title}")

# Get full transcript and summary
full = get_recording_full(recording_id)
print(full['transcript'])  # Raw text
print(full['summary'])     # Markdown

# Search
results = search_recordings("meeting")
```

## API Reference

| Function | Description |
|----------|-------------|
| `get_recordings(days, limit)` | List recent recordings |
| `get_recording_full(id)` | Get transcript + summary + action items + speakers |
| `get_transcript(id)` | Get raw transcript text |
| `get_summarization(id)` | Get markdown summary |
| `search_recordings(query, days, limit)` | Search recordings by text |

## Technical Details

- **API Base**: `https://production.heypocketai.com/api/v1`
- **Auth**: Firebase Bearer token from browser IndexedDB
- **Token Expiry**: 1 hour (Firebase default)

This skill was created by reverse-engineering the Pocket web app at `app.heypocket.com`.

## License

MIT License - See [LICENSE](LICENSE) for details.

## Disclaimer

This is an unofficial integration. Use at your own risk. Not affiliated with or endorsed by Pocket/Open Vision Engineering Inc.
