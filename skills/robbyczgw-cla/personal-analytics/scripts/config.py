#!/usr/bin/env python3
"""
Configuration loader for personal-analytics skill.
"""

import json
from pathlib import Path
from typing import Dict, Optional

SKILL_DIR = Path(__file__).parent.parent
CONFIG_FILE = SKILL_DIR / "config.json"
DATA_FILE = SKILL_DIR / ".analytics_data.json"
TOPIC_CACHE_FILE = SKILL_DIR / ".topic_cache.json"


def load_config() -> Dict:
    """Load configuration from config.json."""
    if not CONFIG_FILE.exists():
        raise FileNotFoundError(
            f"Config file not found: {CONFIG_FILE}\n"
            "Copy config.example.json to config.json and customize it."
        )
    
    with open(CONFIG_FILE) as f:
        return json.load(f)


def save_config(config: Dict):
    """Save configuration to config.json."""
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)


def load_data() -> Dict:
    """Load analytics data."""
    if DATA_FILE.exists():
        with open(DATA_FILE) as f:
            return json.load(f)
    return {
        "sessions": [],
        "topic_stats": {},
        "time_stats": {
            "hourly_distribution": {},
            "daily_distribution": {}
        },
        "sentiment_stats": {
            "positive": 0,
            "neutral": 0,
            "negative": 0,
            "mixed": 0
        }
    }


def save_data(data: Dict):
    """Save analytics data."""
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def is_enabled() -> bool:
    """Check if analytics tracking is enabled."""
    try:
        config = load_config()
        return config.get("enabled", False)
    except FileNotFoundError:
        return False


def get_tracking_settings() -> Dict:
    """Get tracking settings."""
    config = load_config()
    return config.get("tracking", {})


def get_privacy_settings() -> Dict:
    """Get privacy settings."""
    config = load_config()
    return config.get("privacy", {})


def get_insights_settings() -> Dict:
    """Get insights settings."""
    config = load_config()
    return config.get("insights", {})


def get_report_settings() -> Dict:
    """Get report settings."""
    config = load_config()
    return config.get("reports", {})


def get_integration_settings(integration: str) -> Dict:
    """Get integration settings for specific integration."""
    config = load_config()
    integrations = config.get("integrations", {})
    return integrations.get(integration, {})
