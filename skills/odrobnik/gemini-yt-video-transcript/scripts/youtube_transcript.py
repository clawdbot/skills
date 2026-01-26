#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

# Gemini model used for transcript generation.
GEMINI_MODEL = "gemini-3-pro-preview"
API_ENDPOINT = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

PROMPT = (
    "Create a clean verbatim transcript for the YouTube video at the URL below. "
    "Use the video content directly (do not request captions). "
    "Identify speakers when clearly implied by the text; otherwise use a generic label like 'Speaker'. "
    "Use reasonable paragraph breaks. "
    "NO time codes. "
    "Output ONLY transcript lines in the form: Speaker: text. "
    "No extra info, no headings, no lists."
)


def eprint(*args: object) -> None:
    print(*args, file=sys.stderr)


def gemini_generate(api_key: str, parts: list[dict]) -> str:
    payload = {
        "contents": [{"role": "user", "parts": parts}],
        "generationConfig": {"temperature": 0.2},
    }

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        API_ENDPOINT,
        data=data,
        headers={
            "Content-Type": "application/json",
            "x-goog-api-key": api_key,
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=900) as resp:
            raw = resp.read().decode("utf-8")
    except urllib.error.HTTPError as ex:
        body = ex.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Gemini API error: HTTP {ex.code}\n{body}")

    obj = json.loads(raw)
    candidates = obj.get("candidates") or []
    if not candidates:
        raise RuntimeError(f"No candidates in response: {raw}")

    content = candidates[0].get("content") or {}
    out_parts = content.get("parts") or []
    text_chunks = [p.get("text", "") for p in out_parts if isinstance(p, dict)]
    text = "".join(text_chunks).strip()
    if not text:
        raise RuntimeError(f"Empty response text: {raw}")
    return text


def fetch_youtube_title_oembed(url: str) -> str | None:
    """Get title without downloading anything."""
    try:
        oembed = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(url, safe="")
        req = urllib.request.Request(oembed, method="GET")
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            title = (data.get("title") or "").strip()
            return title or None
    except Exception:
        return None


def safe_slug(s: str, max_len: int = 60) -> str:
    keep: list[str] = []
    for ch in s:
        if ch.isalnum():
            keep.append(ch.lower())
        elif ch in (" ", "-", "_", "."):
            keep.append("-")
    slug = "".join(keep)
    while "--" in slug:
        slug = slug.replace("--", "-")
    slug = slug.strip("-")
    if not slug:
        slug = "video"
    if len(slug) > max_len:
        slug = slug[:max_len].rstrip("-")
    return slug


def suggest_filename_stem(api_key: str, title: str) -> str | None:
    prompt = (
        "Suggest a short, filesystem-safe filename stem for a transcript file based on this title. "
        "Rules: output ONLY the filename stem, no extension, no quotes, no extra words. "
        "Use lowercase ASCII with hyphens, max 40 characters.\n\n"
        f"Title: {title}"
    )
    try:
        text = gemini_generate(api_key, [{"text": prompt}])
    except Exception:
        return None

    stem = text.strip().splitlines()[0].strip()
    stem = safe_slug(stem, max_len=40)
    return stem or None


def default_out_dir() -> Path:
    """Default output directory: the workspace 'out/' (outside the skills folder)."""
    here = Path(__file__).resolve()
    for p in here.parents:
        if p.name == "skills":
            return p.parent / "out"
    return Path.cwd() / "out"


def main() -> int:
    ap = argparse.ArgumentParser(
        prog="youtube_transcript",
        description="Verbatim transcript for a YouTube URL using Gemini 3 Pro.",
    )
    ap.add_argument("url", help="YouTube URL")
    ap.add_argument("--out", help="Write transcript to this file (default: auto-named in workspace out/)"
    )
    args = ap.parse_args()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        eprint("Missing GEMINI_API_KEY environment variable")
        eprint("Get a key from https://aistudio.google.com/apikey")
        return 2

    url = args.url
    title = fetch_youtube_title_oembed(url)

    out_path: Path
    if args.out:
        out_path = Path(args.out)
    else:
        stem: str | None = None
        if title:
            stem = suggest_filename_stem(api_key, title)
        if not stem:
            stem = safe_slug(title or "transcript", max_len=40) or "transcript"
        out_path = default_out_dir() / f"{stem}.txt"

    out_path.parent.mkdir(parents=True, exist_ok=True)

    parts = [
        {"text": PROMPT},
        # Key trick: pass the YouTube URL as a "file" so Gemini can ingest the video directly.
        {"file_data": {"file_uri": url}},
    ]

    transcript = gemini_generate(api_key, parts)

    header = title or "Transcript"
    out_path.write_text(header + "\n\n" + transcript.strip() + "\n", encoding="utf-8")
    print(str(out_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
