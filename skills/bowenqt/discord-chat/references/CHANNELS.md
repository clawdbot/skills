# Discord Channel Management

Create, edit, and manage Discord channels.

## List Channels

Get all channels in a server:

```bash
message action=channel-list channel=discord guildId="server-id"
```

Returns channel names, IDs, types, and hierarchy.

## Get Channel Info

Detailed info for a specific channel:

```bash
message action=channel-info channel=discord channelId="1234567890"
```

Returns name, topic, permissions, member count, etc.

## Create Channels

**Create text channel:**
```bash
message action=channel-create channel=discord guildId="server-id" name="new-channel" type=0
```

**Create voice channel:**
```bash
message action=channel-create channel=discord guildId="server-id" name="voice-room" type=2
```

**Create with topic:**
```bash
message action=channel-create channel=discord guildId="server-id" name="discussions" type=0 topic="General discussions"
```

**Create in category:**
```bash
message action=channel-create channel=discord guildId="server-id" name="support" type=0 parentId="category-id"
```

## Channel Types

- `0` - Text channel
- `2` - Voice channel
- `4` - Category
- `5` - Announcement channel
- `10` - Announcement thread
- `11` - Public thread
- `12` - Private thread
- `13` - Stage channel
- `15` - Forum channel

## Edit Channels

Update channel properties:

```bash
message action=channel-edit channel=discord channelId="1234567890" name="renamed-channel"
```

**Change topic:**
```bash
message action=channel-edit channel=discord channelId="1234567890" topic="New topic"
```

**Change position:**
```bash
message action=channel-edit channel=discord channelId="1234567890" position=5
```

**Toggle NSFW:**
```bash
message action=channel-edit channel=discord channelId="1234567890" nsfw=true
```

**Slow mode:**
```bash
message action=channel-edit channel=discord channelId="1234567890" rateLimitPerUser=10
```

Rate limit is in seconds (0-21600). 0 disables slow mode.

## Move Channels

Move channel to different category:

```bash
message action=channel-move channel=discord channelId="1234567890" parentId="new-category-id"
```

Remove from category:

```bash
message action=channel-move channel=discord channelId="1234567890" clearParent=true
```

## Delete Channels

**Delete a channel:**
```bash
message action=channel-delete channel=discord channelId="1234567890"
```

**With reason (audit log):**
```bash
message action=channel-delete channel=discord channelId="1234567890" reason="No longer needed"
```

⚠️ **Warning**: Deletion is permanent. Cannot be undone.

## Categories

**Create category:**
```bash
message action=category-create channel=discord guildId="server-id" name="HELP DESK"
```

**Edit category:**
```bash
message action=category-edit channel=discord categoryId="1234567890" name="SUPPORT"
```

**Delete category:**
```bash
message action=category-delete channel=discord categoryId="1234567890"
```

Note: Deleting a category doesn't delete channels inside it. They become uncategorized.

## Threads

**Create thread from message:**
```bash
message action=thread-create channel=discord channelId="1234567890" messageId="msg-id" threadName="Discussion"
```

**Create standalone thread:**
```bash
message action=thread-create channel=discord channelId="1234567890" threadName="New Topic"
```

**List threads:**
```bash
message action=thread-list channel=discord channelId="1234567890"
```

**Reply in thread:**
```bash
message action=thread-reply channel=discord threadId="thread-id" message="Reply text"
```

## Permissions

Check user/role permissions in a channel:

```bash
message action=permissions channel=discord channelId="1234567890" userId="user-id"
```

Or for a role:

```bash
message action=permissions channel=discord channelId="1234567890" roleId="role-id"
```

## Pins

**Pin message:**
```bash
message action=pin channel=discord messageId="1234567890"
```

**Unpin message:**
```bash
message action=unpin channel=discord messageId="1234567890"
```

**List pinned messages:**
```bash
message action=list-pins channel=discord channelId="1234567890"
```

## Best Practices

1. **Name channels clearly** - Use descriptive, lowercase-with-hyphens names
2. **Set topics** - Help users understand channel purpose
3. **Use categories** - Organize related channels together
4. **Check before deleting** - Deletion is permanent
5. **Document reasons** - Use `reason` parameter for audit logs
6. **Test permissions** - Verify bot has needed permissions before operations
