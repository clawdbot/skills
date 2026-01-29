# Parakeet Reminder System

## Philosophy

- ADHD brains are terrible at time awareness
- Deadlines sneak up unexpectedly ("wait, that's today!?")
- Need external memory aids, but not nagging

**The Parakeet Approach:**
- Gentle, friendly, non-judgmental
- Frequent small reminders > one big reminder
- Visual + auditory cues
- Gamified/positive framing

## Implementation

```python
from enum import Enum
from datetime import datetime, timedelta

class ReminderUrgency(Enum):
    FUTURE_FYI = 1      # 1+ week out
    UPCOMING = 2        # 3-7 days
    SOON = 3            # 1-3 days
    URGENT = 4          # &lt;24 hours
    CRITICAL = 5        # &lt;4 hours

class ParakeetReminder:
    def __init__(self, task: str, deadline: datetime, engineer: str):
        self.task = task
        self.deadline = deadline
        self.engineer = engineer
        self.reminders_sent = []

    def calculate_urgency(self) -> ReminderUrgency:
        """Determine urgency based on time remaining"""
        now = datetime.now()
        time_left = self.deadline - now

        if time_left < timedelta(hours=4):
            return ReminderUrgency.CRITICAL
        elif time_left < timedelta(days=1):
            return ReminderUrgency.URGENT
        elif time_left < timedelta(days=3):
            return ReminderUrgency.SOON
        elif time_left < timedelta(days=7):
            return ReminderUrgency.UPCOMING
        else:
            return ReminderUrgency.FUTURE_FYI

    def get_reminder_message(self, urgency: ReminderUrgency) -> str:
        """Generate appropriate reminder based on urgency"""
        messages = {
            ReminderUrgency.FUTURE_FYI: (
                f"🦜 Parakeet FYI\n\n"
                f"Just a heads up: **{self.task}** is due {self.deadline.strftime('%B %d')}.\n\n"
                f"No action needed now - just wanted to keep it on your radar!"
            ),
            ReminderUrgency.UPCOMING: (
                f"🦜 Parakeet Reminder\n\n"
                f"**{self.task}** is coming up in a few days ({self.deadline.strftime('%A, %B %d')}).\n\n"
                f"Might be a good time to start thinking about it when you finish your current hyperfocus!"
            ),
            ReminderUrgency.SOON: (
                f"🦜 Parakeet Nudge\n\n"
                f"**{self.task}** is due in {(self.deadline - datetime.now()).days} days.\n\n"
                f"Would you like to:\n"
                f"- Add it to your active projects list?\n"
                f"- Time-box 2 hours for it tomorrow?\n"
                f"- Delegate it (if possible)?"
            ),
            ReminderUrgency.URGENT: (
                f"⚠️ Parakeet Alert\n\n"
                f"**{self.task}** is due tomorrow ({self.deadline.strftime('%I:%M %p')})!\n\n"
                f"Current status? Do you need:\n"
                f"- Time blocked on your calendar?\n"
                f"- Help/unblocking?\n"
                f"- Deadline extension?"
            ),
            ReminderUrgency.CRITICAL: (
                f"🚨 URGENT: Parakeet Emergency 🚨\n\n"
                f"**{self.task}** is due in {(self.deadline - datetime.now()).total_seconds() / 3600:.1f} hours!\n\n"
                f"Dropping everything to help you finish this.\n\n"
                f"What do you need RIGHT NOW?"
            )
        }

        return messages.get(urgency, "Reminder message unavailable")

    def should_send_reminder(self) -> bool:
        """Determine if reminder should be sent (not too frequent)"""
        urgency = self.calculate_urgency()

        # Frequency based on urgency
        frequency_map = {
            ReminderUrgency.FUTURE_FYI: timedelta(days=7),
            ReminderUrgency.UPCOMING: timedelta(days=2),
            ReminderUrgency.SOON: timedelta(days=1),
            ReminderUrgency.URGENT: timedelta(hours=6),
            ReminderUrgency.CRITICAL: timedelta(hours=1)
        }

        min_interval = frequency_map[urgency]

        if not self.reminders_sent:
            return True

        last_reminder = max(self.reminders_sent)
        return (datetime.now() - last_reminder) >= min_interval

    def send(self):
        """Send reminder if appropriate"""
        if not self.should_send_reminder():
            return

        urgency = self.calculate_urgency()
        message = self.get_reminder_message(urgency)

        send_slack_dm(self.engineer, message, urgent=(urgency == ReminderUrgency.CRITICAL))
        self.reminders_sent.append(datetime.now())
```

## Reminder Scheduling

```python
class ParakeetScheduler:
    def __init__(self):
        self.reminders = []

    def add_task(self, task: str, deadline: datetime, engineer: str):
        """Add a new task to track"""
        reminder = ParakeetReminder(task, deadline, engineer)
        self.reminders.append(reminder)

        # Schedule initial reminder based on time to deadline
        time_until = deadline - datetime.now()

        if time_until > timedelta(days=14):
            # First reminder 2 weeks before
            first_reminder = deadline - timedelta(days=14)
        elif time_until > timedelta(days=7):
            # First reminder 1 week before
            first_reminder = deadline - timedelta(days=7)
        else:
            # Immediate reminder
            first_reminder = datetime.now()

        schedule_task(first_reminder, reminder.send)

    def check_all(self):
        """Check all reminders and send if needed"""
        for reminder in self.reminders:
            if reminder.deadline > datetime.now():  # Not yet past
                reminder.send()
```

## Message Templates

### Friendly Check-ins
```
🦜 Hey there!

Just your friendly PM parakeet checking in.

How's [task] going? No pressure - just wanted to see if you need anything!

Options:
[ ] All good, on track
[ ] Could use some help
[ ] Need to reschedule
```

### Deadline Approaching
```
⏰ Heads up!

[task] is due in [X days/hours].

Quick check:
- Status: [dropdown]
- Blockers: [text field]
- Need extension? [yes/no]

Remember: It's okay to ask for help! 💪
```

### Celebration
```
🎉 AMAZING WORK!

You completed [task] with [X hours] to spare!

🏆 Achievement Unlocked: Early Bird
📈 Your streak: [N] tasks on time

Keep being awesome! 🚀
```
