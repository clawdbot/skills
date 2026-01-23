#!/usr/bin/env python3
"""Tests for alert detection logic."""

import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

# Import the check_thresholds function from alerts
import importlib.util
spec = importlib.util.spec_from_file_location("alerts", Path(__file__).resolve().parent.parent / "scripts" / "alerts.py")
alerts_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alerts_module)

check_thresholds = alerts_module.check_thresholds


class TestAlertLogic:
    """Test alert detection and threshold checking."""

    @pytest.fixture
    def sample_sleep_data(self):
        """Sample sleep data for testing."""
        return [
            {"day": "2026-01-15", "efficiency": 85, "total_sleep_duration": 25200},
            {"day": "2026-01-16", "efficiency": 75, "total_sleep_duration": 21600},  # Low efficiency
            {"day": "2026-01-17", "efficiency": 90, "total_sleep_duration": 28800},  # Good day
        ]

    @pytest.fixture
    def sample_readiness_data(self):
        """Sample readiness data for testing."""
        return [
            {"day": "2026-01-15", "score": 70},  # Below threshold
            {"day": "2026-01-16", "score": 55},  # Below threshold
            {"day": "2026-01-17", "score": 85},  # Above threshold
        ]

    def test_no_alerts_when_all_above_threshold(self, sample_sleep_data, sample_readiness_data):
        """Test no alerts when all metrics are above thresholds."""
        thresholds = {"readiness": 50, "efficiency": 70, "sleep_hours": 5}

        result = check_thresholds(sample_sleep_data, sample_readiness_data, thresholds)

        assert len(result) == 0

    def test_readiness_alert_fires(self, sample_sleep_data, sample_readiness_data):
        """Test readiness alerts fire when below threshold."""
        thresholds = {"readiness": 60, "efficiency": 70, "sleep_hours": 5}

        result = check_thresholds(sample_sleep_data, sample_readiness_data, thresholds)

        # Should have alerts for 2026-01-15 (70 >= 60, so not alert)
        # and 2026-01-16 (55 < 60, so alert)
        alert_dates = [r["date"] for r in result]
        assert "2026-01-16" in alert_dates

        # Check the alert message
        alert_16 = next(r for r in result if r["date"] == "2026-01-16")
        readiness_alerts = [a for a in alert_16["alerts"] if "Readiness" in a]
        assert len(readiness_alerts) == 1
        assert "55" in readiness_alerts[0]

    def test_efficiency_alert_fires(self, sample_sleep_data, sample_readiness_data):
        """Test efficiency alerts fire when below threshold."""
        thresholds = {"readiness": 50, "efficiency": 80, "sleep_hours": 5}

        result = check_thresholds(sample_sleep_data, sample_readiness_data, thresholds)

        # 2026-01-15 has 85% efficiency (no alert)
        # 2026-01-16 has 75% efficiency (alert)
        # 2026-01-17 has 90% efficiency (no alert)
        alert_dates = [r["date"] for r in result]
        assert "2026-01-16" in alert_dates

    def test_sleep_duration_alert_fires(self, sample_sleep_data, sample_readiness_data):
        """Test sleep duration alerts fire when below threshold."""
        thresholds = {"readiness": 50, "efficiency": 70, "sleep_hours": 8}

        result = check_thresholds(sample_sleep_data, sample_readiness_data, thresholds)

        # 2026-01-16 has 21600s = 6h (below 8h threshold)
        alert_dates = [r["date"] for r in result]
        assert "2026-01-16" in alert_dates

        alert_16 = next(r for r in result if r["date"] == "2026-01-16")
        sleep_alerts = [a for a in alert_16["alerts"] if "Sleep" in a]
        assert len(sleep_alerts) == 1

    def test_no_false_positive_for_missing_readiness(self):
        """Test that missing readiness data does NOT trigger alert.

        This was a bug: alerts.py had `day.get("readiness", {}).get("score", 100)`
        which silently never fired because 100 >= any threshold.
        """
        sleep = [{"day": "2026-01-15", "efficiency": 85, "total_sleep_duration": 25200}]
        readiness = []  # No readiness data

        thresholds = {"readiness": 60, "efficiency": 70, "sleep_hours": 5}

        result = check_thresholds(sleep, readiness, thresholds)

        # Should NOT add "Readiness N/A" alert
        assert len(result) == 0

    def test_multiple_alerts_same_day(self, sample_sleep_data, sample_readiness_data):
        """Test multiple alerts can fire for the same day."""
        # Create a day with multiple issues
        sleep = [{"day": "2026-01-16", "efficiency": 50, "total_sleep_duration": 18000}]
        readiness = [{"day": "2026-01-16", "score": 30}]

        thresholds = {"readiness": 60, "efficiency": 80, "sleep_hours": 7}

        result = check_thresholds(sleep, readiness, thresholds)

        assert len(result) == 1
        alert = result[0]
        assert alert["date"] == "2026-01-16"
        # Should have 3 alerts: readiness, efficiency, sleep
        assert len(alert["alerts"]) == 3

    def test_threshold_defaults(self):
        """Test that threshold defaults work correctly."""
        sleep = [{"day": "2026-01-16", "efficiency": 50, "total_sleep_duration": 18000}]
        readiness = [{"day": "2026-01-16", "score": 30}]

        # Empty thresholds should use defaults: readiness=60, efficiency=80, sleep_hours=7
        result = check_thresholds(sleep, readiness, {})

        assert len(result) == 1  # All 3 metrics below defaults

    def test_readiness_join_by_day(self, sample_sleep_data, sample_readiness_data):
        """Test that readiness is correctly joined to sleep by day."""
        thresholds = {"readiness": 65, "efficiency": 70, "sleep_hours": 5}

        result = check_thresholds(sample_sleep_data, sample_readiness_data, thresholds)

        # 2026-01-15: readiness 70 >= 65 (no alert)
        # 2026-01-16: readiness 55 < 65 (alert)
        # 2026-01-17: readiness 85 >= 65 (no alert)
        alert_dates = [r["date"] for r in result]
        assert "2026-01-16" in alert_dates
        assert "2026-01-15" not in alert_dates
        assert "2026-01-17" not in alert_dates

    def test_empty_sleep_data(self, sample_readiness_data):
        """Test handling of empty sleep data."""
        result = check_thresholds([], sample_readiness_data, {"readiness": 60})

        assert result == []

    def test_empty_readiness_data(self, sample_sleep_data):
        """Test handling of empty readiness data."""
        result = check_thresholds(sample_sleep_data, [], {"readiness": 60})

        # Should not alert for readiness (data pending)
        # May still alert for efficiency/sleep
        efficiency_alerts = []
        for alert in result:
            efficiency_alerts.extend([a for a in alert["alerts"] if "Efficiency" in a])

        # Only 2026-01-16 has low efficiency
        assert len(efficiency_alerts) == 1
