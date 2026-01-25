---
name: gettr-transcribe-summarize
description: Download a video from a GETTR post (via HTML og:video), transcribe it locally with MLX Whisper on Apple Silicon (optionally with timestamps via SRT/VTT), and summarize the transcript into bullet points and/or a timestamped outline. Use when given a GETTR post URL and asked to produce a transcript or summary, or when building a repeatable GETTR→MP4→MLX Whisper→summary pipeline.
---

# Gettr Transcribe + Summarize (MLX Whisper)

## Workflow (GETTR URL → transcript → summary)

### Inputs to confirm
Ask for:
- GETTR post URL
- Output format: **bullets only** or **bullets + timestamped outline**
- Summary size: **short**, **medium** (default), or **detailed**

Notes:
- This skill does **not** handle authentication-gated GETTR posts.
- This skill does **not** translate; outputs stay in the video’s original language.

### Prereqs (local)
- `mlx_whisper` installed and on PATH
- `ffmpeg` installed (recommended: `brew install ffmpeg`)

### Step 0 — Pick an output directory
Recommended convention:
- `./out/gettr.mp4`
- `./out/gettr.srt` (or `gettr.vtt`)
- `./out/summary.md`

### Step 1 — Extract the media URL (usually `.m3u8`)
Preferred: fetch the post HTML and read `og:video*`.

```bash
python3 scripts/extract_gettr_og_video.py "<GETTR_POST_URL>"
```
This prints the best candidate video URL (often an HLS `.m3u8`).

If this fails, ask the user to provide the `.m3u8`/MP4 URL directly (common if the post is private/gated or the HTML is dynamic).

### Step 2 — Download/record with ffmpeg
```bash
bash scripts/download_with_ffmpeg.sh "<M3U8_OR_MP4_URL>" ./out/gettr.mp4
```

Optional audio-only (faster transcription sometimes):
```bash
ffmpeg -y -i ./out/gettr.mp4 -vn -ac 1 -ar 16000 ./out/gettr.wav
```

### Step 3 — Transcribe with MLX Whisper
Timestamp-friendly (recommended):
```bash
mlx_whisper ./out/gettr.mp4 -f srt -o ./out --model mlx-community/whisper-large-v3-turbo
```
Plain text:
```bash
mlx_whisper ./out/gettr.mp4 -f txt -o ./out --model mlx-community/whisper-large-v3-turbo
```

Notes:
- Prefer SRT/VTT when you need a timestamped outline.
- If `large-v3-turbo` is too slow or memory-heavy, switch to a smaller Whisper model.

### Step 4 — Summarize
Write the final deliverable to `./out/summary.md`.

Pick a **summary size** (user-selectable):
- **Short:** 5–8 bullets; (if outline) 4–6 sections
- **Medium (default):** 8–20 bullets; (if outline) 6–15 sections
- **Detailed:** 20–40 bullets; (if outline) 15–30 sections

Write the final deliverable to `./out/summary.md` with:
- **Bullets** (per size above)
- Optional **timestamped outline** (per size above)

Timestamped outline format (default heading style):
```
[00:00 - 02:15] Section heading
- 1–3 sub-bullets
```

When building the outline from SRT cues:
- Group adjacent cues into coherent sections.
- Use the start time of the first cue and end time of the last cue in the section.

## Bundled scripts
- `scripts/extract_gettr_og_video.py`: fetch GETTR HTML and extract `og:video*` URL
- `scripts/download_with_ffmpeg.sh`: download/record HLS or MP4 URL to a local MP4

## Troubleshooting
See `references/troubleshooting.md`.
