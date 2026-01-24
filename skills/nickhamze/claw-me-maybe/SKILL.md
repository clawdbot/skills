---
name: claw-me-maybe
version: 1.2.0
description: Beeper integration for Clawdbot. Send messages and search chats across WhatsApp, Telegram, Signal, Discord, Slack, Instagram, iMessage, LinkedIn, Facebook Messenger, Google Messages via Beeper Desktop API. Reactions, reminders, attachments, mark as read. Unified multi-platform messaging automation—just ask.
author: nickhamze
keywords: Beeper, messaging, WhatsApp, Telegram, Signal, Discord, Slack, Instagram, iMessage, LinkedIn, Facebook Messenger, Google Messages, Google Chat, chat automation, unified messaging, Desktop API, send messages, search messages, reactions, reminders, multi-platform, cross-platform messaging, chat search, message history, unread messages
metadata: {"clawdbot":{"emoji":"📟","skillKey":"claw-me-maybe","requires":{"bins":["curl"]},"homepage":"https://www.beeper.com","defaultEnv":{"BEEPER_API_URL":"http://localhost:23373"}}}
user-invocable: true
---

# Claw Me Maybe - Beeper Desktop API & Multi-Platform Messaging 📟

**Your lobster just got a Beeper.**

Finally, your Clawdbot can reach you (and everyone else) across *every* chat platform. WhatsApp? Telegram? Signal? Discord? Slack? Instagram DMs? LinkedIn? iMessage? **All of them. One skill. One claw.**

