#!/usr/bin/env python3
"""
Morning Briefing Formatter for Oura Analytics

Generates concise, actionable daily briefings with:
- Headline metrics with baseline context
- Driver analysis (what's causing the scores)
- Recovery status (GREEN/YELLOW/RED)
- Decision recommendations
- Pattern detection (trends, streaks)
"""

import sys
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple
from datetime import datetime, timedelta

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from schema import NightRecord, SleepRecord, ReadinessRecord, ActivityRecord


class Baseline:
    """Baseline metrics calculated from historical data."""
    
    def __init__(self, 
                 avg_sleep_hours: float = 7.5,
                 avg_readiness: float = 75.0,
                 avg_hrv: float = 40.0,
                 avg_rhr: float = 60.0):
        self.avg_sleep_hours = avg_sleep_hours
        self.avg_readiness = avg_readiness
        self.avg_hrv = avg_hrv
        self.avg_rhr = avg_rhr
    
    @classmethod
    def from_history(cls, nights: List[NightRecord]) -> 'Baseline':
        """Calculate baseline from historical night records with outlier removal."""
        if not nights:
            return cls()
        
        # Calculate averages with outlier removal (remove top/bottom 10% if sample is large enough)
        sleep_hours = sorted([n.sleep.total_sleep_hours for n in nights if n.sleep])
        readiness_scores = sorted([n.readiness.score for n in nights if n.readiness])
        hrv_values = sorted([n.sleep.average_hrv_ms for n in nights if n.sleep and n.sleep.average_hrv_ms])
        rhr_values = sorted([n.sleep.lowest_heart_rate_bpm for n in nights if n.sleep and n.sleep.lowest_heart_rate_bpm])
        
        def robust_avg(values: List[float], default: float) -> float:
            """Calculate average with outlier removal (trim 10% from each end if n >= 10)."""
            if not values:
                return default
            if len(values) < 10:
                # Too few samples for outlier removal
                return sum(values) / len(values)
            
            # Remove top/bottom 10%
            trim = max(1, int(len(values) * 0.1))
            trimmed = values[trim:-trim]
            return sum(trimmed) / len(trimmed)
        
        return cls(
            avg_sleep_hours=robust_avg(sleep_hours, 7.5),
            avg_readiness=robust_avg(readiness_scores, 75.0),
            avg_hrv=robust_avg(hrv_values, 40.0),
            avg_rhr=robust_avg(rhr_values, 60.0)
        )


