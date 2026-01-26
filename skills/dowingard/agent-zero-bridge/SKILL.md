---
name: agent-zero-bridge
description: Delegate complex coding, research, or autonomous tasks to Agent Zero framework. Use when user says "ask Agent Zero", "delegate to A0", "have Agent Zero build", or needs long-running autonomous coding with self-correction loops. Supports bidirectional communication, file attachments, task breakdown, and progress reporting.
---

# Agent Zero Bridge

Bidirectional communication between Clawdbot and [Agent Zero](https://github.com/frdel/agent-zero).

## When to Use

- Complex coding tasks requiring iteration/self-correction
- Long-running builds, tests, or infrastructure work
- Tasks needing persistent Docker execution environment
- Research with many sequential tool calls
- User explicitly asks for Agent Zero

## Setup (First Time Only)

### 1. Prerequisites
- Node.js 18+ (for built-in fetch)
- Agent Zero running (Docker recommended, port 50001)
- Clawdbot Gateway with HTTP endpoints enabled

### 2. Install
```bash
# Copy skill to Clawdbot skills directory
cp -r <this-skill-folder> ~/.clawdbot/skills/agent-zero-bridge

# Create config from template
cd ~/.clawdbot/skills/agent-zero-bridge
cp .env.example .env
```

### 3. Configure .env
```env
# Agent Zero (get token from A0 settings or calculate from runtime ID)
A0_API_URL=http://127.0.0.1:50001
A0_API_KEY=your_agent_zero_token

# Clawdbot Gateway
CLAWDBOT_API_URL=http://127.0.0.1:18789
CLAWDBOT_API_TOKEN=your_gateway_token

# For Docker containers reaching host (use your machine's LAN IP)
CLAWDBOT_API_URL_DOCKER=http://192.168.1.x:18789
```

### 4. Get Agent Zero Token
```python
# Calculate from A0's runtime ID
import hashlib, base64
runtime_id = "your_A0_PERSISTENT_RUNTIME_ID"  # from A0's .env
hash_bytes = hashlib.sha256(f"{runtime_id}::".encode()).digest()
token = base64.urlsafe_b64encode(hash_bytes).decode().replace("=", "")[:16]
print(token)
```

### 5. Enable Clawdbot Gateway Endpoints
Add to `~/.clawdbot/clawdbot.json`:
```json
{
  "gateway": {
    "bind": "0.0.0.0",
    "auth": { "mode": "token", "token": "your_token" },
    "http": { "endpoints": { "chatCompletions": { "enabled": true } } }
  }
}
```
Then: `clawdbot gateway restart`

### 6. Deploy Client to Agent Zero Container
```bash
docker exec <container> mkdir -p /a0/bridge/lib
docker cp scripts/lib/. <container>:/a0/bridge/lib/
docker cp scripts/clawdbot_client.js <container>:/a0/bridge/
docker cp .env <container>:/a0/bridge/
docker exec <container> sh -c 'echo "DOCKER_CONTAINER=true" >> /a0/bridge/.env'
```

## Usage

### Send Task to Agent Zero
```bash
node scripts/a0_client.js "Build a REST API with JWT authentication"
node scripts/a0_client.js "Review this code" --attach ./file.py
node scripts/a0_client.js "New task" --new  # Start fresh conversation
```

### Check Status
```bash
node scripts/a0_client.js status
node scripts/a0_client.js history
node scripts/a0_client.js reset  # Clear conversation
```

### Task Breakdown (Creates Tracked Project)
```bash
node scripts/task_breakdown.js "Build e-commerce platform"
# Creates notebook/tasks/projects/<name>.md with checkable steps
```

### From Agent Zero → Clawdbot
Inside A0 container:
```bash
# Report progress
node /a0/bridge/clawdbot_client.js notify "Working on step 3..."

# Ask for input
node /a0/bridge/clawdbot_client.js "Should I use PostgreSQL or SQLite?"

# Invoke Clawdbot tool
node /a0/bridge/clawdbot_client.js tool web_search '{"query":"Node.js best practices"}'
```

## Troubleshooting

| Error | Fix |
|-------|-----|
| 401 / API key error | Check A0_API_KEY matches Agent Zero's mcp_server_token |
| Connection refused from Docker | Use host LAN IP in CLAWDBOT_API_URL_DOCKER, ensure gateway binds 0.0.0.0 |
| A0 500 errors | Check Agent Zero's LLM API key (Gemini/OpenAI) is valid |
