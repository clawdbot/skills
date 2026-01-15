---
name: veo
description: Generate video using Google Veo (Veo 3.1 / Veo 3.0).
---

# Veo (Google Video Generation)

Generate video clips using Google's Veo API.

Generate video
```bash
uv run {baseDir}/scripts/generate_video.py --prompt "your video description" --filename "output.mp4"
```

Options
- `--duration` / `-d`: Video duration in seconds (default: 8, max varies by model)
- `--aspect-ratio` / `-a`: Aspect ratio (16:9, 9:16, 1:1)
- `--model`: Veo model to use (veo-2.0-generate-001, veo-3.0-generate-001, veo-3.1-generate-preview, etc.)
- `--api-key`: Override GEMINI_API_KEY

API key
- `GEMINI_API_KEY` env var (preferred)
- Or set `skills."veo".env.GEMINI_API_KEY` in `~/.clawdbot/clawdbot.json`

Notes
- Veo 3.1 supports higher quality and longer durations
- Output is MP4 format
- Use `--model veo-3.1-generate-preview` for best results
- Veo 3.0-fast-generate-001 is faster but lower quality
- The script prints a `MEDIA:` line for Clawdbot to auto-attach on supported chat providers.
