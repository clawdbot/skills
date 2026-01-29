# Integration Guide

How to integrate the Agent Protocol with existing and new Clawdbot skills.

## Integration Checklist

- [ ] Identify events your skill should publish
- [ ] Add event publishing code
- [ ] Define event type names (follow conventions)
- [ ] Create workflow definitions (if needed)
- [ ] Test event publishing
- [ ] Document event types in skill README

## Step-by-Step Integration

### 1. Sports Ticker Integration

**Goal:** Publish goal events for automated announcements

**Event Types:**
- `sports.goal_scored`
- `sports.match_started`
- `sports.match_ended`

**Code Changes:**

Edit `sports-ticker/scripts/live_monitor.py`:

```python
import sys
from pathlib import Path

# Add agent-protocol to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "agent-protocol" / "scripts"))
from publish import publish_event

# In your goal detection code (around line 150):
if "Goal" in event_type and alerts_config.get("goals", True):
    # ... existing alert code ...
    
    # PUBLISH EVENT
    publish_event(
        event_type="sports.goal_scored",
        source_agent="sports-ticker",
        payload={
            "team": team_name,
            "team_emoji": team_emoji,
            "scorer": player,
            "opponent": opponent,
            "score": f"{home_score}-{away_score}",
            "minute": clock,
            "sport": sport,
            "league": league
        }
    )

# In kick-off detection (around line 100):
if is_live and not was_live:
    # ... existing code ...
    
    # PUBLISH EVENT
    publish_event(
        event_type="sports.match_started",
        source_agent="sports-ticker",
        payload={
            "team": team_name,
            "opponent": opponent,
            "league": league,
            "sport": sport
        }
    )

# In full-time detection (around line 200):
if status == "Final":
    # ... existing code ...
    
    # PUBLISH EVENT
    publish_event(
        event_type="sports.match_ended",
        source_agent="sports-ticker",
        payload={
            "team": team_name,
            "result": result,  # "WIN", "LOSS", "DRAW"
            "score": f"{home_score}-{away_score}",
            "sport": sport
        }
    )
```

**Workflow Example (TTS Announcement):**

Create `agent-protocol/config/workflows/goal-tts.json`:
```json
{
  "workflow_id": "goal-tts-announce",
  "trigger": {
    "event_type": "sports.goal_scored",
    "conditions": {
      "payload.team": { "eq": "Barcelona" }
    }
  },
  "steps": [
    {
      "agent": "elevenlabs-voices",
      "action": "speak",
      "input": {
        "text": "Goal for {{payload.team}}! {{payload.scorer}} scores in the {{payload.minute}}! The score is now {{payload.score}}!",
        "voice": "excited"
      }
    }
  ]
}
```

### 2. Web Search Plus Integration

**Goal:** Publish search results for automated research workflows

**Event Types:**
- `search.results_ready`
- `search.interesting_result`

**Code Changes:**

Edit `web-search-plus/scripts/search.py`:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "agent-protocol" / "scripts"))
from publish import publish_event

def perform_search(query, config):
    results = brave_search(query, config)
    
    # Publish results event
    publish_event(
        event_type="search.results_ready",
        source_agent="web-search-plus",
        payload={
            "query": query,
            "results_count": len(results),
            "results": results[:5],  # Top 5
            "timestamp": datetime.utcnow().isoformat()
        }
    )
    
    # Check for highly relevant results
    for result in results:
        relevance_score = calculate_relevance(result, query)
        if relevance_score > 0.8:
            publish_event(
                event_type="search.interesting_result",
                source_agent="web-search-plus",
                payload={
                    "query": query,
                    "title": result["title"],
                    "url": result["url"],
                    "snippet": result["snippet"],
                    "relevance": relevance_score
                }
            )
    
    return results
```

### 3. Personal Analytics Integration

**Goal:** Publish daily insights for automated actions

**Event Types:**
- `analytics.insight`
- `analytics.daily_report`
- `analytics.alert`

**Code Changes:**

Create `personal-analytics/scripts/publish_insights.py`:

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "agent-protocol" / "scripts"))
from publish import publish_event

def publish_daily_insights(insights):
    """Publish daily analytics insights."""
    
    for insight in insights:
        publish_event(
            event_type="analytics.insight",
            source_agent="personal-analytics",
            payload={
                "type": insight["type"],  # "productivity", "health", "habit"
                "insight": insight["message"],
                "importance": insight["importance"],
                "recommendations": insight.get("recommendations", []),
                "data": insight.get("data", {})
            }
        )
    
    # Publish summary
    publish_event(
        event_type="analytics.daily_report",
        source_agent="personal-analytics",
        payload={
            "date": datetime.utcnow().date().isoformat(),
            "insights_count": len(insights),
            "top_insight": insights[0] if insights else None
        }
    )
```

**Workflow Example (Auto Research):**

```json
{
  "workflow_id": "insights-to-research",
  "trigger": {
    "event_type": "analytics.insight",
    "conditions": {
      "payload.importance": { "gte": 8 },
      "payload.type": { "eq": "productivity" }
    }
  },
  "steps": [
    {
      "agent": "research-agent",
      "action": "suggest_topics",
      "input": {
        "insight": "{{payload.insight}}",
        "recommendations": "{{payload.recommendations}}"
      }
    }
  ]
}
```

### 4. Creating a New Event-Driven Skill

**Example: Email Monitor Skill**

**Structure:**
```
email-monitor/
  ├── scripts/
  │   ├── check_email.py      # Main monitoring script
  │   └── process_email.py    # Email processor
  ├── config/
  │   └── config.json
  └── SKILL.md
```

