# Agent Protocol Architecture

## Overview

The Agent Protocol is a **file-based event bus** with a **workflow orchestration engine** that enables asynchronous, decoupled communication between Clawdbot skills and agents.

## Core Components

### 1. Event Bus (`event_bus.py`)

**Purpose:** Persistent message queue for agent events

**Key Features:**
- File-based storage (no database required)
- Atomic writes (JSON files)
- Event validation
- Size limits and retention policies
- Audit logging

**Storage Structure:**
```
~/.clawdbot/events/
  ├── queue/       # Pending events (*.json)
  ├── processed/   # Successfully processed events
  ├── failed/      # Failed processing attempts
  └── log/         # Event and audit logs
```

**Event Schema:**
```json
{
  "event_id": "evt_20260128_235959_abc123",
  "event_type": "research.article_found",
  "timestamp": "2026-01-28T23:59:59Z",
  "source_agent": "research-agent",
  "payload": {
    "title": "Article Title",
    "url": "https://...",
    "importance": 8
  },
  "metadata": {
    "priority": "normal",
    "session_id": "main"
  }
}
```

### 2. Workflow Engine (`workflow_engine.py`)

**Purpose:** Orchestrate multi-step workflows based on event triggers

**Key Features:**
- Event pattern matching (supports wildcards)
- Conditional routing
- Parallel step execution
- Error handling and retries
- Variable substitution ({{payload.field}})
- Agent invocation via subprocess

**Workflow Schema:**
```json
{
  "workflow_id": "unique-id",
  "trigger": {
    "event_type": "pattern.*",
    "conditions": {
      "payload.field": { "gte": 7 }
    }
  },
  "steps": [
    {
      "agent": "agent-name",
      "action": "action-name",
      "input": {"key": "{{payload.value}}"},
      "output_event": "next.event"
    }
  ]
}
```

**Execution Flow:**
1. Poll event queue (configurable interval)
2. Match events to workflow triggers
3. Evaluate conditions
4. Execute steps sequentially
5. Handle errors and retries
6. Mark events as processed/failed

### 3. Publisher (`publish.py`)

**Purpose:** Simple API for publishing events

**Usage:**
```python
from publish import publish_event

publish_event(
    event_type="my.event",
    source_agent="my-agent",
    payload={"key": "value"}
)
```

**CLI:**
```bash
python3 publish.py \
  --type "my.event" \
  --source "my-agent" \
  --payload '{"key": "value"}'
```

### 4. Subscriber (`subscribe.py`)

**Purpose:** Event subscription and routing

**Features:**
- Event type filtering (supports wildcards)
- Conditional filters
- Handler invocation
- Subscription persistence

**Usage:**
```bash
python3 subscribe.py \
  --types "research.*,sports.goal_scored" \
  --handler "./my_handler.py"
```

## Design Decisions

### Why File-Based?

**Advantages:**
- ✅ No database dependencies
- ✅ Simple to debug (just open JSON files)
- ✅ Persistent across restarts
- ✅ Atomic operations (filesystem guarantees)
- ✅ Easy backup and replay
- ✅ Works on any platform

**Trade-offs:**
- ⚠️ Not suitable for very high throughput (1000s/sec)
- ⚠️ Polling-based (not real-time push)

**Mitigation:**
- Configurable poll intervals
- Parallel workflow execution
- Event size limits
- Auto-cleanup of old events

### Why Subprocess for Agent Calls?

**Current:** Workflow engine calls agent scripts via subprocess

**Advantages:**
- ✅ Language-agnostic (Python, Node.js, shell)
- ✅ Sandboxed execution
- ✅ Timeout support
- ✅ Works with existing skills

**Future Enhancement:**
- Add HTTP API for agent registration
- Support WebSocket connections
- Direct Python imports for performance

### Event Matching Algorithm

```python
def matches_event_type(event_type, pattern):
    if pattern.endswith(".*"):
        return event_type.startswith(pattern[:-2])
    return event_type == pattern

def matches_conditions(payload, conditions):
    for field, condition in conditions.items():
        value = get_nested_value(payload, field)
        if isinstance(condition, dict):
            # {"gte": 7, "lte": 10}
            for op, expected in condition.items():
                if not evaluate_op(op, value, expected):
                    return False
        else:
            # Direct equality
            if value != condition:
                return False
    return True
```

### Variable Substitution

