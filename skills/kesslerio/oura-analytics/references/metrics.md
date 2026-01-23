# Oura Metrics Reference

## Core Scores

| Score | Range | Interpretation |
|-------|-------|----------------|
| Sleep Score | 0-100 | <50: Poor, 50-70: Fair, 70-85: Good, >85: Excellent |
| Readiness Score | 0-100 | <50: Recovery needed, 50-70: Moderate, 70-85: Good, >85: Optimal |
| Activity Score | 0-100 | Measures daily movement balance |

## Sleep Stages (in seconds)

| Stage | Typical Range | Notes |
|-------|--------------|-------|
| Deep | 3000-7200 | Critical for physical recovery |
| REM | 4500-8100 | Important for cognitive recovery |
| Light | 10800-21600 | Transition stage |
| Awake | <1800 | Minimal is ideal |

## HRV Metrics

| Metric | Healthy Range | Notes |
|--------|--------------|-------|
| RMSSD | 20-80 ms | Primary HRV metric |
| Balance | 40-60% | LF/HF ratio indicator |
| Low Frequency | - | Parasympathetic activity |
| High Frequency | - | Sympathetic activity |

## Temperature Deviation

- Normal: ±0.1°C
- Elevated: >0.2°C (possible illness/stress)
- Suppressed: < -0.2°C (recovery indication)

## Derived Metrics

```python
# Sleep Efficiency
sleep_efficiency = sleep_duration / (sleep_duration + awake_duration)

# Recovery Index
recovery_index = (readiness_score + sleep_score + hrv_score) / 3

# Balance Score
balance = (activity_score + readiness_score + sleep_score) / 3
```

## Optimal Ranges for Performance

| Metric | Optimal | Warning |
|--------|---------|---------|
| Sleep Score | >75 | <60 |
| Readiness Score | >75 | <60 |
| Deep Sleep % | >15% of total | <12% |
| REM Sleep % | >20% of total | <15% |
| HRV (RMSSD) | 40-80 ms | <30 or >100 |
| Temperature | ±0.1°C | >0.3°C deviation |
