#!/usr/bin/env python3
"""
SearXNG Search for Moltbot
Privacy-respecting metasearch via self-hosted SearXNG.

Environment:
    SEARXNG_URL  Base URL of SearXNG instance (required)

Examples:
    python3 searxng_search.py "python tutorial"
    python3 searxng_search.py "rust vs go" --count 10
    python3 searxng_search.py "berlin restaurants" --lang de
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

__version__ = "1.0.0"


def get_base_url() -> str:
    """Get and validate SEARXNG_URL from environment."""
    url = os.environ.get("SEARXNG_URL", "").strip()
    if not url:
        return ""
    # Normalize: remove trailing slash, ensure no /search suffix for base
    url = url.rstrip("/")
    if url.endswith("/search"):
        url = url[:-7]
    return url


def search(query: str, count: int = 5, lang: str = None) -> dict:
    """
    Query SearXNG and return structured results.
    
    Args:
        query: Search terms
        count: Max results (1-20)
        lang: Language code (optional)
    
    Returns:
        Dict with query, count, and results array
    """
    base_url = get_base_url()
    if not base_url:
        return {
            "error": "SEARXNG_URL not set",
            "hint": "export SEARXNG_URL=http://your-searxng:8888"
        }

    params = {"q": query, "format": "json"}
    if lang:
        params["language"] = lang

    url = f"{base_url}/search?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={
        "Accept": "application/json",
        "User-Agent": "Moltbot-SearXNG/1.0"
    })

    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        return {"error": f"HTTP {e.code}: {e.reason}", "query": query}
    except urllib.error.URLError as e:
        return {"error": f"Connection failed: {e.reason}", "query": query, "url": base_url}
    except json.JSONDecodeError:
        return {"error": "Invalid JSON from SearXNG", "query": query}
    except Exception as e:
        return {"error": str(e), "query": query}

    results = [
        {
            "title": r.get("title", ""),
            "url": r.get("url", ""),
            "description": r.get("content", ""),
            "engines": r.get("engines", []),
            "score": r.get("score", 0),
        }
        for r in data.get("results", [])[:count]
    ]

    return {"query": query, "count": len(results), "results": results}


def main():
    parser = argparse.ArgumentParser(
        description="Search via SearXNG metasearch",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="Requires SEARXNG_URL environment variable."
    )
    parser.add_argument("query", help="Search query")
    parser.add_argument("-n", "--count", type=int, default=5, metavar="N",
                        help="Number of results (default: 5, max: 20)")
    parser.add_argument("-l", "--lang", metavar="CODE",
                        help="Language code (en, de, fr, etc.)")
    parser.add_argument("-v", "--version", action="version", 
                        version=f"%(prog)s {__version__}")

    args = parser.parse_args()
    count = max(1, min(20, args.count))

    result = search(args.query, count=count, lang=args.lang)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    sys.exit(1 if "error" in result else 0)


if __name__ == "__main__":
    main()