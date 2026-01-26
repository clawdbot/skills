---
name: reve-ai
description: Generate, edit, and remix images using the Reve AI API. Use when creating images from text prompts, editing existing images with instructions, or combining/remixing multiple reference images. Requires REVE_API_KEY or REVE_AI_API_KEY environment variable.
---

# Reve AI Image Generation

Generate, edit, and remix images using Reve's AI API.

## Prerequisites

- Bun runtime
- `REVE_API_KEY` or `REVE_AI_API_KEY` environment variable set

## Quick Usage

```bash
# Generate image from prompt
bun scripts/reve.ts create "A beautiful sunset over mountains" -o sunset.png

# With aspect ratio
bun scripts/reve.ts create "A cat in space" -o cat.png --aspect 16:9

# Edit existing image
bun scripts/reve.ts edit "Add dramatic clouds" -i photo.png -o edited.png

# Remix multiple images
bun scripts/reve.ts remix "Person from <img>0</img> in scene from <img>1</img>" -i person.png -i background.png -o remix.png
```

## Commands

### create
Generate a new image from a text prompt.

Options:
- `-o, --output FILE` — Output file path (default: output.png)
- `--aspect RATIO` — Aspect ratio: 16:9, 9:16, 3:2, 2:3, 4:3, 3:4, 1:1 (default: 3:2)
- `--version VER` — Model version (default: latest)

### edit
Modify an existing image using text instructions.

Options:
- `-i, --input FILE` — Input image to edit (required)
- `-o, --output FILE` — Output file path (default: output.png)
- `--version VER` — Model version: latest, latest-fast, reve-edit@20250915, reve-edit-fast@20251030

### remix
Combine text prompts with reference images. Use `<img>N</img>` in prompt to reference images by index (0-based).

Options:
- `-i, --input FILE` — Reference images (can specify multiple, up to 6)
- `-o, --output FILE` — Output file path (default: output.png)
- `--aspect RATIO` — Aspect ratio (same options as create)
- `--version VER` — Model version: latest, latest-fast, reve-remix@20250915, reve-remix-fast@20251030

## Constraints

- Max prompt length: 2560 characters
- Max reference images for remix: 6
- Valid aspect ratios: 16:9, 9:16, 3:2, 2:3, 4:3, 3:4, 1:1

## Response

The script outputs JSON with generation details:
```json
{
  "output": "path/to/output.png",
  "version": "reve-create@20250915",
  "credits_used": 18,
  "credits_remaining": 982
}
```

## Errors

- `401` — Invalid API key
- `402` — Insufficient credits
- `429` — Rate limited (includes retry_after)
- `422` — Invalid input (prompt too long, bad aspect ratio)
