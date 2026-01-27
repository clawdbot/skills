# Skylight Calendar Skill

ClawdHub skill for interacting with Skylight Calendar smart displays.

## Quick Start

### Option A: Email/Password Authentication (Recommended)

```bash
export SKYLIGHT_EMAIL="your_email@example.com"
export SKYLIGHT_PASSWORD="your_password"
export SKYLIGHT_FRAME_ID="your_frame_id"
export SKYLIGHT_URL="https://app.ourskylight.com"
```

The skill will automatically login and generate an auth token.

### Option B: Pre-captured Token

```bash
export SKYLIGHT_TOKEN="Basic your_base64_token_here"
export SKYLIGHT_FRAME_ID="your_frame_id"
export SKYLIGHT_URL="https://app.ourskylight.com"
```

Capture tokens using an HTTPS proxy (Proxyman/Charles/mitmproxy).

## Features

- **Calendar Events** - View upcoming events from synced calendars
- **Chores** - List, create, and manage family chores
- **Lists** - Access shopping and to-do lists
- **Task Box** - Quick task creation
- **Categories** - Family member profiles for chore assignment
- **Rewards** - Track reward points and redemptions

## Authentication Methods

| Method | Environment Variables | Notes |
|--------|----------------------|-------|
| Email/Password | `SKYLIGHT_EMAIL`, `SKYLIGHT_PASSWORD` | Recommended; auto-generates token |
| Pre-captured Token | `SKYLIGHT_TOKEN` | Manual capture via HTTPS proxy |

Both methods require `SKYLIGHT_FRAME_ID` (your household ID).

## Finding Your Frame ID

1. Log into [ourskylight.com](https://ourskylight.com/)
2. Click on your calendar name
3. Look at the URL - the Frame ID is the number at the end

**Example:** In the URL `https://ourskylight.com/calendar/1234567`, the Frame ID is `1234567`

## Requirements

- `SKYLIGHT_FRAME_ID` environment variable (household frame ID)
- Either `SKYLIGHT_EMAIL` + `SKYLIGHT_PASSWORD` OR `SKYLIGHT_TOKEN`
- `curl` and `jq` for API requests

## Version

0.1.0

## Disclaimer

This skill uses an **unofficial, reverse-engineered API**. It is not affiliated with or endorsed by Skylight. Use responsibly and only with your own account.
