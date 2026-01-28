#!/usr/bin/env python3
"""
Zoom Webhook Server — receives Zoom events and notifies via Clawdbot.

Usage:
  python3 webhook.py [--port 8765]

Environment:
  ZOOM_WEBHOOK_SECRET_TOKEN — Webhook secret token for validation (from Zoom app)

Events handled:
  - chat_message.sent — new Team Chat message received
"""

import hashlib
import hmac
import json
import os
import subprocess
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

PORT = int(sys.argv[sys.argv.index("--port") + 1]) if "--port" in sys.argv else 8765
ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", ".env")


def _load_env():
    env_path = os.path.normpath(ENV_FILE)
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


_load_env()
WEBHOOK_SECRET = os.environ.get("ZOOM_WEBHOOK_SECRET_TOKEN", "")


def notify(message):
    """Send notification via clawdbot CLI."""
    try:
        subprocess.run(
            ["clawdbot", "message", "send", "--channel", "whatsapp", "--target", os.environ.get("ZOOM_NOTIFY_TARGET", "+6593632452"), "--message", message],
            timeout=30,
            capture_output=True,
        )
        print(f"[NOTIFY] {message}")
    except Exception as e:
        print(f"[NOTIFY ERROR] {e}", file=sys.stderr)


class WebhookHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)

        try:
            data = json.loads(body)
        except json.JSONDecodeError:
            self.send_response(400)
            self.end_headers()
            return

        event = data.get("event", "")

        # Zoom URL validation challenge
        if event == "endpoint.url_validation":
            plain_token = data.get("payload", {}).get("plainToken", "")
            if WEBHOOK_SECRET and plain_token:
                h = hmac.new(WEBHOOK_SECRET.encode(), plain_token.encode(), hashlib.sha256).hexdigest()
                resp = json.dumps({"plainToken": plain_token, "encryptedToken": h})
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(resp.encode())
                print(f"[VALIDATE] URL validation successful")
                return

        # Chat message received
        if event == "chat_message.sent":
            payload = data.get("payload", {}).get("object", {})
            sender = payload.get("sender", {})
            sender_name = sender.get("display_name", sender.get("email", "Unknown"))
            message_text = payload.get("message", "(no text)")
            channel = payload.get("channel_name", "DM")
            date_time = payload.get("date_time", "")

            # Don't notify for messages from ourselves
            my_email = os.environ.get("ZOOM_USER_EMAIL", "")
            if sender.get("email", "").lower() == my_email.lower():
                self.send_response(200)
                self.end_headers()
                return

            notify(f"💬 Zoom Chat from *{sender_name}*{' in ' + channel if channel != 'DM' else ''}:\n{message_text}")

        # Meeting started
        elif event == "meeting.started":
            payload = data.get("payload", {}).get("object", {})
            topic = payload.get("topic", "Untitled")
            host = payload.get("host_id", "?")
            notify(f"📹 Zoom Meeting started: *{topic}*")

        # Meeting ended
        elif event == "meeting.ended":
            payload = data.get("payload", {}).get("object", {})
            topic = payload.get("topic", "Untitled")
            notify(f"📹 Zoom Meeting ended: *{topic}*")

        # Recording completed
        elif event == "recording.completed":
            payload = data.get("payload", {}).get("object", {})
            topic = payload.get("topic", "Untitled")
            notify(f"🎥 Zoom Recording ready: *{topic}*")

        else:
            print(f"[EVENT] {event} (unhandled)")

        self.send_response(200)
        self.end_headers()

    def do_GET(self):
        """Health check."""
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status": "ok", "service": "zoom-webhook"}).encode())

    def log_message(self, format, *args):
        print(f"[HTTP] {args[0]}")


if __name__ == "__main__":
    print(f"Zoom Webhook Server starting on port {PORT}...")
    print(f"Webhook secret: {'configured' if WEBHOOK_SECRET else 'NOT SET (set ZOOM_WEBHOOK_SECRET_TOKEN in .env)'}")
    print(f"Notify target: {os.environ.get('ZOOM_NOTIFY_TARGET', '+6593632452')}")
    server = HTTPServer(("0.0.0.0", PORT), WebhookHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down.")
        server.server_close()
