---
name: idea-clawdbot
description: "Launch background Clawdbot sessions to explore and analyze business ideas. Say 'Idea: [description]' to trigger. Fork of 'idea' skill rewritten to use sessions_spawn instead of claude CLI + tmux + telegram CLI. Results sent to current chat, not Saved Messages. Zero external dependencies."
metadata: {"clawdbot":{"emoji":"💡"}}
---

# Idea Exploration Skill (Clawdbot Native)

Launch autonomous background sessions to explore business ideas in depth. Get market research, technical analysis, GTM strategy, and actionable recommendations—all using built-in Clawdbot features.

## Quick Start

**Trigger phrase:** Say `Idea: [description]` and the assistant will:
1. Spawn a background sub-agent session using `sessions_spawn`
2. Research and analyze the idea comprehensively
3. Save results to `~/clawd/ideas/<slug>/research.md`
4. Send the file + summary back to this Telegram chat

## How It Works

```
User: "Idea: AI calendar assistant"
       ↓
┌─────────────────────────────────┐
│  1. Detect "Idea:" trigger      │
│  2. sessions_spawn background   │
│  3. Sub-agent researches        │
│  4. Writes research.md          │
│  5. Returns to main chat        │
│  6. Sends file + summary        │
└─────────────────────────────────┘
```

## Prerequisites

- Clawdbot with `sessions_spawn` enabled
- No external CLIs needed (fully native)

## AGENTS.md Integration

Add this to your `AGENTS.md`:

```markdown
## Idea Exploration

**When user says "Idea: [description]":**

1. Extract the idea description
2. Create a slug from the idea (lowercase, hyphens)
3. Use `sessions_spawn` to launch a background research session:
   - **task**: Use the template from `skills/idea-clawdbot/templates/idea-exploration-prompt.md`
   - **label**: `idea-research-<slug>`
   - **cleanup**: keep (so we can review the session later)
4. Confirm: "🔬 Research started for: [idea]. I'll ping you when done (usually 3-5 minutes)."
5. When the sub-agent completes, send the research file to the chat

**Result handling:**
- Research saved to: `~/clawd/ideas/<slug>/research.md`
- Send file as document via Telegram
- Include brief summary of verdict (🟢/🟡/🟠/🔴)
```

## Analysis Framework

The exploration covers:

1. **Core Concept Analysis** - Problem, assumptions, uniqueness
2. **Market Research** - Users, TAM/SAM/SOM, competitors
3. **Technical Implementation** - Stack, MVP scope, challenges
4. **Business Model** - Revenue, pricing, unit economics
5. **Go-to-Market Strategy** - Launch, acquisition, partnerships
6. **Risks & Challenges** - Technical, competitive, regulatory
7. **Verdict & Recommendations** - Clear yes/no with action plan

## Verdict Types

- 🟢 **STRONG YES** - Clear opportunity, pursue aggressively
- 🟡 **CONDITIONAL YES** - Promising but needs validation
- 🟠 **PIVOT RECOMMENDED** - Core insight good, execution needs work
- 🔴 **PASS** - Too many red flags

## Example Output

```
~/clawd/ideas/ai-calendar-assistant/
├── metadata.txt
├── research.md    # 400-500 line comprehensive analysis
```

## Tips

- Ideas typically take 3-5 minutes to analyze
- Check session progress: `clawdbot sessions list --kinds spawn`
- Monitor sub-agent: `clawdbot sessions history <session-key>`
- Results come back to the same chat automatically

## Template Variables

When spawning the sub-agent, replace these in the prompt template:
- `{IDEA_DESCRIPTION}`: The actual idea text
- `{IDEA_SLUG}`: URL-friendly version (e.g., "ai-powered-calendar")
