#!/usr/bin/env python3
"""
Simmer Weather Trading Skill

Trades Polymarket weather markets using NOAA forecasts.
Inspired by gopfan2's $2M+ weather trading strategy.

Usage:
    python weather_trader.py              # Run trading scan
    python weather_trader.py --dry-run    # Show opportunities without trading
    python weather_trader.py --positions  # Show current positions only

Requires:
    SIMMER_API_KEY environment variable (get from simmer.markets/dashboard)
"""

import os
import sys
import re
import json
import argparse
from datetime import datetime, timezone, timedelta
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode

# =============================================================================
# Configuration
# =============================================================================

SIMMER_API_BASE = "https://api.simmer.markets"
NOAA_API_BASE = "https://api.weather.gov"

# Polymarket constraints
MIN_SHARES_PER_ORDER = 5.0  # Polymarket requires minimum 5 shares
MIN_TICK_SIZE = 0.01        # Minimum tradeable price

# Strategy parameters - configurable via environment variables
# Users can set these via Clawdbot chat during setup
ENTRY_THRESHOLD = float(os.environ.get("SIMMER_WEATHER_ENTRY", "0.15"))
EXIT_THRESHOLD = float(os.environ.get("SIMMER_WEATHER_EXIT", "0.45"))
MAX_POSITION_USD = float(os.environ.get("SIMMER_WEATHER_MAX_POSITION", "2.00"))

# Supported locations (matching Polymarket resolution sources)
LOCATIONS = {
    "NYC": {"lat": 40.7769, "lon": -73.8740, "name": "New York City (LaGuardia)"},
    "Chicago": {"lat": 41.9742, "lon": -87.9073, "name": "Chicago (O'Hare)"},
    "Seattle": {"lat": 47.4502, "lon": -122.3088, "name": "Seattle (Sea-Tac)"},
    "Atlanta": {"lat": 33.6407, "lon": -84.4277, "name": "Atlanta (Hartsfield)"},
    "Dallas": {"lat": 32.8998, "lon": -97.0403, "name": "Dallas (DFW)"},
    "Miami": {"lat": 25.7959, "lon": -80.2870, "name": "Miami (MIA)"},
}

# Active locations - configurable via environment (comma-separated)
# Example: SIMMER_WEATHER_LOCATIONS="NYC,Chicago,Miami"
_locations_env = os.environ.get("SIMMER_WEATHER_LOCATIONS", "NYC")
ACTIVE_LOCATIONS = [loc.strip().upper() for loc in _locations_env.split(",") if loc.strip()]

# =============================================================================
# NOAA Weather API
# =============================================================================

def fetch_json(url, headers=None):
    """Fetch JSON from URL with error handling."""
    try:
        req = Request(url, headers=headers or {})
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        print(f"  HTTP Error {e.code}: {url}")
        return None
    except URLError as e:
        print(f"  URL Error: {e.reason}")
        return None
    except Exception as e:
        print(f"  Error fetching {url}: {e}")
        return None


def get_noaa_forecast(location: str) -> dict:
    """
    Get NOAA forecast for a location.

    Returns dict with date -> {"high": temp, "low": temp}
    """
    if location not in LOCATIONS:
        print(f"  Unknown location: {location}")
        return {}

    loc = LOCATIONS[location]
    headers = {
        "User-Agent": "SimmerWeatherSkill/1.0 (https://simmer.markets)",
        "Accept": "application/geo+json",
    }

    # Step 1: Get grid info for coordinates
    points_url = f"{NOAA_API_BASE}/points/{loc['lat']},{loc['lon']}"
    points_data = fetch_json(points_url, headers)

    if not points_data or "properties" not in points_data:
        print(f"  Failed to get NOAA grid for {location}")
        return {}

    forecast_url = points_data["properties"].get("forecast")
    if not forecast_url:
        print(f"  No forecast URL for {location}")
        return {}

    # Step 2: Get forecast
    forecast_data = fetch_json(forecast_url, headers)

    if not forecast_data or "properties" not in forecast_data:
        print(f"  Failed to get NOAA forecast for {location}")
        return {}

    # Parse periods into daily forecasts
    periods = forecast_data["properties"].get("periods", [])
    forecasts = {}

    for period in periods:
        start_time = period.get("startTime", "")
        if not start_time:
            continue

        date_str = start_time[:10]  # "2026-01-28"
        temp = period.get("temperature")
        is_daytime = period.get("isDaytime", True)

        if date_str not in forecasts:
            forecasts[date_str] = {"high": None, "low": None}

        if is_daytime:
            forecasts[date_str]["high"] = temp
        else:
            forecasts[date_str]["low"] = temp

    return forecasts


