---
name: reddit
description: "Read and search Reddit posts via web scraping of old.reddit.com. Use when Clawdbot needs to browse Reddit content - read posts from subreddits, search for topics, monitor specific communities. Read-only access with no posting or comments."
---

# Reddit Skill 📰

Read and search Reddit posts using the public JSON API. No API key required.

## Quick Start

```bash
# Read top posts from a subreddit
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --subreddit LocalLLaMA --limit 5

# Search for posts
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --search "clawdbot" --limit 5

# Read newest posts
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --subreddit ClaudeAI --sort nuevos --limit 5
```

## Options

| Option | Short | Description | Default |
|--------|-------|-------------|---------|
| `--subreddit` | `-s` | Subreddit name (without r/) | - |
| `--search` | `-q` | Search query | - |
| `--sort` | - | Sort: hot, new, top, populares, nuevos, rising | top |
| `--time` | `-t` | Time filter: hour, day, week, month, year, all | day |
| `--limit` | `-n` | Number of posts (max 100) | 25 |
| `--json` | `-j` | Output as JSON | false |
| `--verbose` | `-v` | Show post preview text | false |

## Examples

### Read subreddit posts
```bash
# Top posts of the day (default)
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --subreddit programming

# Hot posts
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --subreddit programming --sort hot

# New posts
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --subreddit programming --sort nuevos

# Top posts of the week
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --subreddit programming --sort top --time week
```

### Search posts
```bash
# Search all of Reddit
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --search "machine learning"

# Search within a subreddit
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --subreddit selfhosted --search "docker"

# Search with time filter
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --search "AI news" --time week
```

### JSON output
```bash
# Get raw JSON data for processing
python3 /root/clawd/skills/reddit/scripts/reddit_scraper.py --subreddit technology --limit 3 --json
```

## Output Fields (JSON)

- `title`: Post title
- `author`: Username
- `score`: Upvotes (net)
- `num_comments`: Comment count
- `url`: Link URL
- `permalink`: Reddit discussion URL
- `subreddit`: Subreddit name
- `created_utc`: Unix timestamp
- `selftext`: Post text (first 200 chars)
- `upvote_ratio`: Upvote percentage (0-1)

## Limitations

- **Read-only**: Cannot post, comment, or vote
- **Rate limits**: Reddit may rate-limit if too many requests
- **No auth**: Some content may be restricted

## Technical Details

See [TECHNICAL.md](references/TECHNICAL.md) for implementation details.
