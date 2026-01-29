---
name: agent-protocol
description: Agent-to-agent communication protocol. Enables skills to communicate via events, build workflow chains, and orchestrate without human intervention.
version: 1.0.0
---

# Agent-to-Agent Protocol

**A foundational communication layer for Clawdbot skills and agents.**

Enable your agents to talk to each other, build automated workflows, and orchestrate complex multi-step tasks without human intervention.

## Vision

```
Research-Agent finds article
    ↓ publishes "research.found"
Summary-Agent subscribes to events
    ↓ generates digest
    ↓ publishes "summary.ready"
Notification-Agent subscribes
    ↓ posts to Telegram/Discord
```

## Architecture

### 1. **Event Bus** (File-based Message Passing)
- Agents publish events to `~/.clawdbot/events/`
- Events are JSON files with schema validation
- Persistent, debuggable, auditable
- Automatic cleanup of processed events

### 2. **Workflow Engine**
- Define pipelines in JSON or YAML
- Conditional routing based on event data
- Error handling, retries, fallbacks
- Cron integration for scheduled execution

### 3. **Shared Context**
- Agents read/write to shared memory space
- Context passing between workflow steps
- State persistence across agent invocations

### 4. **Agent Registry**
- Discover available agents/skills
- Capability advertisement
- Permission management

## Core Concepts

### Events
Events are the fundamental unit of communication:
```json
{
  "event_id": "evt_20260128_001",
  "event_type": "research.article_found",
  "timestamp": "2026-01-28T23:00:00Z",
  "source_agent": "research-agent",
  "payload": {
    "title": "ETH 2.0 Upgrade Complete",
    "url": "https://example.com/article",
    "importance": 9,
    "summary": "Major Ethereum upgrade..."
  },
  "metadata": {
    "session_id": "main",
    "requires_action": true
  }
}
```

### Workflows
Workflows define how agents respond to events:
```json
{
  "workflow_id": "research-to-telegram",
  "name": "Research → Summary → Notification",
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
      "input": "{{payload}}",
      "output_event": "summary.ready"
    },
    {
      "agent": "notification-agent",
      "action": "notify",
      "input": "{{previous.summary}}",
      "channels": ["telegram"]
    }
  ]
}
```

## Quick Start

### 1. Installation
```bash
cd /root/clawd/skills/agent-protocol
python3 scripts/setup.py
```

### 2. Start Event Bus
```bash
python3 scripts/event_bus.py start
```

### 3. Publish Your First Event
```bash
python3 scripts/publish.py \
  --type "test.hello" \
  --source "my-agent" \
  --payload '{"message": "Hello, world!"}'
```

### 4. Subscribe to Events
```bash
python3 scripts/subscribe.py \
  --types "test.hello" \
  --handler "./my_handler.py"
```

### 5. Define a Workflow
```bash
cp examples/simple-workflow.json config/workflows/my-workflow.json
python3 scripts/workflow_engine.py --validate
```

## Event Types (Conventions)

### Standard Event Types
- `research.article_found` - Research agent found relevant content
- `research.topic_suggested` - New research topic suggested
- `summary.ready` - Summary generated
- `analytics.insight` - Personal analytics insight
- `sports.goal_scored` - Sports ticker goal event
- `sports.match_started` - Match started
- `notification.sent` - Notification delivered
- `workflow.started` - Workflow execution started
- `workflow.completed` - Workflow completed
- `workflow.failed` - Workflow failed

### Event Naming Convention
`<domain>.<action_past_tense>`
- Use lowercase, underscores
- Domain: broad category (research, sports, notification)
- Action: what happened (article_found, goal_scored)

## Workflow Examples

### Example 1: Research → Notification
```json
{
  "workflow_id": "eth-news-alert",
  "trigger": {
    "event_type": "research.article_found",
    "conditions": {
      "payload.keywords": { "contains": ["ethereum", "ETH"] },
      "payload.importance": { "gte": 8 }
    }
  },
  "steps": [
    {
      "agent": "notification-agent",
      "action": "send_telegram",
      "input": {
        "message": "🚨 Important ETH News!\n{{payload.title}}\n{{payload.url}}"
      }
    }
  ]
}
```

