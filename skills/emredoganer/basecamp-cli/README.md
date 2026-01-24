# Basecamp CLI

A command-line interface for managing Basecamp (via the official bc3 API / 37signals Launchpad) projects, to-dos, messages, and campfires.

## Installation

```bash
npm install -g @emredoganer/basecamp-cli
```

## Setup

### 1. Create a Basecamp Integration

1. Go to [Basecamp Integrations](https://launchpad.37signals.com/integrations)
2. Click "Register another application"
3. Fill in the details:
   - Name: Your app name
   - Company: Your company
   - Website: Your website
   - Redirect URI: `http://localhost:9292/callback`
4. Note your Client ID and Client Secret

### 2. Configure Credentials

Set environment variables:

```bash
export BASECAMP_CLIENT_ID="your-client-id"
export BASECAMP_CLIENT_SECRET="your-client-secret"
```

Or configure via CLI:

```bash
basecamp auth configure --client-id "your-client-id" --client-secret "your-client-secret"
```

### 3. Login

```bash
basecamp auth login
```

This will open your browser for OAuth authentication.

## Usage

### Authentication

```bash
# Login via OAuth
basecamp auth login

# Check auth status
basecamp auth status

# Logout
basecamp auth logout
```

### Accounts

```bash
# List available accounts
basecamp accounts

# Set current account
basecamp account set <id>

# Show current account
basecamp account current
```

### Projects

```bash
# List all projects
basecamp projects list

# Get project details
basecamp projects get <id>

# Create a project
basecamp projects create --name "My Project" --description "Description"

# Archive a project
basecamp projects archive <id>
```

### To-do Lists

```bash
# List to-do lists in a project
basecamp todolists list --project <id>

# Create a to-do list
basecamp todolists create --project <id> --name "Tasks"
```

### To-dos

```bash
# List to-dos
basecamp todos list --project <id> --list <list-id>

# Show completed to-dos
basecamp todos list --project <id> --list <list-id> --completed

# Get to-do details
basecamp todos get <id> --project <project-id>

# Create a to-do
basecamp todos create --project <id> --list <list-id> --content "Task description"

# Create with options
basecamp todos create --project <id> --list <list-id> --content "Task" \
  --due "2024-12-31" --assignees "123,456"

# Update a to-do
basecamp todos update <id> --project <project-id> --content "Updated content"

# Complete a to-do
basecamp todos complete <id> --project <project-id>

# Uncomplete a to-do
basecamp todos uncomplete <id> --project <project-id>
```

### Messages

```bash
# List messages
basecamp messages list --project <id>

# Get message details
basecamp messages get <id> --project <project-id>

# Create a message
basecamp messages create --project <id> --subject "Subject" --content "<p>HTML content</p>"
```

### Campfires (Chat)

```bash
# List campfires
basecamp campfires list --project <id>

# Get recent messages
basecamp campfires lines --project <id> --campfire <campfire-id>

# Send a message
basecamp campfires send --project <id> --campfire <campfire-id> --message "Hello!"
```

### People

```bash
# List all people
basecamp people list

# List people in a project
basecamp people list --project <id>

# Get person details
basecamp people get <id>

# Get your profile
basecamp me
```

## Output Formats

All list and get commands support `--json` flag for JSON output:

```bash
basecamp projects list --json
basecamp todos get <id> --project <project-id> --json
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `BASECAMP_CLIENT_ID` | OAuth Client ID |
| `BASECAMP_CLIENT_SECRET` | OAuth Client Secret |
| `BASECAMP_REDIRECT_URI` | OAuth Redirect URI (default: `http://localhost:9292/callback`) |
| `BASECAMP_ACCESS_TOKEN` | Access token (alternative to OAuth flow) |

## License

MIT
