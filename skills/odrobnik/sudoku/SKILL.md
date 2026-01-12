---
name: sudoku
description: Fetch Sudoku puzzles and store them as JSON in the workspace; render images on demand; reveal solutions later.
metadata:
  clawdbot:
    emoji: "🧩"
    requires:
      bins: ["python3", "node"]
---

# Skill: sudoku

This skill fetches Sudoku puzzles from **sudokuonline.io**, stores them as **JSON files in the workspace**, and generates images from JSON **on demand**.

## Storage model (default)

- Stored puzzles live here:
  - `./sudoku/puzzles/*.json`

- Generated images (ephemeral, can be deleted/recreated anytime) go here:
  - `./sudoku/renders/*.png`

No `state.json` and no append-only history file.

**“Latest puzzle”** = the newest JSON file in `./sudoku/puzzles/`.

## Presets (what we can provide)

```bash
# from the workspace
./sudoku.py list
./sudoku.py list --json
```

Current presets:
- `kids4n` — Kids 4x4
- `kids4l` — Kids 4x4 with Letters
- `kids6` — Kids 6x6
- `kids6l` — Kids 6x6 with Letters
- `easy9` / `medium9` / `hard9` / `evil9` — Classic 9x9 (Easy/Medium/Hard/Evil)

## Getting a puzzle (store JSON)

```bash
./sudoku.py get kids4n --json
./sudoku.py get easy9 --json
```

This creates a new JSON file under `./sudoku/puzzles/` containing:
- metadata (preset, source URL, puzzle id, size)
- `clues` grid
- `solution` grid (stored but not revealed unless asked)

### User preference: image vs link vs both

Telegram: send links as a short titled link (button-like), not as raw URLs (unless debugging).

When responding to “get me a puzzle”, decide what to send:
- **image only**
- **link only**
- **both image + link**

Defaults:
- If the user says “just the image” → send only the generated image.
- If the user asks for a “link” → send only the link (if available).
- If vague → send the image, and include the link when available.

### Important: SudokuPad share link support

- Only **Classic 9x9** puzzles produce a SudokuPad share link.
- Kids 4x4/6x6 should be treated as **image-first** (no link).

#### Link format & URL-encoding gotcha (Telegram-safe)

SudokuPad `/puzzle/<payload>` links are **fragile** if anything URL-encodes the payload:
- If `+` becomes `%2B` (or `+` is treated as space), the LZ-String bitstream changes and the puzzle **won’t load**.

**Fix:** generate the payload using **LZString `compressToEncodedURIComponent`**.
- This produces a URL-safe alphabet (avoids `+`, `/`, `=`)
- You must **not** percent-encode the payload afterwards

Resulting link shape:
- `https://sudokupad.svencodes.com/puzzle/<url-safe-payload>`

## Generating a puzzle image from JSON

### Clean image (default)

The default render is a clean grid image with no header text (good for sharing).

### Printable layout (optional)

For printing you should prefer generating an **A4 PDF** (margin-safe, high DPI) so borders don’t get clipped and text stays crisp:

```bash
./venv/bin/python skills/sudoku/sudoku.py puzzle --pdf
```

A printable PNG variant still exists (useful for previews):

```bash
./venv/bin/python skills/sudoku/sudoku.py puzzle --printable
```

Current printable header layout:
- top-left: difficulty label (e.g. “Easy Classic”)
- top-right: short ID (8 chars)


```bash
# render latest puzzle (clean PNG)
./sudoku.py puzzle

# A4 PDF for printing (recommended)
./sudoku.py puzzle --pdf

# printable PNG (preview)
./sudoku.py puzzle --printable

# pick a specific stored JSON
./sudoku.py puzzle --file sudoku/puzzles/<file>.json

# pick by puzzle id (full UUID or short 8-char id from filename)
./sudoku.py puzzle --id 324306f5
```

The command prints the image path (or JSON output if `--json`).

## Revealing solutions later (on explicit request)

Reveal uses the latest stored puzzle JSON by default.

### Full solution image

```bash
./sudoku.py reveal
# or explicitly
./sudoku.py reveal --full

# A4 PDF for printing (recommended)
./sudoku.py reveal --pdf

# printable PNG (preview)
./sudoku.py reveal --printable
```

Reveal styling:
- givens/clues are **black**
- filled-in values are **blue**

### Single box

```bash
./venv/bin/python skills/sudoku/sudoku.py reveal --box 5
./venv/bin/python skills/sudoku/sudoku.py reveal --box 2 3
```

### Single cell

```bash
./venv/bin/python skills/sudoku/sudoku.py reveal --cell 3 7

# optionally also generate a tiny cell image
./venv/bin/python skills/sudoku/sudoku.py reveal --cell 3 7 --image
```

## Assistant rules

- Never reveal solutions unless the user explicitly asks.
- Use “latest JSON” behavior by default when the user says “reveal”.
- Telegram UX: headlines should be sent as a separate text message *before* the image. Image captions appear **below** the image.
  - If the Telegram media send requires a non-empty caption, use a minimal invisible caption like a zero‑width space (`\u200b`).
