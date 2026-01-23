# MinerU PDF Parser - Clawdbot Skill

A [Clawdbot](https://github.com/clawdbot/clawdbot) skill for parsing PDFs locally using [MinerU](https://github.com/opendatalab/MinerU) (CPU). Produces rich structured output including Markdown, JSON with layout data, and extracted images.

## Features

- **Local CPU processing** — No GPU required; runs entirely on your machine
- **Rich structured output** — Markdown + detailed JSON with layout information
- **Image extraction** — Automatically extracts embedded images
- **Table support** — Optional table extraction (if supported by your MinerU version)
- **Configurable** — Flexible env overrides for different MinerU wrappers

## Installation

### Prerequisites

1. **MinerU CLI** installed and accessible (see [MinerU installation](https://github.com/opendatalab/MinerU))
2. **Clawdbot** installed

### Install the skill

```bash
# Clone the repo
git clone https://github.com/kesslerio/MinerU-PDF-Parser-Clawdbot-Skill.git

# Or copy the mineru-pdf/ folder to your Clawdbot skills directory
cp -r MinerU-PDF-Parser-Clawdbot-Skill/mineru-pdf ~/.clawdbot/skills/
```

## Usage

### Quick start

```bash
# Run from the skill directory
./scripts/mineru_parse.sh /path/to/document.pdf
```

### Options

```bash
./scripts/mineru_parse.sh /path/to/document.pdf --format json
./scripts/mineru_parse.sh /path/to/document.pdf --tables --images
./scripts/mineru_parse.sh /path/to/document.pdf --outroot ./my-output
```

| Option | Default | Description |
|--------|---------|-------------|
| `--format` | `both` | Output format: `md`, `json`, or `both` |
| `--outroot` | `./mineru-output` | Output root directory |
| `--tables` | off | Extract tables (if supported) |
| `--images` | off | Extract images (if supported) |
| `--threads` | `4` | Thread count (OMP_NUM_THREADS) |
| `--lang` | `en` | Language |
| `--backend` | `pipeline` | MinerU backend |
| `--method` | `auto` | Processing method |
| `--device` | `cpu` | Device (cpu/gpu) |

### Configuration

If your MinerU wrapper uses different flags, set env overrides. See `mineru-pdf/references/mineru-cli.md` for full documentation.

```bash
export MINERU_CMD=~/.local/bin/mineru
export MINERU_INPUT_FLAG=-p
export MINERU_OUTPUT_FLAG=-o
```

## Output

MinerU creates a per-document subfolder under the output root:

```
./mineru-output/
└── document-name/
    └── auto/
        ├── document-name.md          # Markdown output
        ├── document-name_middle.json # Rich structured JSON (~50KB+)
        ├── document-name_layout.pdf  # Layout visualization
        └── images/                   # Extracted images
```

### Output quality

MinerU produces **rich structured output** including:
- Layout-aware text extraction
- Detailed JSON with position/structure metadata
- Extracted images and layout PDFs

**Best for:** Documents requiring accurate layout preservation, image extraction, or structured data output.

## Comparison with PyMuPDF

| Aspect | MinerU | PyMuPDF |
|--------|--------|---------|
| Speed | Slower (~15-30s/page) | Fast (~1s/page) |
| JSON output | Rich (~50KB+, layout data) | Minimal (~1KB, text only) |
| Image extraction | Yes (automatic) | Yes (optional) |
| Layout preservation | Excellent | Basic |
| Dependencies | Heavy (~20GB models) | Light (pip install) |

**Use MinerU when:** Quality and structure matter more than speed.  
**Use PyMuPDF when:** Speed matters or for simple text extraction.

## License

Apache 2.0

## Contributing

Issues and PRs welcome. Please test with a variety of PDFs before submitting changes.

## Related

- [PyMuPDF PDF Parser Skill](https://github.com/kesslerio/PyMuPDF-PDF-Parser-Clawdbot-Skill) — Fast, lightweight alternative
- [MinerU](https://github.com/opendatalab/MinerU) — The underlying PDF parser
- [Clawdbot](https://github.com/clawdbot/clawdbot) — The AI agent framework
