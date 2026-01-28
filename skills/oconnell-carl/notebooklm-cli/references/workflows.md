# Workflows

## Workflow 1: Create Audio Podcast from Research Sources

### Goal
Generate an audio podcast overview from notebook sources.

### Steps

1. **Authenticate**
   ```bash
   nlm login
   ```

2. **Create Notebook**
   ```bash
   nlm notebook create "Podcast Project"
   ```
   Note the notebook ID from output.

3. **Add Sources**
   ```bash
   nlm source add <notebook-id> --url "https://example.com/article1"
   nlm source add <notebook-id> --url "https://example.com/article2"
   nlm source add <notebook-id> --text "Additional notes here" --title "My Notes"
   ```

4. **Verify Sources**
   ```bash
   nlm source list <notebook-id>
   ```

5. **Generate Audio**
   ```bash
   nlm audio create <notebook-id> --confirm
   ```

6. **Check Status**
   ```bash
   nlm studio status <notebook-id>
   ```

### Complete One-Liner (After Setup)
```bash
nlm audio create <notebook-id> --confirm && nlm studio status <notebook-id>
```

---

## Workflow 2: Create Study Materials from Documents

### Goal
Generate quizzes, flashcards, and reports from notebook sources for studying.

### Steps

1. **Setup Notebook**
   ```bash
   nlm notebook create "Study Materials"
   nlm source add <notebook-id> --url "https://lecture-notes.edu/course1"
   nlm source add <notebook-id> --drive <doc-id>
   ```

2. **Generate All Study Materials**
   ```bash
   nlm quiz create <notebook-id> --confirm
   nlm flashcards create <notebook-id> --confirm
   nlm report create <notebook-id> --confirm
   ```

3. **Review Generated Content**
   ```bash
   nlm studio status <notebook-id>
   ```

### Alternative: Interactive Chat
```bash
nlm notebook query <notebook-id> "What are the key concepts in these sources?"
```

---

## Workflow 3: Create Presentation from Research

### Goal
Generate slides and infographics for presenting notebook content.

### Steps

1. **Prepare Notebook**
   ```bash
   nlm notebook create "Q4 Report"
   nlm source add <notebook-id> --url "https://company-reports.com/q4-summary"
   ```

2. **Generate Visual Content**
   ```bash
   nlm slides create <notebook-id> --confirm
   nlm infographic create <notebook-id> --confirm
   ```

3. **Check Outputs**
   ```bash
   nlm studio status <notebook-id>
   ```

### For Multiple Presentation Types
```bash
nlm mindmap create <notebook-id> --confirm
nlm video create <notebook-id> --confirm
```

---

## Workflow 4: Research and Import Sources

### Goal
Automatically discover and import relevant sources for a notebook.

### Steps

1. **Create Notebook**
   ```bash
   nlm notebook create "AI Research"
   ```

2. **Start Research**
   ```bash
   nlm research start "large language model prompting techniques" --notebook-id <id>
   ```

3. **Check Progress**
   ```bash
   nlm research status <notebook-id>
   ```

4. **Import Results**
   Once research completes:
   ```bash
   nlm research import <notebook-id> <task-id>
   ```

### Deep Research (More Thorough)
```bash
nlm research start "machine learning transformers architecture" --notebook-id <id> --mode deep
```

---

## Workflow 5: Interactive Q&A Session

### Goal
Have an interactive conversation with notebook sources.

### Steps

1. **Start Chat Session**
   ```bash
   nlm chat start <notebook-id>
   ```

2. **Ask Questions**
   ```
   /sources
   "What are the main arguments in these documents?"
   "Can you summarize the key points?"
   "What evidence supports claim X?"
   ```

3. **End Session**
   ```
   /exit
   ```

### One-Shot Query (No Session)
```bash
nlm notebook query <notebook-id> "Summarize the main conclusions from these sources."
```

---

## Workflow 6: Manage Multiple Google Accounts

### Goal
Work with different Google accounts for different notebooks.

### Steps

1. **Login to Work Account**
   ```bash
   nlm login --profile work
   ```

2. **Create Work Notebook**
   ```bash
   nlm notebook create "Work Project"
   ```

3. **Switch to Personal Account**
   ```bash
   nlm login --profile personal
   ```

4. **Create Personal Notebook**
   ```bash
   nlm notebook create "Personal Research"
   ```

