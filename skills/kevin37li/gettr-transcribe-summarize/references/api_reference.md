# Notes / Reference

This skill assumes a simple, mostly-static GETTR post HTML page where the media URL is discoverable via `og:video*` meta tags.

## Meta tags searched
The extractor script prefers these, in order:
1. `og:video:secure_url`
2. `og:video:url`
3. `og:video`

## Output files (suggested)
- `./out/gettr.mp4` – downloaded video container
- `./out/gettr.srt` – timestamped transcript (recommended)
- `./out/gettr.txt` – plain transcript (optional)
