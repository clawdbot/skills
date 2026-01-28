#!/usr/bin/env python3
"""Fetch essays/posts from supported blog sites."""

import argparse
import json
import os
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup

SITES = {
    "paulgraham": {
        "archive_url": "https://paulgraham.com/articles.html",
        "base_url": "https://paulgraham.com/",
        "link_selector": "a[href$='.html']",
        "content_selector": "font",
        "title_selector": "title",
    },
    "kevinkelly": {
        "archive_url": "https://kk.org/thetechnium/",
        "base_url": "https://kk.org/thetechnium/",
        "link_selector": "article a",
        "content_selector": "article .entry-content",
        "title_selector": "h1.entry-title",
    },
    "sivers": {
        "archive_url": "https://sive.rs/blog",
        "base_url": "https://sive.rs/",
        "link_selector": "ul.posts a",
        "content_selector": "article",
        "title_selector": "h1",
    },
}


def fetch_page(url: str, retries: int = 3) -> str:
    """Fetch a page with retries."""
    for i in range(retries):
        try:
            resp = httpx.get(url, follow_redirects=True, timeout=30)
            resp.raise_for_status()
            return resp.text
        except Exception as e:
            if i == retries - 1:
                raise
            time.sleep(2 ** i)
    return ""


def get_article_links(archive_html: str, config: dict, base_url: str) -> list[str]:
    """Extract article links from archive page."""
    soup = BeautifulSoup(archive_html, "html.parser")
    links = []
    seen = set()
    
    for a in soup.select(config["link_selector"]):
        href = a.get("href", "")
        if not href or href.startswith("#"):
            continue
        full_url = urljoin(base_url, href)
        if full_url not in seen:
            seen.add(full_url)
            links.append(full_url)
    
    return links


def extract_article(html: str, url: str, config: dict) -> dict:
    """Extract article content from page."""
    soup = BeautifulSoup(html, "html.parser")
    
    # Get title
    title_elem = soup.select_one(config["title_selector"])
    title = title_elem.get_text(strip=True) if title_elem else urlparse(url).path.split("/")[-1]
    
    # Get content
    content_elem = soup.select_one(config["content_selector"])
    if not content_elem:
        content_elem = soup.find("body")
    
    # Convert to markdown-ish text
    content = content_elem.get_text("\n\n", strip=True) if content_elem else ""
    
    return {
        "url": url,
        "title": title,
        "content": content,
    }


def save_as_markdown(article: dict, output_dir: Path, index: int) -> Path:
    """Save article as markdown file."""
    # Clean title for filename
    clean_title = re.sub(r'[^\w\s-]', '', article["title"])[:50].strip()
    clean_title = re.sub(r'\s+', '-', clean_title).lower()
    filename = f"{index:03d}-{clean_title}.md"
    
    filepath = output_dir / filename
    with open(filepath, "w") as f:
        f.write(f"# {article['title']}\n\n")
        f.write(article["content"])
    
    return filepath


def main():
    parser = argparse.ArgumentParser(description="Fetch blog essays")
    parser.add_argument("--site", required=True, choices=list(SITES.keys()) + ["custom"])
    parser.add_argument("--url", help="Archive URL for custom sites")
    parser.add_argument("--output", required=True, help="Output directory")
    parser.add_argument("--limit", type=int, help="Limit number of articles")
    args = parser.parse_args()
    
    if args.site == "custom":
        if not args.url:
            print("Error: --url required for custom sites")
            return 1
        config = SITES["paulgraham"].copy()  # Use as template
        config["archive_url"] = args.url
        config["base_url"] = urljoin(args.url, "/")
    else:
        config = SITES[args.site]
    
    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)
    essays_dir = output_dir / "essays"
    essays_dir.mkdir(exist_ok=True)
    
    print(f"Fetching archive from {config['archive_url']}...")
    archive_html = fetch_page(config["archive_url"])
    
    links = get_article_links(archive_html, config, config["base_url"])
    print(f"Found {len(links)} article links")
    
    if args.limit:
        links = links[:args.limit]
    
    articles = []
    for i, url in enumerate(links):
        print(f"[{i+1}/{len(links)}] Fetching {url}...")
        try:
            html = fetch_page(url)
            article = extract_article(html, url, config)
            if article["content"]:
                save_as_markdown(article, essays_dir, i)
                articles.append({"url": url, "title": article["title"]})
            time.sleep(0.5)  # Be polite
        except Exception as e:
            print(f"  Error: {e}")
    
    # Save manifest
    manifest = {
        "site": args.site,
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "article_count": len(articles),
        "articles": articles,
    }
    with open(output_dir / "manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    
    print(f"\nFetched {len(articles)} articles to {output_dir}")
    return 0


if __name__ == "__main__":
    exit(main())
