#!/usr/bin/env python3
"""
Oura Morning Briefing CLI

Generate concise, actionable daily briefings.

Usage:
    python oura_briefing.py                    # Today's briefing
    python oura_briefing.py --date 2026-01-20  # Specific date
    python oura_briefing.py --verbose          # Detailed briefing
    python oura_briefing.py --format json      # JSON output
    python oura_briefing.py --format brief     # 3-line brief
"""

import argparse
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from oura_api import OuraClient
from schema import create_night_record
from briefing import BriefingFormatter, Baseline, format_brief_briefing, format_json_briefing, format_hybrid_briefing


def _seconds_to_hours(seconds):
    """Convert seconds to hours. Returns None only if seconds is None."""
    return round(seconds / 3600, 1) if seconds is not None else None


def _calculate_sleep_score(day):
    """Calculate sleep score from day record. Guards against null efficiency."""
    efficiency = day.get("efficiency") or 0  # Handle None/null values
    duration_hours = _seconds_to_hours(day.get("total_sleep_duration", 0)) or 0
    eff_score = min(efficiency, 100) if efficiency else 0
    dur_score = min(duration_hours / 8 * 100, 100)
    return round((eff_score * 0.6) + (dur_score * 0.4), 1)


def _analyze_week(sleep_data, readiness_data=None):
    """Analyze weekly data for hybrid briefing."""
    if not sleep_data:
        return None
    
    # Calculate sleep scores
    scores = []
    for d in sleep_data:
        score = _calculate_sleep_score(d)
        if score is None or score == 0:
            duration_sec = d.get("total_sleep_duration", 0)
            duration_hours = duration_sec / 3600 if duration_sec else 0
            dur_score = min(duration_hours / 8 * 100, 100)
            score = round(dur_score, 1)
        scores.append(score)
    
    # Get efficiency (handle None/null values)
    efficiencies = [d.get("efficiency") or 0 for d in sleep_data]
    avg_efficiency = round(sum(efficiencies) / len(efficiencies), 1) if efficiencies else None
    
    # Get durations
    durations = [_seconds_to_hours(d.get("total_sleep_duration", 0)) for d in sleep_data]
    
    # Build readiness lookup by day
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
    
    # Calculate trends (first half vs second half)
    sleep_trend = 0
    if len(scores) >= 2:
        half = len(scores) // 2
        if half >= 1:
            first_half_avg = sum(scores[:half]) / half
            second_half_avg = sum(scores[half:]) / (len(scores) - half)
            sleep_trend = round(second_half_avg - first_half_avg, 1)
    
    readiness_trend = 0
    if len(readiness_scores) >= 2:
        half = len(readiness_scores) // 2
        first_half_avg = sum(readiness_scores[:half]) / half
        second_half_avg = sum(readiness_scores[half:]) / (len(readiness_scores) - half)
        readiness_trend = round(second_half_avg - first_half_avg, 1)
    
    # Get last 2 days data
    last_2_days = []
    for i, d in enumerate(sleep_data[-2:]):
        day = d.get("day")
        score = scores[-(2-i)] if len(scores) >= 2-i else scores[0]
        hours = _seconds_to_hours(d.get("total_sleep_duration", 0))
        r_score = readiness_by_day.get(day, {}).get("score") if day in readiness_by_day else None
        last_2_days.append({
            "day": day,
            "sleep_score": score,
            "readiness": r_score,
            "hours": hours
        })
    
    # Calculate averages (filter None values from durations)
    avg_sleep_score = round(sum(scores) / len(scores), 1) if scores else None
    avg_readiness = round(sum(readiness_scores) / len(readiness_scores), 1) if readiness_scores else None
    valid_durations = [d for d in durations if d is not None]
    avg_duration = round(sum(valid_durations) / len(valid_durations), 1) if valid_durations else None
    
    # Get HRV from most recent record (with data)
    hrv = None
    for d in reversed(sleep_data):
        if d.get("average_hrv"):
            hrv = d.get("average_hrv")
            break
    
    return {
        "avg_sleep_score": avg_sleep_score,
        "avg_readiness": avg_readiness,
        "avg_efficiency": avg_efficiency,
        "avg_duration": avg_duration,
        "avg_hrv": hrv,
        "sleep_trend": sleep_trend,
        "readiness_trend": readiness_trend,
        "last_2_days": last_2_days
    }


