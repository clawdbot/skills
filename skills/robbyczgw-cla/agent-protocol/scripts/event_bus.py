#!/usr/bin/env python3
"""
Event Bus - Core message passing system for agent-to-agent communication.

Provides:
- Event publishing
- Event persistence
- Event queue management
- Subscription routing
- Cleanup and retention
"""

import json
import os
import sys
import time
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import hashlib
import fcntl

# Event storage paths
HOME = Path.home()
EVENT_DIR = HOME / ".clawdbot" / "events"
QUEUE_DIR = EVENT_DIR / "queue"
PROCESSED_DIR = EVENT_DIR / "processed"
FAILED_DIR = EVENT_DIR / "failed"
LOG_DIR = EVENT_DIR / "log"
CONFIG_FILE = Path(__file__).parent.parent / "config" / "protocol.json"

# Ensure directories exist
for dir_path in [EVENT_DIR, QUEUE_DIR, PROCESSED_DIR, FAILED_DIR, LOG_DIR]:
    dir_path.mkdir(parents=True, exist_ok=True)


class EventBus:
    """Core event bus for publishing, subscribing, and managing events."""
    
    def __init__(self, config_path: Optional[Path] = None):
        self.config = self._load_config(config_path or CONFIG_FILE)
        self.log_file = LOG_DIR / "events.log"
    
    def _load_config(self, config_path: Path) -> Dict:
        """Load configuration or return defaults."""
        defaults = {
            "event_bus": {
                "storage_path": str(EVENT_DIR),
                "retention_days": 7,
                "max_event_size_kb": 512
            },
            "workflow_engine": {
                "enabled": True,
                "poll_interval_seconds": 30,
                "max_concurrent_workflows": 5
            },
            "security": {
                "require_permissions": False,
                "audit_log": True
            }
        }
        
        if config_path.exists():
            try:
                return json.loads(config_path.read_text())
            except Exception as e:
                self._log(f"Error loading config: {e}, using defaults")
                return defaults
        return defaults
    
    def _log(self, message: str, level: str = "INFO"):
        """Log to file and optionally stdout."""
        timestamp = datetime.utcnow().isoformat()
        log_line = f"[{timestamp}] [{level}] {message}\n"
        
        try:
            with open(self.log_file, "a") as f:
                f.write(log_line)
        except Exception as e:
            print(f"Failed to write log: {e}", file=sys.stderr)
    
    def _generate_event_id(self) -> str:
        """Generate unique event ID."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        random_suffix = hashlib.md5(os.urandom(8)).hexdigest()[:8]
        return f"evt_{timestamp}_{random_suffix}"
    
    def _validate_event(self, event: Dict) -> tuple[bool, Optional[str]]:
        """Validate event structure."""
        required_fields = ["event_type", "source_agent", "payload"]
        
        for field in required_fields:
            if field not in event:
                return False, f"Missing required field: {field}"
        
        # Check event size
        event_json = json.dumps(event)
        max_size = self.config["event_bus"]["max_event_size_kb"] * 1024
        if len(event_json) > max_size:
            return False, f"Event too large: {len(event_json)} bytes (max: {max_size})"
        
        return True, None
    
    def publish(self, event: Dict) -> tuple[bool, str]:
        """
        Publish an event to the queue.
        
        Args:
            event: Event dictionary with event_type, source_agent, payload
        
        Returns:
            (success, event_id or error_message)
        """
        # Add metadata
        if "event_id" not in event:
            event["event_id"] = self._generate_event_id()
        if "timestamp" not in event:
            event["timestamp"] = datetime.utcnow().isoformat() + "Z"
        
        # Validate
        valid, error = self._validate_event(event)
        if not valid:
            self._log(f"Event validation failed: {error}", "ERROR")
            return False, error
        
        event_id = event["event_id"]
        
        # Write to queue
        try:
            event_file = QUEUE_DIR / f"{event_id}.json"
            event_file.write_text(json.dumps(event, indent=2))
            
            self._log(f"Published event: {event_id} (type: {event['event_type']}, source: {event['source_agent']})")
            
            if self.config["security"]["audit_log"]:
                self._audit_log("publish", event)
            
            return True, event_id
        
        except Exception as e:
            error_msg = f"Failed to publish event: {e}"
            self._log(error_msg, "ERROR")
            return False, error_msg
    
    def get_pending_events(self, event_types: Optional[List[str]] = None) -> List[Dict]:
        """
        Get pending events from queue, optionally filtered by type.
        
        Args:
            event_types: List of event type patterns (supports wildcards like "research.*")
        
        Returns:
            List of event dictionaries
        """
        events = []
        
        try:
            for event_file in sorted(QUEUE_DIR.glob("*.json")):
                try:
                    event = json.loads(event_file.read_text())
                    
                    # Filter by event type if specified
                    if event_types:
                        if not self._matches_event_types(event["event_type"], event_types):
                            continue
                    
                    events.append(event)
                
                except Exception as e:
                    self._log(f"Error reading event {event_file.name}: {e}", "ERROR")
        
        except Exception as e:
            self._log(f"Error listing pending events: {e}", "ERROR")
        
        return events
    
    def _matches_event_types(self, event_type: str, patterns: List[str]) -> bool:
        """Check if event type matches any pattern (supports wildcards)."""
        for pattern in patterns:
            if pattern.endswith(".*"):
                prefix = pattern[:-2]
                if event_type.startswith(prefix):
                    return True
            elif pattern == event_type:
                return True
        return False
    
    def mark_processed(self, event_id: str, success: bool = True):
        """Mark an event as processed (move to processed or failed directory)."""
        src = QUEUE_DIR / f"{event_id}.json"
        
        if not src.exists():
            self._log(f"Event not found: {event_id}", "WARNING")
            return
        
        try:
            dest_dir = PROCESSED_DIR if success else FAILED_DIR
            dest = dest_dir / f"{event_id}.json"
            src.rename(dest)
            
            status = "processed" if success else "failed"
            self._log(f"Event {event_id} marked as {status}")
        
        except Exception as e:
            self._log(f"Error marking event {event_id}: {e}", "ERROR")
    
    def cleanup_old_events(self):
        """Remove events older than retention period."""
        retention_days = self.config["event_bus"]["retention_days"]
        cutoff = datetime.utcnow() - timedelta(days=retention_days)
        
        removed_count = 0
        
        for directory in [PROCESSED_DIR, FAILED_DIR]:
            try:
                for event_file in directory.glob("*.json"):
                    try:
                        # Parse timestamp from event_id (evt_YYYYMMDD_HHMMSS_...)
                        parts = event_file.stem.split("_")
                        if len(parts) >= 3:
                            timestamp_str = f"{parts[1]}_{parts[2]}"
                            event_time = datetime.strptime(timestamp_str, "%Y%m%d_%H%M%S")
                            
                            if event_time < cutoff:
                                event_file.unlink()
                                removed_count += 1
                    
                    except Exception as e:
                        self._log(f"Error processing {event_file.name}: {e}", "WARNING")
            
            except Exception as e:
                self._log(f"Error cleaning up {directory}: {e}", "ERROR")
        
        if removed_count > 0:
            self._log(f"Cleaned up {removed_count} old events")
    
    def _audit_log(self, action: str, event: Dict):
        """Log audit trail."""
        audit_file = LOG_DIR / "audit.log"
        audit_entry = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "action": action,
            "event_id": event.get("event_id"),
            "event_type": event.get("event_type"),
            "source_agent": event.get("source_agent")
        }
        
        try:
            with open(audit_file, "a") as f:
                f.write(json.dumps(audit_entry) + "\n")
        except Exception as e:
            self._log(f"Audit log failed: {e}", "ERROR")
    
    def get_stats(self) -> Dict:
        """Get event bus statistics."""
        return {
            "queue_size": len(list(QUEUE_DIR.glob("*.json"))),
            "processed_count": len(list(PROCESSED_DIR.glob("*.json"))),
            "failed_count": len(list(FAILED_DIR.glob("*.json"))),
            "log_size_kb": self.log_file.stat().st_size // 1024 if self.log_file.exists() else 0
        }
    
    def tail_events(self, count: int = 20) -> List[Dict]:
        """Get most recent events from all directories."""
        all_events = []
        
        for directory in [QUEUE_DIR, PROCESSED_DIR, FAILED_DIR]:
            for event_file in directory.glob("*.json"):
                try:
                    event = json.loads(event_file.read_text())
                    event["_status"] = directory.name
                    all_events.append(event)
                except:
                    pass
        
        # Sort by timestamp, most recent first
        all_events.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
        return all_events[:count]


def main():
    """CLI interface for event bus management."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Agent Protocol Event Bus")
    parser.add_argument("command", choices=["start", "stop", "status", "tail", "cleanup", "stats"])
    parser.add_argument("--count", type=int, default=20, help="Number of events to tail")
    
    args = parser.parse_args()
    
    bus = EventBus()
    
    if args.command == "status":
        stats = bus.get_stats()
        print("Event Bus Status:")
        print(f"  Queue: {stats['queue_size']} pending")
        print(f"  Processed: {stats['processed_count']}")
        print(f"  Failed: {stats['failed_count']}")
        print(f"  Log size: {stats['log_size_kb']} KB")
    
    elif args.command == "tail":
        events = bus.tail_events(args.count)
        if not events:
            print("No events found.")
        else:
            for event in events:
                status = event.pop("_status", "unknown")
                print(f"\n[{status.upper()}] {event['event_id']}")
                print(f"  Type: {event['event_type']}")
                print(f"  Source: {event['source_agent']}")
                print(f"  Time: {event['timestamp']}")
                print(f"  Payload: {json.dumps(event['payload'], indent=4)}")
    
    elif args.command == "cleanup":
        print("Running cleanup...")
        bus.cleanup_old_events()
        print("Cleanup complete.")
    
    elif args.command == "stats":
        stats = bus.get_stats()
        print(json.dumps(stats, indent=2))
    
    elif args.command == "start":
        print("Event bus is file-based and always active.")
        print("No daemon needed - events are processed by workflow engine.")
        print("Run: python3 workflow_engine.py --daemon")
    
    elif args.command == "stop":
        print("Event bus is file-based - nothing to stop.")
        print("To stop workflow processing: kill the workflow_engine.py process")


if __name__ == "__main__":
    main()
