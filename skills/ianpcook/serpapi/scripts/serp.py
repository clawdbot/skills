#!/usr/bin/env python3
"""
SerpAPI CLI wrapper - unified search across Google, Amazon, Yelp, OpenTable, and more.

Usage:
    serp <engine> <query> [options]
    serp google "coffee shops"
    serp amazon "mechanical keyboard" --num 5
    serp yelp "pizza" --location "New York, NY"
    serp google_maps "restaurants" --location "15238"

Engines:
    google, google_maps, google_shopping, google_images, google_news,
    amazon, yelp, opentable, walmart, ebay, tripadvisor, home_depot

Environment:
    SERPAPI_API_KEY - Required API key from serpapi.com
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError


SERPAPI_BASE = "https://serpapi.com/search.json"

# Engine name mapping (CLI name -> SerpAPI engine parameter)
ENGINES = {
    # Google family
    "google": "google",
    "google_maps": "google_maps",
    "google_local": "google_local",
    "google_shopping": "google_shopping",
    "google_images": "google_images",
    "google_news": "google_news",
    "google_jobs": "google_jobs",
    "google_scholar": "google_scholar",
    "google_videos": "google_videos",
    # E-commerce
    "amazon": "amazon",
    "walmart": "walmart",
    "ebay": "ebay",
    "home_depot": "home_depot",
    # Local/Travel
    "yelp": "yelp",
    "opentable": "opentable",
    "tripadvisor": "tripadvisor",
    # Other search engines
    "bing": "bing",
    "duckduckgo": "duckduckgo",
    "yahoo": "yahoo",
}


def get_api_key() -> str:
    """Get API key from environment."""
    key = os.environ.get("SERPAPI_API_KEY")
    if not key:
        print("Error: SERPAPI_API_KEY environment variable not set", file=sys.stderr)
        sys.exit(1)
    return key


def get_default_location() -> str | None:
    """Try to read default location from TOOLS.md."""
    # Check common workspace locations
    workspace_paths = [
        Path.home() / "clawd" / "TOOLS.md",
        Path.cwd() / "TOOLS.md",
        Path(os.environ.get("CLAWDBOT_WORKSPACE", "")) / "TOOLS.md",
    ]
    
    for tools_path in workspace_paths:
        if tools_path.exists():
            try:
                content = tools_path.read_text()
                # Look for "Default location:" in SerpAPI section
                match = re.search(
                    r"##\s*SerpAPI.*?Default location:\s*(.+?)(?:\n|$)",
                    content,
                    re.IGNORECASE | re.DOTALL
                )
                if match:
                    return match.group(1).strip()
            except Exception:
                pass
    return None


def search(engine: str, query: str, **kwargs) -> dict:
    """Execute a SerpAPI search."""
    api_key = get_api_key()
    
    # Build parameters
    params = {
        "api_key": api_key,
        "engine": ENGINES.get(engine, engine),
    }
    
    # Query parameter varies by engine
    if engine in ("google_maps", "google_local"):
        params["q"] = query
    elif engine == "amazon":
        params["k"] = query
        params["amazon_domain"] = "amazon.com"
    elif engine == "yelp":
        params["find_desc"] = query
    elif engine == "opentable":
        params["restaurant"] = query
    elif engine == "walmart":
        params["query"] = query
    elif engine == "ebay":
        params["_nkw"] = query
    elif engine in ("tripadvisor",):
        params["query"] = query
    else:
        params["q"] = query
    
    # Add optional parameters
    if kwargs.get("location"):
        if engine == "yelp":
            params["find_loc"] = kwargs["location"]
        elif engine == "amazon":
            params["amazon_domain"] = "amazon.com"  # Could be extended
        elif engine in ("google_maps", "google_local"):
            # Google Maps works best with location in the query
            params["q"] = f"{query} in {kwargs['location']}"
        else:
            params["location"] = kwargs["location"]
    
    if kwargs.get("num"):
        params["num"] = kwargs["num"]
    
    if kwargs.get("type") and engine == "google":
        params["tbm"] = kwargs["type"]  # e.g., "shop", "isch", "nws"
    
    if kwargs.get("page"):
        if engine == "amazon":
            params["page"] = kwargs["page"]
        else:
            params["start"] = (int(kwargs["page"]) - 1) * int(kwargs.get("num", 10))
    
    # Additional raw parameters
    for key in ("gl", "hl", "domain", "safe", "device"):
        if kwargs.get(key):
            params[key] = kwargs[key]
    
    # Make request
    url = f"{SERPAPI_BASE}?{urlencode(params)}"
    
    try:
        req = Request(url, headers={"User-Agent": "SerpAPI-Clawdbot/1.0"})
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        error_body = e.read().decode() if e.fp else ""
        return {"error": f"HTTP {e.code}: {e.reason}", "details": error_body}
    except URLError as e:
        return {"error": f"Connection failed: {e.reason}"}
    except Exception as e:
        return {"error": str(e)}


def format_results(data: dict, engine: str) -> str:
    """Format results as human-readable text."""
    lines = []
    
    if "error" in data:
        return f"Error: {data['error']}"
    
    # Google organic results
    if "organic_results" in data:
        lines.append("=== Web Results ===")
        for r in data["organic_results"][:10]:
            lines.append(f"\n{r.get('position', '?')}. {r.get('title', 'No title')}")
            lines.append(f"   {r.get('link', '')}")
            if r.get("snippet"):
                lines.append(f"   {r['snippet'][:200]}")
    
    # Local results
    if "local_results" in data:
        places = data["local_results"]
        if isinstance(places, dict):
            places = places.get("places", [])
        lines.append("\n=== Local Results ===")
        for r in places[:10]:
            rating = f"★{r.get('rating', 'N/A')}" if r.get('rating') else ""
            price = r.get('price', '')
            lines.append(f"\n• {r.get('title', 'No name')} {rating} {price}")
            lines.append(f"  {r.get('address', '')}")
            if r.get('type'):
                lines.append(f"  Type: {r['type']}")
    
    # Shopping results
    if "shopping_results" in data:
        lines.append("\n=== Shopping Results ===")
        for r in data["shopping_results"][:10]:
            lines.append(f"\n• {r.get('title', 'No title')}")
            lines.append(f"  {r.get('price', 'No price')} - {r.get('source', '')}")
            if r.get('rating'):
                lines.append(f"  Rating: {r['rating']} ({r.get('reviews', 0)} reviews)")
    
    # Amazon results
    if "organic_results" not in data and "shopping_results" not in data:
        # Check for Amazon-style results
        if "products" in data:
            lines.append("=== Products ===")
            for r in data.get("products", [])[:10]:
                lines.append(f"\n• {r.get('title', 'No title')}")
                price = r.get('price', {})
                if isinstance(price, dict):
                    lines.append(f"  {price.get('raw', 'No price')}")
                else:
                    lines.append(f"  {price}")
                if r.get('rating'):
                    lines.append(f"  Rating: {r['rating']} ({r.get('reviews', 0)} reviews)")
    
    # Yelp results
    if "organic_results" in data and engine == "yelp":
        lines.append("=== Yelp Results ===")
        for r in data["organic_results"][:10]:
            rating = f"★{r.get('rating', 'N/A')}" if r.get('rating') else ""
            lines.append(f"\n• {r.get('title', 'No name')} {rating}")
            lines.append(f"  {r.get('neighborhoods', '')}")
            if r.get('snippet'):
                lines.append(f"  {r['snippet'][:150]}")
    
    # Knowledge graph
    if "knowledge_graph" in data:
        kg = data["knowledge_graph"]
        lines.append(f"\n=== {kg.get('title', 'Knowledge Graph')} ===")
        if kg.get("type"):
            lines.append(f"Type: {kg['type']}")
        if kg.get("description"):
            lines.append(kg["description"][:300])
    
    if not lines:
        lines.append("No results found.")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="SerpAPI search CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    parser.add_argument("engine", choices=list(ENGINES.keys()),
                        help="Search engine to use")
    parser.add_argument("query", help="Search query")
    parser.add_argument("--location", "-l", help="Location for local results")
    parser.add_argument("--num", "-n", type=int, default=10,
                        help="Number of results (default: 10)")
    parser.add_argument("--page", "-p", type=int, default=1,
                        help="Page number (default: 1)")
    parser.add_argument("--type", "-t", 
                        help="Search type for Google (shop, isch, nws, vid)")
    parser.add_argument("--format", "-f", choices=["json", "text"], default="json",
                        help="Output format (default: json)")
    parser.add_argument("--gl", help="Country code (e.g., 'us', 'uk')")
    parser.add_argument("--hl", help="Language code (e.g., 'en', 'es')")
    parser.add_argument("--raw", action="store_true",
                        help="Output raw API response")
    
    args = parser.parse_args()
    
    # Get location with fallback to default
    location = args.location
    if not location:
        location = get_default_location()
    
    # Execute search
    results = search(
        engine=args.engine,
        query=args.query,
        location=location,
        num=args.num,
        page=args.page,
        type=args.type,
        gl=args.gl,
        hl=args.hl,
    )
    
    # Output
    if args.raw or args.format == "json":
        print(json.dumps(results, indent=2))
    else:
        print(format_results(results, args.engine))


if __name__ == "__main__":
    main()
