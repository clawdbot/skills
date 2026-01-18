---
name: assemblyai-transcribe
description: Transcribe audio/video with AssemblyAI (local upload or URL), plus subtitles + paragraph/sentence exports.
homepage: https://www.assemblyai.com/docs
user-invocable: true
metadata: {"clawdbot":{"skillKey":"assemblyai","emoji":"🎙️","requires":{"bins":["node"],"env":["ASSEMBLYAI_API_KEY"]},"primaryEnv":"ASSEMBLYAI_API_KEY"}}
---

# AssemblyAI transcription + exports

Use this skill when you need to transcribe audio/video or export readable formats (subtitles, paragraphs, sentences) using AssemblyAI.

The helper script in this skill implements the basic REST flow:

1. (Local files) Upload via `POST /v2/upload`.
2. Create a transcript job via `POST /v2/transcript`.
3. Poll `GET /v2/transcript/:id` until the transcript `status` is `completed` (or `error`).

## Setup

This skill requires:

- `node` on PATH (Node.js 18+ recommended; script uses built-in fetch)
- `ASSEMBLYAI_API_KEY` in the environment

Recommended Clawdbot config (`~/.clawdbot/clawdbot.json`):

```js
{
  skills: {
    entries: {
      // This skill declares metadata.clawdbot.skillKey = "assemblyai"
      assemblyai: {
        enabled: true,
        // Because this skill declares primaryEnv = ASSEMBLYAI_API_KEY,
        // you can use apiKey as a convenience:
        apiKey: "YOUR_ASSEMBLYAI_KEY",
        env: {
          ASSEMBLYAI_API_KEY: "YOUR_ASSEMBLYAI_KEY",

          // Optional: use EU async endpoint
          // ASSEMBLYAI_BASE_URL: "https://api.eu.assemblyai.com"
        }
      }
    }
  }
}
```

## Usage

Run these commands via the Exec tool.

### Transcribe (local file or public URL)

Print transcript text to stdout:

```bash
node {baseDir}/assemblyai.mjs transcribe "./path/to/audio.mp3"
node {baseDir}/assemblyai.mjs transcribe "https://example.com/audio.mp3"
```

Write transcript to a file (recommended for long audio):

```bash
node {baseDir}/assemblyai.mjs transcribe "./path/to/audio.mp3" --out ./transcript.txt
```

### Pass advanced transcription options

Any fields supported by `POST /v2/transcript` can be passed via `--config`:

```bash
node {baseDir}/assemblyai.mjs transcribe "./path/to/audio.mp3" \
  --config '{"speaker_labels":true,"summarization":true,"summary_model":"informative","summary_type":"bullets"}' \
  --export json \
  --out ./transcript.json
```

### Export subtitles (SRT/VTT)

Transcribe and immediately export subtitles:

```bash
node {baseDir}/assemblyai.mjs transcribe "./path/to/video.mp4" --export srt --out ./subtitles.srt
node {baseDir}/assemblyai.mjs transcribe "./path/to/video.mp4" --export vtt --out ./subtitles.vtt
```

Or export subtitles from an existing transcript ID:

```bash
node {baseDir}/assemblyai.mjs subtitles <transcript_id> srt --out ./subtitles.srt
```

### Export paragraphs / sentences

```bash
node {baseDir}/assemblyai.mjs paragraphs <transcript_id> --out ./paragraphs.txt
node {baseDir}/assemblyai.mjs sentences <transcript_id> --out ./sentences.txt
```

### Fetch an existing transcript

```bash
node {baseDir}/assemblyai.mjs get <transcript_id> --format json
node {baseDir}/assemblyai.mjs get <transcript_id> --wait --format text
```

## Guidance

- Prefer `--out <file>` when output might be large.
- Keep API keys out of logs and chat; rely on env injection.
- If a user asks for EU processing/data residency, set `ASSEMBLYAI_BASE_URL` to the EU host.
- AssemblyAI requires that uploads and the subsequent transcript request use an API key from the same AssemblyAI project (otherwise you can get a 403 / 'Cannot access uploaded file').
