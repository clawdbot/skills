#!/usr/bin/env python3
"""
Zoom API CLI — meetings, recordings, chat, users, phone.
Uses Server-to-Server OAuth for authentication.

Environment variables:
  ZOOM_ACCOUNT_ID    — Zoom Account ID
  ZOOM_CLIENT_ID     — OAuth Client ID
  ZOOM_CLIENT_SECRET — OAuth Client Secret
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path
from urllib.parse import quote

try:
    import requests
except ImportError:
    print("ERROR: requests not installed. Run: pip3 install requests --break-system-packages", file=sys.stderr)
    sys.exit(1)

BASE_URL = "https://api.zoom.us/v2"
TOKEN_URL = "https://zoom.us/oauth/token"
TOKEN_CACHE = "/tmp/zoom_token.json"
ENV_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".env")


def _user_id():
    """Get the user ID (email or 'me') from env."""
    _load_env()
    return os.environ.get("ZOOM_USER_EMAIL", "me")


def _load_env():
    """Load .env file from workspace root."""
    env_path = os.path.normpath(ENV_FILE)
    if os.path.exists(env_path):
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    os.environ.setdefault(k.strip(), v.strip())


def get_token():
    """Get or refresh Server-to-Server OAuth token."""
    _load_env()
    account_id = os.environ.get("ZOOM_ACCOUNT_ID")
    client_id = os.environ.get("ZOOM_CLIENT_ID")
    client_secret = os.environ.get("ZOOM_CLIENT_SECRET")

    if not all([account_id, client_id, client_secret]):
        print("ERROR: ZOOM_ACCOUNT_ID, ZOOM_CLIENT_ID, and ZOOM_CLIENT_SECRET must be set", file=sys.stderr)
        sys.exit(1)

    # Check cache
    if os.path.exists(TOKEN_CACHE):
        try:
            with open(TOKEN_CACHE) as f:
                cached = json.load(f)
            if cached.get("expires_at", 0) > time.time() + 60:
                return cached["access_token"]
        except (json.JSONDecodeError, KeyError):
            pass

    # Request new token
    resp = requests.post(
        TOKEN_URL,
        params={"grant_type": "account_credentials", "account_id": account_id},
        auth=(client_id, client_secret),
        timeout=15,
    )
    resp.raise_for_status()
    data = resp.json()
    data["expires_at"] = time.time() + data.get("expires_in", 3600)

    with open(TOKEN_CACHE, "w") as f:
        json.dump(data, f)

    return data["access_token"]


def api(method, path, **kwargs):
    """Make an authenticated Zoom API request with retry on 429."""
    token = get_token()
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

    for attempt in range(3):
        resp = requests.request(method, f"{BASE_URL}{path}", headers=headers, timeout=30, **kwargs)
        if resp.status_code == 429:
            retry_after = int(resp.headers.get("Retry-After", 5))
            print(f"Rate limited, retrying in {retry_after}s...", file=sys.stderr)
            time.sleep(retry_after)
            continue
        if resp.status_code == 204:
            return None
        if not resp.ok:
            try:
                err = resp.json()
                code = err.get("code", resp.status_code)
                msg = err.get("message", resp.reason)
                print(f"ERROR {code}: {msg}", file=sys.stderr)
                if resp.status_code == 401 or "scope" in msg.lower() or "access token" in msg.lower():
                    print("HINT: Add the required scope to your Zoom Marketplace S2S app at https://marketplace.zoom.us/", file=sys.stderr)
                if resp.status_code == 403 and "not been enabled" in msg.lower():
                    print("HINT: This feature is not enabled on your Zoom account. Check your Zoom plan/settings.", file=sys.stderr)
            except Exception:
                print(f"ERROR {resp.status_code}: {resp.text}", file=sys.stderr)
            sys.exit(1)
        return resp.json()

    print("ERROR: Max retries exceeded", file=sys.stderr)
    sys.exit(1)


def _require(value, name):
    """Exit with a helpful message if a required value is missing."""
    if not value:
        print(f"ERROR: Missing required parameter: {name}", file=sys.stderr)
        sys.exit(1)
    return value


# === Meetings ===

def cmd_meetings_list(args):
    """List upcoming meetings."""
    params = {"type": "upcoming", "page_size": 30}
    data = api("GET", f"/users/{_user_id()}/meetings", params=params)
    meetings = data.get("meetings", [])
    if not meetings:
        print("No upcoming meetings.")
        return
    for m in meetings:
        start = m.get("start_time", "TBD")
        duration = m.get("duration", "?")
        topic = m.get("topic", "Untitled")
        mid = m.get("id", "?")
        print(f"  [{mid}] {topic}")
        print(f"    Start: {start} | Duration: {duration}min")
        join = m.get("join_url", "")
        if join:
            print(f"    Join: {join}")
        print()


def cmd_meetings_live(args):
    """List currently live/in-progress meetings via the Dashboard API."""
    params = {"type": "live", "page_size": 30}
    data = api("GET", "/metrics/meetings", params=params)
    meetings = data.get("meetings", [])
    if not meetings:
        print("No live meetings right now.")
        return
    print(f"🔴 {len(meetings)} live meeting(s):\n")
    for m in meetings:
        topic = m.get("topic", "Untitled")
        mid = m.get("id", "?")
        uuid = m.get("uuid", "?")
        host = m.get("host", m.get("email", "?"))
        participants = m.get("participants", 0)
        start = m.get("start_time", "?")
        duration = m.get("duration", "?")
        has_video = "✅" if m.get("has_video", False) else "❌"
        has_screen = "✅" if m.get("has_screen_share", False) else "❌"
        has_recording = "✅" if m.get("has_recording", False) else "❌"
        print(f"  [{mid}] {topic}")
        print(f"    UUID: {uuid}")
        print(f"    Host: {host}")
        print(f"    Participants: {participants} | Started: {start} | Duration: {duration}")
        print(f"    Video: {has_video} | Screen share: {has_screen} | Recording: {has_recording}")
        print()


def _get_live_meeting_host_user_id(meeting_id):
    """Get the host's participant_user_id for a live meeting."""
    data = api("GET", "/metrics/meetings", params={"type": "live", "page_size": 30})
    for m in data.get("meetings", []):
        if str(m.get("id")) == str(meeting_id):
            host_email = m.get("email")
            if not host_email:
                print("ERROR: Could not find host email for this meeting", file=sys.stderr)
                sys.exit(1)
            user = api("GET", f"/users/{host_email}")
            return user.get("id")
    print(f"ERROR: Meeting {meeting_id} is not currently live", file=sys.stderr)
    sys.exit(1)


