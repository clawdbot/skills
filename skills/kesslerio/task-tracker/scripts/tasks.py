#!/usr/bin/env python3
"""
Task Tracker CLI - CRUD operations for work tasks.
"""

import argparse
import sys
from datetime import datetime, timedelta
from pathlib import Path

from utils import (
    TASKS_FILE,
    ARCHIVE_DIR,
    get_current_quarter,
    parse_tasks,
    load_tasks,
    check_due_date,
)


def list_tasks(args):
    """List tasks with optional filters."""
    _, tasks_data = load_tasks()
    tasks = tasks_data['all']
    
    # Apply filters
    filtered = tasks
    
    if args.priority:
        priority_map = {
            'high': 'high_priority',
            'medium': 'medium_priority',
            'low': 'delegated',
        }
        target_key = priority_map.get(args.priority.lower())
        if target_key:
            filtered = tasks_data.get(target_key, [])
    
    if args.status:
        # Normalize status: replace hyphens with spaces for comparison
        # Handle both "in-progress" (CLI) and "In Progress" (stored)
        normalized_status = args.status.lower().replace('-', ' ')
        filtered = [t for t in filtered if t.get('status', '').lower().replace('-', ' ') == normalized_status]
    
    if args.due:
        filtered = [t for t in filtered if check_due_date(t.get('due', ''), args.due)]
    
    # Output
    if not filtered:
        print("No tasks found matching criteria.")
        return
    
    print(f"\n📋 Tasks ({len(filtered)} items)\n")
    
    current_section = None
    for task in filtered:
        section = task.get('section')
        if section != current_section:
            section_names = {
                '🔴': 'High Priority',
                '🟡': 'Medium Priority',
                '🟢': 'Delegated',
                '📅': 'Upcoming',
                '✅': 'Done',
            }
            current_section = section
            print(f"### {section_names.get(section, section or 'Uncategorized')}\n")
        
        checkbox = '✅' if task['done'] else '⬜'
        due_str = f" (due: {task['due']})" if task.get('due') else ''
        blocks_str = f" [blocks: {task['blocks']}]" if task.get('blocks') else ''
        
        print(f"{checkbox} **{task['title']}**{due_str}{blocks_str}")
        if task.get('description'):
            print(f"   {task['description']}")


def add_task(args):
    """Add a new task."""
    # Import here to avoid circular dependency
    from utils import TASKS_FILE
    
    content = TASKS_FILE.read_text()
    
    # Build task entry
    priority_section = {
        'high': '🔴 High Priority',
        'medium': '🟡 Medium Priority',
        'low': '🟢 Delegated / Waiting',
    }.get(args.priority, '🟡 Medium Priority')
    
    task_lines = [f'- [ ] **{args.title}**']
    if args.owner and args.owner != 'martin':
        task_lines.append(f'  - Owner: {args.owner}')
    if args.due:
        task_lines.append(f'  - Due: {args.due}')
    if args.blocks:
        task_lines.append(f'  - Blocks: {args.blocks}')
    
    task_entry = '\n'.join(task_lines)
    
    # Find section and insert
    import re
    section_pattern = rf'(## {re.escape(priority_section)}.*?\n)(.*?)(\n## |\n---|\Z)'
    match = re.search(section_pattern, content, re.DOTALL)
    
    if match:
        insert_content = match.group(2).rstrip() + '\n\n' + task_entry + '\n'
        new_content = content[:match.start(2)] + insert_content + content[match.end(2):]
        TASKS_FILE.write_text(new_content)
        print(f"✅ Added task: {args.title}")
    else:
        print(f"⚠️ Section '{priority_section}' not found. Add manually.")


def done_task(args):
    """Mark a task as done using fuzzy matching."""
    from utils import TASKS_FILE
    
    content = TASKS_FILE.read_text()
    tasks_data = parse_tasks(content)
    tasks = tasks_data['all']
    
    query = args.query.lower()
    matches = [t for t in tasks if query in t['title'].lower() and not t['done']]
    
    if not matches:
        print(f"No matching task found for: {args.query}")
        return
    
    if len(matches) > 1:
        print(f"Multiple matches found:")
        for i, t in enumerate(matches, 1):
            print(f"  {i}. {t['title']}")
        print("\nBe more specific.")
        return
    
    task = matches[0]
    
    # Update in content
    old_line = task['raw_lines'][0]
    new_line = old_line.replace('- [ ]', '- [x]')
    
    new_content = content.replace(old_line, new_line)
    TASKS_FILE.write_text(new_content)
    print(f"✅ Completed: {task['title']}")


