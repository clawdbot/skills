---
name: flights
description: Track flight status, delays, and search routes. Uses FlightAware data.
homepage: https://flightaware.com
metadata: {"clawdis":{"emoji":"✈️","requires":{"bins":[],"env":[]}}}
---

# Flights Skill

Track flight status, search routes, and monitor delays using FlightAware data.

## Quick Commands

```bash
cd skills/flights

# Search flights by route
uv run python scripts/flights.py search PVD ORF --airline MX

# Get specific flight status
uv run python scripts/flights.py status MXY704
```

## Usage Examples

**Search for Breeze flights PVD → ORF:**
```bash
flights.py search PVD ORF --airline MX
```

**Check specific flight:**
```bash
flights.py status AA100
flights.py status MXY704 --date 2026-01-08
```

## Output Format

```json
{
  "flight": "MXY704",
  "airline": "Breeze Airways",
  "origin": "PVD",
  "destination": "ORF",
  "departure": "Thu 05:04PM EST",
  "arrival": "06:41PM EST",
  "status": "Scheduled / Delayed",
  "aircraft": "BCS3"
}
```

## Status Values

- `Scheduled` - Flight on time
- `Scheduled / Delayed` - Delay expected
- `En Route / On Time` - In the air, on time
- `En Route / Delayed` - In the air, running late
- `Arrived / Gate Arrival` - Landed and at gate
- `Cancelled` - Flight cancelled

## Airline Codes

| Code | Airline |
|------|---------|
| MX/MXY | Breeze Airways |
| AA | American |
| DL | Delta |
| UA | United |
| WN | Southwest |
| B6 | JetBlue |

## Optional: AviationStack API

For more detailed data, set `AVIATIONSTACK_API_KEY` (free tier available at aviationstack.com).

## Dependencies

```bash
cd skills/flights && uv sync
```
