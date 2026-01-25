---
name: openai-tts
description: |
  Text-to-speech conversion using OpenAI's TTS API for generating high-quality, natural-sounding audio.
  Supports 6 voices (alloy, echo, fable, onyx, nova, shimmer), speed control (0.25x-4.0x),
  HD quality model, multiple output formats (mp3, opus, aac, flac), and automatic text chunking
  for long content (4096 char limit per request).
  Use when: (1) User requests audio/voice output with triggers like "read this to me",
  "convert to audio", "generate speech", "text to speech", "tts", "narrate", "speak",
  or when keywords "openai tts", "voice", "podcast" appear. (2) Content needs to be spoken
  rather than read (multitasking, accessibility). (3) User wants specific voice preferences
  like "alloy", "echo", "fable", "onyx", "nova", "shimmer" or speed adjustments.
---

# OpenAI TTS

Text-to-speech conversion using OpenAI's TTS API for generating high-quality, natural-sounding audio from text.

## Features
- 6 different voice options (male/female)
- Standard and HD quality models
- Automatic text chunking for long content (4096 char limit)
- Multiple output formats (mp3, opus, aac, flac)

## Activation

This skill activates when the user:
- Requests audio/voice output: "read this to me", "convert to audio", "generate speech", "make this an audio file"
- Uses keywords: "tts", "openai tts", "text to speech", "voice", "audio", "podcast"
- Needs content spoken for accessibility, multitasking, or podcast creation
- Specifies voice preferences: "alloy", "echo", "fable", "onyx", "nova", "shimmer"
- Asks to "narrate", "speak", or "vocalize" text

## Requirements

- `OPENAI_API_KEY` environment variable must be set
- Python 3.8+
- Dependencies: `openai`, `pydub` (optional, for long text)

## Voices

| Voice | Type | Description |
|-------|------|-------------|
| alloy | Neutral | Balanced, versatile |
| echo | Male | Warm, conversational |
| fable | Neutral | Expressive, storytelling |
| onyx | Male | Deep, authoritative |
| nova | Female | Friendly, upbeat |
| shimmer | Female | Clear, professional |

## Usage

### Basic Usage
```python
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

response = client.audio.speech.create(
    model="tts-1",      # or "tts-1-hd" for higher quality
    voice="onyx",       # choose from: alloy, echo, fable, onyx, nova, shimmer
    input="Your text here",
    speed=1.0           # 0.25 to 4.0 (optional)
)

with open("output.mp3", "wb") as f:
    for chunk in response.iter_bytes():
        f.write(chunk)
```

### Command Line
```bash
# Basic
python -c "
from openai import OpenAI
client = OpenAI()
response = client.audio.speech.create(model='tts-1', voice='onyx', input='Hello world')
open('output.mp3', 'wb').write(response.content)
"
```

### Long Text (Auto-chunking)
```python
from openai import OpenAI
from pydub import AudioSegment
import tempfile
import os
import re

client = OpenAI()
MAX_CHARS = 4096

def split_text(text):
    if len(text) <= MAX_CHARS:
        return [text]

    chunks = []
    sentences = re.split(r'(?<=[.!?])\s+', text)
    current = ''

    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= MAX_CHARS:
            current += (' ' if current else '') + sentence
        else:
            if current:
                chunks.append(current)
            current = sentence

    if current:
        chunks.append(current)

    return chunks

def generate_tts(text, output_path, voice='onyx', model='tts-1'):
    chunks = split_text(text)

    if len(chunks) == 1:
        response = client.audio.speech.create(model=model, voice=voice, input=text)
        with open(output_path, 'wb') as f:
            f.write(response.content)
    else:
        segments = []
        for chunk in chunks:
            response = client.audio.speech.create(model=model, voice=voice, input=chunk)
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                tmp.write(response.content)
                segments.append(AudioSegment.from_mp3(tmp.name))
                os.unlink(tmp.name)

        combined = segments[0]
        for seg in segments[1:]:
            combined += seg
        combined.export(output_path, format='mp3')

    return output_path

# Usage
generate_tts("Your long text here...", "output.mp3", voice="nova")
```

## Models

| Model | Quality | Speed | Cost |
|-------|---------|-------|------|
| tts-1 | Standard | Fast | $0.015/1K chars |
| tts-1-hd | High Definition | Slower | $0.030/1K chars |

## Output Formats

Supported formats: `mp3` (default), `opus`, `aac`, `flac`

```python
response = client.audio.speech.create(
    model="tts-1",
    voice="onyx",
    input="Hello",
    response_format="opus"  # or mp3, aac, flac
)
```

## Error Handling

```python
from openai import OpenAI, APIError, RateLimitError
import time

client = OpenAI()

def generate_with_retry(text, voice='onyx', max_retries=3):
    for attempt in range(max_retries):
        try:
            response = client.audio.speech.create(
                model="tts-1",
                voice=voice,
                input=text
            )
            return response.content
        except RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            raise
        except APIError as e:
            print(f"API Error: {e}")
            raise

    return None
```

## Examples

### Convert Article to Podcast
```python
def article_to_podcast(article_text, output_file):
    intro = "Welcome to today's article reading."
    outro = "Thank you for listening."

    full_text = f"{intro}\n\n{article_text}\n\n{outro}"

    generate_tts(full_text, output_file, voice='nova', model='tts-1-hd')
    print(f"Podcast saved to {output_file}")
```

### Batch Processing
```python
def batch_tts(texts, output_dir, voice='onyx'):
    import os
    os.makedirs(output_dir, exist_ok=True)

    for i, text in enumerate(texts):
        output_path = os.path.join(output_dir, f"audio_{i+1}.mp3")
        generate_tts(text, output_path, voice=voice)
        print(f"Generated: {output_path}")
```

## Links

- [OpenAI TTS Documentation](https://platform.openai.com/docs/guides/text-to-speech)
- [OpenAI API Reference](https://platform.openai.com/docs/api-reference/audio/createSpeech)
- [Pricing](https://openai.com/pricing)
