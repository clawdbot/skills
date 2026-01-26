---
name: serpapi
description: Unified search API across Google, Amazon, Yelp, OpenTable, Walmart, and more. Use when searching for products, local businesses, restaurants, shopping, images, news, or any web search. One API key, many engines.
homepage: https://serpapi.com
metadata: {"clawdbot":{"emoji":"🔍","requires":{"env":["SERPAPI_API_KEY"]}}}
---

# SerpAPI - Unified Search

SerpAPI provides structured data from Google, Amazon, Yelp, OpenTable, and 20+ other search engines through a single API.

## Setup

1. Get an API key from https://serpapi.com (free tier: 100 searches/month)
2. Set environment variable: `export SERPAPI_API_KEY=your-key-here`
3. Optionally set default location in `<workspace>/TOOLS.md`:
   ```markdown
   ## SerpAPI
   Default location: Pittsburgh, PA
   ```

## Usage

```bash
# General syntax
<skill>/scripts/serp.py <engine> "<query>" [options]

# Examples
serp.py google "best coffee shops"
serp.py google_maps "restaurants near me" --location "15238"
serp.py amazon "mechanical keyboard" --num 10
serp.py yelp "pizza" --location "New York, NY"
serp.py google_shopping "standing desk"
```

## Engines

| Engine | Use for | Key features |
|--------|---------|--------------|
| `google` | General web search | Organic results, knowledge graph, local pack |
| `google_maps` | Local places/businesses | Ratings, reviews, hours, GPS coordinates |
| `google_shopping` | Product search | Prices, merchants, reviews |
| `google_images` | Image search | Thumbnails, sources |
| `google_news` | News articles | Headlines, sources, dates |
| `amazon` | Amazon products | Prices, ratings, reviews, Prime status |
| `yelp` | Local businesses | Reviews, ratings, categories |
| `opentable` | Restaurant reviews | Dining reviews, ratings |
| `walmart` | Walmart products | Prices, availability |
| `ebay` | eBay listings | Prices, bids, conditions |
| `tripadvisor` | Travel/attractions | Hotels, restaurants, things to do |

## Options

| Option | Description |
|--------|-------------|
| `--location`, `-l` | Location for local results (city, zip, address) |
| `--num`, `-n` | Number of results (default: 10) |
| `--format`, `-f` | Output format: `json` (default) or `text` |
| `--type`, `-t` | Google search type: `shop`, `isch`, `nws`, `vid` |
| `--page`, `-p` | Page number for pagination |
| `--gl` | Country code (e.g., `us`, `uk`, `de`) |
| `--hl` | Language code (e.g., `en`, `es`, `fr`) |

## When to Use Which Engine

**Finding local businesses/restaurants:**
- `google_maps` — Best for discovering places, hours, reviews
- `yelp` — Deep reviews and ratings for restaurants/services
- `opentable` — Restaurant-specific, dining reviews

**Shopping/Products:**
- `google_shopping` — Compare prices across merchants
- `amazon` — Amazon-specific search with Prime info
- `walmart` — Walmart inventory and prices
- `ebay` — Used items, auctions, collectibles

**General research:**
- `google` — Web pages, articles, general info
- `google_news` — Current events, news articles
- `google_images` — Finding images

## Examples

### Find restaurants near a location
```bash
serp.py google_maps "italian restaurants" --location "Pittsburgh, PA" --num 5
```

### Compare product prices
```bash
serp.py google_shopping "sony wh-1000xm5" --num 10
```

### Check Amazon reviews and pricing
```bash
serp.py amazon "standing desk" --num 10
```

### Get Yelp reviews for local services
```bash
serp.py yelp "plumber" --location "15238"
```

### Search news on a topic
```bash
serp.py google_news "AI regulation" --num 5
```

## Output Formats

**JSON (default):** Full structured data from SerpAPI. Best for programmatic use or when you need all details.

**Text (`--format text`):** Human-readable summary. Best for quick answers.

## Integration Notes

- Results are structured JSON — parse and extract what you need
- Local results include GPS coordinates for mapping
- Shopping results include extracted prices for comparison
- Knowledge graph provides entity information when available
- Rate limits: 100/month on free tier, check your plan at serpapi.com/dashboard
