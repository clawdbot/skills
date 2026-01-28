# Manual Blog-to-Kindle Workflow

When scripts are unavailable or for custom sites, follow this workflow.

## Step 1: Fetch Articles

### Find the archive/index page
Most blogs have an archive page listing all posts:
- `/archives`, `/blog`, `/articles`, `/posts`, `/all`
- Look for "All Posts", "Archives", "Index" links

### Extract article URLs
```bash
# Fetch archive page
curl -s "https://example.com/archives" > archive.html

# Extract links (adjust selector)
grep -oP 'href="[^"]*\.html"' archive.html | sort -u > links.txt
```

### Fetch each article
```bash
mkdir -p essays
cat links.txt | while read url; do
  slug=$(echo "$url" | sed 's/.*\///' | sed 's/\.html//')
  curl -s "$url" > "essays/$slug.html"
  sleep 0.5
done
```

### Convert to markdown
```bash
for f in essays/*.html; do
  pandoc "$f" -o "${f%.html}.md" --from html --to markdown
done
```

## Step 2: Generate Cover

Use the nano-banana-pro skill with this prompt template:

```
Book cover for '[Author]: [Subtitle/Topic]'.
Minimalist design with elegant typography.
[Accent color] accent color.
Clean white/cream background.
Simple geometric or abstract [topic] motif.
Professional literary feel.
No photos, no faces.
Portrait orientation book cover dimensions.
```

Example for Paul Graham:
```bash
GEMINI_API_KEY=$(security find-generic-password -a "aineko" -s "api/gemini" -w) \
uv run ~/clawd/skills/nano-banana-pro/scripts/generate_image.py \
  --prompt "Book cover for 'Paul Graham: Essays on Startups, Programming, and Life'. Minimalist design with elegant typography. Y Combinator orange accent. Clean cream background. Abstract code/startup motif. Professional literary feel. No photos. Portrait book cover." \
  --filename "pg-cover.png" \
  --resolution 2K
```

## Step 3: Combine and Compile

### Create combined markdown
```bash
cat > combined.md << 'EOF'
---
title: Essays by [Author]
author: [Author Name]
lang: en
---

EOF

for f in essays/*.md; do
  cat "$f" >> combined.md
  echo -e "\n\n---\n\n" >> combined.md
done
```

### Convert to EPUB with cover
```bash
pandoc combined.md -o book.epub \
  --epub-cover-image=cover.png \
  --toc \
  --toc-depth=2 \
  --metadata title="Essays by Author" \
  --metadata author="Author Name"
```

## Step 4: Send to Kindle

### Via Mail.app (AppleScript)
```bash
osascript <<'EOF'
tell application "Mail"
    set newMessage to make new outgoing message with properties {subject:"Book Title", visible:false}
    tell newMessage
        make new to recipient at end of to recipients with properties {address:"simonpilkington74_8oVjpj@kindle.com"}
        set content to "Sent via blog-to-kindle."
        make new attachment with properties {file name:"/path/to/book.epub"} at after the last paragraph
    end tell
    send newMessage
end tell
EOF
```

### Via command line (if mutt/sendmail configured)
```bash
echo "Book attached" | mutt -s "Book Title" -a book.epub -- user@kindle.com
```

## Tips

### File size
- EPUB compresses well; 3MB markdown → ~1.5MB EPUB
- Kindle limit: 50MB
- If too large, split into volumes

### Kindle conversion
- Kindle converts EPUB to AZW automatically
- Tables and complex formatting may not survive
- Images are converted; vector graphics may blur

### Approved senders
- Kindle only accepts email from approved addresses
- Add sender to: Amazon → Manage Content & Devices → Preferences → Approved Personal Document E-mail List

### Cover dimensions
- Ideal: 1600x2560 pixels (1:1.6 ratio)
- Minimum: 625x1000 pixels
- 2K resolution from Nano Banana Pro works well
