# track17 (17TRACK) Clawdbot skill

This folder is a self-contained Clawdbot skill that lets your assistant track parcels using the **17TRACK Tracking API v2.2**.

It includes:

- `SKILL.md` — the skill prompt/instructions Clawdbot loads.
- `scripts/track17.py` — a dependency-free Python CLI that:
  - stores packages in a local SQLite DB,
  - registers tracking numbers with 17TRACK,
  - polls status (`sync`),
  - ingests webhooks (`ingest-webhook`, `process-inbox`),
  - optionally runs an HTTP webhook receiver (`webhook-server`).

## Where data is stored

By default (workspace-local):

- `<workspace>/packages/track17/track17.sqlite3`
- `<workspace>/packages/track17/inbox/` (raw webhook payloads)

Where `<workspace>` is auto-detected as the parent directory of the nearest `skills/` directory that contains this skill.
So if the skill is installed at `/clawd/skills/track17/`, data will be stored at `/clawd/packages/track17/`.

Override with:

- `TRACK17_DATA_DIR=/some/path` (data will be stored directly in that directory)
- `TRACK17_WORKSPACE_DIR=/some/workspace` (data will be stored under `/some/workspace/packages/track17/`)

## Configure the API token

This skill declares `metadata.clawdbot.primaryEnv = TRACK17_TOKEN`, so you can configure it in your Clawdbot config as:

```jsonc
{
  "skills": {
    "entries": {
      "track17": {
        "enabled": true,
        "apiKey": "YOUR_17TRACK_TOKEN"
      }
    }
  }
}
```

(Or set `TRACK17_TOKEN` in your shell/service env.)

## Basic usage (manual)

```bash
python3 skills/track17/scripts/track17.py init
python3 skills/track17/scripts/track17.py add RR123456789CN --label "New headphones"
python3 skills/track17/scripts/track17.py list
python3 skills/track17/scripts/track17.py sync
python3 skills/track17/scripts/track17.py status 1 --refresh
```

## Webhooks (optional)

If you prefer push updates:

1) Run the webhook receiver:

```bash
python3 skills/track17/scripts/track17.py webhook-server --bind 127.0.0.1 --port 8789
```

2) Configure the webhook URL in your 17TRACK dashboard.

3) Periodically process the inbox:

```bash
python3 skills/track17/scripts/track17.py process-inbox
```

If you set a webhook signing key, export it as:

```bash
export TRACK17_WEBHOOK_SECRET='...'
```

The tool will verify signatures when it has both the secret and a signature header.

## Notes

- The code uses only the standard library (no `pip install` required).
- 17TRACK rate limits apply (docs mention 3 requests/second); the script batches up to 40 packages per API call.
