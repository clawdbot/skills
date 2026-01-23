#!/usr/bin/env python3
"""Debug Oura API response structure."""

import os
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from oura_api import OuraClient

# Load token
token = os.environ.get("OURA_API_TOKEN")
if not token:
    print("Error: OURA_API_TOKEN not set")
    sys.exit(1)

client = OuraClient(token=token)

print("=" * 60)
print("DEBUG: Oura API Response Structure")
print("=" * 60)

# Get sleep data
print("\n📊 SLEEP DATA:")
sleep = client.get_sleep(start_date="2026-01-17", end_date="2026-01-20")
if sleep:
    print(f"Found {len(sleep)} records")
    for i, day in enumerate(sleep[:2]):  # Show first 2
        print(f"\nDay {i+1}: {day.get('day')}")
        print(f"  All keys: {list(day.keys())}")
        print(f"  score: {day.get('score')}")
        print(f"  efficiency: {day.get('efficiency')}")
        print(f"  total_sleep_duration: {day.get('total_sleep_duration')}")
else:
    print("No sleep data found!")

# Get readiness data
print("\n⚡ READINESS DATA:")
readiness = client.get_readiness(start_date="2026-01-17", end_date="2026-01-20")
if readiness:
    print(f"Found {len(readiness)} records")
    for i, day in enumerate(readiness[:2]):  # Show first 2
        print(f"\nDay {i+1}: {day.get('day')}")
        print(f"  All keys: {list(day.keys())}")
        print(f"  score: {day.get('score')}")
        print(f"  contributors: {day.get('contributors')}")
else:
    print("No readiness data found!")

# Get daily_sleep (alternative endpoint)
print("\n📊 DAILY_SLEEP (alternative):")
daily_sleep = client.get_daily_sleep(start_date="2026-01-17", end_date="2026-01-20")
if daily_sleep:
    print(f"Found {len(daily_sleep)} records")
    for i, day in enumerate(daily_sleep[:2]):
        print(f"\nDay {i+1}: {day.get('day')}")
        print(f"  All keys: {list(day.keys())}")
        print(f"  score: {day.get('score')}")
else:
    print("No daily_sleep data found!")

print("\n" + "=" * 60)