# =============================================================================
# Market Parsing
# =============================================================================

def parse_weather_event(event_name: str) -> dict:
    """
    Parse weather event name to extract location, date, metric.

    Example: "Highest temperature in NYC on January 19?"
    Returns: {"location": "NYC", "date": "2026-01-19", "metric": "high"}
    """
    if not event_name:
        return None

    event_lower = event_name.lower()

    # Detect metric
    if 'highest' in event_lower or 'high temp' in event_lower:
        metric = 'high'
    elif 'lowest' in event_lower or 'low temp' in event_lower:
        metric = 'low'
    else:
        metric = 'high'  # Default

    # Detect location
    location = None
    location_aliases = {
        'nyc': 'NYC', 'new york': 'NYC', 'laguardia': 'NYC', 'la guardia': 'NYC',
        'chicago': 'Chicago', "o'hare": 'Chicago', 'ohare': 'Chicago',
        'seattle': 'Seattle', 'sea-tac': 'Seattle',
        'atlanta': 'Atlanta', 'hartsfield': 'Atlanta',
        'dallas': 'Dallas', 'dfw': 'Dallas',
        'miami': 'Miami',
    }

    for alias, loc in location_aliases.items():
        if alias in event_lower:
            location = loc
            break

    if not location:
        return None

    # Parse date ("on January 19")
    month_day_match = re.search(r'on\s+([a-zA-Z]+)\s+(\d{1,2})', event_name, re.IGNORECASE)
    if not month_day_match:
        return None

    month_name = month_day_match.group(1).lower()
    day = int(month_day_match.group(2))

    month_map = {
        'january': 1, 'jan': 1, 'february': 2, 'feb': 2, 'march': 3, 'mar': 3,
        'april': 4, 'apr': 4, 'may': 5, 'june': 6, 'jun': 6, 'july': 7, 'jul': 7,
        'august': 8, 'aug': 8, 'september': 9, 'sep': 9, 'october': 10, 'oct': 10,
        'november': 11, 'nov': 11, 'december': 12, 'dec': 12,
    }

    month = month_map.get(month_name)
    if not month:
        return None

    # Determine year (current or next if date passed)
    now = datetime.now(timezone.utc)
    year = now.year
    try:
        target_date = datetime(year, month, day, tzinfo=timezone.utc)
        if target_date < now - timedelta(days=30):
            year += 1
        date_str = f"{year}-{month:02d}-{day:02d}"
    except ValueError:
        return None

    return {"location": location, "date": date_str, "metric": metric}


def parse_temperature_bucket(outcome_name: str) -> tuple:
    """
    Parse temperature bucket from outcome name.

    Examples:
        "32-33°F" → (32, 33)
        "25°F or below" → (-999, 25)
        "36°F or higher" → (36, 999)
    """
    if not outcome_name:
        return None

    # "X°F or below"
    below_match = re.search(r'(\d+)\s*°?[fF]?\s*(or below|or less)', outcome_name, re.IGNORECASE)
    if below_match:
        return (-999, int(below_match.group(1)))

    # "X°F or higher"
    above_match = re.search(r'(\d+)\s*°?[fF]?\s*(or higher|or above|or more)', outcome_name, re.IGNORECASE)
    if above_match:
        return (int(above_match.group(1)), 999)

    # "X-Y°F"
    range_match = re.search(r'(\d+)\s*[-–to]+\s*(\d+)', outcome_name)
    if range_match:
        low, high = int(range_match.group(1)), int(range_match.group(2))
        return (min(low, high), max(low, high))

    return None


