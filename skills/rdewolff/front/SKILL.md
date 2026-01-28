---
name: front
description: Front.app API for managing conversations, messages, comments, and team collaboration.
homepage: https://front.com
metadata: {"clawdbot":{"emoji":"📬","requires":{"bins":["curl"],"env":["FRONT_API_TOKEN"]},"primaryEnv":"FRONT_API_TOKEN"}}
---

# Front

Use Front's API to manage conversations, read/send messages, and collaborate with team comments.

## Setup

Get your API token from Front → Settings → Developers → API Tokens.
Store it in `~/.clawdbot/clawdbot.json`:
```json
{
  "skills": {
    "entries": {
      "front": {
        "apiKey": "YOUR_FRONT_API_TOKEN"
      }
    }
  }
}
```

Or set env: `FRONT_API_TOKEN=your_token`

## Quick Reference

### List Inboxes
```bash
{baseDir}/scripts/front.sh inboxes
```

### List Conversations
```bash
{baseDir}/scripts/front.sh conversations [inbox_id]      # Active conversations (unassigned + assigned)
{baseDir}/scripts/front.sh conversations --all           # Include archived
{baseDir}/scripts/front.sh conversations --archived      # Archived only
{baseDir}/scripts/front.sh conversations --unassigned    # Unassigned only
{baseDir}/scripts/front.sh conversations --assigned      # Assigned only
{baseDir}/scripts/front.sh conversations --limit 200     # Increase result limit (default: 100)
```

### Get Conversation Details
```bash
{baseDir}/scripts/front.sh conversation <conversation_id>
```

### List Messages in Conversation
```bash
{baseDir}/scripts/front.sh messages <conversation_id>
```

### Search Conversations
```bash
{baseDir}/scripts/front.sh search "query text"
{baseDir}/scripts/front.sh search "from:client@example.com"
{baseDir}/scripts/front.sh search "tag:urgent"
```

### Read Comments (Team Notes)
```bash
{baseDir}/scripts/front.sh comments <conversation_id>
```

### Add Comment (Team Note)
```bash
{baseDir}/scripts/front.sh add-comment <conversation_id> "Your team note here"
```

### Reply to Conversation
```bash
{baseDir}/scripts/front.sh reply <conversation_id> "Your reply message"
# With --draft flag to save as draft instead of sending:
{baseDir}/scripts/front.sh reply <conversation_id> "Draft message" --draft
```

### List Teammates
```bash
{baseDir}/scripts/front.sh teammates
```

### Assign Conversation
```bash
{baseDir}/scripts/front.sh assign <conversation_id> <teammate_id>
```

### Tag Conversation
```bash
{baseDir}/scripts/front.sh tag <conversation_id> <tag_id>
```

### List Tags
```bash
{baseDir}/scripts/front.sh tags
```

### Get Contact Info
```bash
{baseDir}/scripts/front.sh contact <contact_id_or_handle>
```

### List Drafts
```bash
{baseDir}/scripts/front.sh drafts [inbox_id]    # Search conversations for drafts
```
Note: Front API doesn't have a global drafts endpoint. This command checks active conversations for draft replies.

## Common Workflows

**Daily inbox review:**
```bash
# List unassigned open conversations
{baseDir}/scripts/front.sh conversations --unassigned --status open
```

**Find customer conversations:**
```bash
{baseDir}/scripts/front.sh search "from:customer@company.com"
```

**Add team context:**
```bash
{baseDir}/scripts/front.sh add-comment cnv_abc123 "Customer is VIP - handle with care"
```

## Notes

- API base: Auto-detected (company-specific, e.g., `https://company.api.frontapp.com`)
- Auth: Bearer token in header
- Rate limit: 120 requests/minute
- Conversation IDs start with `cnv_`
- Inbox IDs start with `inb_`
- Always confirm before sending replies

## API Limitations

- **No global search**: The `/conversations/search` endpoint may return 404 depending on API plan
- **No global drafts**: Drafts are stored per-conversation, not globally accessible
- **Conversations vs Inbox**: By default shows non-archived/non-deleted conversations (open, unassigned, assigned)
