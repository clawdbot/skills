# Agent-to-Agent Protocol

**Enable your Clawdbot skills to communicate and orchestrate workflows automatically.**

## What Is This?

The Agent Protocol allows Clawdbot skills to:
- **Publish events** when something interesting happens
- **Subscribe to events** from other skills
- **Chain workflows** across multiple agents
- **Automate complex tasks** without human intervention

## Real-World Examples

### 1. Research → Summary → Notification
```
Research Agent finds article about ETH
    ↓ publishes "research.article_found"
Summary Agent sees event
    ↓ generates digest
    ↓ publishes "summary.ready"
Telegram Notifier sees event
    ↓ sends notification
```

### 2. Sports Goal → TTS Announcement
```
Sports Ticker detects Barcelona goal
    ↓ publishes "sports.goal_scored"
TTS Agent sees event
    ↓ announces via speaker
"Goal for Barcelona! Messi scores!"
```

### 3. Daily Analytics → Research Topics
```
Cron triggers at 9 AM
    ↓ Personal Analytics generates insights
    ↓ publishes "analytics.insights_ready"
Research Agent sees event
    ↓ suggests topics based on insights
```

## Quick Start

### 1. Installation
```bash
cd /root/clawd/skills/agent-protocol
cp config.example.json config/protocol.json
chmod +x scripts/*.py
```

### 2. Test the Event Bus
```bash
# Publish a test event
python3 scripts/publish.py \
  --type "test.hello" \
  --source "my-skill" \
  --payload '{"message": "Hello from agent protocol!"}'

# Check event bus status
python3 scripts/event_bus.py status
```

### 3. Create Your First Workflow
```bash
# Copy an example workflow
cp examples/simple-workflow.json config/workflows/my-workflow.json

# Edit it for your needs
nano config/workflows/my-workflow.json

# Validate
python3 scripts/workflow_engine.py --validate
```

### 4. Start the Workflow Engine
```bash
# Run once to process pending events
python3 scripts/workflow_engine.py --run

# Or run as daemon (polls every 30 seconds)
python3 scripts/workflow_engine.py --daemon
```

## Integration Guide

### From Python Skills
```python
import sys
from pathlib import Path

# Add agent-protocol to path
sys.path.insert(0, str(Path(__file__).parent.parent / "agent-protocol" / "scripts"))

from publish import publish_event

# Publish event
publish_event(
    event_type="my_skill.something_happened",
    source_agent="my-skill",
    payload={
        "key": "value",
        "importance": 8
    }
)
```

### From JavaScript Skills
```javascript
const { publishEvent } = require('../agent-protocol/scripts/protocol.js');

// Publish event
await publishEvent({
  eventType: 'my_skill.something_happened',
  source: 'my-skill',
  payload: {
    key: 'value',
    importance: 8
  }
});
```

### From Shell Scripts
```bash
python3 /root/clawd/skills/agent-protocol/scripts/publish.py \
  --type "shell.command_completed" \
  --source "backup-script" \
  --payload '{"files": 42, "size_mb": 1024}'
```

## Workflow Definition

Workflows are JSON files in `config/workflows/`:

```json
{
  "workflow_id": "unique-id",
  "name": "Human-readable name",
  "enabled": true,
  "trigger": {
    "event_type": "research.article_found",
    "conditions": {
      "payload.importance": { "gte": 7 }
    }
  },
  "steps": [
    {
      "agent": "summary-agent",
      "action": "summarize",
      "input": {
        "url": "{{payload.url}}"
      },
      "output_event": "summary.ready"
    },
    {
      "agent": "notification-agent",
      "action": "notify",
      "input": {
        "message": "{{payload.title}}\n\n{{previous.summary}}"
      }
    }
  ]
}
```

## Event Types (Standard Conventions)

### Research
- `research.article_found` - Article discovered
- `research.topic_suggested` - New topic suggested

### Sports
- `sports.goal_scored` - Goal/point scored
- `sports.match_started` - Match/game started
- `sports.match_ended` - Match/game finished

