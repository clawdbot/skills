---
name: gcal-pro
description: Google Calendar integration for viewing, creating, and managing calendar events. Use when the user asks about their schedule, wants to add/edit/delete events, check availability, or needs a morning brief. Supports natural language like "What's on my calendar tomorrow?" or "Schedule lunch with Alex at noon Friday." Free tier provides read access; Pro tier ($12) adds create/edit/delete and morning briefs.
---

# gcal-pro

Manage Google Calendar through natural conversation.

## Quick Reference

| Action | Command | Tier |
|--------|---------|------|
| View today | `python scripts/gcal_core.py today` | Free |
| View tomorrow | `python scripts/gcal_core.py tomorrow` | Free |
| View week | `python scripts/gcal_core.py week` | Free |
| Search events | `python scripts/gcal_core.py search -q "meeting"` | Free |
| List calendars | `python scripts/gcal_core.py calendars` | Free |
| Find free time | `python scripts/gcal_core.py free` | Free |
| Quick add | `python scripts/gcal_core.py quick -q "Lunch Friday noon"` | Pro |
| Delete event | `python scripts/gcal_core.py delete --id EVENT_ID -y` | Pro |
| Morning brief | `python scripts/gcal_core.py brief` | Pro |

## Setup

**First-time setup required:**

1. User must create Google Cloud project and OAuth credentials
2. Save `client_secret.json` to `~/.config/gcal-pro/`
3. Run authentication:
   ```bash
   python scripts/gcal_auth.py auth
   ```
4. Browser opens → user grants calendar access → done

**Check auth status:**
```bash
python scripts/gcal_auth.py status
```

## Tiers

### Free Tier
- View events (today, tomorrow, week, month)
- Search events
- List calendars
- Find free time slots

### Pro Tier ($12 one-time)
- Everything in Free, plus:
- Create events
- Quick add (natural language)
- Update/reschedule events
- Delete events
- Morning brief via cron

## Usage Patterns

### Viewing Schedule

When user asks "What's on my calendar?" or "What do I have today?":

```bash
cd /path/to/gcal-pro
python scripts/gcal_core.py today
```

For specific ranges:
- "tomorrow" → `python scripts/gcal_core.py tomorrow`
- "this week" → `python scripts/gcal_core.py week`
- "meetings with Alex" → `python scripts/gcal_core.py search -q "Alex"`

### Creating Events (Pro)

When user says "Add X to my calendar" or "Schedule Y":

**Option 1: Quick add (natural language)**
```bash
python scripts/gcal_core.py quick -q "Lunch with Alex Friday at noon"
```

**Option 2: Structured create (via Python)**
```python
from scripts.gcal_core import create_event, parse_datetime

create_event(
    summary="Lunch with Alex",
    start=parse_datetime("Friday noon"),
    location="Cafe Roma",
    confirmed=True  # Set False to show confirmation prompt
)
```

### Modifying Events (Pro)

**⚠️ CONFIRMATION REQUIRED for destructive actions!**

Before deleting or significantly modifying an event, ALWAYS confirm with the user:

1. Show event details
2. Ask "Should I delete/reschedule this?"
3. Only proceed with `confirmed=True` or `-y` flag after user confirms

**Delete:**
```bash
# First, find the event
python scripts/gcal_core.py search -q "dentist"
# Shows event ID

# Then delete (with user confirmation)
python scripts/gcal_core.py delete --id abc123xyz -y
```

### Finding Free Time

When user asks "When am I free?" or "Find time for a 1-hour meeting":

```bash
python scripts/gcal_core.py free
```

### Morning Brief (Pro + Cron)

Set up via Clawdbot cron to send daily agenda:

```python
from scripts.gcal_core import generate_morning_brief
print(generate_morning_brief())
```

**Cron setup example:**
- Schedule: 8:00 AM daily
- Action: Run `python scripts/gcal_core.py brief`
- Delivery: Send output to user's messaging channel

## Error Handling

| Error | Cause | Solution |
|-------|-------|----------|
| "client_secret.json not found" | Setup incomplete | Complete Google Cloud setup |
| "Token refresh failed" | Expired/revoked | Run `python scripts/gcal_auth.py auth --force` |
| "requires Pro tier" | Free user attempting write | Prompt upgrade or explain limitation |
| "Event not found" | Invalid event ID | Search for correct event first |

## Timezone Handling

- All times are interpreted in user's local timezone (default: America/New_York)
- When user specifies timezone (e.g., "2 PM EST"), honor it
- Display times in user's local timezone
- Store in ISO 8601 format with timezone

## Response Formatting

**For event lists, use this format:**

```
📅 **Monday, January 27**
  • 9:00 AM — Team standup
  • 12:00 PM — Lunch with Alex 📍 Cafe Roma
  • 3:00 PM — Client call

📅 **Tuesday, January 28**
  • 10:00 AM — Dentist appointment 📍 123 Main St
```

**For confirmations:**

```
✓ Event created: "Lunch with Alex"
  📅 Friday, Jan 31 at 12:00 PM
  📍 Cafe Roma
```

**For morning brief:**

```
☀️ Good morning! Here's your day:
📆 Monday, January 27, 2026

You have 3 events today:
  • 9:00 AM — Team standup
  • 12:00 PM — Lunch with Alex
  • 3:00 PM — Client call

👀 Tomorrow: 2 events
```

## File Locations

```
~/.config/gcal-pro/
├── client_secret.json   # OAuth app credentials (user provides)
├── token.json           # User's access token (auto-generated)
└── license.json         # Pro license (if purchased)
```

## Integration with Clawdbot

This skill works with:
- **Cron**: Schedule morning briefs
- **Memory**: Store calendar preferences
- **Messaging**: Deliver briefs via Telegram/WhatsApp/etc.

## Upgrade Prompt

When a Free user attempts a Pro action, respond:

> ⚠️ Creating events requires **gcal-pro Pro** ($12 one-time).
> 
> Pro includes: Create, edit, delete events + morning briefs.
> 
> 👉 Upgrade: [gumroad-link]
> 
> For now, I can show you your schedule (free) — want to see today's events?
