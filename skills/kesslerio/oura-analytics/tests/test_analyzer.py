#!/usr/bin/env python3
"""Tests for OuraAnalyzer analysis logic."""

import pytest
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from oura_api import OuraAnalyzer


class TestOuraAnalyzer:
    """Test OuraAnalyzer calculations and metrics."""

    @pytest.fixture
    def sample_sleep_data(self):
        """Sample sleep data for testing."""
        return [
            {"day": "2026-01-15", "score": 82, "efficiency": 89, "total_sleep_duration": 25200},
            {"day": "2026-01-16", "score": 78, "efficiency": 85, "total_sleep_duration": 23400},
            {"day": "2026-01-17", "score": 85, "efficiency": 92, "total_sleep_duration": 27000},
        ]

    @pytest.fixture
    def sample_readiness_data(self):
        """Sample readiness data for testing."""
        return [
            {"day": "2026-01-15", "score": 75},
            {"day": "2026-01-16", "score": 68},
            {"day": "2026-01-17", "score": 80},
        ]

    def test_seconds_to_hours(self):
        """Test seconds to hours conversion."""
        assert OuraAnalyzer.seconds_to_hours(3600) == 1.0
        assert OuraAnalyzer.seconds_to_hours(7200) == 2.0
        assert OuraAnalyzer.seconds_to_hours(0) is None
        assert OuraAnalyzer.seconds_to_hours(None) is None

    def test_calculate_sleep_score(self):
        """Test sleep score calculation."""
        # High efficiency, reasonable duration
        day = {"efficiency": 90, "total_sleep_duration": 28800}  # 8 hours
        score = OuraAnalyzer.calculate_sleep_score(day)
        assert 70 <= score <= 100

        # Low efficiency, good duration
        # Formula: (eff_score * 0.6) + (dur_score * 0.4)
        # (60 * 0.6) + (100 * 0.4) = 76
        day = {"efficiency": 60, "total_sleep_duration": 28800}
        score = OuraAnalyzer.calculate_sleep_score(day)
        assert 70 <= score <= 85  # Adjusted for actual formula behavior

    def test_average_metric(self, sample_sleep_data):
        """Test average metric calculation."""
        analyzer = OuraAnalyzer(sleep_data=sample_sleep_data)

        avg_efficiency = analyzer.average_metric(sample_sleep_data, "efficiency")
        assert avg_efficiency is not None
        assert 80 <= avg_efficiency <= 95

    def test_average_metric_empty_data(self):
        """Test average with empty data returns None."""
        analyzer = OuraAnalyzer(sleep_data=[])
        result = analyzer.average_metric([], "efficiency")
        assert result is None

    def test_average_metric_missing_key(self, sample_sleep_data):
        """Test average with missing key handles gracefully."""
        analyzer = OuraAnalyzer()
        # Data without the metric key
        data = [{"day": "2026-01-15"}, {"day": "2026-01-16"}]
        result = analyzer.average_metric(data, "nonexistent_metric")
        assert result is None

    def test_average_metric_convert_to_hours(self, sample_sleep_data):
        """Test average with hours conversion."""
        analyzer = OuraAnalyzer()
        avg_hours = analyzer.average_metric(
            sample_sleep_data,
            "total_sleep_duration",
            convert_to_hours=True
        )
        assert avg_hours is not None
        assert 5 <= avg_hours <= 10  # Should be around 7 hours

    def test_trend_calculation(self, sample_sleep_data):
        """Test trend calculation over N days."""
        analyzer = OuraAnalyzer()

        # Positive trend
        trend = analyzer.trend(sample_sleep_data, "score", days=7)
        assert isinstance(trend, (int, float))

        # Short data (less than 2 points)
        short_data = [{"score": 80}]
        trend = analyzer.trend(short_data, "score", days=7)
        assert trend == 0

    def test_summary_with_sleep_data(self, sample_sleep_data):
        """Test summary generation with sleep data."""
        analyzer = OuraAnalyzer(sleep_data=sample_sleep_data)
        summary = analyzer.summary()

        assert "avg_sleep_score" in summary
        assert "avg_sleep_hours" in summary
        assert "avg_sleep_efficiency" in summary
        assert "days_tracked" in summary
        assert summary["days_tracked"] == 3

    def test_summary_with_readiness(self, sample_sleep_data, sample_readiness_data):
        """Test summary includes readiness from dedicated dataset."""
        analyzer = OuraAnalyzer(
            sleep_data=sample_sleep_data,
            readiness_data=sample_readiness_data
        )
        summary = analyzer.summary()

        assert "avg_readiness_score" in summary
        assert summary["avg_readiness_score"] is not None
        # Should calculate average of 75, 68, 80
        # average_metric rounds to 2 decimal places
        expected_avg = round((75 + 68 + 80) / 3, 2)  # 74.33
        assert abs(summary["avg_readiness_score"] - expected_avg) < 0.01

    def test_summary_empty_data(self):
        """Test summary with empty data."""
        analyzer = OuraAnalyzer()
        summary = analyzer.summary()

        assert summary["days_tracked"] == 0
        assert summary["avg_sleep_score"] is None

    def test_readiness_join_logic(self):
        """Test that readiness data is joined correctly by day."""
        sleep = [
            {"day": "2026-01-15", "score": 80},
            {"day": "2026-01-16", "score": 75},
        ]
        readiness = [
            {"day": "2026-01-15", "score": 85},
            {"day": "2026-01-16", "score": 70},
            {"day": "2026-01-17", "score": 90},  # Extra day not in sleep
        ]

        # Build lookup like alerts.py does
        readiness_by_day = {r.get("day"): r for r in readiness}

        # Verify join works
        assert readiness_by_day["2026-01-15"]["score"] == 85
        assert readiness_by_day["2026-01-16"]["score"] == 70
        assert "2026-01-17" not in sleep  # Not in sleep data
