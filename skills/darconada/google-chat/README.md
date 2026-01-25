# Google Chat Skill

Send messages to Google Chat spaces and users via webhooks or OAuth 2.0.

## Features

✅ **Webhook support** - Send to predefined channels (messages appear as configured bot)  
✅ **OAuth support** - Send to any space dynamically (messages appear from your Google Chat App)  
✅ **Space discovery** - List all available spaces and DMs  
✅ **Automatic emoji prefix** - OAuth messages include 🤖 emoji (configurable)  
✅ **Message threading** - Support for threaded conversations

## Quick Start

### Webhook (fastest)
```bash
python3 scripts/send_webhook.py "$WEBHOOK_URL" "Your message"
```

### OAuth (flexible)
```bash
# First time: authenticate
python3 scripts/send_oauth.py \
  --credentials oauth-creds.json \
  --token token.json \
  --space "Channel Name" \
  "Your message"

# List spaces
python3 scripts/send_oauth.py \
  --credentials oauth-creds.json \
  --token token.json \
  --list-spaces
```

## Setup Requirements

**For webhooks:**
- Create incoming webhook in Google Chat space settings

**For OAuth:**
1. Google Cloud Console → Create OAuth 2.0 credentials (Desktop app)
2. Enable Google Chat API
3. Download credentials JSON
4. Run authentication flow (opens browser)

## Configuration Example

See `references/config-example.json` for a config template with multiple webhooks.

## Limitations

- **OAuth cannot create new DMs by email** - This is a Google Chat API limitation
- To send DMs via OAuth, you need the space ID of an existing conversation
- Use `--list-spaces` to discover available DM space IDs

## Full Documentation

See `SKILL.md` for complete usage, examples, and troubleshooting.

---

**Created:** 2026-01-25  
**Tested with:** Google Workspace
