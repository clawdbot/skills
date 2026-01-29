---
name: lenny-search
description: Search Lenny Rachitsky's open-sourced podcast transcripts. Provides deep insights from product leaders.
metadata: {
  "clawdbot": {
    "emoji": "🎙️",
    "requires": {
      "optionalBins": ["qmd", "git"]
    },
    "notes": [
      "Access utilizing the /lenny command syntax (conceptual).",
      "Points to https://github.com/ChatPRD/lennys-podcast-transcripts.",
      "Requires one-time setup of the 'lenny' collection."
    ]
  }
}
---

# Lenny Search

Access and query the complete archive of **Lenny Rachitsky's Podcast Transcripts**. This skill helps you find specific advice, strategies, and stories from top product leaders and growth experts.

## 🚀 Usage

You can use the `/lenny` style command to trigger searches (or simply ask the bot to "search Lenny").

```bash
qmd query "how to hire a first PM" -c lenny
```

## 🛠️ One-Time Setup

To enable this skill, you need to download the transcripts and index them locally.

1.  **Clone the Repository:**
    ```bash
    mkdir -p ~/knowledge
    git clone https://github.com/ChatPRD/lennys-podcast-transcripts.git ~/knowledge/lennys-podcast-transcripts
    ```

2.  **Create the QMD Collection:**
    This tells QMD to scan the transcripts and create a searchable index named `lenny`.
    ```bash
    qmd collection add ~/knowledge/lennys-podcast-transcripts --name lenny --mask "**/*.md"
    ```

## 🔍 Search Capabilities

This skill uses QMD's hybrid search to find answers deep within the transcripts.

**Examples:**
- "What does Casey Winters say about growth loops?" -> `qmd query "Casey Winters growth loops" -c lenny`
- "Find advice on pricing strategies." -> `qmd query "pricing strategy" -c lenny`
- "Who talked about B2B sales?" -> `qmd query "B2B sales guest" -c lenny`

## 📄 Output Data
Transcripts include rich metadata that can be extracted with `--json`:
- **Guest Name** & Role
- **Company** affiliations
- **YouTube Link** (often with timestamps)

To update your local archive with new episodes:
```bash
cd ~/knowledge/lennys-podcast-transcripts && git pull && qmd update --pull
```
