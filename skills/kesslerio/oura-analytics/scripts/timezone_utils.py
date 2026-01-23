#!/usr/bin/env python3
"""
Timezone Utilities for Oura Analytics

Handles timezone-aware day alignment, travel detection, and DST handling.
"""

import os
import pytz
from datetime import datetime, date
from typing import Optional, Tuple, List


def get_user_timezone() -> str:
    """Get user's configured timezone or default to America/Los_Angeles."""
    return os.environ.get("USER_TIMEZONE", "America/Los_Angeles")


def get_canonical_day(utc_timestamp: str, user_tz: Optional[str] = None) -> Tuple[Optional[date], Optional[datetime]]:
    """
    Convert a UTC timestamp to the user's canonical day.

    Args:
        utc_timestamp: ISO format timestamp (e.g., "2026-01-15T00:00:00.000+00:00")
        user_tz: User's timezone (default: from USER_TIMEZONE env or America/Los_Angeles)

    Returns:
        Tuple of (date object or None, timezone-aware datetime or None)
        Returns (None, None) for invalid/missing timestamps
    """
    if user_tz is None:
        user_tz = get_user_timezone()

    # Handle empty or invalid timestamps
    if not utc_timestamp or len(utc_timestamp) < 10:
        return None, None

    try:
        # Parse the UTC timestamp
        # Handle both +00:00 and Z format
        ts_clean = utc_timestamp.replace("Z", "+00:00")
        utc_dt = datetime.fromisoformat(ts_clean)

        # Handle naive timestamps by assuming UTC
        if utc_dt.tzinfo is None:
            utc_dt = pytz.UTC.localize(utc_dt)

        # Convert to user's timezone
        user_tz_obj = pytz.timezone(user_tz)
        local_dt = utc_dt.astimezone(user_tz_obj)

        return local_dt.date(), local_dt
    except (ValueError, pytz.UnknownTimeZoneError):
        # Return None for any parsing errors
        return None, None


def get_canonical_day_from_date_str(date_str: str, user_tz: Optional[str] = None) -> Optional[date]:
    """
    Get canonical day from a date string (YYYY-MM-DD).

    For dates, we assume the date is in the user's local timezone.
    Returns None for invalid/empty dates.
    """
    if user_tz is None:
        user_tz = get_user_timezone()

    # Handle empty or invalid date strings
    if not date_str or len(date_str) < 10:
        return None

    try:
        # Parse the date as midnight in user's timezone
        user_tz_obj = pytz.timezone(user_tz)
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        local_dt = user_tz_obj.localize(dt)
        return local_dt.date()
    except (ValueError, pytz.UnknownTimeZoneError):
        return None


def is_travel_day(sleep_records: list, threshold_hours: float = 3.0, user_tz: Optional[str] = None) -> List[date]:
    """
    Detect potential travel days based on bedtime shifts.

    Args:
        sleep_records: List of sleep records with bedtime_start
        threshold_hours: Minimum hour shift to flag as potential travel
        user_tz: User's timezone (default: from USER_TIMEZONE env or America/Los_Angeles)

    Returns:
        List of dates that may be travel days
    """
    if not sleep_records or len(sleep_records) < 2:
        return []

    travel_days = []
    if user_tz is None:
        user_tz = get_user_timezone()

    # Extract bedtimes in user's local hour
    bedtimes = []
    for record in sleep_records:
        bedtime_start = record.get("bedtime_start", "")
        if not bedtime_start:
            continue

        canonical_day, local_dt = get_canonical_day(bedtime_start, user_tz)
        if local_dt:
            bedtimes.append((canonical_day, local_dt.hour + local_dt.minute / 60))

    # Need at least 3 records for meaningful travel detection
    if len(bedtimes) < 3:
        return []

    hours = [h for _, h in bedtimes]
    median_hour = sorted(hours)[len(hours) // 2]

    for day, hour in bedtimes:
        # Use min to handle the wraparound at midnight
        shift = min(abs(hour - median_hour), 24 - abs(hour - median_hour))
        if shift > threshold_hours:
            if day not in travel_days:
                travel_days.append(day)

    return travel_days


def get_sleep_for_canonical_day(sleep_data: list, target_date: date,
                                  user_tz: Optional[str] = None) -> list:
    """
    Get all sleep records that belong to a canonical day.

    Oura assigns sleep to the wake date, but sleep starting the previous
    day may still be relevant for the "night before".
    """
    if user_tz is None:
        user_tz = get_user_timezone()

    matching = []
    for record in sleep_data:
        record_day_str = record.get("day")
        if not record_day_str:
            continue

        canonical_day = get_canonical_day_from_date_str(record_day_str, user_tz)

        if canonical_day == target_date:
            matching.append(record)

    return matching


def group_by_canonical_day(data: list, timestamp_field: str = "day",
                           user_tz: Optional[str] = None) -> dict:
    """
    Group data records by canonical day.

    Args:
        data: List of records with a date field
        timestamp_field: Field name containing the date (e.g., "day" or "bedtime_start")
        user_tz: User's timezone

    Returns:
        Dict mapping date strings to lists of records
        Skips records with missing/invalid timestamps
    """
    if user_tz is None:
        user_tz = get_user_timezone()

    grouped = {}
    for record in data:
        if timestamp_field == "day":
            record_date = record.get("day", "")
            if not record_date:
                continue
            canonical = get_canonical_day_from_date_str(record_date, user_tz)
        else:
            record_ts = record.get(timestamp_field, "")
            if not record_ts:
                continue
            canonical, _ = get_canonical_day(record_ts, user_tz)

        if canonical is None:
            continue

        date_str = canonical.isoformat()
        if date_str not in grouped:
            grouped[date_str] = []
        grouped[date_str].append(record)

    return grouped


def format_localized_datetime(utc_timestamp: str, fmt: str = "%Y-%m-%d %H:%M",
                               user_tz: Optional[str] = None) -> str:
    """
    Format a UTC timestamp in user's local time.

    Args:
        utc_timestamp: ISO format timestamp
        fmt: Output format (default: "YYYY-MM-DD HH:MM")
        user_tz: User's timezone

    Returns:
        Formatted datetime string in local time, or original if invalid
    """
    _, local_dt = get_canonical_day(utc_timestamp, user_tz)
    if local_dt:
        return local_dt.strftime(fmt)
    # Fallback: return the date only
    return utc_timestamp[:10]


# Alias for backwards compatibility
get_canonical_date = get_canonical_day
