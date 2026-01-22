---
name: tesla
description: Control your Tesla vehicle - lock/unlock, climate, location, charge status, and more via the unofficial Tesla API.
homepage: https://tesla-api.timdorr.com
metadata: {"clawdbot":{"emoji":"🚗","requires":{"env":["TESLA_EMAIL"]}}}
---

# Tesla

Control your Tesla vehicle from Clawdbot.

## Setup

### First-time authentication:

```bash
python3 {baseDir}/scripts/tesla.py auth
```

This will:
1. Open a Tesla login URL
2. You log in and authorize
3. Paste the callback URL back
4. Saves refresh token for future use

### Environment variables:

- `TESLA_EMAIL` — Your Tesla account email
- Token is cached in `~/.tesla_cache.json`

## Commands

```bash
# Get vehicle status
python3 {baseDir}/scripts/tesla.py status

# Lock/unlock
python3 {baseDir}/scripts/tesla.py lock
python3 {baseDir}/scripts/tesla.py unlock

# Climate
python3 {baseDir}/scripts/tesla.py climate on
python3 {baseDir}/scripts/tesla.py climate off
python3 {baseDir}/scripts/tesla.py climate temp 72

# Charging
python3 {baseDir}/scripts/tesla.py charge status
python3 {baseDir}/scripts/tesla.py charge start
python3 {baseDir}/scripts/tesla.py charge stop

# Location
python3 {baseDir}/scripts/tesla.py location

# Honk & flash
python3 {baseDir}/scripts/tesla.py honk
python3 {baseDir}/scripts/tesla.py flash

# Wake up (if asleep)
python3 {baseDir}/scripts/tesla.py wake
```

## Example Usage

From chat:
- "Is my Tesla locked?"
- "Start the AC in my car"
- "Where's my Tesla?"
- "What's the battery level?"
- "Lock my car"

## API Reference

Uses the unofficial Tesla Owner API documented at:
https://tesla-api.timdorr.com

## Privacy

- Credentials are stored locally
- Refresh token cached in `~/.tesla_cache.json`
- No data sent to third parties
