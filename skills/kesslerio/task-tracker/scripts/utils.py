#!/usr/bin/env python3
"""
Shared utilities for task tracker scripts.
"""

import re
from datetime import datetime, timedelta
from pathlib import Path

TASKS_FILE = Path.home() / "clawd" / "memory" / "work" / "TASKS.md"
ARCHIVE_DIR = Path.home() / "clawd" / "memory" / "work"


def get_current_quarter() -> str:
    """Return current quarter string like '2026-Q1'."""
    now = datetime.now()
    quarter = (now.month - 1) // 3 + 1
    return f"{now.year}-Q{quarter}"


def parse_tasks(content: str) -> dict:
    """Parse TASKS.md content into categorized task lists.
    
    Returns dict with keys:
    - high_priority: list of high priority tasks
    - medium_priority: list of medium priority tasks
    - delegated: list of delegated/waiting tasks
    - done: list of completed tasks
    - upcoming: list of upcoming tasks
    - blocking: list of tasks that block others
    - due_today: list of tasks due today or ASAP
    - all: list of all tasks
    """
    result = {
        'high_priority': [],
        'medium_priority': [],
        'delegated': [],
        'done': [],
        'upcoming': [],
        'blocking': [],
        'due_today': [],
        'all': [],
    }
    
    current_section = None
    current_task = None
    today = datetime.now().date()
    
    for line in content.split('\n'):
        # Detect section headers
        if line.startswith('## '):
            section_match = re.match(r'## ([🔴🟡🟢📅✅]) (.+)', line)
            if section_match:
                current_section = section_match.group(1)
            continue
        
        # Detect task line
        task_match = re.match(r'^- \[([ x])\] \*\*(.+?)\*\*(.*)$', line)
        if task_match:
            done = task_match.group(1) == 'x'
            title = task_match.group(2).strip()
            rest = task_match.group(3).strip()
            description = rest.lstrip('—').lstrip('-').strip() if rest else ''
            
            current_task = {
                'title': title,
                'description': description,
                'done': done,
                'section': current_section,
                'due': None,
                'blocks': None,
            }
            
            result['all'].append(current_task)
            
            # Categorize by section
            if done:
                result['done'].append(current_task)
            elif current_section == '🔴':
                result['high_priority'].append(current_task)
            elif current_section == '🟡':
                result['medium_priority'].append(current_task)
            elif current_section == '🟢':
                result['delegated'].append(current_task)
            elif current_section == '📅':
                result['upcoming'].append(current_task)
            
            continue
        
        # Detect task metadata
        if current_task and line.strip().startswith('-'):
            meta_line = line.strip()[1:].strip()
            
            if meta_line.lower().startswith('due:'):
                due_str = meta_line.split(':', 1)[1].strip()
                current_task['due'] = due_str
                
                # Check if due today or ASAP (only if not done)
                if not done:
                    if due_str.lower() in ['asap', 'immediately', 'today']:
                        result['due_today'].append(current_task)
                    else:
                        # Parse date
                        date_str = due_str
                        if due_str.lower().startswith('before '):
                            date_str = due_str[7:].strip()
                        
                        for fmt in ['%Y-%m-%d', '%B %d', '%b %d']:
                            try:
                                due_date = datetime.strptime(date_str, fmt).date()
                                if due_date.year == 1900:
                                    due_date = due_date.replace(year=today.year)
                                if due_date <= today:
                                    result['due_today'].append(current_task)
                                break
                            except ValueError:
                                continue
            
            elif meta_line.lower().startswith('blocks:'):
                blocks = meta_line.split(':', 1)[1].strip()
                current_task['blocks'] = blocks
                if not done and current_task not in result['blocking']:
                    result['blocking'].append(current_task)
    
    return result


def load_tasks() -> tuple[str, dict]:
    """Load and parse tasks from file."""
    if not TASKS_FILE.exists():
        print(f"\n❌ Tasks file not found: {TASKS_FILE}\n", file=sys.stderr)
        print("To create a new tasks file, run:")
        print(f"  python3 scripts/init.py\n")
        sys.exit(1)
    
    content = TASKS_FILE.read_text()
    tasks = parse_tasks(content)
    return content, tasks


def check_due_date(due: str, check_type: str = 'today') -> bool:
    """Check if a due date matches the given type.
    
    Args:
        due: Due date string
        check_type: 'today', 'this-week', or 'overdue'
    
    Returns:
        True if the due date matches the check type
    """
    if not due or due.lower() in ['asap', 'immediately']:
        return check_type == 'today'
    
    today = datetime.now().date()
    week_end = today + timedelta(days=(6 - today.weekday()))
    
    # Strip "Before" prefix if present
    date_str = due
    if due.lower().startswith('before '):
        date_str = due[7:].strip()
    
    # Try to parse date with various formats
    for fmt in ['%Y-%m-%d', '%B %d', '%b %d']:
        try:
            due_date = datetime.strptime(date_str, fmt).date()
            if due_date.year == 1900:
                due_date = due_date.replace(year=today.year)
            
            if check_type == 'today':
                return due_date <= today
            elif check_type == 'this-week':
                return due_date <= week_end
            elif check_type == 'overdue':
                return due_date < today
        except ValueError:
            continue
    
    # Non-parseable date (e.g., "Before IMCAS") - treat as future
    return False
