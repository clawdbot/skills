#!/usr/bin/env python3
"""
Daily Standup Generator - Creates a concise summary of today's priorities.
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

from utils import load_tasks, check_due_date


def generate_standup(date_str: str = None, json_output: bool = False) -> str | dict:
    """Generate daily standup summary.
    
    Args:
        date_str: Optional date string (YYYY-MM-DD) for standup
        json_output: If True, return dict instead of markdown
    
    Returns:
        String summary (default) or dict if json_output=True
    """
    _, tasks_data = load_tasks()
    
    today = datetime.now()
    if date_str:
        try:
            standup_date = datetime.strptime(date_str, '%Y-%m-%d').date()
        except ValueError:
            standup_date = today.date()
    else:
        standup_date = today.date()
    
    date_display = standup_date.strftime("%A, %B %d")
    
    # Build output
    output = {
        'date': str(standup_date),
        'date_display': date_display,
        'priority': None,
        'due_today': [],
        'blocking': [],
        'high_priority': [],
        'completed': [],
        'upcoming': [],
    }
    
    # #1 Priority (blocking tasks first, then high priority)
    if tasks_data['blocking']:
        output['priority'] = tasks_data['blocking'][0]
    elif tasks_data['high_priority']:
        output['priority'] = tasks_data['high_priority'][0]
    
    # Due today
    output['due_today'] = tasks_data['due_today']
    
    # Blocking others
    output['blocking'] = tasks_data['blocking']
    
    # Other high priority
    output['high_priority'] = [t for t in tasks_data['high_priority'] 
                               if t not in tasks_data['blocking']]
    
    # Completed
    output['completed'] = tasks_data['done']
    
    # Upcoming
    output['upcoming'] = tasks_data['upcoming']
    
    if json_output:
        return output
    
    # Format as markdown
    lines = [f"📋 **Daily Standup — {date_display}**\n"]
    
    if output['priority']:
        priority = output['priority']
        lines.append(f"🎯 **#1 Priority:** {priority['title']}")
        if priority.get('blocks'):
            lines.append(f"   ↳ Blocking: {priority['blocks']}")
        lines.append("")
    
    if output['due_today']:
        lines.append("⏰ **Due Today:**")
        for t in output['due_today'][:5]:
            lines.append(f"  • {t['title']}")
        lines.append("")
    
    if output['blocking']:
        lines.append("🚧 **Blocking Others:**")
        for t in output['blocking'][:3]:
            lines.append(f"  • {t['title']} → {t.get('blocks', '?')}")
        lines.append("")
    
    if output['high_priority']:
        lines.append("🔴 **High Priority:**")
        for t in output['high_priority'][:3]:
            lines.append(f"  • {t['title']}")
        lines.append("")
    
    if output['completed']:
        lines.append(f"✅ **Recently Completed:** {len(output['completed'])} items")
        for t in output['completed'][:3]:
            lines.append(f"  • {t['title']}")
        lines.append("")
    
    if output['upcoming']:
        lines.append("📅 **Upcoming:**")
        for t in output['upcoming'][:3]:
            due_str = f" ({t['due']})" if t.get('due') else ""
            lines.append(f"  • {t['title']}{due_str}")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Generate daily standup summary')
    parser.add_argument('--date', help='Date for standup (YYYY-MM-DD)')
    parser.add_argument('--json', action='store_true', help='Output as JSON')
    
    args = parser.parse_args()
    
    result = generate_standup(date_str=args.date, json_output=args.json)
    
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(result)


if __name__ == '__main__':
    main()
