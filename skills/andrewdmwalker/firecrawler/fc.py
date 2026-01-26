#!/usr/bin/env python3
"""Firecrawl web skill for Clawdbot.

Features:
- markdown: Scrape URL to clean markdown
- screenshot: Capture webpage screenshot
- extract: Extract structured data with JSON schema
- search: Search the web
- crawl: Crawl documentation sites
- map: Discover URLs on a site
"""

import argparse
import base64
import json
import os
import sys
import urllib.request
from pathlib import Path

try:
    from firecrawl import Firecrawl
except ImportError:
    print("Error: firecrawl not installed. Run: pip3 install firecrawl", file=sys.stderr)
    sys.exit(1)


def get_client():
    """Initialize Firecrawl client."""
    api_key = os.environ.get("FIRECRAWL_API_KEY")
    if not api_key:
        print("Error: FIRECRAWL_API_KEY environment variable not set", file=sys.stderr)
        print("Get your key at: https://www.firecrawl.dev/app/api-keys", file=sys.stderr)
        sys.exit(1)
    return Firecrawl(api_key=api_key)


def cmd_markdown(args):
    """Scrape a URL and return markdown content."""
    app = get_client()
    result = app.scrape(
        args.url,
        formats=["markdown"],
        only_main_content=args.main_only
    )
    if result and hasattr(result, 'markdown') and result.markdown:
        print(result.markdown)
    elif isinstance(result, dict) and "markdown" in result:
        print(result["markdown"])
    else:
        print(f"Error: Could not scrape {args.url}", file=sys.stderr)
        print(f"Result: {result}", file=sys.stderr)
        sys.exit(1)


def cmd_screenshot(args):
    """Take a screenshot of a URL."""
    app = get_client()
    result = app.scrape(
        args.url,
        formats=["screenshot"]
    )
    
    screenshot_data = None
    if hasattr(result, 'screenshot'):
        screenshot_data = result.screenshot
    elif isinstance(result, dict) and "screenshot" in result:
        screenshot_data = result["screenshot"]
    
    if not screenshot_data:
        print(f"Error: Could not screenshot {args.url}", file=sys.stderr)
        sys.exit(1)
    
    # Handle URL response (Firecrawl returns hosted URL)
    if screenshot_data.startswith("http://") or screenshot_data.startswith("https://"):
        if args.output:
            urllib.request.urlretrieve(screenshot_data, args.output)
            print(f"Screenshot saved to {args.output}")
        else:
            print(f"Screenshot URL: {screenshot_data}")
        return
    
    # Handle base64 data URI response (fallback)
    if screenshot_data.startswith("data:image"):
        screenshot_data = screenshot_data.split(",", 1)[1]
    
    if args.output:
        with open(args.output, "wb") as f:
            f.write(base64.b64decode(screenshot_data))
        print(f"Screenshot saved to {args.output}")
    else:
        print(f"[Screenshot: {len(screenshot_data)} bytes base64]")


def cmd_extract(args):
    """Extract structured data from a URL using a schema."""
    app = get_client()
    
    with open(args.schema) as f:
        schema = json.load(f)
    
    result = app.scrape(
        args.url,
        formats=["extract"],
        extract={"schema": schema, "prompt": args.prompt} if args.prompt else {"schema": schema}
    )
    
    extract_data = None
    if hasattr(result, 'extract'):
        extract_data = result.extract
    elif isinstance(result, dict) and "extract" in result:
        extract_data = result["extract"]
    
    if extract_data:
        print(json.dumps(extract_data, indent=2))
    else:
        print(f"Error: Could not extract data from {args.url}", file=sys.stderr)
        sys.exit(1)


def cmd_search(args):
    """Search the web and return results."""
    app = get_client()
    results = app.search(args.query, limit=args.limit)
    
    # Handle different response formats
    data = []
    if hasattr(results, 'data'):
        data = results.data
    elif isinstance(results, dict) and "data" in results:
        data = results["data"]
    elif isinstance(results, list):
        data = results
    
    if not data:
        print(f"No results found for: {args.query}", file=sys.stderr)
        return
    
    for r in data:
        if hasattr(r, 'title'):
            print(f"## {r.title}")
            print(f"URL: {r.url}")
            if r.description:
                print(r.description)
            if hasattr(r, 'markdown') and r.markdown:
                print(f"\n{r.markdown[:2000]}...")
        else:
            print(f"## {r.get('title', 'Untitled')}")
            print(f"URL: {r.get('url', 'N/A')}")
            if r.get("description"):
                print(r["description"])
            if r.get("markdown"):
                print(f"\n{r['markdown'][:2000]}...")
        print("\n---\n")


