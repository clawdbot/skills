---
name: github-kb
description: Manage a local GitHub knowledge base and provide GitHub search capabilities via gh CLI. Use when users ask about repos, PRs, issues, request to clone GitHub repositories, explore codebases, or need information about GitHub projects. Supports searching GitHub via gh CLI and managing local KB with GITHUB_KB.md catalog. Configure via GITHUB_TOKEN and GITHUB_KB_PATH environment variables.
---

# GitHub Knowledge Base

Manage a local GitHub knowledge base and provide GitHub search capabilities via gh CLI. Key file: GITHUB_KB.md at the root of the KB directory catalogs all projects with brief descriptions.

## Configuration

Set environment variables before use:
- `GITHUB_TOKEN` - GitHub Personal Access Token (optional, for private repos)
- `GITHUB_KB_PATH` - Path to local KB directory (default: `/home/node/clawd/github-kb`)

Example:
```bash
export GITHUB_TOKEN="ghp_xxxx..."
export GITHUB_KB_PATH="/your/path/github-kb"
```

**Token Privacy:** Never hardcode tokens. Inject via environment variables or container secrets.

## GitHub CLI (gh)

**Requirement:** GitHub CLI must be installed and authenticated.

**Installation:**
- **macOS:** `brew install gh`
- **Linux:** `apt install gh` or see [official install guide](https://github.com/cli/cli/blob/trunk/docs/install_linux.md)
- **Windows:** `winget install GitHub.cli`

**Authentication:**
```bash
# Interactive login
gh auth login

# Or use token from GITHUB_TOKEN env var
gh auth login --with-token <(echo "$GITHUB_TOKEN")
```

**Verify:** `gh auth status`

If `gh` is not installed or not authenticated, skip search operations and use only local KB features.

### Searching Repos

```bash
# Search repos by keyword
gh search repos <query> [--limit <n>]

# Examples:
gh search repos "typescript cli" --limit 10
gh search repos "language:python stars:>1000" --limit 20
gh search repos "topic:mcp" --limit 15
```

**Search qualifiers:**
- `language:<lang>` - Filter by programming language
- `stars:<n>` or `stars:><n>` - Filter by star count
- `topic:<name>` - Filter by topic
- `user:<owner>` - Search within a user's repos
- `org:<org>` - Search within an organization

### Searching Issues

```bash
gh search issues "react hooks bug" --limit 20
gh search issues "repo:facebook/react state:open" --limit 30
gh search issues "language:typescript label:bug" --limit 15
```

**Search qualifiers:**
- `repo:<owner/repo>` - Search in specific repository
- `state:open|closed` - Filter by issue state
- `author:<username>` - Filter by author
- `label:<name>` - Filter by label
- `language:<lang>` - Filter by repo language
- `comments:<n>` or `comments:><n>` - Filter by comment count

### Searching Pull Requests

```bash
# Search PRs
gh search prs <query> [--limit <n>]

# Examples:
gh search prs "repo:vercel/next.js state:open" --limit 30
gh search prs "language:go is:merged" --limit 15
```

**Search qualifiers:**
- `repo:<owner/repo>` - Search in specific repository
- `state:open|closed|merged` - Filter by PR state
- `author:<username>` - Filter by author
- `label:<name>` - Filter by label
- `language:<lang>` - Filter by repo language
- `is:merged|unmerged` - Filter by merge status

### Viewing PR/Issue Details

```bash
# View issue/PR details
gh issue view <number> --repo <owner/repo>
gh pr view <number> --repo <owner/repo>

# View with comments
gh issue view <number> --repo <owner/repo> --comments
gh pr view <number> --repo <owner/repo> --comments
```

## Local Knowledge Base Workflow

### Querying About a Repo in KB

1. Read GITHUB_KB.md to understand what projects exist
2. Locate the project directory under ${GITHUB_KB_PATH:-/home/node/clawd/github-kb}/

### Cloning a New Repo to KB

1. Search GitHub if the full repo name is not known
2. Clone to KB directory:
   ```bash
   git clone https://github.com/<owner>/<name>.git ${GITHUB_KB_PATH:-/home/node/clawd/github-kb}/<name>
   ```
3. Generate project description: Read README or key files to understand the project
4. Update GITHUB_KB.md: Add entry for the new repo following the existing format:
   ```markdown
   ### [<name>](/<name>)
   Brief one-line description of what the project does. Additional context if useful (key features, tech stack, etc.).
   ```
5. Confirm completion: Tell user the repo was cloned and where to find it

### Default Clone Location

If user says "clone X" without specifying a directory, default to ${GITHUB_KB_PATH:-/home/node/clawd/github-kb}/.

## GITHUB_KB.md Format

The catalog file follows this structure:

```markdown
# GitHub Knowledge Base

This directory contains X GitHub projects covering various domains.

---

## Category Name

### [project-name](/project-name)
Brief description of the project.
```

Maintain categorization and consistent formatting when updating.