class BriefingFormatter:
    """Formats morning briefings with context and recommendations."""
    
    def __init__(self, baseline: Optional[Baseline] = None):
        self.baseline = baseline or Baseline()
    
    def format(self, night: NightRecord, verbose: bool = False) -> str:
        """
        Format a morning briefing.
        
        Args:
            night: NightRecord for the day
            verbose: Include additional detail
        
        Returns:
            Formatted briefing string
        """
        lines = []
        
        # Header
        lines.append(self._header(night.date))
        lines.append("")
        
        # Headline metrics
        if night.sleep:
            lines.append(self._sleep_line(night.sleep))
        
        if night.readiness:
            lines.append(self._readiness_line(night.readiness))
            if verbose:
                lines.append(self._driver_analysis(night.readiness))
        
        lines.append("")
        
        # Status and recommendation
        status, recommendation = self._get_status_and_recommendation(night)
        lines.append(f"Recovery Status: {status}")
        lines.append(f"Recommendation: {recommendation}")
        
        # Pattern detection
        if verbose:
            pattern = self._detect_pattern(night)
            if pattern:
                lines.append("")
                lines.append(f"Notable: {pattern}")
        
        return "\n".join(lines)
    
    def _header(self, date: str) -> str:
        """Format header with date."""
        dt = datetime.strptime(date, "%Y-%m-%d")
        return f"☀️  Morning Briefing ({dt.strftime('%b %d')})"
    
    def _sleep_line(self, sleep: SleepRecord) -> str:
        """Format sleep line with context."""
        hours = sleep.total_sleep_hours
        
        # Delta from baseline
        delta_hours = hours - self.baseline.avg_sleep_hours
        delta_min = int(delta_hours * 60)
        
        if abs(delta_min) < 15:
            delta_str = "on target"
            indicator = "✓"
        elif delta_min > 0:
            delta_str = f"↑{delta_min}min vs avg"
            indicator = "✓"
        else:
            delta_str = f"↓{abs(delta_min)}min vs avg"
            indicator = "⚠️" if abs(delta_min) > 60 else "○"
        
        # Format duration
        h = int(hours)
        m = int((hours - h) * 60)
        
        return f"Sleep: {h}h {m}m ({delta_str}) {indicator}"
    
    def _readiness_line(self, readiness: ReadinessRecord) -> str:
        """Format readiness line with context."""
        score = readiness.score
        
        # Delta from baseline
        delta = score - self.baseline.avg_readiness
        
        if score >= 85:
            indicator = "✓"
        elif score >= 70:
            indicator = "○"
        else:
            indicator = "⚠️"
        
        if abs(delta) < 3:
            delta_str = "stable"
        elif delta > 0:
            delta_str = f"↑{int(delta)} vs baseline"
        else:
            delta_str = f"↓{abs(int(delta))} vs baseline"
        
        return f"Readiness: {score} ({delta_str}) {indicator}"
    
    def _driver_analysis(self, readiness: ReadinessRecord) -> str:
        """Analyze what's driving readiness score."""
        # Identify low contributors
        contributors = {
            "HRV balance": readiness.hrv_balance,
            "Sleep balance": readiness.sleep_balance,
            "Recovery index": readiness.recovery_index,
            "RHR": readiness.resting_heart_rate,
            "Body temp": readiness.body_temperature,
            "Activity balance": readiness.activity_balance
        }
        
        # Filter out None values and sort by score
        valid_contributors = {k: v for k, v in contributors.items() if v is not None}
        sorted_contributors = sorted(valid_contributors.items(), key=lambda x: x[1])
        
        # Identify lowest contributors (<70)
        low = [k for k, v in sorted_contributors if v < 70]
        
        if low:
            drivers = ", ".join(low[:2])  # Top 2 lowest
            return f"└─ Driven by: {drivers}"
        else:
            return "└─ All contributors balanced"
    
    def _get_status_and_recommendation(self, night: NightRecord) -> Tuple[str, str]:
        """Determine recovery status and recommendation."""
        if not night.readiness:
            return "UNKNOWN", "Insufficient data"
        
        score = night.readiness.score
        
        if score >= 85:
            status = "🟢 GREEN"
            recommendation = "Optimal day. Ready for intensity."
        elif score >= 70:
            status = "🟡 YELLOW"
            recommendation = "Moderate day. Avoid heavy training."
        else:
            status = "🔴 RED"
            recommendation = "Recovery day. Light activity only."
        
        return status, recommendation
    
    def _detect_pattern(self, night: NightRecord) -> Optional[str]:
        """Detect notable patterns (placeholder for trend analysis)."""
        # This would require historical data for real trend detection
        # For now, just highlight extremes
        
        if night.sleep and night.sleep.total_sleep_hours >= 8.5:
            return "Excellent sleep duration"
        
        if night.readiness and night.readiness.score <= 65:
            return "Low readiness - prioritize recovery"
        
        if night.sleep and night.sleep.efficiency_percent >= 90:
            return "High sleep efficiency"
        
        return None


def format_brief_briefing(night: NightRecord, baseline: Optional[Baseline] = None) -> str:
    """
    Format a brief 3-line briefing (for notifications).
    
    Args:
        night: NightRecord for the day
        baseline: Optional baseline metrics
    
    Returns:
        3-line briefing string
    """
    formatter = BriefingFormatter(baseline)
    
    lines = []
    
    if night.sleep:
        hours = night.sleep.total_sleep_hours
        h = int(hours)
        m = int((hours - h) * 60)
        lines.append(f"Sleep: {h}h {m}m")
    
    if night.readiness:
        score = night.readiness.score
        if score >= 85:
            status = "Green"
        elif score >= 70:
            status = "Yellow"
        else:
            status = "Red"
        lines.append(f"Readiness: {score} ({status})")
    
    _, recommendation = formatter._get_status_and_recommendation(night)
    lines.append(recommendation)
    
    return "\n".join(lines)


