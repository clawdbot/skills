#!/usr/bin/env python3
"""
Nest Pub/Sub Webhook Server (stdlib only)

Receives push messages from Google Cloud Pub/Sub for Nest device events
and triggers Clawdbot alerts via cron wake events.
"""

import base64
import json
import os
import sys
import urllib.request
import urllib.error
from datetime import datetime
from http.server import HTTPServer, BaseHTTPRequestHandler

# Clawdbot gateway config
GATEWAY_URL = os.environ.get('CLAWDBOT_GATEWAY_URL', 'http://localhost:18789')
HOOKS_TOKEN = os.environ.get('CLAWDBOT_HOOKS_TOKEN', '')

# Event type descriptions
EVENT_TYPES = {
    'sdm.devices.events.DoorbellChime.Chime': '🔔 Doorbell rang!',
    'sdm.devices.events.CameraMotion.Motion': '📹 Motion detected',
    'sdm.devices.events.CameraPerson.Person': '🚶 Person detected',
    'sdm.devices.events.CameraSound.Sound': '🔊 Sound detected',
    'sdm.devices.events.CameraClipPreview.ClipPreview': '🎬 Clip ready',
}


def get_device_name(device_id: str) -> str:
    """Extract friendly device name from device ID."""
    parts = device_id.split('/')
    if len(parts) >= 4:
        return parts[-1][:8]
    return device_id


def send_clawdbot_alert(message: str) -> bool:
    """Send alert via hooks/agent endpoint with direct delivery to Telegram."""
    if not HOOKS_TOKEN:
        print(f"[ALERT] {message}")
        print("Warning: CLAWDBOT_HOOKS_TOKEN not set, can't send alert")
        return False
    
    try:
        payload = {
            'message': f'NEST ALERT: {message}\n\nRelay this exact alert to Andrew immediately, nothing else.',
            'name': 'Nest',
            'deliver': True,
            'channel': 'telegram',
            'wakeMode': 'now'
        }
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            f"{GATEWAY_URL}/hooks/agent",
            data=data,
            headers={
                'Authorization': f'Bearer {HOOKS_TOKEN}',
                'Content-Type': 'application/json'
            },
            method='POST'
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            print(f"[SENT] {message}")
            return True
    except Exception as e:
        print(f"[ERROR] Failed to send alert: {e}")
        return False


class NestWebhookHandler(BaseHTTPRequestHandler):
    """HTTP handler for Nest Pub/Sub events."""
    
    def log_message(self, format, *args):
        """Custom log format."""
        print(f"[HTTP] {args[0]}")
    
    def send_json(self, data: dict, status: int = 200):
        """Send JSON response."""
        body = json.dumps(data).encode('utf-8')
        self.send_response(status)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)
    
    def do_GET(self):
        """Handle GET requests."""
        if self.path == '/health':
            self.send_json({'status': 'healthy', 'service': 'nest-webhook'})
        elif self.path == '/':
            self.send_json({
                'service': 'Nest Pub/Sub Webhook',
                'endpoints': {
                    '/nest/events': 'POST - Pub/Sub push endpoint',
                    '/health': 'GET - Health check'
                }
            })
        else:
            self.send_json({'error': 'Not found'}, 404)
    
    def do_POST(self):
        """Handle POST requests (Pub/Sub push)."""
        if self.path != '/nest/events':
            self.send_json({'error': 'Not found'}, 404)
            return
        
        # Read body
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        
        try:
            envelope = json.loads(body.decode('utf-8'))
        except json.JSONDecodeError:
            self.send_json({'error': 'Invalid JSON'}, 400)
            return
        
        # Extract the Pub/Sub message
        pubsub_message = envelope.get('message', {})
        if not pubsub_message:
            self.send_json({'error': 'No message in envelope'}, 400)
            return
        
        # Decode the data (base64 encoded)
        data_b64 = pubsub_message.get('data', '')
        try:
            data_json = base64.b64decode(data_b64).decode('utf-8')
            data = json.loads(data_json)
        except Exception as e:
            print(f"Failed to decode message: {e}")
            self.send_json({'error': 'Invalid message data'}, 400)
            return
        
        print(f"[RECEIVED] {json.dumps(data, indent=2)}")
        
        # Parse the Nest event
        resource_update = data.get('resourceUpdate', {})
        events = resource_update.get('events', {})
        device_id = resource_update.get('name', 'unknown')
        device_name = get_device_name(device_id)
        
        for event_type, event_data in events.items():
            description = EVENT_TYPES.get(event_type, f'Event: {event_type}')
            alert = f"{description}"
            if device_name != 'unknown':
                alert += f" (device: {device_name})"
            send_clawdbot_alert(alert)
        
        # Log trait updates but don't spam alerts
        traits = resource_update.get('traits', {})
        if traits and not events:
            for trait_name, trait_value in traits.items():
                print(f"[TRAIT] {trait_name}: {trait_value}")
        
        self.send_json({'status': 'ok'})


def main():
    port = int(os.environ.get('PORT', 8420))
    print(f"Starting Nest webhook server on port {port}")
    print(f"Gateway URL: {GATEWAY_URL}")
    print(f"Hooks token: {'set' if HOOKS_TOKEN else 'NOT SET'}")
    
    server = HTTPServer(('0.0.0.0', port), NestWebhookHandler)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == '__main__':
    main()
