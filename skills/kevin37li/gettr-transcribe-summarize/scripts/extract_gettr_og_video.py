#!/usr/bin/env python3
"""Extract a GETTR post's media URL from HTML og:video meta tags.

Usage:
  python3 extract_gettr_og_video.py <gettr_post_url>

Prints the best candidate URL to stdout.

Implementation notes:
- Uses only stdlib.
- Looks for (in order): og:video:secure_url, og:video:url, og:video
"""

from __future__ import annotations

import html
import re
import sys
import urllib.request

META_RE = re.compile(
    r"<meta\s+[^>]*?(?:property|name)\s*=\s*['\"](?P<key>og:video(?::secure_url|:url)?)['\"][^>]*?>",
    re.IGNORECASE,
)
CONTENT_RE = re.compile(r"content\s*=\s*['\"](?P<val>[^'\"]+)['\"]", re.IGNORECASE)

PREF_ORDER = ["og:video:secure_url", "og:video:url", "og:video"]


def fetch(url: str) -> str:
    req = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X) AppleWebKit/537.36 (KHTML, like Gecko) Chrome Safari"
        },
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    # Best effort decode
    for enc in ("utf-8", "utf-8-sig", "latin-1"):
        try:
            return data.decode(enc)
        except Exception:
            pass
    return data.decode("utf-8", errors="replace")


def extract(html_text: str) -> dict[str, str]:
    found: dict[str, str] = {}
    for m in META_RE.finditer(html_text):
        tag = m.group(0)
        key = m.group("key").lower()
        cm = CONTENT_RE.search(tag)
        if not cm:
            continue
        val = html.unescape(cm.group("val")).strip()
        if val and key not in found:
            found[key] = val
    return found


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("Usage: extract_gettr_og_video.py <gettr_post_url>", file=sys.stderr)
        return 2

    url = argv[1]
    if not (url.startswith("http://") or url.startswith("https://")):
        print("URL must start with http:// or https://", file=sys.stderr)
        return 2

    html_text = fetch(url)
    found = extract(html_text)

    for key in PREF_ORDER:
        v = found.get(key)
        if v:
            print(v)
            return 0

    print("No og:video meta tag found.", file=sys.stderr)
    # Helpful debug: show what we did find
    if found:
        print("Found keys: " + ", ".join(sorted(found.keys())), file=sys.stderr)
    return 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
