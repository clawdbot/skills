---
name: gemini-yt-video-transcript
description: "Create a verbatim transcript for a YouTube URL using Google Gemini (speaker labels, paragraph breaks; no time codes). Use when the user asks to transcribe a YouTube video or wants a clean transcript (no timestamps)."
summary: "Generate a verbatim YouTube transcript via Google Gemini (speaker labels, no time codes)."
version: 1.0.2
homepage: https://github.com/odrobnik/gemini-yt-video-transcript-skill
metadata: {"clawdbot":{"emoji":"📝","requires":{"env":["GEMINI_API_KEY"],"bins":["python3"]}}}
---

# Gemini YouTube Video Transcript

Create a **verbatim transcript** for a YouTube URL using **Google Gemini**.

**Output format**
- First line: YouTube video title
- Then transcript lines only in the form:

```
Speaker: text
```

**Requirements**
- No time codes
- No extra headings / lists / commentary

## Usage

```bash
python3 {baseDir}/scripts/youtube_transcript.py "https://www.youtube.com/watch?v=..."
```

Options:
- `--out <path>` Write transcript to a specific file (default: auto-named in the workspace `out/` folder).

## Delivery

When chatting: send the resulting transcript as a document/attachment.
