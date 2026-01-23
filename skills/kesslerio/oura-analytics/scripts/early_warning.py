#!/usr/bin/env python3
"""
Early Warning System - Detect illness/overtraining before symptoms

Multi-signal monitoring for early detection of:
- Illness (temperature elevation, HRV drop, RHR increase)
- Overtraining (sustained low readiness, elevated RHR, low HRV)
- Recovery debt (multiple nights of poor sleep)

Uses rolling baselines and requires 2+ signals to trigger alarm.
"""

import argparse
import sys
import statistics
from datetime import datetime, timedelta
from pathlib import Path
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from oura_api import OuraClient


@dataclass
class Signal:
    """A warning signal."""
    name: str
    value: float
    baseline: float
    delta: float
    threshold_exceeded: bool
    severity: str  # "high" | "medium" | "low"
    
    def __str__(self) -> str:
        sign = "+" if self.delta > 0 else ""
        emoji = "🔴" if self.severity == "high" else "🟡" if self.severity == "medium" else "⚪"
        return f"{emoji} {self.name}: {self.value:.1f} ({sign}{self.delta:.1f} vs {self.baseline:.1f})"


@dataclass
class WarningReport:
    """Early warning report."""
    date: str
    alarm_triggered: bool
    signals_triggered: int
    signals: List[Signal]
    recommendation: str
    
    def format(self) -> str:
        """Format report for console output."""
        lines = []
        
        if self.alarm_triggered:
            lines.append(f"\n⚠️  EARLY WARNING - {self.date}")
            lines.append("=" * 50)
            lines.append(f"\nMultiple recovery signals elevated ({self.signals_triggered} signals):\n")
            
            for signal in self.signals:
                if signal.threshold_exceeded:
                    lines.append(f"   {signal}")
            
            lines.append(f"\n💡 {self.recommendation}")
        else:
            lines.append(f"\n✅ No Warning - {self.date}")
            lines.append("=" * 50)
            lines.append("\nAll recovery signals within normal range.")
            
            # Show any borderline signals
            borderline = [s for s in self.signals if s.severity == "medium"]
            if borderline:
                lines.append("\n   Monitoring:")
                for signal in borderline:
                    lines.append(f"   {signal}")
        
        lines.append("")
        return "\n".join(lines)


