---
name: oura-ring
description: Fetch Oura Ring readiness/sleep + 7-day readiness trends via Oura Cloud API V2, and generate a Morning Readiness Brief.
---

# Oura Ring (V1)

This skill provides a small, public-facing reference implementation for pulling **Readiness**, **Sleep**, and **7-day Readiness trends** from the **Oura V2 API** (`/v2/usercollection/*`).

## Quick Reference

- CLI (raw data):
  - `python3 skills/oura-ring/cli.py --format json --pretty readiness`
  - `python3 skills/oura-ring/cli.py --format json --pretty sleep`
  - `python3 skills/oura-ring/cli.py --format json --pretty trends`
  - `python3 skills/oura-ring/cli.py --format json --pretty resilience`
  - `python3 skills/oura-ring/cli.py --format json --pretty stress`

- Morning brief (formatted):
  - `./skills/oura-ring/scripts/morning_brief.sh`

## Features

- **Morning Readiness Brief**: Tactical recommendation based on latest scores.
- **Trend Analysis**: Insights on score changes over the last 7 days.
- **Resilience Tracking**: Real-time capacity mapping for stress management.

## Setup

### 1) Install dependencies (recommended: venv)

macOS/Homebrew Python often blocks system-wide `pip install` (PEP 668), so use a virtualenv:

```bash
python3 -m venv skills/oura-ring/.venv
source skills/oura-ring/.venv/bin/activate
python -m pip install -r skills/oura-ring/requirements.txt
```

### 2) Create your `.env`

Create `skills/oura-ring/.env`:

```bash
cp skills/oura-ring/.env.example skills/oura-ring/.env
# then edit skills/oura-ring/.env
```

The CLI reads:
- `OURA_TOKEN` (required)
- `OURA_BASE_URL` (optional; defaults to `https://api.ouraring.com/v2/usercollection`)

## Getting an Oura token (OAuth2)

Oura V2 uses OAuth2 bearer tokens.

1. Create an Oura API application:
   - https://cloud.ouraring.com/oauth/applications
2. Set a Redirect URI (for local testing, something like `http://localhost:8080/callback`).
3. Open the authorization URL (replace `CLIENT_ID`, `REDIRECT_URI`, and `scope`):

```text
https://cloud.ouraring.com/oauth/authorize?response_type=code&client_id=CLIENT_ID&redirect_uri=REDIRECT_URI&scope=readiness%20sleep
```

4. After approving, you’ll be redirected to your Redirect URI with a `code=...` query parameter.
5. Exchange the code for an access token:

```bash
curl -X POST https://api.ouraring.com/oauth/token \
  -H 'Content-Type: application/x-www-form-urlencoded' \
  -d grant_type=authorization_code \
  -d client_id=CLIENT_ID \
  -d client_secret=CLIENT_SECRET \
  -d redirect_uri=REDIRECT_URI \
  -d code=AUTH_CODE
```

6. Put the returned `access_token` into `skills/oura-ring/.env` as `OURA_TOKEN=...`.

Notes:
- Access tokens can expire; you may need to refresh using the `refresh_token`.
- Do **not** commit your `.env` file.

## Usage

### Readiness

```bash
python3 skills/oura-ring/cli.py --env-file skills/oura-ring/.env --format json --pretty readiness
```

### Sleep

```bash
python3 skills/oura-ring/cli.py --env-file skills/oura-ring/.env --format json --pretty sleep
```

### Trends (last 7 days; paginated)

```bash
python3 skills/oura-ring/cli.py --env-file skills/oura-ring/.env --format json --pretty trends
```

## Wrapper: Morning Readiness Brief

```bash
./skills/oura-ring/scripts/morning_brief.sh
```

Override the env file location:

```bash
OURA_ENV_FILE=/path/to/.env ./skills/oura-ring/scripts/morning_brief.sh
```

Run in mock mode (no token):

```bash
OURA_MOCK=1 ./skills/oura-ring/scripts/morning_brief.sh
```

## Verification (no token required)

```bash
python3 skills/oura-ring/cli.py --mock readiness --format json
python3 skills/oura-ring/cli.py --mock sleep --format json
python3 skills/oura-ring/cli.py --mock trends --format json
```
