#!/usr/bin/env python3
"""
Convert a web article URL into a clean EPUB or PDF for e-readers.

Uses the same document creation methodology as the Read on reMarkable
Chrome extension: Readability extraction → HTML sanitization → minimal
EPUB3 packaging with clean XHTML and simple CSS.

Usage:
    python3 article2ebook.py URL [--format epub|pdf] [--output PATH] [--title TITLE]

Requires: requests, readability-lxml, beautifulsoup4, lxml
"""
import argparse
import html
import io
import os
import re
import sys
import tempfile
import uuid
import zipfile
from datetime import datetime, timezone
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup
from readability import Document


# Minimal CSS matching the Chrome extension's "lipstick-on-pig.css" style
ARTICLE_CSS = """\
p {
  margin-top: 1em;
  margin-bottom: 1em;
}

ul, ol {
  padding: 1em;
}

ul li, ol li {
  margin-left: 1.5em;
  padding-left: 0.5em;
}

figcaption {
  font-size: 0.5rem;
  font-style: italic;
}
"""

# Tags allowed through sanitization (matches the extension's whitelist)
ALLOWED_TAGS = {
    'a', 'abbr', 'address', 'acronym', 'article', 'aside', 'audio',
    'b', 'bdi', 'bdo', 'big', 'blockquote', 'br', 'button',
    'canvas', 'caption', 'center', 'cite', 'code', 'col', 'colgroup',
    'datalist', 'dd', 'del', 'details', 'dfn', 'div', 'dl', 'dt',
    'em', 'embed', 'fieldset', 'figcaption', 'figure', 'font', 'footer',
    'form', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'header', 'hgroup',
    'hr', 'i', 'img', 'input', 'ins', 'kbd', 'label', 'li', 'link',
    'main', 'map', 'mark', 'menu', 'meter', 'nav', 'object', 'ol',
    'output', 'p', 'param', 'pre', 'progress', 'q', 'ruby', 's',
    'samp', 'section', 'select', 'small', 'span', 'strike', 'strong',
    'style', 'sub', 'sup', 'table', 'tbody', 'td', 'textarea', 'tfoot',
    'th', 'thead', 'time', 'tr', 'tt', 'u', 'ul', 'var', 'video', 'wbr',
}


def fetch_article(url):
    """Fetch and extract readable article content using Readability."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) '
                       'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    resp = requests.get(url, headers=headers, timeout=30)
    resp.raise_for_status()

    doc = Document(resp.text)
    title = doc.title()
    content_html = doc.summary()

    return title, content_html, url


def sanitize_html(content_html):
    """Sanitize HTML, keeping only allowed tags (matches extension whitelist)."""
    soup = BeautifulSoup(content_html, 'lxml')

    # Remove disallowed tags but keep their text content
    for tag in soup.find_all(True):
        if tag.name not in ALLOWED_TAGS:
            tag.unwrap()

    # Remove script/style/iframe/noscript entirely (content and all)
    for tag in soup.find_all(['script', 'style', 'iframe', 'noscript']):
        tag.decompose()

    return soup


def process_images(soup, base_url):
    """Download images and embed them, returning list of image entries."""
    images = []
    for i, img in enumerate(soup.find_all('img')):
        src = img.get('src') or img.get('data-src', '')
        if not src:
            img.decompose()
            continue

        # Resolve relative URLs
        if src.startswith('//'):
            src = 'https:' + src
        elif src.startswith('/'):
            parsed = urlparse(base_url)
            src = f"{parsed.scheme}://{parsed.netloc}{src}"
        elif not src.startswith(('http://', 'https://', 'data:')):
            parsed = urlparse(base_url)
            src = f"{parsed.scheme}://{parsed.netloc}/{src}"

        # Download
        try:
            resp = requests.get(src, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
            resp.raise_for_status()
            data = resp.content
            ct = resp.headers.get('Content-Type', 'image/png')

            # Skip tiny images (likely tracking pixels)
            if len(data) < 100:
                img.decompose()
                continue

            img_name = f"image-{i}.png"
            img['src'] = img_name
            images.append({'name': img_name, 'data': data, 'type': ct})
        except Exception:
            img.decompose()

    return images


def build_article_xhtml(title, body_content):
    """Build the article XHTML file matching the extension's format.

    The extension creates: <html> with xmlns, <head> with <link> to CSS,
    <body> with <h1> title prepended, then Readability content.
    """
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head>
<title>{html.escape(title)}</title>
<link rel="stylesheet" type="text/css" href="lipstick-on-pig.css"/>
</head>
<body>
<h1>{html.escape(title)}</h1>
{body_content}
</body>
</html>"""