def cmd_meetings_rtms_start(args):
    """Start RTMS for a live meeting."""
    _load_env()
    _require(args.meeting_id, "meeting_id")
    rtms_client_id = os.environ.get("ZOOM_RTMS_CLIENT_ID")
    if not rtms_client_id:
        print("ERROR: ZOOM_RTMS_CLIENT_ID must be set (Client ID of your RTMS Marketplace app)", file=sys.stderr)
        sys.exit(1)
    host_user_id = _get_live_meeting_host_user_id(args.meeting_id)
    api("PATCH", f"/live_meetings/{args.meeting_id}/rtms_app/status", json={
        "action": "start",
        "settings": {
            "participant_user_id": host_user_id,
            "client_id": rtms_client_id,
        }
    })
    print(f"✅ RTMS started for meeting {args.meeting_id} (host: {host_user_id})")


def cmd_meetings_rtms_stop(args):
    """Stop RTMS for a live meeting."""
    _load_env()
    _require(args.meeting_id, "meeting_id")
    rtms_client_id = os.environ.get("ZOOM_RTMS_CLIENT_ID")
    if not rtms_client_id:
        print("ERROR: ZOOM_RTMS_CLIENT_ID must be set (Client ID of your RTMS Marketplace app)", file=sys.stderr)
        sys.exit(1)
    host_user_id = _get_live_meeting_host_user_id(args.meeting_id)
    api("PATCH", f"/live_meetings/{args.meeting_id}/rtms_app/status", json={
        "action": "stop",
        "settings": {
            "participant_user_id": host_user_id,
            "client_id": rtms_client_id,
        }
    })
    print(f"🛑 RTMS stopped for meeting {args.meeting_id} (host: {host_user_id})")


