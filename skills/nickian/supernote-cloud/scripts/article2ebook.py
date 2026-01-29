#!/usr/bin/env python3
"""
Convert a web article URL into a clean EPUB or PDF for e-readers.

Usage:
    python3 article2ebook.py URL [--format epub|pdf] [--output PATH] [--title TITLE]

Requires: requests, readability-lxml, beautifulsoup4, lxml, ebooklib
"""
import argparse
import hashlib
import html
import os
import re
import sys
import tempfile
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from readability import Document


def fetch_article(url):
    """Fetch and extract readable article content."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    doc = Document(resp.text)
    title = doc.title()
    content_html = doc.summary()

    # Clean up with BeautifulSoup
    soup = BeautifulSoup(content_html, 'lxml')

    # Remove scripts, styles, iframes
    for tag in soup.find_all(['script', 'style', 'iframe', 'noscript']):
        tag.decompose()

    # Extract images (download for EPUB embedding)
    images = []
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src', '')
        if src:
            if src.startswith('//'):
                src = 'https:' + src
            elif src.startswith('/'):
                parsed = urlparse(url)
                src = f"{parsed.scheme}://{parsed.netloc}{src}"
            images.append({'tag': img, 'src': src})

    return title, soup, images, url


def download_image(src, timeout=10):
    """Download an image, return (content_bytes, content_type, extension)."""
    try:
        resp = requests.get(src, timeout=timeout, headers={
            'User-Agent': 'Mozilla/5.0'
        })
        resp.raise_for_status()
        ct = resp.headers.get('Content-Type', 'image/jpeg')
        ext = 'jpg'
        if 'png' in ct:
            ext = 'png'
        elif 'gif' in ct:
            ext = 'gif'
        elif 'webp' in ct:
            ext = 'webp'
        elif 'svg' in ct:
            ext = 'svg'
        return resp.content, ct, ext
    except Exception:
        return None, None, None


def make_clean_html(title, soup, source_url):
    """Generate a clean, readable HTML document."""
    # Get body content
    body = soup.get_text() if not soup.body else str(soup)

    date_str = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    domain = urlparse(source_url).netloc

    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>{html.escape(title)}</title>
<style>
    body {{
        font-family: Georgia, 'Times New Roman', serif;
        max-width: 42em;
        margin: 2em auto;
        padding: 0 1em;
        line-height: 1.7;
        color: #1a1a1a;
        font-size: 16px;
    }}
    h1 {{
        font-size: 1.8em;
        line-height: 1.2;
        margin-bottom: 0.3em;
    }}
    .meta {{
        color: #666;
        font-size: 0.9em;
        margin-bottom: 2em;
        border-bottom: 1px solid #ddd;
        padding-bottom: 1em;
    }}
    img {{
        max-width: 100%;
        height: auto;
    }}
    blockquote {{
        border-left: 3px solid #ccc;
        margin-left: 0;
        padding-left: 1em;
        color: #555;
    }}
    a {{ color: #1a5276; }}
    p {{ margin: 1em 0; }}
    pre, code {{
        background: #f5f5f5;
        padding: 0.2em 0.4em;
        font-size: 0.9em;
    }}
    pre {{
        padding: 1em;
        overflow-x: auto;
    }}
</style>
</head>
<body>
<h1>{html.escape(title)}</h1>
<div class="meta">Source: {html.escape(domain)} &middot; Saved: {date_str}</div>
{body}
</body>
</html>"""


