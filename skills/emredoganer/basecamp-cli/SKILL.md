---
name: basecamp-cli
description: Manage Basecamp (via bc3 API / 37signals Launchpad) projects, to-dos, messages, and campfires via a TypeScript CLI. Use when you want to list/create/update Basecamp projects and todos from the terminal, or when integrating Basecamp automation into Clawdbot workflows.
---

# Basecamp CLI

This repo contains a standalone CLI.

## Install

```bash
npm i -g @emredoganer/basecamp-cli
```

## Auth

Create an integration (OAuth app) in 37signals Launchpad:
- https://launchpad.37signals.com/integrations

Then:
```bash
basecamp auth configure --client-id <id> --redirect-uri http://localhost:9292/callback
export BASECAMP_CLIENT_SECRET="<secret>"
basecamp auth login
```

## Notes

- This uses the Basecamp API docs published under bc3-api: https://github.com/basecamp/bc3-api
- `BASECAMP_CLIENT_SECRET` is intentionally NOT stored on disk by the CLI.
