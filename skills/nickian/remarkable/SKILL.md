---
name: remarkable
description: Send files and web articles to a reMarkable e-ink tablet via the reMarkable Cloud. Upload PDFs, EPUBs, or convert web articles to readable ebooks and send them to the device. Also browse and manage files on the device. Use when the user mentions reMarkable, wants to send an article or document to their e-reader, or manage reMarkable cloud files.
---

# reMarkable Cloud

Send documents and web articles to a reMarkable tablet via the cloud API. Uses `rmapi` for cloud access.

## Setup

Install rmapi (Go required):
```bash
cd /tmp && git clone --depth 1 https://github.com/ddvk/rmapi.git
cd rmapi && go build -o /usr/local/bin/rmapi .
```

First run will prompt for a one-time code from https://my.remarkable.com/device/browser?showOtp=true

Python dependencies (for article conversion): `readability-lxml`, `ebooklib`, `requests`, `beautifulsoup4`, `lxml`.

## Commands

### Send a web article to the device

```bash
{baseDir}/scripts/remarkable.sh send-article --url "https://example.com/article" --dir /Articles
{baseDir}/scripts/remarkable.sh send-article --url "https://example.com/article" --format pdf --dir /
{baseDir}/scripts/remarkable.sh send-article --url "https://example.com/article" --title "Custom Title" --dir /Articles
```

Fetches article, extracts readable content, converts to EPUB (default) or PDF, uploads to reMarkable cloud. Device syncs automatically.

### List files

```bash
{baseDir}/scripts/remarkable.sh ls /
{baseDir}/scripts/remarkable.sh ls /Articles
{baseDir}/scripts/remarkable.sh ls "/Book Notes"
```

Output: `[f]` = file, `[d]` = directory.

### Upload a file

```bash
{baseDir}/scripts/remarkable.sh upload --file /path/to/document.pdf --dir /Books
{baseDir}/scripts/remarkable.sh upload --file /path/to/book.epub --dir /
```

### Create a folder

```bash
{baseDir}/scripts/remarkable.sh mkdir --path /NewFolder
```

### Search for files

```bash
{baseDir}/scripts/remarkable.sh find --name "article title"
```

## Notes

- EPUB is recommended for articles — reflows nicely on e-ink
- Device syncs automatically when connected to WiFi
- Auth tokens are cached by rmapi at `~/.rmapi`
- Some sites block scraping — if article fetch fails, try a different URL
