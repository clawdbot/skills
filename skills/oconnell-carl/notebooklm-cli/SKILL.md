---
name: notebooklm-cli
description: Comprehensive CLI for Google NotebookLM including notebooks, sources, audio podcasts, reports, quizzes, flashcards, mind maps, slides, infographics, videos, and data tables. Use when working with NotebookLM programmatically: managing notebooks/sources, generating audio overviews (podcasts), creating study materials (quizzes, flashcards), producing presentations (slides, infographics), or querying sources via chat.
---

# NotebookLM CLI

## Overview

This skill provides complete access to Google NotebookLM through a command-line interface. Manage notebooks, sources, and generate various content formats including audio podcasts, reports, quizzes, flashcards, mind maps, slides, infographics, videos, and data tables.

## When to Use This Skill

Use this skill when:
- Managing NotebookLM notebooks and sources programmatically
- Generating audio overviews (podcasts) from notebook sources
- Creating study materials: quizzes, flashcards, reports
- Producing visual content: slides, infographics, mind maps, videos
- Querying sources via chat or one-shot questions
- Researching and importing new sources automatically

## Quick Start

### Authentication

```bash
nlm login
```

Launches Chrome, navigates to NotebookLM, and extracts session cookies. Requires Google Chrome installed.

### List Notebooks

```bash
nlm notebook list
```

### Create Notebook and Add Sources

```bash
nlm notebook create "My Research"
nlm source add <notebook-id> --url "https://example.com/article"
nlm source add <notebook-id> --text "Your content here" --title "My Notes"
```

### Generate Content (All Types)

All generation commands require `--confirm` or `-y`:

```bash
nlm audio create <id> --confirm          # Podcast
nlm report create <id> --confirm         # Briefing doc or study guide
nlm quiz create <id> --confirm           # Quiz questions
nlm flashcards create <id> --confirm     # Flashcards
nlm mindmap create <id> --confirm        # Mind map
nlm slides create <id> --confirm         # Slide deck
nlm infographic create <id> --confirm    # Infographic
nlm video create <id> --confirm          # Video overview
nlm data-table create <id> "description" --confirm  # Data table
```

## Authentication

| Command | Description |
|---------|-------------|
| `nlm login` | Authenticate with NotebookLM (opens Chrome) |
| `nlm login --check` | Verify current credentials |
| `nlm auth status` | Check session validity |
| `nlm auth list` | List all profiles |
| `nlm auth delete <profile> --confirm` | Delete a profile |
| `nlm login --profile <name>` | Login to specific profile |

Sessions last ~20 minutes. Re-authenticate with `nlm login` if commands fail.

## Notebook Management

| Command | Description |
|---------|-------------|
| `nlm notebook list` | List all notebooks |
| `nlm notebook create "Title"` | Create a new notebook |
| `nlm notebook get <id>` | Get notebook details |
| `nlm notebook describe <id>` | AI-generated summary |
| `nlm notebook query <id> "question"` | Chat with sources |
| `nlm notebook delete <id> --confirm` | Delete a notebook |

## Source Management

| Command | Description |
|---------|-------------|
| `nlm source list <notebook-id>` | List sources in notebook |
| `nlm source list <notebook-id> --drive` | Show Drive sources with freshness |
| `nlm source add <id> --url "..."` | Add URL or YouTube source |
| `nlm source add <id> --text "..." --title "..."` | Add pasted text |
| `nlm source add <id> --drive <doc-id>` | Add Google Drive document |
| `nlm source describe <source-id>` | AI summary of source |
| `nlm source content <source-id>` | Get raw text content |
| `nlm source stale <notebook-id>` | List outdated Drive sources |
| `nlm source sync <notebook-id> --confirm` | Sync Drive sources |

## Content Generation

All generation commands require `--confirm` or `-y`:

### Media Types

| Command | Output |
|---------|--------|
| `nlm audio create <id> --confirm` | Audio podcast overview |
| `nlm report create <id> --confirm` | Briefing doc or study guide |
| `nlm quiz create <id> --confirm` | Quiz questions |
| `nlm flashcards create <id> --confirm` | Flashcards |
| `nlm mindmap create <id> --confirm` | Mind map |
| `nlm slides create <id> --confirm` | Slide deck |
| `nlm infographic create <id> --confirm` | Infographic |
| `nlm video create <id> --confirm` | Video overview |
| `nlm data-table create <id> "description" --confirm` | Data table extraction |

## Studio (Artifact Management)

| Command | Description |
|---------|-------------|
| `nlm studio status <notebook-id>` | List all generated artifacts |
| `nlm studio delete <notebook-id> <artifact-id> --confirm` | Delete an artifact |

## Chat

| Command | Description |
|---------|-------------|
| `nlm chat start <notebook-id>` | Start interactive REPL session |
| `nlm chat configure <notebook-id>` | Configure chat goal and response style |
| `nlm notebook query <id> "question"` | One-shot question (no session) |

Chat REPL commands: `/sources`, `/clear`, `/help`, `/exit`

## Research

| Command | Description |
|---------|-------------|
| `nlm research start "query" --notebook-id <id>` | Web search (~30s) |
| `nlm research start "query" --notebook-id <id> --mode deep` | Deep research (~5min) |
| `nlm research start "query" --notebook-id <id> --source drive` | Search Google Drive |
| `nlm research status <notebook-id>` | Check research progress |
| `nlm research import <notebook-id> <task-id>` | Import discovered sources |

## Aliases (UUID Shortcuts)

```bash
nlm alias set myproject <uuid>           # Create alias
nlm notebook get myproject               # Use alias
nlm alias list                           # List all aliases
nlm alias get myproject                  # Resolve to UUID
nlm alias delete myproject               # Remove alias
```

## Output Formats

Most list commands support multiple formats:

```bash
nlm notebook list                # Rich table (default)
nlm notebook list --json         # JSON output
nlm notebook list --quiet        # IDs only (for scripting)
nlm notebook list --title        # "ID: Title" format
nlm notebook list --full         # All columns
```

## Profiles (Multiple Accounts)

```bash
nlm login --profile work         # Login to profile
nlm notebook list --profile work # Use profile
nlm auth list                    # List all profiles
nlm auth delete work --confirm   # Delete profile
```

## Configuration

```bash
nlm config show                  # Show current configuration
nlm config get <key>             # Get specific setting
nlm config set <key> <value>     # Update setting
```

## AI Documentation

For AI assistants, generate comprehensive documentation:

```bash
nlm --ai
```

Outputs 400+ lines covering all commands, authentication flow, error handling, task sequences, and automation tips.

## References

- [Command Reference](references/commands.md) - Complete command signatures
- [Troubleshooting](references/troubleshooting.md) - Error diagnosis and solutions
- [Workflows](references/workflows.md) - End-to-end task sequences