def to_epub(title, soup, images, source_url, output_path):
    """Convert article to EPUB."""
    from ebooklib import epub

    book = epub.EpubBook()

    # Metadata
    safe_id = hashlib.md5(source_url.encode()).hexdigest()
    book.set_identifier(f'article-{safe_id}')
    book.set_title(title)
    book.set_language('en')
    book.add_author('Web Article')

    # Download and embed images
    img_map = {}
    for i, img_info in enumerate(images):
        data, ct, ext = download_image(img_info['src'])
        if data:
            img_name = f'images/img_{i}.{ext}'
            epub_img = epub.EpubImage()
            epub_img.file_name = img_name
            epub_img.media_type = ct
            epub_img.content = data
            book.add_item(epub_img)
            img_info['tag']['src'] = img_name
            img_map[img_info['src']] = img_name

    # Build chapter content
    clean_html = make_clean_html(title, soup, source_url)

    chapter = epub.EpubHtml(title=title, file_name='article.xhtml', lang='en')
    chapter.content = clean_html

    book.add_item(chapter)
    book.toc = [chapter]
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    book.spine = ['nav', chapter]

    # Default CSS
    style = epub.EpubItem(
        uid='style',
        file_name='style/default.css',
        media_type='text/css',
        content=b'''
body { font-family: Georgia, serif; line-height: 1.7; margin: 1em; }
h1 { font-size: 1.6em; line-height: 1.2; }
.meta { color: #666; font-size: 0.85em; margin-bottom: 1.5em; }
img { max-width: 100%; }
blockquote { border-left: 3px solid #ccc; padding-left: 1em; color: #555; margin-left: 0; }
'''
    )
    book.add_item(style)
    chapter.add_item(style)

    epub.write_epub(output_path, book)
    return output_path


def to_pdf(title, soup, images, source_url, output_path):
    """Convert article to PDF using basic HTML rendering.
    
    Falls back to a simple text-based approach if no PDF renderer is available.
    """
    clean_html = make_clean_html(title, soup, source_url)

    # Try weasyprint first
    try:
        from weasyprint import HTML
        HTML(string=clean_html).write_pdf(output_path)
        return output_path
    except ImportError:
        pass
    except Exception:
        pass

    # Fallback: use macOS textutil if available
    tmp_html = output_path.replace('.pdf', '.html')
    with open(tmp_html, 'w', encoding='utf-8') as f:
        f.write(clean_html)

    # Try cupsfilter or textutil → PDF
    import subprocess

    # Try using /usr/sbin/cupsfilter (macOS built-in)
    try:
        result = subprocess.run(
            ['/usr/bin/python3', '-c', f'''
import subprocess, sys
# Use macOS Automator/AppKit for HTML to PDF
from Foundation import NSURL
from AppKit import NSPrintOperation, NSPrintInfo
from WebKit import WKWebView, WKWebViewConfiguration
# This is complex, try simpler approach
sys.exit(1)
'''],
            capture_output=True, timeout=10
        )
    except Exception:
        pass

    # Simplest fallback: use textutil to make RTF, then python to wrap
    # Actually, let's just save as HTML and note it in output
    try:
        # cupsfilter can convert HTML to PDF on macOS
        result = subprocess.run(
            ['cupsfilter', tmp_html],
            capture_output=True, timeout=30
        )
        if result.returncode == 0 and result.stdout:
            with open(output_path, 'wb') as f:
                f.write(result.stdout)
            os.unlink(tmp_html)
            return output_path
    except Exception:
        pass

    # Final fallback: save as HTML (still very readable on Supernote)
    os.rename(tmp_html, output_path.replace('.pdf', '.html'))
    print(f"Note: PDF generation unavailable. Saved as HTML instead.", file=sys.stderr)
    return output_path.replace('.pdf', '.html')


def sanitize_filename(title, ext):
    """Create a safe filename from the article title."""
    # Remove special chars, truncate
    safe = re.sub(r'[^\w\s\-]', '', title)
    safe = re.sub(r'\s+', '_', safe.strip())
    if len(safe) > 80:
        safe = safe[:80]
    return f"supernote_{safe}.{ext}"


def main():
    parser = argparse.ArgumentParser(description='Convert web article to EPUB/PDF')
    parser.add_argument('url', help='Article URL')
    parser.add_argument('--format', '-f', choices=['epub', 'pdf'], default='epub',
                        help='Output format (default: epub)')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--title', '-t', help='Override article title')
    args = parser.parse_args()

    print(f"Fetching: {args.url}", file=sys.stderr)
    title, soup, images, url = fetch_article(args.url)

    if args.title:
        title = args.title

    print(f"Title: {title}", file=sys.stderr)

    # Determine output path
    if args.output:
        output_path = args.output
    else:
        filename = sanitize_filename(title, args.format)
        output_path = os.path.join(tempfile.gettempdir(), filename)

    if args.format == 'epub':
        result = to_epub(title, soup, images, url, output_path)
    else:
        result = to_pdf(title, soup, images, url, output_path)

    print(f"Saved: {result}", file=sys.stderr)
    # Print path to stdout for piping
    print(result)


if __name__ == '__main__':
    main()