### Example 2: Sports Goal → TTS Announcement
```json
{
  "workflow_id": "goal-announcement",
  "trigger": {
    "event_type": "sports.goal_scored",
    "conditions": {
      "payload.team": { "eq": "Barcelona" }
    }
  },
  "steps": [
    {
      "agent": "tts-agent",
      "action": "announce",
      "input": {
        "text": "Goal for Barcelona! {{payload.scorer}} scores! {{payload.score}}"
      }
    }
  ]
}
```

### Example 3: Daily Analytics → Research Topics
```json
{
  "workflow_id": "analytics-to-research",
  "trigger": {
    "event_type": "analytics.daily_report",
    "schedule": "0 9 * * *"
  },
  "steps": [
    {
      "agent": "analytics-agent",
      "action": "generate_insights",
      "output_event": "analytics.insights_ready"
    },
    {
      "agent": "research-agent",
      "action": "suggest_topics",
      "input": "{{previous.insights}}",
      "conditions": {
        "previous.insights.count": { "gte": 3 }
      }
    }
  ]
}
```

## Commands

### Event Bus
```bash
# Start the event bus daemon
python3 scripts/event_bus.py start

# Check status
python3 scripts/event_bus.py status

# Stop
python3 scripts/event_bus.py stop

# View recent events
python3 scripts/event_bus.py tail --count 20
```

### Publishing Events
```bash
# Publish event (JSON payload)
python3 scripts/publish.py \
  --type "research.article_found" \
  --source "research-agent" \
  --payload '{"title": "Article", "url": "..."}'

# Publish from file
python3 scripts/publish.py --file event.json

# Publish with priority
python3 scripts/publish.py \
  --type "alert.urgent" \
  --priority high \
  --payload '{"message": "Critical alert!"}'
```

### Subscribing to Events
```bash
# Subscribe to event types
python3 scripts/subscribe.py \
  --types "research.*,sports.goal_scored" \
  --handler "./handlers/my_handler.py"

# Subscribe with filter
python3 scripts/subscribe.py \
  --types "research.*" \
  --filter '{"importance": {"gte": 8}}' \
  --handler "./handlers/important_only.py"

# List active subscriptions
python3 scripts/subscribe.py --list
```

### Workflow Management
```bash
# Validate workflows
python3 scripts/workflow_engine.py --validate

# Run workflow engine (processes workflows)
python3 scripts/workflow_engine.py --run

# Test specific workflow
python3 scripts/workflow_engine.py --test eth-news-alert

# List workflows
python3 scripts/workflow_engine.py --list

# Enable/disable workflow
python3 scripts/workflow_engine.py --enable research-to-telegram
python3 scripts/workflow_engine.py --disable research-to-telegram
```

### Agent Registry
```bash
# Register your agent
python3 scripts/registry.py register \
  --name "my-agent" \
  --capabilities "summarize,notify" \
  --events "research.article_found"

# List available agents
python3 scripts/registry.py list

# Query agents by capability
python3 scripts/registry.py query --capability "summarize"
```

## Integration with Existing Skills

### Sports Ticker Integration
Modify `sports-ticker/scripts/live_monitor.py` to publish events:
```python
from agent_protocol import publish_event

# After detecting a goal:
publish_event(
    event_type="sports.goal_scored",
    source="sports-ticker",
    payload={
        "team": team_name,
        "scorer": player_name,
        "opponent": opponent,
        "score": f"{home_score}-{away_score}",
        "minute": clock
    }
)
```

### Research Agent Integration
```python
from agent_protocol import publish_event

# After finding an article:
publish_event(
    event_type="research.article_found",
    source="research-agent",
    payload={
        "title": article_title,
        "url": article_url,
        "importance": calculate_importance(article),
        "summary": snippet
    }
)
```

### Personal Analytics Integration
```python
from agent_protocol import publish_event

# Daily insights:
publish_event(
    event_type="analytics.insight",
    source="personal-analytics",
    payload={
        "type": "productivity",
        "insight": "Your focus time increased 20% this week",
        "recommendations": ["Schedule deep work in morning"]
    }
)
```

## Security & Permissions

### Permission Model
```json
{
  "agent": "research-agent",
  "permissions": {
    "publish": ["research.*"],
    "subscribe": ["summary.*", "notification.*"],
    "workflows": ["research-to-telegram"]
  }
}
```

### Sandboxing
- Agents can only publish to their designated event types
- Subscriptions require explicit permission
- Workflows are validated before execution

