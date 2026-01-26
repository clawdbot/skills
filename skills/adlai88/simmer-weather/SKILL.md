---
name: simmer-weather
description: Trade Polymarket weather markets using NOAA forecasts via Simmer API. Inspired by gopfan2's $2M+ strategy.
metadata: {"clawdbot":{"emoji":"🌡️","requires":{"env":["SIMMER_API_KEY"]},"cron":"0 */2 * * *"}}
authors:
  - Simmer (@simmer_markets)
attribution: "Strategy inspired by gopfan2"
---

# Simmer Weather Trading

Trade temperature markets on Polymarket using NOAA forecast data.

## When to Use This Skill

Use this skill when the user wants to:
- Trade weather markets automatically
- Set up gopfan2-style temperature trading
- Buy low on weather predictions
- Check their weather trading positions
- Configure trading thresholds or locations

## Setup Flow

When user asks to install or configure this skill:

1. **Ask for Simmer API key**
   - They can get it from simmer.markets/dashboard → SDK tab
   - Store in environment as `SIMMER_API_KEY`

2. **Ask about settings** (or confirm defaults)
   - Entry threshold: When to buy (default 15¢)
   - Exit threshold: When to sell (default 45¢)
   - Max position: Amount per trade (default $2.00)
   - Locations: Which cities to trade (default NYC)

3. **Save settings to environment variables**
   - `SIMMER_WEATHER_ENTRY` - entry threshold (e.g., "0.15" for 15¢)
   - `SIMMER_WEATHER_EXIT` - exit threshold (e.g., "0.45" for 45¢)
   - `SIMMER_WEATHER_MAX_POSITION` - max per trade (e.g., "2.00")
   - `SIMMER_WEATHER_LOCATIONS` - comma-separated cities (e.g., "NYC,Chicago")

4. **Set up cron**
   - Runs every 2 hours by default
   - User can request different frequency

## Configuration

All settings can be customized via environment variables:

| Setting | Environment Variable | Default | Description |
|---------|---------------------|---------|-------------|
| Entry threshold | `SIMMER_WEATHER_ENTRY` | 0.15 | Buy when price below this (0.15 = 15¢) |
| Exit threshold | `SIMMER_WEATHER_EXIT` | 0.45 | Sell when price above this (0.45 = 45¢) |
| Max position | `SIMMER_WEATHER_MAX_POSITION` | 2.00 | Maximum USD per trade |
| Locations | `SIMMER_WEATHER_LOCATIONS` | NYC | Comma-separated: NYC,Chicago,Miami,Seattle,Dallas,Atlanta |

**Supported locations:**
- NYC (New York - LaGuardia)
- Chicago (O'Hare)
- Seattle (Sea-Tac)
- Atlanta (Hartsfield)
- Dallas (DFW)
- Miami (MIA)

To view current config, run:
```bash
python weather_trader.py --config
```

## How It Works

Each cycle the script:
1. Fetches active weather markets from Simmer API (tagged with "weather")
2. Groups markets by event (each temperature day is one event with multiple buckets)
3. Parses event names to get location and date
4. Fetches NOAA forecast for that location/date
5. Finds the temperature bucket that matches the forecast
6. **Entry:** If bucket price < entry threshold → executes BUY via Simmer SDK
7. **Exit:** Checks open positions, sells if price > exit threshold
8. Reports results back to user

## Running the Skill

**Run a scan:**
```bash
python weather_trader.py
```

**Dry run (no actual trades):**
```bash
python weather_trader.py --dry-run
```

**Check positions only:**
```bash
python weather_trader.py --positions
```

**View current config:**
```bash
python weather_trader.py --config
```

## Reporting Results

After each run, message the user with:
- Current configuration
- Number of weather markets found
- NOAA forecast for each location
- Entry opportunities (and trades executed)
- Exit opportunities (and sells executed)
- Current positions

Example output to share:
```
🌤️ Weather Trading Scan Complete

Configuration: Entry <15¢, Exit >45¢, Max $2.00, Locations: NYC

Found 12 active weather markets across 4 events

NYC Jan 28: NOAA forecasts 34°F (high)
→ Bucket "34-35°F" trading at $0.12
→ Below 15¢ threshold - BUY opportunity!
→ Executed: Bought 16.6 shares @ $0.12 ($2.00)

Checked 2 open positions:
→ NYC Jan 27 "32-33°F" @ $0.52 - SELL opportunity!
→ Executed: Sold 15.0 shares @ $0.52

Summary: 1 buy, 1 sell executed
Next scan in 2 hours.
```

## Example Conversations

**User: "Set up weather trading"**
→ Walk through setup flow:
1. Ask for API key
2. Ask for entry threshold (suggest 15¢ as default)
3. Ask for exit threshold (suggest 45¢ as default)
4. Ask for max position size (suggest $2)
5. Ask which locations (NYC default, can add more)
6. Save settings and set up cron

**User: "Run my weather skill"**
→ Execute the script immediately and report results

**User: "How are my weather trades doing?"**
→ Run script with --positions flag and summarize

**User: "Make it more aggressive"**
→ Explain current thresholds and offer options:
- Increase entry threshold to 20¢ (more opportunities)
- Increase max position to $5 (bigger trades)
→ Update the relevant environment variable

**User: "Add Chicago to my weather trading"**
→ Update SIMMER_WEATHER_LOCATIONS to include Chicago
→ Example: "NYC,Chicago"

**User: "What are my current settings?"**
→ Run script with --config flag and show settings

**User: "Change my exit threshold to 50 cents"**
→ Update SIMMER_WEATHER_EXIT to "0.50"

## Troubleshooting

**"No weather markets found"**
- Weather markets may not be active (seasonal)
- Check simmer.markets to see if weather markets exist

**"API key invalid"**
- Verify SIMMER_API_KEY environment variable is set
- Get a new key from simmer.markets/dashboard → SDK tab

**"NOAA request failed"**
- NOAA API may be rate-limited, wait a few minutes
- Check if weather.gov is accessible

**"Max position too small for 5 shares"**
- Polymarket requires minimum 5 shares per order
- Increase SIMMER_WEATHER_MAX_POSITION or wait for lower prices

**"Price below min tick"**
- Market is at an extreme (near 0% or 100%)
- These are skipped automatically to avoid issues