def show_blockers(args):
    """Show tasks that are blocking others."""
    _, tasks_data = load_tasks()
    blockers = tasks_data['blocking']
    
    if args.person:
        blockers = [t for t in blockers if args.person.lower() in t['blocks'].lower()]
    
    if not blockers:
        print("No blocking tasks found.")
        return
    
    print(f"\n🚧 Blocking Tasks ({len(blockers)} items)\n")
    
    for task in blockers:
        print(f"⬜ **{task['title']}**")
        print(f"   Blocks: {task['blocks']}")
        if task.get('due'):
            print(f"   Due: {task['due']}")
        print()


def archive_done(args):
    """Archive completed tasks to quarterly file."""
    from utils import TASKS_FILE, ARCHIVE_DIR, get_current_quarter
    
    content = TASKS_FILE.read_text()
    tasks_data = parse_tasks(content)
    done_tasks = tasks_data['done']
    
    if not done_tasks:
        print("No completed tasks to archive.")
        return
    
    # Create archive entry
    quarter = get_current_quarter()
    archive_file = ARCHIVE_DIR / f"ARCHIVE-{quarter}.md"
    
    archive_entry = f"\n## Archived {datetime.now().strftime('%Y-%m-%d')}\n\n"
    for task in done_tasks:
        archive_entry += f"- ✅ **{task['title']}**\n"
    
    # Append to archive
    if archive_file.exists():
        archive_content = archive_file.read_text()
    else:
        archive_content = f"# Task Archive - {quarter}\n"
    
    archive_content += archive_entry
    archive_file.write_text(archive_content)
    
    # Remove from done section in TASKS.md
    import re
    done_section_pattern = r'(## ✅ Done.*?\n\n).*?(\n## |\n---|\Z)'
    new_content = re.sub(
        done_section_pattern,
        r'\1_Move completed items here during daily standup_\n\n\2',
        content,
        flags=re.DOTALL
    )
    
    TASKS_FILE.write_text(new_content)
    print(f"✅ Archived {len(done_tasks)} tasks to {archive_file.name}")


def main():
    parser = argparse.ArgumentParser(description='Task Tracker CLI')
    subparsers = parser.add_subparsers(dest='command', required=True)
    
    # List command
    list_parser = subparsers.add_parser('list', help='List tasks')
    list_parser.add_argument('--priority', choices=['high', 'medium', 'low'])
    list_parser.add_argument('--status', choices=['todo', 'in-progress', 'blocked', 'waiting', 'done'])
    list_parser.add_argument('--due', choices=['today', 'this-week', 'overdue'])
    list_parser.set_defaults(func=list_tasks)
    
    # Add command
    add_parser = subparsers.add_parser('add', help='Add a task')
    add_parser.add_argument('title', help='Task title')
    add_parser.add_argument('--priority', default='medium', choices=['high', 'medium', 'low'])
    add_parser.add_argument('--due', help='Due date (YYYY-MM-DD or description)')
    add_parser.add_argument('--owner', default='martin')
    add_parser.add_argument('--blocks', help='Who/what this blocks')
    add_parser.set_defaults(func=add_task)
    
    # Done command
    done_parser = subparsers.add_parser('done', help='Mark task as done')
    done_parser.add_argument('query', help='Task title (fuzzy match)')
    done_parser.set_defaults(func=done_task)
    
    # Blockers command
    blockers_parser = subparsers.add_parser('blockers', help='Show blocking tasks')
    blockers_parser.add_argument('--person', help='Filter by person being blocked')
    blockers_parser.set_defaults(func=show_blockers)
    
    # Archive command
    archive_parser = subparsers.add_parser('archive', help='Archive completed tasks')
    archive_parser.set_defaults(func=archive_done)
    
    args = parser.parse_args()
    args.func(args)


if __name__ == '__main__':
    main()
