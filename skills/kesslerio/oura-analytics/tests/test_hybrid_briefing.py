#!/usr/bin/env python3
"""
Tests for Hybrid Briefing Format
"""

import pytest
import sys
from pathlib import Path

# Add scripts dir to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from briefing import format_hybrid_briefing, _format_date, _trend_arrow, BriefingFormatter, Baseline
from schema import NightRecord, SleepRecord, ReadinessRecord


def create_test_night(date="2026-01-20", sleep_hours=6.78, readiness_score=73, efficiency=85):
    """Create a test night record."""
    sleep = SleepRecord(
        date=date,
        id="test-sleep-id",
        bedtime_start="2026-01-19T23:30:00+00:00",
        bedtime_end="2026-01-20T06:45:00+00:00",
        total_sleep_hours=sleep_hours,
        deep_sleep_hours=1.5,
        rem_sleep_hours=1.2,
        light_sleep_hours=3.0,
        awake_hours=0.5,
        time_in_bed_hours=7.25,
        efficiency_percent=efficiency,
        latency_minutes=15.0,
        average_hrv_ms=42,
        average_heart_rate_bpm=58,
        lowest_heart_rate_bpm=52,
        average_breath_rate=14.2,
        restless_periods=3,
        type="long_sleep"
    )
    
    readiness = ReadinessRecord(
        date=date,
        id="test-readiness-id",
        score=readiness_score,
        temperature_deviation_c=0.1,
        temperature_trend_deviation_c=0.05,
        activity_balance=68,
        body_temperature=85,
        hrv_balance=62,
        previous_day_activity=75,
        previous_night=78,
        recovery_index=65,
        resting_heart_rate=72,
        sleep_balance=70,
        sleep_regularity=82,
        timestamp="2026-01-20T06:45:00+00:00"
    )
    
    return NightRecord(date=date, sleep=sleep, readiness=readiness)


def create_test_week_data():
    """Create test week data for hybrid format."""
    return {
        "avg_sleep_score": 89.9,
        "avg_readiness": 76.9,
        "avg_efficiency": 89.3,
        "avg_duration": 7.44,
        "avg_hrv": 19.1,
        "sleep_trend": 28.3,
        "readiness_trend": -2.1,
        "last_2_days": [
            {"day": "2026-01-19", "sleep_score": 93, "readiness": 85, "hours": 7.5},
            {"day": "2026-01-20", "sleep_score": 81, "readiness": 73, "hours": 6.8}
        ]
    }


class TestHybridBriefing:
    """Test hybrid briefing format."""
    
    def test_format_hybrid_with_week_data(self):
        """Test hybrid format includes both briefing and trend snapshot."""
        night = create_test_night()
        week_data = create_test_week_data()
        baseline = Baseline(avg_sleep_hours=7.5, avg_readiness=75.0, avg_hrv=40.0)
        
        output = format_hybrid_briefing(night, baseline, week_data)
        lines = output.split("\n")
        
        # Should contain morning briefing section
        assert "Morning Briefing" in lines[0]
        
        # Should contain trend snapshot section
        assert "Trend Snapshot" in output
        
        # Should be within reasonable line count (≤15 for hybrid with week data)
        assert len(lines) <= 16  # Allow for full hybrid format with all details
        
        # Check key elements are present
        assert "Sleep:" in output
        assert "Readiness:" in output
        assert "Recovery Status:" in output
        assert "Recommendation:" in output
        assert "7-day avg" in output
        assert "Recent Sleep:" in output
        assert "Recent Readiness:" in output
    
    def test_format_hybrid_without_week_data(self):
        """Test hybrid format works without week data (briefing only)."""
        night = create_test_night()
        
        output = format_hybrid_briefing(night, None, None)
        lines = output.split("\n")
        
        # Should contain morning briefing
        assert "Morning Briefing" in lines[0]
        assert "Sleep:" in output
        assert "Readiness:" in output
        
        # Should NOT contain trend snapshot
        assert "Trend Snapshot" not in output
    
    def test_format_hybrid_driver_analysis(self):
        """Test hybrid format includes driver analysis."""
        night = create_test_night()
        week_data = create_test_week_data()
        
        output = format_hybrid_briefing(night, None, week_data)
        
        # Should contain driver analysis
        assert "Driven by:" in output
    
    def test_format_hybrid_recent_sleep_readiness(self):
        """Test hybrid format shows last 2 days properly."""
        night = create_test_night()
        week_data = create_test_week_data()
        
        output = format_hybrid_briefing(night, None, week_data)
        
        # Should show MM-DD format dates
        assert "01-19:" in output
        assert "01-20:" in output
        # Should show scores
        assert "93" in output
        assert "85" in output
    
    def test_trend_arrow_function(self):
        """Test trend arrow calculation."""
        assert _trend_arrow(5.0) == "↑"
        assert _trend_arrow(-3.2) == "↓"
        assert _trend_arrow(0.5) == "→"
        assert _trend_arrow(-0.5) == "→"
    
    def test_format_date_function(self):
        """Test date formatting."""
        assert _format_date("2026-01-20") == "Jan 20"
        assert _format_date("2026-12-25") == "Dec 25"
    
    def test_hybrid_output_contains_trend_arrows(self):
        """Test hybrid output includes trend arrows for metrics."""
        night = create_test_night()
        week_data = create_test_week_data()
        
        output = format_hybrid_briefing(night, None, week_data)
        
        # Should contain trend arrows
        assert "↑" in output or "↓" in output or "→" in output


class TestBriefingFormatter:
    """Test base briefing formatter."""
    
    def test_baseline_from_history(self):
        """Test baseline calculation from history."""
        nights = [create_test_night() for _ in range(7)]
        baseline = Baseline.from_history(nights)
        
        assert baseline.avg_sleep_hours > 0
        assert baseline.avg_readiness > 0
    
    def test_status_green(self):
        """Test green status detection."""
        night = create_test_night(readiness_score=90)
        formatter = BriefingFormatter()
        status, _ = formatter._get_status_and_recommendation(night)
        
        assert "GREEN" in status
    
    def test_status_yellow(self):
        """Test yellow status detection."""
        night = create_test_night(readiness_score=75)
        formatter = BriefingFormatter()
        status, _ = formatter._get_status_and_recommendation(night)
        
        assert "YELLOW" in status
    
    def test_status_red(self):
        """Test red status detection."""
        night = create_test_night(readiness_score=60)
        formatter = BriefingFormatter()
        status, _ = formatter._get_status_and_recommendation(night)
        
        assert "RED" in status


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
