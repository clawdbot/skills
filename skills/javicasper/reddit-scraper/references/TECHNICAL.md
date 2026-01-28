# Reddit Skill - Technical Details

## Method

Uses Reddit's **public JSON API** (no authentication required).

**Endpoints:**
- Subreddit: `https://www.reddit.com/r/{subreddit}/{sort}.json`
- Search: `https://www.reddit.com/search.json?q={query}`
- Subreddit search: `https://www.reddit.com/r/{subreddit}/search.json?q={query}&restrict_sr=on`

## Dependencies

```bash
# System package (already installed)
apt-get install python3-requests
```

## How It Works

1. Sends HTTP GET request to Reddit's JSON API
2. Parses JSON response
3. Extracts post data: title, author, score, comments, URL, etc.
4. Filters out promoted posts
5. Formats output (text or JSON)

## API Response Format

Reddit returns JSON with this structure:
```json
{
  "kind": "Listing",
  "data": {
    "children": [
      {
        "kind": "t3",
        "data": {
          "title": "...",
          "author": "...",
          "score": 123,
          ...
        }
      }
    ]
  }
}
```

## Rate Limiting

Reddit's JSON API has rate limits:
- ~60 requests per minute (unauthenticated)
- Use `--limit` to reduce requests
- Add delays between multiple requests if needed

## Known Issues

### 403 Forbidden
- Reddit occasionally blocks requests
- Try again in a few minutes
- May need different User-Agent

### Empty Results
- Subreddit may be private or quarantined
- Search query may be too specific

## Previous Versions

**v1 (Web Scraping)**
- Scraped old.reddit.com HTML
- Issues with subreddit name extraction
- Search didn't work reliably

**v2 (JSON API) - Current**
- Uses public JSON API
- More reliable and faster
- Full search support
