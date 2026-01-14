#!/usr/bin/env python3
import argparse
import json
import os
import sys
from pathlib import Path


def load_gemini_key() -> str | None:
    # Prefer env var if set.
    env_key = (os.environ.get("GEMINI_API_KEY") or "").strip()
    if env_key:
        return env_key

    # Fall back to Clawdbot config (local machine).
    cfg_path = Path.home() / ".clawdbot" / "clawdbot.json"
    try:
        raw = cfg_path.read_text(encoding="utf-8")
        cfg = json.loads(raw)
        return (
            cfg.get("skills", {})
            .get("entries", {})
            .get("nano-banana-pro", {})
            .get("apiKey")
            or ""
        ).strip() or None
    except Exception:
        return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Generate a mood image via Nano Banana Pro.")
    ap.add_argument("--prompt", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--resolution", choices=["1K", "2K", "4K"], default="1K")
    args = ap.parse_args()

    api_key = load_gemini_key()
    if not api_key:
        print("Missing GEMINI_API_KEY (env or ~/.clawdbot/clawdbot.json skills.entries.nano-banana-pro.apiKey)", file=sys.stderr)
        return 2

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    from google import genai
    from google.genai import types
    from PIL import Image as PILImage
    from io import BytesIO

    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3-pro-image-preview",
        contents=args.prompt,
        config=types.GenerateContentConfig(
            response_modalities=["TEXT", "IMAGE"],
            image_config=types.ImageConfig(image_size=args.resolution),
        ),
    )

    image_saved = False
    for part in getattr(response, "parts", []) or []:
        inline = getattr(part, "inline_data", None)
        if inline is None:
            continue
        data = getattr(inline, "data", None)
        if not data:
            continue

        if isinstance(data, str):
            import base64

            data = base64.b64decode(data)

        image = PILImage.open(BytesIO(data))
        if image.mode == "RGBA":
            rgb = PILImage.new("RGB", image.size, (255, 255, 255))
            rgb.paste(image, mask=image.split()[3])
            rgb.save(str(out_path), "PNG")
        else:
            image.convert("RGB").save(str(out_path), "PNG")
        image_saved = True
        break

    if not image_saved:
        print("No image returned by model", file=sys.stderr)
        return 1

    print(out_path.as_posix())
    # Clawdbot can auto-attach files when it sees MEDIA tokens.
    print(f"MEDIA: {out_path.as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
