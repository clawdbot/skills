# Oura Cloud API Reference

## Authentication

Get your Personal Access Token at: https://cloud.ouraring.com/personal-access-token

```python
import requests

headers = {"Authorization": "Bearer YOUR_API_TOKEN"}
```

## Endpoints

### Daily Sleep
`GET /v2/usercollection/sleep`

Returns sleep summary including:
- `score` - Overall sleep score (0-100)
- `deep_sleep_duration` - Deep sleep in seconds
- `light_sleep_duration` - Light sleep in seconds
- `rem_sleep_duration` - REM sleep in seconds
- `awake_duration` - Time awake in seconds
- `sleep_duration` - Total sleep in seconds

### Daily Readiness
`GET /v2/usercollection/readiness`

Returns readiness scores including:
- `score` - Overall readiness score (0-100)
- `score_recovery_index` - Recovery metric
- `score_sleep_balance` - Sleep balance metric
- `score_temperature` - Temperature deviation indicator

### Daily Activity
`GET /v2/usercollection/activity`

Returns activity metrics including:
- `score` - Activity score (0-100)
- `steps` - Total steps
- `calories` - Calories burned
- `met_minutes` - MET minutes

### Heart Rate Variability
`GET /v2/usercollection/hrv`

Returns HRV metrics:
- `average` - Average HRV (ms)
- `low_frequency` - LF component
- `high_frequency` - HF component

### Sleep Time Series (Optional)
`GET /v2/usercollection/sleep_time_series`

Minute-by-minute data for detailed analysis.

## Rate Limits

- 1000 requests/hour
- 10000 requests/day

## Example Response

```json
{
  "sleep": [{
    "score": 85,
    "deep_sleep_duration": 5400,
    "light_sleep_duration": 18000,
    "rem_sleep_duration": 7200,
    "awake_duration": 1800,
    "sleep_duration": 30600,
    "hrv": 65,
    "respiratory_rate": 14.2,
    "temperature_deviation": 0.12
  }]
}
```