def cmd_meetings_get(args):
    """Get meeting details."""
    _require(args.meeting_id, "meeting_id")
    data = api("GET", f"/meetings/{args.meeting_id}")
    print(json.dumps(data, indent=2))


def cmd_meetings_create(args):
    """Schedule a new meeting."""
    _require(args.topic, "--topic")
    _require(args.start, "--start")
    body = {
        "topic": args.topic,
        "type": 2,  # Scheduled
        "start_time": args.start,
        "duration": args.duration,
        "timezone": os.environ.get("TZ", "Asia/Singapore"),
    }
    if args.agenda:
        body["agenda"] = args.agenda
    if args.password:
        body["password"] = args.password

    data = api("POST", f"/users/{_user_id()}/meetings", json=body)
    print(f"Meeting created!")
    print(f"  ID: {data.get('id')}")
    print(f"  Topic: {data.get('topic')}")
    print(f"  Start: {data.get('start_time')}")
    print(f"  Join URL: {data.get('join_url')}")
    print(f"  Password: {data.get('password', 'N/A')}")


def cmd_meetings_delete(args):
    """Delete a meeting."""
    _require(args.meeting_id, "meeting_id")
    api("DELETE", f"/meetings/{args.meeting_id}")
    print(f"Meeting {args.meeting_id} deleted.")


def cmd_meetings_update(args):
    """Update a meeting."""
    _require(args.meeting_id, "meeting_id")
    body = {}
    settings = {}
    if args.topic:
        body["topic"] = args.topic
    if args.start:
        body["start_time"] = args.start
    if args.duration:
        body["duration"] = args.duration
    if args.join_before_host is not None:
        settings["join_before_host"] = args.join_before_host
    if args.auto_recording:
        settings["auto_recording"] = args.auto_recording
    if args.waiting_room is not None:
        settings["waiting_room"] = args.waiting_room
    if settings:
        body["settings"] = settings
    if not body:
        print("Nothing to update.")
        return
    api("PATCH", f"/meetings/{args.meeting_id}", json=body)
    print(f"Meeting {args.meeting_id} updated.")


# === Recordings ===

def cmd_recordings_list(args):
    """List cloud recordings."""
    params = {"page_size": 30}
    if args.from_date:
        params["from"] = args.from_date
    if args.to_date:
        params["to"] = args.to_date
    data = api("GET", f"/users/{_user_id()}/recordings", params=params)
    meetings = data.get("meetings", [])
    if not meetings:
        print("No recordings found.")
        return
    for m in meetings:
        topic = m.get("topic", "Untitled")
        start = m.get("start_time", "?")
        mid = m.get("id", "?")
        files = m.get("recording_files", [])
        print(f"  [{mid}] {topic} ({start})")
        for f in files:
            print(f"    {f.get('recording_type', '?')}: {f.get('download_url', '?')}")
        print()


def cmd_recordings_get(args):
    """Get recording details."""
    data = api("GET", f"/meetings/{args.meeting_id}/recordings")
    print(json.dumps(data, indent=2))


