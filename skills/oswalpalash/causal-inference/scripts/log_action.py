#!/usr/bin/env python3
"""
Log a causal action event to the action log.

Usage:
    python log_action.py --action send_email --outcome reply_received \
        --context '{"recipient_type": "warm"}' \
        --pre '{"days_since_contact": 5}' \
        --post '{"reply_delay_hours": 2}'
"""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_LOG_PATH = "memory/causal/action_log.jsonl"


def log_action(
    action: str,
    outcome: str,
    context: dict = None,
    pre_state: dict = None,
    post_state: dict = None,
    log_path: str = DEFAULT_LOG_PATH,
):
    """Append an action event to the causal action log."""
    event = {
        "action": action,
        "context": context or {},
        "time": datetime.now(timezone.utc).isoformat(),
        "pre_state": pre_state or {},
        "post_state": post_state or {},
        "outcome": outcome,
    }
    
    path = Path(log_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(path, "a") as f:
        f.write(json.dumps(event) + "\n")
    
    return event


def main():
    parser = argparse.ArgumentParser(description="Log a causal action event")
    parser.add_argument("--action", "-a", required=True, help="Action name")
    parser.add_argument("--outcome", "-o", required=True, help="Outcome label")
    parser.add_argument("--context", "-c", default="{}", help="Context JSON")
    parser.add_argument("--pre", default="{}", help="Pre-state JSON")
    parser.add_argument("--post", default="{}", help="Post-state JSON")
    parser.add_argument("--log-path", "-l", default=DEFAULT_LOG_PATH, help="Log file path")
    
    args = parser.parse_args()
    
    event = log_action(
        action=args.action,
        outcome=args.outcome,
        context=json.loads(args.context),
        pre_state=json.loads(args.pre),
        post_state=json.loads(args.post),
        log_path=args.log_path,
    )
    
    print(json.dumps(event, indent=2))


if __name__ == "__main__":
    main()
