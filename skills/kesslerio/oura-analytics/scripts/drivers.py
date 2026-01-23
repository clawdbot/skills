#!/usr/bin/env python3
"""
Driver Analysis - Identify what's affecting your scores

Analyzes sub-metrics to explain why readiness or sleep scores are high/low.
Provides actionable insights based on which components deviate from baseline.
"""

from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Driver:
    """A factor contributing to score deviation."""
    metric: str
    value: float
    baseline: float
    delta: float
    impact: str  # "positive" | "negative" | "neutral"
    severity: str  # "high" | "medium" | "low"
    
    def __str__(self) -> str:
        emoji = "✅" if self.impact == "positive" else "⚠️" if self.impact == "negative" else "➡️"
        sign = "+" if self.delta > 0 else ""
        return f"{emoji} {self.metric}: {self.value} ({sign}{self.delta:.1f} vs baseline)"


class DriverAnalyzer:
    """Analyze sub-metrics to identify score drivers."""
    
    def __init__(self, baseline: Optional[Dict] = None):
        """
        Initialize with optional baseline values.
        
        Args:
            baseline: Dict with baseline values for each metric
        """
        self.baseline = baseline or {
            "sleep_hours": 7.5,
            "efficiency": 85.0,
            "deep_sleep": 1.5,
            "rem_sleep": 1.8,
            "hrv": 40.0,
            "rhr": 60.0,
            "readiness": 75.0,
            "temperature_deviation": 0.0
        }
    
    def analyze_sleep_drivers(self, sleep_data: Dict) -> List[Driver]:
        """
        Analyze what's driving sleep score.
        
        Args:
            sleep_data: Sleep data dict from Oura API
        
        Returns:
            List of Driver objects, sorted by impact
        """
        drivers = []
        
        # Duration
        duration_hours = sleep_data.get("total_sleep_duration", 0) / 3600 if sleep_data.get("total_sleep_duration") else 0
        if duration_hours > 0:
            baseline = self.baseline.get("sleep_hours", 7.5)
            delta = duration_hours - baseline
            impact = self._classify_impact(delta, thresholds=[0.5, 1.0])
            severity = self._classify_severity(abs(delta), thresholds=[0.5, 1.0])
            drivers.append(Driver("Sleep Duration", duration_hours, baseline, delta, impact, severity))
        
        # Efficiency
        efficiency = sleep_data.get("efficiency")
        if efficiency:
            baseline = self.baseline.get("efficiency", 85.0)
            delta = efficiency - baseline
            impact = self._classify_impact(delta, thresholds=[3, 5])
            severity = self._classify_severity(abs(delta), thresholds=[3, 5])
            drivers.append(Driver("Efficiency", efficiency, baseline, delta, impact, severity))
        
        # Deep sleep
        deep_sleep_hours = sleep_data.get("deep_sleep_duration", 0) / 3600 if sleep_data.get("deep_sleep_duration") else 0
        if deep_sleep_hours > 0:
            baseline = self.baseline.get("deep_sleep", 1.5)
            delta = deep_sleep_hours - baseline
            impact = self._classify_impact(delta, thresholds=[0.3, 0.5])
            severity = self._classify_severity(abs(delta), thresholds=[0.3, 0.5])
            drivers.append(Driver("Deep Sleep", deep_sleep_hours, baseline, delta, impact, severity))
        
        # REM sleep
        rem_sleep_hours = sleep_data.get("rem_sleep_duration", 0) / 3600 if sleep_data.get("rem_sleep_duration") else 0
        if rem_sleep_hours > 0:
            baseline = self.baseline.get("rem_sleep", 1.8)
            delta = rem_sleep_hours - baseline
            impact = self._classify_impact(delta, thresholds=[0.3, 0.5])
            severity = self._classify_severity(abs(delta), thresholds=[0.3, 0.5])
            drivers.append(Driver("REM Sleep", rem_sleep_hours, baseline, delta, impact, severity))
        
        # Sort by severity and impact (negatives first, high severity first)
        # Lower sort values come first, so negative=0, positive=1; high=0, medium=1, low=2
        severity_order = {"high": 0, "medium": 1, "low": 2}
        impact_order = {"negative": 0, "neutral": 1, "positive": 2}
        drivers.sort(key=lambda d: (impact_order.get(d.impact, 1), severity_order.get(d.severity, 1), -abs(d.delta)))
        return drivers
    
    def analyze_readiness_drivers(self, sleep_data: Dict, readiness_data: Dict) -> List[Driver]:
        """
        Analyze what's driving readiness score.
        
        Args:
            sleep_data: Sleep data dict
            readiness_data: Readiness data dict
        
        Returns:
            List of Driver objects, sorted by impact
        """
        drivers = []
        
        # Sleep duration (affects readiness)
        duration_hours = sleep_data.get("total_sleep_duration", 0) / 3600 if sleep_data.get("total_sleep_duration") else 0
        if duration_hours > 0:
            baseline = self.baseline.get("sleep_hours", 7.5)
            delta = duration_hours - baseline
            impact = self._classify_impact(delta, thresholds=[0.5, 1.0])
            severity = self._classify_severity(abs(delta), thresholds=[0.5, 1.0])
            drivers.append(Driver("Sleep Duration", duration_hours, baseline, delta, impact, severity))
        
        # HRV
        hrv = sleep_data.get("average_hrv")
        if hrv:
            baseline = self.baseline.get("hrv", 40.0)
            delta = hrv - baseline
            impact = self._classify_impact(delta, thresholds=[5, 10])
            severity = self._classify_severity(abs(delta), thresholds=[5, 10])
            drivers.append(Driver("HRV", hrv, baseline, delta, impact, severity))
        
        # Resting Heart Rate
        rhr = sleep_data.get("lowest_heart_rate")
        if rhr:
            baseline = self.baseline.get("rhr", 60.0)
            delta = rhr - baseline
            # For RHR, lower is better (inverse impact)
            impact = self._classify_impact(-delta, thresholds=[3, 5])
            severity = self._classify_severity(abs(delta), thresholds=[3, 5])
            drivers.append(Driver("Resting HR", rhr, baseline, delta, impact, severity))
        
        # Temperature deviation (if available)
        temp_dev = readiness_data.get("temperature_deviation")
        if temp_dev is not None:
            baseline = self.baseline.get("temperature_deviation", 0.0)
            delta = temp_dev - baseline
            impact = self._classify_impact(-abs(delta), thresholds=[0.2, 0.4])  # Any deviation is negative
            severity = self._classify_severity(abs(delta), thresholds=[0.2, 0.4])
            drivers.append(Driver("Temperature", temp_dev, baseline, delta, impact, severity))
        
        # Sort by severity and impact (negatives first, high severity first)
        severity_order = {"high": 0, "medium": 1, "low": 2}
        impact_order = {"negative": 0, "neutral": 1, "positive": 2}
        drivers.sort(key=lambda d: (impact_order.get(d.impact, 1), severity_order.get(d.severity, 1), -abs(d.delta)))
        return drivers
    
    def generate_suggestion(self, readiness_score: float, drivers: List[Driver]) -> str:
        """
        Generate actionable suggestion based on readiness score and drivers.
        
        Args:
            readiness_score: Current readiness score
            drivers: List of Driver objects
        
        Returns:
            Actionable suggestion string
        """
        # Find high-severity negative drivers
        negative_drivers = [d for d in drivers if d.impact == "negative" and d.severity in ["high", "medium"]]
        
        if readiness_score >= 85:
            if not negative_drivers:
                return "All systems optimal. Green light for intensity."
            else:
                return "Good recovery, but watch: " + ", ".join(d.metric for d in negative_drivers[:2])
        
        elif readiness_score >= 70:
            if negative_drivers:
                main_driver = negative_drivers[0].metric.lower()
                return f"Moderate recovery. Main concern: {main_driver}. Keep training light."
            else:
                return "Moderate recovery. Avoid heavy training today."
        
        else:  # < 70
            if negative_drivers:
                top_drivers = ", ".join(d.metric.lower() for d in negative_drivers[:2])
                return f"Low recovery due to: {top_drivers}. Prioritize rest."
            else:
                return "Low recovery. Consider a rest day or light activity only."
    
    def _classify_impact(self, delta: float, thresholds: List[float]) -> str:
        """Classify impact as positive, negative, or neutral."""
        if delta > thresholds[1]:
            return "positive"
        elif delta > thresholds[0]:
            return "neutral"
        elif delta < -thresholds[1]:
            return "negative"
        elif delta < -thresholds[0]:
            return "neutral"
        else:
            return "neutral"
    
    def _classify_severity(self, abs_delta: float, thresholds: List[float]) -> str:
        """Classify severity as high, medium, or low."""
        if abs_delta > thresholds[1]:
            return "high"
        elif abs_delta > thresholds[0]:
            return "medium"
        else:
            return "low"


def format_drivers_report(drivers: List[Driver], title: str = "Drivers") -> str:
    """Format drivers for console output."""
    if not drivers:
        return ""
    
    lines = [f"\n{title}:"]
    for driver in drivers[:3]:  # Top 3 drivers
        lines.append(f"   {driver}")
    
    return "\n".join(lines)
