#!/usr/bin/env python3
"""
Oura Baseline & Comparison Analysis

Calculate baselines from historical data and compare current metrics.
Provides statistical significance (z-score, percentiles) and actionable insights.
"""

import argparse
import sys
import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import statistics

# Add scripts directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from oura_api import OuraClient
from schema import NightRecord


@dataclass
class BaselineMetrics:
    """Statistical baseline for a metric."""
    mean: float
    median: float
    std_dev: float
    min: float
    max: float
    p25: float  # 25th percentile
    p75: float  # 75th percentile
    sample_size: int
    
    def z_score(self, value: float) -> float:
        """Calculate z-score (standard deviations from mean)."""
        if self.std_dev == 0:
            return 0.0
        return (value - self.mean) / self.std_dev
    
    def percentile_rank(self, value: float, samples: List[float]) -> float:
        """Calculate percentile rank of value in distribution."""
        if not samples:
            return 50.0
        below = sum(1 for s in samples if s < value)
        return (below / len(samples)) * 100
    
    def interpret_delta(self, value: float) -> Tuple[str, str, str]:
        """
        Interpret delta from baseline.
        Returns: (emoji, label, severity)
        """
        z = self.z_score(value)
        
        if z >= 1.5:
            return "🔥", "Well above baseline", "excellent"
        elif z >= 0.5:
            return "↗️", "Above baseline", "good"
        elif z >= -0.5:
            return "➡️", "Within baseline", "normal"
        elif z >= -1.5:
            return "↘️", "Below baseline", "attention"
        else:
            return "⚠️", "Well below baseline", "concern"


@dataclass
class Baseline:
    """Complete baseline analysis."""
    sleep_score: BaselineMetrics
    readiness: BaselineMetrics
    sleep_hours: BaselineMetrics
    efficiency: BaselineMetrics
    hrv: Optional[BaselineMetrics]
    rhr: Optional[BaselineMetrics]
    period_days: int
    end_date: str


