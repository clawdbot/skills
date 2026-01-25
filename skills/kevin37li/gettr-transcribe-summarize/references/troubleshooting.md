# Troubleshooting (GETTR → ffmpeg → MLX Whisper)

## ffmpeg not found
Install on macOS:
```bash
brew install ffmpeg
```

## og:video not found
- GETTR may be serving different HTML to different user agents, or the content is loaded dynamically.
- Try opening the post in a browser and **View Source**; confirm an `og:video` meta tag exists.
- If the page requires auth/JS rendering, you may need a different fetch method (e.g., browser automation) instead of a plain HTTP fetch.

## ffmpeg download fails on HLS (.m3u8)
Common fixes:
- Try re-encode fallback (the script does this automatically)
- If the playlist uses redirects, test:
  ```bash
  ffmpeg -loglevel warning -i "<m3u8>" -t 00:00:30 -c copy /tmp/test.mp4
  ```

## Private/gated GETTR posts (auth)
This skill does **not** handle GETTR authentication.

If extraction fails because the post is private/gated or requires JS:
- Ask the user for a direct `.m3u8` or MP4 URL, or
- Use a browser/manual approach to retrieve the media URL.

## Timestamps
- If you need strict timestamps for a timestamped outline, prefer SRT/VTT output.

## Quality tips
- Audio-only `wav` at 16kHz mono can improve speed and stability:
  ```bash
  ffmpeg -y -i gettr.mp4 -vn -ac 1 -ar 16000 gettr.wav
  mlx_whisper gettr.wav -f srt -o ./out --model mlx-community/whisper-large-v3-turbo
  ```
