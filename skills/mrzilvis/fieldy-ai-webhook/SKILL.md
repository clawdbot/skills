---
name: fieldy
description: Wire a Fieldy webhook transform into Moltbot hooks.
---

## What this sets up

You’ll configure Moltbot Gateway webhooks so an incoming request to `POST /hooks/fieldy` runs through a **transform module** (`fieldy-webhook.js`) before triggering an **agent** run.

Behavior notes (defaults in `fieldy-webhook.js`):
- Saying **"Hey, Fieldy"** (or just **"Fieldy"**) will **trigger** the agent with the text **after** the wake word.
- Transcripts **without** the wake word will **not** wake the agent; they’ll only be **logged to JSONL files** by `fieldy-webhook.js` (under `<workspace>/fieldy/transcripts/`).
- You can adjust wake words, parsing, and logging behavior by editing `fieldy-webhook.js`.

## 1) Put the transform script in the configured transforms dir

Your `hooks.transformsDir` is:

`/root/clawd/skills/fieldy/scripts`

Move the script from this repo:

- From: `src/fieldy-webhook.js`
- To: `/root/clawd/skills/fieldy/scripts/fieldy-webhook.js`

Notes:
- Make sure the destination filename is exactly `fieldy-webhook.js` (matches the config below).

## 2) Add the webhook mapping to `~/.clawdbot/moltbot.json`

Add this config:

```json
"hooks": {
  "token": "insert-your-token",
  "transformsDir": "/root/clawd/skills/fieldy/scripts",
  "mappings": [
    {
      "match": {
        "path": "fieldy"
      },
      "action": "agent",
      "name": "Fieldy",
      "messageTemplate": "{{message}}",
      "deliver": true,
      "transform": {
        "module": "fieldy-webhook.js"
      }
    }
  ]
}
```

Important:
- `hooks.token` is required when hooks are enabled (see [Webhooks docs](https://docs.molt.bot/automation/webhook.md)).
- Ensure `hooks.enabled: true` exists somewhere in your config (and optionally `hooks.path`, default is `/hooks`).

## 3) Restart the Gateway

Plugins/config changes generally require a gateway restart. After restarting, the webhook endpoint should be live.

## 4) Configure the webhook URL in the Fieldy app

- Log in to your Fieldy app
- Go to **Settings** → **Developer Settings**
- Set **Webhook Endpoint URL** to:

`https://your-url.com/hooks/fieldy?token=insert-your-token`

Note: Moltbot supports sending the token via header too, but many webhook providers only support query params. Moltbot still accepts `?token=` (see [Webhooks docs](https://docs.molt.bot/automation/webhook.md)).

## 5) Test

Example request (adjust host/port and token):

```bash
curl -X POST "http://127.0.0.1:18789/hooks/fieldy" \
  -H "Authorization: Bearer insert-your-token" \
  -H "Content-Type: application/json" \
  -d '{"transcript":"Hey Fieldy summarize this: hello world"}'
```