def cmd_crawl(args):
    """Crawl a documentation site."""
    app = get_client()
    
    print(f"Crawling {args.url} (limit: {args.limit} pages)...", file=sys.stderr)
    
    result = app.crawl(
        args.url,
        limit=args.limit,
        scrape_options={
            "formats": ["markdown"],
            "onlyMainContent": True
        }
    )
    
    # Handle different response formats
    pages = []
    if hasattr(result, 'data'):
        pages = result.data
    elif isinstance(result, dict) and "data" in result:
        pages = result["data"]
    elif isinstance(result, list):
        pages = result
    
    if not pages:
        print(f"Error: Could not crawl {args.url}", file=sys.stderr)
        sys.exit(1)
    
    if args.output:
        Path(args.output).mkdir(parents=True, exist_ok=True)
        for i, page in enumerate(pages):
            # Get metadata
            if hasattr(page, 'metadata'):
                meta = page.metadata
                url = meta.sourceURL if hasattr(meta, 'sourceURL') else str(i)
                title = meta.title if hasattr(meta, 'title') else "Untitled"
            elif isinstance(page, dict):
                meta = page.get("metadata", {})
                url = meta.get("sourceURL", str(i))
                title = meta.get("title", "Untitled")
            else:
                url = str(i)
                title = "Untitled"
            
            # Create filename from URL
            slug = url.split("/")[-1] or f"page_{i}"
            slug = "".join(c if c.isalnum() or c in "-_" else "_" for c in slug)
            filename = f"{args.output}/{i:03d}_{slug[:50]}.md"
            
            # Get content
            content = page.markdown if hasattr(page, 'markdown') else page.get("markdown", "")
            
            with open(filename, "w") as f:
                f.write(f"# {title}\n\n")
                f.write(f"Source: {url}\n\n---\n\n")
                f.write(content or "")
        
        print(f"Saved {len(pages)} pages to {args.output}/")
    else:
        for page in pages:
            if hasattr(page, 'metadata'):
                title = page.metadata.title if hasattr(page.metadata, 'title') else "Untitled"
                url = page.metadata.sourceURL if hasattr(page.metadata, 'sourceURL') else ""
                content = page.markdown if hasattr(page, 'markdown') else ""
            else:
                title = page.get("metadata", {}).get("title", "Untitled")
                url = page.get("metadata", {}).get("sourceURL", "")
                content = page.get("markdown", "")
            
            print(f"## {title}")
            print(f"URL: {url}")
            print((content or "")[:1000])
            print("\n---\n")
        
        print(f"\nTotal: {len(pages)} pages crawled")


def cmd_map(args):
    """Map a website to discover URLs."""
    app = get_client()
    
    result = app.map(
        args.url,
        search=args.search,
        limit=args.limit
    )
    
    # Handle different response formats
    links = []
    if hasattr(result, 'links'):
        links = result.links
    elif isinstance(result, dict) and "links" in result:
        links = result["links"]
    elif isinstance(result, list):
        links = result
    
    if not links:
        print(f"Error: Could not map {args.url}", file=sys.stderr)
        sys.exit(1)
    
    print(f"Found {len(links)} URLs:\n")
    for link in links:
        print(link)


def main():
    parser = argparse.ArgumentParser(
        description="Firecrawl web tools for Clawdbot",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  fc.py markdown "https://example.com"
  fc.py screenshot "https://example.com" -o shot.png
  fc.py search "Python async best practices"
  fc.py crawl "https://docs.astro.build" --limit 30 --output ./astro-docs
        """
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Markdown
    md = subparsers.add_parser("markdown", help="Get page as markdown")
    md.add_argument("url", help="URL to scrape")
    md.add_argument("--main-only", action="store_true", help="Exclude nav/footer")
    
    # Screenshot
    ss = subparsers.add_parser("screenshot", help="Screenshot a webpage")
    ss.add_argument("url", help="URL to capture")
    ss.add_argument("--output", "-o", help="Save to file (PNG)")
    
    # Extract
    ex = subparsers.add_parser("extract", help="Extract structured data")
    ex.add_argument("url", help="URL to extract from")
    ex.add_argument("--schema", required=True, help="Path to JSON schema file")
    ex.add_argument("--prompt", help="Extraction guidance prompt")
    
    # Search
    se = subparsers.add_parser("search", help="Search the web")
    se.add_argument("query", help="Search query")
    se.add_argument("--limit", type=int, default=5, help="Number of results (default: 5)")
    
    # Crawl
    cr = subparsers.add_parser("crawl", help="Crawl a docs site")
    cr.add_argument("url", help="Starting URL")
    cr.add_argument("--limit", type=int, default=50, help="Max pages (default: 50)")
    cr.add_argument("--output", "-o", help="Save to directory")
    
    # Map
    mp = subparsers.add_parser("map", help="Discover URLs on a site")
    mp.add_argument("url", help="URL to map")
    mp.add_argument("--search", help="Filter URLs containing this term")
    mp.add_argument("--limit", type=int, default=100, help="Max URLs (default: 100)")
    
    args = parser.parse_args()
    
    commands = {
        "markdown": cmd_markdown,
        "screenshot": cmd_screenshot,
        "extract": cmd_extract,
        "search": cmd_search,
        "crawl": cmd_crawl,
        "map": cmd_map,
    }
    
    commands[args.command](args)


if __name__ == "__main__":
    main()
