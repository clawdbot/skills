---
name: xkcd
description: Fetch xkcd comics - latest, random, by number, or search by keyword. Display comics with title, image, and alt text (the hidden joke). Generate custom xkcd-style stick figure comics using image generation. Perfect for daily comic delivery via cron, on-demand requests, or creating original xkcd-inspired content.
homepage: https://xkcd.com
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["uv"]}}}
---

# xkcd

Fetch comics from xkcd.com or generate xkcd-style images.

## Commands

### Latest Comic
```bash
uv run {baseDir}/scripts/xkcd.py
```

### Random Comic
```bash
uv run {baseDir}/scripts/xkcd.py --random
```

### Specific Comic
```bash
uv run {baseDir}/scripts/xkcd.py 327         # Bobby Tables
uv run {baseDir}/scripts/xkcd.py 353         # Python
uv run {baseDir}/scripts/xkcd.py 1053        # Ten Thousand
```

### Search by Keyword
```bash
uv run {baseDir}/scripts/xkcd.py --search "python"
uv run {baseDir}/scripts/xkcd.py --search "space" --limit 3
```

### JSON Output
```bash
uv run {baseDir}/scripts/xkcd.py --format json
uv run {baseDir}/scripts/xkcd.py --random --format json
```

## Output Format

Default markdown output includes:
- **Title**: Comic title with number
- **Image**: Direct image URL
- **Alt text**: The hidden hover text (often the best part!)
- **Link**: Permalink to xkcd.com

## Generating Custom xkcd-Style Comics

Use an image generation skill (e.g., nano-banana-pro) with this prompt pattern:

```
Create an xkcd-style comic: [your scene description]

Style: simple black and white stick figures, hand-drawn wobbly lines,
minimal background, clean white background, comic panel layout
```

Example prompt:
```
Create an xkcd-style comic: Two programmers at computers. First says
"I spent 6 hours automating a task." Second: "How long did the task take?"
First: "5 minutes." Second: "How often do you do it?" First: "Once a year."
```

## Cron Examples

```bash
# Daily latest comic at 9 AM
cron add --schedule "0 9 * * *" --task "Fetch latest xkcd and send via Telegram"

# Random classic every Monday
cron add --schedule "0 10 * * 1" --task "Fetch random xkcd comic and share"
```

## Classic Comics

- **#327** "Exploits of a Mom" — Bobby Tables / SQL injection
- **#353** "Python" — import antigravity
- **#303** "Compiling" — sword fighting while code compiles
- **#386** "Duty Calls" — someone is wrong on the internet
- **#1053** "Ten Thousand" — lucky 10,000 learning something new
- **#979** "Wisdom of the Ancients" — unanswered forum posts
- **#927** "Standards" — how standards proliferate

## API

Uses the official [xkcd JSON API](https://xkcd.com/json.html) (no auth required).
- Latest: `https://xkcd.com/info.0.json`
- Specific: `https://xkcd.com/{num}/info.0.json`
