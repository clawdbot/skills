---
name: lenny-search
description: Deep search across all Lenny's Podcast transcripts using QMD. Requires setup.
metadata: {
  "clawdbot": {
    "emoji": "🎙️",
    "requires": {
      "optionalBins": ["qmd", "git"]
    },
    "notes": [
      "Requires one-time setup: cloning the transcript repo and indexing it.",
      "Uses the 'lenny' collection in QMD for focused search.",
      "Source data: https://github.com/ChatPRD/lennys-podcast-transcripts"
    ]
  }
}
---

# Lenny's Podcast Search

This skill enables deep semantic search over the entire archive of Lenny's Podcast transcripts. It uses **QMD** to index and query the data locally.

## 🛠️ One-Time Setup

Before you can search, you must download the data and tell QMD where it is. Run these commands:

1.  **Get the Data:**
    Clones the public transcript repository to a standard location (e.g., `~/knowledge`).
    ```bash
    mkdir -p ~/knowledge
    git clone https://github.com/ChatPRD/lennys-podcast-transcripts.git ~/knowledge/lennys-podcast-transcripts
    ```

2.  **Index with QMD:**
    Creates a dedicated collection named `lenny`.
    ```bash
    qmd collection add ~/knowledge/lennys-podcast-transcripts --name lenny --mask "**/*.md"
    ```

## 🔍 How to Search

Once setup is complete, query the `lenny` collection:

### Ask a Question
```bash
qmd query "how to hire a first PM" -c lenny
```

### Find Specific Guests
```bash
qmd query "Brian Chesky interview" -c lenny
```

### Get Structured Output (for AI Analysis)
Use `--json` to get rich metadata (guest name, video URL, timestamps) found in the transcript frontmatter.
```bash
qmd query "growth loops" -c lenny --json
```

## 📄 Transcript Format
Each transcript file contains YAML frontmatter with useful metadata:
```yaml
guest: "Casey Winters"
company: "Eventbrite, Pinterest"
role: "CPO"
youtube_url: "https://www.youtube.com/watch?v=..."
video_id: "VIDEO_ID"
```
You can use `qmd get` to retrieve this raw content if needed.

## 🔄 Updates
To get the latest episodes:
```bash
cd ~/knowledge/lennys-podcast-transcripts
git pull
qmd update --pull
```