def cmd_recordings_download(args):
    """Download recording files for a meeting."""
    _require(args.meeting_id, "meeting_id")
    data = api("GET", f"/meetings/{args.meeting_id}/recordings")
    files = data.get("recording_files", [])
    if not files:
        print("No recording files found.")
        return

    topic = data.get("topic", "recording").replace(" ", "_").replace("/", "_")
    out_dir = args.output or "."
    os.makedirs(out_dir, exist_ok=True)
    token = get_token()

    for f in files:
        url = f.get("download_url")
        if not url:
            continue
        rec_type = f.get("recording_type", "unknown")
        ext = f.get("file_extension", "mp4").lower()
        fname = f"{topic}_{rec_type}_{f.get('id', 'file')}.{ext}"
        fpath = os.path.join(out_dir, fname)

        print(f"Downloading {rec_type} → {fpath} ...")
        resp = requests.get(f"{url}?access_token={token}", stream=True, timeout=60)
        resp.raise_for_status()
        with open(fpath, "wb") as out:
            for chunk in resp.iter_content(chunk_size=8192):
                out.write(chunk)
        size_mb = os.path.getsize(fpath) / (1024 * 1024)
        print(f"  ✓ {size_mb:.1f} MB")

    print(f"\nDownloaded {len(files)} file(s).")


def cmd_recordings_download_transcript(args):
    """Download transcript files for a meeting recording."""
    _require(args.meeting_id, "meeting_id")
    data = api("GET", f"/meetings/{args.meeting_id}/recordings")
    files = data.get("recording_files", [])
    transcript_files = [f for f in files if f.get("recording_type") in ("audio_transcript", "chat_file", "timeline", "closed_caption")]
    # Also check for separate transcript files
    transcript_files += [f for f in files if f.get("file_extension", "").lower() in ("vtt", "txt", "srt")]

    if not transcript_files:
        print("No transcript files found in recording.")
        return

    topic = data.get("topic", "recording").replace(" ", "_").replace("/", "_")
    out_dir = args.output or "."
    os.makedirs(out_dir, exist_ok=True)
    token = get_token()

    downloaded = 0
    for f in transcript_files:
        url = f.get("download_url")
        if not url:
            continue
        rec_type = f.get("recording_type", "transcript")
        ext = f.get("file_extension", "vtt").lower()
        fname = f"{topic}_{rec_type}_{f.get('id', 'file')}.{ext}"
        fpath = os.path.join(out_dir, fname)

        print(f"Downloading {rec_type} → {fpath} ...")
        resp = requests.get(f"{url}?access_token={token}", stream=True, timeout=60)
        resp.raise_for_status()
        with open(fpath, "wb") as out:
            for chunk in resp.iter_content(chunk_size=8192):
                out.write(chunk)
        size_kb = os.path.getsize(fpath) / 1024
        print(f"  ✓ {size_kb:.1f} KB")
        downloaded += 1

    print(f"\nDownloaded {downloaded} transcript file(s).")


def cmd_recordings_download_summary(args):
    """Download AI Companion meeting summary and save to file."""
    _require(args.meeting_id, "meeting_id (use meeting UUID)")
    encoded_id = quote(quote(args.meeting_id, safe=""), safe="")
    data = api("GET", f"/meetings/{encoded_id}/meeting_summary")

    topic = data.get("meeting_topic", "meeting").replace(" ", "_").replace("/", "_")
    out_dir = args.output or "."
    os.makedirs(out_dir, exist_ok=True)

    # Build markdown content
    lines = []
    lines.append(f"# {data.get('meeting_topic', 'Meeting Summary')}")
    lines.append(f"")
    lines.append(f"- **Date:** {data.get('meeting_start_time', '?')} — {data.get('meeting_end_time', '?')}")
    lines.append(f"- **Host:** {data.get('meeting_host_email', '?')}")
    if data.get("summary_title"):
        lines.append(f"- **Title:** {data['summary_title']}")
    lines.append("")

    summary = data.get("meeting_summary", data.get("summary", {}))
    if isinstance(summary, str):
        lines.append(summary)
    elif isinstance(summary, dict):
        overview = summary.get("summary_overview", summary.get("overview", ""))
        if overview:
            lines.append("## Summary")
            lines.append(overview)
            lines.append("")
        details = summary.get("summary_details", summary.get("details", []))
        if details:
            lines.append("## Details")
            for d in details if isinstance(details, list) else [details]:
                if isinstance(d, dict):
                    label = d.get("label", "")
                    content = d.get("content", "")
                    if label:
                        lines.append(f"### {label}")
                    lines.append(content)
                    lines.append("")
                else:
                    lines.append(str(d))
        next_steps = summary.get("next_steps", [])
        if next_steps:
            lines.append("## Next Steps")
            for step in next_steps:
                lines.append(f"- {step}")

    fname = f"{topic}_ai_summary.md"
    fpath = os.path.join(out_dir, fname)
    with open(fpath, "w") as f:
        f.write("\n".join(lines))
    print(f"✅ AI summary saved to {fpath}")