def calculate_baseline_metrics(values: List[float]) -> Optional[BaselineMetrics]:
    """Calculate statistical baseline from a list of values."""
    if not values or len(values) < 3:
        return None
    
    sorted_values = sorted(values)
    
    try:
        return BaselineMetrics(
            mean=round(statistics.mean(values), 1),
            median=round(statistics.median(values), 1),
            std_dev=round(statistics.stdev(values), 1) if len(values) > 1 else 0,
            min=round(min(values), 1),
            max=round(max(values), 1),
            p25=round(sorted_values[len(values) // 4], 1),
            p75=round(sorted_values[3 * len(values) // 4], 1),
            sample_size=len(values)
        )
    except Exception:
        return None


def calculate_sleep_score(sleep_data: dict) -> float:
    """Calculate sleep score from sleep data (matches weekly_report.py logic)."""
    efficiency = sleep_data.get("efficiency", 0)
    duration_hours = sleep_data.get("total_sleep_duration", 0) / 3600 if sleep_data.get("total_sleep_duration") else 0
    
    eff_score = min(efficiency, 100)
    dur_score = min(duration_hours / 8 * 100, 100)
    return round((eff_score * 0.6) + (dur_score * 0.4), 1)


def build_baseline(sleep_data: List[dict], readiness_data: List[dict], period_days: int) -> Baseline:
    """Build baseline from historical data."""
    # Build readiness lookup
    readiness_by_day = {r.get("day"): r for r in readiness_data}
    
    # Extract metrics
    sleep_scores = []
    readiness_scores = []
    sleep_hours = []
    efficiencies = []
    hrv_values = []
    rhr_values = []
    
    for sleep in sleep_data:
        day = sleep.get("day")
        
        # Sleep score
        score = calculate_sleep_score(sleep)
        if score > 0:
            sleep_scores.append(score)
        
        # Sleep hours
        duration_sec = sleep.get("total_sleep_duration", 0)
        if duration_sec:
            sleep_hours.append(round(duration_sec / 3600, 1))
        
        # Efficiency
        eff = sleep.get("efficiency")
        if eff:
            efficiencies.append(eff)
        
        # HRV
        hrv = sleep.get("average_hrv")
        if hrv:
            hrv_values.append(hrv)
        
        # RHR
        rhr = sleep.get("lowest_heart_rate")
        if rhr:
            rhr_values.append(rhr)
        
        # Readiness
        r = readiness_by_day.get(day)
        if r and r.get("score"):
            readiness_scores.append(r["score"])
    
    return Baseline(
        sleep_score=calculate_baseline_metrics(sleep_scores),
        readiness=calculate_baseline_metrics(readiness_scores),
        sleep_hours=calculate_baseline_metrics(sleep_hours),
        efficiency=calculate_baseline_metrics(efficiencies),
        hrv=calculate_baseline_metrics(hrv_values) if hrv_values else None,
        rhr=calculate_baseline_metrics(rhr_values) if rhr_values else None,
        period_days=period_days,
        end_date=sleep_data[-1].get("day") if sleep_data else ""
    )


def compare_to_baseline(current_data: dict, baseline: Baseline, metric_name: str, current_value: float, baseline_metric: BaselineMetrics) -> Dict:
    """Compare current value to baseline and generate insight."""
    delta = current_value - baseline_metric.mean
    z_score = baseline_metric.z_score(current_value)
    emoji, label, severity = baseline_metric.interpret_delta(current_value)
    
    return {
        "metric": metric_name,
        "current": round(current_value, 1),
        "baseline_mean": baseline_metric.mean,
        "baseline_range": f"{baseline_metric.p25}-{baseline_metric.p75}",
        "delta": round(delta, 1),
        "z_score": round(z_score, 2),
        "emoji": emoji,
        "label": label,
        "severity": severity
    }


def format_baseline_report(baseline: Baseline) -> str:
    """Format baseline report for console output."""
    lines = []
    lines.append(f"\n📊 Baseline Analysis ({baseline.period_days}-day period)")
    lines.append(f"   Period ending: {baseline.end_date}")
    lines.append("")
    
    metrics = [
        ("Sleep Score", baseline.sleep_score, "/100"),
        ("Readiness", baseline.readiness, "/100"),
        ("Sleep Duration", baseline.sleep_hours, "h"),
        ("Efficiency", baseline.efficiency, "%"),
    ]
    
    if baseline.hrv:
        metrics.append(("HRV", baseline.hrv, "ms"))
    if baseline.rhr:
        metrics.append(("RHR", baseline.rhr, "bpm"))
    
    for name, metric, unit in metrics:
        if metric:
            lines.append(f"   {name}:")
            lines.append(f"      Mean: {metric.mean}{unit} (±{metric.std_dev})")
            lines.append(f"      Range: {metric.min}-{metric.max}{unit}")
            lines.append(f"      P25-P75: {metric.p25}-{metric.p75}{unit}")
            lines.append(f"      Samples: {metric.sample_size}")
            lines.append("")
    
    return "\n".join(lines)


def format_comparison_report(comparisons: List[Dict], period_label: str) -> str:
    """Format comparison report for console output."""
    lines = []
    lines.append(f"\n📈 Current vs Baseline ({period_label})")
    lines.append("")
    
    for comp in comparisons:
        emoji = comp["emoji"]
        metric = comp["metric"]
        current = comp["current"]
        delta = comp["delta"]
        z = comp["z_score"]
        label = comp["label"]
        
        delta_str = f"+{delta}" if delta > 0 else str(delta)
        lines.append(f"   {emoji} {metric}: {current} ({delta_str}, z={z})")
        lines.append(f"      {label}")
        lines.append("")
    
    # Summary
    concerns = [c for c in comparisons if c["severity"] == "concern"]
    if concerns:
        lines.append("⚠️  Metrics needing attention:")
        for c in concerns:
            lines.append(f"   • {c['metric']}: {c['label']}")
    else:
        lines.append("✅ All metrics within or above baseline range")
    
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Oura Baseline & Comparison Analysis")
    parser.add_argument("--baseline-days", type=int, default=30, help="Days for baseline calculation (default: 30)")
    parser.add_argument("--current-days", type=int, default=7, help="Days for current period comparison (default: 7)")
    parser.add_argument("--token", help="Oura API token")
    parser.add_argument("--json", action="store_true", help="Output JSON format")
    parser.add_argument("--baseline-only", action="store_true", help="Show baseline without comparison")
    
    args = parser.parse_args()
    
    try:
        client = OuraClient(args.token)
        
        # Fetch baseline period data
        baseline_end = datetime.now()
        baseline_start = baseline_end - timedelta(days=args.baseline_days)
        
        baseline_sleep = client.get_sleep(
            baseline_start.strftime("%Y-%m-%d"),
            baseline_end.strftime("%Y-%m-%d")
        )
        baseline_readiness = client.get_readiness(
            baseline_start.strftime("%Y-%m-%d"),
            baseline_end.strftime("%Y-%m-%d")
        )
        
        # Calculate baseline
        baseline = build_baseline(baseline_sleep, baseline_readiness, args.baseline_days)
        
        if args.baseline_only:
            if args.json:
                print(json.dumps({
                    "baseline": {
                        "sleep_score": baseline.sleep_score.__dict__ if baseline.sleep_score else None,
                        "readiness": baseline.readiness.__dict__ if baseline.readiness else None,
                        "sleep_hours": baseline.sleep_hours.__dict__ if baseline.sleep_hours else None,
                        "efficiency": baseline.efficiency.__dict__ if baseline.efficiency else None,
                        "hrv": baseline.hrv.__dict__ if baseline.hrv else None,
                        "rhr": baseline.rhr.__dict__ if baseline.rhr else None,
                        "period_days": baseline.period_days,
                        "end_date": baseline.end_date
                    }
                }, indent=2))
            else:
                print(format_baseline_report(baseline))
            return
        
        # Fetch current period data
        current_end = datetime.now()
        current_start = current_end - timedelta(days=args.current_days)
        
        current_sleep = client.get_sleep(
            current_start.strftime("%Y-%m-%d"),
            current_end.strftime("%Y-%m-%d")
        )
        current_readiness = client.get_readiness(
            current_start.strftime("%Y-%m-%d"),
            current_end.strftime("%Y-%m-%d")
        )
        
        # Calculate current averages
        readiness_by_day = {r.get("day"): r for r in current_readiness}
        
        current_sleep_scores = [calculate_sleep_score(s) for s in current_sleep if calculate_sleep_score(s) > 0]
        current_readiness_scores = [r.get("score") for r in current_readiness if r.get("score")]
        current_sleep_hours = [s.get("total_sleep_duration", 0) / 3600 for s in current_sleep if s.get("total_sleep_duration")]
        current_efficiencies = [s.get("efficiency") for s in current_sleep if s.get("efficiency")]
        
        avg_sleep_score = statistics.mean(current_sleep_scores) if current_sleep_scores else 0
        avg_readiness = statistics.mean(current_readiness_scores) if current_readiness_scores else 0
        avg_sleep_hours = statistics.mean(current_sleep_hours) if current_sleep_hours else 0
        avg_efficiency = statistics.mean(current_efficiencies) if current_efficiencies else 0
        
        # Generate comparisons
        comparisons = []
        
        if baseline.sleep_score and avg_sleep_score:
            comparisons.append(compare_to_baseline({}, baseline, "Sleep Score", avg_sleep_score, baseline.sleep_score))
        
        if baseline.readiness and avg_readiness:
            comparisons.append(compare_to_baseline({}, baseline, "Readiness", avg_readiness, baseline.readiness))
        
        if baseline.sleep_hours and avg_sleep_hours:
            comparisons.append(compare_to_baseline({}, baseline, "Sleep Duration", avg_sleep_hours, baseline.sleep_hours))
        
        if baseline.efficiency and avg_efficiency:
            comparisons.append(compare_to_baseline({}, baseline, "Efficiency", avg_efficiency, baseline.efficiency))
        
        # Output
        period_label = f"Last {args.current_days}d vs {args.baseline_days}d baseline"
        
        if args.json:
            print(json.dumps({
                "baseline": {
                    "period_days": baseline.period_days,
                    "end_date": baseline.end_date
                },
                "current": {
                    "period_days": args.current_days,
                    "avg_sleep_score": round(avg_sleep_score, 1),
                    "avg_readiness": round(avg_readiness, 1),
                    "avg_sleep_hours": round(avg_sleep_hours, 1),
                    "avg_efficiency": round(avg_efficiency, 1)
                },
                "comparisons": comparisons
            }, indent=2))
        else:
            print(format_comparison_report(comparisons, period_label))
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