def main():
    parser = argparse.ArgumentParser(description="Oura Morning Briefing")
    parser.add_argument("--date", help="Date for briefing (YYYY-MM-DD, default: today)")
    parser.add_argument("--token", help="Oura API token")
    parser.add_argument("--verbose", action="store_true", help="Detailed briefing with driver analysis")
    parser.add_argument("--format", choices=["text", "brief", "json", "hybrid"], default="text",
                       help="Output format (text=full briefing, brief=3 lines, json=structured, hybrid=briefing+trends)")
    parser.add_argument("--baseline-days", type=int, default=14,
                       help="Days to use for baseline calculation (default: 14)")
    
    args = parser.parse_args()
    
    try:
        # Initialize client
        client = OuraClient(args.token)
        
        # Determine date
        if args.date:
            target_date = args.date
        else:
            target_date = datetime.now().strftime("%Y-%m-%d")
        
        # Get data for target date
        sleep_data = client.get_sleep(target_date, target_date)
        readiness_data = client.get_readiness(target_date, target_date)
        activity_data = client.get_activity(target_date, target_date)
        
        # Bounds check: ensure arrays are not empty before accessing
        if not sleep_data and not readiness_data:
            print(f"No data available for {target_date}", file=sys.stderr)
            sys.exit(1)
        
        # Create night record (safe access with bounds check)
        night = create_night_record(
            date=target_date,
            sleep=sleep_data[0] if (sleep_data and len(sleep_data) > 0) else None,
            readiness=readiness_data[0] if (readiness_data and len(readiness_data) > 0) else None,
            activity=activity_data[0] if (activity_data and len(activity_data) > 0) else None
        )
        
        # Calculate baseline from historical data
        baseline_start = (datetime.strptime(target_date, "%Y-%m-%d") - timedelta(days=args.baseline_days)).strftime("%Y-%m-%d")
        baseline_end = (datetime.strptime(target_date, "%Y-%m-%d") - timedelta(days=1)).strftime("%Y-%m-%d")
        
        baseline_sleep = client.get_sleep(baseline_start, baseline_end)
        baseline_readiness = client.get_readiness(baseline_start, baseline_end)
        
        # Create baseline nights for calculation (align by date, not index)
        baseline_nights = []
        readiness_by_date = {r["day"]: r for r in baseline_readiness}
        
        for sleep_entry in baseline_sleep:
            date = sleep_entry["day"]
            readiness_entry = readiness_by_date.get(date)
            
            baseline_night = create_night_record(
                date=date,
                sleep=sleep_entry,
                readiness=readiness_entry
            )
            baseline_nights.append(baseline_night)
        
        baseline = Baseline.from_history(baseline_nights) if baseline_nights else None
        
        # Fetch week data for hybrid format (7-day window: target_date - 6 through target_date)
        week_data = None
        if args.format == "hybrid":
            week_start = (datetime.strptime(target_date, "%Y-%m-%d") - timedelta(days=6)).strftime("%Y-%m-%d")
            week_sleep = client.get_sleep(week_start, target_date)
            week_readiness = client.get_readiness(week_start, target_date)
            week_data = _analyze_week(week_sleep, week_readiness)
        
        # Format output
        if args.format == "json":
            output = format_json_briefing(night, baseline)
            print(json.dumps(output, indent=2))
        elif args.format == "brief":
            output = format_brief_briefing(night, baseline)
            print(output)
        elif args.format == "hybrid":
            output = format_hybrid_briefing(night, baseline, week_data)
            print(output)
        else:  # text
            formatter = BriefingFormatter(baseline)
            output = formatter.format(night, verbose=args.verbose)
            print(output)
    
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
