# iCloud Reminders CloudKit API Reference

## Overview

iOS 13+ stores Reminders in CloudKit container `com.apple.reminders`. This document details the API behavior discovered through reverse engineering.

## Authentication

Uses pyicloud session with main Apple ID credentials (not app-specific password for CalDAV).

```python
from pyicloud import PyiCloudService
api = PyiCloudService(email, password)
ck_url = api.get_webservice_url('ckdatabasews')
```

## Endpoints

Base URL: `https://pXXX-ckdatabasews.icloud.com:443/database/1/com.apple.reminders/production/private/`

### zones/list
Get available zones.

```json
POST /zones/list
{}
```

Response includes:
- `Reminders` - Main zone with all data (use this)
- `RemindersMigration` - Migration tracking (empty)
- `_defaultZone` - Default zone (can't query changes)

**IMPORTANT:** Zone ID includes `ownerRecordName` which must be used in all requests:
```json
{
  "zoneName": "Reminders",
  "ownerRecordName": "_a9a19481e77141536eb672b297d0ce4c",
  "zoneType": "REGULAR_CUSTOM_ZONE"
}
```

### records/changes
Fetch all records (supports pagination).

```json
POST /records/changes
{
  "zoneID": {...}
}
```

For pagination, use `syncToken` from response:
```json
{
  "zoneID": {...},
  "syncToken": "HwoD..."
}
```

Response:
- `records`: Array of records
- `moreComing`: Boolean for pagination
- `syncToken`: Use for next request

### records/lookup
Fetch specific records by name.

```json
POST /records/lookup
{
  "records": [{"recordName": "Reminder/xxx"}],
  "zoneID": {...}
}
```

### records/query
Query records by type. **NOTE: Most types return FIELD_NOT_QUERYABLE error.**

```json
POST /records/query
{
  "zoneID": {...},
  "query": {"recordType": "Reminder"},
  "resultsLimit": 100
}
```

### records/modify
Create, update, or delete records.

```json
POST /records/modify
{
  "zoneID": {...},
  "operations": [
    {
      "operationType": "create|update|forceUpdate|delete|forceDelete",
      "record": {...}
    }
  ]
}
```

## Operation Types

| Operation | recordChangeTag Required | Description |
|-----------|-------------------------|-------------|
| `create` | No | Create new record |
| `update` | **Yes** | Update with conflict check |
| `forceUpdate` | No | Update without conflict check |
| `delete` | **Yes** | Delete with conflict check |
| `forceDelete` | No | Delete without conflict check |

## Record Types

### Reminder
Main reminder record.

**Required Fields:**
| Field | Type | Description |
|-------|------|-------------|
| TitleDocument | ENCRYPTED_BYTES | Protobuf-encoded title |
| List | REFERENCE | Reference to List record |
| Completed | NUMBER_INT64 | 0=pending, 1=completed |
| Deleted | NUMBER_INT64 | 0=active, 1=deleted |
| CreationDate | TIMESTAMP | Creation timestamp (ms) |
| LastModifiedDate | TIMESTAMP | Last modified (ms) |

**Optional Fields:**
| Field | Type | Description |
|-------|------|-------------|
| Flagged | NUMBER_INT64 | 0=no, 1=flagged |
| Priority | NUMBER_INT64 | 0=none, 1=high, 5=medium, 9=low |
| AllDay | NUMBER_INT64 | 0=specific time, 1=all-day |
| DueDate | TIMESTAMP | Due date (ms) |
| TimeZone | STRING | e.g., "America/Toronto" |
| NotesDocument | ENCRYPTED_BYTES | Protobuf-encoded notes |
| CompletionDate | TIMESTAMP | When completed (ms) |
| AlarmIDs | STRING_LIST | UUIDs of linked Alarm records |
| HashtagIDs | STRING_LIST | UUIDs of linked Hashtag records |
| RecurrenceRuleIDs | STRING_LIST | UUIDs of recurrence rules |
| AttachmentIDs | STRING_LIST | UUIDs of attachments |
| Imported | NUMBER_INT64 | Migration flag |

### List
Reminder list/folder.

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| Name | STRING (auto-encrypted) | List name |
| Color | STRING | JSON color data |
| IsGroup | NUMBER_INT64 | 1=folder, 0=list |
| IsLinkedToAccount | NUMBER_INT64 | Account linked |
| ParentList | REFERENCE | Parent folder (optional) |
| SortingStyle | STRING | "manual" etc. |
| Deleted | NUMBER_INT64 | Soft delete flag |
| BadgeEmblem | STRING | Icon name (optional) |

### Alarm
Reminder alarm/notification.

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| AlarmUID | STRING | UUID matching Reminder.AlarmIDs |
| TriggerID | STRING | UUID of AlarmTrigger |
| Reminder | REFERENCE | Parent reminder |
| Deleted | NUMBER_INT64 | Soft delete flag |
| AcknowledgedDate | TIMESTAMP | When dismissed |

### AlarmTrigger
Alarm trigger configuration.

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| Type | STRING | "Date" for time-based |
| DateComponentsData | BYTES | Base64 JSON with time info |
| Alarm | REFERENCE | Parent Alarm record |
| Deleted | NUMBER_INT64 | Soft delete flag |

DateComponentsData format:
```json
{
  "minute": 0,
  "hour": 9,
  "second": 0,
  "timeZone": {"identifier": "America/Toronto"}
}
```

### SmartList
System smart lists (Today, Scheduled, Flagged, etc.)

### Hashtag
Tags attached to reminders.

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| Name | STRING | Tag name (without #) |
| Reminder | REFERENCE | Parent reminder |
| Type | NUMBER_INT64 | Tag type |
| CreationDate | TIMESTAMP | When created |

### RecurrenceRule
Recurring reminder rules.

**Fields:**
| Field | Type | Description |
|-------|------|-------------|
| Frequency | NUMBER_INT64 | 0=daily, 1=weekly, etc. |
| Interval | NUMBER_INT64 | Every N periods |
| EndDate | TIMESTAMP | When recurrence ends |
| OccurrenceCount | NUMBER_INT64 | Max occurrences |
| Reminder | REFERENCE | Parent reminder |

## Reference Relationships

```
Reminder.List -> List
Reminder.ParentReminder -> Reminder (subtasks)
List.ParentList -> List (folder hierarchy)
Alarm.Reminder -> Reminder
AlarmTrigger.Alarm -> Alarm
Hashtag.Reminder -> Reminder
Attachment.Reminder -> Reminder
RecurrenceRule.Reminder -> Reminder
ListSection.List -> List
```

**DELETE ORDER:** When deleting a Reminder with alarms:
1. Delete AlarmTrigger records first
2. Delete Alarm records
3. Delete Reminder

## TitleDocument Format

The TitleDocument field uses a specific protobuf structure:

```
base64(gzip(protobuf))
```

Protobuf structure:
```
Field 1 (varint): 0
Field 2 (bytes): styled text container
  Field 1 (varint): 0
  Field 2 (varint): 0
  Field 3 (bytes): text content
    Field 2 (string): actual title text
    Field 3+ : text styling attributes (font, range, UUID)
```

Simple text won't sync to iOS — must use this exact format.

## Timestamps

All timestamps are **milliseconds since Unix epoch** (int64).

```python
import time
now_ms = int(time.time() * 1000)
```

## Field Types

| Type | Description |
|------|-------------|
| STRING | Plain text |
| NUMBER_INT64 | 64-bit integer |
| NUMBER_DOUBLE | Double precision float |
| TIMESTAMP | Milliseconds since epoch |
| BYTES | Base64-encoded binary |
| ENCRYPTED_BYTES | Base64(gzip(protobuf)) |
| REFERENCE | Link to another record |
| STRING_LIST | Array of strings |
| EMPTY_LIST | Empty array |
| ASSETID | File attachment reference |

## Reference Format

```json
{
  "value": {
    "recordName": "Type/UUID",
    "action": "NONE",
    "zoneID": {
      "zoneName": "Reminders",
      "ownerRecordName": "...",
      "zoneType": "REGULAR_CUSTOM_ZONE"
    }
  },
  "type": "REFERENCE"
}
```

Actions: `NONE` (no validation), `VALIDATE` (check exists)

## Error Codes

| Code | Meaning |
|------|---------|
| BAD_REQUEST | Missing required field or invalid format |
| FIELD_NOT_QUERYABLE | Record type can't be queried directly |
| NOT_FOUND | Record doesn't exist |
| CONFLICT | recordChangeTag mismatch |
| VALIDATING_REFERENCE | Can't delete - referenced by another record |

## Best Practices

1. **Always fetch zone ID dynamically** — ownerRecordName changes per account
2. **Use forceUpdate** when you don't need conflict detection
3. **Delete in dependency order** — triggers → alarms → reminders
4. **Use proper protobuf encoding** for TitleDocument/NotesDocument
5. **Include recordChangeTag** for update/delete operations
6. **Handle pagination** for accounts with many reminders

## Query Limitations

Most record types return `FIELD_NOT_QUERYABLE` for direct queries. Use `/records/changes` to fetch all records and filter client-side.