def format_json_briefing(night: NightRecord, baseline: Optional[Baseline] = None) -> Dict[str, Any]:
    """
    Format briefing as JSON for API integration.
    
    Args:
        night: NightRecord for the day
        baseline: Optional baseline metrics
    
    Returns:
        Dictionary with briefing data
    """
    formatter = BriefingFormatter(baseline)
    status, recommendation = formatter._get_status_and_recommendation(night)
    
    # Extract status code (remove emoji)
    # Status format: "🟢 GREEN" → "GREEN"
    status_code = status.split()[-1] if status else "UNKNOWN"
    
    briefing = {
        "date": night.date,
        "sleep": None,
        "readiness": None,
        "status": status_code,
        "recommendation": recommendation
    }
    
    if night.sleep:
        briefing["sleep"] = {
            "duration_hours": round(night.sleep.total_sleep_hours, 2),
            "efficiency_percent": night.sleep.efficiency_percent,
            "hrv_ms": night.sleep.average_hrv_ms
        }
    
    if night.readiness:
        briefing["readiness"] = {
            "score": night.readiness.score,
            "delta_vs_baseline": round(night.readiness.score - formatter.baseline.avg_readiness, 1) if baseline else None,
            "low_contributors": _get_low_contributors(night.readiness)
        }
    
    return briefing


def _get_low_contributors(readiness: ReadinessRecord) -> List[str]:
    """Get list of low contributors (<70)."""
    contributors = {
        "hrv_balance": readiness.hrv_balance,
        "sleep_balance": readiness.sleep_balance,
        "recovery_index": readiness.recovery_index,
        "resting_heart_rate": readiness.resting_heart_rate,
        "body_temperature": readiness.body_temperature,
        "activity_balance": readiness.activity_balance
    }
    
    return [k for k, v in contributors.items() if v is not None and v < 70]


