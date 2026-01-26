# Google Calendar API Quick Reference

## Base URL
```
https://www.googleapis.com/calendar/v3
```

## Authentication
All requests require OAuth 2.0 Bearer token:
```
Authorization: Bearer {access_token}
```

## Common Endpoints

### List Events
```
GET /calendars/{calendarId}/events
```

Parameters:
- `timeMin` (datetime): Start of range (RFC3339)
- `timeMax` (datetime): End of range (RFC3339)
- `maxResults` (int): Max events to return
- `singleEvents` (bool): Expand recurring events
- `orderBy` (string): "startTime" or "updated"
- `q` (string): Search query

### Get Event
```
GET /calendars/{calendarId}/events/{eventId}
```

### Create Event
```
POST /calendars/{calendarId}/events
```

Body:
```json
{
  "summary": "Event title",
  "description": "Details",
  "location": "Address",
  "start": {
    "dateTime": "2026-01-27T10:00:00-05:00",
    "timeZone": "America/New_York"
  },
  "end": {
    "dateTime": "2026-01-27T11:00:00-05:00",
    "timeZone": "America/New_York"
  },
  "attendees": [
    {"email": "person@example.com"}
  ]
}
```

### Quick Add (Natural Language)
```
POST /calendars/{calendarId}/events/quickAdd?text={text}
```

Example text: "Lunch with Alex Friday noon at Cafe Roma"

### Update Event
```
PUT /calendars/{calendarId}/events/{eventId}
```
or
```
PATCH /calendars/{calendarId}/events/{eventId}
```

### Delete Event
```
DELETE /calendars/{calendarId}/events/{eventId}
```

### List Calendars
```
GET /users/me/calendarList
```

### Free/Busy Query
```
POST /freeBusy
```

Body:
```json
{
  "timeMin": "2026-01-27T00:00:00Z",
  "timeMax": "2026-01-28T00:00:00Z",
  "items": [{"id": "primary"}]
}
```

## Event Object

```json
{
  "id": "abc123",
  "summary": "Meeting",
  "description": "Discuss project",
  "location": "Conference Room A",
  "start": {
    "dateTime": "2026-01-27T10:00:00-05:00",
    "timeZone": "America/New_York"
  },
  "end": {
    "dateTime": "2026-01-27T11:00:00-05:00",
    "timeZone": "America/New_York"
  },
  "attendees": [
    {
      "email": "person@example.com",
      "responseStatus": "accepted"
    }
  ],
  "organizer": {
    "email": "me@example.com",
    "self": true
  },
  "status": "confirmed",
  "htmlLink": "https://calendar.google.com/event?eid=..."
}
```

## All-Day Events

Use `date` instead of `dateTime`:
```json
{
  "start": {"date": "2026-01-27"},
  "end": {"date": "2026-01-28"}
}
```

## Recurring Events

```json
{
  "recurrence": [
    "RRULE:FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20261231"
  ]
}
```

## Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 201 | Created |
| 204 | Deleted (no content) |
| 400 | Bad request |
| 401 | Unauthorized (token expired) |
| 403 | Forbidden (no access) |
| 404 | Not found |
| 410 | Gone (deleted) |
| 429 | Rate limited |

## Rate Limits

- ~10 requests/second per user
- Exponential backoff recommended

## Scopes

| Scope | Access |
|-------|--------|
| `calendar.readonly` | Read calendars and events |
| `calendar.events` | Read/write events only |
| `calendar` | Full access |
