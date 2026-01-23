#!/usr/bin/env python3
"""
Oura Weekly Report Generator

Generates automated weekly health reports and can send to Telegram.
"""

import argparse
import os
import sys
import json
import urllib.request
import urllib.error
from datetime import datetime, timedelta
from pathlib import Path

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from oura_api import OuraClient


def seconds_to_hours(seconds):
    return round(seconds / 3600, 1) if seconds else None


def calculate_sleep_score(day):
    efficiency = day.get("efficiency", 0)
    duration_hours = seconds_to_hours(day.get("total_sleep_duration", 0)) or 0
    eff_score = min(efficiency, 100)
    dur_score = min(duration_hours / 8 * 100, 100)
    return round((eff_score * 0.6) + (dur_score * 0.4), 1)


def analyze_week(sleep_data, readiness_data=None):
    """Analyze weekly data

    Args:
        sleep_data: List of sleep records from get_sleep()
        readiness_data: List of readiness records from get_readiness() (optional for backwards compatibility)
    """
    if not sleep_data:
        return None

    # Calculate scores - handle case where efficiency may not be in sleep endpoint
    scores = []
    for d in sleep_data:
        score = calculate_sleep_score(d)
        if score is None or score == 0:
            # Calculate from duration only when efficiency missing
            duration_sec = d.get("total_sleep_duration", 0)
            duration_hours = duration_sec / 3600 if duration_sec else 0
            dur_score = min(duration_hours / 8 * 100, 100)
            score = round(dur_score, 1)
        scores.append(score)

    # Get efficiency from sleep data (may be 0 if not in /sleep endpoint)
    efficiencies = [d.get("efficiency", 0) for d in sleep_data]
    avg_efficiency = round(sum(efficiencies) / len(efficiencies), 1) if efficiencies and any(efficiencies) else None

    durations = [seconds_to_hours(d.get("total_sleep_duration", 0)) for d in sleep_data]

    # Build readiness lookup by day from dedicated dataset
    readiness_by_day = {}
    if readiness_data:
        readiness_by_day = {r.get("day"): r for r in readiness_data}

    readiness_scores = []
    for d in sleep_data:
        day = d.get("day")
        if day in readiness_by_day:
            r = readiness_by_day[day].get("score")
            if r:
                readiness_scores.append(r)
        else:
            # Fallback: try nested readiness (old broken format, for backwards compat)
            r = d.get("readiness", {})
            if r and isinstance(r, dict) and r.get("score"):
                readiness_scores.append(r["score"])

    # Calculate trend (first half vs second half)
    half = len(scores) // 2
    if half >= 1:
        first_half_avg = sum(scores[:half]) / half
        second_half_avg = sum(scores[half:]) / (len(scores) - half)
        sleep_trend = round(second_half_avg - first_half_avg, 1)
    else:
        sleep_trend = 0

    if len(readiness_scores) >= 2:
        half = len(readiness_scores) // 2
        first_half_avg = sum(readiness_scores[:half]) / half
        second_half_avg = sum(readiness_scores[half:]) / (len(readiness_scores) - half)
        readiness_trend = round(second_half_avg - first_half_avg, 1)
    else:
        readiness_trend = 0

    # Get last 2 days individual data
    last_2_days = []
    for i, d in enumerate(sleep_data[-2:]):
        day = d.get("day")
        score = scores[-(2-i)] if len(scores) >= 2-i else scores[0]
        hours = seconds_to_hours(d.get("total_sleep_duration", 0))
        r_score = readiness_by_day.get(day, {}).get("score") if day in readiness_by_day else None
        last_2_days.append({
            "day": day,
            "sleep_score": score,
            "readiness": r_score,
            "hours": hours
        })

    return {
        "avg_sleep_score": round(sum(scores) / len(scores), 1) if scores else None,
        "avg_readiness": round(sum(readiness_scores) / len(readiness_scores), 1) if readiness_scores else None,
        "avg_efficiency": avg_efficiency,
        "avg_duration": round(sum(durations) / len(durations), 1) if durations else None,
        "sleep_trend": sleep_trend,
        "readiness_trend": readiness_trend,
        "best_day": sleep_data[scores.index(max(scores))].get("day") if sleep_data and scores else None,
        "worst_day": sleep_data[scores.index(min(scores))].get("day") if sleep_data and scores else None,
        "days_tracked": len(sleep_data),
        "last_2_days": last_2_days
    }


