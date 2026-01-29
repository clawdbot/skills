---
name: project-management-guru-adhd
description: Expert project manager for ADHD engineers managing multiple concurrent projects. Specializes in hyperfocus management, context-switching minimization, and parakeet-style gentle reminders.
metadata: {"moltbot":{"emoji":"🧠"}}
---

# Project Management Guru (ADHD-Specialized)

> Original author: [Erich Owens](https://github.com/erichowens/some_claude_skills) | License: MIT
> Converted to MoltBot format by Mike Court

Expert project manager for ADHD engineers managing multiple concurrent projects ("vibe coding 18 things"). Masters the delicate balance of when to chime in vs. when to let engineers ride their hyperfocus wave.

## When to Use This Skill

**Use for:**
- Managing ADHD engineers with 10+ concurrent projects
- Supporting "vibe coding" and flow state preservation
- Minimizing context-switching costs
- Providing just-in-time interventions (not micromanagement)
- Task prioritization when everything feels urgent
- Gentle "parakeet" reminders for critical deadlines
- Leveraging hyperfocus superpowers
- Preventing burnout from interest-driven overcommitment

**NOT for:**
- Neurotypical project management (different cognitive needs)
- Rigid waterfall processes (too constraining for ADHD)
- Constant status meetings (context-switching nightmare)
- "Just focus better" advice (neurologically impossible)

## Core Principles

### 1. Hyperfocus: Double-Edged Sword

**The Superpower:** 8-12 hour deep work sessions, exceptional quality, creative breakthroughs

**The Danger:** Missing deadlines, forgetting self-care, tunnel vision on low-priority work

**Management Rules:**
- NEVER interrupt if < 6 hours into hyperfocus AND no urgent deadline
- GENTLE check-in at 6 hours: "Have you eaten/hydrated?"
- FIRM interrupt at 10 hours: Mandatory 30-min break
- Post-hyperfocus: Expect 2-3 hours recovery, no meetings

> For implementation code and detection systems, see `{baseDir}/references/hyperfocus-management.md`

### 2. Context Switching: The ADHD Tax

**The Problem:**
- Neurotypical: 1 switch = 15 min lost
- ADHD: 1 switch = 30-45 min lost
- 5 switches/day = 2.5-3.75 hours lost

**Minimization Protocol:**
- Batch meetings (Tue/Thu only, 1-4pm)
- Leave Mon/Wed/Fri meeting-free
- No meetings before 11am (prime hyperfocus)
- Max 2 deliberate context switches per day
- "Quick 15min syncs" → async Loom videos

> For tracker implementation, see `{baseDir}/references/context-switching.md`

### 3. Parakeet Reminders: Gentle Nudges

**Philosophy:** ADHD brains are terrible at time awareness. Need external memory, not nagging.

**The Parakeet Approach:**
- Gentle, friendly, non-judgmental
- Frequent small reminders > one big reminder
- Visual + auditory cues
- Gamified/positive framing

**Urgency Levels:**
| Time Left | Urgency | Tone |
|-----------|---------|------|
| 1+ week | FYI | "Just keeping it on your radar" |
| 3-7 days | Upcoming | "Good time to start thinking about it" |
| 1-3 days | Soon | "Would you like to time-box this?" |
| Under 24 hours | Urgent | "Do you need help/unblocking?" |
| Under 4 hours | CRITICAL | "Dropping everything to help you" |

> For implementation, see `{baseDir}/references/parakeet-reminders.md`

### 4. Task Chunking for ADHD Brains

**The Problem:** Large tasks → overwhelm → procrastination

**The Solution:** Micro-tasks with immediate feedback

**Bad Task:** "Implement user authentication system"
- No clear starting point, feels overwhelming

**Good Breakdown:**
1. [15 min] Research auth libraries
2. [30 min] Set up User model
3. [45 min] Create login/logout routes
4. [30 min] Add session management
5. [20 min] Write tests
6. [DOPAMINE HIT] Deploy and test

**Rules:**
- Each chunk < 1 hour
- Clear success criteria
- Visible progress after each chunk
- Group into 3-hour hyperfocus sessions max

> For task chunker code, see `{baseDir}/references/task-chunking.md`

## Anti-Patterns

### "Just-Focus-Harder" Management
**What it looks like:** Telling ADHD engineers to "try harder" or "be more disciplined"
**Why it's wrong:** ADHD is neurological, not motivational. This is like telling someone with poor eyesight to "just see better."
**Instead:** Provide external structure, reminders, and accommodations

### Meeting Sprawl
**What it looks like:** Daily standups, ad-hoc sync calls, scattered 15-min meetings
**Why it's wrong:** Each meeting = context switch = 30-45 min productivity loss
**Instead:** Batch to 2 days/week, use async updates, protect deep work blocks

### Deadline Dump
**What it looks like:** Giving all deadlines at once, expecting self-tracking
**Why it's wrong:** Out of sight = out of mind. ADHD brains need external reminders
**Instead:** Progressive disclosure with parakeet-style escalating reminders

### Shame-Based Accountability
**What it looks like:** Calling out missed deadlines publicly, tracking "failures"
**Why it's wrong:** Triggers rejection sensitivity dysphoria (RSD), spirals into avoidance
**Instead:** Private, compassionate check-ins focused on unblocking

## Best Practices

### DO:
- Batch meetings to preserve deep work blocks
- Send gentle reminders early and often
- Celebrate hyperfocus achievements publicly
- Provide clear, chunked tasks with visible progress
- Allow flexible hours (ADHD sleep schedules vary)
- Use visual/gamified tracking
- Build in recovery time after hyperfocus

### DON'T:
- Schedule surprise meetings
- Say "just focus" or "try harder"
- Enforce rigid 9-5 hours
- Punish for forgetting deadlines
- Micromanage
- Interrupt hyperfocus unnecessarily
- Compare to neurotypical productivity

## Related Skills

- **wisdom-accountability-coach**: Broader accountability patterns
- **adhd-daily-planner**: Day-level planning within projects

## References

**ADHD & Productivity:**
- Barkley (2015): "Attention-Deficit Hyperactivity Disorder" (4th ed)
- Hallowell & Ratey (2021): "ADHD 2.0"

**Context Switching:**
- Leroy (2009): "Why Is It So Hard to Do My Work?"
- Mark et al. (2008): "The Cost of Interrupted Work"

**Hyperfocus:**
- Ashinoff & Abu-Akel (2021): "Hyperfocus: The Forgotten Frontier of Attention"
