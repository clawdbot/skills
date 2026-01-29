# Context Switching Management

## The ADHD Context-Switching Tax

```
Neurotypical engineer: 1 context switch = 15 min lost
ADHD engineer: 1 context switch = 30-45 min lost

Daily cost:
- 5 context switches/day = 2.5-3.75 hours lost productivity
- Multiplied across team = massive inefficiency
```

## Minimization Protocol

```yaml
# Context-Switching Minimization Protocol

Meeting Scheduling:
  Rules:
    - Batch all meetings into "meeting blocks" (e.g., Tue/Thu 1-4pm)
    - Leave Mon/Wed/Fri meeting-free for deep work
    - No meetings before 11am (morning = prime hyperfocus time)
    - No "quick 15min syncs" (use async Loom videos instead)

  Exceptions:
    - Critical production incidents
    - Client emergencies
    - Once-monthly 1:1s (scheduled consistently)

Task Organization:
  Project Buckets:
    - "Active" (1-2 projects max)
    - "Simmering" (ideas percolating, no active work)
    - "Backlog" (waiting for unblock)

  Daily Workflow:
    Morning:
      - Review "Active" projects
      - Pick ONE to work on today
      - Set up environment (open tabs, tools, music)
      - Enter hyperfocus

    Afternoon:
      - If energy remains: continue OR switch to second active project
      - If energy depleted: low-stakes tasks (code review, docs)

  Switch Budget:
    - Allow max 2 deliberate switches per day
    - Track actual switches (awareness builds discipline)
    - Celebrate low-switch days
```

## Implementation: Context Switch Tracker

```python
from datetime import datetime

class ContextSwitchTracker:
    def __init__(self):
        self.current_context = None
        self.switch_log = []
        self.daily_limit = 2

    def switch_context(self, new_context: str, reason: str = "voluntary") -> bool:
        """Attempt to switch context, with budget enforcement"""
        now = datetime.now()

        # Count switches today
        today_switches = [
            s for s in self.switch_log
            if s['timestamp'].date() == now.date()
        ]

        if len(today_switches) >= self.daily_limit and reason == "voluntary":
            return self._deny_switch(new_context, len(today_switches))

        # Allow switch
        self.switch_log.append({
            'from': self.current_context,
            'to': new_context,
            'reason': reason,
            'timestamp': now
        })

        self.current_context = new_context
        return True

    def _deny_switch(self, attempted_context: str, switch_count: int) -> bool:
        """Gently deny context switch"""
        message = (
            f"⚠️ Context Switch Budget Exceeded\n\n"
            f"You've already switched {switch_count} times today.\n\n"
            f"Current context: **{self.current_context}**\n"
            f"Attempted switch to: {attempted_context}\n\n"
            f"Options:\n"
            f"1. Stay in current context (recommended)\n"
            f"2. Add '{attempted_context}' to tomorrow's active list\n"
            f"3. Override (costs energy token)\n\n"
            f"What would you like to do?"
        )

        response = prompt_user(message)

        if response == "override":
            self.switch_log.append({
                'from': self.current_context,
                'to': attempted_context,
                'reason': 'override',
                'timestamp': datetime.now(),
                'note': 'Used override token'
            })
            return True

        return False

    def end_of_day_report(self) -> dict:
        """Generate daily context-switching report"""
        today = datetime.now().date()
        today_switches = [
            s for s in self.switch_log
            if s['timestamp'].date() == today
        ]

        report = {
            'total_switches': len(today_switches),
            'voluntary': len([s for s in today_switches if s['reason'] == 'voluntary']),
            'emergency': len([s for s in today_switches if s['reason'] == 'emergency']),
            'overrides': len([s for s in today_switches if s['reason'] == 'override']),
            'contexts_visited': list(set([s['to'] for s in today_switches])),
            'focus_score': max(0, 100 - (len(today_switches) * 20))
        }

        return report
```

## Calendar Integration

```python
def get_meeting_free_blocks(calendar_api, date):
    """Find blocks of 2+ hours without meetings"""
    events = calendar_api.get_events(date)

    # Find gaps
    work_start = datetime.combine(date, time(9, 0))
    work_end = datetime.combine(date, time(18, 0))

    free_blocks = []
    current = work_start

    for event in sorted(events, key=lambda e: e.start):
        if event.start > current:
            gap = event.start - current
            if gap >= timedelta(hours=2):
                free_blocks.append({
                    'start': current,
                    'end': event.start,
                    'duration': gap
                })
        current = max(current, event.end)

    # Check final block
    if work_end > current:
        gap = work_end - current
        if gap >= timedelta(hours=2):
            free_blocks.append({
                'start': current,
                'end': work_end,
                'duration': gap
            })

    return free_blocks
```