def format_telegram_message(week_data, period):
    """Format report for Telegram"""
    emoji = {
        "sleep": "😴",
        "readiness": "⚡",
        "efficiency": "📊",
        "duration": "⏰",
        "best": "🏆",
        "worst": "⚠️",
        "trend_up": "↗️",
        "trend_down": "↘️",
        "trend_same": "➡️"
    }

    # Trend indicators
    sleep_trend = week_data.get('sleep_trend', 0)
    readiness_trend = week_data.get('readiness_trend', 0)

    def trend_emoji(val):
        if val > 1:
            return emoji["trend_up"]
        elif val < -1:
            return emoji["trend_down"]
        return emoji["trend_same"]

    msg = f"📈 *Oura Weekly Report* ({period})\n\n"

    # Averages with trends
    msg += f"{emoji['sleep']} Sleep Score: *{week_data['avg_sleep_score']}*/100 {trend_emoji(sleep_trend)}"
    if sleep_trend != 0:
        msg += f" ({'+' if sleep_trend > 0 else ''}{sleep_trend})"
    msg += "\n"

    msg += f"{emoji['readiness']} Readiness: *{week_data['avg_readiness']}*/100 {trend_emoji(readiness_trend)}"
    if readiness_trend != 0:
        msg += f" ({'+' if readiness_trend > 0 else ''}{readiness_trend})"
    msg += "\n"

    msg += f"{emoji['efficiency']} Efficiency: *{week_data['avg_efficiency']}%*\n"
    msg += f"{emoji['duration']} Avg Sleep: *{week_data['avg_duration']}h*\n"

    # Last 2 days
    last_2_days = week_data.get('last_2_days', [])
    if last_2_days:
        msg += "\n📅 *Last 2 Days:*\n"
        for day_data in last_2_days:
            day = day_data.get('day', '')
            sleep = day_data.get('sleep_score', 'N/A')
            ready = day_data.get('readiness', 'N/A')
            hours = day_data.get('hours', 'N/A')
            ready_str = f"{ready}/100" if ready is not None else "N/A"
            msg += f"  {day}: 😴{sleep} ⚡{ready_str} ⏰{hours}h\n"

    msg += f"\n{emoji['best']} Best: {week_data['best_day']}\n"
    msg += f"{emoji['worst']} Worst: {week_data['worst_day']}\n"
    msg += f"\n_Tracked: {week_data['days_tracked']} days_"

    return msg


def send_telegram(message, chat_id=None, bot_token=None):
    """Send report to Telegram using urllib"""
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
    parser = argparse.ArgumentParser(description="Oura Weekly Report")
    parser.add_argument("--days", type=int, default=7, help="Report period")
    parser.add_argument("--telegram", action="store_true", help="Send to Telegram")
    parser.add_argument("--token", help="Oura API token")
    
    args = parser.parse_args()
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
    period = f"{start_date} → {end_date}"
    
    try:
        client = OuraClient(args.token)
        sleep = client.get_sleep(start_date, end_date)
        readiness = client.get_readiness(start_date, end_date)
        week_data = analyze_week(sleep, readiness)
        
        if not week_data:
            print("No data available")
            sys.exit(1)
        
        # Print nicely
        print(f"\n📊 Oura Weekly Report ({period})")
        sleep_trend = week_data.get('sleep_trend', 0)
        readiness_trend = week_data.get('readiness_trend', 0)

        def trend_symbol(v):
            return "↗️" if v > 0 else ("↘️" if v < 0 else "➡️")

        print(f"   Sleep Score: {week_data['avg_sleep_score']} {trend_symbol(sleep_trend)} ({'+' if sleep_trend > 0 else ''}{sleep_trend})")
        print(f"   Readiness: {week_data['avg_readiness']} {trend_symbol(readiness_trend)} ({'+' if readiness_trend > 0 else ''}{readiness_trend})")
        print(f"   Efficiency: {week_data['avg_efficiency']}%")
        print(f"   Avg Duration: {week_data['avg_duration']}h")

        # Last 2 days
        last_2 = week_data.get('last_2_days', [])
        if last_2:
            print("\n   📅 Last 2 Days:")
            for d in last_2:
                ready = d.get('readiness')
                print(f"      {d['day']}: 😴{d['sleep_score']} ⚡{ready}/100 ⏰{d['hours']}h")

        print(f"\n   Best: {week_data['best_day']} | Worst: {week_data['worst_day']}")
        print(f"   Tracked: {week_data['days_tracked']} days")
        
        # Send to Telegram
        if args.telegram:
            msg = format_telegram_message(week_data, period)
            if send_telegram(msg):
                print("\n✅ Sent to Telegram!")
            else:
                print("\n❌ Telegram failed")
        
        # Save to file
        output_dir = os.environ.get("OURA_OUTPUT_DIR", str(Path.home() / ".oura-analytics" / "reports"))
        report_file = f"{output_dir}/oura_weekly_{end_date}.json"
        os.makedirs(output_dir, exist_ok=True)
        with open(report_file, "w") as f:
            json.dump({"period": period, "summary": week_data, "raw": sleep}, f, indent=2)
        print(f"\n💾 Saved to {report_file}")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
