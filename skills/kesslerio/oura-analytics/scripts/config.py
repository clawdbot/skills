#!/usr/bin/env python3
"""
Alert Configuration and Quality Controls

Provides debounce, hysteresis, and configurable thresholds for alerts.
"""

import yaml
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional


@dataclass
class AlertThresholds:
    """Alert threshold configuration."""
    # Readiness thresholds (0-100)
    low_threshold: int = 60
    critical_threshold: int = 45

    # Sleep thresholds (hours)
    min_hours: float = 6.5
    critical_hours: float = 5.0

    # Efficiency thresholds (percentage)
    min_efficiency: int = 80
    critical_efficiency: int = 70

    # HRV threshold (percentage drop from baseline)
    hrv_drop_percent: int = 15

    # Temperature deviation threshold (Celsius)
    temp_deviation: float = 0.3


@dataclass
class AlertConfig:
    """Main alert configuration with debounce and hysteresis."""

    # Debounce settings
    consecutive_days_required: int = 2  # Alert only after N consecutive bad days
    signals_required: int = 2  # Require N signals to alert (out of checked)

    # Cooldown to prevent alert spam
    cooldown_hours: int = 24

    # Per-category thresholds
    readiness: AlertThresholds = field(default_factory=AlertThresholds)
    sleep: AlertThresholds = field(default_factory=AlertThresholds)
    efficiency: AlertThresholds = field(default_factory=AlertThresholds)
    hrv: AlertThresholds = field(default_factory=AlertThresholds)
    temperature: AlertThresholds = field(default_factory=AlertThresholds)


@dataclass
class AlertState:
    """Track alert state to prevent spam and track acknowledgments."""

    last_alert_time: dict[str, datetime] = field(default_factory=dict)
    acknowledged: set[str] = field(default_factory=set)
    consecutive_bad_days: dict[str, int] = field(default_factory=dict)

    def should_alert(self, category: str, current_time: datetime) -> bool:
        """Check if we should alert (respects cooldown)."""
        last_time = self.last_alert_time.get(category)
        if last_time and (current_time - last_time) < timedelta(hours=24):
            return False
        return True

    def record_alert(self, category: str, current_time: datetime):
        """Record that we alerted for this category."""
        self.last_alert_time[category] = current_time

    def record_bad_day(self, category: str):
        """Record a consecutive bad day for this category."""
        current = self.consecutive_bad_days.get(category, 0)
        self.consecutive_bad_days[category] = current + 1

    def reset_bad_days(self, category: str):
        """Reset consecutive bad day counter."""
        self.consecutive_bad_days[category] = 0

    def get_consecutive_bad_days(self, category: str) -> int:
        """Get consecutive bad day count for category."""
        return self.consecutive_bad_days.get(category, 0)


class ConfigLoader:
    """Load configuration from YAML file with environment overrides."""

    DEFAULT_CONFIG_PATH = Path.home() / ".oura-analytics" / "config.yaml"

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or self.DEFAULT_CONFIG_PATH
        self._config: Optional[AlertConfig] = None

    def load(self) -> AlertConfig:
        """Load configuration from file or return defaults."""
        if self._config is not None:
            return self._config

        if not self.config_path.exists():
            self._config = AlertConfig()
            return self._config

        try:
            with open(self.config_path) as f:
                data = yaml.safe_load(f) or {}
            self._config = self._parse_config(data)
        except Exception as e:
            print(f"Warning: Failed to load config: {e}. Using defaults.")
            self._config = AlertConfig()

        return self._config

    def _parse_config(self, data: dict) -> AlertConfig:
        """Parse YAML data into AlertConfig."""
        # Parse debounce settings
        debounce = data.get("debounce", {})
        consecutive_days = debounce.get("consecutive_days_required", 2)
        signals_required = debounce.get("signals_required", 2)
        cooldown_hours = debounce.get("cooldown_hours", 24)

        # Parse thresholds
        def parse_thresholds(category: str) -> AlertThresholds:
            cat_data = data.get(category, {})
            return AlertThresholds(
                low_threshold=cat_data.get("low_threshold", 60),
                critical_threshold=cat_data.get("critical_threshold", 45),
                min_hours=cat_data.get("min_hours", 6.5),
                critical_hours=cat_data.get("critical_hours", 5.0),
                min_efficiency=cat_data.get("min_efficiency", 80),
                critical_efficiency=cat_data.get("critical_efficiency", 70),
                hrv_drop_percent=cat_data.get("hrv_drop_percent", 15),
                temp_deviation=cat_data.get("temp_deviation", 0.3),
            )

        return AlertConfig(
            consecutive_days_required=consecutive_days,
            signals_required=signals_required,
            cooldown_hours=cooldown_hours,
            readiness=parse_thresholds("readiness"),
            sleep=parse_thresholds("sleep"),
            efficiency=parse_thresholds("efficiency"),
            hrv=parse_thresholds("hrv"),
            temperature=parse_thresholds("temperature"),
        )

    def save(self, config: AlertConfig, path: Optional[Path] = None):
        """Save configuration to YAML file."""
        save_path = path or self.config_path
        save_path.parent.mkdir(parents=True, exist_ok=True)

        data = {
            "debounce": {
                "consecutive_days_required": config.consecutive_days_required,
                "signals_required": config.signals_required,
                "cooldown_hours": config.cooldown_hours,
            },
            "readiness": {
                "low_threshold": config.readiness.low_threshold,
                "critical_threshold": config.readiness.critical_threshold,
            },
            "sleep": {
                "min_hours": config.sleep.min_hours,
                "critical_hours": config.sleep.critical_hours,
            },
            "efficiency": {
                "min_efficiency": config.efficiency.min_efficiency,
                "critical_efficiency": config.efficiency.critical_efficiency,
            },
            "hrv": {
                "hrv_drop_percent": config.hrv.hrv_drop_percent,
            },
            "temperature": {
                "temp_deviation": config.temperature.temp_deviation,
            },
        }

        with open(save_path, "w") as f:
            yaml.dump(data, f, default_flow_style=False)

        self._config = config


