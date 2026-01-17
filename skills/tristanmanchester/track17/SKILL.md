---
name: track17
description: Track parcels via the 17TRACK API (local SQLite DB, polling + optional webhook ingestion)
user-invocable: true
metadata: {"clawdbot":{"emoji":"📦","requires":{"anyBins":["python3","python"],"env":["TRACK17_TOKEN"]},"primaryEnv":"TRACK17_TOKEN"}}
---

# track17 (17TRACK parcel tracking)

This skill lets Clawdbot keep a local list of your parcels, track their state via the **17TRACK Tracking API v2.2**, and summarise changes.

It stores everything in a small **SQLite DB** under your **workspace** (by default: `<workspace>/packages/track17/track17.sqlite3`).

`<workspace>` is auto-detected as the parent directory of the nearest `skills/` directory that contains this skill.
For example, if you install it at `/clawd/skills/track17/`, data will be stored at `/clawd/packages/track17/`.

## Requirements

- `TRACK17_TOKEN` must be set (17TRACK API token; used as the `17token` header).
- Python (`python3` preferred).

Optional:
- `TRACK17_WEBHOOK_SECRET` if you want to verify webhook signatures.
- `TRACK17_DATA_DIR` to override where the DB/inbox live.
- `TRACK17_WORKSPACE_DIR` to override what this tool considers the workspace directory.

## Quick start

1) Initialise storage (safe to run multiple times):

```bash
python3 {baseDir}/scripts/track17.py init
```

2) Add a package (registers it with 17TRACK and stores it locally):

```bash
python3 {baseDir}/scripts/track17.py add "RR123456789CN" --label "AliExpress headphones"
```

If carrier auto-detection fails, specify a carrier code:

```bash
python3 {baseDir}/scripts/track17.py add "RR123456789CN" --carrier 3011 --label "..."
```

3) List tracked packages:

```bash
python3 {baseDir}/scripts/track17.py list
```

4) Poll for updates (recommended if you don't want webhooks):

```bash
python3 {baseDir}/scripts/track17.py sync
```

5) Show details for one package:

```bash
python3 {baseDir}/scripts/track17.py status 1
# or
python3 {baseDir}/scripts/track17.py status "RR123456789CN"
```

## Webhooks (optional)

17TRACK can push updates to a webhook URL. This skill supports webhook ingestion in two ways:

### A) Run the included webhook server

```bash
python3 {baseDir}/scripts/track17.py webhook-server --bind 127.0.0.1 --port 8789
```

Then point 17TRACK's webhook URL at that server (ideally via a reverse proxy or Tailscale Funnel).

### B) Ingest webhook payloads from stdin/file

```bash
cat payload.json | python3 {baseDir}/scripts/track17.py ingest-webhook
# or
python3 {baseDir}/scripts/track17.py ingest-webhook --file payload.json
```

If you saved webhook deliveries to the inbox directory, process them:

```bash
python3 {baseDir}/scripts/track17.py process-inbox
```

## Common actions

- Stop tracking:

```bash
python3 {baseDir}/scripts/track17.py stop 1
```

- Retrack a stopped parcel:

```bash
python3 {baseDir}/scripts/track17.py retrack 1
```

- Delete a parcel from local DB (does not delete at 17TRACK unless you also call `delete-remote`):

```bash
python3 {baseDir}/scripts/track17.py remove 1
```

- Show API quota:

```bash
python3 {baseDir}/scripts/track17.py quota
```

## Operating guidance for the agent

- Prefer **sync** (polling) for simplicity unless the user explicitly wants webhooks.
- After adding a package, run `status` once to confirm a valid carrier/status was returned.
- When summarising, prioritise:
  - delivered/out for delivery
  - exception/failed delivery
  - customs holds
  - carrier handoffs
- Never echo `TRACK17_TOKEN` or `TRACK17_WEBHOOK_SECRET`.
