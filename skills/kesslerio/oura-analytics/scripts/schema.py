#!/usr/bin/env python3
"""
Canonical Data Schema for Oura Analytics

This module defines normalized data structures for Oura Ring data with:
- Consistent naming conventions
- Explicit units in field names
- Type hints for all fields
- Transformation functions from raw API responses

Units:
- Durations: hours (converted from seconds)
- Percentages: 0-100 scale
- Scores: 0-100 scale
- HRV: milliseconds
- Temperature: °C deviation from baseline
- Heart rate: beats per minute (bpm)
- Calories: kcal
- Distance: meters
"""

from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Optional, Dict, Any
import json


@dataclass
class SleepRecord:
    """
    Normalized sleep data for a single night.
    
    All durations are in hours (converted from Oura's seconds).
    Date represents the calendar day (wake date, not bedtime date).
    """
    # Identity
    date: str  # YYYY-MM-DD (local timezone, wake date)
    id: str    # Oura record ID
    
    # Timestamps (ISO 8601 with timezone)
    bedtime_start: str  # When user went to bed
    bedtime_end: str    # When user woke up
    
    # Sleep durations (hours)
    total_sleep_hours: float
    deep_sleep_hours: float
    rem_sleep_hours: float
    light_sleep_hours: float
    awake_hours: float
    time_in_bed_hours: float
    
    # Quality metrics
    efficiency_percent: float  # 0-100
    latency_minutes: Optional[float]  # Time to fall asleep
    
    # Physiological
    average_hrv_ms: Optional[float]
    average_heart_rate_bpm: Optional[float]
    lowest_heart_rate_bpm: Optional[float]
    average_breath_rate: Optional[float]  # breaths per minute
    
    # Metadata
    restless_periods: Optional[int]
    type: str  # "long_sleep", "late_nap", etc.
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values"""
        return {k: v for k, v in asdict(self).items() if v is not None}
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class ReadinessRecord:
    """
    Normalized readiness data for a single day.
    
    Readiness represents recovery status for the day.
    """
    # Identity
    date: str  # YYYY-MM-DD (local timezone)
    id: str    # Oura record ID
    
    # Overall score
    score: int  # 0-100
    
    # Temperature
    temperature_deviation_c: Optional[float]  # °C deviation from baseline
    temperature_trend_deviation_c: Optional[float]  # Trend deviation
    
    # Contributors (all 0-100)
    activity_balance: Optional[int]
    body_temperature: Optional[int]
    hrv_balance: Optional[int]
    previous_day_activity: Optional[int]
    previous_night: Optional[int]
    recovery_index: Optional[int]
    resting_heart_rate: Optional[int]
    sleep_balance: Optional[int]
    sleep_regularity: Optional[int]
    
    # Timestamp
    timestamp: str  # ISO 8601
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values"""
        return {k: v for k, v in asdict(self).items() if v is not None}
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class ActivityRecord:
    """
    Normalized activity data for a single day.
    
    Activity represents movement and calories for the calendar day.
    """
    # Identity
    date: str  # YYYY-MM-DD (local timezone)
    id: str    # Oura record ID
    
    # Overall
    score: int  # 0-100
    steps: int
    
    # Calories (kcal)
    active_calories: int
    total_calories: int
    target_calories: int
    
    # Activity time (hours)
    high_activity_hours: float
    medium_activity_hours: float
    low_activity_hours: float
    sedentary_hours: float
    resting_hours: float
    non_wear_hours: float
    
    # MET (metabolic equivalent)
    average_met_minutes: float
    high_activity_met_minutes: int
    medium_activity_met_minutes: int
    low_activity_met_minutes: int
    sedentary_met_minutes: int
    
    # Distance
    equivalent_walking_distance_m: int
    target_meters: int
    meters_to_target: int
    
    # Metadata
    inactivity_alerts: int
    timestamp: str  # ISO 8601
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary, excluding None values"""
        return {k: v for k, v in asdict(self).items() if v is not None}
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)


@dataclass
class NightRecord:
    """
    Unified record combining sleep, readiness, and activity for a single night/day.
    
    This is the primary data structure for analysis, joining:
    - Sleep from the night (date = wake date)
    - Readiness for the day (date = wake date)
    - Activity from the previous day (date = wake date - 1)
    
    All Optional fields may be None if data is unavailable.
    """
    # Identity
    date: str  # YYYY-MM-DD (local timezone, wake date)
    
    # Sleep (from night)
    sleep: Optional[SleepRecord] = None
    
    # Readiness (for day)
    readiness: Optional[ReadinessRecord] = None
    
    # Activity (from previous day)
    activity: Optional[ActivityRecord] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to nested dictionary"""
        result = {"date": self.date}
        if self.sleep:
            result["sleep"] = self.sleep.to_dict()
        if self.readiness:
            result["readiness"] = self.readiness.to_dict()
        if self.activity:
            result["activity"] = self.activity.to_dict()
        return result
    
    def to_json(self) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=2)


