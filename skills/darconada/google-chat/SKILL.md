---
name: google-chat
description: Send messages to Google Chat spaces and users via webhooks or OAuth. Use when you need to send notifications, alerts, or messages to Google Chat channels (spaces) or direct messages to specific users. Supports both incoming webhooks (for predefined channels) and OAuth 2.0 (for dynamic messaging to any space or user).
---

# Google Chat Messaging

Send messages to Google Chat using two methods:

1. **Webhooks** - Fast, pre-configured channels (messages appear as a bot)
2. **OAuth** - Dynamic messaging to any space or user (requires authentication)

## Quick Start

### Method 1: Webhooks (Recommended for Known Channels)

Send to a pre-configured channel:

```bash
python3 scripts/send_webhook.py "$WEBHOOK_URL" "Your message here"
```

Example with threading:
```bash
python3 scripts/send_webhook.py "$WEBHOOK_URL" "Reply message" --thread_key "unique-thread-id"
```

**Configuration:** Store webhooks in `google-chat-config.json`:

```json
{
  "webhooks": {
    "acs_engineering_network": "https://chat.googleapis.com/v1/spaces/...",
    "general": "https://chat.googleapis.com/v1/spaces/..."
  }
}
```

Read config and send:
```bash
WEBHOOK_URL=$(jq -r '.webhooks.acs_engineering_network' google-chat-config.json)
python3 scripts/send_webhook.py "$WEBHOOK_URL" "Deploy completed ✅"
```

### Method 2: OAuth (For Dynamic Messaging)

**First-time setup:**

1. Save OAuth credentials to a file (e.g., `google-chat-oauth-credentials.json`)
2. Run initial authentication (opens browser, saves token):

```bash
python3 scripts/send_oauth.py \
  --credentials google-chat-oauth-credentials.json \
  --token google-chat-token.json \
  --space "General" \
  "Test message"
```

**Send to a space by name:**
```bash
python3 scripts/send_oauth.py \
  --credentials google-chat-oauth-credentials.json \
  --token google-chat-token.json \
  --space "Engineering Network" \
  "Deploy completed"
```

**Note:** OAuth messages automatically include `🤖` emoji prefix. Use `--no-emoji` to disable this:
```bash
python3 scripts/send_oauth.py \
  --credentials google-chat-oauth-credentials.json \
  --token google-chat-token.json \
  --space "Engineering Network" \
  "Message without emoji" \
  --no-emoji
```

**List available spaces:**
```bash
python3 scripts/send_oauth.py \
  --credentials google-chat-oauth-credentials.json \
  --token google-chat-token.json \
  --list-spaces
```

**Send to a DM (requires existing space ID):**
```bash
# Note: Google Chat API doesn't support creating new DMs by email
# You need the space ID of an existing DM conversation
python3 scripts/send_oauth.py \
  --credentials google-chat-oauth-credentials.json \
  --token google-chat-token.json \
  --space-id "spaces/xxxxx" \
  "The report is ready"
```

**Send to space by ID (faster):**
```bash
python3 scripts/send_oauth.py \
  --credentials google-chat-oauth-credentials.json \
  --token google-chat-token.json \
  --space-id "spaces/AAAALtlqgVA" \
  "Direct message to space"
```

## Dependencies

Install required Python packages:

```bash
pip install google-auth-oauthlib google-auth-httplib2 google-api-python-client
```

**Required OAuth Scopes:**
- `https://www.googleapis.com/auth/chat.messages` - Send messages
- `https://www.googleapis.com/auth/chat.spaces` - Access space information
- `https://www.googleapis.com/auth/chat.memberships.readonly` - List space members (for DM identification)

## OAuth Setup Guide

If OAuth credentials don't exist yet:

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Select your project or create one
3. Enable **Google Chat API**
4. Go to **APIs & Services → Credentials**
5. Create **OAuth 2.0 Client ID** (Desktop app type)
6. Download JSON and save as `google-chat-oauth-credentials.json`

The credentials JSON should look like:
```json
{
  "installed": {
    "client_id": "...apps.googleusercontent.com",
    "client_secret": "GOCSPX-...",
    "redirect_uris": ["http://localhost"],
    ...
  }
}
```

## Webhook Setup Guide

To create a webhook for a Google Chat space:

1. Open Google Chat in browser
2. Go to the space
3. Click space name → **Apps & integrations**
4. Click **Manage webhooks** → **Add webhook**
5. Give it a name (e.g., "Agustin Networks")
6. Copy the webhook URL
7. Add to `google-chat-config.json`

## Choosing the Right Method

**Use Webhooks when:**
- Sending to the same channels repeatedly
- Messages should appear as a bot/service
- Speed is important (no OAuth handshake)
- Configuration is static

**Use OAuth when:**
- Sending to different spaces dynamically
- Messages should appear from your configured Google Chat App
- Space names are determined at runtime
- Need to list and discover available spaces

**OAuth Limitations:**
- Cannot create new DMs by email address (Google Chat API restriction)
- To send DMs, you need the space ID of an existing conversation
- Use `--list-spaces` to find available DM space IDs

## Message Formatting

Both methods support simple text. For advanced formatting (cards, buttons), construct JSON payloads:

**Webhook with card:**
```python
import json
import urllib.request

payload = {
    "cardsV2": [{
        "cardId": "unique-card-id",
        "card": {
            "header": {"title": "Deploy Status"},
            "sections": [{
                "widgets": [{
                    "textParagraph": {"text": "Production deploy completed successfully"}
                }]
            }]
        }
    }]
}

data = json.dumps(payload).encode("utf-8")
req = urllib.request.Request(webhook_url, data=data, headers={"Content-Type": "application/json"})
urllib.request.urlopen(req)
```

## Troubleshooting

**Webhook errors:**
- Verify webhook URL is correct and active
- Check space still exists and webhook wasn't deleted
- Ensure message isn't empty

**OAuth errors:**
- Run authentication flow again if token expired
- Verify Google Chat API is enabled in Cloud Console
- Check user has access to the target space
- For DMs, ensure user email is correct and in same workspace

**Permission errors:**
- Webhooks: Must be member of the space
- OAuth: Must have access to target space or user
- Corporate Workspace: Some features may be restricted by admin policies

## Examples

**Deploy notification to engineering channel:**
```bash
WEBHOOK=$(jq -r '.webhooks.acs_engineering_network' google-chat-config.json)
python3 scripts/send_webhook.py "$WEBHOOK" "🚀 Production deploy v2.1.0 completed"
```

**Alert specific user about task:**
```bash
python3 scripts/send_oauth.py \
  --credentials google-chat-oauth-credentials.json \
  --token google-chat-token.json \
  --dm juan@empresa.com \
  "Your report is ready for review: https://docs.company.com/report"
```

**Thread multiple messages together (webhook):**
```bash
WEBHOOK=$(jq -r '.webhooks.general' google-chat-config.json)
THREAD_KEY="deploy-$(date +%s)"

python3 scripts/send_webhook.py "$WEBHOOK" "Starting deploy..." --thread_key "$THREAD_KEY"
# ... deployment happens ...
python3 scripts/send_webhook.py "$WEBHOOK" "Deploy completed ✅" --thread_key "$THREAD_KEY"
```