def check_thresholds_with_quality(
    sleep_data: list,
    readiness_data: list,
    config: AlertConfig,
    state: Optional[AlertState] = None,
) -> list:
    """Check thresholds with debounce and hysteresis.

    Args:
        sleep_data: List of sleep records
        readiness_data: List of readiness records
        config: AlertConfig with thresholds and debounce settings
        state: Optional AlertState for tracking

    Returns:
        List of alert dictionaries
    """
    if state is None:
        state = AlertState()

    # Build lookups by day
    readiness_by_day = {r.get("day"): r for r in readiness_data}

    alerts = []

    for day in sleep_data:
        date = day.get("day")
        category_issues = []
        bad_categories = set()

        # Check readiness
        readiness_record = readiness_by_day.get(date)
        readiness_score = readiness_record.get("score") if readiness_record else None
        if readiness_score and readiness_score < config.readiness.low_threshold:
            category_issues.append(("readiness", readiness_score))
            bad_categories.add("readiness")

        # Check efficiency
        efficiency = day.get("efficiency", 100)
        if efficiency < config.efficiency.min_efficiency:
            category_issues.append(("efficiency", efficiency))
            bad_categories.add("efficiency")

        # Check sleep duration
        duration_hours = day.get("total_sleep_duration", 0) / 3600
        if duration_hours and duration_hours < config.sleep.min_hours:
            category_issues.append(("sleep", duration_hours))
            bad_categories.add("sleep")

        # Reset consecutive counter for categories that improved
        for cat in ["readiness", "efficiency", "sleep"]:
            if cat not in bad_categories:
                state.reset_bad_days(cat)

        # Apply debounce: require consecutive bad days
        for category, value in category_issues:
            state.record_bad_day(category)

            consecutive = state.get_consecutive_bad_days(category)
            if consecutive < config.consecutive_days_required:
                continue

            # Check cooldown using config value
            last_time = state.last_alert_time.get(category)
            if last_time:
                cooldown = timedelta(hours=config.cooldown_hours)
                if (datetime.now() - last_time) < cooldown:
                    continue

            # Create alert message
            if category == "readiness":
                msg = f"Readiness {value}"
            elif category == "efficiency":
                msg = f"Efficiency {value}%"
            else:
                msg = f"Sleep {value:.1f}h"

            alerts.append({
                "date": date,
                "alerts": [msg],
                "consecutive_days": consecutive,
            })

            state.record_alert(category, datetime.now())

    return alerts


def main():
    """CLI for alert configuration."""
    import argparse

    parser = argparse.ArgumentParser(description="Manage Oura alert configuration")
    parser.add_argument("--config", type=str, help="Path to config file")
    parser.add_argument("--show", action="store_true", help="Show current config")
    parser.add_argument("--reset", action="store_true", help="Reset to defaults")

    args = parser.parse_args()

    loader = ConfigLoader(Path(args.config) if args.config else None)

    if args.reset:
        config = AlertConfig()
        loader.save(config)
        print("Configuration reset to defaults.")
        return

    config = loader.load()

    if args.show:
        print("Alert Configuration:")
        print(f"  Consecutive days required: {config.consecutive_days_required}")
        print(f"  Cooldown hours: {config.cooldown_hours}")
        print(f"  Readiness threshold: {config.readiness.low_threshold}")
        print(f"  Sleep minimum hours: {config.sleep.min_hours}")
        print(f"  Efficiency minimum: {config.efficiency.min_efficiency}%")


if __name__ == "__main__":
    main()
