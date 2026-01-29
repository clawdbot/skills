# Hyperfocus Management

## Detection & Intervention Protocol

```yaml
# Hyperfocus Management Protocol

Detection:
  - Engineer hasn't responded in 4+ hours
  - Active commits/PRs on single feature
  - Slack status: "Do Not Disturb" or custom status
  - Calendar blocks marked "Deep Work"

Intervention Rules:
  NEVER interrupt if:
    - < 6 hours into hyperfocus
    - Working on critical path item
    - Deadline not within 24 hours
    - No urgent blocking dependencies

  GENTLE check-in at 6 hours:
    - Slack DM: "Hey! Just checking - have you eaten/hydrated? No rush to reply."
    - Don't expect immediate response
    - Respect the flow

  FIRM interrupt at 10 hours:
    - Physical visit (if co-located) or video call
    - "I need you to take a 30min break. Non-negotiable."
    - Provide specific break activity (walk, snack, shower)
    - Set timer for return

Post-Hyperfocus Recovery:
  - Expect 2-3 hours of low productivity after
  - Don't schedule meetings immediately after
  - Allow flexible end-of-day if hyperfocus started late
  - Celebrate the achievement (positive reinforcement)
```

## Implementation: Hyperfocus Monitor

```python
from datetime import datetime, timedelta
from typing import Optional

class HyperfocusMonitor:
    def __init__(self, engineer_name: str):
        self.engineer = engineer_name
        self.last_activity = None
        self.hyperfocus_start = None
        self.notifications_sent = []

    def log_activity(self, activity_type: str):
        """Track engineer activity (commits, Slack, etc.)"""
        now = datetime.now()

        if self.last_activity and (now - self.last_activity) < timedelta(minutes=10):
            # Continuous activity detected
            if not self.hyperfocus_start:
                self.hyperfocus_start = self.last_activity
                print(f"✨ {self.engineer} entered hyperfocus state")
        else:
            # Break in activity
            if self.hyperfocus_start:
                duration = now - self.hyperfocus_start
                print(f"🎉 {self.engineer} completed {duration.total_seconds()/3600:.1f}h hyperfocus session")
                self.hyperfocus_start = None
                self.notifications_sent = []

        self.last_activity = now

    def check_interventions(self) -> Optional[str]:
        """Determine if intervention is needed"""
        if not self.hyperfocus_start:
            return None

        duration = datetime.now() - self.hyperfocus_start
        hours = duration.total_seconds() / 3600

        # 6 hour gentle check-in
        if hours >= 6 and "6h_checkin" not in self.notifications_sent:
            self.notifications_sent.append("6h_checkin")
            return "gentle_checkin"

        # 10 hour firm break
        if hours >= 10 and "10h_break" not in self.notifications_sent:
            self.notifications_sent.append("10h_break")
            return "mandatory_break"

        return None

    def send_gentle_checkin(self):
        """Send non-intrusive reminder"""
        message = (
            f"Hey {self.engineer}! 👋\n\n"
            "You've been in the zone for 6+ hours - amazing work! 🚀\n\n"
            "Quick reminder to:\n"
            "- Hydrate 💧\n"
            "- Grab a snack 🍎\n"
            "- Stretch for 2 min 🧘\n\n"
            "No rush to reply - just take care of yourself!\n\n"
            "- Your friendly PM parakeet 🦜"
        )
        send_slack_dm(self.engineer, message, urgent=False)

    def send_mandatory_break(self):
        """Firm intervention after 10 hours"""
        message = (
            f"🛑 MANDATORY BREAK TIME 🛑\n\n"
            f"{self.engineer}, you've been hyperfocused for 10+ hours.\n\n"
            "I need you to:\n"
            "1. Stand up right now\n"
            "2. Take a 30-minute break\n"
            "3. Eat something substantial\n"
            "4. Walk around outside if possible\n\n"
            "Set a timer. I'll check back in 30 min.\n\n"
            "This is non-negotiable - doctor's orders! 👩‍⚕️"
        )
        send_slack_dm(self.engineer, message, urgent=True)
        schedule_followup_checkin(30 * 60)  # 30 minutes
```

## Integration Points

- **Slack Bot**: Monitor activity, DND status
- **GitHub Webhooks**: Track commit frequency
- **Calendar API**: Detect "Deep Work" blocks
- **Time Tracking**: Optional Toggl/Clockify integration
