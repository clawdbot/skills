#!/usr/bin/env python3
"""
Example: Integrating sports-ticker with agent-protocol.

This shows how to modify sports-ticker to publish events when goals are scored.
Add this to your sports-ticker/scripts/live_monitor.py
"""

import sys
from pathlib import Path

# Add agent-protocol to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "agent-protocol" / "scripts"))

from publish import publish_event

def publish_goal_event(team_name, team_emoji, scorer, opponent, score, minute):
    """Publish a goal event to the agent protocol bus."""
    success, event_id = publish_event(
        event_type="sports.goal_scored",
        source_agent="sports-ticker",
        payload={
            "team": team_name,
            "team_emoji": team_emoji,
            "scorer": scorer,
            "opponent": opponent,
            "score": score,
            "minute": minute,
            "sport": "soccer"
        }
    )
    
    if success:
        print(f"Published goal event: {event_id}")
    else:
        print(f"Failed to publish goal event: {event_id}", file=sys.stderr)

def publish_match_start_event(team_name, team_emoji, opponent, league):
    """Publish match start event."""
    publish_event(
        event_type="sports.match_started",
        source_agent="sports-ticker",
        payload={
            "team": team_name,
            "team_emoji": team_emoji,
            "opponent": opponent,
            "league": league
        }
    )

def publish_match_end_event(team_name, result, score):
    """Publish match end event."""
    publish_event(
        event_type="sports.match_ended",
        source_agent="sports-ticker",
        payload={
            "team": team_name,
            "result": result,  # "WIN", "LOSS", "DRAW"
            "score": score
        }
    )

# In your sports-ticker live_monitor.py, add these calls:
#
# When goal is detected:
# publish_goal_event(team_name, team_emoji, player, opponent, f"{home_score}-{away_score}", clock)
#
# When match starts:
# publish_match_start_event(team_name, team_emoji, opponent, league)
#
# When match ends:
# publish_match_end_event(team_name, result, f"{home_score}-{away_score}")