def cmd_recordings_delete(args):
    """Delete a recording."""
    _require(args.meeting_id, "meeting_id")
    api("DELETE", f"/meetings/{args.meeting_id}/recordings")
    print(f"Recordings for meeting {args.meeting_id} deleted.")


# === Users ===

def cmd_users_me(args):
    """Get my profile."""
    data = api("GET", f"/users/{_user_id()}")
    print(f"Name: {data.get('first_name')} {data.get('last_name')}")
    print(f"Email: {data.get('email')}")
    print(f"Type: {data.get('type')} (1=Basic, 2=Licensed, 3=On-Prem)")
    print(f"PMI: {data.get('pmi')}")
    print(f"Timezone: {data.get('timezone')}")
    print(f"Status: {data.get('status')}")


def cmd_users_list(args):
    """List users (admin)."""
    data = api("GET", "/users", params={"page_size": 30})
    for u in data.get("users", []):
        print(f"  {u.get('email')} — {u.get('first_name')} {u.get('last_name')} (type={u.get('type')})")


# === Chat ===

def cmd_chat_channels(args):
    """List chat channels."""
    data = api("GET", f"/chat/users/{_user_id()}/channels", params={"page_size": 50})
    for ch in data.get("channels", []):
        print(f"  [{ch.get('id')}] {ch.get('name')} (type={ch.get('type')})")


def cmd_chat_messages(args):
    """List messages in a channel."""
    params = {"page_size": 20}
    data = api("GET", f"/chat/users/{_user_id()}/messages", params={**params, "to_channel": args.channel_id})
    for msg in data.get("messages", []):
        sender = msg.get("sender", "?")
        text = msg.get("message", "")
        ts = msg.get("date_time", "?")
        print(f"  [{ts}] {sender}: {text}")


def cmd_chat_send(args):
    """Send a message to a channel."""
    body = {"message": args.message, "to_channel": args.channel_id}
    api("POST", f"/chat/users/{_user_id()}/messages", json=body)
    print(f"Message sent to channel {args.channel_id}.")


def cmd_chat_dm(args):
    """Send a direct message."""
    body = {"message": args.message, "to_contact": args.email}
    api("POST", f"/chat/users/{_user_id()}/messages", json=body)
    print(f"DM sent to {args.email}.")


def cmd_chat_contacts(args):
    """List chat contacts."""
    data = api("GET", "/contacts", params={"page_size": 50, "type": "company"})
    for c in data.get("contacts", []):
        print(f"  {c.get('email', '?')} — {c.get('first_name', '')} {c.get('last_name', '')}")


# === Phone ===

def cmd_phone_calls(args):
    """List call logs."""
    params = {"page_size": 30}
    if args.from_date:
        params["from"] = args.from_date
    if args.to_date:
        params["to"] = args.to_date
    data = api("GET", f"/phone/users/{_user_id()}/call_logs", params=params)
    for c in data.get("call_logs", []):
        direction = c.get("direction", "?")
        number = c.get("caller_number") or c.get("callee_number", "?")
        duration = c.get("duration", "?")
        ts = c.get("date_time", "?")
        print(f"  [{ts}] {direction} {number} ({duration}s)")


