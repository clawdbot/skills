#!/usr/bin/env python3
"""
Publish Event - CLI and library for publishing events to the event bus.

Usage:
    python3 publish.py --type "research.article_found" --source "my-agent" --payload '{"title": "..."}'
    
Or import and use programmatically:
    from publish import publish_event
    publish_event("research.found", "my-agent", {"title": "Article"})
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from event_bus import EventBus


def publish_event(
    event_type: str,
    source_agent: str,
    payload: Dict[str, Any],
    priority: str = "normal",
    metadata: Optional[Dict] = None
) -> tuple[bool, str]:
    """
    Publish an event to the event bus.
    
    Args:
        event_type: Event type (e.g., "research.article_found")
        source_agent: Name of the agent publishing the event
        payload: Event data
        priority: Event priority (low, normal, high)
        metadata: Optional metadata
    
    Returns:
        (success, event_id or error_message)
    """
    event = {
        "event_type": event_type,
        "source_agent": source_agent,
        "payload": payload,
        "metadata": metadata or {}
    }
    
    if priority != "normal":
        event["metadata"]["priority"] = priority
    
    bus = EventBus()
    return bus.publish(event)


def main():
    """CLI interface for publishing events."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Publish event to agent protocol bus")
    parser.add_argument("--type", required=True, help="Event type (e.g., research.article_found)")
    parser.add_argument("--source", required=True, help="Source agent name")
    parser.add_argument("--payload", help="JSON payload")
    parser.add_argument("--file", help="Load event from JSON file")
    parser.add_argument("--priority", choices=["low", "normal", "high"], default="normal")
    
    args = parser.parse_args()
    
    # Load payload
    if args.file:
        try:
            event = json.loads(Path(args.file).read_text())
            success, result = EventBus().publish(event)
        except Exception as e:
            print(f"Error loading event file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        if not args.payload:
            print("Error: Either --payload or --file must be provided", file=sys.stderr)
            sys.exit(1)
        
        try:
            payload = json.loads(args.payload)
        except Exception as e:
            print(f"Error parsing payload JSON: {e}", file=sys.stderr)
            sys.exit(1)
        
        success, result = publish_event(
            event_type=args.type,
            source_agent=args.source,
            payload=payload,
            priority=args.priority
        )
    
    if success:
        print(f"✓ Event published: {result}")
        sys.exit(0)
    else:
        print(f"✗ Failed to publish event: {result}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
