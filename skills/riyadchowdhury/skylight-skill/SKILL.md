---
name: skylight
description: Interact with Skylight Calendar frame - manage calendar events, chores, lists, task box items, and rewards. Use when the user wants to view/create calendar events, manage family chores, work with shopping or to-do lists, check reward points, or interact with their Skylight smart display.
homepage: https://ourskylight.com
metadata:
  clawdbot:
    emoji: 📅
    requires:
      bins:
        - curl
      env:
        - SKYLIGHT_FRAME_ID
    primaryEnv: SKYLIGHT_EMAIL
---

# Skylight Calendar

Control Skylight Calendar frame via the unofficial API.

## Setup

Set environment variables:
- `SKYLIGHT_URL`: Base URL (default: `https://app.ourskylight.com`)
- `SKYLIGHT_FRAME_ID`: Your frame (household) ID — find this by logging into [ourskylight.com](https://ourskylight.com/), clicking your calendar, and copying the number from the URL (e.g., `4197102` from `https://ourskylight.com/calendar/4197102`)

**Authentication (choose one):**

Option A - Email/Password (recommended):
- `SKYLIGHT_EMAIL`: Your Skylight account email
- `SKYLIGHT_PASSWORD`: Your Skylight account password

Option B - Pre-captured token:
- `SKYLIGHT_TOKEN`: Full Authorization header value (e.g., `Basic abc123...`)

## Authentication

### Option A: Login with Email/Password (Recommended)

Generate a token by logging in with email and password:

```bash
# Login and get user credentials
LOGIN_RESPONSE=$(curl -s -X POST "$SKYLIGHT_URL/api/sessions" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "'"$SKYLIGHT_EMAIL"'",
    "password": "'"$SKYLIGHT_PASSWORD"'",
    "name": "",
    "phone": "",
    "resettingPassword": "false",
    "textMeTheApp": "true",
    "agreedToMarketing": "true"
  }')

# Extract user_id and user_token from response
USER_ID=$(echo "$LOGIN_RESPONSE" | jq -r '.data.id')
USER_TOKEN=$(echo "$LOGIN_RESPONSE" | jq -r '.data.attributes.token')

# Generate Basic auth token (base64 of user_id:user_token)
SKYLIGHT_TOKEN="Basic $(echo -n "${USER_ID}:${USER_TOKEN}" | base64)"

# Now use $SKYLIGHT_TOKEN for all API requests
```

The login endpoint returns:
- `data.id`: User ID
- `data.attributes.token`: User token

Combine as `{user_id}:{user_token}` and base64 encode for Basic auth.

### Option B: Capture Token via Proxy

If you prefer to capture a token manually:

1. Install Proxyman/Charles/mitmproxy and trust root certificate
2. Enable SSL proxying for `app.ourskylight.com`
3. Log into Skylight app and capture any API request
4. Copy `Authorization` header value (e.g., `Basic <token>`)

Tokens rotate on logout; recapture after re-login.

## API Format

Responses use JSON:API format with `data`, `included`, and `relationships` fields.

## Calendar Events

### List events
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/calendar_events?date_min=2025-01-27&date_max=2025-01-31" \
  -H "Authorization: $SKYLIGHT_TOKEN" \
  -H "Accept: application/json"
```

Query params:
- `date_min` (required): Start date YYYY-MM-DD
- `date_max` (required): End date YYYY-MM-DD
- `timezone`: Timezone string (optional)
- `include`: CSV of related resources (`categories,calendar_account,event_notification_setting`)

### List source calendars
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/source_calendars" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

## Chores

### List chores
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/chores?after=2025-01-27&before=2025-01-31" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

Query params:
- `after`: Start date YYYY-MM-DD
- `before`: End date YYYY-MM-DD
- `include_late`: Include overdue chores (bool)
- `filter`: Filter by `linked_to_profile`

### Create chore
```bash
curl -s -X POST "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/chores" \
  -H "Authorization: $SKYLIGHT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "type": "chore",
      "attributes": {
        "summary": "Take out trash",
        "status": "pending",
        "start": "2025-01-28",
        "start_time": "08:00",
        "recurring": false
      },
      "relationships": {
        "category": {
          "data": {"type": "category", "id": "CATEGORY_ID"}
        }
      }
    }
  }'
```

Chore attributes:
- `summary`: Chore title
- `status`: `pending` or `completed`
- `start`: Date YYYY-MM-DD
- `start_time`: Time HH:MM (optional)
- `recurring`: Boolean
- `recurrence_set`: RRULE string for recurring chores
- `reward_points`: Integer (optional)
- `emoji_icon`: Emoji (optional)

## Lists (Shopping/To-Do)

### List all lists
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/lists" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

### Get list with items
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/lists/{listId}" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

Response includes `data.attributes.kind` (`shopping` or `to_do`) and `included` array with list items.

List item attributes:
- `label`: Item text
- `status`: `pending` or `completed`
- `section`: Section name (optional)
- `position`: Sort order

## Task Box

### Create task box item
```bash
curl -s -X POST "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/task_box/items" \
  -H "Authorization: $SKYLIGHT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "data": {
      "type": "task_box_item",
      "attributes": {
        "summary": "Pack lunches"
      }
    }
  }'
```

Task box attributes:
- `summary`: Task title
- `emoji_icon`: Emoji (optional)
- `routine`: Boolean (optional)
- `reward_points`: Integer (optional)

## Categories

### List categories
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/categories" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

Categories are used to assign chores to family members. Attributes include:
- `label`: Category name (e.g., "Mom", "Dad", "Kids")
- `color`: Hex color `#RRGGBB`
- `profile_pic_url`: Avatar URL

## Rewards

### List rewards
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/rewards" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

Optional query: `redeemed_at_min` (datetime) to filter by redemption date.

### List reward points
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/reward_points" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

## Frame Info

### Get frame details
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

### List devices
```bash
curl -s "$SKYLIGHT_URL/api/frames/$SKYLIGHT_FRAME_ID/devices" \
  -H "Authorization: $SKYLIGHT_TOKEN"
```

## Notes

- API is **unofficial** and reverse-engineered; endpoints may change
- Tokens expire on logout; recapture as needed
- Responses return 304 Not Modified when data unchanged
- Use `jq` to parse JSON:API responses
- Frame ID is your household identifier; all resources are scoped to it
