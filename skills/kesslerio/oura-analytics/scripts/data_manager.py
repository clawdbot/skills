#!/usr/bin/env python3
"""
Data management and privacy controls for Oura Analytics.

Provides commands for:
- Exporting data (backup, portability)
- Clearing data (privacy, cleanup)
- Listing stored data
- Managing retention policies
"""

import json
import csv
import shutil
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
import sys


class OuraDataManager:
    """Manage local Oura data storage, export, and cleanup."""
    
    def __init__(self, data_dir: Optional[Path] = None):
        """
        Initialize data manager.
        
        Args:
            data_dir: Base data directory (default: ~/.oura-analytics/)
        """
        if data_dir is None:
            data_dir = Path.home() / ".oura-analytics"
        
        self.data_dir = data_dir
        self.cache_dir = data_dir / "cache"
        self.events_file = data_dir / "events.jsonl"
        self.config_file = data_dir / "config.yaml"
        self.alert_state_file = data_dir / "alert_state.json"
        
        # Ensure directories exist
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def get_storage_info(self) -> Dict[str, Any]:
        """
        Get information about stored data.
        
        Returns:
            Dictionary with storage statistics
        """
        info = {
            "data_dir": str(self.data_dir),
            "total_size_bytes": 0,
            "cache": {
                "size_bytes": 0,
                "file_count": 0,
                "endpoints": {}
            },
            "events": {
                "exists": self.events_file.exists(),
                "size_bytes": 0,
                "count": 0
            },
            "config": {
                "exists": self.config_file.exists(),
                "size_bytes": 0
            },
            "alert_state": {
                "exists": self.alert_state_file.exists(),
                "size_bytes": 0
            }
        }
        
        # Calculate cache size and file counts
        if self.cache_dir.exists():
            for endpoint_dir in self.cache_dir.iterdir():
                if endpoint_dir.is_dir():
                    endpoint_name = endpoint_dir.name
                    files = list(endpoint_dir.glob("*.json"))
                    endpoint_size = sum(f.stat().st_size for f in files)
                    
                    info["cache"]["endpoints"][endpoint_name] = {
                        "file_count": len(files),
                        "size_bytes": endpoint_size,
                        "oldest_date": min((f.stem for f in files), default=None),
                        "newest_date": max((f.stem for f in files), default=None)
                    }
                    
                    info["cache"]["size_bytes"] += endpoint_size
                    info["cache"]["file_count"] += len(files)
        
        # Events file
        if self.events_file.exists():
            info["events"]["size_bytes"] = self.events_file.stat().st_size
            with open(self.events_file, "r") as f:
                info["events"]["count"] = sum(1 for _ in f)
        
        # Config file
        if self.config_file.exists():
            info["config"]["size_bytes"] = self.config_file.stat().st_size
        
        # Alert state file
        if self.alert_state_file.exists():
            info["alert_state"]["size_bytes"] = self.alert_state_file.stat().st_size
        
        # Total size
        info["total_size_bytes"] = (
            info["cache"]["size_bytes"] +
            info["events"]["size_bytes"] +
            info["config"]["size_bytes"] +
            info["alert_state"]["size_bytes"]
        )
        
        return info
    
    def export_data(self, output_file: Path, format: str = "json") -> None:
        """
        Export all local data to a file.
        
        Args:
            output_file: Output file path
            format: Export format (json, tar.gz)
        """
        if format == "json":
            self._export_json(output_file)
        elif format == "tar.gz":
            self._export_tarball(output_file)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _export_json(self, output_file: Path) -> None:
        """Export all data as single JSON file."""
        export_data = {
            "export_date": datetime.now().isoformat(),
            "data_dir": str(self.data_dir),
            "cache": {},
            "events": [],
            "config": None,
            "alert_state": None
        }
        
        # Export cache
        if self.cache_dir.exists():
            for endpoint_dir in self.cache_dir.iterdir():
                if endpoint_dir.is_dir():
                    endpoint_name = endpoint_dir.name
                    export_data["cache"][endpoint_name] = {}
                    
                    for cache_file in endpoint_dir.glob("*.json"):
                        date = cache_file.stem
                        with open(cache_file, "r") as f:
                            export_data["cache"][endpoint_name][date] = json.load(f)
        
        # Export events
        if self.events_file.exists():
            with open(self.events_file, "r") as f:
                export_data["events"] = [json.loads(line) for line in f]
        
        # Export config
        if self.config_file.exists():
            with open(self.config_file, "r") as f:
                export_data["config"] = f.read()
        
        # Export alert state
        if self.alert_state_file.exists():
            with open(self.alert_state_file, "r") as f:
                export_data["alert_state"] = json.load(f)
        
        # Write export file
        with open(output_file, "w") as f:
            json.dump(export_data, f, indent=2)
        
        print(f"Exported to {output_file}", file=sys.stderr)
        print(f"Size: {output_file.stat().st_size / 1024:.1f} KB", file=sys.stderr)
    
    def _export_tarball(self, output_file: Path) -> None:
        """Export data directory as compressed tarball."""
        import tarfile
        
        with tarfile.open(output_file, "w:gz") as tar:
            tar.add(self.data_dir, arcname=self.data_dir.name)
        
        print(f"Exported to {output_file}", file=sys.stderr)
        print(f"Size: {output_file.stat().st_size / 1024:.1f} KB", file=sys.stderr)
    
    def export_events(self, output_file: Path, format: str = "json") -> None:
        """
        Export events to a file.
        
        Args:
            output_file: Output file path
            format: Export format (json, csv)
        """
        if not self.events_file.exists():
            print("No events to export", file=sys.stderr)
            return
        
        with open(self.events_file, "r") as f:
            events = [json.loads(line) for line in f]
        
        if format == "json":
            with open(output_file, "w") as f:
                json.dump(events, f, indent=2)
        elif format == "csv":
            if not events:
                print("No events to export", file=sys.stderr)
                return
            
            # Get all possible fields
            fieldnames = set()
            for event in events:
                fieldnames.update(event.keys())
            fieldnames = sorted(fieldnames)
            
            with open(output_file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(events)
        else:
            raise ValueError(f"Unsupported export format: {format}")
        
        print(f"Exported {len(events)} events to {output_file}", file=sys.stderr)
    
    def clear_cache(self, endpoint: Optional[str] = None, confirm: bool = False) -> None:
        """
        Clear cached data.
        
        Args:
            endpoint: Specific endpoint to clear (sleep, readiness, activity), or None for all
            confirm: Require confirmation before deleting
        """
        if not confirm:
            print("ERROR: Must pass --confirm to clear data", file=sys.stderr)
            sys.exit(1)
        
        if endpoint:
            endpoint_dir = self.cache_dir / endpoint
            if endpoint_dir.exists():
                shutil.rmtree(endpoint_dir)
                print(f"Cleared cache for {endpoint}", file=sys.stderr)
            else:
                print(f"No cache found for {endpoint}", file=sys.stderr)
        else:
            if self.cache_dir.exists():
                shutil.rmtree(self.cache_dir)
                self.cache_dir.mkdir(parents=True, exist_ok=True)
                print("Cleared all cache", file=sys.stderr)
            else:
                print("No cache to clear", file=sys.stderr)
    
    def clear_events(self, confirm: bool = False) -> None:
        """
        Clear events file.
        
        Args:
            confirm: Require confirmation before deleting
        """
        if not confirm:
            print("ERROR: Must pass --confirm to clear data", file=sys.stderr)
            sys.exit(1)
        
        if self.events_file.exists():
            self.events_file.unlink()
            print("Cleared events", file=sys.stderr)
        else:
            print("No events to clear", file=sys.stderr)
    
    def clear_all(self, confirm: bool = False) -> None:
        """
        Clear all local data.
        
        Args:
            confirm: Require confirmation before deleting
        """
        if not confirm:
            print("ERROR: Must pass --confirm to clear data", file=sys.stderr)
            sys.exit(1)
        
        if self.data_dir.exists():
            shutil.rmtree(self.data_dir)
            print(f"Cleared all data from {self.data_dir}", file=sys.stderr)
        else:
            print("No data to clear", file=sys.stderr)
    
    def cleanup_old_cache(self, days: int = 90) -> None:
        """
        Delete cached data older than specified days.
        
        Args:
            days: Delete cache files older than this many days
        """
        cutoff_date = datetime.now() - timedelta(days=days)
        cutoff_str = cutoff_date.strftime("%Y-%m-%d")
        
        deleted_count = 0
        deleted_size = 0
        
        if self.cache_dir.exists():
            for endpoint_dir in self.cache_dir.iterdir():
                if endpoint_dir.is_dir():
                    for cache_file in endpoint_dir.glob("*.json"):
                        date_str = cache_file.stem
                        if date_str < cutoff_str:
                            size = cache_file.stat().st_size
                            cache_file.unlink()
                            deleted_count += 1
                            deleted_size += size
        
        if deleted_count > 0:
            print(f"Deleted {deleted_count} files older than {days} days", file=sys.stderr)
            print(f"Freed {deleted_size / 1024:.1f} KB", file=sys.stderr)
        else:
            print(f"No cache files older than {days} days", file=sys.stderr)


def format_size(bytes: int) -> str:
    """Format bytes as human-readable size."""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes < 1024:
            return f"{bytes:.1f} {unit}"
        bytes /= 1024
    return f"{bytes:.1f} TB"
