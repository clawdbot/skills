# API Response Schemas

## Output Formats

The CLI supports multiple output formats via `--format` flag:

| Format | Description | Use Case |
|--------|-------------|----------|
| `json` | Full structured data (default) | API integration, Clawdbot parsing |
| `brief` | 5-8 line human summary | Quick checks, Telegram messages |
| `alert` | Warnings only (empty if OK) | Health monitoring, alerts |
| `silent` | No output (exit code only) | Cron jobs, background tasks |

## Summary Response (`summary` command)

**JSON format:**
```json
{
  "avg_sleep_score": 85.3,
  "avg_readiness_score": 78.0,
  "avg_sleep_hours": 7.2,
  "avg_sleep_efficiency": 88.5,
  "avg_hrv": 42.3,
  "days_tracked": 7
}
```

**Brief format:**
```
avg_sleep_score: 85.3
avg_readiness_score: 78.0
avg_sleep_hours: 7.2
avg_sleep_efficiency: 88.5
avg_hrv: 42.3
days_tracked: 7
```

**Alert format:**
```
⚠️  Low sleep: 5.8h avg
⚠️  Low readiness: 65
```

**Schema:**

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `avg_sleep_score` | float | 0-100 | Average sleep quality score |
| `avg_readiness_score` | float/null | 0-100 | Average readiness score (null if unavailable) |
| `avg_sleep_hours` | float | 0-12 | Average sleep duration in hours |
| `avg_sleep_efficiency` | float | 0-100 | Average sleep efficiency percentage |
| `avg_hrv` | float/null | 0-200 | Average HRV in milliseconds |
| `days_tracked` | int | 0+ | Number of days in summary |

## Report Response (`report` command)

**JSON format:**
```json
{
  "report_type": "weekly",
  "period": "2026-01-14 to 2026-01-21",
  "timezone": "America/Los_Angeles",
  "travel_days": ["2026-01-18", "2026-01-19"],
  "summary": {
    "avg_sleep_score": 85.3,
    "avg_readiness_score": 78.0,
    "avg_sleep_hours": 7.2,
    "avg_sleep_efficiency": 88.5,
    "avg_hrv": 42.3,
    "days_tracked": 7
  },
  "daily_data": {
    "sleep": [...],
    "readiness": [...],
    "activity": [...]
  }
}
```

**Brief format:**
```
📊 Weekly (2026-01-14 to 2026-01-21)
Sleep: 7.2h avg, 85.3 score
Readiness: 78.0
Efficiency: 88.5%
HRV: 42.3 ms
Days: 7
Travel: 2026-01-18, 2026-01-19
```

**Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `report_type` | string | "weekly" or "monthly" |
| `period` | string | ISO date range "YYYY-MM-DD to YYYY-MM-DD" |
| `timezone` | string | IANA timezone (e.g., "America/Los_Angeles") |
| `travel_days` | array[string] | ISO dates with potential travel/timezone shifts |
| `summary` | object | Same schema as Summary Response |
| `daily_data` | object | Raw Oura API data (sleep, readiness, activity arrays) |

## Comparison Response (`comparison` command)

**JSON format:**
```json
{
  "current": {
    "avg_sleep_score": 85.3,
    "avg_sleep_hours": 7.2,
    ...
  },
  "previous": {
    "avg_sleep_score": 82.1,
    "avg_sleep_hours": 6.8,
    ...
  },
  "diff": {
    "avg_sleep_score": 3.2,
    "avg_sleep_hours": 0.4,
    ...
  }
}
```

**Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `current` | object | Summary for current period |
| `previous` | object | Summary for previous period (same duration) |
| `diff` | object | Difference (current - previous) for numeric fields |

## Sleep Data Response (`sleep` command)

**JSON format:**
```json
[
  {
    "id": "abc123",
    "day": "2026-01-20",
    "bedtime_start": "2026-01-19T23:30:00.000-08:00",
    "bedtime_end": "2026-01-20T07:15:00.000-08:00",
    "total_sleep_duration": 27000,
    "efficiency": 88,
    "average_hrv": 42,
    "score": 85
  }
]
```

**Brief format:**
```
8 records
```

**Schema:** See [Oura API Documentation](https://cloud.ouraring.com/v2/docs) for full field definitions.

## Sync Response (`sync` command)

**JSON format:**
```json
{
  "sleep": 7,
  "daily_readiness": 7,
  "daily_activity": 7
}
```

**Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `<endpoint>` | int | Number of days synced for endpoint |

## Cache Stats Response (`cache` command)

**JSON format:**
```json
{
  "sleep": {
    "cached_days": 90,
    "last_sync": "2026-01-21"
  },
  "daily_readiness": {
    "cached_days": 90,
    "last_sync": "2026-01-21"
  }
}
```

**Schema:**

| Field | Type | Description |
|-------|------|-------------|
| `<endpoint>.cached_days` | int | Number of cached day files |
| `<endpoint>.last_sync` | string/null | ISO date of last sync, null if never synced |

## Error Response

**All commands use consistent error handling:**

**Standard Error (stderr):**
```
Error: OURA_API_TOKEN not set. Get it at https://cloud.ouraring.com/personal-access-token
```

**Exit Codes:**

| Code | Meaning |
|------|---------|
| 0 | Success |
| 1 | Configuration error (missing token, invalid args) |
| 2 | API error (rate limit, auth failure, network error) |
| 3 | Data error (no data available, cache issue) |

**Error Format (JSON):**
```json
{
  "error": "RateLimitError",
  "message": "Rate limited. Waiting 60s before retry...",
  "code": 2
}
```

## Alert Thresholds

**Used in `--format alert` mode:**

| Metric | Threshold | Alert Triggered When |
|--------|-----------|---------------------|
| Sleep hours | 6h | avg_sleep_hours < 6 |
| Readiness | 70 | avg_readiness_score < 70 |
| Efficiency | 80% | avg_sleep_efficiency < 80 |

**No output is produced if all metrics are above thresholds.**

## Usage Examples

```bash
# Get full JSON (default)
python oura_api.py summary --days 7

# Get brief summary (human-readable)
python oura_api.py report --type weekly --format brief

# Check for alerts (empty if OK)
python oura_api.py summary --days 7 --format alert

# Cron job (silent, exit code only - reflects script success, not health status)
python oura_api.py summary --days 7 --format silent
if [ $? -ne 0 ]; then
  echo "Script execution failed"
fi

# For health-based cron alerts, use alert mode:
ALERTS=$(python oura_api.py summary --days 7 --format alert)
if [ -n "$ALERTS" ]; then
  echo "$ALERTS"
fi
```
