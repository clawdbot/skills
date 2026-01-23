# Oura Analytics - Clawdbot Skill

[![Clawdbot Community Skill](https://img.shields.io/badge/clawdbot-community%20skill-blue)](https://github.com/clawdbot/clawdbot)
[![ClawdHub Listed](https://img.shields.io/badge/clawdhub-listed-green)](https://clawdhub.com/skills/oura-analytics)

**Production-grade Oura Ring data integration for Clawdbot**  
Fetch sleep scores, readiness, activity, HRV, and trends from Oura Cloud API. Generate automated health reports and trigger-based alerts.

## Features

✅ **Oura Cloud API Integration** - Personal Access Token authentication  
✅ **Sleep Analytics** - Score, duration, efficiency, REM/deep stages  
✅ **Readiness Tracking** - Recovery score, HRV balance, temperature  
✅ **Activity Metrics** - Steps, calories, MET minutes  
✅ **Trend Analysis** - Moving averages, correlations, anomaly detection  
✅ **Automated Alerts** - Low readiness/sleep notifications via Telegram

## Why This Exists

Clawdbot needs access to Oura Ring health data for:
- Daily morning briefings ("How did I sleep?")
- Correlating recovery with productivity/calendar
- Automated alerts for low recovery days
- Weekly/monthly health trend reports

**This skill provides:**
- Simple Python API client for Oura Cloud API v2
- Trend analysis and correlation tools
- Threshold-based alerting system
- Report generation templates

## Installation

### 1. Get Oura Personal Access Token

1. Go to https://cloud.ouraring.com/personal-access-tokens
2. Create new token (select all scopes)
3. Copy token to secrets file:

```bash
echo 'OURA_API_TOKEN="your_token_here"' >> ~/.config/systemd/user/secrets.conf
```

### 2. Install the skill

```bash
git clone https://github.com/kesslerio/oura-analytics-clawdbot-skill.git ~/.clawdbot/skills/oura-analytics
pip install -r requirements.txt
```

### 3. Add to Clawdbot's TOOLS.md

```markdown
### oura-analytics
- Fetch Oura Ring metrics (sleep, readiness, activity, HRV)
- Generate health reports and correlations
- Set up automated alerts for low recovery
- Usage: `python ~/.clawdbot/skills/oura-analytics/scripts/oura_api.py sleep --days 7`
```

## Usage Examples

> Note: For Python imports, set `PYTHONPATH` to the `scripts/` folder:
>
> ```bash
> export PYTHONPATH="$(pwd)/scripts"
> ```

### Fetch Sleep Data

```bash
# Last 7 days
python scripts/oura_api.py sleep --days 7
```

### Get Readiness Summary

```bash
python scripts/oura_api.py readiness --days 7
```

### Generate Reports

```bash
# Weekly summary (last 7 days)
python scripts/weekly_report.py --days 7

# Monthly trends (last 30 days)
python scripts/weekly_report.py --days 30
```

### Trigger Alerts

```bash
# Check for low readiness and send Telegram notification
python scripts/alerts.py --days 7 --readiness 60 --efficiency 80 --telegram
```

### Generate Hybrid Morning Briefing

```bash
# Daily hybrid report (morning briefing + 7-day trends)
python scripts/oura_briefing.py --format hybrid
```

**Example hybrid output:**
```
🌅 *Morning Briefing — Jan 22*
────────────────────────
💤 *Sleep*: 6h 47m (↑75min vs avg) ⚠️
⚡ *Readiness*: 80 (stable) ✅
*Drivers*: recovery_index, body_temperature
*Recovery*: 🟡 YELLOW
*Rec*: Moderate day. Avoid heavy training.

*📊 7-Day Trends*
────────────────────────
*Sleep Score*: `89.5` ↓
*Readiness*: `77.1` ↑
• *7.3h* sleep • *89.7%* eff • *21ms* HRV

*Recent*: 01-20 → `87.4`/`73` • 01-21 → `90.4`/`80`
```

### Baseline & Comparison Analysis

```bash
# Compare last 7 days vs 30-day baseline
python scripts/baseline.py --current-days 7 --baseline-days 30

# View 90-day baseline statistics
python scripts/baseline.py --baseline-only --baseline-days 90

# JSON output for programmatic use
python scripts/baseline.py --json
```

**Example output:**
```
📈 Current vs Baseline (Last 7d vs 30d baseline)

   ↗️ Sleep Score: 89.5 (+10.6, z=0.53)
      Above baseline

   ➡️ Readiness: 77.1 (+1.0, z=0.15)
      Within baseline

   ↗️ Sleep Duration: 7.3 (+1.4, z=0.52)
      Above baseline

   ↗️ Efficiency: 89.7 (+6.8, z=0.52)
      Above baseline

✅ All metrics within or above baseline range
```

**Interpretation:**
- **z-score**: Standard deviations from baseline mean
  - `z > 1.5`: 🔥 Well above baseline
  - `0.5 < z < 1.5`: ↗️ Above baseline
  - `-0.5 < z < 0.5`: ➡️ Within baseline
  - `-1.5 < z < -0.5`: ↘️ Below baseline
  - `z < -1.5`: ⚠️ Well below baseline (needs attention)
- **Baseline range**: P25-P75 (middle 50% of your historical data)
- **Sample size**: Number of days used to calculate baseline

## Core Workflows

### 1. Morning Health Check

```python
from oura_api import OuraClient, OuraAnalyzer

client = OuraClient(token=os.getenv("OURA_API_TOKEN"))
sleep_data = client.get_sleep(start_date="2026-01-18", end_date="2026-01-18")
today = sleep_data[0] if sleep_data else {}

if today:
    print(f"Sleep Score: {today.get('score', 'N/A')}/100")
    print(f"Total Sleep: {today.get('total_sleep_duration', 0)/3600:.1f}h")
    print(f"REM: {today.get('rem_sleep_duration', 0)/3600:.1f}h")
    print(f"Deep: {today.get('deep_sleep_duration', 0)/3600:.1f}h")
```

### 2. Recovery Tracking

```python
readiness = client.get_readiness(start_date="2026-01-11", end_date="2026-01-18")
avg_readiness = sum(d.get('score', 0) for d in readiness) / len(readiness) if readiness else 0
print(f"7-day avg readiness: {avg_readiness:.0f}")
```

### 3. Trend Analysis

```python
from oura_api import OuraAnalyzer

analyzer = OuraAnalyzer(sleep_data, readiness_data)
avg_sleep = analyzer.average_metric(sleep_data, "score")
avg_readiness = analyzer.average_metric(readiness_data, "score")
print(f"Avg Sleep Score: {avg_sleep}")
print(f"Avg Readiness Score: {avg_readiness}")
```

## API Client Reference

### OuraClient

```python
client = OuraClient(token="your_token")

# Sleep data (date range required)
sleep = client.get_sleep(start_date="2026-01-01", end_date="2026-01-16")

# Readiness data
readiness = client.get_readiness(start_date="2026-01-01", end_date="2026-01-16")

# Activity data
activity = client.get_activity(start_date="2026-01-01", end_date="2026-01-16")

# HRV trends
hrv = client.get_hrv(start_date="2026-01-01", end_date="2026-01-16")
```

### OuraAnalyzer

```python
from oura_api import OuraClient, OuraAnalyzer

client = OuraClient(token="your_token")
sleep = client.get_sleep(start_date="2026-01-01", end_date="2026-01-16")
readiness = client.get_readiness(start_date="2026-01-01", end_date="2026-01-16")

analyzer = OuraAnalyzer(sleep_data=sleep, readiness_data=readiness)

# Average metrics
avg_sleep = analyzer.average_metric(sleep, "score")
avg_readiness = analyzer.average_metric(readiness, "score")

# Trend analysis
trend = analyzer.trend(sleep, "score", days=7)

# Summary
summary = analyzer.summary()
```

### OuraReporter

```python
from oura_api import OuraClient, OuraReporter

client = OuraClient(token="your_token")
reporter = OuraReporter(client)

# Generate weekly report
report = reporter.generate_report(report_type="weekly", days=7)
print(json.dumps(report, indent=2))
```

## Metrics Reference

| Metric | Description | Range |
|--------|-------------|-------|
| **Sleep Score** | Overall sleep quality | 0-100 |
| **Readiness Score** | Recovery readiness | 0-100 |
| **HRV Balance** | Heart rate variability | -3 to +3 |
| **Sleep Efficiency** | Time asleep / time in bed | 0-100% |
| **REM Sleep** | REM stage duration | hours |
| **Deep Sleep** | Deep stage duration | hours |
| **Temperature Deviation** | Body temp vs baseline | °C |

See `references/metrics.md` for full definitions.

## Architecture

- **`scripts/oura_api.py`** - Oura Cloud API v2 client with OuraAnalyzer and OuraReporter classes
- **`scripts/alerts.py`** - Threshold-based alerting CLI
- **`scripts/weekly_report.py`** - Weekly report generator
- **`scripts/data_manager.py`** - Data storage and privacy controls
- **`scripts/oura_data.py`** - Data management CLI
- **`scripts/schema.py`** - Canonical data structures with unit normalization
- **`references/`** - API docs, metric definitions

## Data Management & Privacy

### What Data is Stored

All data is stored locally in `~/.oura-analytics/`:

```
~/.oura-analytics/
├── cache/                  # Cached API responses (cleanup is manual)
│   ├── sleep/             # Sleep records by date (YYYY-MM-DD.json)
│   ├── daily_readiness/   # Readiness records
│   └── daily_activity/    # Activity records
├── events.jsonl           # User-logged events (optional)
├── config.yaml            # User preferences (optional)
└── alert_state.json       # Alert tracking (optional)
```

**No data is sent to third parties.** All Oura data stays on your local machine.

### View Storage Info

```bash
python scripts/oura_data.py info
```

Output:
```
Data directory: /home/user/.oura-analytics
Total size: 187.1 KB

Cache:
  Size: 187.1 KB
  Files: 21
  sleep: 7 files, 46.4 KB, 2026-01-14 to 2026-01-20
  daily_readiness: 7 files, 3.6 KB, 2026-01-14 to 2026-01-20
  daily_activity: 7 files, 137.2 KB, 2026-01-14 to 2026-01-20
```

### Export Data (Backup)

Export all local data to a single JSON file:

```bash
# Full backup
python scripts/oura_data.py export --output backup.json

# Compressed tarball
python scripts/oura_data.py export --output backup.tar.gz --format tar.gz

# Export events only
python scripts/oura_data.py export-events --output events.csv --format csv
```

### Clear Data (Privacy)

```bash
# Clear cache only (keeps events/config)
python scripts/oura_data.py clear-cache --confirm

# Clear specific endpoint
python scripts/oura_data.py clear-cache --endpoint sleep --confirm

# Clear events
python scripts/oura_data.py clear-events --confirm

# Clear ALL local data
python scripts/oura_data.py clear-all --confirm
```

**Important:** All clear commands require `--confirm` flag to prevent accidental deletion.

### Automatic Cleanup

Delete cached data older than 90 days:

```bash
# Default: 90 days
python scripts/oura_data.py cleanup

# Custom retention period
python scripts/oura_data.py cleanup --days 180
```

### GDPR Compliance

- ✅ **Data ownership:** You own your data (local storage only)
- ✅ **Data retention:** You control retention (manual cleanup)
- ✅ **No data sharing:** No third-party services
- ✅ **Right to deletion:** Clear data anytime with `clear-all`

**Note:** This skill is NOT HIPAA-compliant. Do not use for medical decision-making. Consult healthcare professionals for health concerns.

## Troubleshooting

### Authentication Failed

```bash
# Check token is set
echo $OURA_API_TOKEN

# Or use explicit token
python scripts/oura_api.py sleep --days 7 --token "your_token"
```

### No Data Returned

```bash
# Check date range (Oura data has ~24h delay)
python scripts/oura_api.py sleep --days 10

# Or fetch and inspect manually
python scripts/oura_api.py sleep --days 7 | python -m json.tool | head -50
```

## Credits

**Created for production Clawdbot health tracking**  
Developed by [@kesslerio](https://github.com/kesslerio) • Part of the [ClawdHub](https://clawdhub.com) ecosystem

**Powered by:**
- [Oura Ring](https://ouraring.com/) - Wearable health tracker
- [Oura Cloud API v2](https://cloud.ouraring.com/v2/docs) - Official API

## License

MIT
