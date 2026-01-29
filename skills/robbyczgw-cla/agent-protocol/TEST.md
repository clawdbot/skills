# Testing Guide

## Quick Smoke Test

### 1. Setup
```bash
cd /root/clawd/skills/agent-protocol
python3 scripts/setup.py
```

### 2. Publish Test Event
```bash
python3 scripts/publish.py \
  --type "test.hello" \
  --source "test-agent" \
  --payload '{"message": "Hello World!", "importance": 10}'
```

Expected output:
```
✓ Event published: evt_20260128_230736_abc123
```

### 3. Check Event Bus
```bash
python3 scripts/event_bus.py status
```

Expected output:
```
Event Bus Status:
  Queue: 1 pending
  Processed: 0
  Failed: 0
  Log size: 0 KB
```

### 4. View Event
```bash
python3 scripts/event_bus.py tail --count 1
```

Expected output:
```
[QUEUE] evt_20260128_230736_abc123
  Type: test.hello
  Source: test-agent
  Time: 2026-01-28T23:07:36Z
  Payload: {
    "message": "Hello World!",
    "importance": 10
  }
```

### 5. Validate Workflows
```bash
python3 scripts/workflow_engine.py --validate
```

Expected output:
```
Validating workflows in /root/clawd/skills/agent-protocol/config/workflows...
Validation complete: 0 valid, 0 invalid
```

## Full Integration Test

### Step 1: Create Test Handler

Create `test_handler.py`:
```python
#!/usr/bin/env python3
import json
import sys

event = json.loads(sys.stdin.read())
print(f"✓ Handler received: {event['event_type']}")
print(f"  Payload: {event['payload']}")
```

Make it executable:
```bash
chmod +x test_handler.py
```

### Step 2: Create Test Workflow

Create `config/workflows/test-workflow.json`:
```json
{
  "workflow_id": "test-workflow",
  "name": "Test Workflow",
  "enabled": true,
  "trigger": {
    "event_type": "test.hello",
    "conditions": {
      "payload.importance": { "gte": 5 }
    }
  },
  "steps": [
    {
      "agent": "test",
      "action": "log",
      "input": {
        "message": "Received: {{payload.message}}"
      }
    }
  ]
}
```

### Step 3: Validate Workflow
```bash
python3 scripts/workflow_engine.py --validate
```

Expected:
```
✓ test-workflow
```

### Step 4: Publish Event
```bash
python3 scripts/publish.py \
  --type "test.hello" \
  --source "test" \
  --payload '{"message": "Integration test", "importance": 8}'
```

### Step 5: Run Workflow Engine
```bash
python3 scripts/workflow_engine.py --run
```

### Step 6: Verify Processing
```bash
# Check queue is empty (event processed)
python3 scripts/event_bus.py status

# Should show: Queue: 0 pending, Processed: 1

# View processed events
ls ~/.clawdbot/events/processed/
```

## Performance Test

### Generate Multiple Events
```bash
for i in {1..10}; do
  python3 scripts/publish.py \
    --type "test.perf" \
    --source "test" \
    --payload "{\"id\": $i}"
done
```

### Check Performance
```bash
time python3 scripts/workflow_engine.py --run
```

### View Statistics
```bash
python3 scripts/event_bus.py stats
```

## Cleanup Test Data
```bash
rm -rf ~/.clawdbot/events/queue/*
rm -rf ~/.clawdbot/events/processed/*
rm -rf ~/.clawdbot/events/failed/*
```

## Common Issues

### Issue: "Module not found"
**Solution:** Add agent-protocol to Python path
```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "agent-protocol" / "scripts"))
```

### Issue: "Workflow not triggering"
**Solution:** Check event type matches exactly
```bash
# View event
cat ~/.clawdbot/events/queue/evt_*.json | jq .event_type

# Check workflow trigger
cat config/workflows/my-workflow.json | jq .trigger.event_type
```

### Issue: "Handler fails"
**Solution:** Test handler manually
```bash
echo '{"event_type":"test","payload":{}}' | python3 your_handler.py
```

## Success Criteria

✅ Events can be published  
✅ Events appear in queue  
✅ Workflow engine validates workflows  
✅ Workflow engine processes events  
✅ Events move from queue to processed  
✅ Handlers execute successfully  
✅ Logs show execution details  

---

**All tests passing? You're ready to integrate! 🦎**
