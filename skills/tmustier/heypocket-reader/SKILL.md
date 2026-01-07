---
name: pocket-transcripts
description: Read transcripts and summaries from Pocket AI (heypocket.com) recording devices. Use when users want to retrieve, search, or analyze their Pocket recordings, transcripts, summaries, or action items. Triggers on requests involving Pocket device data, conversation transcripts, meeting recordings, or audio note retrieval.
---

# Pocket Transcripts

Read transcripts and summaries from Pocket AI devices via reverse-engineered API.

## Quick Reference

| Function | Description |
|----------|-------------|
| `get_recordings(days, limit)` | List recent recordings |
| `get_recording_full(id)` | Get transcript + summary + action items |
| `get_transcript(id)` | Get raw transcript text |
| `get_summarization(id)` | Get markdown summary |
| `search_recordings(query)` | Search by text |

## Setup (One-Time)

### 1. Start Chrome with User Profile

```bash
~/.factory/skills/browser/start.js --profile
# or
~/.claude/skills/browser/start.js --profile
```

### 2. Log into Pocket

Navigate to and log in:
```bash
~/.factory/skills/browser/nav.js https://app.heypocket.com
```

### 3. Extract Token

```bash
python3 scripts/reader.py extract
```

Token is saved to `~/.pocket_token.json` and expires in 1 hour.

## Usage

### List Recordings

```python
from pathlib import Path
import sys
sys.path.insert(0, str(Path.home() / '.claude/skills/pocket-transcripts/scripts'))
from reader import get_recordings, get_recording_full

recordings = get_recordings(days=30, limit=20)
for r in recordings:
    print(f"{r.recorded_at:%Y-%m-%d} | {r.duration_str} | {r.title}")
```

### Get Full Transcript and Summary

```python
full = get_recording_full(recording_id)

print(f"Transcript ({len(full['transcript'])} chars):")
print(full['transcript'][:500])

print(f"\nSummary (markdown):")
print(full['summary'])

print(f"\nAction Items: {len(full['action_items'])}")
for item in full['action_items']:
    print(f"  - {item}")
```

### Search Recordings

```python
results = search_recordings("meeting", days=90)
for r in results:
    print(f"{r.title} - {r.description[:100]}")
```

## API Details

**Base URL**: `https://production.heypocketai.com/api/v1`

**Auth**: Firebase Bearer token from browser IndexedDB

**Key Endpoints**:
- `GET /recordings` - List with pagination, filters
- `GET /recordings/{id}?include=all` - Full data with transcript/summary

**Data Structure**:
- Transcript: `data.transcription.transcription.text`
- Summary: `data.summarizations[id].v2.summary.markdown`
- Action Items: `data.summarizations[id].v2.actionItems.items`

## Token Refresh

Firebase tokens expire in 1 hour. When expired:

1. Ensure Chrome is running with `--profile`
2. Confirm logged into app.heypocket.com
3. Re-run: `python3 scripts/reader.py extract`

## Data Model

### PocketRecording
- `id`, `title`, `description`
- `duration` (seconds), `duration_str` (human readable)
- `recorded_at`, `created_at`
- `has_transcription`, `has_summarization`
- `num_speakers`
- `latitude`, `longitude` (if location enabled)
- `tags` (list of strings)

### PocketSummarization
- `summary` (markdown formatted)
- `action_items` (list)
- `transcript` (raw text)