Powered by [Beeper](https://www.beeper.com) - the app that unifies all your chats.

## What Can Your Lobster Do With Beeper?

🔍 **Search Everything** - "What did Sarah say about the project last week?" Your lobster will dig through all your Beeper chats instantly.

💬 **Send Messages Anywhere** - "Tell Mom I'll be late" - and it goes to WhatsApp. "Message the team on Slack" - done. No app switching.

📊 **Summarize Your Inbox** - "What did I miss?" Get a digest of unread messages across all your Beeper networks.

🔔 **Set Reminders** - "Remind me to reply to this chat tomorrow" - your lobster remembers so you don't have to.

📎 **Grab Attachments** - Download files, images, and media from any Beeper conversation.

😀 **React to Messages** - Add emoji reactions to any message across any Beeper network.

✅ **Mark as Read** - Keep your Beeper inbox tidy by marking conversations as read.

## Supported Beeper Networks

Your Clawdbot can reach you on **any platform Beeper supports**:

| Platform | Status |
|----------|--------|
| WhatsApp | ✅ Full Support |
| Telegram | ✅ Full Support |
| Signal | ✅ Full Support |
| Discord | ✅ Full Support |
| Slack | ✅ Full Support |
| Instagram DMs | ✅ Full Support |
| Facebook Messenger | ✅ Full Support |
| LinkedIn Messages | ✅ Full Support |
| X (Twitter) DMs | ✅ Full Support |
| Google Messages | ✅ Full Support |
| Google Chat | ✅ Full Support |
| iMessage | ✅ macOS only |

**One skill. Twelve platforms. Infinite possibilities.**

## Quick Start

### 1. Get Beeper

Don't have Beeper yet? [Download it free](https://www.beeper.com/download) - it's the app that brings all your chats together.

### 2. Enable the Beeper Desktop API

Open Beeper Desktop → **Settings** → **Developers** → Toggle **"Beeper Desktop API"** ON

That's it. Your lobster now has a direct line to all your chats.

### 3. (Optional) Add Your Beeper Token

For smoother automation, grab an access token:

1. Beeper Desktop → Settings → Developers
2. Click "Create Access Token"
3. Add to `~/.clawdbot/clawdbot.json`:

```json
{
  "skills": {
    "entries": {
      "claw-me-maybe": {
        "enabled": true,
        "env": {
          "BEEPER_ACCESS_TOKEN": "your-token-here"
        }
      }
    }
  }
}
```

Note: `BEEPER_API_URL` defaults to `http://localhost:23373` - no need to set it unless you're running Beeper on a different port.

## Talk to Your Lobster

Once set up, just ask naturally:

> "Show me my unread messages in Beeper"

> "Search my Beeper chats for messages about dinner plans"

> "Send a WhatsApp message to John saying I'm on my way"

> "What's the latest in my Signal group chat?"

> "Message the #general channel on Slack: standup in 5 minutes"

> "Find all messages from Lisa in the last week"

> "React with 👍 to that last message"

> "Mark my Discord chats as read"

Your lobster handles the rest through Beeper.

## The Technical Stuff

*(For those who like to peek under the shell)*

### Beeper API Basics

Base URL: `http://localhost:23373` (Beeper Desktop must be running)

```bash
# Auth header (when using a token)
-H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}"
```

### Accounts

#### List Your Beeper Accounts

See all connected platforms in your Beeper:

```bash
curl -s "${BEEPER_API_URL}/v1/accounts" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}"
```

**Example Response:**
```json
[
  {
    "id": "whatsapp-abc123",
    "service": "whatsapp",
    "displayName": "+1 555-123-4567",
    "connected": true
  },
  {
    "id": "telegram-xyz789",
    "service": "telegram",
    "displayName": "@myusername",
    "connected": true
  },
  {
    "id": "signal-def456",
    "service": "signal",
    "displayName": "+1 555-987-6543",
    "connected": true
  }
]
```

### Chats

#### List All Beeper Chats

```bash
curl -s "${BEEPER_API_URL}/v1/chats" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}"
```

**Example Response:**
```json
[
  {
    "id": "chat-abc123",
    "name": "Family Group",
    "service": "whatsapp",
    "unreadCount": 5,
    "lastMessage": {
      "text": "See you at dinner!",
      "timestamp": "2026-01-23T15:30:00Z"
    }
  },
  {
    "id": "chat-xyz789",
    "name": "Work Team",
    "service": "slack",
    "unreadCount": 0,
    "lastMessage": {
      "text": "Meeting moved to 3pm",
      "timestamp": "2026-01-23T14:00:00Z"
    }
  }
]
```

#### Search Beeper Chats

```bash
curl -s "${BEEPER_API_URL}/v1/chats/search?q=project+meeting" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}"
```

#### Get Chat Details

```bash
curl -s "${BEEPER_API_URL}/v1/chats/{chatID}" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}"
```

**Example Response:**
```json
{
  "id": "chat-abc123",
  "name": "Family Group",
  "service": "whatsapp",
  "unreadCount": 5,
  "participants": [
    {"id": "user-1", "name": "Mom", "phone": "+15551234567"},
    {"id": "user-2", "name": "Dad", "phone": "+15559876543"},
    {"id": "user-3", "name": "You", "phone": "+15555555555"}
  ],
  "archived": false,
  "muted": false
}
```

#### Create a New Beeper Chat

```bash
curl -X POST "${BEEPER_API_URL}/v1/chats" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "accountID": "whatsapp-abc123",
    "participants": ["+1234567890"]
  }'
```

#### Archive/Unarchive Chat

```bash
curl -X POST "${BEEPER_API_URL}/v1/chats/{chatID}/archive" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"archived": true}'
```

### Messages

#### List Messages in a Chat

```bash
curl -s "${BEEPER_API_URL}/v1/chats/{chatID}/messages" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}"
```

**Example Response:**
```json
[
  {
    "id": "msg-001",
    "chatID": "chat-abc123",
    "sender": {"id": "user-1", "name": "Mom"},
    "text": "Don't forget to call grandma!",
    "timestamp": "2026-01-23T15:30:00Z",
    "reactions": [
      {"emoji": "👍", "user": {"id": "user-2", "name": "Dad"}}
    ]
  },
  {
    "id": "msg-002",
    "chatID": "chat-abc123",
    "sender": {"id": "user-2", "name": "Dad"},
    "text": "See you at dinner!",
    "timestamp": "2026-01-23T15:25:00Z",
    "reactions": []
  }
]
```

#### Search Messages Across All Beeper Networks

```bash
curl -s "${BEEPER_API_URL}/v1/messages/search?q=dinner+plans" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}"
```

**Example Response:**
```json
{
  "results": [
    {
      "id": "msg-xyz",
      "chatID": "chat-abc123",
      "chatName": "Family Group",
      "service": "whatsapp",
      "text": "What are the dinner plans for tonight?",
      "sender": {"name": "Mom"},
      "timestamp": "2026-01-23T12:00:00Z"
    }
  ],
  "total": 1
}
```

#### Send a Message via Beeper

```bash
curl -X POST "${BEEPER_API_URL}/v1/chats/{chatID}/messages" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello from my lobster! 🦞"}'
```

**Example Response:**
```json
{
  "id": "msg-new123",
  "chatID": "chat-abc123",
  "text": "Hello from my lobster! 🦞",
  "timestamp": "2026-01-23T16:00:00Z",
  "status": "sent"
}
```

#### Reply to a Message

```bash
curl -X POST "${BEEPER_API_URL}/v1/chats/{chatID}/messages" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Sounds good!",
    "replyTo": "msg-001"
  }'
```

#### Mark Messages as Read

```bash
curl -X POST "${BEEPER_API_URL}/v1/chats/{chatID}/read" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"upToMessageID": "msg-001"}'
```

### Reactions

#### Add a Reaction to a Message

```bash
curl -X POST "${BEEPER_API_URL}/v1/chats/{chatID}/messages/{messageID}/reactions" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"emoji": "👍"}'
```

#### Remove a Reaction

```bash
curl -X DELETE "${BEEPER_API_URL}/v1/chats/{chatID}/messages/{messageID}/reactions" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"emoji": "👍"}'
```

### Contacts

#### Search Contacts on an Account

```bash
curl -s "${BEEPER_API_URL}/v1/accounts/{accountID}/contacts?q=john" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}"
```

**Example Response:**
```json
[
  {
    "id": "contact-123",
    "name": "John Smith",
    "phone": "+15551234567",
    "avatar": "https://..."
  },
  {
    "id": "contact-456",
    "name": "Johnny Appleseed",
    "phone": "+15559876543",
    "avatar": "https://..."
  }
]
```

### Reminders

#### Create Chat Reminder

Set a reminder for a chat:

```bash
curl -X POST "${BEEPER_API_URL}/v1/chats/{chatID}/reminders" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"remindAt": "2026-01-25T10:00:00Z"}'
```

#### Delete Chat Reminder

```bash
curl -X DELETE "${BEEPER_API_URL}/v1/chats/{chatID}/reminders" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}"
```

### Assets

#### Download Message Attachment

```bash
curl -X POST "${BEEPER_API_URL}/v1/assets/download" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"assetID": "asset-id-here"}' \
  --output attachment.file
```

## Pro Tips 🦞

### Get Unread Summary from Beeper

```bash
curl -s "${BEEPER_API_URL}/v1/chats?unreadOnly=true" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}" | \
  jq '.[] | "[\(.service)] \(.name): \(.unreadCount) unread"'
```

**Example Output:**
```
[whatsapp] Family Group: 5 unread
[slack] Work Team: 12 unread
[signal] Best Friend: 2 unread
```

### Find a WhatsApp Chat in Beeper

```bash
# Get your WhatsApp account ID from Beeper
WHATSAPP=$(curl -s "${BEEPER_API_URL}/v1/accounts" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}" | \
  jq -r '.[] | select(.service == "whatsapp") | .id')

# Search for a contact
curl -s "${BEEPER_API_URL}/v1/chats/search?q=Mom" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}"
```

### Mark All Chats as Read

```bash
for chatID in $(curl -s "${BEEPER_API_URL}/v1/chats?unreadOnly=true" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}" | jq -r '.[].id'); do
  curl -X POST "${BEEPER_API_URL}/v1/chats/${chatID}/read" \
    -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}"
  echo "Marked ${chatID} as read"
done
```

### Quick React to Last Message

```bash
# Get the last message ID from a chat
LAST_MSG=$(curl -s "${BEEPER_API_URL}/v1/chats/{chatID}/messages?limit=1" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}" | jq -r '.[0].id')

# React with thumbs up
curl -X POST "${BEEPER_API_URL}/v1/chats/{chatID}/messages/${LAST_MSG}/reactions" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"emoji": "👍"}'
```

### Check if Beeper is Ready

```bash
curl -s --connect-timeout 2 "${BEEPER_API_URL:-http://localhost:23373}/health" && echo "Beeper is ready!"
```

### Get Messages from Last 24 Hours

```bash
YESTERDAY=$(date -u -v-1d +"%Y-%m-%dT%H:%M:%SZ" 2>/dev/null || date -u -d "1 day ago" +"%Y-%m-%dT%H:%M:%SZ")

curl -s "${BEEPER_API_URL}/v1/messages/search?after=${YESTERDAY}" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}"
```

### Filter Chats by Service

```bash
# Get only Signal chats
curl -s "${BEEPER_API_URL}/v1/chats" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}" | \
  jq '[.[] | select(.service == "signal")]'

# Get only Slack chats
curl -s "${BEEPER_API_URL}/v1/chats" \
  -H "Authorization: Bearer ${BEEPER_ACCESS_TOKEN}" | \
  jq '[.[] | select(.service == "slack")]'
```

## Good to Know

**Beeper Desktop must be running** - The API lives inside Beeper Desktop. No Beeper = no connection.

**It's local & private** - The Beeper API runs entirely on your machine. Your messages never touch external servers through this skill.

**Respect the networks** - This is for personal use. Sending too many messages might trigger rate limits on WhatsApp, etc.

**iMessage needs macOS** - Apple gonna Apple.

**Reactions vary by network** - Not all platforms support all emoji. Beeper handles the translation.

## Troubleshooting

### "Can't connect to Beeper"

1. Is Beeper Desktop running? Look for it in your menu bar.
2. Is the API enabled? Beeper → Settings → Developers → Beeper Desktop API
3. Check the port: `curl http://localhost:23373/health`

### "Authentication failed"

1. Generate a fresh token in Beeper → Settings → Developers
2. Make sure it's in your config (no extra spaces!)
3. Or just remove the token - Beeper will prompt for OAuth

### "Chat not found"

1. Make sure the chat exists in your Beeper app
2. Try different search terms
3. Check that the account (WhatsApp, Telegram, etc.) is connected in Beeper

### "Reaction not supported"

Some networks have limited emoji support. Try a more common emoji like 👍 ❤️ 😂 😮 😢 😡

## Links

- [Get Beeper](https://www.beeper.com/download) - Free download
- [Beeper Developer Docs](https://developers.beeper.com) - Full API reference
- [Beeper MCP](https://www.beeper.com/mcp) - For Claude Desktop & Cursor users
- [Beeper Desktop API Reference](https://developers.beeper.com/desktop-api-reference/) - Complete endpoint docs

## Credits

Built with 🦞 by @nickhamze and the Clawdbot community.

Powered by [Beeper](https://www.beeper.com) - One app for all your chats.

*Claw Me Maybe - because your lobster should be able to reach you anywhere.*