# === Meeting Summaries (AI Companion) ===

def cmd_summary_get(args):
    """Get AI meeting summary for a specific meeting."""
    _require(args.meeting_id, "meeting_id (use meeting UUID from 'summary list')")
    encoded_id = quote(quote(args.meeting_id, safe=""), safe="")
    data = api("GET", f"/meetings/{encoded_id}/meeting_summary")
    print(f"Meeting: {data.get('meeting_topic', 'Untitled')}")
    print(f"Date: {data.get('meeting_start_time', '?')} — {data.get('meeting_end_time', '?')}")
    print(f"Host: {data.get('meeting_host_email', '?')}")
    if data.get("summary_title"):
        print(f"Title: {data['summary_title']}")
    print()

    # Try multiple possible content locations
    summary = data.get("meeting_summary", data.get("summary", {}))
    if isinstance(summary, str):
        print(summary)
        return
    if isinstance(summary, dict):
        overview = summary.get("summary_overview", summary.get("overview", ""))
        if overview:
            print("=== Summary ===")
            print(overview)
            print()
        details = summary.get("summary_details", summary.get("details", []))
        if details:
            print("=== Details ===")
            for d in details if isinstance(details, list) else [details]:
                if isinstance(d, dict):
                    label = d.get("label", "")
                    content = d.get("content", "")
                    if label:
                        print(f"\n**{label}**")
                    print(content)
                else:
                    print(d)
            print()
        next_steps = summary.get("next_steps", [])
        if next_steps:
            print("=== Next Steps ===")
            for step in next_steps:
                print(f"  • {step}")
        if not overview and not details and not next_steps:
            print("(Summary metadata exists but no content available — meeting may have been too short)")

    # Also check top-level summary_details
    top_details = data.get("summary_details", [])
    if top_details:
        print("=== Details ===")
        for d in top_details:
            print(d)

    if not summary and not top_details:
        print("(No summary content available)")


def cmd_summary_list(args):
    """List AI meeting summaries."""
    params = {"page_size": 20}
    if args.from_date:
        params["from"] = args.from_date
    if args.to_date:
        params["to"] = args.to_date
    data = api("GET", "/meetings/meeting_summaries", params=params)
    summaries = data.get("summaries", [])
    if not summaries:
        print("No meeting summaries found.")
        return
    for s in summaries:
        uuid = s.get("meeting_uuid", "?")
        topic = s.get("meeting_topic", "Untitled")
        start = s.get("meeting_start_time", "?")
        print(f"  [{uuid}] {topic} ({start})")


# === Main ===

