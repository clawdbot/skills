# ai-meta-tags

Scan any URL or HTML file and get the meta tags you're missing. SEO basics, Open Graph, Twitter cards. It reads your page content and generates tags that actually match what's on the page.

## Install

```bash
npm install -g ai-meta-tags
```

## Usage

```bash
npx ai-meta-tags --url https://mysite.com
npx ai-meta-tags --file index.html
```

## Setup

```bash
export OPENAI_API_KEY=sk-...
```

## Options

- `-u, --url <url>` - URL to scan
- `-f, --file <path>` - Local HTML file to scan

## What it checks

- `title` and `description`
- Open Graph tags (og:title, og:description, og:image, og:url, og:type)
- Twitter Card tags (twitter:card, twitter:title, twitter:description, twitter:image)

It tells you what's missing and gives you the HTML to paste into your `<head>`. The descriptions are generated from your actual page content, not generic filler.

## License

MIT
