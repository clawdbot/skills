# Simmer Weather Trading Skill

Trade Polymarket weather markets using NOAA forecasts. Inspired by [gopfan2's $2M+ weather trading strategy](https://twitter.com/gopfan2).

## How It Works

1. Fetches active weather markets from Simmer (tagged with "weather")
2. Gets NOAA forecasts for the relevant dates
3. Finds markets where the forecast matches a low-priced bucket
4. Buys when price < 15¢ (gopfan2's threshold)

## Setup

### 1. Install Clawdbot

Follow the [Clawdbot installation guide](https://docs.clawd.bot/getting-started).

### 2. Get Your Simmer API Key

1. Go to [simmer.markets/dashboard](https://simmer.markets/dashboard)
2. Click the **SDK** tab
3. Create an API key
4. Copy the key (starts with `sk_`)

### 3. Install This Skill

Copy this folder to your Clawdbot skills directory:

```bash
cp -r simmer-weather ~/.clawdbot/skills/
```

### 4. Set Your API Key

Add to your environment (e.g., `~/.bashrc` or `~/.zshrc`):

```bash
export SIMMER_API_KEY="sk_your_key_here"
```

Or tell Clawdbot to set it via chat.

## Usage

### Via Clawdbot Chat

```
You: Run my weather skill
Clawd: 🌤️ Running weather scan...
       [Results]

You: Check my weather positions
Clawd: [Shows current positions]
```

### Manual CLI

```bash
# Run trading scan
python ~/.clawdbot/skills/simmer-weather/weather_trader.py

# Dry run (show opportunities without trading)
python ~/.clawdbot/skills/simmer-weather/weather_trader.py --dry-run

# Show positions only
python ~/.clawdbot/skills/simmer-weather/weather_trader.py --positions
```

### Cron Schedule

The skill runs every 2 hours by default when configured in Clawdbot.

To set up manually:
```bash
# Add to crontab (crontab -e)
0 */2 * * * SIMMER_API_KEY="sk_your_key" python ~/.clawdbot/skills/simmer-weather/weather_trader.py >> ~/.clawdbot/logs/weather.log 2>&1
```

## Configuration

Edit `weather_trader.py` to customize:

```python
# Strategy parameters
ENTRY_THRESHOLD = 0.15  # Buy when price < 15¢
EXIT_THRESHOLD = 0.45   # Sell when price > 45¢
MAX_POSITION_USD = 2.00 # Max $2 per trade

# Locations to trade (minimal version)
ACTIVE_LOCATIONS = ["NYC"]  # Add "Chicago", "Miami", etc.
```

## Strategy Details

Based on gopfan2's approach:

- **Entry**: Buy YES when price < 15¢ AND NOAA forecast matches the bucket
- **Exit**: Sell when price > 45¢
- **Risk**: Max $2 per position to limit exposure

Weather markets on Polymarket resolve using official airport temperature readings (LaGuardia for NYC, O'Hare for Chicago, etc.). NOAA forecasts are generally accurate 1-3 days out.

## Troubleshooting

### "No weather markets found"
Weather markets are seasonal. Check [simmer.markets](https://simmer.markets) to see if any are active.

### "API key invalid"
Make sure `SIMMER_API_KEY` is set in your environment:
```bash
echo $SIMMER_API_KEY
```

### "NOAA request failed"
The NOAA API occasionally rate-limits or has outages. Wait a few minutes and try again.

### "Trade failed: Real trading not enabled"
You need to enable real trading in your Simmer dashboard:
1. Go to simmer.markets/dashboard → SDK tab
2. Enable "Real Trading"
3. Create and fund a Polymarket wallet

## Links

- [Simmer Markets](https://simmer.markets)
- [Clawdbot](https://clawd.bot)
- [gopfan2's Strategy](https://twitter.com/gopfan2)
- [NOAA Weather API](https://www.weather.gov/documentation/services-web-api)
