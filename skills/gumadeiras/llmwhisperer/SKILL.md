---
name: llmwhisperer
description: Extract text and layout from images and PDFs using LLMWhisperer API. Good for handwriting and complex forms.
metadata: {"clawdbot":{"emoji":"📄","scripts":["scripts/llmwhisperer"]}}
---

# LLMWhisperer

Extract text from images and PDFs using the [LLMWhisperer API](https://unstract.com/llmwhisperer/) — great for handwriting and complex forms.

## Configuration

Requires `LLMWHISPERER_API_KEY` in `~/.clawdbot/.env`:
```bash
echo "LLMWHISPERER_API_KEY=your_key_here" >> ~/.clawdbot/.env
```

### Get an API Key
Get a free API key at [unstract.com/llmwhisperer](https://unstract.com/llmwhisperer/).
- **Free Tier:** 100 pages/day

## Usage

```bash
llmwhisperer <file>
```

The script is located at `~/.clawdbot/skills/llmwhisperer/scripts/llmwhisperer`.

## Examples

**Print text to terminal:**
```bash
llmwhisperer flyer.jpg
```

**Save output to a text file:**
```bash
llmwhisperer invoice.pdf > invoice.txt
```

**Process a handwritten note:**
```bash
llmwhisperer notes.jpg
```
