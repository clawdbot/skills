#!/usr/bin/env python3
"""
Subscribe - Subscribe to events and route them to handlers.

Lightweight subscription system that monitors event queue and executes handlers.
"""

import json
import sys
import time
import subprocess
from pathlib import Path
from typing import List, Dict, Callable, Optional
from event_bus import EventBus

SUBSCRIPTIONS_FILE = Path.home() / ".clawdbot" / "events" / "subscriptions.json"


class Subscriber:
    """Event subscription manager."""
    
    def __init__(self):
        self.bus = EventBus()
        self.subscriptions = self._load_subscriptions()
    
    def _load_subscriptions(self) -> List[Dict]:
        """Load subscription configuration."""
        if SUBSCRIPTIONS_FILE.exists():
            try:
                return json.loads(SUBSCRIPTIONS_FILE.read_text())
            except:
                return []
        return []
    
    def _save_subscriptions(self):
        """Save subscription configuration."""
        SUBSCRIPTIONS_FILE.parent.mkdir(parents=True, exist_ok=True)
        SUBSCRIPTIONS_FILE.write_text(json.dumps(self.subscriptions, indent=2))
    
    def add_subscription(
        self,
        event_types: List[str],
        handler: str,
        filter_conditions: Optional[Dict] = None
    ):
        """Add a new subscription."""
        subscription = {
            "event_types": event_types,
            "handler": handler,
            "filter": filter_conditions or {}
        }
        
        self.subscriptions.append(subscription)
        self._save_subscriptions()
    
    def remove_subscription(self, index: int):
        """Remove subscription by index."""
        if 0 <= index < len(self.subscriptions):
            self.subscriptions.pop(index)
            self._save_subscriptions()
    
    def process_subscriptions(self):
        """Process pending events for all subscriptions."""
        for subscription in self.subscriptions:
            event_types = subscription["event_types"]
            handler = subscription["handler"]
            filter_cond = subscription.get("filter", {})
            
            # Get matching events
            events = self.bus.get_pending_events(event_types)
            
            for event in events:
                # Apply filter
                if filter_cond:
                    if not self._matches_filter(event["payload"], filter_cond):
                        continue
                
                # Call handler
                try:
                    self._call_handler(handler, event)
                    self.bus.mark_processed(event["event_id"])
                except Exception as e:
                    print(f"Handler error: {e}", file=sys.stderr)
                    self.bus.mark_processed(event["event_id"], success=False)
    
    def _matches_filter(self, payload: Dict, filter_cond: Dict) -> bool:
        """Check if payload matches filter conditions."""
        for key, condition in filter_cond.items():
            value = payload.get(key)
            
            if isinstance(condition, dict):
                for op, expected in condition.items():
                    if op == "gte" and not (value >= expected):
                        return False
                    elif op == "lte" and not (value <= expected):
                        return False
                    elif op == "eq" and value != expected:
                        return False
            else:
                if value != condition:
                    return False
        
        return True
    
    def _call_handler(self, handler: str, event: Dict):
        """Execute handler script with event as input."""
        handler_path = Path(handler)
        
        if not handler_path.exists():
            raise FileNotFoundError(f"Handler not found: {handler}")
        
        event_json = json.dumps(event)
        
        if handler_path.suffix == ".py":
            subprocess.run(
                ["python3", str(handler_path)],
                input=event_json,
                text=True,
                check=True
            )
        elif handler_path.suffix == ".js":
            subprocess.run(
                ["node", str(handler_path)],
                input=event_json,
                text=True,
                check=True
            )
        else:
            subprocess.run(
                [str(handler_path)],
                input=event_json,
                text=True,
                check=True
            )


def subscribe_decorator(event_types: List[str]):
    """Decorator for subscribing functions to events (for library use)."""
    def decorator(func: Callable):
        func._event_types = event_types
        return func
    return decorator


def main():
    """CLI for managing subscriptions."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Subscribe to agent protocol events")
    parser.add_argument("--types", help="Comma-separated event types (supports wildcards)")
    parser.add_argument("--handler", help="Path to handler script")
    parser.add_argument("--filter", help="JSON filter conditions")
    parser.add_argument("--list", action="store_true", help="List subscriptions")
    parser.add_argument("--remove", type=int, help="Remove subscription by index")
    parser.add_argument("--daemon", action="store_true", help="Run as daemon")
    parser.add_argument("--interval", type=int, default=30, help="Poll interval (seconds)")
    
    args = parser.parse_args()
    
    subscriber = Subscriber()
    
    if args.list:
        if not subscriber.subscriptions:
            print("No active subscriptions.")
        else:
            print("Active subscriptions:\n")
            for i, sub in enumerate(subscriber.subscriptions):
                print(f"{i}. Event types: {', '.join(sub['event_types'])}")
                print(f"   Handler: {sub['handler']}")
                if sub.get('filter'):
                    print(f"   Filter: {json.dumps(sub['filter'])}")
                print()
    
    elif args.remove is not None:
        subscriber.remove_subscription(args.remove)
        print(f"Removed subscription {args.remove}")
    
    elif args.types and args.handler:
        event_types = [t.strip() for t in args.types.split(",")]
        filter_cond = json.loads(args.filter) if args.filter else None
        
        subscriber.add_subscription(event_types, args.handler, filter_cond)
        print(f"Added subscription for {event_types} → {args.handler}")
    
    elif args.daemon:
        print("Starting subscription daemon...")
        try:
            while True:
                subscriber.process_subscriptions()
                time.sleep(args.interval)
        except KeyboardInterrupt:
            print("\nSubscription daemon stopped.")
    
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
