---
name: gamma
description: Generate AI-powered presentations, documents, and social posts using Gamma.app API. Use when user asks to create a presentation, pitch deck, slide deck, document, or social media carousel. Triggers on requests like "create a presentation about X", "make a pitch deck", "generate slides", or "create a Gamma about X".
metadata: {"clawdbot":{"requires":{"env":["GAMMA_API_KEY"]}}}
---

# Gamma.app API

Generate beautiful presentations, documents, and social posts with AI.

## Setup

```bash
export GAMMA_API_KEY="sk-gamma-xxxxx"
```

## Quick Commands

```bash
# Generate a presentation
{baseDir}/scripts/gamma.sh generate "Your content or topic here"

# Generate with options
{baseDir}/scripts/gamma.sh generate "Content" --format presentation --cards 12

# Check generation status
{baseDir}/scripts/gamma.sh status <generationId>

# List recent generations (if supported)
{baseDir}/scripts/gamma.sh list
```

## Script Usage

### Generate

```bash
{baseDir}/scripts/gamma.sh generate "<content>" [options]

Options:
  --format       presentation|document|social (default: presentation)
  --cards        Number of cards/slides (default: 10)
  --instructions Additional instructions for styling/tone
  --amount       concise|detailed (default: detailed)
  --tone         e.g., "professional", "casual", "technical"
  --audience     e.g., "investors", "developers", "general"
  --image-source aiGenerated|web|none (default: aiGenerated)
  --image-style  illustration|photo|mixed (default: illustration)
  --wait         Wait for completion and return URL
```

### Examples

```bash
# Simple presentation
{baseDir}/scripts/gamma.sh generate "The future of AI automation" --wait

# Pitch deck with specific styling
{baseDir}/scripts/gamma.sh generate "$(cat pitch.md)" \
  --format presentation \
  --cards 15 \
  --instructions "Make it a professional pitch deck for investors" \
  --tone "professional" \
  --audience "investors" \
  --wait

# Social carousel
{baseDir}/scripts/gamma.sh generate "5 tips for productivity" \
  --format social \
  --cards 5 \
  --wait

# Document/report
{baseDir}/scripts/gamma.sh generate "Q4 2025 Performance Report" \
  --format document \
  --amount detailed \
  --wait
```

## API Reference

### Endpoint
```
POST https://public-api.gamma.app/v1.0/generations
```

### Headers
```
X-API-KEY: <your-api-key>
Content-Type: application/json
```

### Request Body

```json
{
  "inputText": "Your content (1-750,000 chars)",
  "textMode": "generate",
  "format": "presentation|document|social",
  "numCards": 10,
  "additionalInstructions": "Styling instructions",
  "textOptions": {
    "amount": "concise|detailed",
    "tone": "professional",
    "audience": "target audience"
  },
  "imageOptions": {
    "source": "aiGenerated|web|none",
    "model": "flux-kontext-pro",
    "style": "illustration|photo"
  },
  "cardOptions": {
    "dimensions": "fluid|16x9|4x3|1x1|4x5|9x16"
  }
}
```

### Response

Initial response:
```json
{"generationId": "abc123"}
```

Poll for status:
```
GET https://public-api.gamma.app/v1.0/generations/<generationId>
```

Completed response:
```json
{
  "generationId": "abc123",
  "status": "completed",
  "gammaUrl": "https://gamma.app/docs/xxxxx",
  "credits": {"deducted": 150, "remaining": 7500}
}
```

## Format Options

| Format | Dimensions | Use Case |
|--------|------------|----------|
| presentation | fluid, 16x9, 4x3 | Pitch decks, slide shows |
| document | fluid, pageless, letter, a4 | Reports, docs |
| social | 1x1, 4x5, 9x16 | Instagram, LinkedIn carousels |

## Notes

- Generation typically takes 1-3 minutes
- Credits are deducted per generation (~150-300 per deck)
- Input text can be markdown formatted
- Use `--wait` flag to block until completion and get URL directly
