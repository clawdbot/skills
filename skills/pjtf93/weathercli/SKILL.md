---
name: weathercli
description: Get current weather conditions and forecasts for any location worldwide. Returns structured data with temperature, humidity, wind, precipitation, and more. No API key required.
---

# Weather CLI

Use the `weathercli` command to retrieve weather information for any location worldwide.

## Commands

### Current Weather
Get real-time weather conditions including temperature, humidity, wind, and precipitation.

```bash
weathercli current "<location>"
weathercli current "<location>" --json
```

**Returns:** Current temperature, "feels like" temperature, humidity %, wind speed/direction, pressure, cloud cover, UV index, precipitation, weather condition description, and timestamp in local timezone.

### Forecast
Get daily or hourly weather forecasts.

```bash
# Daily forecast (default: 7 days, max: 16)
weathercli forecast "<location>" --days <N>

# Hourly forecast (max: 384 hours)
weathercli forecast "<location>" --hourly --hours <N>

# JSON output for parsing
weathercli forecast "<location>" --json
```

**Returns:** For each day/hour: temperature (high/low or current), weather condition, precipitation probability and amount, wind speed/direction, UV index, sunrise/sunset times (daily only).

### Location Search
Find coordinates and timezone information for a location.

```bash
weathercli search "<location>"
weathercli search "<location>" --json
```

**Returns:** Location name, coordinates (lat/lon), country, region/state, timezone.

## Location Format

Locations are flexible and geocoded automatically:
- City names: `"London"`, `"Tokyo"`, `"New York"`
- City + country: `"Paris, France"`, `"Berlin, Germany"`
- City + state/region: `"Portland, Oregon"`, `"Barcelona, Catalonia"`
- Ambiguous names: Add country/region for precision

## Options

- `--json` - Output structured JSON (recommended for parsing)
- `--no-color` - Disable color output (for plain text parsing)
- `--days N` - Number of days for forecast (1-16, default: 7)
- `--hourly` - Show hourly instead of daily forecast
- `--hours N` - Number of hours for hourly forecast (1-384)
- `--verbose` - Show detailed request information

## Output Format

### Human-Readable (default)
Color-coded temperatures, formatted with emojis and units. Times shown in location's local timezone.

### JSON Structure

**Current weather:**
```json
{
  "location": {
    "name": "Tokyo",
    "latitude": 35.6895,
    "longitude": 139.6917,
    "country": "Japan",
    "timezone": "Asia/Tokyo"
  },
  "time": "2026-01-12T18:45:00+09:00",
  "temperature": 4.7,
  "apparent": 1.8,
  "humidity": 66,
  "wind_speed": 3.6,
  "wind_direction": 135,
  "condition": "Clear sky",
  "weather_code": 0,
  "precipitation": 0,
  "cloud_cover": 0,
  "pressure": 1015.2,
  "uv_index": 0
}
```

**Forecast:**
```json
{
  "location": { ... },
  "daily": [
    {
      "date": "2026-01-12",
      "temp_max": 12.1,
      "temp_min": 4.3,
      "condition": "Slight rain",
      "precip_prob": 75,
      "precipitation": 1.5,
      "sunrise": "2026-01-12T08:04:00+09:00",
      "sunset": "2026-01-12T16:45:00+09:00",
      "wind_speed_max": 15.3,
      "wind_direction": 202,
      "uv_index_max": 2.4
    }
  ]
}
```

## Usage Guidelines

### When to Use

- User asks for weather, temperature, forecast, or conditions
- Planning activities and need weather data
- Checking if it will rain, snow, or be sunny
- Getting climate information for travel planning
- Need sunrise/sunset times
- Comparing weather across locations

### Location Handling

1. If user provides clear location, use it directly
2. If ambiguous (e.g., "Portland"), ask for clarification or add context
3. If location not found, suggest checking spelling or adding country
4. For coordinates, use `search` command first to validate

### Parsing Output

- **Always use `--json`** for programmatic parsing
- Extract `temperature`, `condition`, `wind_speed` for quick summaries
- Check `precip_prob` for rain likelihood
- Use `sunrise`/`sunset` for daylight planning
- `weather_code` follows WMO standard (0-99)

### Best Practices

- Request 3-5 days for travel planning (not full 16)
- Use hourly forecast for detailed day planning
- Check `apparent` temperature for "feels like" comfort
- UV index >3 = recommend sun protection
- Wind speed >20 km/h = mention it's windy

## Examples

**Quick weather check:**
```bash
weathercli current "London" --json | jq '.temperature, .condition'
```

**Week forecast for trip:**
```bash
weathercli forecast "Barcelona" --days 5 --json
```

**Detailed today's hourly:**
```bash
weathercli forecast "Seattle" --hourly --hours 24
```

**Check multiple cities:**
```bash
for city in "Tokyo" "London" "New York"; do
  weathercli current "$city" --json | jq -r '"\(.location.name): \(.temperature)°C, \(.condition)"'
done
```

**Find exact location:**
```bash
weathercli search "Springfield" --json
```

## Notes

- **No API key required** - Uses free Open-Meteo API
- **Worldwide coverage** - Works for any location globally
- **Temperatures in Celsius** - Convert if needed (°F = °C × 9/5 + 32)
- **Wind speed in km/h** - Convert to mph if needed (×0.621)
- **Local timezone** - All times automatically converted
- **Rate limits** - Reasonable for personal/agent use; avoid hammering
- **Accuracy** - Data from multiple meteorological sources
- **Updates** - Current weather updates every 15 minutes
- **Offline** - Requires internet connection

## Error Handling

**Location not found:**
```
Error: location not found: Atlantis
```
→ Check spelling, try adding country/region

**Network error:**
```
Error: weather API error: network timeout
```
→ Retry after brief delay

**Invalid input:**
```
Error: invalid days value
```
→ Check `--days` is between 1-16

## Installation

If `weathercli` is not available:
```bash
# Via Go
go install github.com/pjtf93/weathercli/cmd/weathercli@latest

# Or download binary from releases
# https://github.com/pjtf93/weathercli/releases
```