def normalize_sleep(raw: Dict[str, Any]) -> SleepRecord:
    """
    Convert raw Oura sleep API response to normalized SleepRecord.
    
    Args:
        raw: Raw sleep data from Oura API (single record from data array)
    
    Returns:
        SleepRecord with normalized units and naming
    """
    return SleepRecord(
        date=raw["day"],
        id=raw["id"],
        bedtime_start=raw["bedtime_start"],
        bedtime_end=raw["bedtime_end"],
        # Convert seconds to hours
        total_sleep_hours=raw["total_sleep_duration"] / 3600,
        deep_sleep_hours=raw.get("deep_sleep_duration", 0) / 3600,
        rem_sleep_hours=raw.get("rem_sleep_duration", 0) / 3600,
        light_sleep_hours=raw.get("light_sleep_duration", 0) / 3600,
        awake_hours=raw.get("awake_time", 0) / 3600,
        time_in_bed_hours=raw.get("time_in_bed", 0) / 3600,
        # Quality metrics
        efficiency_percent=raw.get("efficiency", 0),
        latency_minutes=raw.get("latency") / 60 if raw.get("latency") is not None else None,
        # Physiological
        average_hrv_ms=raw.get("average_hrv"),
        average_heart_rate_bpm=raw.get("average_heart_rate"),
        lowest_heart_rate_bpm=raw.get("lowest_heart_rate"),
        average_breath_rate=raw.get("average_breath"),
        # Metadata
        restless_periods=raw.get("restless_periods"),
        type=raw.get("type", "long_sleep")
    )


def normalize_readiness(raw: Dict[str, Any]) -> ReadinessRecord:
    """
    Convert raw Oura readiness API response to normalized ReadinessRecord.
    
    Args:
        raw: Raw readiness data from Oura API (single record from data array)
    
    Returns:
        ReadinessRecord with normalized units and naming
    """
    contributors = raw.get("contributors", {})
    
    return ReadinessRecord(
        date=raw["day"],
        id=raw["id"],
        score=raw["score"],
        temperature_deviation_c=raw.get("temperature_deviation"),
        temperature_trend_deviation_c=raw.get("temperature_trend_deviation"),
        # Contributors
        activity_balance=contributors.get("activity_balance"),
        body_temperature=contributors.get("body_temperature"),
        hrv_balance=contributors.get("hrv_balance"),
        previous_day_activity=contributors.get("previous_day_activity"),
        previous_night=contributors.get("previous_night"),
        recovery_index=contributors.get("recovery_index"),
        resting_heart_rate=contributors.get("resting_heart_rate"),
        sleep_balance=contributors.get("sleep_balance"),
        sleep_regularity=contributors.get("sleep_regularity"),
        timestamp=raw["timestamp"]
    )


def normalize_activity(raw: Dict[str, Any]) -> ActivityRecord:
    """
    Convert raw Oura activity API response to normalized ActivityRecord.
    
    Args:
        raw: Raw activity data from Oura API (single record from data array)
    
    Returns:
        ActivityRecord with normalized units and naming
    """
    return ActivityRecord(
        date=raw["day"],
        id=raw["id"],
        score=raw["score"],
        steps=raw["steps"],
        # Calories
        active_calories=raw["active_calories"],
        total_calories=raw["total_calories"],
        target_calories=raw["target_calories"],
        # Convert seconds to hours
        high_activity_hours=raw.get("high_activity_time", 0) / 3600,
        medium_activity_hours=raw.get("medium_activity_time", 0) / 3600,
        low_activity_hours=raw.get("low_activity_time", 0) / 3600,
        sedentary_hours=raw.get("sedentary_time", 0) / 3600,
        resting_hours=raw.get("resting_time", 0) / 3600,
        non_wear_hours=raw.get("non_wear_time", 0) / 3600,
        # MET
        average_met_minutes=raw["average_met_minutes"],
        high_activity_met_minutes=raw["high_activity_met_minutes"],
        medium_activity_met_minutes=raw["medium_activity_met_minutes"],
        low_activity_met_minutes=raw["low_activity_met_minutes"],
        sedentary_met_minutes=raw["sedentary_met_minutes"],
        # Distance
        equivalent_walking_distance_m=raw["equivalent_walking_distance"],
        target_meters=raw["target_meters"],
        meters_to_target=raw["meters_to_target"],
        # Metadata
        inactivity_alerts=raw["inactivity_alerts"],
        timestamp=raw["timestamp"]
    )


def create_night_record(
    date: str,
    sleep: Optional[Dict[str, Any]] = None,
    readiness: Optional[Dict[str, Any]] = None,
    activity: Optional[Dict[str, Any]] = None
) -> NightRecord:
    """
    Create a unified NightRecord from raw API data.
    
    Args:
        date: YYYY-MM-DD date for the night (wake date)
        sleep: Raw sleep data (optional)
        readiness: Raw readiness data (optional)
        activity: Raw activity data (optional)
    
    Returns:
        NightRecord with normalized data from all sources
    """
    return NightRecord(
        date=date,
        sleep=normalize_sleep(sleep) if sleep else None,
        readiness=normalize_readiness(readiness) if readiness else None,
        activity=normalize_activity(activity) if activity else None
    )
