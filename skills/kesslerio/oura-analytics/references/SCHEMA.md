# Data Schema Reference

## Overview

This document defines the canonical data structures used by the Oura Analytics skill. All data is normalized to consistent units, naming conventions, and types.

## Design Principles

1. **Explicit units in field names** - No guessing if duration is seconds or hours
2. **Consistent naming** - `_hours`, `_percent`, `_ms`, `_bpm`, `_m`, `_c`
3. **Type safety** - Python dataclasses with type hints
4. **Timezone awareness** - All dates in local timezone (YYYY-MM-DD)
5. **Optional fields** - Missing data is `None`, not `0` or empty string

## Unit Conventions

| Unit Type | Suffix | Example | Notes |
|-----------|--------|---------|-------|
| Duration | `_hours` | `total_sleep_hours` | Converted from Oura's seconds |
| Duration (short) | `_minutes` | `latency_minutes` | For sub-hour durations |
| Percentage | `_percent` | `efficiency_percent` | 0-100 scale |
| Score | (no suffix) | `score` | 0-100 scale |
| Heart rate variability | `_ms` | `average_hrv_ms` | Milliseconds |
| Heart rate | `_bpm` | `average_heart_rate_bpm` | Beats per minute |
| Temperature | `_c` | `temperature_deviation_c` | °Celsius deviation from baseline |
| Distance | `_m` | `equivalent_walking_distance_m` | Meters |
| Calories | (no suffix) | `active_calories` | Kilocalories (kcal) |
| Steps | (no suffix) | `steps` | Count |

## Core Data Structures

### SleepRecord

Normalized sleep data for a single night.

```python
@dataclass
class SleepRecord:
    # Identity
    date: str                          # YYYY-MM-DD (wake date, local timezone)
    id: str                            # Oura record ID
    
    # Timestamps (ISO 8601 with timezone)
    bedtime_start: str                 # When user went to bed
    bedtime_end: str                   # When user woke up
    
    # Sleep durations (hours)
    total_sleep_hours: float           # Total sleep time
    deep_sleep_hours: float            # Deep (N3) sleep
    rem_sleep_hours: float             # REM sleep
    light_sleep_hours: float           # Light (N1+N2) sleep
    awake_hours: float                 # Time awake after sleep onset
    time_in_bed_hours: float           # Total time in bed
    
    # Quality metrics
    efficiency_percent: float          # Sleep efficiency (0-100)
    latency_minutes: Optional[float]   # Time to fall asleep
    
    # Physiological
    average_hrv_ms: Optional[float]    # Heart rate variability
    average_heart_rate_bpm: Optional[float]
    lowest_heart_rate_bpm: Optional[float]
    average_breath_rate: Optional[float]  # Breaths per minute
    
    # Metadata
    restless_periods: Optional[int]    # Count of restless periods
    type: str                          # "long_sleep", "late_nap", etc.
```

**Key fields:**
- `date` - Wake date in local timezone (not bedtime date)
- All durations converted from seconds to hours
- `efficiency_percent` - (total_sleep / time_in_bed) × 100
- `latency_minutes` - Time from bed to sleep onset

### ReadinessRecord

Normalized readiness data for a single day.

```python
@dataclass
class ReadinessRecord:
    # Identity
    date: str                          # YYYY-MM-DD (local timezone)
    id: str                            # Oura record ID
    
    # Overall score
    score: int                         # 0-100 readiness score
    
    # Temperature
    temperature_deviation_c: Optional[float]       # °C from baseline
    temperature_trend_deviation_c: Optional[float] # Trend deviation
    
    # Contributors (all 0-100)
    activity_balance: Optional[int]
    body_temperature: Optional[int]
    hrv_balance: Optional[int]
    previous_day_activity: Optional[int]
    previous_night: Optional[int]
    recovery_index: Optional[int]
    resting_heart_rate: Optional[int]
    sleep_balance: Optional[int]
    sleep_regularity: Optional[int]
    
    # Timestamp
    timestamp: str                     # ISO 8601
```

**Key fields:**
- `score` - Overall readiness (0-100), higher is better
- `temperature_deviation_c` - Deviation from your personal baseline (negative = cooler)
- Contributors show what drove the readiness score

### ActivityRecord

Normalized activity data for a single day.

```python
@dataclass
class ActivityRecord:
    # Identity
    date: str                          # YYYY-MM-DD (local timezone)
    id: str                            # Oura record ID
    
    # Overall
    score: int                         # 0-100 activity score
    steps: int                         # Step count
    
    # Calories (kcal)
    active_calories: int               # Calories from activity
    total_calories: int                # Total daily expenditure
    target_calories: int               # Daily target
    
    # Activity time (hours)
    high_activity_hours: float         # High intensity
    medium_activity_hours: float       # Medium intensity
    low_activity_hours: float          # Low intensity (walking, etc.)
    sedentary_hours: float             # Sitting/minimal movement
    resting_hours: float               # Lying down/sleep
    non_wear_hours: float              # Ring not worn
    
    # MET (metabolic equivalent)
    average_met_minutes: float
    high_activity_met_minutes: int
    medium_activity_met_minutes: int
    low_activity_met_minutes: int
    sedentary_met_minutes: int
    
    # Distance
    equivalent_walking_distance_m: int # Total distance as walking
    target_meters: int                 # Daily target
    meters_to_target: int              # Shortfall/excess
    
    # Metadata
    inactivity_alerts: int             # Count of inactivity alerts
    timestamp: str                     # ISO 8601
```

