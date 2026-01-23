---
name: mineru-pdf
description: Parse PDFs locally (CPU) into Markdown/JSON using MinerU. Assumes MinerU creates per‑doc output folders; supports table/image extraction.
---

# MinerU PDF

## Overview
Parse a PDF locally with MinerU (CPU). Default output is Markdown + JSON. Use tables/images only when requested.

## Quick start (single PDF)
```bash
# Run from the skill directory
./scripts/mineru_parse.sh /path/to/file.pdf
```

Optional examples:
```bash
./scripts/mineru_parse.sh /path/to/file.pdf --format json
./scripts/mineru_parse.sh /path/to/file.pdf --tables --images
```

## When to read references
If flags differ from your wrapper or you need advanced defaults (backend/method/device/threads/format mapping), read:
- `references/mineru-cli.md`

## Output conventions
- Output root defaults to `./mineru-output/`.
- MinerU creates the per-document subfolder under the output root (e.g., `./mineru-output/<basename>/...`).

## Batching
Default is single-PDF parsing. Only implement batch folder parsing if explicitly requested.
