#!/usr/bin/env python3
"""
Oura Alerts - Readiness & Sleep Alerts

Sends Telegram notifications when metrics drop below thresholds.
Uses debounce, hysteresis, and configurable thresholds.
"""

import os
import sys
import json
import argparse
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from oura_api import OuraClient
from config import AlertState, ConfigLoader, check_thresholds_with_quality


def seconds_to_hours(seconds):
    return round(seconds / 3600, 1) if seconds else None


def check_thresholds_legacy(sleep_data, readiness_data, thresholds):
    """Legacy threshold checking (simple, no debounce)."""
    readiness_by_day = {r.get("day"): r for r in readiness_data}

    alerts = []

    for day in sleep_data:
        date = day.get("day")
        readiness_record = readiness_by_day.get(date)
        readiness_score = readiness_record.get("score") if readiness_record else None

        efficiency = day.get("efficiency", 100)
        duration_sec = day.get("total_sleep_duration", 0)
        duration_hours = seconds_to_hours(duration_sec)

        day_alerts = []

        if readiness_score is not None and readiness_score < thresholds.get("readiness", 60):
            day_alerts.append(f"Readiness {readiness_score}")

        if efficiency < thresholds.get("efficiency", 80):
            day_alerts.append(f"Efficiency {efficiency}%")

        if duration_hours and duration_hours < thresholds.get("sleep_hours", 7):
            day_alerts.append(f"Sleep {duration_hours}h")

        if day_alerts:
            alerts.append({"date": date, "alerts": day_alerts})

    return alerts


# Keep the old name as an alias for backwards compatibility
def check_thresholds(sleep_data, readiness_data, thresholds):
    """Check all days against thresholds.

    Note: For debounce and hysteresis, use check_thresholds_with_quality() from config module.
    """
    return check_thresholds_legacy(sleep_data, readiness_data, thresholds)


def format_alert_message(alerts):
    """Format alerts for Telegram"""
    if not alerts:
        return None
    
    msg = "⚠️ *Oura Alerts*\n\n"
    
    for alert in alerts[-5:]:  # Last 5 alerts
        msg += f"📅 *{alert['date']}*\n"
        for a in alert["alerts"]:
            msg += f"   • {a}\n"
        msg += "\n"
    
    msg += f"_Total: {len(alerts)} alert days_"
    return msg


def send_telegram(message, chat_id=None, bot_token=None):
    """Send to Telegram using urllib"""
    chat_id = chat_id or os.environ.get("TELEGRAM_CHAT_ID")
    bot_token = bot_token or os.environ.get("TELEGRAM_BOT_TOKEN")

    if not chat_id or not bot_token:
        print("TELEGRAM_CHAT_ID or TELEGRAM_BOT_TOKEN not set")
        return False

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    # Keep chat_id as string to support both numeric IDs and @channel usernames
    data = json.dumps({"chat_id": chat_id, "text": message, "parse_mode": "Markdown"}).encode("utf-8")

    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status == 200
    except urllib.error.HTTPError:
        return False


def main():
    parser = argparse.ArgumentParser(description="Oura Alerts")
    parser.add_argument("--days", type=int, default=7, help="Check period")
    parser.add_argument("--readiness", type=int, default=60, help="Readiness threshold (legacy)")
    parser.add_argument("--efficiency", type=int, default=80, help="Efficiency threshold (legacy)")
    parser.add_argument("--sleep-hours", type=float, default=7, help="Sleep hours threshold (legacy)")
    parser.add_argument("--config", help="Path to config.yaml")
    parser.add_argument("--telegram", action="store_true", help="Send to Telegram")
    parser.add_argument("--token", help="Oura API token")

    args = parser.parse_args()

    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")

    try:
        client = OuraClient(args.token)
        sleep = client.get_sleep(start_date, end_date)
        readiness = client.get_readiness(start_date, end_date)

        # Use config file if specified, otherwise use CLI args
        if args.config:
            config_loader = ConfigLoader(Path(args.config))
            config = config_loader.load()
            state = AlertState()

            alerts = check_thresholds_with_quality(
                sleep, readiness, config, state
            )
        else:
            # Legacy mode: simple thresholds
            thresholds = {
                "readiness": args.readiness,
                "efficiency": args.efficiency,
                "sleep_hours": args.sleep_hours
            }
            alerts = check_thresholds_legacy(sleep, readiness, thresholds)

        if alerts:
            mode = "Quality Mode" if args.config else "Legacy Mode"
            print(f"\n⚠️  {mode}: {len(alerts)} Alert Days Found:\n")
            for alert in alerts:
                consecutive = alert.get("consecutive_days", "")
                if consecutive:
                    print(f"  {alert['date']} ({consecutive} bad days): {', '.join(alert['alerts'])}")
                else:
                    print(f"  {alert['date']}: {', '.join(alert['alerts'])}")

            if args.telegram:
                msg = format_alert_message(alerts)
                if msg and send_telegram(msg):
                    print("\n✅ Alerts sent to Telegram!")
                else:
                    print("\n❌ Telegram failed")
        else:
            mode = "Quality Mode" if args.config else "Legacy Mode"
            print(f"\n✅ {mode}: All metrics above thresholds!")

        # Save to file (portable path)
        output_dir = os.environ.get("OURA_OUTPUT_DIR", str(Path.home() / ".oura-analytics" / "reports"))
        alert_file = f"{output_dir}/oura_alerts_{end_date}.json"
        os.makedirs(output_dir, exist_ok=True)
        with open(alert_file, "w") as f:
            json.dump({"period": f"{start_date} to {end_date}", "alerts": alerts}, f, indent=2)
        print(f"\n💾 Saved to {alert_file}")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
