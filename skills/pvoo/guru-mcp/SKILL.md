---
name: guru-mcp
description: Access Guru knowledge base via MCP - ask AI questions, search documents, create drafts, and update cards. Connects to all your Guru sources including Slack, Drive, Confluence, and SharePoint.
homepage: https://www.getguru.com
metadata: {"clawdbot":{"emoji":"🧠","requires":{"bins":["mcporter"],"env":["GURU_API_TOKEN"]}}}
---

# Guru MCP

Access your Guru knowledge base via the official MCP server. Ask AI-powered questions, search documents, create drafts, and update cards.

## Features

- **AI-Powered Answers** — Get comprehensive answers from Knowledge Agents
- **Document Search** — Find cards and content across your knowledge base
- **Create Drafts** — Generate new card drafts from AI tools
- **Update Cards** — Modify existing cards directly
- **Connected Sources** — Access Salesforce, Slack, Google Drive, Confluence, SharePoint through Guru
- **Permission-Aware** — Respects all existing Guru permissions
- **Analytics** — All queries logged in AI Agent Center

## Setup

### 1. Get API Token

1. Go to **Guru Admin → API Tokens**
2. Create a new token
3. Note your email and token

### 2. Configure Environment

Add to `~/.clawdbot/.env`:
```bash
GURU_API_TOKEN=your.email@company.com:your-api-token
```

### 3. Configure mcporter

Add to `config/mcporter.json`:
```json
{
  "mcpServers": {
    "guru": {
      "baseUrl": "https://mcp.api.getguru.com/mcp",
      "headers": {
        "Authorization": "Bearer ${GURU_API_TOKEN}"
      }
    }
  }
}
```

### 4. Verify

```bash
mcporter list guru
```

## Available Tools

### `guru_list_knowledge_agents`

List all Knowledge Agents in your workspace. **Always call this first** to get agent IDs for other tools.

```bash
mcporter call 'guru.guru_list_knowledge_agents()'
```

Returns:
```json
[
  {"id": "08de66e8-...", "name": "Guru"},
  {"id": "abc123...", "name": "Engineering Docs"}
]
```

### `guru_answer_generation`

Get AI-powered answers from a Knowledge Agent. Best for specific questions like "What is X?" or "How do I Y?".

```bash
mcporter call 'guru.guru_answer_generation(
  agentId: "YOUR_AGENT_ID",
  question: "How do I submit expenses?"
)'
```

Optional filters:
- `collectionIds` — Limit to specific collections
- `sourceIds` — Limit to specific sources

Returns comprehensive answer with sources.

### `guru_search_documents`

Find documents, cards, and sources. Best for browsing content like "find docs on X" or "do we have cards about Y?".

```bash
mcporter call 'guru.guru_search_documents(
  agentId: "YOUR_AGENT_ID",
  query: "onboarding process"
)'
```

Returns list of matching documents with snippets.

### `guru_get_card_by_id`

Get full card content in HTML format.

```bash
mcporter call 'guru.guru_get_card_by_id(id: "CARD_ID")'
```

Returns card ID, title, and HTML content.

### `guru_create_draft`

Create a new card draft.

```bash
mcporter call 'guru.guru_create_draft(
  title: "New Process Guide",
  content: "<h2>Overview</h2><p>This guide covers...</p>"
)'
```

Returns draft ID and URL.

### `guru_update_card`

Update an existing card. First retrieve current content with `guru_get_card_by_id`, then modify.

```bash
mcporter call 'guru.guru_update_card(
  cardId: "CARD_ID",
  title: "Updated Title",
  content: "<p>Updated HTML content...</p>"
)'
```

**Important:** Preserve HTML structure when updating. Insert/replace content within existing DOM hierarchy.

## Usage Patterns

### Ask a Question

```bash
# 1. Get agent ID
mcporter call 'guru.guru_list_knowledge_agents()'

# 2. Ask question
mcporter call 'guru.guru_answer_generation(
  agentId: "08de66e8-...",
  question: "What is the PTO policy?"
)'
```

### Find and Read a Card

```bash
# 1. Search for cards
mcporter call 'guru.guru_search_documents(
  agentId: "08de66e8-...",
  query: "expense report"
)'

# 2. Get full content
mcporter call 'guru.guru_get_card_by_id(id: "CARD_ID_FROM_SEARCH")'
```

### Create New Documentation

```bash
mcporter call 'guru.guru_create_draft(
  title: "API Authentication Guide",
  content: "<h2>Overview</h2><p>This guide explains how to authenticate with our API.</p><h2>Steps</h2><ol><li>Generate API key</li><li>Add to headers</li></ol>"
)'
```

## Choosing the Right Tool

| Use Case | Tool |
|----------|------|
| "What is X?" / "How do I Y?" | `guru_answer_generation` |
| "Find docs about X" | `guru_search_documents` |
| "Show me card XYZ" | `guru_get_card_by_id` |
| "Create a new guide for X" | `guru_create_draft` |
| "Update this card with..." | `guru_update_card` |

## Token Format

The `GURU_API_TOKEN` must be in format `email:token`:
```
your.email@company.com:a1b2c3d4-e5f6-7890-abcd-ef1234567890
```

## Notes

- Questions appear in Guru's **AI Agent Center** analytics
- All permissions enforced (users only see what they have access to)
- Knowledge Agents can be domain-specific — choose the right one for your question
- Card content is HTML — preserve structure when updating

## Resources

- [Guru MCP Documentation](https://help.getguru.com/docs/connecting-gurus-mcp-server)
- [Guru API Reference](https://developer.getguru.com)
- [AI Agent Center](https://app.getguru.com/ai-agent-center)
- [MCP Feedback](https://help.getguru.com/docs/connecting-gurus-mcp-server#feedback)
