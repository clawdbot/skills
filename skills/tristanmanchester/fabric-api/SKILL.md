---
name: fabric-api
description: Create/search Fabric resources via HTTP API (notepads, folders, bookmarks, files).
homepage: https://fabric.so
metadata: {"clawdbot":{"emoji":"🧵","requires":{"env":["FABRIC_API_KEY"],"bins":["curl"]},"primaryEnv":"FABRIC_API_KEY"}}
---

# Fabric API (HTTP via curl)

Use this skill to read/write content in a user's Fabric workspace using the Fabric HTTP API (`https://api.fabric.so`).

## Critical gotchas (read first)

- "Notes" are created via **POST `/v2/notepads`** (not `/v2/notes`).
- Most create endpoints require **`parentId`**:
  - A UUID **or** one of: `@alias::inbox`, `@alias::bin`.
- Notepad create requires:
  - `parentId`
  - AND either `text` (markdown string) **or** `ydoc` (advanced/structured).
- `tags` must be an array of objects, each *either*:
  - `{ "name": "tag name" }` or `{ "id": "<uuid>" }`
  - Never nested arrays; never strings.

When the user doesn't specify a destination folder: default to `parentId: "@alias::inbox"`.

## Setup (Clawdbot)

This skill expects the API key in:

- `FABRIC_API_KEY`

Recommended config (use `apiKey`; Clawdbot will inject `FABRIC_API_KEY` because `primaryEnv` is set):

```json5
{
  skills: {
    entries: {
      "fabric-api": {
        enabled: true,
        apiKey: "YOUR_FABRIC_API_KEY"
      }
    }
  }
}
````

## HTTP basics

* Base: `https://api.fabric.so`
* Auth: `X-Api-Key: $FABRIC_API_KEY`
* JSON: `Content-Type: application/json`

For debugging: prefer `--fail-with-body` so 4xx bodies are shown.

## Canonical curl templates (use heredocs to avoid quoting bugs)

### GET

```bash
curl -sS --fail-with-body "https://api.fabric.so/v2/user/me" \
  -H "X-Api-Key: $FABRIC_API_KEY"
```

### POST (JSON)

```bash
curl -sS --fail-with-body -X POST "https://api.fabric.so/v2/ENDPOINT" \
  -H "X-Api-Key: $FABRIC_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{ "replace": "me" }
JSON
```

## Core workflows

### 1) Create a notepad (note)

Endpoint: `POST /v2/notepads`

* Map user-provided "title" → `name` in the API payload.
* Always include `parentId`.
* Use `text` for markdown content.

```bash
curl -sS --fail-with-body -X POST "https://api.fabric.so/v2/notepads" \
  -H "X-Api-Key: $FABRIC_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{
  "name": "Calendar Test Note",
  "text": "Created via Clawdbot",
  "parentId": "@alias::inbox",
  "tags": [{"name":"calendar"},{"name":"draft"}]
}
JSON
```

If tags cause validation trouble, omit them and create/assign later via `/v2/tags`.

### 2) Create a folder

Endpoint: `POST /v2/folders`

```bash
curl -sS --fail-with-body -X POST "https://api.fabric.so/v2/folders" \
  -H "X-Api-Key: $FABRIC_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{
  "name": "My new folder",
  "parentId": "@alias::inbox",
  "description": null
}
JSON
```

### 3) Create a bookmark

Endpoint: `POST /v2/bookmarks`

```bash
curl -sS --fail-with-body -X POST "https://api.fabric.so/v2/bookmarks" \
  -H "X-Api-Key: $FABRIC_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{
  "url": "https://example.com",
  "parentId": "@alias::inbox",
  "name": "Example",
  "tags": [{"name":"reading"}]
}
JSON
```

### 4) Browse resources (list children of a folder)

Endpoint: `POST /v2/resources/filter`

Use this to list what's inside a folder (use a folder UUID as `parentId`).

```bash
curl -sS --fail-with-body -X POST "https://api.fabric.so/v2/resources/filter" \
  -H "X-Api-Key: $FABRIC_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{
  "parentId": "PARENT_UUID_HERE",
  "limit": 50,
  "order": { "property": "modifiedAt", "direction": "DESC" }
}
JSON
```

### 5) Search

Endpoint: `POST /v2/search`

Use search when the user gives a fuzzy description (“the note about…”).

```bash
curl -sS --fail-with-body -X POST "https://api.fabric.so/v2/search" \
  -H "X-Api-Key: $FABRIC_API_KEY" \
  -H "Content-Type: application/json" \
  --data-binary @- <<'JSON'
{
  "queries": [
    {
      "mode": "text",
      "text": "meeting notes",
      "filters": { "kinds": ["notepad"] }
    }
  ],
  "pagination": { "page": 1, "pageSize": 20 },
  "sort": { "field": "modifiedAt", "order": "desc" }
}
JSON
```

## Tags (safe patterns)

### List tags

`GET /v2/tags?limit=100`

### Create tag

`POST /v2/tags` with `{ "name": "tag name", "description": null, "resourceId": null }`

### Assign tags on create

Use `tags: [{"name":"x"}]` or `tags: [{"id":"<uuid>"}]` only.

## Rate limiting + retries

If you get `429 Too Many Requests`:

* Back off (sleep + jitter) and retry.
* Avoid tight loops; do pagination slowly.

Do not blindly retry create requests without idempotency (you may create duplicates).

## Troubleshooting quick map

* `404 Not Found`: almost always wrong endpoint, wrong resourceId/parentId, or permissions.
* `400 Bad Request`: schema validation; check required fields and tag shape.
* `403 Forbidden`: subscription/permission limits.
* `429 Too Many Requests`: back off + retry.

## API reference

The OpenAPI schema lives here:

* `{baseDir}/fabric-api.yaml`

When in doubt, consult it before guessing endpoint names or payload shapes.