def format_hybrid_briefing(
    night: NightRecord, 
    baseline: Optional[Baseline] = None,
    week_data: Optional[Dict[str, Any]] = None
) -> str:
    """
    Format a hybrid daily report combining morning briefing with trend snapshot.
    
    This combines:
    1) Morning Briefing (top): actionable daily guidance with driver analysis
    2) Trend Snapshot (bottom): 7-day averages + recent sleep/readiness history
    
    Args:
        night: NightRecord for the day
        baseline: Optional baseline metrics
        week_data: Optional pre-calculated 7-day statistics
    
    Returns:
        Hybrid briefing string (≤12 lines for chat readability)
    """
    formatter = BriefingFormatter(baseline)
    
    lines = []
    
    # === SECTION 1: Morning Briefing ===
    lines.append(f"🌅 *Morning Briefing — {_format_date(night.date)}*")
    lines.append("─" * 24)
    
    # Sleep line with delta
    if night.sleep:
        hours = night.sleep.total_sleep_hours
        h = int(hours)
        m = int((hours - h) * 60)
        delta_min = int((hours - formatter.baseline.avg_sleep_hours) * 60)
        if abs(delta_min) < 15:
            delta_str = "on target"
        elif delta_min > 0:
            delta_str = f"↑{delta_min}min vs avg"
        else:
            delta_str = f"↓{abs(delta_min)}min vs avg"
        sleep_indicator = "✅" if abs(delta_min) < 60 else "⚠️"
        lines.append(f"💤 *Sleep*: {h}h {m}m ({delta_str}) {sleep_indicator}")
    
    # Readiness line with delta
    if night.readiness:
        score = night.readiness.score
        delta = score - formatter.baseline.avg_readiness
        if abs(delta) < 3:
            delta_str = "stable"
        elif delta > 0:
            delta_str = f"↑{int(delta)} vs baseline"
        else:
            delta_str = f"↓{abs(int(delta))} vs baseline"
        ready_indicator = "✅" if score >= 70 else "⚠️"
        lines.append(f"⚡ *Readiness*: {score} ({delta_str}) {ready_indicator}")
        
        # Driver analysis (compact)
        drivers = _get_low_contributors(night.readiness)
        if drivers:
            lines.append(f"*Drivers*: {', '.join(drivers[:2])}")
        else:
            lines.append("*Drivers*: All balanced")
    
    # Recovery status + recommendation
    status, recommendation = formatter._get_status_and_recommendation(night)
    lines.append(f"*Recovery*: {status}")
    lines.append(f"*Rec*: {recommendation}")
    
    # === SECTION 2: Trend Snapshot ===
    if week_data:
        lines.append("")
        lines.append(f"*📊 7-Day Trends*")
        lines.append("─" * 24)
        
        # 7-day averages with delta arrows
        avg_sleep = week_data.get("avg_sleep_score")
        avg_readiness = week_data.get("avg_readiness")
        avg_duration = week_data.get("avg_duration")
        avg_efficiency = week_data.get("avg_efficiency")
        avg_hrv = week_data.get("avg_hrv")
        
        # Sleep score with trend
        sleep_trend = week_data.get("sleep_trend", 0)
        if avg_sleep:
            trend_arrow = _trend_arrow(sleep_trend)
            lines.append(f"*Sleep Score*: `{avg_sleep:>2}` {trend_arrow}")
        
        # Readiness with trend
        readiness_trend = week_data.get("readiness_trend", 0)
        if avg_readiness:
            trend_arrow = _trend_arrow(readiness_trend)
            lines.append(f"*Readiness*: `{avg_readiness:>2}` {trend_arrow}")
        
        # Key metrics row
        metrics = []
        if avg_duration:
            metrics.append(f"*{avg_duration}h* sleep")
        if avg_efficiency:
            metrics.append(f"*{avg_efficiency}%* eff")
        if avg_hrv:
            metrics.append(f"*{avg_hrv}ms* HRV")
        if metrics:
            lines.append(f"• {' • '.join(metrics)}")
        
        # Last 2 nights
        last_2_days = week_data.get("last_2_days", [])
        if last_2_days and len(last_2_days) >= 2:
            d1 = last_2_days[-2]
            d2 = last_2_days[-1]
            d1_sleep = d1.get("sleep_score", "N/A")
            d1_ready = d1.get("readiness", "N/A")
            d2_sleep = d2.get("sleep_score", "N/A")
            d2_ready = d2.get("readiness", "N/A")
            
            d1_date = d1.get("day", "")[-5:]  # MM-DD
            d2_date = d2.get("day", "")[-5:]
            lines.append("")
            lines.append(f"*Recent*: {d1_date} → `{d1_sleep}`/`{d1_ready}` • {d2_date} → `{d2_sleep}`/`{d2_ready}`")
    
    return "\n".join(lines)


def _format_date(date_str: str) -> str:
    """Format date string for display."""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    return dt.strftime("%b %d")


def _trend_arrow(trend: float) -> str:
    """Get arrow indicator for trend value."""
    if trend > 1:
        return "↑"  # Trending up
    elif trend < -1:
        return "↓"  # Trending down
    else:
        return "→"  # Stable


if __name__ == "__main__":
    import argparse
    from oura_api import OuraClient
    from schema import create_night_record

    parser = argparse.ArgumentParser(description="Oura Morning Briefing")
    parser.add_argument("--date", help="Date (YYYY-MM-DD, default: yesterday)")
    parser.add_argument("--format", choices=["brief", "hybrid", "json"], default="hybrid")
    parser.add_argument("--token", help="Oura API token")
    args = parser.parse_args()

    # Default to yesterday
    if args.date:
        target_date = args.date
    else:
        target_date = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")

    try:
        client = OuraClient(args.token)
        sleep_data = client.get_sleep(target_date, target_date)
        readiness_data = client.get_readiness(target_date, target_date)

        if not sleep_data:
            print(f"No data for {target_date}")
            sys.exit(1)

        # Build NightRecord from API response using schema normalizer
        night = create_night_record(
            date=target_date,
            sleep=sleep_data[0] if sleep_data else None,
            readiness=readiness_data[0] if readiness_data else None
        )

        if args.format == "json":
            import json
            print(json.dumps(format_json_briefing(night), indent=2))
        elif args.format == "brief":
            print(format_brief_briefing(night))
        else:
            print(format_hybrid_briefing(night))

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
