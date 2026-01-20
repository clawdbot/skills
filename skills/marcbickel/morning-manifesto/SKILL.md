---
name: morning-manifesto
description: Daily morning reflection workflow with task sync to Obsidian, Apple Reminders, and Linear
metadata: {"clawdbot":{"emoji":"🌅","trigger":"/morning_manifesto"}}
---

# Morning Manifesto 🌅

Trigger: `/morning_manifesto`

## Flow

### 1. Send the prompts
When `/morning-manifesto` is triggered, immediately send:
```
Good morning! 🚀 Please tell me about:
- What you did yesterday?
- One small thing you are grateful for
- Today's adventure
- Tasks and commitments
- How are the weekly priorities going?
```

### 2. Wait for response
Wait for user reply (text or audio). Audio is automatically transcribed via whisper.cpp.

### 3. Parse and append to Obsidian daily note
Parse the response and append to today's note in the Obsidian vault (🔥 Fires). Structure:
```markdown
## Morning Manifesto - [YYYY-MM-DD]

### What I did yesterday
[user's response]

### Grateful for
[user's response]

### Today's adventure
[user's response]

### Tasks and commitments
- [task 1]
- [task 2]

### Weekly priorities status
[user's response]
```

### 4. Sync tasks with Apple Reminders
For each task/commitment mentioned:
- **If task exists**: Update its due date to today
- **If new task**: Create a new reminder with due date today
- Use the `apple-reminders` skill for this

### 5. Query Linear for urgent issues
Query all teams for issues with priority = urgent (1). Format:
```
🔴 Urgent Linear Issues:
- [Team] [Issue ID]: [Title]
```

### 6. Send summary
Send a final message with:
- Today's Apple Reminders (all due today)
- Urgent Linear issues across all teams

## Key details
- Use today's date for Obsidian note naming (YYYY-MM-DD.md)
- For Apple Reminders: query by due date, create with due date
- For Linear: use `priority = 1` filter, query all teams
- Pay special attention to "Tasks and commitments" section
