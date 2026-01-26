---
name: firecrawl
description: Web scraping and crawling with Firecrawl API. Fetch webpage content as markdown, take screenshots, extract structured data, search the web, and crawl documentation sites. Use when the user needs to scrape a URL, get current web info, capture a screenshot, extract specific data from pages, or crawl docs for a framework/library.
version: 1.0.0
author: captmarbles
---

# Firecrawl Web Skill

Scrape, search, and crawl the web using [Firecrawl](https://firecrawl.dev).

## Setup

1. Get your API key from [firecrawl.dev/app/api-keys](https://www.firecrawl.dev/app/api-keys)
2. Set the environment variable:
   ```bash
   export FIRECRAWL_API_KEY=fc-your-key-here
   ```
3. Install the SDK:
   ```bash
   pip3 install firecrawl
   ```

## Usage

All commands use the bundled `fc.py` script in this skill's directory.

### Get Page as Markdown

Fetch any URL and convert to clean markdown. Handles JavaScript-rendered content.

```bash
python3 fc.py markdown "https://example.com"
python3 fc.py markdown "https://example.com" --main-only  # skip nav/footer
```

### Take Screenshot

Capture a full-page screenshot of any URL.

```bash
python3 fc.py screenshot "https://example.com" -o screenshot.png
```

### Extract Structured Data

Pull specific fields from a page using a JSON schema.

**Schema example** (`schema.json`):
```json
{
  "type": "object",
  "properties": {
    "title": { "type": "string" },
    "price": { "type": "number" },
    "features": { "type": "array", "items": { "type": "string" } }
  }
}
```

```bash
python3 fc.py extract "https://example.com/product" --schema schema.json
python3 fc.py extract "https://example.com/product" --schema schema.json --prompt "Extract the main product details"
```

### Web Search

Search the web and get content from results (may require paid tier).

```bash
python3 fc.py search "Python 3.13 new features" --limit 5
```

### Crawl Documentation

Crawl an entire documentation site. Great for learning new frameworks.

```bash
python3 fc.py crawl "https://docs.example.com" --limit 30
python3 fc.py crawl "https://docs.example.com" --limit 50 --output ./docs
```

**Note:** Each page costs 1 credit. Set reasonable limits.

### Map Site URLs

Discover all URLs on a website before deciding what to scrape.

```bash
python3 fc.py map "https://example.com" --limit 100
python3 fc.py map "https://example.com" --search "api"
```

## Example Prompts

- *"Scrape https://blog.example.com/post and summarize it"*
- *"Take a screenshot of stripe.com"*
- *"Extract the name, price, and features from this product page"*
- *"Crawl the Astro docs so you can help me build a site"*
- *"Map all the URLs on docs.stripe.com"*

## Pricing

Free tier includes 500 credits. 1 credit = 1 page/screenshot/search query.
