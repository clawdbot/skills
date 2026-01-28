# Zoom Unofficial Community Skill

A Python CLI for interacting with Zoom's REST API — manage meetings, recordings, team chat, AI meeting summaries, live meeting monitoring, and RTMS control. Works standalone or as a skill for any AI agent.

> **Unofficial** — This skill is not affiliated with or endorsed by Zoom Video Communications.

## Features

- **Meetings** — List, create, update, delete, and view meeting details
- **Live Meetings** — Monitor currently active meetings via Dashboard API
- **RTMS Control** — Start and stop Real-Time Media Streams for live meetings
- **Recordings** — List, download, and delete cloud recordings
- **Transcripts** — Download meeting transcript files
- **AI Summaries** — Retrieve and download AI Companion meeting summaries
- **Team Chat** — Send messages, DMs, list channels and contacts
- **Users** — View profiles and list account users
- **Phone** — View call logs (requires Zoom Phone)

## Quick Start

### 1. Install dependencies

```bash
pip3 install requests PyJWT --break-system-packages
```

### 2. Create a Zoom Server-to-Server OAuth App

1. Go to https://marketplace.zoom.us/
2. Click **Develop** → **Build App**
3. Choose **Server-to-Server OAuth**
4. Note your **Account ID**, **Client ID**, and **Client Secret**
5. Add the scopes you need (see [Scopes](#scopes) below)
6. Activate the app

### 3. Configure

Copy `.env.example` to `.env` and fill in your credentials:

```env
ZOOM_ACCOUNT_ID=your_account_id
ZOOM_CLIENT_ID=your_client_id
ZOOM_CLIENT_SECRET=your_client_secret
ZOOM_USER_EMAIL=you@example.com
ZOOM_RTMS_CLIENT_ID=your_rtms_app_client_id
```

- `ZOOM_USER_EMAIL` — tells the S2S app which user to act as (defaults to `me` if unset)
- `ZOOM_RTMS_CLIENT_ID` — Client ID of your RTMS Marketplace app (required for `rtms-start`/`rtms-stop`; this is a **separate app** from the S2S OAuth app)

## Usage

```bash
# Your profile
python3 scripts/zoom.py users me

# List upcoming meetings
python3 scripts/zoom.py meetings list

# List live/in-progress meetings (requires Business+ plan with Dashboard)
python3 scripts/zoom.py meetings live

# Start RTMS for a live meeting
python3 scripts/zoom.py meetings rtms-start <meeting_id>

# Stop RTMS for a live meeting
python3 scripts/zoom.py meetings rtms-stop <meeting_id>

# Schedule a meeting
python3 scripts/zoom.py meetings create --topic "Standup" --start "2026-01-28T10:00:00" --duration 30

# Update meeting settings
python3 scripts/zoom.py meetings update <id> --duration 60 --join-before-host true --auto-recording cloud

# List cloud recordings
python3 scripts/zoom.py recordings list --from "2026-01-01" --to "2026-01-31"

# Download recordings
python3 scripts/zoom.py recordings download <meeting_id> --output ~/Downloads

# Download transcript files
python3 scripts/zoom.py recordings download-transcript <meeting_id> --output ~/Downloads

# Download AI Companion summary as markdown
python3 scripts/zoom.py recordings download-summary <meeting_uuid> --output ~/Downloads

# AI meeting summaries
python3 scripts/zoom.py summary list
python3 scripts/zoom.py summary get <meeting_uuid>

# Send a Team Chat DM
python3 scripts/zoom.py chat dm user@example.com "Hey!"

# Send to a channel
python3 scripts/zoom.py chat send <channel_id> "Hello team!"

# List chat channels
python3 scripts/zoom.py chat channels
```

See [SKILL.md](SKILL.md) for full command reference.

## RTMS Control

The `rtms-start` and `rtms-stop` commands let you programmatically start/stop Real-Time Media Streams for live meetings.

**How it works:**
1. `meetings live` finds in-progress meetings and their host email
2. `rtms-start` looks up the host's user ID via "Get a User" API
3. Calls `PATCH /live_meetings/{meetingId}/rtms_app/status` with the host's `participant_user_id` and your RTMS app's `client_id`

**Requirements:**
- `ZOOM_RTMS_CLIENT_ID` set in `.env` (Client ID of a Marketplace app with RTMS access)
- The RTMS app must be allowed in **Zoom Web Portal → Settings → "Allow apps to access meeting content"**
- `meetings live` requires a Business+ plan with Dashboard enabled

**Companion skill:** Use with [zoom-meeting-assistance-rtms-unofficial-community](https://github.com/tanchunsiong/zoom-meeting-assistance-with-rtms-unofficial-community-skill) to capture and analyze RTMS streams.

## Scopes

Add only the scopes you need in your Zoom Marketplace app:

| Feature | Scopes |
|---|---|
| Users | `user:read:admin` |
| Meetings | `meeting:read:admin`, `meeting:write:admin` |
| Live Meetings | `dashboard_meetings:read:admin` |
| Recordings | `recording:read:admin`, `recording:write:admin` |
| Team Chat | `chat_channel:read:admin`, `chat_message:read:admin`, `chat_message:write:admin` |
| Contacts | `contact:read:admin` |
| AI Summaries | `meeting_summary:read:admin` |
| Phone | `phone:read:admin` |

If you get a scope error, the CLI will tell you exactly which scope to add and link you to the Zoom Marketplace.

## Error Handling

- **Scope errors** — Clear message with link to add the missing scope
- **Rate limits** — Automatic retry with backoff on 429 responses
- **Missing params** — Validates required parameters before calling the API
- **Feature not enabled** — Helpful hint when a Zoom feature isn't available on your plan

## Authentication Details

See [references/AUTH.md](references/AUTH.md) for a detailed guide on setting up Server-to-Server OAuth.

## Related Skills

- **[ngrok-unofficial-webhook-skill](https://github.com/tanchunsiong/ngrok-unofficial-webhook-skill)** — Public webhook endpoint via ngrok for receiving Zoom events
- **[zoom-meeting-assistance-rtms-unofficial-community](https://github.com/tanchunsiong/zoom-meeting-assistance-with-rtms-unofficial-community-skill)** — RTMS meeting capture and AI analysis

## Bug Reports & Contributing

Found a bug? Please raise an issue at:
👉 https://github.com/tanchunsiong/zoom-unofficial-community-skill/issues

Pull requests are also welcome!

## License

MIT
