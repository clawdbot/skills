---
name: freshrss
description: Query headlines and articles from a self-hosted FreshRSS instance. Use when the user asks for RSS news, latest headlines, feed updates, or wants to browse articles from their FreshRSS reader. Supports filtering by category, time range, and count.
---

# FreshRSS

Query headlines from a self-hosted FreshRSS instance via the Google Reader compatible API.

## Setup

Set these environment variables:

```bash
export FRESHRSS_URL="https://your-freshrss-instance.com"
export FRESHRSS_USER="your-username"
export FRESHRSS_API_PASSWORD="your-api-password"
```

API password is set in FreshRSS → Settings → Profile → API Management.

## Commands

### Get latest headlines

```bash
{baseDir}/scripts/freshrss.sh headlines --count 10
```

### Get headlines from the last N hours

```bash
{baseDir}/scripts/freshrss.sh headlines --hours 2
```

### Get headlines from a specific category

```bash
{baseDir}/scripts/freshrss.sh headlines --category "Technology" --count 15
```

### Get only unread headlines

```bash
{baseDir}/scripts/freshrss.sh headlines --unread --count 20
```

### Combine filters

```bash
{baseDir}/scripts/freshrss.sh headlines --category "News" --hours 4 --count 10 --unread
```

### List categories

```bash
{baseDir}/scripts/freshrss.sh categories
```

### List feeds

```bash
{baseDir}/scripts/freshrss.sh feeds
```

## Output

Headlines are formatted as:
```
[date] [source] Title
  URL
  Categories: cat1, cat2
```

## Notes

- Default count is 20 headlines if not specified
- Time filtering uses `--hours` for relative time (e.g., last 2 hours)
- Category names are case-sensitive and must match your FreshRSS categories
- Use `categories` command first to see available category names
