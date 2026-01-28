# Command Reference

## Authentication Commands

### nlm login
Authenticate with NotebookLM by launching Chrome and extracting session cookies.

```bash
nlm login
nlm login --check
nlm login --profile <name>
```

**Requirements:**
- Google Chrome must be installed
- Requires user interaction in browser

### nlm auth status
Check if current session is valid.

```bash
nlm auth status
```

### nlm auth list
List all authenticated profiles.

```bash
nlm auth list
```

### nlm auth delete
Delete a specific profile.

```bash
nlm auth delete <profile> --confirm
```

## Notebook Commands

### nlm notebook list
List all notebooks.

```bash
nlm notebook list
nlm notebook list --json
nlm notebook list --quiet
nlm notebook list --title
nlm notebook list --full
```

### nlm notebook create
Create a new notebook.

```bash
nlm notebook create "Notebook Title"
```

### nlm notebook get
Get notebook details.

```bash
nlm notebook get <notebook-id>
```

### nlm notebook describe
Get AI-generated summary of notebook.

```bash
nlm notebook describe <notebook-id>
```

### nlm notebook query
Chat with sources in notebook (one-shot question).

```bash
nlm notebook query <notebook-id> "Your question here"
```

### nlm notebook delete
Delete a notebook.

```bash
nlm notebook delete <notebook-id> --confirm
```

## Source Commands

### nlm source list
List sources in a notebook.

```bash
nlm source list <notebook-id>
nlm source list <notebook-id> --drive
nlm source list <notebook-id> --drive -S
```

### nlm source add
Add a source to a notebook.

```bash
nlm source add <notebook-id> --url "https://example.com/article"
nlm source add <notebook-id> --url "https://youtube.com/watch?v=..."
nlm source add <notebook-id> --text "Your content here" --title "Source Title"
nlm source add <notebook-id> --drive <document-id>
```

### nlm source describe
Get AI summary of a source.

```bash
nlm source describe <source-id>
```

### nlm source content
Get raw text content of a source.

```bash
nlm source content <source-id>
```

### nlm source stale
List outdated Google Drive sources.

```bash
nlm source stale <notebook-id>
```

### nlm source sync
Sync Google Drive sources.

```bash
nlm source sync <notebook-id> --confirm
```

## Content Generation Commands

All content generation commands require `--confirm` or `-y` flag.

### nlm audio create
Generate audio overview (podcast).

```bash
nlm audio create <notebook-id> --confirm
```

### nlm report create
Generate briefing doc or study guide.

```bash
nlm report create <notebook-id> --confirm
```

### nlm quiz create
Generate quiz questions.

```bash
nlm quiz create <notebook-id> --confirm
```

### nlm flashcards create
Generate flashcards.

```bash
nlm flashcards create <notebook-id> --confirm
```

### nlm mindmap create
Generate mind map.

```bash
nlm mindmap create <notebook-id> --confirm
```

### nlm slides create
Generate slide deck.

```bash
nlm slides create <notebook-id> --confirm
```

### nlm infographic create
Generate infographic.

```bash
nlm infographic create <notebook-id> --confirm
```

### nlm video create
Generate video overview.

```bash
nlm video create <notebook-id> --confirm
```

### nlm data-table create
Extract data as table.

```bash
nlm data-table create <notebook-id> "description" --confirm
```

## Studio Commands

### nlm studio status
List all generated artifacts in a notebook.

```bash
nlm studio status <notebook-id>
```

### nlm studio delete
Delete a generated artifact.

```bash
nlm studio delete <notebook-id> <artifact-id> --confirm
```

## Chat Commands

### nlm chat start
Start interactive REPL session.

```bash
nlm chat start <notebook-id>
```

**REPL Commands:**
- `/sources` - Show sources
- `/clear` - Clear conversation
- `/help` - Show help
- `/exit` - Exit session

### nlm chat configure
Configure chat goal and response style.

```bash
nlm chat configure <notebook-id>
```

## Research Commands

### nlm research start
Start research to discover and import sources.

```bash
nlm research start "search query" --notebook-id <id>
nlm research start "search query" --notebook-id <id> --mode deep
nlm research start "search query" --notebook-id <id> --source drive
```

### nlm research status
Check research progress.

```bash
nlm research status <notebook-id>
```

### nlm research import
Import discovered sources from research.

```bash
nlm research import <notebook-id> <task-id>
```

## Alias Commands

### nlm alias set
Create an alias for a UUID.

```bash
nlm alias set <alias-name> <uuid>
```

### nlm alias list
List all aliases.

```bash
nlm alias list
```

### nlm alias get
Resolve an alias to its UUID.

```bash
nlm alias get <alias-name>
```

### nlm alias delete
Delete an alias.

```bash
nlm alias delete <alias-name>
```

## Configuration Commands

### nlm config show
Show current configuration.

```bash
nlm config show
```

### nlm config get
Get a specific configuration value.

```bash
nlm config get <key>
```

### nlm config set
Update a configuration value.

```bash
nlm config set <key> <value>
```

## Utility Commands

### nlm --ai
Output comprehensive documentation for AI assistants.

```bash
nlm --ai
```

### nlm --install-completion
Install shell tab completion.

```bash
nlm --install-completion
```

### nlm --show-completion
Show completion script for manual installation.

```bash
nlm --show-completion
```

## Output Format Options

### Rich Table (Default)
```bash
nlm notebook list
```

### JSON
```bash
nlm notebook list --json
```

### Quiet (IDs Only)
```bash
nlm notebook list --quiet
```

### Title Format
```bash
nlm notebook list --title
```

### Full Details
```bash
nlm notebook list --full
```

### URL Format
```bash
nlm source list --url
```

## Profile Options

Most commands support `--profile` flag:

```bash
nlm notebook list --profile <profile-name>
nlm audio create <id> --profile <profile-name> --confirm
```