def build_nav_xhtml(title):
    """Build the EPUB3 navigation document."""
    return f"""<?xml version="1.0" encoding="UTF-8"?>
<html xmlns="http://www.w3.org/1999/xhtml" xmlns:epub="http://www.idpf.org/2007/ops" xml:lang="en" lang="en">
<head>
<title>{html.escape(title)}</title>
</head>
<body>
<nav epub:type="toc" id="toc">
<ol>
<li><a href="article.xhtml">{html.escape(title)}</a></li>
</ol>
</nav>
</body>
</html>"""


def build_content_opf(title, author, subject, image_items):
    """Build the OPF package document."""
    book_id = str(uuid.uuid4())
    modified = datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')

    img_manifest = '\n    '.join(
        f'<item id="{img["name"]}" href="{img["name"]}" media-type="{img["type"]}"/>'
        for img in image_items
    )

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<package xmlns="http://www.idpf.org/2007/opf" xmlns:opf="http://www.idpf.org/2007/opf" version="3.0" unique-identifier="BookID">
  <metadata xmlns:dc="http://purl.org/dc/elements/1.1/">
    <dc:identifier id="BookID">{book_id}</dc:identifier>
    <dc:title>{html.escape(title)}</dc:title>
    <dc:creator>{html.escape(author)}</dc:creator>
    <dc:subject>{html.escape(subject)}</dc:subject>
    <dc:language>en</dc:language>
    <meta property="dcterms:modified">{modified}</meta>
  </metadata>
  <manifest>
    <item id="nav.xhtml" href="nav.xhtml" properties="nav" media-type="application/xhtml+xml"/>
    <item id="article.xhtml" href="article.xhtml" media-type="application/xhtml+xml"/>
    <item id="lipstick-on-pig.css" href="lipstick-on-pig.css" media-type="text/css"/>
    {img_manifest}
  </manifest>
  <spine>
    <itemref idref="article.xhtml"/>
  </spine>
</package>"""


def build_epub(title, body_content, images, author='', subject=''):
    """Build an EPUB3 file matching the Chrome extension's structure.

    Structure:
      mimetype
      META-INF/container.xml
      OEBPS/content.opf
      OEBPS/nav.xhtml
      OEBPS/article.xhtml
      OEBPS/lipstick-on-pig.css
      OEBPS/image-*.png (embedded images)
    """
    buf = io.BytesIO()

    with zipfile.ZipFile(buf, 'w', zipfile.ZIP_DEFLATED) as zf:
        # mimetype must be first and uncompressed
        zf.writestr('mimetype', 'application/epub+zip', compress_type=zipfile.ZIP_STORED)

        # META-INF/container.xml
        zf.writestr('META-INF/container.xml', """<?xml version="1.0"?>
