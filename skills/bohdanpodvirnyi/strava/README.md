# Strava Skill for Clawdbot

🏃 **Load and analyze your Strava activities, stats, and workouts** using the Strava API.

## Features

- ✅ List recent activities with pagination
- ✅ Filter activities by date ranges
- ✅ Get detailed activity stats (distance, pace, heart rate, elevation)
- ✅ Access athlete profile and cumulative statistics
- ✅ Auto token refresh helper script
- ✅ Rate limit aware (200/15min, 2000/day)
- ✅ Works with curl only (no additional dependencies)

## Quick Start

### 1. Create Strava API Application

Visit https://www.strava.com/settings/api and create an app.

### 2. Get OAuth Tokens

Follow the setup instructions in [SKILL.md](./SKILL.md) to obtain your access token and refresh token.

### 3. Configure

Add to `~/.clawdbot/clawdbot.json`:

```json
{
  "skills": {
    "entries": {
      "strava": {
        "enabled": true,
        "env": {
          "STRAVA_ACCESS_TOKEN": "your-access-token",
          "STRAVA_REFRESH_TOKEN": "your-refresh-token",
          "STRAVA_CLIENT_ID": "your-client-id",
          "STRAVA_CLIENT_SECRET": "your-client-secret"
        }
      }
    }
  }
}
```

## Usage Examples

Ask your agent:
- "Show me my last 10 Strava activities"
- "What activities did I do last week?"
- "Get details for my most recent run"
- "What's my total distance this month?"
- "Show my Strava profile and stats"

## What You Can Do

- **List Activities**: Recent workouts with customizable page size
- **Filter by Date**: Query specific date ranges using Unix timestamps
- **Activity Details**: Full metrics including pace, heart rate, elevation
- **Athlete Stats**: Profile info and cumulative statistics
- **Token Management**: Auto-refresh expired tokens (expire every 6 hours)

## API Coverage

- `GET /athlete/activities` - List activities
- `GET /activities/{id}` - Activity details
- `GET /athlete` - Athlete profile
- `GET /athletes/{id}/stats` - Athlete statistics
- `POST /oauth/token` - Token refresh

## Documentation

See [SKILL.md](./SKILL.md) for complete setup instructions, API reference, and advanced usage.

## Requirements

- `curl` (bundled with macOS/Linux)
- Strava API application credentials
- OAuth access token

## Links

- **Strava Developers**: https://developers.strava.com/
- **API Docs**: https://developers.strava.com/docs/reference/
- **Create App**: https://www.strava.com/settings/api

## License

MIT

## Author

Created for Clawdbot AI Assistant

---

🦞 Part of the Clawdbot skill ecosystem