def main():
    parser = argparse.ArgumentParser(description="Zoom API CLI")
    sub = parser.add_subparsers(dest="group", required=True)

    # Meetings
    meetings = sub.add_parser("meetings")
    msub = meetings.add_subparsers(dest="action", required=True)

    msub.add_parser("list")
    msub.add_parser("live")
    p = msub.add_parser("rtms-start")
    p.add_argument("meeting_id")
    p = msub.add_parser("rtms-stop")
    p.add_argument("meeting_id")
    p = msub.add_parser("get")
    p.add_argument("meeting_id")
    p = msub.add_parser("create")
    p.add_argument("--topic", required=True)
    p.add_argument("--start", required=True, help="ISO datetime")
    p.add_argument("--duration", type=int, default=30, help="Minutes")
    p.add_argument("--agenda")
    p.add_argument("--password")
    p = msub.add_parser("delete")
    p.add_argument("meeting_id")
    p = msub.add_parser("update")
    p.add_argument("meeting_id")
    p.add_argument("--topic")
    p.add_argument("--start")
    p.add_argument("--duration", type=int)
    p.add_argument("--join-before-host", dest="join_before_host", type=lambda x: x.lower() in ("true", "1", "yes"), default=None)
    p.add_argument("--auto-recording", dest="auto_recording", choices=["local", "cloud", "none"])
    p.add_argument("--waiting-room", dest="waiting_room", type=lambda x: x.lower() in ("true", "1", "yes"), default=None)

    # Recordings
    recordings = sub.add_parser("recordings")
    rsub = recordings.add_subparsers(dest="action", required=True)
    p = rsub.add_parser("list")
    p.add_argument("--from", dest="from_date")
    p.add_argument("--to", dest="to_date")
    p = rsub.add_parser("get")
    p.add_argument("meeting_id")
    p = rsub.add_parser("download")
    p.add_argument("meeting_id")
    p.add_argument("--output", "-o", help="Output directory (default: current)")
    p = rsub.add_parser("download-transcript")
    p.add_argument("meeting_id")
    p.add_argument("--output", "-o", help="Output directory (default: current)")
    p = rsub.add_parser("download-summary")
    p.add_argument("meeting_id", help="Meeting UUID")
    p.add_argument("--output", "-o", help="Output directory (default: current)")
    p = rsub.add_parser("delete")
    p.add_argument("meeting_id")

    # Users
    users = sub.add_parser("users")
    usub = users.add_subparsers(dest="action", required=True)
    usub.add_parser("me")
    usub.add_parser("list")

    # Chat
    chat = sub.add_parser("chat")
    csub = chat.add_subparsers(dest="action", required=True)
    csub.add_parser("channels")
    p = csub.add_parser("messages")
    p.add_argument("channel_id")
    p = csub.add_parser("send")
    p.add_argument("channel_id")
    p.add_argument("message")
    p = csub.add_parser("dm")
    p.add_argument("email")
    p.add_argument("message")
    csub.add_parser("contacts")

    # Summaries (AI Companion)
    summaries = sub.add_parser("summary")
    ssub = summaries.add_subparsers(dest="action", required=True)
    p = ssub.add_parser("get")
    p.add_argument("meeting_id")
    p = ssub.add_parser("list")
    p.add_argument("--from", dest="from_date")
    p.add_argument("--to", dest="to_date")

    # Phone
    phone = sub.add_parser("phone")
    psub = phone.add_subparsers(dest="action", required=True)
    p = psub.add_parser("calls")
    p.add_argument("--from", dest="from_date")
    p.add_argument("--to", dest="to_date")

    args = parser.parse_args()

    cmd_map = {
        ("meetings", "list"): cmd_meetings_list,
        ("meetings", "live"): cmd_meetings_live,
        ("meetings", "rtms-start"): cmd_meetings_rtms_start,
        ("meetings", "rtms-stop"): cmd_meetings_rtms_stop,
        ("meetings", "get"): cmd_meetings_get,
        ("meetings", "create"): cmd_meetings_create,
        ("meetings", "delete"): cmd_meetings_delete,
        ("meetings", "update"): cmd_meetings_update,
        ("recordings", "list"): cmd_recordings_list,
        ("recordings", "get"): cmd_recordings_get,
        ("recordings", "download"): cmd_recordings_download,
        ("recordings", "download-transcript"): cmd_recordings_download_transcript,
        ("recordings", "download-summary"): cmd_recordings_download_summary,
        ("recordings", "delete"): cmd_recordings_delete,
        ("users", "me"): cmd_users_me,
        ("users", "list"): cmd_users_list,
        ("chat", "channels"): cmd_chat_channels,
        ("chat", "messages"): cmd_chat_messages,
        ("chat", "send"): cmd_chat_send,
        ("chat", "dm"): cmd_chat_dm,
        ("chat", "contacts"): cmd_chat_contacts,
        ("summary", "get"): cmd_summary_get,
        ("summary", "list"): cmd_summary_list,
        ("phone", "calls"): cmd_phone_calls,
    }

    func = cmd_map.get((args.group, args.action))
    if func:
        func(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
