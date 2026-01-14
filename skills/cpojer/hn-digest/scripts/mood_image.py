#!/usr/bin/env python3
import argparse
import base64
import json
import os
import sys
import urllib.request
from pathlib import Path


def request_image(api_key: str, prompt: str, model: str, size: str, quality: str) -> dict:
    url = "https://api.openai.com/v1/images/generations"
    body = json.dumps(
        {
            "model": model,
            "prompt": prompt,
            "size": size,
            "quality": quality,
            "n": 1,
        }
    ).encode("utf-8")

    req = urllib.request.Request(
        url,
        method="POST",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        data=body,
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        try:
            payload = e.read().decode("utf-8")
        except Exception:
            payload = ""
        raise RuntimeError(
            f"Images API failed ({e.code} {e.reason})" + (f": {payload}" if payload else "")
        ) from e


def write_png_from_response(out_path: Path, res: dict) -> None:
    data0 = (res.get("data") or [{}])[0] or {}

    b64 = data0.get("b64_json")
    if isinstance(b64, str) and b64:
        out_path.write_bytes(base64.b64decode(b64))
        return

    url = data0.get("url")
    if isinstance(url, str) and url:
        with urllib.request.urlopen(url, timeout=300) as resp:
            out_path.write_bytes(resp.read())
        return

    raise RuntimeError(f"Unexpected Images API response: {json.dumps(res)[:500]}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate one mood image for hn-digest.")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--model", default="gpt-image-1")
    ap.add_argument("--size", default="1024x1024")
    ap.add_argument("--quality", default="high")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    api_key = (os.environ.get("OPENAI_API_KEY") or "").strip()
    if not api_key:
        print("Missing OPENAI_API_KEY", file=sys.stderr)
        return 2

    out_path = Path(args.out).expanduser()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    res = request_image(api_key, args.prompt, args.model, args.size, args.quality)
    write_png_from_response(out_path, res)

    print(out_path.as_posix())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