# =============================================================================
# Simmer API
# =============================================================================

def get_api_key():
    """Get Simmer API key from environment."""
    key = os.environ.get("SIMMER_API_KEY")
    if not key:
        print("Error: SIMMER_API_KEY environment variable not set")
        print("Get your API key from: simmer.markets/dashboard → SDK tab")
        sys.exit(1)
    return key


def fetch_weather_markets():
    """Fetch weather-tagged markets from Simmer API."""
    url = f"{SIMMER_API_BASE}/api/markets?tags=weather&status=active&limit=100"
    data = fetch_json(url)

    if not data or "markets" not in data:
        print("  Failed to fetch markets from Simmer API")
        return []

    return data["markets"]


def execute_trade(api_key: str, market_id: str, side: str, amount: float) -> dict:
    """Execute a trade via Simmer SDK API."""
    url = f"{SIMMER_API_BASE}/api/sdk/trade"

    payload = json.dumps({
        "market_id": market_id,
        "side": side,
        "amount": amount,
        "venue": "polymarket"  # Real trading on Polymarket
    }).encode()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        req = Request(url, data=payload, headers=headers, method="POST")
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        error_body = e.read().decode() if e.fp else str(e)
        return {"success": False, "error": f"HTTP {e.code}: {error_body}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def execute_sell(api_key: str, market_id: str, shares: float) -> dict:
    """Execute a sell trade via Simmer SDK API."""
    url = f"{SIMMER_API_BASE}/api/sdk/trade"

    payload = json.dumps({
        "market_id": market_id,
        "side": "yes",
        "action": "sell",
        "shares": shares,
        "venue": "polymarket"
    }).encode()

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        req = Request(url, data=payload, headers=headers, method="POST")
        with urlopen(req, timeout=30) as response:
            return json.loads(response.read().decode())
    except HTTPError as e:
        error_body = e.read().decode() if e.fp else str(e)
        return {"success": False, "error": f"HTTP {e.code}: {error_body}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def get_positions(api_key: str) -> list:
    """Get current positions from Simmer SDK API."""
    url = f"{SIMMER_API_BASE}/api/sdk/positions"

    headers = {
        "Authorization": f"Bearer {api_key}",
    }

    try:
        req = Request(url, headers=headers)
        with urlopen(req, timeout=30) as response:
            data = json.loads(response.read().decode())
            return data.get("positions", [])
    except Exception as e:
        print(f"  Error fetching positions: {e}")
        return []


def check_exit_opportunities(api_key: str, dry_run: bool = False) -> tuple[int, int]:
    """
    Check open positions for exit opportunities.

    Returns: (exits_found, exits_executed)
    """
    positions = get_positions(api_key)

    if not positions:
        return 0, 0

    # Filter for weather positions (check if market has weather tag or name contains weather keywords)
    weather_positions = []
    for pos in positions:
        question = pos.get("question", "").lower()
        # Weather markets typically have temperature-related questions
        if any(kw in question for kw in ["temperature", "°f", "highest temp", "lowest temp"]):
            weather_positions.append(pos)

    if not weather_positions:
        return 0, 0

    print(f"\n📈 Checking {len(weather_positions)} weather positions for exit...")

    exits_found = 0
    exits_executed = 0

    for pos in weather_positions:
        market_id = pos.get("market_id")
        current_price = pos.get("current_price") or pos.get("price_yes") or 0
        shares = pos.get("shares_yes") or pos.get("shares") or 0
        question = pos.get("question", "Unknown")[:50]

        if shares < MIN_SHARES_PER_ORDER:
            continue  # Position too small to sell

        if current_price >= EXIT_THRESHOLD:
            exits_found += 1
            print(f"  📤 {question}...")
            print(f"     Price ${current_price:.2f} >= exit threshold ${EXIT_THRESHOLD:.2f}")

            if dry_run:
                print(f"     [DRY RUN] Would sell {shares:.1f} shares")
            else:
                print(f"     Selling {shares:.1f} shares...")
                result = execute_sell(api_key, market_id, shares)

                if result.get("success"):
                    exits_executed += 1
                    print(f"     ✅ Sold {shares:.1f} shares @ ${current_price:.2f}")
                else:
                    error = result.get("error", "Unknown error")
                    print(f"     ❌ Sell failed: {error}")
        else:
            print(f"  📊 {question}...")
            print(f"     Price ${current_price:.2f} < exit threshold ${EXIT_THRESHOLD:.2f} - hold")

    return exits_found, exits_executed


# =============================================================================
# Main Strategy Logic
# =============================================================================

def run_weather_strategy(dry_run: bool = False, positions_only: bool = False, show_config: bool = False):
    """Run the weather trading strategy."""
    print("🌤️  Simmer Weather Trading Skill")
    print("=" * 50)

    # Show current configuration
    print(f"\n⚙️  Configuration:")
    print(f"  Entry threshold: {ENTRY_THRESHOLD:.0%} (buy below this)")
    print(f"  Exit threshold:  {EXIT_THRESHOLD:.0%} (sell above this)")
    print(f"  Max position:    ${MAX_POSITION_USD:.2f}")
    print(f"  Locations:       {', '.join(ACTIVE_LOCATIONS)}")

    if show_config:
        print("\n  To change settings, set environment variables:")
        print("    SIMMER_WEATHER_ENTRY=0.20")
        print("    SIMMER_WEATHER_EXIT=0.50")
        print("    SIMMER_WEATHER_MAX_POSITION=5.00")
        print("    SIMMER_WEATHER_LOCATIONS=NYC,Chicago,Miami")
        return

    api_key = get_api_key()

    # Positions only mode
    if positions_only:
        print("\n📊 Current Positions:")
        positions = get_positions(api_key)
        if not positions:
            print("  No open positions")
        else:
            for pos in positions:
                print(f"  • {pos.get('question', 'Unknown')[:50]}...")
                print(f"    YES: {pos.get('shares_yes', 0):.1f} | NO: {pos.get('shares_no', 0):.1f} | P&L: ${pos.get('pnl', 0):.2f}")
        return

    # Fetch weather markets
    print("\n📡 Fetching weather markets...")
    markets = fetch_weather_markets()
    print(f"  Found {len(markets)} weather markets")

    if not markets:
        print("  No weather markets available")
        return

    # Group markets by event
    events = {}
    for market in markets:
        event_id = market.get("event_id") or market.get("event_name", "unknown")
        if event_id not in events:
            events[event_id] = []
        events[event_id].append(market)

    print(f"  Grouped into {len(events)} events")

    # Cache for NOAA forecasts
    forecast_cache = {}
    trades_executed = 0
    opportunities_found = 0

    # Process each event
    for event_id, event_markets in events.items():
        event_name = event_markets[0].get("event_name", "") if event_markets else ""
        event_info = parse_weather_event(event_name)

        if not event_info:
            continue

        location = event_info["location"]
        date_str = event_info["date"]
        metric = event_info["metric"]

        # Filter by active locations
        if location not in ACTIVE_LOCATIONS:
            continue

        print(f"\n📍 {location} {date_str} ({metric} temp)")

        # Get forecast (cached)
        if location not in forecast_cache:
            print(f"  Fetching NOAA forecast...")
            forecast_cache[location] = get_noaa_forecast(location)

        forecasts = forecast_cache[location]
        day_forecast = forecasts.get(date_str, {})
        forecast_temp = day_forecast.get(metric)

        if forecast_temp is None:
            print(f"  ⚠️  No forecast available for {date_str}")
            continue

        print(f"  NOAA forecast: {forecast_temp}°F")

        # Find matching bucket
        matching_market = None
        for market in event_markets:
            outcome_name = market.get("outcome_name", "")
            bucket = parse_temperature_bucket(outcome_name)

            if bucket and bucket[0] <= forecast_temp <= bucket[1]:
                matching_market = market
                matching_bucket = bucket
                break

        if not matching_market:
            print(f"  ⚠️  No bucket found for {forecast_temp}°F")
            continue

        outcome_name = matching_market.get("outcome_name", "")
        price = matching_market.get("external_price_yes") or 0.5
        market_id = matching_market.get("id")

        print(f"  Matching bucket: {outcome_name} @ ${price:.2f}")

        # Validation: Skip extreme prices (market at near-certain outcome)
        if price < MIN_TICK_SIZE:
            print(f"  ⏸️  Price ${price:.4f} below min tick ${MIN_TICK_SIZE} - skip (market at extreme)")
            continue
        if price > (1 - MIN_TICK_SIZE):
            print(f"  ⏸️  Price ${price:.4f} above max tradeable - skip (market at extreme)")
            continue

        # Check entry condition
        if price < ENTRY_THRESHOLD:
            # Validation: Check if we can buy at least MIN_SHARES_PER_ORDER shares
            min_cost_for_shares = MIN_SHARES_PER_ORDER * price
            if min_cost_for_shares > MAX_POSITION_USD:
                print(f"  ⚠️  Max position ${MAX_POSITION_USD:.2f} too small for {MIN_SHARES_PER_ORDER} shares at ${price:.2f} (need ${min_cost_for_shares:.2f})")
                continue

            opportunities_found += 1
            print(f"  ✅ Below threshold (${ENTRY_THRESHOLD:.2f}) - BUY opportunity!")

            if dry_run:
                print(f"  [DRY RUN] Would buy ${MAX_POSITION_USD:.2f} worth (~{MAX_POSITION_USD/price:.1f} shares)")
            else:
                print(f"  Executing trade...")
                result = execute_trade(api_key, market_id, "yes", MAX_POSITION_USD)

                if result.get("success"):
                    trades_executed += 1
                    shares = result.get("shares_bought") or result.get("shares") or 0
                    print(f"  ✅ Bought {shares:.1f} shares @ ${price:.2f}")
                else:
                    error = result.get("error", "Unknown error")
                    print(f"  ❌ Trade failed: {error}")
        else:
            print(f"  ⏸️  Price ${price:.2f} above threshold ${ENTRY_THRESHOLD:.2f} - skip")

    # Check exit conditions for open positions
    exits_found, exits_executed = check_exit_opportunities(api_key, dry_run)

    # Summary
    print("\n" + "=" * 50)
    print("📊 Summary:")
    print(f"  Events scanned: {len(events)}")
    print(f"  Entry opportunities: {opportunities_found}")
    print(f"  Exit opportunities:  {exits_found}")
    print(f"  Trades executed:     {trades_executed + exits_executed}")

    if dry_run:
        print("\n  [DRY RUN MODE - no real trades executed]")


# =============================================================================
# CLI Entry Point
# =============================================================================

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Simmer Weather Trading Skill")
    parser.add_argument("--dry-run", action="store_true", help="Show opportunities without trading")
    parser.add_argument("--positions", action="store_true", help="Show current positions only")
    parser.add_argument("--config", action="store_true", help="Show current config and how to change it")
    args = parser.parse_args()

    run_weather_strategy(dry_run=args.dry_run, positions_only=args.positions, show_config=args.config)
