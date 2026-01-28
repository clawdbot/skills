---
name: meta-tags-gen
description: Scan pages and generate missing meta tags. Use when improving SEO.
---

# Meta Tags Generator

Your pages are missing Open Graph tags and Twitter cards. This tool scans your content and generates the meta tags that actually match what's on the page.

**One command. Zero config. Just works.**

## Quick Start

```bash
npx ai-meta-tags --url https://mysite.com
```

## What It Does

- Scans URLs or local HTML files
- Identifies missing meta tags
- Generates SEO, Open Graph, and Twitter Card tags
- Creates descriptions from actual page content

## Usage Examples

```bash
# Scan a URL
npx ai-meta-tags --url https://mysite.com

# Scan local file
npx ai-meta-tags --file index.html

# Generate for blog post
npx ai-meta-tags --url https://mysite.com/blog/my-post
```

## Best Practices

- **Unique descriptions per page** - not the same everywhere
- **Keep titles under 60 chars** - longer gets truncated
- **Use real images** - og:image matters for shares
- **Test with validators** - Facebook and Twitter have them

## When to Use This

- Links look bad when shared on social media
- SEO audit says meta tags are missing
- Building a new site and need all the tags
- Updating old pages with modern SEO

## Part of the LXGIC Dev Toolkit

This is one of 110+ free developer tools built by LXGIC Studios. No paywalls, no sign-ups, no API keys on free tiers. Just tools that work.

**Find more:**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- Website: https://lxgicstudios.com

## Requirements

No install needed. Just run with npx. Node.js 18+ recommended. Needs OPENAI_API_KEY environment variable.

```bash
npx ai-meta-tags --help
```

## How It Works

Fetches your page content, analyzes the text and structure, then generates appropriate meta tags. The AI creates descriptions that actually summarize your content rather than generic filler.

## License

MIT. Free forever. Use it however you want.