**check_email.py:**
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "agent-protocol" / "scripts"))
from publish import publish_event

def check_emails():
    emails = fetch_new_emails()
    
    for email in emails:
        # Determine importance
        importance = calculate_importance(email)
        
        # Publish event
        publish_event(
            event_type="email.received",
            source_agent="email-monitor",
            payload={
                "from": email["from"],
                "subject": email["subject"],
                "snippet": email["body"][:200],
                "importance": importance,
                "has_attachments": len(email["attachments"]) > 0
            }
        )
        
        # Urgent emails
        if importance >= 9:
            publish_event(
                event_type="email.urgent",
                source_agent="email-monitor",
                payload={
                    "from": email["from"],
                    "subject": email["subject"]
                }
            )
```

**Workflow (Auto-Response):**
```json
{
  "workflow_id": "urgent-email-alert",
  "trigger": {
    "event_type": "email.urgent"
  },
  "steps": [
    {
      "agent": "telegram-notifier",
      "action": "send",
      "input": {
        "message": "🚨 Urgent Email\nFrom: {{payload.from}}\nSubject: {{payload.subject}}"
      }
    },
    {
      "agent": "sms-notifier",
      "action": "send",
      "input": {
        "message": "Urgent email from {{payload.from}}"
      }
    }
  ]
}
```

## Event Type Naming Best Practices

### Convention
`<domain>.<action_past_tense>`

### Good Examples
✅ `research.article_found`  
✅ `sports.goal_scored`  
✅ `email.received`  
✅ `analytics.insight_generated`  
✅ `notification.sent`  

### Bad Examples
❌ `research_article` (missing action)  
❌ `sports.score` (not past tense)  
❌ `EmailReceived` (camelCase, not snake_case)  
❌ `new-email` (no domain namespace)  

### Domain Examples
- `research.*` - Research and discovery
- `sports.*` - Sports tracking
- `email.*` - Email monitoring
- `analytics.*` - Personal analytics
- `notification.*` - Notification delivery
- `workflow.*` - Workflow system events
- `alert.*` - Alert and urgent events

## Testing Your Integration

### 1. Test Event Publishing
```bash
# Trigger your skill's event
cd /root/clawd/skills/sports-ticker
python3 scripts/live_monitor.py --test-event

# Check if event was created
ls -la ~/.clawdbot/events/queue/

# View event
cat ~/.clawdbot/events/queue/evt_*.json | jq
```

### 2. Test Workflow Trigger
```bash
cd /root/clawd/skills/agent-protocol

# Manually publish test event
python3 scripts/publish.py \
  --type "sports.goal_scored" \
  --source "test" \
  --payload '{"team": "Barcelona", "scorer": "Messi", "score": "1-0", "minute": "42'"'"'"}'

# Run workflow engine
python3 scripts/workflow_engine.py --run

# Check if workflow executed
tail ~/.clawdbot/events/log/workflows/engine.log
```

### 3. End-to-End Test
```bash
# Start workflow engine as daemon
python3 scripts/workflow_engine.py --daemon &

# Trigger your skill (e.g., sports ticker check)
cd /root/clawd/skills/sports-ticker
python3 scripts/live_monitor.py

# Monitor workflow execution
tail -f ~/.clawdbot/events/log/workflows/engine.log
```

## Common Patterns

### Pattern 1: Alert → Notification
```
Skill detects something
  ↓ publishes alert event
Workflow engine sees event
  ↓ routes to notifier
Notification sent
```

### Pattern 2: Data → Analysis → Action
```
Skill collects data
  ↓ publishes data event
Analytics skill processes
  ↓ publishes insight event
Action skill acts on insight
```

### Pattern 3: Scheduled Task → Multiple Actions
```
Cron triggers workflow
  ↓ publishes scheduled event
Parallel workflows execute:
  ├─ Generate report
  ├─ Send summary
  └─ Update dashboard
```

## Debugging Integration Issues

### Event Not Being Published
```bash
# Check for errors in your skill
python3 your_skill.py 2>&1 | grep -i error

# Verify agent-protocol path is correct
python3 -c "import sys; sys.path.insert(0, '../agent-protocol/scripts'); from publish import publish_event; print('OK')"

# Check write permissions
ls -la ~/.clawdbot/events/queue/
```

### Workflow Not Triggering
```bash
# Validate workflow syntax
cd /root/clawd/skills/agent-protocol
python3 scripts/workflow_engine.py --validate

# Check if event type matches trigger
python3 scripts/event_bus.py tail --count 10

# Test workflow manually
python3 scripts/workflow_engine.py --test your-workflow-id
```

### Handler Fails
```bash
# Check failed events
ls -la ~/.clawdbot/events/failed/

# View error logs
tail -f ~/.clawdbot/events/log/workflows/engine.log

# Test handler manually
echo '{"event_type":"test","payload":{}}' | python3 your_handler.py
```

## Performance Tips

1. **Batch Events:** Don't publish events for every minor change
2. **Use Conditions:** Filter in triggers to reduce workflow runs
3. **Async Processing:** Let workflow engine handle async work
4. **Event Size:** Keep payloads small (<10 KB ideal)
5. **Cleanup:** Let retention policy handle old events

## Security Tips

1. **Validate Payloads:** Don't trust event data blindly
2. **Sensitive Data:** Avoid publishing secrets/tokens
3. **Rate Limiting:** Don't flood the event bus
4. **Error Handling:** Fail gracefully, log errors

---

**Ready to integrate? Start with the simplest event and build from there!** 🦎