### Analytics
- `analytics.insight` - Insight generated
- `analytics.daily_report` - Daily report ready

### Notifications
- `notification.sent` - Notification delivered
- `notification.failed` - Notification failed

### Workflow
- `workflow.started` - Workflow execution started
- `workflow.completed` - Workflow completed
- `workflow.failed` - Workflow failed

### Custom
Use format: `<domain>.<action_past_tense>`
- Lowercase, underscores only
- Domain: broad category
- Action: what happened

## Advanced Features

### Conditional Routing
```json
{
  "condition": {
    "payload.importance": { "gte": 9 }
  },
  "then": { "agent": "urgent-handler" },
  "else": { "agent": "normal-handler" }
}
```

### Parallel Execution
```json
{
  "parallel": [
    { "agent": "telegram-notifier" },
    { "agent": "discord-notifier" },
    { "agent": "email-notifier" }
  ]
}
```

### Error Handling
```json
{
  "agent": "external-api",
  "retry": {
    "max_attempts": 3,
    "backoff_seconds": 5
  },
  "on_error": {
    "agent": "error-logger",
    "continue": true
  }
}
```

## Cron Integration

Add to Clawdbot cron jobs:

```json
{
  "id": "workflow-engine",
  "name": "Agent Protocol Workflow Engine",
  "schedule": "*/5 * * * *",
  "command": "cd /root/clawd/skills/agent-protocol && python3 scripts/workflow_engine.py --run",
  "enabled": true
}
```

Or run as daemon:
```bash
nohup python3 scripts/workflow_engine.py --daemon > /tmp/workflow-engine.log 2>&1 &
```

## Monitoring

### View Recent Events
```bash
python3 scripts/event_bus.py tail --count 50
```

### Check Workflow Status
```bash
python3 scripts/workflow_engine.py --list
```

### View Logs
```bash
tail -f ~/.clawdbot/events/log/events.log
tail -f ~/.clawdbot/events/log/workflows/engine.log
```

## Architecture

### File-Based Event Bus
- Events stored in `~/.clawdbot/events/queue/`
- Processed events move to `processed/` or `failed/`
- Simple, debuggable, persistent
- No daemon required (optional workflow engine daemon)

### Workflow Engine
- Polls event queue (default: every 30 seconds)
- Matches events to workflow triggers
- Executes workflow steps sequentially or in parallel
- Handles errors and retries

### Directory Structure
```
~/.clawdbot/events/
  ├── queue/           # Pending events
  ├── processed/       # Successfully processed
  ├── failed/          # Failed processing
  ├── log/
  │   ├── events.log   # Event bus log
  │   └── workflows/   # Workflow execution logs
  └── subscriptions.json

/root/clawd/skills/agent-protocol/
  ├── config/
  │   ├── protocol.json
  │   └── workflows/   # Workflow definitions
  ├── scripts/
  │   ├── event_bus.py
  │   ├── publish.py
  │   ├── subscribe.py
  │   ├── workflow_engine.py
  │   └── protocol.js
  └── examples/
```

## Security

- Events validate size limits (default: 512 KB)
- Audit logging tracks all publishes
- Future: Permission system for agents

## Performance

- Lightweight: file-based, no database
- Scalable: handles thousands of events
- Configurable: adjust polling intervals
- Cleanup: auto-delete old events (default: 7 days)

## Troubleshooting

### Events Not Processing
```bash
# Check queue
ls -la ~/.clawdbot/events/queue/

# Check workflow engine is running
ps aux | grep workflow_engine

# Validate workflows
python3 scripts/workflow_engine.py --validate
```

### Handler Errors
```bash
# Check failed events
ls -la ~/.clawdbot/events/failed/

# View logs
tail -f ~/.clawdbot/events/log/workflows/engine.log
```

## Contributing

This is core infrastructure for Clawdbot. Contributions welcome!

Ideas for future features:
- WebSocket support for real-time events
- Visual workflow builder (web UI)
- Cross-instance event relay (multi-bot networks)
- GraphQL query API
- Event replay and debugging tools

## License

MIT

---

**Built with 🦎 for Clawdbot**
