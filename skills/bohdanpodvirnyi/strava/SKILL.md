---
name: strava
description: Load and analyze Strava activities, stats, and workouts using the Strava API
homepage: https://developers.strava.com/
metadata: {"clawdbot":{"emoji":"🏃","requires":{"bins":["curl"],"env":["STRAVA_ACCESS_TOKEN"]},"primaryEnv":"STRAVA_ACCESS_TOKEN"}}
---

# Strava Skill

Interact with Strava to load activities, analyze workouts, and track fitness data.

## Setup

### 1. Create a Strava API Application

1. Go to https://www.strava.com/settings/api
2. Create an app (use `http://localhost` as callback for testing)
3. Note your **Client ID** and **Client Secret**

### 2. Get Initial OAuth Tokens

Visit this URL in your browser (replace CLIENT_ID):
```
https://www.strava.com/oauth/authorize?client_id=CLIENT_ID&response_type=code&redirect_uri=http://localhost&approval_prompt=force&scope=activity:read_all
```

After authorizing, you'll be redirected to `http://localhost/?code=AUTHORIZATION_CODE`

Exchange the code for tokens:
```bash
curl -X POST https://www.strava.com/oauth/token \
  -d client_id=YOUR_CLIENT_ID \
  -d client_secret=YOUR_CLIENT_SECRET \
  -d code=AUTHORIZATION_CODE \
  -d grant_type=authorization_code
```

This returns `access_token` and `refresh_token`.

### 3. Configure Credentials

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

Or use environment variables:
```bash
export STRAVA_ACCESS_TOKEN="your-access-token"
export STRAVA_REFRESH_TOKEN="your-refresh-token"
export STRAVA_CLIENT_ID="your-client-id"
export STRAVA_CLIENT_SECRET="your-client-secret"
```

## Usage

### List Recent Activities

Get the last 30 activities:
```bash
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete/activities?per_page=30"
```

Get the last 10 activities:
```bash
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete/activities?per_page=10"
```

### Filter Activities by Date

Get activities after a specific date (Unix timestamp):
```bash
# Activities after Jan 1, 2024
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete/activities?after=1704067200"
```

Get activities in a date range:
```bash
# Activities between Jan 1 - Jan 31, 2024
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete/activities?after=1704067200&before=1706745600"
```

### Get Activity Details

Get full details for a specific activity (replace ACTIVITY_ID):
```bash
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/activities/ACTIVITY_ID"
```

### Get Athlete Profile

Get the authenticated athlete's profile:
```bash
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete"
```

### Get Athlete Stats

Get athlete statistics (replace ATHLETE_ID):
```bash
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athletes/ATHLETE_ID/stats"
```

### Pagination

Navigate through pages:
```bash
# Page 1 (default)
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete/activities?page=1&per_page=30"

# Page 2
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete/activities?page=2&per_page=30"
```

## Token Refresh

Access tokens expire every 6 hours. Refresh using the helper script:
```bash
bash {baseDir}/scripts/refresh_token.sh
```

Or manually:
```bash
curl -s -X POST https://www.strava.com/oauth/token \
  -d client_id="${STRAVA_CLIENT_ID}" \
  -d client_secret="${STRAVA_CLIENT_SECRET}" \
  -d grant_type=refresh_token \
  -d refresh_token="${STRAVA_REFRESH_TOKEN}"
```

The response includes a new `access_token` and `refresh_token`. Update your configuration with both tokens.

## Common Data Fields

Activity objects include:
- `name` — Activity title
- `distance` — Distance in meters
- `moving_time` — Moving time in seconds
- `elapsed_time` — Total time in seconds
- `total_elevation_gain` — Elevation gain in meters
- `type` — Activity type (Run, Ride, Swim, etc.)
- `sport_type` — Specific sport type
- `start_date` — Start time (ISO 8601)
- `average_speed` — Average speed in m/s
- `max_speed` — Max speed in m/s
- `average_heartrate` — Average heart rate (if available)
- `max_heartrate` — Max heart rate (if available)
- `kudos_count` — Number of kudos received

## Rate Limits

- **200 requests** per 15 minutes
- **2,000 requests** per day

If you hit rate limits, responses will include `X-RateLimit-*` headers.

## Tips

- Convert Unix timestamps: `date -d @TIMESTAMP` (Linux) or `date -r TIMESTAMP` (macOS)
- Convert meters to km: divide by 1000
- Convert meters to miles: divide by 1609.34
- Convert m/s to km/h: multiply by 3.6
- Convert m/s to mph: multiply by 2.237
- Convert seconds to hours: divide by 3600
- Parse JSON with `jq` if available, or use `grep`/`sed` for basic extraction

## Examples

Get running activities from last week with distances:
```bash
LAST_WEEK=$(date -d '7 days ago' +%s 2>/dev/null || date -v-7d +%s)
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete/activities?after=${LAST_WEEK}&per_page=50" \
  | grep -E '"name"|"distance"|"type"'
```

Get total distance from recent activities:
```bash
curl -s -H "Authorization: Bearer ${STRAVA_ACCESS_TOKEN}" \
  "https://www.strava.com/api/v3/athlete/activities?per_page=10" \
  | grep -o '"distance":[0-9.]*' | cut -d: -f2 | awk '{sum+=$1} END {print sum/1000 " km"}'
```

## Error Handling

If you get a 401 Unauthorized error, your access token has expired. Run the token refresh command.

If you get rate limit errors, wait until the limit window resets (check `X-RateLimit-Usage` header).
