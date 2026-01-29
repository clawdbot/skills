# Catbox/Litterbox File Uploader

Upload files to catbox.moe (permanent) or litterbox.catbox.moe (temporary).

## Usage

Upload to Litterbox (temporary, preferred):
```bash
python upload.py /path/to/file.mp4
python upload.py /path/to/file.mp4 --time 24h
```

Upload to Catbox (permanent):
```bash
python upload.py /path/to/file.png --service catbox --userhash YOUR_HASH
```

## Options

- `--service`: `litterbox` (default) or `catbox`
- `--time`: Litterbox expiration: `1h`, `12h`, `24h`, `72h` (default: `24h`)
- `--userhash`: Catbox account hash (optional, required for tracking)

## Limits

| Service | Max Size | Duration |
|---------|----------|----------|
| Litterbox | 1 GB | 1h - 72h |
| Catbox | 200 MB | Permanent |

## Returns

URL of uploaded file on success.