5. **List Profiles**
   ```bash
   nlm auth list
   ```

### Using Specific Profile
```bash
nlm notebook list --profile work
nlm audio create <id> --profile work --confirm
```

---

## Workflow 7: Sync Google Drive Sources

### Goal
Keep Drive sources up to date with latest changes.

### Steps

1. **List Notebook**
   ```bash
   nlm notebook list
   ```

2. **Check Stale Sources**
   ```bash
   nlm source stale <notebook-id>
   ```

3. **Sync Sources**
   ```bash
   nlm source sync <notebook-id> --confirm
   ```

### Quick Sync with Drive-Only Listing
```bash
nlm source list <notebook-id> --drive -S
```

---

## Workflow 8: Create Data Tables from Sources

### Goal
Extract structured data tables from notebook sources.

### Steps

1. **Create Notebook with Data Sources**
   ```bash
   nlm notebook create "Data Analysis"
   nlm source add <notebook-id> --url "https://data-report.com/statistics"
   ```

2. **Generate Data Table**
   ```bash
   nlm data-table create <notebook-id> "quarterly revenue by region" --confirm
   ```

3. **View Results**
   ```bash
   nlm studio status <notebook-id>
   ```

### Multiple Data Extractions
```bash
nlm data-table create <notebook-id> "customer demographics breakdown" --confirm
nlm data-table create <notebook-id> "sales performance metrics" --confirm
```

---

## Workflow 9: Use Aliases for Frequently Accessed Notebooks

### Goal
Create memorable shortcuts for long notebook UUIDs.

### Steps

1. **List Notebooks**
   ```bash
   nlm notebook list
   ```

2. **Create Alias**
   ```bash
   nlm alias set myproject abc123-def456-7890-...
   ```

3. **Use Alias Everywhere**
   ```bash
   nlm notebook get myproject
   nlm source list myproject
   nlm audio create myproject --confirm
   ```

4. **Manage Aliases**
   ```bash
   nlm alias list
   nlm alias get myproject
   nlm alias delete myproject
   ```

---

## Workflow 10: Complete Project Setup to Generation

### Goal
Full workflow: authenticate, create notebook, add sources, generate multiple content types.

### Steps

1. **Authenticate**
   ```bash
   nlm login
   ```

2. **Create Project Notebook**
   ```bash
   nlm notebook create "Complete Project"
   ```

3. **Add Multiple Sources**
   ```bash
   nlm source add <id> --url "https://article1.com"
   nlm source add <id> --url "https://article2.com"
   nlm source add <id> --text "Additional context" --title "Context Notes"
   ```

4. **Generate All Content Types**
   ```bash
   nlm audio create <id> --confirm
   nlm report create <id> --confirm
   nlm quiz create <id> --confirm
   nlm flashcards create <id> --confirm
   nlm slides create <id> --confirm
   nlm mindmap create <id> --confirm
   ```

5. **Review All Artifacts**
   ```bash
   nlm studio status <id>
   ```

---

## Workflow 11: Batch Operations with JSON Output

### Goal
Script multiple operations using JSON output for parsing.

### Steps

1. **List All Notebooks as JSON**
   ```bash
   nlm notebook list --json > notebooks.json
   ```

2. **Extract Notebook IDs**
   ```bash
   cat notebooks.json | jq -r '.[].id' | while read id; do
     nlm audio create "$id" --confirm
   done
   ```

3. **Check Status in Batch**
   ```bash
   for id in $(cat notebooks.json | jq -r '.[].id'); do
     echo "Notebook: $id"
     nlm studio status "$id"
   done
   ```

### Quiet Mode for Scripting
```bash
nlm notebook list --quiet | xargs -I {} nlm audio create {} --confirm
```

---

## Workflow 12: Use AI Documentation for Learning

### Goal
Get comprehensive documentation for AI assistant consumption.

### Steps

1. **Generate AI Documentation**
   ```bash
   nlm --ai > nlm-ai-docs.md
   ```

2. **Use in Claude/GPT Context**
   Paste the output to teach AI assistants about nlm usage.

3. **Quick Reference**
   ```bash
   nlm --ai | head -100
   ```

### Include in Skill Documentation
The `--ai` output includes:
- All command signatures
- Authentication flow
- Error handling procedures
- Task sequences
- AI automation tips