## Configuration

### Main Config: `config/protocol.json`
```json
{
  "event_bus": {
    "storage_path": "~/.clawdbot/events",
    "retention_days": 7,
    "max_event_size_kb": 512
  },
  "workflow_engine": {
    "enabled": true,
    "poll_interval_seconds": 30,
    "max_concurrent_workflows": 5
  },
  "registry": {
    "agents_path": "~/.clawdbot/agents/registry.json"
  },
  "security": {
    "require_permissions": true,
    "audit_log": true
  }
}
```

## Advanced Features

### 1. Conditional Routing
```json
{
  "steps": [
    {
      "condition": {
        "payload.importance": { "gte": 9 }
      },
      "then": { "agent": "urgent-notifier" },
      "else": { "agent": "standard-notifier" }
    }
  ]
}
```

### 2. Parallel Execution
```json
{
  "steps": [
    {
      "parallel": [
        { "agent": "telegram-notifier" },
        { "agent": "discord-notifier" },
        { "agent": "email-notifier" }
      ]
    }
  ]
}
```

### 3. Error Handling
```json
{
  "steps": [
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
  ]
}
```

### 4. Scheduled Workflows
```json
{
  "trigger": {
    "schedule": "0 9 * * *",
    "event_type": "cron.daily_run"
  }
}
```

## Monitoring & Debugging

### Event Log
All events are logged to `~/.clawdbot/events/log/`
```bash
# View event log
tail -f ~/.clawdbot/events/log/events.log

# Search events
python3 scripts/query.py --type "research.*" --since "1 hour ago"
```

### Workflow Execution Log
```bash
# View workflow executions
python3 scripts/workflow_engine.py --history

# Inspect failed workflow
python3 scripts/workflow_engine.py --inspect <workflow_id>
```

### Metrics
```bash
# Show event statistics
python3 scripts/metrics.py

# Output:
# Total events published: 1,234
# Event types: 15
# Active subscriptions: 8
# Workflows executed: 456
# Average workflow duration: 2.3s
```

## Best Practices

1. **Event Design**
   - Keep payloads small and focused
   - Include enough context for handlers
   - Use consistent naming conventions

2. **Workflow Design**
   - Keep workflows simple and focused
   - Use descriptive names
   - Test thoroughly before enabling

3. **Error Handling**
   - Always define error handlers
   - Log errors for debugging
   - Use retries for transient failures

4. **Performance**
   - Avoid high-frequency events
   - Clean up old events regularly
   - Monitor workflow execution times

5. **Security**
   - Validate event payloads
   - Use permission system
   - Audit sensitive operations

## Python API

```python
from agent_protocol import (
    publish_event,
    subscribe,
    create_workflow,
    register_agent
)

# Publish event
publish_event(
    event_type="my.event",
    source="my-agent",
    payload={"key": "value"}
)

# Subscribe to events
@subscribe(["research.*"])
def handle_research(event):
    print(f"Got research event: {event['payload']}")

# Create workflow programmatically
workflow = create_workflow(
    workflow_id="my-workflow",
    trigger={"event_type": "my.trigger"},
    steps=[
        {"agent": "processor", "action": "process"}
    ]
)

# Register agent
register_agent(
    name="my-agent",
    capabilities=["process", "notify"],
    event_types=["my.event"]
)
```

## JavaScript API

```javascript
const { publishEvent, subscribe, createWorkflow } = require('./scripts/protocol.js');

// Publish event
await publishEvent({
  eventType: 'my.event',
  source: 'my-agent',
  payload: { key: 'value' }
});

// Subscribe
subscribe(['research.*'], (event) => {
  console.log('Got event:', event);
});

// Create workflow
await createWorkflow({
  workflowId: 'my-workflow',
  trigger: { eventType: 'my.trigger' },
  steps: [
    { agent: 'processor', action: 'process' }
  ]
});
```

## Roadmap

- [ ] Visual workflow builder (web UI)
- [ ] WebSocket support for real-time events
- [ ] Cross-instance event relay (multi-bot networks)
- [ ] AI-powered workflow suggestions
- [ ] Event replay and debugging tools
- [ ] Performance profiling
- [ ] GraphQL query API for events

## Contributing

This skill is part of Clawdbot's core infrastructure. Contributions welcome!

## License

MIT

---

**Built with 🦎 by Robby**
