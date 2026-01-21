#!/usr/bin/env python3
"""
Task Extractor - Extract action items from meeting notes.

This script can:
1. Extract tasks using regex patterns (fast, local)
2. Output tasks.py add commands (executable)
3. Generate LLM prompts (for complex extraction)
"""

import argparse
import re
import sys
from pathlib import Path


# Regex patterns for common meeting note formats
TASK_PATTERNS = [
    # Markdown checkbox: "- [ ] Task" or "- [x] Task"
    (r'-\s*\[\s*\]\s*(.+?)$', 'medium'),
    # TODO marker: "TODO: Task" or "- TODO: Task"
    (r'(?:^-?\s*)?TODO:\s*(.+?)$', 'medium'),
    # Action marker: "Action: Task" or "- Action: Task"
    (r'(?:^-?\s*)?Action:\s*(.+?)$', 'medium'),
    # Assignee pattern: "@person: Task" or "- @person: Task"
    (r'@(\w+):\s*(.+?)$', 'medium'),
    # "Task:" prefix: "Task: Task description"
    (r'(?:^-?\s*)?Task:\s*(.+?)$', 'medium'),
    # Numbered list items that look like tasks (verb + noun)
    (r'^\d+[.)]\s*([A-Z][a-z]+(?:\s+[a-z]+)*\s+(?:to|for|on|complete|finish|review|create|add|set up|post|analyze|update)\b.+)', 'medium'),
]


def extract_tasks_local(text: str) -> list[dict]:
    """Extract tasks using regex patterns (fast, local)."""
    tasks = []
    lines = text.split('\n')
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        for pattern, default_priority in TASK_PATTERNS:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                title = match.group(1).strip()
                # Clean up the title
                title = re.sub(r'^\-\s*', '', title)  # Remove leading dash
                title = title.strip('.,;:')
                
                if len(title) < 5:  # Skip very short matches
                    continue
                
                tasks.append({
                    'title': title,
                    'priority': default_priority,
                    'owner': 'martin',
                    'due': None,
                    'blocks': None,
                })
                break  # Only match first pattern per line
    
    return tasks


def format_task_command(task: dict) -> str:
    """Format a task as a tasks.py add command."""
    parts = [f'tasks.py add "{task["title"]}"']
    
    if task.get('priority') and task['priority'] != 'medium':
        parts.append(f'--priority {task["priority"]}')
    
    if task.get('owner') and task['owner'] != 'martin':
        parts.append(f'--owner {task["owner"]}')
    
    if task.get('due'):
        parts.append(f'--due "{task["due"]}"')
    
    if task.get('blocks'):
        parts.append(f'--blocks "{task["blocks"]}"')
    
    return ' '.join(parts)


def extract_prompt(text: str) -> str:
    """Generate a prompt for LLM to extract tasks (for complex notes)."""
    return f"""Extract action items from these meeting notes and format each as a task.

For each task, determine:
- title: Brief, actionable title (verb + noun)
- priority: high (blocking/deadline/revenue), medium (important), low (nice-to-have)
- due: Date if mentioned, ASAP if urgent, or leave blank
- owner: Person responsible (default: martin)
- blocks: Who/what is blocked if this isn't done

Meeting Notes:
---
{text}
---

Output each task as a command:
```
tasks.py add "Task title" --priority high --due YYYY-MM-DD --blocks "person (reason)"
```

Only output the commands, one per line. No explanations."""


def main():
    parser = argparse.ArgumentParser(
        description='Extract action items from meeting notes. Outputs tasks.py add commands.'
    )
    parser.add_argument('--from-text', help='Meeting notes text')
    parser.add_argument('--from-file', type=Path, help='File containing meeting notes')
    parser.add_argument(
        '--llm', action='store_true',
        help='Use LLM prompt instead of local regex extraction'
    )
    
    args = parser.parse_args()
    
    if args.from_file:
        if not args.from_file.exists():
            print(f"Error: File not found: {args.from_file}", file=sys.stderr)
            sys.exit(1)
        text = args.from_file.read_text()
    elif args.from_text:
        text = args.from_text
    else:
        parser.print_help()
        print("\nError: Provide --from-text or --from-file", file=sys.stderr)
        sys.exit(1)
    
    if args.llm:
        # Output LLM prompt
        print(extract_prompt(text))
        print("\n---")
        print("NOTE: This output is meant for LLM processing.")
        print("The LLM should parse meeting notes and call tasks.py add for each task.")
    else:
        # Local extraction using regex
        tasks = extract_tasks_local(text)
        
        if not tasks:
            print("No tasks found using local extraction.")
            print("Try --llm flag for LLM-based extraction.")
            sys.exit(0)
        
        print(f"# Extracted {len(tasks)} task(s) from meeting notes")
        print("# Run these commands to add them:\n")
        
        for i, task in enumerate(tasks, 1):
            cmd = format_task_command(task)
            print(cmd)


if __name__ == '__main__':
    main()
