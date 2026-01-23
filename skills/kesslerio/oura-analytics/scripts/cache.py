#!/usr/bin/env python3
"""Simple file-based cache for Oura API data."""

import json
from pathlib import Path
from typing import Optional
from datetime import datetime


class OuraCache:
    """File-based cache for Oura data (sleep, readiness, activity)."""

    def __init__(self, cache_dir: Optional[Path] = None):
        """Initialize cache with optional custom directory."""
        if cache_dir is None:
            cache_dir = Path.home() / ".oura-analytics" / "cache"
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def get(self, endpoint: str, date: str) -> Optional[list]:
        """
        Get cached data for endpoint and date.

        Args:
            endpoint: API endpoint (sleep, readiness, activity)
            date: ISO date string (YYYY-MM-DD)

        Returns:
            Cached data list (Oura API returns data: []) or None if not cached
        """
        cache_file = self._get_cache_path(endpoint, date)
        if not cache_file.exists():
            return None

        try:
            with open(cache_file, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return None

    def set(self, endpoint: str, date: str, data: list) -> None:
        """
        Cache data for endpoint and date.

        Args:
            endpoint: API endpoint (sleep, readiness, activity)
            date: ISO date string (YYYY-MM-DD)
            data: Data to cache
        """
        cache_file = self._get_cache_path(endpoint, date)
        cache_file.parent.mkdir(parents=True, exist_ok=True)

        with open(cache_file, "w") as f:
            json.dump(data, f, indent=2)

    def clear(self, endpoint: Optional[str] = None) -> int:
        """
        Clear cache for specific endpoint or all endpoints.

        Args:
            endpoint: API endpoint to clear, or None to clear all

        Returns:
            Number of files deleted
        """
        if endpoint:
            target_dir = self.cache_dir / endpoint
            if not target_dir.exists():
                return 0
            files = list(target_dir.glob("*.json"))
        else:
            files = list(self.cache_dir.glob("*/*.json"))

        for f in files:
            f.unlink()
        
        # Also reset sync state
        sync_state_file = self.cache_dir / "sync_state.json"
        if sync_state_file.exists():
            try:
                sync_state = json.loads(sync_state_file.read_text())
                if endpoint:
                    # Clear specific endpoint
                    sync_state.pop(endpoint, None)
                else:
                    # Clear all
                    sync_state = {}
                sync_state_file.write_text(json.dumps(sync_state, indent=2))
            except (json.JSONDecodeError, IOError):
                # If sync_state is corrupted, just delete it
                if not endpoint:
                    sync_state_file.unlink()

        return len(files)

    def _get_cache_path(self, endpoint: str, date: str) -> Path:
        """Get cache file path for endpoint and date."""
        return self.cache_dir / endpoint / f"{date}.json"

    def get_last_sync(self, endpoint: str) -> Optional[str]:
        """
        Get last synced date for endpoint.

        Returns:
            ISO date string or None if never synced
        """
        sync_state_file = self.cache_dir / "sync_state.json"
        if not sync_state_file.exists():
            return None

        try:
            with open(sync_state_file, "r") as f:
                sync_state = json.load(f)
                return sync_state.get(endpoint)
        except (json.JSONDecodeError, IOError):
            return None

    def set_last_sync(self, endpoint: str, date: str) -> None:
        """
        Update last synced date for endpoint.

        Args:
            endpoint: API endpoint
            date: ISO date string (YYYY-MM-DD)
        """
        sync_state_file = self.cache_dir / "sync_state.json"

        # Load existing state
        sync_state = {}
        if sync_state_file.exists():
            try:
                with open(sync_state_file, "r") as f:
                    sync_state = json.load(f)
            except (json.JSONDecodeError, IOError):
                pass

        # Update and save
        sync_state[endpoint] = date
        with open(sync_state_file, "w") as f:
            json.dump(sync_state, f, indent=2)
