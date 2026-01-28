#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "google-genai>=1.0.0",
#     "pillow>=10.0.0",
# ]
# ///
"""Generate videos using Google Veo 3.x via Gemini API (google-genai).

Supports multi-segment generation + automatic concatenation, with per-segment prompting and optional continuity via the previous segment's last frame.

Usage:
  uv run generate_video.py \
    --prompt "..." \
    --filename "out.mp4" \
    [--model veo-3.1-generate-preview] \
    [--aspect-ratio 16:9|9:16|1:1] \
    [--segments 1] \
    [--poll-seconds 10] \
    [--timeout-seconds 900] \
    [--api-key KEY]

Notes:
- Requires GEMINI_API_KEY if --api-key not provided.
- Veo 3.x commonly generates ~8s clips per request; use --segments to build longer videos.
- If --segments > 1, requires ffmpeg on PATH to concatenate the clips.
- Prints a MEDIA: line for Clawdbot to auto-attach on supported providers.
"""

from __future__ import annotations

import argparse
import os
import shlex
import subprocess
import sys
import time
from pathlib import Path


def get_api_key(provided_key: str | None) -> str | None:
    if provided_key:
        return provided_key
    return os.environ.get("GEMINI_API_KEY")


def require_bin(name: str) -> None:
    if subprocess.run(["bash", "-lc", f"command -v {shlex.quote(name)}"], capture_output=True).returncode != 0:
        raise RuntimeError(f"Required binary not found on PATH: {name}")


def extract_last_frame_png(video_path: Path, out_png: Path) -> Path:
    """Extract the last frame of a video to a PNG using ffmpeg."""
    require_bin("ffmpeg")
    out_png.parent.mkdir(parents=True, exist_ok=True)

    # Use -sseof to seek from the end; grab a single frame.
    cmd = [
        "ffmpeg",
        "-y",
        "-sseof",
        "-0.05",
        "-i",
        str(video_path),
        "-frames:v",
        "1",
        "-q:v",
        "2",
        str(out_png),
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"ffmpeg last-frame extract failed: {p.stderr[-2000:]}")
    return out_png


def poll_until_done(client, operation, poll_seconds: int, timeout_seconds: int):
    started = time.time()
    while not getattr(operation, "done", False):
        elapsed = int(time.time() - started)
        if elapsed > timeout_seconds:
            raise TimeoutError(f"Timed out after {timeout_seconds}s waiting for video generation")
        print("Waiting for video generation to complete…")
        time.sleep(poll_seconds)
        operation = client.operations.get(operation)
    return operation


def extract_first_video_handle(client, operation, wait_seconds: int = 60, poll_seconds: int = 5):
    """Extract the first video handle from a finished operation.

    In practice, some operations may flip to done=True before the response payload is
    populated (eventual consistency). We retry `operations.get()` briefly. Also surface
    operation.error when present.
    """

    deadline = time.time() + wait_seconds
    while True:
        # Surface explicit operation error if present.
        op_err = getattr(operation, "error", None) or getattr(operation, "Error", None)
        if op_err:
            raise RuntimeError(f"Operation error: {op_err}")

        resp = getattr(operation, "response", None) or getattr(operation, "Response", None)
        if resp is not None:
            break

        if time.time() >= deadline:
            raise RuntimeError("Operation finished but no response found")

        # Retry fetch
        time.sleep(poll_seconds)
        try:
            operation = client.operations.get(operation)
        except Exception:
            # If polling fails intermittently, keep trying until deadline.
            pass

    vids = (
        getattr(resp, "generated_videos", None)
        or getattr(resp, "generatedVideos", None)
        or getattr(resp, "GeneratedVideos", None)
    )
    if not vids:
        raise RuntimeError(f"No generated_videos in response (resp={type(resp).__name__})")

    first = vids[0]
    video_file = getattr(first, "video", None)
    if video_file is None:
        raise RuntimeError("generated video file handle missing")

    return video_file


