# Discord Bot Configuration

Guide to configuring Discord integration in Clawdbot gateway.

## Overview

Discord integration uses the `message` tool with `channel=discord`. Your bot token and guild info should be configured in the gateway config.

## Configuration Structure

Your gateway config should have a Discord channel plugin entry:

```yaml
channels:
  discord:
    plugin: discord
    token: "YOUR_BOT_TOKEN"
    guildId: "YOUR_GUILD_ID"  # Default guild/server
    # Optional settings:
    logMessages: true
    defaultChannel: "1234567890"  # Default channel ID
```

## Getting Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create new application or select existing
3. Go to "Bot" section
4. Click "Reset Token" to get your token
5. **Important**: Keep token secret! Don't commit to git

## Bot Permissions

Your bot needs these permissions (integer: 2147485696):

- Read Messages/View Channels
- Send Messages
- Embed Links
- Attach Files
- Read Message History
- Add Reactions
- Use Slash Commands (optional)

**Permission calculator**: https://discord.com/developers/docs/topics/permissions

## Invite Bot to Server

Generate invite URL with correct permissions:

```
https://discord.com/api/oauth2/authorize?client_id=YOUR_CLIENT_ID&permissions=2147485696&scope=bot
```

Replace `YOUR_CLIENT_ID` with your application's client ID from the developer portal.

## Getting Guild/Channel IDs

### Enable Developer Mode

1. Discord Settings → Advanced → Enable Developer Mode
2. Now you can right-click servers/channels to copy IDs

### Get Guild ID

Right-click your server name → Copy Server ID

### Get Channel ID

Right-click channel name → Copy Channel ID

## Testing Configuration

Once configured, test with:

```bash
message action=channel-list channel=discord guildId="YOUR_GUILD_ID"
```

Should return list of channels in your server.

## Multiple Guilds

To interact with multiple Discord servers, specify `guildId` in each command:

```bash
message action=send channel=discord guildId="server-1-id" target="#general" message="Hi"
message action=send channel=discord guildId="server-2-id" target="#general" message="Hello"
```

## Webhook Inbound

For receiving Discord events (messages, reactions), configure webhook:

```yaml
channels:
  discord:
    plugin: discord
    token: "YOUR_BOT_TOKEN"
    webhook:
      enabled: true
      path: /webhook/discord
      secret: "random-secret-string"
```

Then configure Discord webhook in your guild:
1. Server Settings → Integrations → Webhooks
2. Create webhook pointing to `https://your-gateway.com/webhook/discord`
3. Include secret in webhook headers or query params

## Troubleshooting

**"Missing Permissions" error:**
- Check bot has correct permissions in Discord server
- Verify role hierarchy (bot role must be high enough)

**"Unknown Channel" error:**
- Verify channel ID is correct
- Check bot can see the channel

**No response:**
- Verify bot is online in Discord
- Check token is valid
- Review gateway logs for errors

**Messages not sending:**
- Check bot has "Send Messages" permission
- Verify channel isn't locked/archived
- Test with `action=channel-info` first

## Security

1. **Never commit tokens** - Use environment variables
2. **Rotate tokens** - If exposed, regenerate immediately
3. **Limit permissions** - Only grant what's needed
4. **Use secrets** - For webhook verification
5. **Monitor usage** - Watch for unexpected activity

## Environment Variables

Recommended: Store sensitive data in environment:

```yaml
channels:
  discord:
    plugin: discord
    token: ${DISCORD_BOT_TOKEN}
    guildId: ${DISCORD_GUILD_ID}
```

Then set in shell:
```bash
export DISCORD_BOT_TOKEN="your-token"
export DISCORD_GUILD_ID="your-guild-id"
```

## Updating Config

After editing gateway config, restart:

```bash
clawdbot gateway restart
```

Or use the gateway tool:

```bash
gateway action=config.patch raw='{"channels":{"discord":{"token":"new-token"}}}'
```

## Resources

- [Discord Developer Portal](https://discord.com/developers/applications)
- [Discord API Docs](https://discord.com/developers/docs)
- [Permissions Calculator](https://discord.com/developers/docs/topics/permissions)
- [Discord.js Guide](https://discordjs.guide) (for reference)