**Key fields:**
- All activity times converted from seconds to hours
- `active_calories` - Calories burned above resting metabolic rate
- `total_calories` - BMR + active calories
- MET minutes - Metabolic equivalent of task (intensity × duration)

### NightRecord (Unified)

Combined sleep, readiness, and activity for holistic analysis.

```python
@dataclass
class NightRecord:
    date: str                          # YYYY-MM-DD (wake date, local timezone)
    sleep: Optional[SleepRecord]       # Sleep from the night
    readiness: Optional[ReadinessRecord]  # Readiness for the day
    activity: Optional[ActivityRecord]    # Activity from previous day
```

**Usage:**
- Primary structure for analysis and reporting
- Joins data by calendar day (wake date)
- Activity is from previous day (yesterday's steps affect today's readiness)
- All fields are Optional (handles missing data gracefully)

## Normalization Functions

### normalize_sleep(raw: Dict) → SleepRecord

Converts raw Oura sleep API response to normalized SleepRecord.

**Transformations:**
- Converts all durations from seconds to hours
- Renames fields for clarity (`total_sleep_duration` → `total_sleep_hours`)
- Converts latency from seconds to minutes
- Preserves ISO 8601 timestamps with timezone

### normalize_readiness(raw: Dict) → ReadinessRecord

Converts raw Oura readiness API response to normalized ReadinessRecord.

**Transformations:**
- Extracts contributors from nested object
- Preserves temperature deviation in °C

### normalize_activity(raw: Dict) → ActivityRecord

Converts raw Oura activity API response to normalized ActivityRecord.

**Transformations:**
- Converts all time durations from seconds to hours
- Preserves MET minutes and distance in meters

### create_night_record(date, sleep, readiness, activity) → NightRecord

Creates unified NightRecord from raw API data.

**Usage:**
```python
from scripts.schema import create_night_record

night = create_night_record(
    date="2026-01-20",
    sleep=raw_sleep_data,
    readiness=raw_readiness_data,
    activity=raw_activity_data
)

# Access normalized data
print(f"Sleep: {night.sleep.total_sleep_hours}h")
print(f"Readiness: {night.readiness.score}")
print(f"Steps: {night.activity.steps}")
```

## Raw API Mapping

### Sleep API → SleepRecord

| Oura API Field | Schema Field | Transformation |
|----------------|--------------|----------------|
| `day` | `date` | No change |
| `id` | `id` | No change |
| `bedtime_start` | `bedtime_start` | No change |
| `bedtime_end` | `bedtime_end` | No change |
| `total_sleep_duration` | `total_sleep_hours` | seconds → hours (÷ 3600) |
| `deep_sleep_duration` | `deep_sleep_hours` | seconds → hours |
| `rem_sleep_duration` | `rem_sleep_hours` | seconds → hours |
| `light_sleep_duration` | `light_sleep_hours` | seconds → hours |
| `awake_time` | `awake_hours` | seconds → hours |
| `time_in_bed` | `time_in_bed_hours` | seconds → hours |
| `efficiency` | `efficiency_percent` | No change (already 0-100) |
| `latency` | `latency_minutes` | seconds → minutes (÷ 60) |
| `average_hrv` | `average_hrv_ms` | No change (already ms) |
| `average_heart_rate` | `average_heart_rate_bpm` | No change |
| `lowest_heart_rate` | `lowest_heart_rate_bpm` | No change |
| `average_breath` | `average_breath_rate` | No change |
| `restless_periods` | `restless_periods` | No change |
| `type` | `type` | No change |

### Readiness API → ReadinessRecord

| Oura API Field | Schema Field | Transformation |
|----------------|--------------|----------------|
| `day` | `date` | No change |
| `id` | `id` | No change |
| `score` | `score` | No change |
| `temperature_deviation` | `temperature_deviation_c` | No change (already °C) |
| `temperature_trend_deviation` | `temperature_trend_deviation_c` | No change |
| `contributors.activity_balance` | `activity_balance` | Extract from nested |
| `contributors.body_temperature` | `body_temperature` | Extract from nested |
| `contributors.hrv_balance` | `hrv_balance` | Extract from nested |
| `contributors.previous_day_activity` | `previous_day_activity` | Extract from nested |
| `contributors.previous_night` | `previous_night` | Extract from nested |
| `contributors.recovery_index` | `recovery_index` | Extract from nested |
| `contributors.resting_heart_rate` | `resting_heart_rate` | Extract from nested |
| `contributors.sleep_balance` | `sleep_balance` | Extract from nested |
| `contributors.sleep_regularity` | `sleep_regularity` | Extract from nested |
| `timestamp` | `timestamp` | No change |

### Activity API → ActivityRecord