def save_video_file(client, video_file, out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Some SDK variants need an explicit download call before save().
    try:
        client.files.download(file=video_file)
    except Exception:
        pass

    video_file.save(str(out_path))


def ffmpeg_concat(inputs: list[Path], out_path: Path) -> None:
    require_bin("ffmpeg")
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Create concat list file.
    lst = out_path.with_suffix(out_path.suffix + ".concat.txt")
    lines = [f"file '{p.as_posix()}'" for p in inputs]
    lst.write_text("\n".join(lines) + "\n", encoding="utf-8")

    cmd = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(lst),
        "-c",
        "copy",
        str(out_path),
    ]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        # Fallback: re-encode (more compatible, slower)
        print("ffmpeg stream copy concat failed; falling back to re-encode…", file=sys.stderr)
        cmd2 = [
            "ffmpeg",
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            str(lst),
            "-c:v",
            "libx264",
            "-preset",
            "veryfast",
            "-crf",
            "18",
            "-c:a",
            "aac",
            "-b:a",
            "192k",
            str(out_path),
        ]
        p2 = subprocess.run(cmd2, capture_output=True, text=True)
        if p2.returncode != 0:
            raise RuntimeError(
                "ffmpeg concat failed.\n"
                f"copy stderr:\n{p.stderr[-2000:]}\n\n"
                f"reencode stderr:\n{p2.stderr[-2000:]}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate videos via Veo 3.x (Gemini API)")
    parser.add_argument("--prompt", "-p", required=False, help="Text prompt (used for all segments unless --segment-prompt is provided)")
    parser.add_argument(
        "--segment-prompt",
        action="append",
        default=[],
        help="Per-segment prompt. Repeat this flag for each segment (e.g. 3 times). Overrides --prompt.",
    )
    parser.add_argument("--filename", "-f", required=True, help="Output .mp4 path")
    parser.add_argument(
        "--model",
        "-m",
        default="veo-3.1-generate-preview",
        help="Model id (e.g., veo-3.1-generate-preview)",
    )
    parser.add_argument(
        "--aspect-ratio",
        default=None,
        choices=["16:9", "9:16", "1:1"],
        help="Optional aspect ratio (if supported by the model/config)",
    )
    parser.add_argument(
        "--segments",
        type=int,
        default=1,
        help="Number of segments to generate and concatenate (use for longer videos)",
    )
    parser.add_argument(
        "--reference-image",
        action="append",
        default=[],
        help="Path to a reference image to guide generation (repeatable).",
    )
    parser.add_argument(
        "--reference-type",
        default="asset",
        choices=["asset", "style", "subject"],
        help="Reference type hint passed to the API (default: asset).",
    )
    parser.add_argument(
        "--generate-audio",
        default=True,
        action=argparse.BooleanOptionalAction,
        help="Whether to generate audio (default: true).",
    )
    parser.add_argument(
        "--base-style",
        default=None,
        help="Style/system prompt prepended to every segment prompt (recommended for consistency).",
    )
    parser.add_argument(
        "--segment-style",
        choices=["same", "continuation"],
        default="continuation",
        help="How to prompt segments: same prompt each time, or continuation prompts.",
    )
    parser.add_argument(
        "--use-last-frame",
        action="store_true",
        help="For segment >=2 (single run), extract the previous segment's last frame and pass it as lastFrame to encourage continuity.",
    )
    parser.add_argument(
        "--last-frame-image",
        default=None,
        help="Explicit last frame image path to pass as lastFrame (useful when running segments as separate commands).",
    )
    parser.add_argument(
        "--emit-segment-media",
        action="store_true",
        help="Print MEDIA: lines for each segment as they finish (useful for progress updates).",
    )
    parser.add_argument(
        "--poll-seconds",
        type=int,
        default=10,
        help="Polling interval seconds",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=900,
        help="Max time to wait for each segment generation to finish",
    )
    parser.add_argument(
        "--api-key",
        "-k",
        help="API key (overrides GEMINI_API_KEY)",
    )
    parser.add_argument(
        "--keep-segments",
        action="store_true",
        help="Keep intermediate segment mp4 files",
    )

    args = parser.parse_args()

    api_key = get_api_key(args.api_key)
    if not api_key:
        print("Error: No API key provided.", file=sys.stderr)
        print("Set GEMINI_API_KEY or pass --api-key", file=sys.stderr)
        sys.exit(1)

    if args.segments < 1:
        print("Error: --segments must be >= 1", file=sys.stderr)
        sys.exit(1)

    # Determine per-segment prompts
    seg_prompts: list[str] = []
    if args.segment_prompt:
        seg_prompts = [p for p in args.segment_prompt if p and p.strip()]
        if not seg_prompts:
            print("Error: --segment-prompt provided but empty", file=sys.stderr)
            sys.exit(1)
        if args.segments != 1 and args.segments != len(seg_prompts):
            print(
                f"Error: --segments ({args.segments}) does not match number of --segment-prompt ({len(seg_prompts)})",
                file=sys.stderr,
            )
            sys.exit(1)
        args.segments = len(seg_prompts)
    else:
        if not args.prompt or not args.prompt.strip():
            print("Error: provide --prompt or one/more --segment-prompt", file=sys.stderr)
            sys.exit(1)
        seg_prompts = [args.prompt]

    # Lazy import after validation
    from google import genai
    from google.genai import types
    import mimetypes

    client = genai.Client(api_key=api_key)

    out = Path(args.filename)
    out.parent.mkdir(parents=True, exist_ok=True)

    reference_images = []
    for p in args.reference_image or []:
        try:
            img_path = Path(p)
            b = img_path.read_bytes()
            mt, _ = mimetypes.guess_type(str(img_path))
            mt = mt or "image/jpeg"
            img = types.Image(imageBytes=b, mimeType=mt)
        except Exception as e:
            print(f"Error loading reference image {p}: {e}", file=sys.stderr)
            sys.exit(1)
        reference_images.append(
            types.VideoGenerationReferenceImage(
                image=img,
                referenceType=args.reference_type,
            )
        )

    # Build base config (use canonical field names)
    base_cfg_kwargs = {}
    if args.aspect_ratio:
        base_cfg_kwargs["aspectRatio"] = args.aspect_ratio
    if reference_images:
        base_cfg_kwargs["referenceImages"] = reference_images

    # Optional explicit lastFrame image
    if args.last_frame_image:
        import mimetypes

        p = Path(args.last_frame_image)
        b = p.read_bytes()
        mt, _ = mimetypes.guess_type(str(p))
        mt = mt or "image/png"
        base_cfg_kwargs["lastFrame"] = types.Image(imageBytes=b, mimeType=mt)

        # Empirically, some Veo requests reject combining lastFrame + referenceImages.
        # To maximize compatibility, drop referenceImages when lastFrame is provided.
        if "referenceImages" in base_cfg_kwargs:
            print(
                "Note: lastFrame provided; dropping referenceImages for compatibility.",
                file=sys.stderr,
            )
            base_cfg_kwargs.pop("referenceImages", None)

    # Note: As of google-genai SDK 1.60.0, generate_audio is NOT supported on the Gemini API
    # for Veo video generation (SDK raises ValueError). We keep the CLI flag for forward-compat,
    # but do not send it today.
    if args.generate_audio is not None and args.generate_audio is not True:
        print("Note: --no-generate-audio requested, but Gemini API does not currently support the generateAudio flag; proceeding.")

    seg_paths: list[Path] = []
    base = out.with_suffix("")

    for i in range(1, args.segments + 1):
        # Segment prompt strategy:
        # - Always send exactly ONE segment prompt per Veo request.
        # - If --segment-prompt is provided, use that prompt for this segment.
        # - Otherwise, use --prompt for all segments and optionally append continuation guidance.
        raw_seg_prompt = seg_prompts[min(i - 1, len(seg_prompts) - 1)]
        if not args.segment_prompt and args.segments > 1 and args.segment_style != "same":
            raw_seg_prompt = raw_seg_prompt + (
                f"\n\nThis is segment {i} of {args.segments}. Continue seamlessly from the previous segment with consistent characters, lighting, camera style, and setting."
            )

        if args.base_style:
            seg_prompt = args.base_style.strip() + "\n\n" + raw_seg_prompt.strip()
        else:
            seg_prompt = raw_seg_prompt.strip()

        seg_out = base.parent / f"{base.name}.seg{i:02d}.mp4"

        # Build per-segment config, optionally with lastFrame.
        seg_cfg_kwargs = dict(base_cfg_kwargs)
        if args.use_last_frame and i >= 2:
            try:
                last_png = base.parent / f"{base.name}.seg{i-1:02d}.last.png"
                extract_last_frame_png(seg_paths[-1], last_png)
                b = last_png.read_bytes()
                import mimetypes

                mt, _ = mimetypes.guess_type(str(last_png))
                mt = mt or "image/png"
                seg_cfg_kwargs["lastFrame"] = types.Image(imageBytes=b, mimeType=mt)

                # Empirically, some Veo requests reject combining lastFrame + referenceImages.
                # Drop referenceImages for segment>=2 to improve success rate.
                seg_cfg_kwargs.pop("referenceImages", None)
            except Exception as e:
                print(f"Warning: failed to attach lastFrame for segment {i}: {e}", file=sys.stderr)

        seg_config = types.GenerateVideosConfig(**seg_cfg_kwargs) if seg_cfg_kwargs else None

        print(f"Starting video generation segment {i}/{args.segments} (model={args.model})…")
        operation = client.models.generate_videos(
            model=args.model,
            prompt=seg_prompt,
            config=seg_config,
        )

        try:
            operation = poll_until_done(client, operation, args.poll_seconds, args.timeout_seconds)
        except Exception as e:
            print(f"Error while waiting for segment {i}: {e}", file=sys.stderr)
            sys.exit(2)

        try:
            video_file = extract_first_video_handle(client, operation)
            save_video_file(client, video_file, seg_out)
        except Exception as e:
            print(f"Error downloading/saving segment {i}: {e}", file=sys.stderr)
            sys.exit(3)

        seg_full = seg_out.resolve()
        print(f"Saved segment {i}: {seg_full}")
        if args.emit_segment_media:
            print(f"MEDIA: {seg_full}")
        seg_paths.append(seg_out)

    if args.segments == 1:
        # Rename seg file to requested filename
        seg_paths[0].replace(out)
        full = out.resolve()
        print(f"Generated video saved: {full}")
        print(f"MEDIA: {full}")
        return

    # Concatenate segments
    try:
        ffmpeg_concat(seg_paths, out)
    except Exception as e:
        print(f"Error concatenating segments: {e}", file=sys.stderr)
        sys.exit(4)

    full = out.resolve()
    print(f"Generated stitched video saved: {full}")
    print(f"MEDIA: {full}")

    if not args.keep_segments:
        for p in seg_paths:
            try:
                p.unlink(missing_ok=True)
            except Exception:
                pass


if __name__ == "__main__":
    main()
