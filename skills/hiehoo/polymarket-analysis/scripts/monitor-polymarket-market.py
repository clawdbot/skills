#!/usr/bin/env python3
"""
Polymarket Market Monitor
Fetches market data, compares to previous state, detects alerts.
Usage: python monitor-polymarket-market.py <market_url_or_id> [--threshold-price 0.05] [--threshold-whale 5000]
"""

import argparse
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.request import urlopen, Request
from urllib.error import URLError

SCRIPT_DIR = Path(__file__).parent
STATE_DIR = SCRIPT_DIR.parent / "state"
API_BASE = "https://gamma-api.polymarket.com"

# Default thresholds
DEFAULT_PRICE_THRESHOLD = 0.05  # 5% price change
DEFAULT_WHALE_THRESHOLD = 5000  # $5000 trade
DEFAULT_ARB_THRESHOLD = 0.98    # Pair cost < $0.98


def extract_slug_from_url(url: str) -> str | None:
    """Extract market slug from Polymarket URL."""
    # Pattern: polymarket.com/event/{event-slug}/{market-slug}
    match = re.search(r'polymarket\.com/event/[^/]+/([^/\?\#]+)', url)
    if match:
        return match.group(1)
    # Pattern: polymarket.com/event/{event-slug} (no specific market)
    match = re.search(r'polymarket\.com/event/([^/\?\#]+)', url)
    if match:
        return match.group(1)
    return None


def fetch_api(endpoint: str) -> dict | list | None:
    """Fetch data from Gamma API."""
    url = f"{API_BASE}{endpoint}"
    try:
        req = Request(url, headers={"User-Agent": "ClawdbotMonitor/1.0"})
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except (URLError, json.JSONDecodeError) as e:
        print(f"Error fetching {url}: {e}", file=sys.stderr)
        return None


def find_market_by_slug(slug: str) -> dict | None:
    """Search for market by slug."""
    # Try direct market lookup
    data = fetch_api(f"/markets?slug={slug}")
    if data and isinstance(data, list) and len(data) > 0:
        return data[0]

    # Try searching active markets
    data = fetch_api(f"/markets?active=true&closed=false&limit=100")
    if data and isinstance(data, list):
        for market in data:
            if slug in str(market.get("slug", "")) or slug in str(market.get("question", "")).lower():
                return market
    return None


def find_market_by_id(market_id: str) -> dict | None:
    """Fetch market by numeric ID."""
    return fetch_api(f"/markets/{market_id}")


def resolve_market(url_or_id: str) -> dict | None:
    """Resolve market from URL, slug, or ID."""
    # If it's a URL, extract slug
    if url_or_id.startswith("http"):
        slug = extract_slug_from_url(url_or_id)
        if slug:
            market = find_market_by_slug(slug)
            if market:
                return market

    # Try as numeric ID
    if url_or_id.isdigit():
        market = find_market_by_id(url_or_id)
        if market:
            return market

    # Try as slug directly
    market = find_market_by_slug(url_or_id)
    if market:
        return market

    return None


def load_state(market_id: str) -> dict:
    """Load previous state from file."""
    state_file = STATE_DIR / f"{market_id}.json"
    if state_file.exists():
        try:
            with open(state_file) as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            pass
    return {}


