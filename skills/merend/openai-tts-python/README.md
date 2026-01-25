# OpenAI TTS Skill

Text-to-speech conversion using OpenAI's TTS API for generating high-quality, natural-sounding audio from text.

## Installation

```bash
pip install openai pydub

# For audio processing (pydub dependency)
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg
```

## Setup

Set your OpenAI API key:

```bash
export OPENAI_API_KEY="sk-..."
```

## Usage

### Command Line

```bash
# Basic usage
python openai_tts.py "Hello world" -o output.mp3

# From file
python openai_tts.py -f article.txt -o article.mp3

# With voice selection
python openai_tts.py "Your text" -o output.mp3 --voice nova

# High quality
python openai_tts.py "Your text" -o output.mp3 --model tts-1-hd

# Adjust speed (0.25 to 4.0)
python openai_tts.py "Your text" -o output.mp3 --speed 1.5

# Pipe input
echo "Hello world" | python openai_tts.py -o output.mp3

# Verbose mode
python openai_tts.py "Test" -o test.mp3 -v

# List available voices
python openai_tts.py --list-voices
```

### As Module

```python
from openai_tts import generate_tts

# Basic
generate_tts("Hello world", "output.mp3")

# With options
generate_tts(
    text="Your text here",
    output_path="output.mp3",
    voice="nova",
    model="tts-1-hd",
    response_format="mp3",
    speed=1.25,  # 0.25 to 4.0
    verbose=True
)
```

## Voices

| Voice | Type | Description |
|-------|------|-------------|
| alloy | Neutral | Balanced, versatile |
| echo | Male | Warm, conversational |
| fable | Neutral | Expressive, storytelling |
| **onyx** | Male | Deep, authoritative (default) |
| nova | Female | Friendly, upbeat |
| shimmer | Female | Clear, professional |

## Models

| Model | Quality | Speed | Cost |
|-------|---------|-------|------|
| **tts-1** | Standard | Fast | $0.015/1K chars |
| tts-1-hd | High Definition | Slower | $0.030/1K chars |

## Features

- **Auto-chunking**: Automatically splits text longer than 4096 characters
- **Multiple formats**: mp3, opus, aac, flac
- **6 voices**: Male and female options
- **Pipe support**: Read from stdin

## Output Formats

| Format | Description |
|--------|-------------|
| **mp3** | Default, widely compatible |
| opus | Smaller file size, good quality |
| aac | Apple/iOS compatible |
| flac | Lossless, larger files |

## License

MIT
