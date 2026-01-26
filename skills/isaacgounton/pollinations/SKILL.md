---
name: pollinations
description: Pollinations.ai API for AI generation - text, images, videos, audio, and analysis. Use when user requests AI-powered generation (text completion, images, videos, audio, vision/analysis, transcription) or mentions Pollinations. Supports 25+ models (OpenAI, Claude, Gemini, Flux, Veo, etc.) with OpenAI-compatible chat endpoint and specialized generation endpoints.
---

# Pollinations 🧬

Unified AI platform for text, images, videos, and audio generation with 25+ models.

## API Key

Get free or paid keys at https://enter.pollinations.ai
- Secret Keys (`sk_`): Server-side, no rate limits (recommended)
- Optional for many operations (free tier available)

Store key in environment variable:
```bash
export POLLINATIONS_API_KEY="sk_your_key_here"
```

## Quick Start

### Text Generation

**Simple text generation:**
```bash
curl "https://gen.pollinations.ai/text/Hello%20world"
```

**Chat completions (OpenAI-compatible):**
```bash
curl -X POST https://gen.pollinations.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $POLLINATIONS_API_KEY" \
  -d '{
    "model": "openai",
    "messages": [{"role": "user", "content": "Hello"}]
  }'
```

**Use script:** `scripts/chat.sh` for easy chat completions

### Image Generation

```bash
curl "https://gen.pollinations.ai/image/A%20sunset%20over%20mountains?model=flux&width=1024&height=1024"
```

**Use script:** `scripts/image.sh` for image generation

### Audio Generation (TTS)

```bash
curl -X POST https://gen.pollinations.ai/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai-audio",
    "messages": [
      {"role": "system", "content": "You are a text reader. Read the user text exactly without responding, adding conversation, or changing anything."},
      {"role": "user", "content": "Say: Hello world"}
    ],
    "modalities": ["text", "audio"],
    "audio": {"voice": "nova", "format": "mp3"}
  }'
```

**Use script:** `scripts/tts.sh` for text-to-speech

## API Endpoints

### Base URLs
- Chat/Text: `https://gen.pollinations.ai/v1/chat/completions`
- Simple Text: `https://gen.pollinations.ai/text/{prompt}`
- Image: `https://gen.pollinations.ai/image/{prompt}?{params}`
- Video: `https://gen.pollinations.ai/image/{prompt}?{params}` (generates video)

### Supported Operations

#### 1. Text/Chat Generation

**Models:** OpenAI, Claude, Gemini, Mistral, DeepSeek, Grok, Qwen Coder, Perplexity, and 20+ more

**Common models:** `openai`, `claude`, `gemini`, `mistral`, `deepseek`, `qwen`, `gpt-4`, `o1`, `o3`

**Parameters:**
- `model` (string): Model name/ID
- `messages` (array): Chat messages with roles (system/user/assistant)
- `temperature` (number): 0-2, default 1
- `max_tokens` (number): Max response length
- `top_p` (number): Nucleus sampling, default 1
- `seed` (number): Reproducibility (-1 for random)
- `jsonMode` (boolean): Force JSON response
- `reasoning_effort` (string): For o1/o3/R1 (high/medium/low/minimal/none)
- `thinking_budget` (number): Tokens for reasoning (thinking models)

**Vision support:** Include `image_url` in message content for multi-modal:
```json
{
  "role": "user",
  "content": [
    {"type": "text", "text": "Describe this image"},
    {"type": "image_url", "image_url": {"url": "https://example.com/image.jpg"}}
  ]
}
```

#### 2. Image Generation

**Models:** `flux` (default), `turbo`, `gptimage`, `kontext`, `seedream`, `nanobanana`, `nanobanana-pro`

**Parameters:**
- `model` (string): Model selection
- `width`/`height` (number): 16-2048px, default 1024
- `seed` (number): Reproducibility
- `negative_prompt` (string): What to avoid
- `nologo` (boolean): Remove watermark
- `private` (boolean): Private generation
- `safe` (boolean): Enable NSFW filter
- `enhance` (boolean): AI prompt enhancement
- `quality` (string): low/medium/high/hd (gptimage)
- `transparent` (boolean): Transparent background (gptimage)
- `count` (number): 1-4 images (premium)
- `image` (string): Input image URL (image-to-image)

**Format:** Returns binary image data (determined by Content-Type header)

#### 3. Image to Image

Use same image endpoint with `image` parameter:
```
https://gen.pollinations.ai/image/make%20it%20blue?image={source_url}
```

#### 4. Video Generation

**Models:** `veo` (4-8s), `seedance` (2-10s)

**Parameters:**
- `model` (string): veo or seedance
- `width`/`height` (number): Dimensions
- `duration` (number): Seconds (veo: 4/6/8, seedance: 2-10)
- `aspectRatio` (string): 16:9 or 9:16
- `audio` (boolean): Enable audio (veo only)
- `image` (string): Input image URL (frame interpolation: image[0]=first, image[1]=last)
- `negative_prompt` (string): What to avoid
- `seed` (number): Reproducibility
- `private`/`safe` (boolean): Privacy/safety options

**Format:** Returns binary video data

#### 5. Audio Generation (TTS)

**Models:** `openai-audio`

**Voices:** alloy, echo, fable, onyx, nova, shimmer, coral, verse, ballad, ash, sage, amuch, dan

**Formats:** mp3, wav, flac, opus, pcm16

**Parameters:**
- `model`: openai-audio
- `modalities`: ["text", "audio"]
- `audio.voice`: Voice selection
- `audio.format`: Output format

**Note:** Use "Say:" prefix in user message for direct text reading

#### 6. Audio Transcription

Use chat completions endpoint with vision/audio-capable models:
- **Models:** gemini, gemini-large, gemini-legacy, openai-audio
- Upload audio file as binary input
- Include transcription prompt in system message

#### 7. Image Analysis

Use chat completions with vision models:
- **Models:** Any vision-capable model (gemini, claude, openai)
- Include `image_url` in message content

#### 8. Video Analysis

Use chat completions with video-capable models:
- **Models:** gemini, claude, openai
- Upload video file as binary input
- Include analysis prompt

## Scripts

### `scripts/chat.sh`
Interactive chat completions with model selection and options.

**Usage:**
```bash
scripts/chat.sh "your message here"
scripts/chat.sh "your message" --model claude --temp 0.7
```

### `scripts/image.sh`
Generate images from text prompts.

**Usage:**
```bash
scripts/image.sh "a sunset over mountains"
scripts/image.sh "a sunset" --model flux --width 1024 --height 1024 --seed 123
```

### `scripts/tts.sh`
Convert text to speech.

**Usage:**
```bash
scripts/tts.sh "Hello world"
scripts/tts.sh "Hello world" --voice nova --format mp3 --output hello.mp3
```

## Tips

1. **Free tier available**: Many operations work without an API key (rate limited)
2. **OpenAI-compatible**: Use chat endpoint with existing OpenAI integrations
3. **Reproducibility**: Use `seed` parameter for consistent outputs
4. **Image enhancement**: Enable `enhance=true` for AI-improved prompts
5. **Video interpolation**: Pass two images with `image[0]=first&image[1]=last` for veo
6. **Audio reading**: Always use "Say:" prefix and proper system prompt for TTS

## API Documentation

Full docs: https://enter.pollinations.ai/api/docs
