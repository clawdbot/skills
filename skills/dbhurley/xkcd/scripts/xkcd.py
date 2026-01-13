#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["httpx"]
# ///
"""
xkcd comic fetcher - latest, random, specific, or search.
"""

import argparse
import json
import random
import sys
from datetime import date

import httpx

BASE_URL = "https://xkcd.com"
TIMEOUT = 10


def fetch_comic(num: int | None = None) -> dict:
    """Fetch a specific comic or latest if num is None."""
    if num:
        url = f"{BASE_URL}/{num}/info.0.json"
    else:
        url = f"{BASE_URL}/info.0.json"
    
    resp = httpx.get(url, timeout=TIMEOUT, follow_redirects=True)
    resp.raise_for_status()
    data = resp.json()
    
    return {
        "num": data["num"],
        "title": data["title"],
        "alt": data["alt"],
        "img": data["img"],
        "url": f"{BASE_URL}/{data['num']}/",
        "date": f"{data['year']}-{data['month'].zfill(2)}-{data['day'].zfill(2)}",
    }


def fetch_random() -> dict:
    """Fetch a random comic."""
    # First get latest to know the range
    latest = fetch_comic()
    max_num = latest["num"]
    # Pick random (skip #404 which doesn't exist as a joke)
    num = random.randint(1, max_num)
    while num == 404:
        num = random.randint(1, max_num)
    return fetch_comic(num)


def search_comics(query: str, limit: int = 5) -> list[dict]:
    """
    Search comics by keyword in title/alt text.
    Uses concurrent requests to search recent comics quickly.
    """
    import concurrent.futures
    
    query_lower = query.lower()
    latest = fetch_comic()
    max_num = latest["num"]
    
    def check_comic(num: int) -> dict | None:
        if num == 404:
            return None
        try:
            comic = fetch_comic(num)
            if query_lower in comic["title"].lower() or query_lower in comic["alt"].lower():
                return comic
        except Exception:
            pass
        return None
    
    results = []
    # Search last 200 comics concurrently in batches
    search_range = list(range(max_num, max(1, max_num - 200), -1))
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(check_comic, num): num for num in search_range}
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                results.append(result)
                if len(results) >= limit:
                    executor.shutdown(wait=False, cancel_futures=True)
                    break
    
    # Sort by comic number descending
    results.sort(key=lambda x: x["num"], reverse=True)
    return results[:limit]


def format_markdown(comic: dict) -> str:
    """Format comic as markdown."""
    return f"""**xkcd #{comic['num']}: {comic['title']}**

![{comic['title']}]({comic['img']})

> {comic['alt']}

🔗 {comic['url']}"""


def main():
    parser = argparse.ArgumentParser(description="Fetch xkcd comics")
    parser.add_argument("number", nargs="?", type=int, help="Comic number (omit for latest)")
    parser.add_argument("--random", "-r", action="store_true", help="Fetch random comic")
    parser.add_argument("--search", "-s", type=str, help="Search comics by keyword")
    parser.add_argument("--limit", "-l", type=int, default=5, help="Max search results")
    parser.add_argument("--format", "-f", choices=["markdown", "json"], default="markdown")
    
    args = parser.parse_args()
    
    try:
        if args.search:
            comics = search_comics(args.search, args.limit)
            if not comics:
                print(f"No comics found matching '{args.search}'", file=sys.stderr)
                sys.exit(1)
            if args.format == "json":
                print(json.dumps(comics, indent=2))
            else:
                for comic in comics:
                    print(format_markdown(comic))
                    print("\n---\n")
        elif args.random:
            comic = fetch_random()
            if args.format == "json":
                print(json.dumps(comic, indent=2))
            else:
                print(format_markdown(comic))
        else:
            comic = fetch_comic(args.number)
            if args.format == "json":
                print(json.dumps(comic, indent=2))
            else:
                print(format_markdown(comic))
    except httpx.HTTPStatusError as e:
        print(f"Error fetching comic: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
