#!/usr/bin/env python3
"""
Example event handler.
Reads event JSON from stdin and processes it.
"""

import json
import sys

def main():
    # Read event from stdin
    event_json = sys.stdin.read()
    event = json.loads(event_json)
    
    # Process event
    print(f"Received event: {event['event_type']}")
    print(f"From: {event['source_agent']}")
    print(f"Payload: {json.dumps(event['payload'], indent=2)}")
    
    # Your processing logic here
    # ...
    
    # Output result (optional)
    result = {
        "status": "success",
        "processed_at": event['timestamp']
    }
    
    print(json.dumps(result))

if __name__ == "__main__":
    main()
