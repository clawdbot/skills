#!/usr/bin/env python3
"""
gcal-pro: Core Calendar Operations Module
Handles all Google Calendar API operations with timezone awareness.
"""

import sys
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Tuple
from zoneinfo import ZoneInfo

from dateutil import parser as date_parser
from dateutil.relativedelta import relativedelta

from gcal_auth import get_calendar_service, is_pro_user

# Default timezone (can be overridden)
DEFAULT_TIMEZONE = "America/New_York"


def get_timezone() -> ZoneInfo:
    """Get the configured timezone."""
    # Could be extended to read from config
    return ZoneInfo(DEFAULT_TIMEZONE)


def now_local() -> datetime:
    """Get current time in local timezone."""
    return datetime.now(get_timezone())


def format_datetime(dt: datetime) -> str:
    """Format datetime for display."""
    return dt.strftime("%a, %b %d at %I:%M %p")


def format_datetime_iso(dt: datetime) -> str:
    """Format datetime as ISO 8601 for API."""
    return dt.isoformat()


def parse_datetime(text: str, reference: datetime = None) -> datetime:
    """
    Parse natural language datetime string.
    
    Args:
        text: Natural language date/time (e.g., "tomorrow 2pm", "next Friday")
        reference: Reference datetime for relative parsing
        
    Returns:
        Parsed datetime with timezone
    """
    if reference is None:
        reference = now_local()
    
    tz = get_timezone()
    
    # Handle common relative terms
    text_lower = text.lower().strip()
    
    if text_lower == "today":
        return reference.replace(hour=9, minute=0, second=0, microsecond=0)
    elif text_lower == "tomorrow":
        return (reference + timedelta(days=1)).replace(hour=9, minute=0, second=0, microsecond=0)
    elif text_lower == "next week":
        return (reference + timedelta(weeks=1)).replace(hour=9, minute=0, second=0, microsecond=0)
    
    # Use dateutil parser for everything else
    try:
        parsed = date_parser.parse(text, fuzzy=True, default=reference)
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=tz)
        return parsed
    except Exception:
        raise ValueError(f"Could not parse datetime: {text}")


# =============================================================================
# READ OPERATIONS (Free Tier)
# =============================================================================

def list_events(
    time_min: datetime = None,
    time_max: datetime = None,
    max_results: int = 10,
    calendar_id: str = "primary"
) -> List[Dict[str, Any]]:
    """
    List calendar events within a time range.
    
    Args:
        time_min: Start of range (default: now)
        time_max: End of range (default: end of today)
        max_results: Maximum events to return
        calendar_id: Calendar ID (default: primary)
        
    Returns:
        List of event dictionaries
    """
    service = get_calendar_service()
    if not service:
        return []
    
    if time_min is None:
        time_min = now_local()
    if time_max is None:
        time_max = time_min.replace(hour=23, minute=59, second=59)
    
    try:
        events_result = service.events().list(
            calendarId=calendar_id,
            timeMin=format_datetime_iso(time_min),
            timeMax=format_datetime_iso(time_max),
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime"
        ).execute()
        
        events = events_result.get("items", [])
        return [_parse_event(e) for e in events]
    except Exception as e:
        print(f"Error listing events: {e}")
        return []


def get_today() -> List[Dict[str, Any]]:
    """Get today's events."""
    now = now_local()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = now.replace(hour=23, minute=59, second=59, microsecond=0)
    return list_events(time_min=start, time_max=end, max_results=20)


def get_tomorrow() -> List[Dict[str, Any]]:
    """Get tomorrow's events."""
    now = now_local()
    tomorrow = now + timedelta(days=1)
    start = tomorrow.replace(hour=0, minute=0, second=0, microsecond=0)
    end = tomorrow.replace(hour=23, minute=59, second=59, microsecond=0)
    return list_events(time_min=start, time_max=end, max_results=20)


def get_week() -> List[Dict[str, Any]]:
    """Get this week's events (next 7 days)."""
    now = now_local()
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=7)
    return list_events(time_min=start, time_max=end, max_results=50)


