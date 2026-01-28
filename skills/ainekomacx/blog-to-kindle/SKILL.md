---
name: blog-to-kindle
description: Scrape blogs/essay sites and compile into Kindle-friendly EPUB with AI-generated cover. Use for requests to download blogs for Kindle, compile essays into ebook, or send blog archives to Kindle. Supports Paul Graham, Kevin Kelly, Derek Sivers, Wait But Why, Astral Codex Ten, and custom sites.
---

# Blog to Kindle

Scrape blog/essay sites, compile into EPUB with cover art, and deliver to Kindle.

## Quick Start

```bash
# 1. Fetch essays from a supported site
uv run scripts/fetch_blog.py --site paulgraham --output ./pg-essays

# 2. Generate cover (uses Nano Banana Pro)
# See nano-banana-pro skill for cover generation

# 3. Compile to EPUB with cover
uv run scripts/compile_epub.py --input ./pg-essays --cover ./cover.png --output essays.epub

# 4. Send to Kindle
uv run scripts/send_to_kindle.py --file essays.epub --kindle-email user@kindle.com
```

## Workflow (MUST follow this order)

1. **Fetch** - Download all essays/posts from the blog
2. **Generate Cover** - Create cover art via Nano Banana Pro skill (DO NOT SKIP)
3. **Compile** - Combine into EPUB with cover embedded
4. **Send** - Email to Kindle address

⚠️ **Always generate and include cover before sending.** Never send without cover.

## Supported Sites

| Site | Key | URL Pattern |
|------|-----|-------------|
| Paul Graham | `paulgraham` | paulgraham.com/articles.html |
| Kevin Kelly | `kevinkelly` | kk.org/thetechnium |
| Derek Sivers | `sivers` | sive.rs/blog |
| Wait But Why | `waitbutwhy` | waitbutwhy.com/archive |
| Astral Codex Ten | `acx` | astralcodexten.com |

For unlisted sites, use `--site custom --url <archive-url>`.

## Cover Generation

Use the `nano-banana-pro` skill to generate covers. Prompt template:

```
Book cover for '[Author Name]: [Subtitle]'. 
Minimalist design with elegant typography. 
[Brand color] accent. Clean white/cream background. 
Simple geometric or abstract motif related to [topic].
Professional literary feel. No photos, no faces.
Portrait orientation book cover dimensions.
```

Generate at 2K resolution for good quality without huge file size.

## Kindle Delivery

Default Kindle address (Simon): `simonpilkington74_8oVjpj@kindle.com`

Uses Mail.app via AppleScript to send. Ensure:
- Sender email is on Kindle approved list
- File under 50MB (EPUB compresses well)

## State Tracking

State files stored in `~/.clawdbot/state/blog-kindle/`:
- `{site}-last-fetch.json` - Last fetch timestamp, article count
- `{site}-sent.json` - List of sent article IDs

Use for incremental updates (only fetch new posts).

## Manual Workflow (no scripts)

If scripts unavailable, follow this pattern:

1. **Fetch**: curl archive page → parse article links → fetch each → convert to markdown
2. **Combine**: Concatenate markdown with YAML frontmatter (title, author)
3. **Cover**: Generate via Nano Banana Pro
4. **Convert**: `pandoc combined.md -o output.epub --epub-cover-image=cover.png --toc`
5. **Send**: AppleScript Mail.app with attachment

See `references/manual-workflow.md` for detailed steps.
