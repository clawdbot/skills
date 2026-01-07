---
name: ticktick
description: Manage TickTick tasks and projects from the command line with OAuth2 auth, batch operations, and rate limit handling.
---

# TickTick CLI Skill

Manage TickTick tasks and projects from the command line.

## Setup

### 1. Register a TickTick Developer App

1. Go to [TickTick Developer Center](https://developer.ticktick.com/manage)
2. Create a new application
3. Set the redirect URI to `http://localhost:8080`
4. Note your `Client ID` and `Client Secret`

### 2. Authenticate

```bash
# Set credentials and start OAuth flow
bun run scripts/ticktick.ts auth --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET

# Check authentication status
bun run scripts/ticktick.ts auth --status

# Logout (clear tokens, keep credentials)
bun run scripts/ticktick.ts auth --logout
```

### Headless / Manual Authentication

```bash
# Use manual mode on headless servers
bun run scripts/ticktick.ts auth --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET --manual
```

This prints an authorization URL. Open it in a browser, approve access, then copy the full redirect URL (it looks like `http://localhost:8080/?code=XXXXX&state=STATE`) and paste it back into the CLI.

The CLI will open your browser to authorize access. After approving, tokens are stored in `~/.clawdbot/credentials/ticktick-cli/config.json`.

## Commands

### List Tasks

```bash
# List all tasks
bun run scripts/ticktick.ts tasks

# List tasks from a specific project
bun run scripts/ticktick.ts tasks --list "Work"

# Filter by status
bun run scripts/ticktick.ts tasks --status pending
bun run scripts/ticktick.ts tasks --status completed

# JSON output
bun run scripts/ticktick.ts tasks --json
```

### Create Task

```bash
# Basic task creation
bun run scripts/ticktick.ts task "Buy groceries" --list "Personal"

# With description and priority
bun run scripts/ticktick.ts task "Review PR" --list "Work" --content "Check the new auth changes" --priority high

# With due date
bun run scripts/ticktick.ts task "Submit report" --list "Work" --due tomorrow
bun run scripts/ticktick.ts task "Plan vacation" --list "Personal" --due "in 7 days"
bun run scripts/ticktick.ts task "Meeting" --list "Work" --due "2024-12-25"

# With tags
bun run scripts/ticktick.ts task "Research" --list "Work" --tag research important
```

### Update Task

```bash
# Update by task name or ID
bun run scripts/ticktick.ts task "Buy groceries" --update --priority medium
bun run scripts/ticktick.ts task "abc123" --update --due tomorrow --content "Updated notes"

# Limit search to specific project
bun run scripts/ticktick.ts task "Review PR" --update --list "Work" --priority low
```

### Complete Task

```bash
# Mark task as complete
bun run scripts/ticktick.ts complete "Buy groceries"

# Complete with project filter
bun run scripts/ticktick.ts complete "Review PR" --list "Work"
```

### Abandon Task (Won't Do)

```bash
# Mark task as won't do
bun run scripts/ticktick.ts abandon "Old task"

# Abandon with project filter
bun run scripts/ticktick.ts abandon "Obsolete item" --list "Do"
```

### Batch Abandon (Multiple Tasks)

```bash
# Abandon multiple tasks in a single API call
bun run scripts/ticktick.ts batch-abandon <taskId1> <taskId2> <taskId3>

# With JSON output
bun run scripts/ticktick.ts batch-abandon abc123def456... xyz789... --json
```

Note: `batch-abandon` requires task IDs (24-character hex strings), not task names. Use `tasks --json` to get task IDs first.

### List Projects

```bash
# List all projects
bun run scripts/ticktick.ts lists

# JSON output
bun run scripts/ticktick.ts lists --json
```

### Create Project

```bash
# Create new project
bun run scripts/ticktick.ts list "New Project"

# With color
bun run scripts/ticktick.ts list "Work Tasks" --color "#FF5733"
```

### Update Project

```bash
# Rename project
bun run scripts/ticktick.ts list "Old Name" --update --name "New Name"

# Change color
bun run scripts/ticktick.ts list "Work" --update --color "#00FF00"
```

## Options Reference

### Priority Levels
- `none` - No priority (default)
- `low` - Low priority
- `medium` - Medium priority
- `high` - High priority

### Due Date Formats
- `today` - Due today
- `tomorrow` - Due tomorrow
- `in N days` - Due in N days (e.g., "in 3 days")
- `next monday` - Next occurrence of weekday
- ISO date - `YYYY-MM-DD` or full ISO format

### Global Options
- `--json` - Output results in JSON format (useful for scripting)
- `--help` - Show help for any command

## Agent Usage Tips

When using this skill as an AI agent:

1. **Always use `--json` flag** for machine-readable output
2. **List projects first** with `lists --json` to get valid project IDs
3. **Use project IDs** rather than names when possible for reliability
4. **Check task status** before completing to avoid errors

Example agent workflow:
```bash
# 1. Get available projects
bun run scripts/ticktick.ts lists --json

# 2. Create a task in a specific project
bun run scripts/ticktick.ts task "Agent task" --list "PROJECT_ID" --priority high --json

# 3. Later, mark it complete
bun run scripts/ticktick.ts complete "Agent task" --list "PROJECT_ID" --json
```

## Configuration

Tokens are stored in `~/.clawdbot/credentials/ticktick-cli/config.json`:
```json
{
  "clientId": "YOUR_CLIENT_ID",
  "clientSecret": "YOUR_CLIENT_SECRET",
  "accessToken": "...",
  "refreshToken": "...",
  "tokenExpiry": 1234567890000,
  "redirectUri": "http://localhost:8080"
}
```

Note: Credentials are stored in plaintext. The CLI attempts to set file permissions to 700/600; treat this file as sensitive.

The CLI automatically refreshes tokens when they expire.

## Troubleshooting

### "Not authenticated" error
Run `bun run scripts/ticktick.ts auth` to authenticate.

### "Project not found" error
Use `bun run scripts/ticktick.ts lists` to see available projects and their IDs.

### "Task not found" error
- Check the task title matches exactly (case-insensitive)
- Try using the task ID instead
- Use `--list` to narrow the search to a specific project

### Token expired errors
The CLI should auto-refresh tokens. If issues persist, run `bun run scripts/ticktick.ts auth` again.

## API Notes

This CLI uses the [TickTick Open API v1](https://developer.ticktick.com/api).

### Rate Limits
- **100 requests per minute**
- **300 requests per 5 minutes**

The CLI makes multiple API calls per operation (listing projects to find task), so bulk operations can hit limits quickly.

### Batch Endpoint
The CLI supports TickTick's batch endpoint for bulk operations:
```
POST https://api.ticktick.com/open/v1/batch/task
{
  "add": [...],    // CreateTaskInput[]
  "update": [...], // UpdateTaskInput[]
  "delete": [...]  // { taskId, projectId }[]
}
```
Use `batch-abandon` to abandon multiple tasks in one API call. The batch API method is also exposed for programmatic use.

### Other Limitations
- Maximum 500 tasks per project
- Some advanced features (focus time, habits) not supported by the API
