---
name: whoop
description: WHOOP Central - OAuth + scripts to fetch WHOOP data (sleep, recovery, strain, workouts). Use when user asks about their sleep, recovery score, HRV, strain, or workout data.
version: 1.0.2
metadata:
  clawdbot:
    emoji: "🏋️"
    requires:
      bins: ["node", "openssl"]
---

# WHOOP Central

Access sleep, recovery, strain, and workout data from WHOOP via the v2 API.

## Quick Commands

```bash
# 1) One-time setup (writes ~/.clawdbot/whoop/credentials.json)
node src/setup.js

# 2) Recommended: Get tokens via Postman (see Auth section), then verify
node src/verify.js
node src/verify.js --refresh

# Prompt-friendly snapshot (includes last workout)
node src/today.js

# Daily summary (all metrics)
node src/summary.js

# Individual metrics
node src/recovery.js
node src/sleep.js
node src/strain.js
node src/workouts.js

# Bulk import to ~/clawd/health/logs/whoop/*
node src/import-historical.js
```

## Data Available

| Metric | Data Points |
|--------|-------------|
| **Recovery** | Score (0-100%), HRV, resting HR, SpO2, skin temp |
| **Sleep** | Duration, stages (REM/deep/light), efficiency, performance |
| **Strain** | Daily strain (0-21), calories, avg/max HR |
| **Workouts** | Activity type, duration, strain, calories, HR |

## Recovery Score Guide

- 💚 **67-100%** Green - Ready to perform
- 💛 **34-66%** Yellow - Moderate readiness
- ❤️ **0-33%** Red - Focus on recovery

## Setup

### 0. Requirements

- Node.js 18+ (this repo uses ESM)
- `openssl` (only needed for the optional `auth.js` flow when using `https://localhost`; Postman auth does not need it)

### 1. Create WHOOP Developer App

1. Go to https://developer.whoop.com/
2. Sign in with your WHOOP account
3. Create a new App
4. Add these Redirect URIs (exact match; no extra trailing slashes):
   - Postman browser callback (recommended auth path):
     ```
     https://oauth.pstmn.io/v1/browser-callback
     ```
   - Optional local callback (only used by `auth.js`):
     ```
     https://localhost:3000/callback
     ```
   You can keep both registered at the same time.
5. Copy the Client ID and Client Secret

Team note: this skill does **not** ship any client credentials. Each user can create their own WHOOP app,
or (if you trust each other) a team can share one app's `client_id`/`client_secret` and let multiple WHOOP
accounts authorize it.

### 2. Save Credentials (recommended: interactive)

Run:
```bash
node src/setup.js
```
This writes `~/.clawdbot/whoop/credentials.json` (and optionally `token.json` if you paste tokens).

### 3. Authenticate (Recommended: Postman)

Postman is the most reliable bootstrap for many accounts because WHOOP may block browser-like traffic
to the OAuth endpoints (or behave differently depending on headers).

Postman checklist (don’t skip these):
- WHOOP dashboard Redirect URIs include:
  - `https://oauth.pstmn.io/v1/browser-callback`
- Postman OAuth settings:
  - Scopes include `offline` (or you won’t get a `refresh_token`)
  - Client Authentication is **Send client credentials in body** (`client_secret_post`)

1) In WHOOP dashboard, ensure you registered the Postman callback Redirect URI:
```text
https://oauth.pstmn.io/v1/browser-callback
```

2) In Postman:
- Create an Environment and set variables:
  - `ClientId` = your WHOOP client id
  - `ClientSecret` = your WHOOP client secret
- Open the WHOOP API collection (or any request), then open the Authorization tab:
  - Type: OAuth 2.0
  - Add auth data to: Request Headers
  - Grant Type: Authorization Code
  - Callback URL: check **Authorize using browser**
  - Auth URL:
    ```
    https://api.prod.whoop.com/oauth/oauth2/auth
    ```
  - Access Token URL:
    ```
    https://api.prod.whoop.com/oauth/oauth2/token
    ```
  - Client ID: `{{ClientId}}`
  - Client Secret: `{{ClientSecret}}`
  - Scope (space-delimited): include `offline` plus any read scopes you need, e.g.:
    ```
    offline read:profile read:sleep read:recovery read:workout read:cycles read:body_measurement
    ```
  - State: any 8+ chars (e.g. `loomingState`)
  - Client Authentication: **Send client credentials in body**

3) Click "Get New Access Token", sign in to WHOOP, and click "Grant".

4) In Postman’s "Manage Access Tokens" modal:
- Click "Use Token" (so requests work)
- IMPORTANT: copy and save both:
  - `access_token`
  - `refresh_token`
  Postman often does not retain the refresh token for you later.

