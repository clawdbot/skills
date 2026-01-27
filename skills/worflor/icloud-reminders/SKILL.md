# iCloud Reminders

CloudKit API access for iOS 13+ Reminders. Full CRUD with alarms, tags, subtasks, and recurrence.

## Setup

### 1. Install dependencies
```bash
pip install pyicloud requests
```

### 2. Get your credentials
- **Email:** Your Apple ID email
- **Password:** Your **main Apple ID password** (not app-specific)
  - 2FA is handled automatically by pyicloud (first run prompts for code)

### 3. First run
```bash
python reminders.py -u "your@email.com" -p "yourpassword" summary
```
If 2FA is enabled, you'll be prompted for a verification code. Session is cached after.

## Usage

```bash
python reminders.py -u EMAIL -p PASSWORD COMMAND [options]
```

Add `--json` for JSON output.

## Commands

### Read
```bash
summary                  # Quick stats (heartbeat-friendly)
pending                  # Incomplete, grouped by list
today | overdue | flagged
lists | tags | all
search "query"
```

### Create
```bash
create "title" [options]

--list NAME              # Target list
--due YYYY-MM-DD         # Due date
--time HH:MM             # Due time (24h format)
--alarm MINUTES          # Alert before due (0, 15, 60, etc.)
--flagged                # Flag it
--priority high|medium|low
--notes "text"
--url URL
--tags "tag1,tag2"       # Hashtags (comma-separated, no #)
--parent REMINDER_ID     # Make subtask
--recurrence daily|weekly|monthly|yearly
--recurrence-interval N  # Every N periods (default: 1)
--recurrence-count N     # Stop after N occurrences
```

### Update
```bash
update "identifier" [options]

--title "new title"
--list NAME
--due YYYY-MM-DD
--flagged | --unflag
--priority high|medium|low
--notes "text"
```

### Other
```bash
complete "identifier"    # Mark done
delete "identifier"      # Delete (cascades alarms)
```

Identifier: Reminder ID (`Reminder/UUID`) or title (partial match).

## Features

| Feature | Create | Read | Update |
|---------|:------:|:----:|:------:|
| Title, List, Due, Flagged, Priority, Notes | ✅ | ✅ | ✅ |
| URL | ✅ | ✅ | - |
| Time-based alarms | ✅ | ✅ | - |
| Hashtags | ✅ | ✅ | - |
| Subtasks | ✅ | ✅ | - |
| Recurrence | ✅ | ✅ | - |

## Limitations

| Feature | Reason | Workaround |
|---------|--------|------------|
| Location alarms | Requires device encryption | Use iOS app |
| Attachments | Complex ASSETID upload | Use iOS app |
| List creation | Server inconsistent | Use iOS app |

## Technical Notes

- **Priority values:** 0=none, 1=high, 5=medium, 9=low
- **Delete cascade:** Automatically removes linked alarms
- **Session cache:** Stored in `~/.pyicloud/` after first auth
