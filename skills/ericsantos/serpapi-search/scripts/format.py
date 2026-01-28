#!/usr/bin/env python3
"""Format SerpAPI JSON results into readable text."""
import json, sys

if len(sys.argv) < 3:
    print("Usage: format.py <json_file> <engine>", file=sys.stderr)
    sys.exit(1)

with open(sys.argv[1]) as f:
    data = json.load(f)

engine = sys.argv[2]

if engine == "google":
    results = data.get("organic_results", [])
    if not results:
        print("No results found.")
        sys.exit(0)
    for i, r in enumerate(results):
        print(f"{i+1}. {r.get('title', 'No title')}")
        print(f"   {r.get('link', '')}")
        snippet = r.get("snippet", "")
        if snippet:
            print(f"   {snippet}")
        print()

elif engine == "google_news":
    results = data.get("news_results", [])
    if not results:
        print("No news results found.")
        sys.exit(0)
    for i, r in enumerate(results):
        print(f"{i+1}. {r.get('title', 'No title')}")
        source = r.get("source", {})
        src_name = source.get("name", "") if isinstance(source, dict) else str(source)
        date = r.get("date", "")
        if src_name or date:
            print(f"   {src_name} · {date}")
        link = r.get("link", "")
        if link:
            print(f"   {link}")
        print()

elif engine == "google_local":
    results = data.get("local_results", [])
    if not results:
        print("No local results found.")
        sys.exit(0)
    for i, r in enumerate(results):
        print(f"{i+1}. {r.get('title', 'No title')}")
        rating = r.get("rating", "")
        reviews = r.get("reviews", "")
        if rating:
            print(f"   ★ {rating} ({reviews} reviews)")
        address = r.get("address", "")
        if address:
            print(f"   {address}")
        phone = r.get("phone", "")
        if phone:
            print(f"   {phone}")
        print()
else:
    print(json.dumps(data, indent=2, ensure_ascii=False))