5) Save tokens to `~/.clawdbot/whoop/token.json`:
- Use `token.example.json` as a template
- Set:
  - `obtained_at` to current time in milliseconds
  - `redirect_uri` to:
    ```
    https://oauth.pstmn.io/v1/browser-callback
    ```

6) Verify (and test refresh):
```bash
node src/verify.js
node src/verify.js --refresh
```

### 4. Optional: Authenticate via `auth.js` (may fail on some accounts)

If you prefer a fully local OAuth loop (and WHOOP allows it), you can use `auth.js`.

Pre-req: add this redirect URI in WHOOP dashboard:
```text
https://localhost:3000/callback
```

Run:
```bash
WHOOP_REDIRECT_URI='https://localhost:3000/callback' node src/auth.js
```

If you need to do it from a phone/remote device:
```bash
WHOOP_REDIRECT_URI='https://localhost:3000/callback' node src/auth.js --manual
```

Note: for localhost HTTPS, the script generates a self-signed cert and your browser will show a TLS warning.
You must proceed past the warning so the redirect can complete.

### 4. Verify It Works

```bash
node src/verify.js
node src/summary.js
```

## Troubleshooting

### Browser shows `NotAuthorizedException` before the login page
This is a WHOOP-side block on browser User-Agents hitting `api.prod.whoop.com` OAuth endpoints.

- Use the updated `node src/auth.js` which bootstraps the login URL and sends your browser directly to `id.whoop.com`.
- If you still see it, try `node src/auth.js --manual` and open the printed URL.

### "redirect_uri not whitelisted"
1. Go to https://developer.whoop.com/
2. Edit your app
3. Ensure this EXACT URI is in Redirect URIs:
   ```
   https://oauth.pstmn.io/v1/browser-callback
   ```
   If you're using `auth.js` locally, also add:
   ```
   https://localhost:3000/callback
   ```
4. Save and try again

### Token Expired
Tokens auto-refresh on demand (no cron needed). If issues persist:
```bash
rm ~/.clawdbot/whoop/token.json
node src/auth.js
```

### "Authorization was not valid"
This usually means your access token is stale/invalidated (common if you re-auth or refresh tokens elsewhere; WHOOP refresh tokens rotate).

- Re-run `node src/auth.js`, or
- Copy the latest `access_token` + `refresh_token` from Postman into `~/.clawdbot/whoop/token.json` and update `obtained_at`.

### Auth from Phone/Remote Device
Use manual mode:
```bash
node src/auth.js --manual
```
Open the URL on any device, authorize, then copy the code from the callback URL.

### `error=request_forbidden` / "The request is not allowed"
This is WHOOP rejecting the authorization request after login/consent. Common causes:
- Redirect URI policy (WHOOP docs only mention `https://` or `whoop://` redirect URIs)
- App/account restrictions (membership/approval/test-user restrictions)
- Scope restrictions (try requesting fewer scopes)

If you suspect redirect URI policy, use an HTTPS tunnel:
```bash
# 1) Get a public HTTPS URL that forwards to localhost:3000 (example)
ngrok http 3000

# 2) Add the ngrok HTTPS URL + /callback to WHOOP dashboard Redirect URIs, then run:
WHOOP_REDIRECT_URI=https://YOUR-NGROK-DOMAIN.ngrok-free.app/callback node src/auth.js
```

If you suspect scope restrictions, try a minimal scope set:
```bash
WHOOP_SCOPES="read:profile" node src/auth.js
```

### If your WHOOP Redirect URL is `https://localhost:3000/callback`
This changes how the local callback server must run: it must be HTTPS (not HTTP).

The script supports this. Run:
```bash
WHOOP_REDIRECT_URI=https://localhost:3000/callback node src/auth.js
```
It will generate a self-signed cert locally and your browser will likely show a warning for `https://localhost`.
Proceed past the warning so the redirect can complete.

## JSON Output (for tooling)

These commands support:
- `--json` (single JSON blob)
- `--jsonl` (one JSON object per line; useful for piping)
- `--limit N` (where supported)
- Time filters (where supported): `--days N`, `--since 7d` / `12h`, `--start ISO`, `--end ISO`

```bash
node src/summary.js --json
node src/recovery.js --json --limit 1
node src/sleep.js --json --limit 1
node src/strain.js --json --limit 1
node src/workouts.js --json --limit 1

# Examples with filters
node src/sleep.js --json --days 7
node src/workouts.js --jsonl --since 30d
node src/recovery.js --json --start 2026-01-01T00:00:00Z --end 2026-02-01T00:00:00Z
```

## API Notes

- Uses WHOOP Developer API v2
- OAuth 2.0 authentication with refresh tokens
- Scopes: offline, read:recovery, read:sleep, read:workout, read:cycles, read:profile
- Token auto-refreshes when expired