def save_state(market_id: str, state: dict):
    """Save current state to file."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    state_file = STATE_DIR / f"{market_id}.json"
    with open(state_file, "w") as f:
        json.dump(state, f, indent=2)


def detect_alerts(current: dict, previous: dict, thresholds: dict) -> list[dict]:
    """Compare current vs previous state, return alerts."""
    alerts = []
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    yes_price = current.get("yes_price", 0)
    no_price = current.get("no_price", 0)
    volume = current.get("volume", 0)

    prev_yes = previous.get("yes_price", yes_price)
    prev_no = previous.get("no_price", no_price)
    prev_volume = previous.get("volume", volume)

    # Price change alert
    if prev_yes > 0:
        yes_change = abs(yes_price - prev_yes) / prev_yes
        if yes_change >= thresholds["price"]:
            direction = "up" if yes_price > prev_yes else "down"
            alerts.append({
                "type": "price_change",
                "timestamp": now,
                "message": f"YES price moved {direction} {yes_change:.1%}: ${prev_yes:.3f} → ${yes_price:.3f}"
            })

    if prev_no > 0:
        no_change = abs(no_price - prev_no) / prev_no
        if no_change >= thresholds["price"]:
            direction = "up" if no_price > prev_no else "down"
            alerts.append({
                "type": "price_change",
                "timestamp": now,
                "message": f"NO price moved {direction} {no_change:.1%}: ${prev_no:.3f} → ${no_price:.3f}"
            })

    # Whale trade alert (volume spike)
    volume_delta = volume - prev_volume
    if volume_delta >= thresholds["whale"]:
        alerts.append({
            "type": "whale_trade",
            "timestamp": now,
            "message": f"Large volume detected: +${volume_delta:,.0f} (${prev_volume:,.0f} → ${volume:,.0f})"
        })

    # Arbitrage opportunity
    pair_cost = yes_price + no_price
    if pair_cost < thresholds["arb"] and pair_cost > 0:
        profit_pct = (1 - pair_cost) * 100
        alerts.append({
            "type": "arbitrage",
            "timestamp": now,
            "message": f"Pair cost ${pair_cost:.4f} < ${thresholds['arb']:.2f} - potential {profit_pct:.2f}% arb"
        })

    return alerts


def main():
    parser = argparse.ArgumentParser(description="Monitor Polymarket market")
    parser.add_argument("market", help="Market URL, slug, or numeric ID")
    parser.add_argument("--threshold-price", type=float, default=DEFAULT_PRICE_THRESHOLD,
                        help=f"Price change threshold (default: {DEFAULT_PRICE_THRESHOLD})")
    parser.add_argument("--threshold-whale", type=float, default=DEFAULT_WHALE_THRESHOLD,
                        help=f"Whale trade threshold in USD (default: {DEFAULT_WHALE_THRESHOLD})")
    parser.add_argument("--threshold-arb", type=float, default=DEFAULT_ARB_THRESHOLD,
                        help=f"Arbitrage pair cost threshold (default: {DEFAULT_ARB_THRESHOLD})")
    parser.add_argument("--json", action="store_true", help="Output as JSON")
    args = parser.parse_args()

    # Resolve market
    data = resolve_market(args.market)
    if not data:
        print(f"Error: Could not find market: {args.market}", file=sys.stderr)
        sys.exit(1)

    market_id = str(data.get("id", data.get("conditionId", "unknown")))

    # Parse prices
    prices = data.get("outcomePrices", [])
    if isinstance(prices, str):
        prices = json.loads(prices) if prices.startswith("[") else []
    yes_price = float(prices[0]) if len(prices) > 0 else 0
    no_price = float(prices[1]) if len(prices) > 1 else 0

    current = {
        "market_id": market_id,
        "name": data.get("question", "Unknown"),
        "slug": data.get("slug", ""),
        "yes_price": yes_price,
        "no_price": no_price,
        "pair_cost": yes_price + no_price,
        "volume": float(data.get("volume", 0) or 0),
        "liquidity": float(data.get("liquidity", 0) or 0),
        "end_date": data.get("endDate", ""),
        "last_check": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    }

    # Load previous state
    previous = load_state(market_id)

    # Detect alerts
    thresholds = {
        "price": args.threshold_price,
        "whale": args.threshold_whale,
        "arb": args.threshold_arb
    }
    alerts = detect_alerts(current, previous, thresholds)

    # Save new state
    save_state(market_id, current)

    # Output
    result = {
        "market": current,
        "alerts": alerts,
        "previous": previous if previous else None
    }

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"## Market: {current['name']}")
        print(f"**ID:** {market_id}")
        print(f"**Prices:** YES ${yes_price:.3f} | NO ${no_price:.3f} | Pair: ${current['pair_cost']:.3f}")
        print(f"**Volume:** ${current['volume']:,.0f} | **Liquidity:** ${current['liquidity']:,.0f}")
        if current['end_date']:
            print(f"**Ends:** {current['end_date']}")
        print()
        if alerts:
            print("### Alerts")
            for alert in alerts:
                print(f"- [{alert['type'].upper()}] {alert['message']}")
        else:
            print("No alerts triggered.")

    # Exit with alert count for cron to detect
    sys.exit(0 if not alerts else len(alerts))


if __name__ == "__main__":
    main()
