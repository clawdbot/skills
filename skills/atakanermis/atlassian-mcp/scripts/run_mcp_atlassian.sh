#!/bin/bash
# MCP Atlassian Docker runner
# Runs the Atlassian MCP container with Jira credentials

set -e

# Check required environment variables
if [ -z "$JIRA_URL" ]; then
    echo "Error: JIRA_URL not set (e.g., https://company.atlassian.net)"
    exit 1
fi

if [ -z "$JIRA_USERNAME" ]; then
    echo "Error: JIRA_USERNAME not set (your Jira email address)"
    exit 1
fi

if [ -z "$JIRA_API_TOKEN" ]; then
    echo "Error: JIRA_API_TOKEN not set"
    exit 1
fi

echo "🐳 Starting MCP Atlassian container..."
echo "   URL: $JIRA_URL"
echo "   User: $JIRA_USERNAME"

docker run --rm -i \
  -e JIRA_URL="$JIRA_URL" \
  -e JIRA_USERNAME="$JIRA_USERNAME" \
  -e JIRA_API_TOKEN="$JIRA_API_TOKEN" \
  ghcr.io/sooperset/mcp-atlassian:latest
