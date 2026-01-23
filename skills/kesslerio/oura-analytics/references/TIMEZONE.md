# Timezone & Day Alignment Guide

## Problem Statement

Oura Ring data involves complex timezone handling:
- **Sleep spans midnight** - Which day does 11pm-7am sleep belong to?
- **Travel across timezones** - User flies SFO → NYC (3hr shift)
- **Local vs UTC timestamps** - API returns UTC, users think in local time
- **DST transitions** - Spring forward/fall back can cause "missing" days

## Solution: Canonical Day Mapping

We use a **canonical day** system that maps all events to the user's local timezone.

### Core Principle

> **Canonical day = The calendar date the user would naturally think of**

- Sleep is assigned to the **wake date** (Oura's convention)
- All timestamps converted to user's local timezone
- Consistent day alignment across sleep/readiness/activity

## Configuration

### Set User Timezone

```bash
# Via environment variable
export USER_TIMEZONE="America/Los_Angeles"

# Or in ~/.bashrc / ~/.zshrc
echo 'export USER_TIMEZONE="America/Los_Angeles"' >> ~/.bashrc

# Or pass explicitly to CLI
python oura_api.py report --type weekly --timezone "America/New_York"
```

### Supported Timezones

Any IANA timezone database name:
- `America/Los_Angeles` (PST/PDT)
- `America/New_York` (EST/EDT)
- `Europe/London` (GMT/BST)
- `Asia/Tokyo` (JST)
- `Australia/Sydney` (AEDT/AEST)

Full list: https://en.wikipedia.org/wiki/List_of_tz_database_time_zones

### Default Behavior

If `USER_TIMEZONE` not set, defaults to `America/Los_Angeles`.

## API Functions

### `get_canonical_day(utc_timestamp, user_tz)`

Convert UTC timestamp to user's canonical day.

```python
from scripts.timezone_utils import get_canonical_day

# Example: Sleep ending at 7am PST
utc_ts = "2026-01-20T15:06:44.000+00:00"  # 7am PST in UTC
canonical_date, local_dt = get_canonical_day(utc_ts, "America/Los_Angeles")

print(canonical_date)  # 2026-01-20
print(local_dt)         # 2026-01-20 07:06:44 PST
```

**Returns:** `(date, datetime)` tuple or `(None, None)` if invalid

### `get_canonical_day_from_date_str(date_str, user_tz)`

Convert date string (YYYY-MM-DD) to canonical day.

```python
from scripts.timezone_utils import get_canonical_day_from_date_str

canonical = get_canonical_day_from_date_str("2026-01-20", "America/Los_Angeles")
print(canonical)  # 2026-01-20
```

**Returns:** `date` object or `None` if invalid

### `is_travel_day(sleep_records, threshold_hours, user_tz)`

Detect potential travel days based on bedtime shifts.

```python
from scripts.timezone_utils import is_travel_day
from scripts.oura_api import OuraClient

client = OuraClient()
sleep_data = client.get_sleep("2026-01-01", "2026-01-31")
travel_days = is_travel_day(sleep_data, threshold_hours=3.0)

# Example output: [date(2026-01-15), date(2026-01-22)]
print(f"Travel days: {travel_days}")
```

**Algorithm:**
1. Calculate median bedtime hour across all records
2. Flag days where bedtime shifts >3 hours from median
3. Handles wraparound at midnight (23:00 vs 01:00)

**Threshold:** Default 3 hours (detects cross-timezone travel)

### `group_by_canonical_day(data, timestamp_field, user_tz)`

Group records by canonical day.

```python
from scripts.timezone_utils import group_by_canonical_day

grouped = group_by_canonical_day(sleep_data, timestamp_field="day")

for date_str, records in grouped.items():
    print(f"{date_str}: {len(records)} records")
```

**Returns:** Dict mapping date strings to record lists

### `format_localized_datetime(utc_timestamp, fmt, user_tz)`

Format UTC timestamp in user's local time.

```python
from scripts.timezone_utils import format_localized_datetime

utc_ts = "2026-01-20T15:06:44.000+00:00"
local_str = format_localized_datetime(utc_ts, fmt="%Y-%m-%d %H:%M %Z")

print(local_str)  # "2026-01-20 07:06 PST"
```

## Edge Cases

### 1. Sleep Spanning Midnight

**Scenario:** Bedtime 11pm Jan 19 → Wake 7am Jan 20

**Oura Convention:** Sleep assigned to wake date (Jan 20)

**Our Handling:**
```python
sleep_record = {
    "day": "2026-01-20",           # Wake date
    "bedtime_start": "2026-01-19T23:00:00-08:00",  # Previous night
    "bedtime_end": "2026-01-20T07:00:00-08:00"     # Wake morning
}

canonical_date, _ = get_canonical_day(sleep_record["bedtime_end"])
print(canonical_date)  # 2026-01-20 (wake date)
```

**Consistent:** Always use wake date for canonical day

### 2. Travel Across Timezones

**Scenario:** User flies SFO → NYC (3hr forward) on Jan 15

**Data Pattern:**
```
Jan 14: Bedtime 23:00 PST → Wake 07:00 PST
Jan 15: Bedtime 02:00 EST → Wake 10:00 EST  (travel day, unusual bedtime)
Jan 16: Bedtime 23:00 EST → Wake 07:00 EST  (back to normal)
```

**Detection:**
```python
travel_days = is_travel_day(sleep_data, threshold_hours=3.0)
# Returns: [date(2026-01-15)]
```

**Usage:**
- Flag travel days in reports
- Exclude from baseline calculations
- Show "(travel)" annotation in summaries

### 3. Local vs UTC Timestamps

**Oura API Returns:** UTC or offset-aware timestamps

**Example:**
```json
{
  "bedtime_start": "2026-01-20T07:00:00.000+00:00",  # UTC
  "bedtime_end": "2026-01-20T15:00:00.000+00:00"      # UTC
}
```

**Conversion:**
```python
# API returns UTC
utc_start = "2026-01-20T07:00:00.000+00:00"

# Convert to user's local time (PST = UTC-8)
canonical_date, local_dt = get_canonical_day(utc_start, "America/Los_Angeles")
print(local_dt)  # 2026-01-19 23:00:00 PST
```

**Reports:** Always show local times, not UTC

### 4. DST Transitions

**Spring Forward (losing 1 hour):**
```
# On 2026-03-08 at 2am PST → 3am PDT
Bedtime: 2026-03-07 23:00 PST
Wake: 2026-03-08 07:00 PDT  # Only 7 hours of wall-clock time, but 8 hours elapsed
```

**Fall Back (gaining 1 hour):**
```
# On 2026-11-01 at 2am PDT → 1am PST
Bedtime: 2026-10-31 23:00 PDT
Wake: 2026-11-01 07:00 PST  # 9 hours of wall-clock time, but only 8 hours elapsed
```

**Handling:**
- Oura tracks **elapsed time** (correct)
- Our timezone conversion handles DST automatically (via `pytz`)
- No manual adjustment needed

**Test:**
```python
# Spring forward example
utc_ts = "2026-03-08T15:00:00.000+00:00"  # 7am PDT
canonical_date, local_dt = get_canonical_day(utc_ts, "America/Los_Angeles")
print(local_dt.tzname())  # "PDT" (not "PST")
```

## CLI Examples

### View Sleep with Local Times

```bash
# Sleep records with local timestamps
python oura_api.py sleep --days 7 --local-time --timezone "America/Los_Angeles"
```

**Output:**
```json
{
  "day": "2026-01-20",
  "bedtime_start": "2026-01-19T23:27:58.000-08:00",
  "bedtime_end": "2026-01-20T07:06:44.000-08:00",
  "local_bedtime_start": "2026-01-19T23:27:58-08:00"
}
```

### Weekly Report with Timezone

```bash
# Report in user's timezone
python oura_api.py report --type weekly --timezone "America/New_York"
```

**Output:**
```json
{
  "report_type": "weekly",
  "period": "2026-01-14 to 2026-01-21",
  "timezone": "America/New_York",
  "travel_days": ["2026-01-18"],
  "summary": { ... }
}
```

### Travel Day Detection

```bash
# Show which days had unusual bedtimes (travel)
python oura_api.py report --type weekly --timezone "America/Los_Angeles" | \
  jq '.travel_days'
```

**Output:**
```json
["2026-01-18", "2026-01-19"]
```

## Integration with Schema

The canonical schema (`scripts/schema.py`) preserves timezone info:

```python
from scripts.schema import normalize_sleep

sleep_record = normalize_sleep(raw_oura_data)

# All timestamps preserve timezone
print(sleep_record.bedtime_start)  # "2026-01-19T23:27:58.000-08:00"
print(sleep_record.bedtime_end)    # "2026-01-20T07:06:44.000-08:00"

# Date is in local timezone
print(sleep_record.date)  # "2026-01-20" (wake date in user's local timezone)
```

## Best Practices

### 1. Always Pass User Timezone

```python
# Good: Explicit timezone
from scripts.timezone_utils import get_canonical_day
canonical, local_dt = get_canonical_day(timestamp, user_tz="America/Los_Angeles")

# Acceptable: Rely on USER_TIMEZONE env var
canonical, local_dt = get_canonical_day(timestamp)  # Uses env var or default
```

### 2. Handle None Returns

```python
canonical, local_dt = get_canonical_day(timestamp)
if canonical is None:
    print("Invalid timestamp")
    return

# Safe to use canonical
print(f"Date: {canonical}")
```

### 3. Flag Travel Days in Analysis

```python
travel_days = is_travel_day(sleep_data)

for record in sleep_data:
    date = record["day"]
    is_travel = date in [str(d) for d in travel_days]
    if is_travel:
        print(f"{date} (travel) - exclude from baseline")
    else:
        # Include in baseline calculation
        pass
```

### 4. Use Canonical Day for Joining

```python
from scripts.timezone_utils import group_by_canonical_day

# Group all data sources by canonical day
sleep_by_day = group_by_canonical_day(sleep_data, "day")
readiness_by_day = group_by_canonical_day(readiness_data, "day")
activity_by_day = group_by_canonical_day(activity_data, "day")

# Join on canonical day
for date_str in sleep_by_day.keys():
    sleep = sleep_by_day[date_str][0]
    readiness = readiness_by_day.get(date_str, [None])[0]
    activity = activity_by_day.get(date_str, [None])[0]
    
    # Now have aligned data for this day
    print(f"{date_str}: Sleep={sleep}, Readiness={readiness}, Activity={activity}")
```

## Troubleshooting

### "Unknown timezone" error

```bash
# Set valid IANA timezone
export USER_TIMEZONE="America/Los_Angeles"

# Not "PST" or "Pacific Time"
# Use IANA database name
```

### Missing `pytz` module

```bash
pip install pytz
```

### Unexpected date assignments

```python
# Check what Oura assigned
print(raw_record["day"])  # Oura's wake date

# Check your local conversion
canonical, local_dt = get_canonical_day(raw_record["bedtime_end"])
print(canonical)  # Should match Oura's day
```

## Technical Details

### Day Assignment Logic

```
Oura Rule: Sleep assigned to wake date
Our Rule: Use wake date as canonical day

Example:
  Bedtime: Jan 19, 11:30pm
  Wake: Jan 20, 7:00am
  Oura day: "2026-01-20"
  Canonical day: 2026-01-20
```

**Consistent:** Always use Oura's day assignment

### Timezone Conversion

```python
# 1. Parse UTC timestamp
utc_dt = datetime.fromisoformat(utc_timestamp)

# 2. Localize to UTC (if naive)
utc_dt = pytz.UTC.localize(utc_dt)

# 3. Convert to user's timezone
user_tz_obj = pytz.timezone(user_tz)
local_dt = utc_dt.astimezone(user_tz_obj)

# 4. Extract date
canonical_date = local_dt.date()
```

### Travel Detection Algorithm

```python
1. Extract bedtime hour for each record (in local time)
2. Calculate median bedtime hour
3. For each record:
   - Compute shift from median
   - Handle wraparound (23 vs 01 = 2hr shift, not 22hr)
   - Flag if shift > threshold (default 3 hours)
4. Return list of flagged dates
```

## See Also

- [SCHEMA.md](./SCHEMA.md) - Canonical data structures
- [Oura API Docs](https://cloud.ouraring.com/v2/docs) - Official API
- [pytz Documentation](https://pythonhosted.org/pytz/) - Timezone library
- [IANA Timezone Database](https://www.iana.org/time-zones) - Timezone names