Template: `"Message: {{payload.title}} - {{payload.url}}"`

Context:
```json
{
  "payload": {
    "title": "Article",
    "url": "https://..."
  },
  "previous": {
    "summary": "..."
  }
}
```

Result: `"Message: Article - https://..."`

Supports:
- Nested paths: `{{payload.nested.field}}`
- Previous step results: `{{previous.summary}}`
- Event metadata: `{{event.timestamp}}`

## Integration Patterns

### Pattern 1: Event Publisher (Skill → Protocol)

```python
# In your skill:
from agent_protocol import publish_event

def on_goal_scored(team, scorer, score):
    publish_event(
        event_type="sports.goal_scored",
        source_agent="sports-ticker",
        payload={
            "team": team,
            "scorer": scorer,
            "score": score
        }
    )
```

### Pattern 2: Event Subscriber (Protocol → Skill)

**Option A: Handler Script**
```python
# handler.py
import json, sys
event = json.loads(sys.stdin.read())
# Process event...
```

```bash
python3 subscribe.py \
  --types "sports.goal_scored" \
  --handler "./handler.py"
```

**Option B: Workflow**
```json
{
  "trigger": {"event_type": "sports.goal_scored"},
  "steps": [
    {
      "agent": "tts-agent",
      "action": "announce",
      "input": {"text": "Goal! {{payload.scorer}}"}
    }
  ]
}
```

### Pattern 3: Multi-Step Workflow

```
Event → Step 1 → Step 2 → Step 3 → Done
         ↓        ↓        ↓
      Result   Result   Result
         ↓        ↓        ↓
      Context  Context  Context
```

Each step receives:
- `{{payload}}` - Original event payload
- `{{previous}}` - Previous step result
- `{{event}}` - Full event object

## Performance Characteristics

### Event Publishing
- **Latency:** ~1-5ms (file write)
- **Throughput:** 100-1000 events/sec (single process)

### Workflow Execution
- **Latency:** Depends on poll interval (default: 30s)
- **Throughput:** Limited by subprocess overhead
- **Concurrency:** Configurable (default: 5 workflows)

### Storage
- **Event Size:** Max 512 KB (configurable)
- **Retention:** 7 days (configurable)
- **Disk Usage:** ~10 MB per 1000 events (typical)

## Security Model

### Current
- Event size validation
- Audit logging
- File permissions (user-only)

### Future
- Permission system (agents can only publish certain event types)
- Event signing and verification
- Rate limiting per agent
- Encrypted event storage

## Monitoring & Observability

### Metrics Available
- Queue size
- Processed/failed counts
- Event types histogram
- Workflow execution times
- Agent invocation counts

### Logs
- `events.log` - All event publishes
- `audit.log` - Security-relevant actions
- `workflows/engine.log` - Workflow execution

### Debugging
```bash
# View recent events
python3 event_bus.py tail --count 50

# Check workflow status
python3 workflow_engine.py --list

# Inspect failed events
ls ~/.clawdbot/events/failed/
```

## Future Enhancements

### Short-term
- [ ] Event replay functionality
- [ ] Workflow visual builder (web UI)
- [ ] Better error reporting
- [ ] Performance metrics dashboard

### Long-term
- [ ] WebSocket support for real-time events
- [ ] Cross-instance event relay (multi-bot networks)
- [ ] GraphQL query API
- [ ] AI-powered workflow suggestions
- [ ] Event sourcing and CQRS patterns

## Comparison to Alternatives

### vs. RabbitMQ/Redis
- ❌ Lower throughput
- ✅ No external dependencies
- ✅ Simpler setup
- ✅ Better for debugging

### vs. WebHooks
- ✅ Persistent queue
- ✅ Built-in retry logic
- ✅ No network configuration
- ❌ Not real-time

### vs. Direct Function Calls
- ✅ Decoupled (no import dependencies)
- ✅ Language-agnostic
- ✅ Async by default
- ❌ Slower (subprocess overhead)

## Conclusion

The Agent Protocol is designed for **reliability and simplicity** over raw performance. It's perfect for:
- Orchestrating multi-skill workflows
- Building automation pipelines
- Decoupling skill dependencies
- Creating event-driven architectures

Not ideal for:
- Real-time sub-second latency requirements
- Extremely high throughput (10,000+ events/sec)
- Complex transactional workflows

---

**Built with 🦎 by Robby**
