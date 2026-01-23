#!/usr/bin/env python3
"""
Daily Summary with Driver Analysis

Enhanced morning briefing with actionable insights and driver analysis.
Shows what's affecting your scores and provides contextual recommendations.
"""

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from oura_api import OuraClient
from drivers import DriverAnalyzer, format_drivers_report
from baseline import build_baseline


def format_hours(seconds: int) -> str:
    """Format seconds as hours and minutes."""
    hours = seconds / 3600
    h = int(hours)
    m = int((hours - h) * 60)
    return f"{h}h {m}m"


def main():
    parser = argparse.ArgumentParser(description="Daily Oura Summary with Driver Analysis")
    parser.add_argument("--date", help="Date (YYYY-MM-DD, default: yesterday)")
    parser.add_argument("--baseline-days", type=int, default=30, help="Days for baseline calculation")
    parser.add_argument("--token", help="Oura API token")
    
    args = parser.parse_args()
    
    # Default to yesterday (since Oura data lags by a day)
    if args.date:
        target_date = args.date
    else:
        target_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    
    try:
        client = OuraClient(args.token)
        
        # Fetch target day data
        sleep_data = client.get_sleep(target_date, target_date)
        readiness_data = client.get_readiness(target_date, target_date)
        
        if not sleep_data:
            print(f"No sleep data for {target_date}")
            sys.exit(1)
        
        sleep = sleep_data[0]
        readiness = readiness_data[0] if readiness_data else {}
        
        # Fetch baseline data (last N days before target)
        baseline_end = datetime.strptime(target_date, "%Y-%m-%d") - timedelta(days=1)
        baseline_start = baseline_end - timedelta(days=args.baseline_days)
        
        baseline_sleep = client.get_sleep(
            baseline_start.strftime("%Y-%m-%d"),
            baseline_end.strftime("%Y-%m-%d")
        )
        baseline_readiness = client.get_readiness(
            baseline_start.strftime("%Y-%m-%d"),
            baseline_end.strftime("%Y-%m-%d")
        )
        
        # Calculate baseline metrics
        baseline = build_baseline(baseline_sleep, baseline_readiness, args.baseline_days)
        
        # Build baseline dict for driver analyzer
        baseline_dict = {
            "sleep_hours": baseline.sleep_hours.mean if baseline.sleep_hours else 7.5,
            "efficiency": baseline.efficiency.mean if baseline.efficiency else 85.0,
            "deep_sleep": 1.5,  # Would calculate from raw data if available
            "rem_sleep": 1.8,   # Would calculate from raw data if available
            "hrv": baseline.hrv.mean if baseline.hrv else 40.0,
            "rhr": baseline.rhr.mean if baseline.rhr else 60.0,
            "readiness": baseline.readiness.mean if baseline.readiness else 75.0
        }
        
        analyzer = DriverAnalyzer(baseline_dict)
        
        # Analyze drivers
        sleep_drivers = analyzer.analyze_sleep_drivers(sleep)
        readiness_drivers = analyzer.analyze_readiness_drivers(sleep, readiness)
        
        readiness_score = readiness.get("score", 0) if readiness else 0
        suggestion = analyzer.generate_suggestion(readiness_score, readiness_drivers)
        
        # Format output
        print(f"\n📊 Daily Oura Summary - {target_date}")
        print("=" * 50)
        
        # Readiness (lead with most important metric)
        if readiness_score:
            baseline_ready = baseline.readiness.mean if baseline.readiness else 75.0
            delta_ready = readiness_score - baseline_ready
            delta_str = f"+{delta_ready:.0f}" if delta_ready > 0 else f"{delta_ready:.0f}"
            
            if readiness_score >= 85:
                emoji = "🟢"
            elif readiness_score >= 70:
                emoji = "🟡"
            else:
                emoji = "🔴"
            
            print(f"\n{emoji} Readiness: {readiness_score}/100 ({delta_str} vs baseline)")
            
            # Show top drivers
            negative_drivers = [d for d in readiness_drivers if d.impact == "negative"]
            if negative_drivers:
                print(format_drivers_report(negative_drivers, "   └─ Factors pulling down"))
        
        # Sleep metrics
        duration = sleep.get("total_sleep_duration")
        efficiency = sleep.get("efficiency")
        
        if duration:
            baseline_dur = baseline.sleep_hours.mean if baseline.sleep_hours else 7.5
            actual_dur = duration / 3600
            delta_dur = actual_dur - baseline_dur
            delta_str = f"+{delta_dur:.1f}h" if delta_dur > 0 else f"{delta_dur:.1f}h"
            
            print(f"\n🌙 Sleep: {format_hours(duration)} ({delta_str} vs baseline)")
        
        if efficiency:
            baseline_eff = baseline.efficiency.mean if baseline.efficiency else 85.0
            delta_eff = efficiency - baseline_eff
            delta_str = f"+{delta_eff:.0f}%" if delta_eff > 0 else f"{delta_eff:.0f}%"
            
            print(f"   Efficiency: {efficiency}% ({delta_str} vs baseline)")
        
        # Sleep stages
        deep = sleep.get("deep_sleep_duration")
        rem = sleep.get("rem_sleep_duration")
        
        if deep or rem:
            print("\n   Sleep Stages:")
            if deep:
                print(f"      Deep: {format_hours(deep)}")
            if rem:
                print(f"      REM: {format_hours(rem)}")
        
        # HRV & RHR
        hrv = sleep.get("average_hrv")
        rhr = sleep.get("lowest_heart_rate")
        
        if hrv or rhr:
            print("\n   Recovery Markers:")
            if hrv:
                baseline_hrv = baseline.hrv.mean if baseline.hrv else 40.0
                delta_hrv = hrv - baseline_hrv
                delta_str = f"+{delta_hrv:.0f}ms" if delta_hrv > 0 else f"{delta_hrv:.0f}ms"
                print(f"      HRV: {hrv}ms ({delta_str})")
            if rhr:
                baseline_rhr = baseline.rhr.mean if baseline.rhr else 60.0
                delta_rhr = rhr - baseline_rhr
                delta_str = f"+{delta_rhr:.0f}bpm" if delta_rhr > 0 else f"{delta_rhr:.0f}bpm"
                print(f"      RHR: {rhr}bpm ({delta_str})")
        
        # Actionable suggestion
        print(f"\n💡 {suggestion}")
        print()
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
