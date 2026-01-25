#!/usr/bin/env python3
"""
Send a message to Google Chat via Incoming Webhook.
Usage: python3 send_webhook.py <webhook_url> <message> [--thread_key <key>]
"""

import sys
import json
import urllib.request
import urllib.error
from typing import Optional


def send_webhook_message(webhook_url: str, message: str, thread_key: Optional[str] = None) -> dict:
    """Send a message via Google Chat webhook."""
    payload = {"text": message}
    
    # Add thread key if provided (for threading replies)
    url = webhook_url
    if thread_key:
        url = f"{webhook_url}&threadKey={thread_key}"
    
    headers = {"Content-Type": "application/json; charset=UTF-8"}
    data = json.dumps(payload).encode("utf-8")
    
    req = urllib.request.Request(url, data=data, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode("utf-8"))
            return {"success": True, "response": result}
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8")
        return {"success": False, "error": f"HTTP {e.code}: {error_body}"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 send_webhook.py <webhook_url> <message> [--thread_key <key>]")
        sys.exit(1)
    
    webhook_url = sys.argv[1]
    message = sys.argv[2]
    thread_key = None
    
    # Parse optional thread key
    if len(sys.argv) >= 5 and sys.argv[3] == "--thread_key":
        thread_key = sys.argv[4]
    
    result = send_webhook_message(webhook_url, message, thread_key)
    
    if result["success"]:
        print(json.dumps(result["response"], indent=2))
    else:
        print(f"Error: {result['error']}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
