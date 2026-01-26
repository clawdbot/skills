# Context Recovery Skill

Automatically recover working context after session compaction or when continuation is implied but context is missing. Works across Discord, Slack, Telegram, Signal, and other supported channels.

## Triggers

### Automatic Triggers
- Session begins with a `<summary>` tag (compaction detected)
- User message contains compaction indicators: "Summary unavailable", "context limits", "truncated"

### Manual Triggers
- User says "continue", "did this happen?", "where were we?", "what was I working on?"
- User references "the project", "the PR", "the branch", "the issue" without specifying which
- User implies prior work exists but context is unclear
- User asks "do you remember...?" or "we were working on..."

## Execution Protocol

### Step 1: Detect Active Channel

Extract from runtime context:
- `channel` — discord | slack | telegram | signal | etc.
- `channelId` — the specific channel/conversation ID
- `threadId` — for threaded conversations (Slack, Discord threads)

### Step 2: Fetch Channel History (Adaptive Depth)

**Initial fetch:**
```
message:read
  channel: <detected-channel>
  channelId: <detected-channel-id>
  limit: 50
```

**Adaptive expansion logic:**
1. Parse timestamps from returned messages
2. Calculate time span: `newest_timestamp - oldest_timestamp`
3. If time span < 2 hours AND message count == limit:
   - Fetch additional 50 messages (using `before` parameter if supported)
   - Repeat until time span ≥ 2 hours OR total messages ≥ 100
4. Hard cap: 100 messages maximum (token budget constraint)

**Thread-aware recovery (Slack/Discord):**
```
# If threadId is present, fetch thread messages first
message:read
  channel: <detected-channel>
  threadId: <thread-id>
  limit: 50

# Then fetch parent channel for broader context
message:read
  channel: <detected-channel>
  channelId: <parent-channel-id>
  limit: 30
```

**Parse for:**
- Recent user requests (what was asked)
- Recent assistant responses (what was done)
- URLs, file paths, branch names, PR numbers
- Incomplete actions (promises made but not fulfilled)
- Project identifiers and working directories

### Step 3: Fetch Session Logs (if available)

```bash
# Find most recent session files for this agent
SESSION_DIR=$(ls -d ~/.clawdbot-*/agents/*/sessions 2>/dev/null | head -1)
SESSIONS=$(ls -t "$SESSION_DIR"/*.jsonl 2>/dev/null | head -3)

for SESSION in $SESSIONS; do
  echo "=== Session: $SESSION ==="
  
  # Extract user requests
  jq -r 'select(.message.role == "user") | .message.content[0].text // empty' "$SESSION" | tail -20
  
  # Extract assistant actions (look for tool calls and responses)
  jq -r 'select(.message.role == "assistant") | .message.content[]? | select(.type == "text") | .text // empty' "$SESSION" | tail -50
done
```

### Step 4: Check Shared Memory

```bash
# Extract keywords from channel history (project names, PR numbers, branch names)
# Search memory for relevant entries
grep -ri "<keyword>" ~/clawd-*/memory/ 2>/dev/null | head -10

# Check for recent daily logs
ls -t ~/clawd-*/memory/202*.md 2>/dev/null | head -3 | xargs grep -l "<keyword>" 2>/dev/null
```

### Step 5: Synthesize Context

Compile a structured summary:

```markdown
## Recovered Context

**Channel:** #<channel-name> (<platform>)
**Time Range:** <oldest-message> to <newest-message>
**Messages Analyzed:** <count>

### Active Project/Task
- **Repository:** <repo-name>
- **Branch:** <branch-name>
- **PR:** #<number> — <title>

### Recent Work Timeline
1. [<timestamp>] <action/request>
2. [<timestamp>] <action/request>
3. [<timestamp>] <action/request>

### Pending/Incomplete Actions
- ⏳ "<quoted incomplete action>"
- ⏳ "<another incomplete item>"

### Key References
| Type | Value |
|------|-------|
| PR | #<number> |
| Branch | <name> |
| Files | <paths> |
| URLs | <links> |

### Last User Request
> "<quoted request that may not have been completed>"

### Confidence Level
- Channel context: <high/medium/low>
- Session logs: <available/partial/unavailable>
- Memory entries: <found/none>
```

### Step 6: Cache Recovered Context

**Persist to memory for future reference:**

```bash
# Write to daily memory file
MEMORY_FILE=~/clawd-*/memory/$(date +%Y-%m-%d).md

cat >> "$MEMORY_FILE" << EOF

## Context Recovery — $(date +%H:%M)

**Channel:** #<channel-name>
**Recovered context for:** <project/task summary>

### Key State
- <bullet points of critical context>

### Pending Items
- <incomplete actions>

EOF
```

This ensures context survives future compactions.

### Step 7: Respond with Context

Present the recovered context, then prompt:

> "Context recovered. Your last request was [X]. This action [completed/did not complete]. Shall I [continue/retry/clarify]?"

## Channel-Specific Notes

### Discord
- Use `channelId` from the incoming message metadata
- Guild channels have full history access
- Thread recovery: check for `threadId` in message metadata
- DMs may have limited history

### Slack
- Use `channel` parameter with Slack channel ID
- Thread context requires `threadId` — always check for thread context first
- Parent channel fetch provides surrounding conversation context
- May need workspace-level permissions for full history

### Telegram / Signal / Others
- Same `message:read` interface
- History depth may vary by platform
- Group vs. DM context may differ

## Constraints

- **MANDATORY:** Execute this protocol before responding "insufficient data" or asking clarifying questions when context appears missing
- Adaptive depth: start with 50, expand to 100 max
- Time-based goal: capture at least 2 hours of context when possible
- Session log extraction: last 3 session files maximum
- Memory cache: append to daily file, do not overwrite
- If recovery fails, state what was attempted and what data sources were unavailable

## Auto-Trigger Detection

At session start, scan for compaction indicators:

```python
# Pseudocode for trigger detection
if message contains "<summary>":
    trigger_context_recovery()
elif message contains any of ["Summary unavailable", "context limits", "truncated", "compacted"]:
    trigger_context_recovery()
elif message matches continuation_patterns:
    # "continue", "where were we", "did this happen", etc.
    trigger_context_recovery()
```

**Do not wait for user to ask** — if compaction is detected, proactively recover and present context.

## Example Invocation

**Scenario:** Session starts with compaction summary

```
User message: "<summary>Summary unavailable due to context limits...</summary>"
User message: "did this happen?"
```

**Agent executes:**
1. Detects compaction via `<summary>` tag
2. `message:read channel=discord channelId=1460342116516364533 limit=50`
3. Calculates time span: 2.5 hours — sufficient, no expansion needed
4. Parses messages, finds last action: "Now let me extract the key orchestration decisions..."
5. Checks session logs — unavailable for current session
6. Writes context summary to `memory/2026-01-25.md`
7. Responds:

> "Context recovered. Your last request was to extract orchestration decisions from Nexus archived sessions for PR #137 (Skills & Agents System). This action did not complete before context was truncated.
>
> **Recovered state:**
> - PR #137: 15,053 additions, 91 files, CONFLICTING merge state
> - Spec location: `content/spec-skills-agents-system.md` (2,067 lines)
> - Nexus sessions: `~/.clawdbot-duke-leto/archive/nexus-sessions/` (96 files)
>
> Shall I proceed with the extraction?"
