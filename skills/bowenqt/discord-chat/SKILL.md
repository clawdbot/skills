---
name: discord-chat
description: Send messages, reply to messages, and search message history in Discord channels using the message tool. Use when the user wants to communicate with Discord (send/reply/search messages), check Discord activity, or interact with Discord channels.
---

# Discord Chat

Interact with Discord channels using Clawdbot's `message` tool.

## Core Actions

### Send Messages

Send a message to a Discord channel:

```bash
message action=send channel=discord target="#channel-name" message="Your message here"
```

Or by channel ID:

```bash
message action=send channel=discord target="1234567890" message="Your message here"
```

**Tips:**
- Use channel names with `#` prefix or channel IDs
- For multiple links, wrap in `<>` to suppress embeds: `<https://example.com>`
- No markdown tables! Use bullet lists instead
- Support effects with `effect=balloons` or `effectId=invisible-ink`

### Reply to Messages

Reply to a specific message:

```bash
message action=send channel=discord target="#channel-name" message="Reply text" replyTo="message-id"
```

The `replyTo` parameter creates a threaded reply to the specified message ID.

### Search Messages

Search for messages in a channel:

```bash
message action=search channel=discord channelId="1234567890" query="search terms" limit=50
```

**Search options:**
- `query`: Search terms
- `authorId`: Filter by author
- `before`/`after`/`around`: Message ID for pagination
- `limit`: Max results (default 25)

See [SEARCH.md](references/SEARCH.md) for advanced search patterns.

### Other Actions

**Read messages:**
```bash
message action=read channel=discord target="#channel-name" limit=20
```

**React to messages:**
```bash
message action=react channel=discord messageId="1234567890" emoji="👍"
```

**Edit messages:**
```bash
message action=edit channel=discord messageId="1234567890" message="Updated text"
```

**Delete messages:**
```bash
message action=delete channel=discord messageId="1234567890"
```

## Quick Reference

Common patterns:

- **Announce to channel**: `action=send target="#announcements"`
- **Reply in thread**: `action=send replyTo="msg-id"`
- **Recent activity**: `action=read limit=10`
- **Find mentions**: `action=search query="@username"`
- **Acknowledge**: `action=react emoji="✅"`

## Channel Management

**List channels:**
```bash
message action=channel-list channel=discord guildId="server-id"
```

**Get channel info:**
```bash
message action=channel-info channel=discord channelId="1234567890"
```

For creating/editing channels, see [CHANNELS.md](references/CHANNELS.md).

## Best Practices

1. **Use target names when possible** - `target="#general"` is clearer than IDs
2. **Batch reactions** - One emoji per message, pick the best fit
3. **Format for Discord** - Bullets not tables, `<link>` to suppress embeds
4. **Search before asking** - Check history before requesting info
5. **React > Reply** - Use reactions for simple acknowledgments

## Configuration

Your Discord bot configuration should be in the gateway config. The `message` tool routes to the configured Discord plugin automatically when `channel=discord` is specified.

For setup help, see [CONFIG.md](references/CONFIG.md).