class EarlyWarningSystem:
    """Multi-signal early warning system."""
    
    def __init__(self, 
                 temp_threshold: float = 0.2,
                 hrv_drop_percent: float = 15.0,
                 rhr_increase_bpm: float = 5.0,
                 readiness_threshold: int = 65,
                 require_signals: int = 2):
        """
        Initialize early warning system.
        
        Args:
            temp_threshold: Temperature deviation threshold (°C)
            hrv_drop_percent: HRV drop threshold (%)
            rhr_increase_bpm: RHR increase threshold (bpm)
            readiness_threshold: Low readiness threshold
            require_signals: Number of signals required to trigger alarm
        """
        self.temp_threshold = temp_threshold
        self.hrv_drop_percent = hrv_drop_percent
        self.rhr_increase_bpm = rhr_increase_bpm
        self.readiness_threshold = readiness_threshold
        self.require_signals = require_signals
    
    def calculate_rolling_baseline(self, values: List[float], window: int = 14) -> float:
        """Calculate rolling baseline (median for robustness)."""
        if not values or len(values) < 3:
            return 0.0
        
        # Use last 'window' values for rolling baseline
        recent = values[-window:] if len(values) > window else values
        return statistics.median(recent)
    
    def check_temperature(self, temp_history: List[float]) -> Tuple[Signal, bool]:
        """Check for temperature elevation."""
        if not temp_history or len(temp_history) < 3:
            return Signal("Temperature", 0, 0, 0, False, "low"), False
        
        current = temp_history[-1]
        baseline = self.calculate_rolling_baseline(temp_history[:-1])
        
        # Skip if insufficient baseline data
        if baseline == 0.0:
            return Signal("Temperature deviation", current, 0, 0, False, "low"), False
        
        delta = current - baseline
        
        # Check threshold
        exceeded = abs(delta) > self.temp_threshold
        
        # Severity based on magnitude
        if abs(delta) > self.temp_threshold * 2:
            severity = "high"
        elif abs(delta) > self.temp_threshold:
            severity = "medium"
        else:
            severity = "low"
        
        signal = Signal("Temperature deviation", current, baseline, delta, exceeded, severity)
        return signal, exceeded
    
    def check_hrv(self, hrv_history: List[float]) -> Tuple[Signal, bool]:
        """Check for HRV drop."""
        if not hrv_history or len(hrv_history) < 2:
            return Signal("HRV", 0, 0, 0, False, "low"), False
        
        current = hrv_history[-1]
        baseline = self.calculate_rolling_baseline(hrv_history[:-1], window=7)
        
        if baseline == 0:
            return Signal("HRV", current, 0, 0, False, "low"), False
        
        delta = current - baseline
        percent_change = (delta / baseline) * 100
        
        # Check threshold
        exceeded = percent_change < -self.hrv_drop_percent
        
        # Severity
        if percent_change < -self.hrv_drop_percent * 1.5:
            severity = "high"
        elif percent_change < -self.hrv_drop_percent:
            severity = "medium"
        else:
            severity = "low"
        
        signal = Signal("HRV", current, baseline, delta, exceeded, severity)
        return signal, exceeded
    
    def check_rhr(self, rhr_history: List[float]) -> Tuple[Signal, bool]:
        """Check for RHR elevation."""
        if not rhr_history or len(rhr_history) < 3:
            return Signal("RHR", 0, 0, 0, False, "low"), False
        
        current = rhr_history[-1]
        baseline = self.calculate_rolling_baseline(rhr_history[:-1], window=7)
        
        # Skip if insufficient baseline data
        if baseline == 0.0:
            return Signal("Resting HR", current, 0, 0, False, "low"), False
        
        delta = current - baseline
        
        # Check threshold
        exceeded = delta > self.rhr_increase_bpm
        
        # Severity
        if delta > self.rhr_increase_bpm * 1.5:
            severity = "high"
        elif delta > self.rhr_increase_bpm:
            severity = "medium"
        else:
            severity = "low"
        
        signal = Signal("Resting HR", current, baseline, delta, exceeded, severity)
        return signal, exceeded
    
    def check_readiness(self, readiness_history: List[int]) -> Tuple[Signal, bool]:
        """Check for sustained low readiness."""
        if not readiness_history or len(readiness_history) < 2:
            return Signal("Readiness", 0, 0, 0, False, "low"), False
        
        current = readiness_history[-1]
        baseline = self.calculate_rolling_baseline(readiness_history[:-1], window=7)
        delta = current - baseline
        
        # Check threshold
        exceeded = current < self.readiness_threshold
        
        # Severity
        if current < self.readiness_threshold - 10:
            severity = "high"
        elif current < self.readiness_threshold:
            severity = "medium"
        else:
            severity = "low"
        
        signal = Signal("Readiness", current, baseline, delta, exceeded, severity)
        return signal, exceeded
    
    def analyze(self, sleep_data: List[Dict], readiness_data: List[Dict]) -> WarningReport:
        """
        Analyze data and generate early warning report.
        
        Args:
            sleep_data: List of sleep dicts (chronological order)
            readiness_data: List of readiness dicts (chronological order)
        
        Returns:
            WarningReport
        """
        # Extract time series
        readiness_by_day = {r.get("day"): r for r in readiness_data}
        
        temp_history = []
        hrv_history = []
        rhr_history = []
        readiness_history = []
        
        for sleep in sleep_data:
            day = sleep.get("day")
            
            # Temperature
            r = readiness_by_day.get(day, {})
            temp = r.get("temperature_deviation")
            if temp is not None:
                temp_history.append(temp)
            
            # HRV
            hrv = sleep.get("average_hrv")
            if hrv:
                hrv_history.append(hrv)
            
            # RHR
            rhr = sleep.get("lowest_heart_rate")
            if rhr:
                rhr_history.append(rhr)
            
            # Readiness
            if r and r.get("score"):
                readiness_history.append(r["score"])
        
        # Check all signals
        temp_signal, temp_triggered = self.check_temperature(temp_history)
        hrv_signal, hrv_triggered = self.check_hrv(hrv_history)
        rhr_signal, rhr_triggered = self.check_rhr(rhr_history)
        readiness_signal, readiness_triggered = self.check_readiness(readiness_history)
        
        signals = [temp_signal, hrv_signal, rhr_signal, readiness_signal]
        signals_triggered = sum([temp_triggered, hrv_triggered, rhr_triggered, readiness_triggered])
        
        alarm = signals_triggered >= self.require_signals
        
        # Generate recommendation
        if alarm:
            triggered_names = [s.name for s in signals if s.threshold_exceeded]
            if "Temperature" in triggered_names[0]:
                recommendation = "Consider: Rest day, monitor for illness symptoms, extra sleep"
            elif "HRV" in triggered_names[0] or "Resting HR" in triggered_names[0]:
                recommendation = "Consider: Reduce training intensity, focus on recovery, evaluate stress"
            elif "Readiness" in triggered_names[0]:
                recommendation = "Consider: Light activity only, prioritize sleep, reduce stressors"
            else:
                recommendation = "Consider: Rest day, monitor symptoms, consult health professional if persists"
        else:
            recommendation = "All clear. Proceed with normal activity."
        
        target_date = sleep_data[-1].get("day") if sleep_data else datetime.now().strftime("%Y-%m-%d")
        
        return WarningReport(
            date=target_date,
            alarm_triggered=alarm,
            signals_triggered=signals_triggered,
            signals=signals,
            recommendation=recommendation
        )


def main():
    parser = argparse.ArgumentParser(description="Oura Early Warning System")
    parser.add_argument("--days", type=int, default=14, help="Days to analyze (for rolling baseline)")
    parser.add_argument("--temp-threshold", type=float, default=0.2, help="Temperature deviation threshold (°C)")
    parser.add_argument("--hrv-drop", type=float, default=15.0, help="HRV drop threshold (%)")
    parser.add_argument("--rhr-increase", type=float, default=5.0, help="RHR increase threshold (bpm)")
    parser.add_argument("--readiness-threshold", type=int, default=65, help="Low readiness threshold")
    parser.add_argument("--require-signals", type=int, default=2, help="Signals required to trigger alarm")
    parser.add_argument("--token", help="Oura API token")
    
    args = parser.parse_args()
    
    try:
        client = OuraClient(args.token)
        
        end_date = datetime.now().strftime("%Y-%m-%d")
        start_date = (datetime.now() - timedelta(days=args.days)).strftime("%Y-%m-%d")
        
        sleep_data = client.get_sleep(start_date, end_date)
        readiness_data = client.get_readiness(start_date, end_date)
        
        if not sleep_data:
            print("No data available")
            sys.exit(1)
        
        # Initialize early warning system
        ews = EarlyWarningSystem(
            temp_threshold=args.temp_threshold,
            hrv_drop_percent=args.hrv_drop,
            rhr_increase_bpm=args.rhr_increase,
            readiness_threshold=args.readiness_threshold,
            require_signals=args.require_signals
        )
        
        # Analyze
        report = ews.analyze(sleep_data, readiness_data)
        
        # Output
        print(report.format())
        
        # Exit code indicates alarm state
        sys.exit(1 if report.alarm_triggered else 0)
    
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
