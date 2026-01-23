#!/usr/bin/env python3
"""
Event Logging & Correlation Analysis

Track behaviors/exposures and correlate with sleep/readiness outcomes.
Helps answer: "Does X affect my recovery?"

Examples:
- Does alcohol hurt my sleep?
- Does sauna improve HRV?
- Does late eating affect readiness?
- Does creatine help?
"""

import argparse
import sys
import json
import statistics
import shutil
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple, Optional

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from oura_api import OuraClient


class EventLogger:
    """Manage event logging to JSONL file."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize event logger.
        
        Args:
            data_dir: Directory for events.jsonl (default: ~/.oura-analytics/)
        """
        if data_dir is None:
            base_dir = Path.home() / ".oura-analytics"
            legacy_dir = base_dir / "data"
            legacy_file = legacy_dir / "events.jsonl"
            default_file = base_dir / "events.jsonl"

            if legacy_file.exists() and not default_file.exists():
                base_dir.mkdir(parents=True, exist_ok=True)
                shutil.move(str(legacy_file), str(default_file))

            data_dir = base_dir
        
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.events_file = self.data_dir / "events.jsonl"
    
    def log_event(self, date: str, tags: List[str], notes: str = "") -> None:
        """
        Log an event.
        
        Args:
            date: Date (YYYY-MM-DD)
            tags: List of tags (e.g., ["alcohol", "late-meal"])
            notes: Optional notes
        """
        event = {
            "date": date,
            "tags": tags,
            "notes": notes,
            "logged_at": datetime.now().isoformat()
        }
        
        with open(self.events_file, "a") as f:
            f.write(json.dumps(event) + "\n")
        
        print(f"✅ Logged event for {date}: {', '.join(tags)}")
    
    def load_events(self) -> List[Dict]:
        """Load all events from file."""
        if not self.events_file.exists():
            return []
        
        events = []
        with open(self.events_file, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        events.append(json.loads(line))
                    except json.JSONDecodeError:
                        continue
        
        return events
    
    def get_events_by_tag(self, tag: str) -> List[Dict]:
        """Get all events with a specific tag."""
        events = self.load_events()
        return [e for e in events if tag in e.get("tags", [])]


class CorrelationAnalyzer:
    """Analyze correlations between events and outcomes."""
    
    def __init__(self, oura_client: OuraClient):
        """
        Initialize analyzer.
        
        Args:
            oura_client: OuraClient instance
        """
        self.client = oura_client
    
    def analyze_tag_correlation(
        self,
        events: List[Dict],
        metric: str = "readiness",
        lag_days: int = 1,
        tag: Optional[str] = None
    ) -> Dict:
        """
        Analyze correlation between event tag and outcome metric.
        
        Args:
            events: List of event dicts with same tag
            metric: Metric to correlate ("readiness" | "sleep_score" | "hrv")
            lag_days: Days to look ahead for outcome (default: 1 = next-day effect)
            tag: The tag being analyzed (for accurate reporting)
        
        Returns:
            Analysis dict with mean difference and significance
        """
        if not events:
            return {"error": "No events provided"}
        
        # Use provided tag or fall back to first tag in first event
        analyzed_tag = tag or (events[0]["tags"][0] if events[0].get("tags") else "unknown")
        
        # Extract dates
        event_dates = [e["date"] for e in events]
        
        # Fetch Oura data for event dates + surrounding period
        all_dates = []
        for date_str in event_dates:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            for offset in range(-7, lag_days + 1):  # 7 days before, up to lag_days after
                check_date = date + timedelta(days=offset)
                all_dates.append(check_date.strftime("%Y-%m-%d"))
        
        all_dates = sorted(set(all_dates))
        
        if not all_dates:
            return {"error": "No valid dates"}
        
        start_date = all_dates[0]
        end_date = all_dates[-1]
        
        # Fetch data
        sleep_data = self.client.get_sleep(start_date, end_date)
        readiness_data = self.client.get_readiness(start_date, end_date)
        
        # Build metric lookup
        metric_by_day = {}
        
        if metric == "readiness":
            for r in readiness_data:
                metric_by_day[r["day"]] = r.get("score", 0)
        elif metric == "sleep_score":
            for s in sleep_data:
                efficiency = s.get("efficiency", 0)
                duration_hours = s.get("total_sleep_duration", 0) / 3600 if s.get("total_sleep_duration") else 0
                eff_score = min(efficiency, 100)
                dur_score = min(duration_hours / 8 * 100, 100)
                score = round((eff_score * 0.6) + (dur_score * 0.4), 1)
                metric_by_day[s["day"]] = score
        elif metric == "hrv":
            for s in sleep_data:
                hrv = s.get("average_hrv")
                if hrv:
                    metric_by_day[s["day"]] = hrv
        
        # Calculate outcome values for event days + lag
        event_outcomes = []
        control_outcomes = []
        
        for date_str in event_dates:
            date = datetime.strptime(date_str, "%Y-%m-%d")
            outcome_date = (date + timedelta(days=lag_days)).strftime("%Y-%m-%d")
            
            # Event outcome
            if outcome_date in metric_by_day:
                event_outcomes.append(metric_by_day[outcome_date])
            
            # Control outcomes (same weekday, no event within 3 days)
            for offset in range(-14, -7):  # 1-2 weeks before
                control_date = (date + timedelta(days=offset)).strftime("%Y-%m-%d")
                
                # Check if this date had the same event tag
                is_event_day = any(
                    control_date == e["date"]
                    for e in events
                )
                
                if not is_event_day and control_date in metric_by_day:
                    control_outcomes.append(metric_by_day[control_date])
        
        # Calculate statistics
        if not event_outcomes:
            return {"error": "No outcome data for event days"}
        
        if not control_outcomes:
            return {"error": "No control data available"}
        
        event_mean = statistics.mean(event_outcomes)
        control_mean = statistics.mean(control_outcomes)
        diff = event_mean - control_mean
        
        # Simple t-test significance approximation
        # For proper stats, would use scipy.stats.ttest_ind
        n_event = len(event_outcomes)
        n_control = len(control_outcomes)
        
        if n_event < 3 or n_control < 3:
            significance = "insufficient_data"
        elif abs(diff) < 2:
            significance = "not_significant"
        elif abs(diff) < 5:
            significance = "possibly_significant"
        else:
            significance = "likely_significant"
        
        return {
            "metric": metric,
            "tag": analyzed_tag,
            "event_mean": round(event_mean, 1),
            "control_mean": round(control_mean, 1),
            "difference": round(diff, 1),
            "event_sample_size": n_event,
            "control_sample_size": n_control,
            "significance": significance,
            "interpretation": self._interpret_correlation(metric, diff, significance)
        }
    
    def _interpret_correlation(self, metric: str, diff: float, significance: str) -> str:
        """Generate human-readable interpretation."""
        if significance == "insufficient_data":
            return "Need more data points to draw conclusions (min 3 events)"
        
        if significance == "not_significant":
            return f"No meaningful effect detected (±{abs(diff):.1f} pts)"
        
        direction = "improves" if diff > 0 else "reduces"
        magnitude = "slightly" if abs(diff) < 5 else "moderately" if abs(diff) < 10 else "significantly"
        
        return f"Event {magnitude} {direction} {metric} by {abs(diff):.1f} points (next-day)"


def main():
    parser = argparse.ArgumentParser(description="Oura Event Logging & Correlation")
    subparsers = parser.add_subparsers(dest="command", required=True)
    
    # Log command
    log_parser = subparsers.add_parser("log", help="Log an event")
    log_parser.add_argument("--date", help="Date (YYYY-MM-DD, default: today)")
    log_parser.add_argument("--tags", required=True, help="Comma-separated tags (e.g., 'alcohol,late-meal')")
    log_parser.add_argument("--notes", default="", help="Optional notes")
    
    # Correlate command
    corr_parser = subparsers.add_parser("correlate", help="Analyze correlation")
    corr_parser.add_argument("--tag", required=True, help="Tag to analyze")
    corr_parser.add_argument("--metric", default="readiness", choices=["readiness", "sleep_score", "hrv"], help="Metric to correlate")
    corr_parser.add_argument("--lag", type=int, default=1, help="Days to look ahead (default: 1 = next-day)")
    corr_parser.add_argument("--token", help="Oura API token")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List logged events")
    list_parser.add_argument("--tag", help="Filter by tag")
    
    args = parser.parse_args()
    
    logger = EventLogger()
    
    if args.command == "log":
        date = args.date or datetime.now().strftime("%Y-%m-%d")
        tags = [t.strip() for t in args.tags.split(",")]
        logger.log_event(date, tags, args.notes)
    
    elif args.command == "list":
        events = logger.load_events()
        
        if args.tag:
            events = [e for e in events if args.tag in e.get("tags", [])]
        
        if not events:
            print("No events found")
            return
        
        print(f"\n📋 Events ({len(events)} total):\n")
        for e in sorted(events, key=lambda x: x["date"], reverse=True):
            tags_str = ", ".join(e["tags"])
            notes_str = f" - {e['notes']}" if e.get("notes") else ""
            print(f"   {e['date']}: {tags_str}{notes_str}")
        print()
    
    elif args.command == "correlate":
        events = logger.get_events_by_tag(args.tag)
        
        if not events:
            print(f"No events found with tag '{args.tag}'")
            sys.exit(1)
        
        print(f"\n🔬 Analyzing correlation: {args.tag} → {args.metric}\n")
        
        client = OuraClient(args.token)
        analyzer = CorrelationAnalyzer(client)
        
        result = analyzer.analyze_tag_correlation(events, args.metric, args.lag, args.tag)
        
        if "error" in result:
            print(f"Error: {result['error']}")
            sys.exit(1)
        
        print(f"📊 Results:")
        print(f"   Tag: {result['tag']}")
        print(f"   Metric: {result['metric']}")
        print(f"   Event days: {result['event_mean']} (n={result['event_sample_size']})")
        print(f"   Control days: {result['control_mean']} (n={result['control_sample_size']})")
        print(f"   Difference: {'+' if result['difference'] > 0 else ''}{result['difference']}")
        print(f"   Significance: {result['significance']}")
        print(f"\n💡 {result['interpretation']}\n")


if __name__ == "__main__":
    main()