def get_event(event_id: str, calendar_id: str = "primary") -> Optional[Dict[str, Any]]:
    """Get a specific event by ID."""
    service = get_calendar_service()
    if not service:
        return None
    
    try:
        event = service.events().get(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()
        return _parse_event(event)
    except Exception as e:
        print(f"Error getting event: {e}")
        return None


def search_events(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Search for events by text."""
    service = get_calendar_service()
    if not service:
        return []
    
    now = now_local()
    
    try:
        events_result = service.events().list(
            calendarId="primary",
            timeMin=format_datetime_iso(now - timedelta(days=30)),
            timeMax=format_datetime_iso(now + timedelta(days=90)),
            maxResults=max_results,
            singleEvents=True,
            orderBy="startTime",
            q=query
        ).execute()
        
        events = events_result.get("items", [])
        return [_parse_event(e) for e in events]
    except Exception as e:
        print(f"Error searching events: {e}")
        return []


def find_free_time(
    duration_minutes: int = 60,
    time_min: datetime = None,
    time_max: datetime = None,
    calendar_id: str = "primary"
) -> List[Tuple[datetime, datetime]]:
    """
    Find free time slots.
    
    Args:
        duration_minutes: Minimum slot duration
        time_min: Start of search range
        time_max: End of search range
        
    Returns:
        List of (start, end) tuples for free slots
    """
    if time_min is None:
        time_min = now_local()
    if time_max is None:
        time_max = time_min + timedelta(days=7)
    
    # Get all events in range
    events = list_events(time_min=time_min, time_max=time_max, max_results=100)
    
    # Find gaps
    free_slots = []
    current = time_min
    
    for event in events:
        event_start = event.get("start_dt")
        event_end = event.get("end_dt")
        
        if event_start and current < event_start:
            gap = (event_start - current).total_seconds() / 60
            if gap >= duration_minutes:
                free_slots.append((current, event_start))
        
        if event_end and event_end > current:
            current = event_end
    
    # Check remaining time after last event
    if current < time_max:
        gap = (time_max - current).total_seconds() / 60
        if gap >= duration_minutes:
            free_slots.append((current, time_max))
    
    return free_slots


def list_calendars() -> List[Dict[str, Any]]:
    """List all available calendars."""
    service = get_calendar_service()
    if not service:
        return []
    
    try:
        calendars_result = service.calendarList().list().execute()
        calendars = calendars_result.get("items", [])
        return [
            {
                "id": cal.get("id"),
                "summary": cal.get("summary"),
                "primary": cal.get("primary", False),
                "access_role": cal.get("accessRole")
            }
            for cal in calendars
        ]
    except Exception as e:
        print(f"Error listing calendars: {e}")
        return []


# =============================================================================
# WRITE OPERATIONS (Pro Tier Only)
# =============================================================================

def _require_pro(operation: str) -> bool:
    """Check if Pro tier is required for an operation."""
    if not is_pro_user():
        print(f"⚠️ {operation} requires gcal-pro Pro tier ($12 one-time).")
        print("  Upgrade at: [your-gumroad-link]")
        return False
    return True


def create_event(
    summary: str,
    start: datetime,
    end: datetime = None,
    description: str = None,
    location: str = None,
    attendees: List[str] = None,
    calendar_id: str = "primary",
    confirmed: bool = False
) -> Optional[Dict[str, Any]]:
    """
    Create a new calendar event.
    
    Args:
        summary: Event title
        start: Start datetime
        end: End datetime (default: 1 hour after start)
        description: Event description
        location: Event location
        attendees: List of attendee emails
        calendar_id: Target calendar
        confirmed: Skip confirmation if True
        
    Returns:
        Created event or None
    """
    if not _require_pro("Creating events"):
        return None
    
    service = get_calendar_service()
    if not service:
        return None
    
    if end is None:
        end = start + timedelta(hours=1)
    
    # Build event body
    event_body = {
        "summary": summary,
        "start": {
            "dateTime": format_datetime_iso(start),
            "timeZone": str(get_timezone())
        },
        "end": {
            "dateTime": format_datetime_iso(end),
            "timeZone": str(get_timezone())
        }
    }
    
    if description:
        event_body["description"] = description
    if location:
        event_body["location"] = location
    if attendees:
        event_body["attendees"] = [{"email": email} for email in attendees]
    
    # Confirmation check
    if not confirmed:
        print(f"\n📅 Create event:")
        print(f"   Title: {summary}")
        print(f"   When:  {format_datetime(start)} - {format_datetime(end)}")
        if location:
            print(f"   Where: {location}")
        if attendees:
            print(f"   With:  {', '.join(attendees)}")
        # In actual skill use, Clawdbot will handle confirmation
        # This is for CLI testing
    
    try:
        event = service.events().insert(
            calendarId=calendar_id,
            body=event_body,
            sendUpdates="all" if attendees else "none"
        ).execute()
        
        print(f"✓ Event created: {event.get('htmlLink')}")
        return _parse_event(event)
    except Exception as e:
        print(f"Error creating event: {e}")
        return None


def quick_add(text: str, calendar_id: str = "primary") -> Optional[Dict[str, Any]]:
    """
    Quick add event using natural language.
    
    Args:
        text: Natural language event description (e.g., "Lunch with Alex tomorrow at noon")
        calendar_id: Target calendar
        
    Returns:
        Created event or None
    """
    if not _require_pro("Quick add"):
        return None
    
    service = get_calendar_service()
    if not service:
        return None
    
    try:
        event = service.events().quickAdd(
            calendarId=calendar_id,
            text=text
        ).execute()
        
        parsed = _parse_event(event)
        print(f"✓ Event created: {parsed.get('summary')}")
        print(f"   When: {format_datetime(parsed.get('start_dt'))}")
        return parsed
    except Exception as e:
        print(f"Error in quick add: {e}")
        return None


def update_event(
    event_id: str,
    summary: str = None,
    start: datetime = None,
    end: datetime = None,
    description: str = None,
    location: str = None,
    calendar_id: str = "primary",
    confirmed: bool = False
) -> Optional[Dict[str, Any]]:
    """
    Update an existing event.
    
    Args:
        event_id: ID of event to update
        summary: New title (optional)
        start: New start time (optional)
        end: New end time (optional)
        description: New description (optional)
        location: New location (optional)
        calendar_id: Calendar ID
        confirmed: Skip confirmation if True
        
    Returns:
        Updated event or None
    """
    if not _require_pro("Updating events"):
        return None
    
    service = get_calendar_service()
    if not service:
        return None
    
    # Get existing event
    try:
        event = service.events().get(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()
    except Exception as e:
        print(f"Event not found: {e}")
        return None
    
    # Apply updates
    if summary:
        event["summary"] = summary
    if start:
        event["start"] = {
            "dateTime": format_datetime_iso(start),
            "timeZone": str(get_timezone())
        }
    if end:
        event["end"] = {
            "dateTime": format_datetime_iso(end),
            "timeZone": str(get_timezone())
        }
    if description is not None:
        event["description"] = description
    if location is not None:
        event["location"] = location
    
    # Confirmation
    if not confirmed:
        print(f"\n✏️ Update event: {event.get('summary')}")
        if summary:
            print(f"   New title: {summary}")
        if start:
            print(f"   New start: {format_datetime(start)}")
        if end:
            print(f"   New end: {format_datetime(end)}")
    
    try:
        updated = service.events().update(
            calendarId=calendar_id,
            eventId=event_id,
            body=event
        ).execute()
        
        print(f"✓ Event updated")
        return _parse_event(updated)
    except Exception as e:
        print(f"Error updating event: {e}")
        return None


def delete_event(
    event_id: str,
    calendar_id: str = "primary",
    confirmed: bool = False
) -> bool:
    """
    Delete an event.
    
    Args:
        event_id: ID of event to delete
        calendar_id: Calendar ID
        confirmed: Skip confirmation if True
        
    Returns:
        True if deleted successfully
    """
    if not _require_pro("Deleting events"):
        return False
    
    service = get_calendar_service()
    if not service:
        return False
    
    # Get event details for confirmation
    try:
        event = service.events().get(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()
    except Exception as e:
        print(f"Event not found: {e}")
        return False
    
    parsed = _parse_event(event)
    
    if not confirmed:
        print(f"\n🗑️ Delete event:")
        print(f"   Title: {parsed.get('summary')}")
        print(f"   When:  {format_datetime(parsed.get('start_dt'))}")
        print(f"\n   ⚠️ This action cannot be undone!")
    
    try:
        service.events().delete(
            calendarId=calendar_id,
            eventId=event_id
        ).execute()
        
        print(f"✓ Event deleted")
        return True
    except Exception as e:
        print(f"Error deleting event: {e}")
        return False


# =============================================================================
# HELPERS
# =============================================================================

def _parse_event(event: Dict[str, Any]) -> Dict[str, Any]:
    """Parse raw API event into clean format."""
    tz = get_timezone()
    
    # Parse start time
    start = event.get("start", {})
    start_dt = None
    if "dateTime" in start:
        start_dt = date_parser.parse(start["dateTime"])
        if start_dt.tzinfo is None:
            start_dt = start_dt.replace(tzinfo=tz)
    elif "date" in start:
        # All-day event
        start_dt = date_parser.parse(start["date"]).replace(tzinfo=tz)
    
    # Parse end time
    end = event.get("end", {})
    end_dt = None
    if "dateTime" in end:
        end_dt = date_parser.parse(end["dateTime"])
        if end_dt.tzinfo is None:
            end_dt = end_dt.replace(tzinfo=tz)
    elif "date" in end:
        end_dt = date_parser.parse(end["date"]).replace(tzinfo=tz)
    
    return {
        "id": event.get("id"),
        "summary": event.get("summary", "(No title)"),
        "description": event.get("description"),
        "location": event.get("location"),
        "start": start.get("dateTime") or start.get("date"),
        "end": end.get("dateTime") or end.get("date"),
        "start_dt": start_dt,
        "end_dt": end_dt,
        "all_day": "date" in start,
        "attendees": [a.get("email") for a in event.get("attendees", [])],
        "html_link": event.get("htmlLink"),
        "status": event.get("status"),
        "organizer": event.get("organizer", {}).get("email")
    }


def format_events_for_display(events: List[Dict[str, Any]]) -> str:
    """Format events list for chat display."""
    if not events:
        return "📭 No events found."
    
    lines = []
    current_date = None
    
    for event in events:
        start_dt = event.get("start_dt")
        if not start_dt:
            continue
        
        # Add date header if new day
        event_date = start_dt.date()
        if event_date != current_date:
            current_date = event_date
            lines.append(f"\n📅 **{start_dt.strftime('%A, %B %d')}**")
        
        # Format event
        if event.get("all_day"):
            time_str = "All day"
        else:
            time_str = start_dt.strftime("%I:%M %p").lstrip("0")
        
        summary = event.get("summary", "(No title)")
        location = event.get("location")
        
        line = f"  • {time_str} — {summary}"
        if location:
            line += f" 📍 {location}"
        
        lines.append(line)
    
    return "\n".join(lines)


# =============================================================================
# MORNING BRIEF (Pro Feature)
# =============================================================================

def generate_morning_brief() -> str:
    """
    Generate morning brief for Clawdbot cron.
    
    Returns:
        Formatted morning brief text
    """
    now = now_local()
    today_events = get_today()
    
    # Build brief
    lines = [f"☀️ **Good morning! Here's your day:**"]
    lines.append(f"📆 {now.strftime('%A, %B %d, %Y')}")
    lines.append("")
    
    if not today_events:
        lines.append("🎉 Your calendar is clear today!")
    else:
        lines.append(f"You have **{len(today_events)} event(s)** today:")
        lines.append(format_events_for_display(today_events))
    
    # Add tomorrow preview
    tomorrow_events = get_tomorrow()
    if tomorrow_events:
        lines.append(f"\n👀 **Tomorrow:** {len(tomorrow_events)} event(s)")
    
    return "\n".join(lines)


# CLI for testing
if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="gcal-pro calendar operations")
    parser.add_argument("command", choices=[
        "today", "tomorrow", "week", "search", "brief",
        "create", "quick", "delete", "calendars", "free"
    ])
    parser.add_argument("--query", "-q", help="Search query or event text")
    parser.add_argument("--id", help="Event ID for delete/update")
    parser.add_argument("--yes", "-y", action="store_true", help="Skip confirmation")
    
    args = parser.parse_args()
    
    if args.command == "today":
        events = get_today()
        print(format_events_for_display(events))
    
    elif args.command == "tomorrow":
        events = get_tomorrow()
        print(format_events_for_display(events))
    
    elif args.command == "week":
        events = get_week()
        print(format_events_for_display(events))
    
    elif args.command == "search":
        if not args.query:
            print("Error: --query required for search")
            sys.exit(1)
        events = search_events(args.query)
        print(format_events_for_display(events))
    
    elif args.command == "brief":
        print(generate_morning_brief())
    
    elif args.command == "quick":
        if not args.query:
            print("Error: --query required for quick add")
            sys.exit(1)
        quick_add(args.query)
    
    elif args.command == "delete":
        if not args.id:
            print("Error: --id required for delete")
            sys.exit(1)
        delete_event(args.id, confirmed=args.yes)
    
    elif args.command == "calendars":
        cals = list_calendars()
        for cal in cals:
            primary = " (primary)" if cal.get("primary") else ""
            print(f"  • {cal.get('summary')}{primary}")
            print(f"    ID: {cal.get('id')}")
    
    elif args.command == "free":
        slots = find_free_time(duration_minutes=60)
        if not slots:
            print("No free slots found in the next 7 days.")
        else:
            print("Free 1-hour slots this week:")
            for start, end in slots[:10]:
                print(f"  • {format_datetime(start)} - {format_datetime(end)}")