<container xmlns="urn:oasis:names:tc:opendocument:xmlns:container" version="1.0">
<rootfiles>
<rootfile full-path="OEBPS/content.opf" media-type="application/oebps-package+xml"/>
</rootfiles>
</container>""")

        # OEBPS content
        zf.writestr('OEBPS/content.opf', build_content_opf(title, author, subject, images))
        zf.writestr('OEBPS/nav.xhtml', build_nav_xhtml(title))
        zf.writestr('OEBPS/article.xhtml', build_article_xhtml(title, body_content))
        zf.writestr('OEBPS/lipstick-on-pig.css', ARTICLE_CSS)

        # Embedded images
        for img in images:
            zf.writestr(f"OEBPS/{img['name']}", img['data'])

    return buf.getvalue()


def to_epub(title, content_html, source_url, output_path):
    """Convert article to EPUB using the extension's methodology."""
    soup = sanitize_html(content_html)
    images = process_images(soup, source_url)

    # Get the sanitized body content (just the inner content, no wrapping html/body)
    body = soup.body
    body_content = ''.join(str(child) for child in body.children) if body else str(soup)

    epub_data = build_epub(title, body_content, images, author='Web Article')

    with open(output_path, 'wb') as f:
        f.write(epub_data)

    return output_path


def to_pdf(title, content_html, source_url, output_path):
    """Convert article to PDF."""
    soup = sanitize_html(content_html)
    images = process_images(soup, source_url)

    body = soup.body
    body_content = ''.join(str(child) for child in body.children) if body else str(soup)

    clean_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8"><title>{html.escape(title)}</title>
<style>
body {{ font-family: Georgia, serif; max-width: 42em; margin: 2em auto; padding: 0 1em; line-height: 1.7; }}
h1 {{ font-size: 1.8em; line-height: 1.2; }}
img {{ max-width: 100%; height: auto; }}
p {{ margin-top: 1em; margin-bottom: 1em; }}
</style>
</head><body><h1>{html.escape(title)}</h1>{body_content}</body></html>"""

    # Try weasyprint
    try:
        from weasyprint import HTML
        HTML(string=clean_html).write_pdf(output_path)
        return output_path
    except (ImportError, Exception):
        pass

    # Fallback: cupsfilter on macOS
    import subprocess
    tmp_html = output_path.replace('.pdf', '.html')
    with open(tmp_html, 'w', encoding='utf-8') as f:
        f.write(clean_html)
    try:
        result = subprocess.run(['cupsfilter', tmp_html], capture_output=True, timeout=30)
        if result.returncode == 0 and result.stdout:
            with open(output_path, 'wb') as f:
                f.write(result.stdout)
            os.unlink(tmp_html)
            return output_path
    except Exception:
        pass

    # Final fallback: save as HTML
    final = output_path.replace('.pdf', '.html')
    os.rename(tmp_html, final)
    print("Note: PDF generation unavailable. Saved as HTML.", file=sys.stderr)
    return final


def sanitize_filename(title, ext):
    """Create a safe filename from the article title (title case, spaces)."""
    safe = re.sub(r'[^\w\s\-]', '', title)
    safe = re.sub(r'\s+', ' ', safe.strip())
    safe = safe.title()
    if len(safe) > 80:
        safe = safe[:80].rstrip()
    return f"{safe}.{ext}"


def main():
    parser = argparse.ArgumentParser(description='Convert web article to EPUB/PDF')
    parser.add_argument('url', help='Article URL')
    parser.add_argument('--format', '-f', choices=['epub', 'pdf'], default='epub',
                        help='Output format (default: epub)')
    parser.add_argument('--output', '-o', help='Output file path')
    parser.add_argument('--title', '-t', help='Override article title')
    args = parser.parse_args()

    print(f"Fetching: {args.url}", file=sys.stderr)
    title, content_html, url = fetch_article(args.url)

    if args.title:
        title = args.title

    print(f"Title: {title}", file=sys.stderr)

    if args.output:
        output_path = args.output
    else:
        filename = sanitize_filename(title, args.format)
        output_path = os.path.join(tempfile.gettempdir(), filename)

    if args.format == 'epub':
        result = to_epub(title, content_html, url, output_path)
    else:
        result = to_pdf(title, content_html, url, output_path)

    print(f"Saved: {result}", file=sys.stderr)
    print(result)


if __name__ == '__main__':
    main()
