#!/usr/bin/env python3
"""
OpenAI TTS - Text-to-speech using OpenAI's TTS API

Usage:
    python openai_tts.py "Your text here" -o output.mp3
    python openai_tts.py -f input.txt -o output.mp3 --voice nova
    echo "Hello" | python openai_tts.py -o output.mp3

Voices: alloy, echo, fable, onyx (default), nova, shimmer
Models: tts-1 (default), tts-1-hd
"""

import argparse
import os
import sys
import re
import tempfile
from typing import List

# Constants
MAX_CHARS = 4096
VOICES = ['alloy', 'echo', 'fable', 'onyx', 'nova', 'shimmer']
MODELS = ['tts-1', 'tts-1-hd']
FORMATS = ['mp3', 'opus', 'aac', 'flac']
SPEED_MIN = 0.25
SPEED_MAX = 4.0
SPEED_DEFAULT = 1.0

VOICE_INFO = {
    'alloy': 'Neutral, balanced',
    'echo': 'Male, warm, conversational',
    'fable': 'Neutral, expressive, storytelling',
    'onyx': 'Male, deep, authoritative',
    'nova': 'Female, friendly, upbeat',
    'shimmer': 'Female, clear, professional'
}


def split_text(text: str, max_chars: int = MAX_CHARS) -> List[str]:
    """Split text into chunks respecting sentence boundaries."""
    if len(text) <= max_chars:
        return [text]

    chunks = []
    sentences = re.split(r'(?<=[.!?])\s+', text)
    current = ''

    for sentence in sentences:
        if len(current) + len(sentence) + 1 <= max_chars:
            current += (' ' if current else '') + sentence
        else:
            if current:
                chunks.append(current)
            if len(sentence) > max_chars:
                words = sentence.split()
                current = ''
                for word in words:
                    if len(current) + len(word) + 1 <= max_chars:
                        current += (' ' if current else '') + word
                    else:
                        if current:
                            chunks.append(current)
                        current = word
            else:
                current = sentence

    if current:
        chunks.append(current)

    return chunks


def generate_tts(
    text: str,
    output_path: str,
    voice: str = 'onyx',
    model: str = 'tts-1',
    response_format: str = 'mp3',
    speed: float = SPEED_DEFAULT,
    verbose: bool = False
) -> bool:
    """Generate TTS audio from text.

    Args:
        text: Text to convert to speech
        output_path: Path to save the audio file
        voice: Voice to use (alloy, echo, fable, onyx, nova, shimmer)
        model: Model to use (tts-1, tts-1-hd)
        response_format: Output format (mp3, opus, aac, flac)
        speed: Playback speed (0.25 to 4.0, default 1.0)
        verbose: Print progress information

    Returns:
        True if successful, False otherwise
    """
    try:
        from openai import OpenAI
    except ImportError:
        print("Error: openai package not installed. Run: pip install openai")
        return False

    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        return False

    client = OpenAI(api_key=api_key)
    chunks = split_text(text)

    if verbose:
        print(f"Text length: {len(text)} chars")
        print(f"Chunks: {len(chunks)}")
        print(f"Voice: {voice}, Model: {model}, Format: {response_format}, Speed: {speed}x")

    try:
        if len(chunks) == 1:
            if verbose:
                print("Generating audio...")
            response = client.audio.speech.create(
                model=model,
                voice=voice,
                input=chunks[0],
                response_format=response_format,
                speed=speed
            )
            with open(output_path, 'wb') as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)
        else:
            try:
                from pydub import AudioSegment
            except ImportError:
                print("Error: pydub required for long text. Run: pip install pydub")
                print("Also ensure ffmpeg is installed.")
                return False

            segments = []
            for i, chunk in enumerate(chunks):
                if verbose:
                    print(f"Generating chunk {i+1}/{len(chunks)}...")
                response = client.audio.speech.create(
                    model=model,
                    voice=voice,
                    input=chunk,
                    response_format='mp3',  # Always use mp3 for combining
                    speed=speed
                )
                with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as tmp:
                    for data in response.iter_bytes():
                        tmp.write(data)
                    segments.append(AudioSegment.from_mp3(tmp.name))
                    os.unlink(tmp.name)

            if verbose:
                print("Combining chunks...")
            combined = segments[0]
            for seg in segments[1:]:
                combined += seg
            combined.export(output_path, format=response_format)

        if verbose:
            size = os.path.getsize(output_path)
            print(f"Saved: {output_path} ({size:,} bytes)")

        return True

    except Exception as e:
        print(f"Error: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description='Generate speech from text using OpenAI TTS API',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  %(prog)s "Hello world" -o hello.mp3
  %(prog)s -f article.txt -o article.mp3 --voice nova
  %(prog)s "Long text..." -o output.mp3 --model tts-1-hd
  echo "Test" | %(prog)s -o test.mp3

Voices:
  alloy   - Neutral, balanced
  echo    - Male, warm, conversational
  fable   - Neutral, expressive, storytelling
  onyx    - Male, deep, authoritative (default)
  nova    - Female, friendly, upbeat
  shimmer - Female, clear, professional
        '''
    )

    parser.add_argument('text', nargs='?', help='Text to convert')
    parser.add_argument('-f', '--file', help='Read text from file')
    parser.add_argument('-o', '--output', default='output.mp3', help='Output file')
    parser.add_argument('--voice', default='onyx', choices=VOICES, help='Voice')
    parser.add_argument('--model', default='tts-1', choices=MODELS, help='Model')
    parser.add_argument('--format', default='mp3', choices=FORMATS, help='Output format')
    parser.add_argument('--speed', type=float, default=SPEED_DEFAULT,
                        help=f'Playback speed ({SPEED_MIN}-{SPEED_MAX}, default: {SPEED_DEFAULT})')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    parser.add_argument('--list-voices', action='store_true', help='List voices')

    args = parser.parse_args()

    if args.list_voices:
        print("Available voices:")
        for voice, desc in VOICE_INFO.items():
            print(f"  {voice:8} - {desc}")
        return 0

    # Validate speed
    if not (SPEED_MIN <= args.speed <= SPEED_MAX):
        print(f"Error: Speed must be between {SPEED_MIN} and {SPEED_MAX}")
        return 1

    # Get text from argument, file, or stdin
    text = None
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return 1
    elif args.text:
        text = args.text
    elif not sys.stdin.isatty():
        text = sys.stdin.read()
    else:
        print("Error: No text provided")
        parser.print_help()
        return 1

    if not text or not text.strip():
        print("Error: Empty text")
        return 1

    success = generate_tts(
        text=text.strip(),
        output_path=args.output,
        voice=args.voice,
        model=args.model,
        response_format=args.format,
        speed=args.speed,
        verbose=args.verbose
    )

    return 0 if success else 1


if __name__ == '__main__':
    sys.exit(main())
