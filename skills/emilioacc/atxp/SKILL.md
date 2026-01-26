---
name: atxp
description: Access ATXP paid API tools for web search, AI image generation, music creation, video generation, and X/Twitter search. Use when users need real-time web search, AI-generated media (images, music, video), or X/Twitter search. Requires authentication via `npx atxp login`.
---

# ATXP Tools

Access ATXP's paid API tools via CLI.

## Authentication

```bash
# Check if authenticated
echo $ATXP_CONNECTION

# If not set, login:
npx atxp login
source ~/.atxp/config
```

## Commands

| Command | Description |
|---------|-------------|
| `npx atxp search <query>` | Real-time web search |
| `npx atxp image <prompt>` | AI image generation |
| `npx atxp music <prompt>` | AI music generation |
| `npx atxp video <prompt>` | AI video generation |
| `npx atxp x <query>` | X/Twitter search |

## Usage

1. Verify `$ATXP_CONNECTION` is set
2. Run the appropriate command
3. Parse and present results

## Programmatic Access

```typescript
import { atxpClient, ATXPAccount } from '@atxp/client';

const client = await atxpClient({
  mcpServer: 'https://search.mcp.atxp.ai',
  account: new ATXPAccount(process.env.ATXP_CONNECTION),
});

const result = await client.callTool({
  name: 'search_search',
  arguments: { query: 'your query' },
});
```

## MCP Servers

| Server | Tool |
|--------|------|
| `search.mcp.atxp.ai` | `search_search` |
| `image.mcp.atxp.ai` | `image_create_image` |
| `music.mcp.atxp.ai` | `music_create` |
| `video.mcp.atxp.ai` | `create_video` |
| `x-live-search.mcp.atxp.ai` | `x_live_search` |
