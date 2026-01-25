---
name: mcp-atlassian
description: Run the Model Context Protocol (MCP) Atlassian server in Docker, enabling integration with Jira, Confluence, and other Atlassian products. Use when you need to query Jira issues, search Confluence, or interact with Atlassian services programmatically. Requires Docker and valid Jira API credentials.
---

# MCP Atlassian

## Overview

The MCP Atlassian server provides programmatic access to Jira and other Atlassian services through the Model Context Protocol. Run it in Docker with your Jira credentials to query issues, manage projects, and interact with Atlassian tools.

## Quick Start

Pull and run the container with your Jira credentials:

```bash
docker pull ghcr.io/sooperset/mcp-atlassian:latest

docker run --rm -i \
  -e JIRA_URL=https://your-company.atlassian.net \
  -e JIRA_USERNAME=your.email@company.com \
  -e JIRA_API_TOKEN=your_api_token \
  ghcr.io/sooperset/mcp-atlassian:latest
```

**With script (faster):**

Run the bundled script with your API token:

```bash
JIRA_API_TOKEN=your_token bash scripts/run_mcp_atlassian.sh
```

## Environment Variables

- **JIRA_URL**: Your Atlassian instance URL (e.g., `https://company.atlassian.net`)
- **JIRA_USERNAME**: Your Jira email address
- **JIRA_API_TOKEN**: Your Jira API token (create in [Account Settings → Security](https://id.atlassian.com/manage-profile/security/api-tokens))

## Using MCP Atlassian with Clawdbot

Once running, the MCP server exposes Jira tools for use. Reference the container as an MCP source in your Clawdbot config to query issues, create tasks, or manage Jira directly from your agent.

## Resources

### scripts/
- **run_mcp_atlassian.sh** - Simplified runner script with credential handling
