# Discord Search Patterns

Advanced search patterns and examples for finding messages in Discord.

## Basic Search

```bash
message action=search channel=discord channelId="1234567890" query="keyword" limit=25
```

## Search Filters

### By Author

Find messages from a specific user:

```bash
message action=search channel=discord channelId="1234567890" authorId="user-id"
```

Or multiple authors:

```bash
message action=search channel=discord channelId="1234567890" authorIds='["user-id-1", "user-id-2"]'
```

### By Time Range

**Messages before a specific message:**
```bash
message action=search channel=discord channelId="1234567890" before="message-id"
```

**Messages after a specific message:**
```bash
message action=search channel=discord channelId="1234567890" after="message-id"
```

**Messages around a specific message:**
```bash
message action=search channel=discord channelId="1234567890" around="message-id"
```

### Combined Filters

Search with multiple criteria:

```bash
message action=search channel=discord channelId="1234567890" query="bug report" authorId="user-id" limit=10
```

## Pagination

Discord returns results in batches. Use message IDs for pagination:

1. First batch: `action=search query="keyword" limit=50`
2. Next batch: Use last message ID from results as `before` parameter
3. Continue: `action=search query="keyword" before="last-msg-id" limit=50`

## Common Search Patterns

### Find Recent Mentions

```bash
message action=search channel=discord channelId="1234567890" query="@me" limit=20
```

### Find Links

```bash
message action=search channel=discord channelId="1234567890" query="https://" limit=25
```

### Find User's Recent Messages

```bash
message action=search channel=discord channelId="1234567890" authorId="user-id" limit=30
```

### Search Across Multiple Channels

Run separate searches for each channel:

```bash
message action=search channel=discord channelId="channel-1" query="keyword"
message action=search channel=discord channelId="channel-2" query="keyword"
```

## Tips

- **Use specific queries** - "error in production" beats "error"
- **Limit wisely** - Start small (10-25), increase if needed
- **Combine filters** - Author + query + time range narrows results
- **Channel IDs required** - Search needs numeric channel ID, not name
- **Case insensitive** - Discord search ignores case by default

## Getting Channel IDs

If you only have channel names:

```bash
message action=channel-list channel=discord guildId="server-id"
```

This returns all channels with their IDs. Then use the ID in search.
