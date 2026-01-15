#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
# ]
# ///
"""
Generate videos using Google's Veo API.

Usage:
    uv run generate_video.py --prompt "your video description" --filename "output.mp4" [--duration 8] [--aspect-ratio 16:9] [--model MODEL]
"""

import argparse
import os
import sys
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(
        description="Generate video using Google Veo API"
    )
    parser.add_argument(
        "--prompt", "-p",
        required=True,
        help="Video description/prompt"
    )
    parser.add_argument(
        "--filename", "-f",
        required=True,
        help="Output filename (e.g., output.mp4)"
    )
    parser.add_argument(
        "--duration", "-d",
        type=int,
        default=8,
        help="Video duration in seconds (default: 8)"
    )
    parser.add_argument(
        "--aspect-ratio", "-a",
        choices=["16:9", "9:16", "1:1"],
        default="16:9",
        help="Aspect ratio (default: 16:9)"
    )
    parser.add_argument(
        "--model", "-m",
        default="veo-3.1-generate-preview",
        help="Veo model to use (default: veo-3.1-generate-preview)"
    )

    args = parser.parse_args()

    # Import after parsing to fail fast if google-genai isn't installed
    from google import genai
    from google.genai import types

    # Initialize client (relies on GEMINI_API_KEY env var)
    client = genai.Client()

    # Set up output path
    output_path = Path(args.filename)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    print(f"Generating video with model {args.model}...")
    print(f"  Prompt: {args.prompt}")
    print(f"  Duration: {args.duration}s")
    print(f"  Aspect ratio: {args.aspect_ratio}")

    try:
        # Start the video generation
        operation = client.models.generate_videos(
            model=args.model,
            prompt=args.prompt,
            config=types.GenerateVideosConfig(
                duration_seconds=args.duration,
                aspect_ratio=args.aspect_ratio,
            )
        )

        print(f"Operation started: {operation.name}")

        # Poll until done
        while not operation.done:
            print("Waiting for video generation to complete...")
            time.sleep(10)
            # Refresh operation state
            operation = client.operations.get(operation)

        print("Video generation complete!")

        # Get the generated video
        generated_video = operation.response.generated_videos[0]

        # Download the video
        print(f"Downloading video...")
        client.files.download(file=generated_video.video)
        generated_video.video.save(str(output_path))

        # Verify and report
        if output_path.exists():
            size_mb = output_path.stat().st_size / (1024 * 1024)
            print(f"\nVideo saved: {output_path} ({size_mb:.2f} MB)")
            print(f"MEDIA: {output_path}")
        else:
            print("Error: Video file was not saved.", file=sys.stderr)
            sys.exit(1)

    except Exception as e:
        print(f"Error generating video: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