| Oura API Field | Schema Field | Transformation |
|----------------|--------------|----------------|
| `day` | `date` | No change |
| `id` | `id` | No change |
| `score` | `score` | No change |
| `steps` | `steps` | No change |
| `active_calories` | `active_calories` | No change |
| `total_calories` | `total_calories` | No change |
| `target_calories` | `target_calories` | No change |
| `high_activity_time` | `high_activity_hours` | seconds → hours |
| `medium_activity_time` | `medium_activity_hours` | seconds → hours |
| `low_activity_time` | `low_activity_hours` | seconds → hours |
| `sedentary_time` | `sedentary_hours` | seconds → hours |
| `resting_time` | `resting_hours` | seconds → hours |
| `non_wear_time` | `non_wear_hours` | seconds → hours |
| `average_met_minutes` | `average_met_minutes` | No change |
| `high_activity_met_minutes` | `high_activity_met_minutes` | No change |
| `medium_activity_met_minutes` | `medium_activity_met_minutes` | No change |
| `low_activity_met_minutes` | `low_activity_met_minutes` | No change |
| `sedentary_met_minutes` | `sedentary_met_minutes` | No change |
| `equivalent_walking_distance` | `equivalent_walking_distance_m` | No change |
| `target_meters` | `target_meters` | No change |
| `meters_to_target` | `meters_to_target` | No change |
| `inactivity_alerts` | `inactivity_alerts` | No change |
| `timestamp` | `timestamp` | No change |

## CLI Usage

### Get normalized data

```bash
# Coming soon: --normalize flag
python oura_api.py sleep --days 7 --normalize

# Output will use canonical schema with explicit units
```

## Examples

### Sleep Record

```json
{
  "date": "2026-01-20",
  "id": "abc123",
  "bedtime_start": "2026-01-19T23:27:58.000-08:00",
  "bedtime_end": "2026-01-20T07:06:44.000-08:00",
  "total_sleep_hours": 6.79,
  "deep_sleep_hours": 1.6,
  "rem_sleep_hours": 1.53,
  "light_sleep_hours": 3.67,
  "awake_hours": 0.85,
  "time_in_bed_hours": 7.65,
  "efficiency_percent": 89,
  "latency_minutes": 5.2,
  "average_hrv_ms": 15,
  "average_heart_rate_bpm": 58,
  "lowest_heart_rate_bpm": 52,
  "average_breath_rate": 14.5,
  "restless_periods": 3,
  "type": "long_sleep"
}
```

### Readiness Record

```json
{
  "date": "2026-01-20",
  "id": "def456",
  "score": 73,
  "temperature_deviation_c": -1.26,
  "temperature_trend_deviation_c": null,
  "activity_balance": 65,
  "body_temperature": 68,
  "hrv_balance": 81,
  "previous_day_activity": 72,
  "previous_night": 81,
  "recovery_index": 36,
  "resting_heart_rate": 82,
  "sleep_balance": 79,
  "sleep_regularity": 83,
  "timestamp": "2026-01-20T07:30:00.000-08:00"
}
```

### Activity Record

```json
{
  "date": "2026-01-20",
  "id": "ghi789",
  "score": 91,
  "steps": 302,
  "active_calories": 28,
  "total_calories": 1816,
  "target_calories": 350,
  "high_activity_hours": 0.0,
  "medium_activity_hours": 0.0,
  "low_activity_hours": 0.55,
  "sedentary_hours": 10.2,
  "resting_hours": 8.5,
  "non_wear_hours": 4.75,
  "average_met_minutes": 1.2,
  "high_activity_met_minutes": 0,
  "medium_activity_met_minutes": 0,
  "low_activity_met_minutes": 120,
  "sedentary_met_minutes": 612,
  "equivalent_walking_distance_m": 2145,
  "target_meters": 8000,
  "meters_to_target": -5855,
  "inactivity_alerts": 0,
  "timestamp": "2026-01-20T23:59:00.000-08:00"
}
```

### Night Record (Unified)

```json
{
  "date": "2026-01-20",
  "sleep": { ... },
  "readiness": { ... },
  "activity": { ... }
}
```

## Migration Notes

### For existing code

1. **Import the schema module:**
   ```python
   from scripts.schema import normalize_sleep, SleepRecord
   ```

2. **Convert raw API data:**
   ```python
   raw_sleep = client.get_sleep(start, end)
   normalized = [normalize_sleep(record) for record in raw_sleep]
   ```

3. **Access with explicit units:**
   ```python
   # Old (ambiguous)
   duration = record['total_sleep_duration']  # seconds? hours? who knows?
   
   # New (explicit)
   duration_hours = record.total_sleep_hours  # clearly hours
   ```

### Benefits

- **No unit confusion** - Field names tell you the unit
- **Type safety** - IDE autocomplete + type checking
- **Consistent analysis** - All code uses same structure
- **Future-proof** - Schema changes happen in one place

## See Also

- [schemas.md](./schemas.md) - API response schemas (output formats)
- [SECURITY.md](../SECURITY.md) - Data storage and privacy
- [Oura API Documentation](https://cloud.ouraring.com/v2/docs) - Official API reference
