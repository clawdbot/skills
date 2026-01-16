---
name: solobuddy
description: Build-in-public companion for indie hackers — content workflow, Twitter engagement, project soul creation. A living assistant, not a tool.
homepage: https://github.com/gHashTag/bip-buddy
metadata: {"clawdbot":{"emoji":"🎯","requires":{"bins":["gh"],"optional":["bird"]},"config":["solobuddy.dataPath","solobuddy.voice"]}}
---

# SoloBuddy

Build-in-public content assistant. A living companion, not a tool.

## Quick Start

1. Set your data path in `~/.clawdbot/clawdbot.json`:
```json
{
  "solobuddy": {
    "dataPath": "~/projects/my-bip-folder",
    "voice": "jester-sage"
  }
}
```

2. Create folder structure (replace path with your own):
```bash
mkdir -p ~/projects/my-bip-folder/ideas ~/projects/my-bip-folder/drafts ~/projects/my-bip-folder/data
touch ~/projects/my-bip-folder/ideas/backlog.md
```

3. Start using: "show backlog", "new idea", "generate post"

## Placeholders

ClawdBot automatically replaces these in commands:
- `{dataPath}` → your configured `solobuddy.dataPath`
- `{baseDir}` → skill installation folder

## Data Structure

All data in `{dataPath}`:
- `ideas/backlog.md` — idea queue
- `ideas/session-log.md` — session captures
- `drafts/` — work in progress
- `data/my-posts.json` — published posts
- `data/activity-snapshot.json` — project activity (updated hourly)

## Voice Profiles

Configure in `solobuddy.voice`. Available:

| Voice | Description |
|-------|-------------|
| `jester-sage` | Ironic, raw, philosophical (default) |
| `technical` | Precise, detailed, structured |
| `casual` | Friendly, conversational |
| `custom` | Use `{dataPath}/voice.md` |

See `{baseDir}/prompts/profile.md` for voice details.

## Modules

### Content Generation
Core workflow: backlog → draft → publish.
See `{baseDir}/prompts/content.md` for rules.

### Twitter Expert
Content strategy for X/Twitter with 2025 algorithm insights.
See `{baseDir}/modules/twitter-expert.md`

### Twitter Monitor (optional)
Proactive engagement — monitors watchlist, suggests comments.
Requires: `bird` CLI. See `{baseDir}/modules/twitter-monitor.md`

### Soul Wizard
Create project personality from documentation.
See `{baseDir}/references/soul-wizard.md`

## Commands

### Backlog

Show ideas:
```bash
cat {dataPath}/ideas/backlog.md
```

Add idea:
```bash
echo "- [ ] New idea text" >> {dataPath}/ideas/backlog.md
```

### Session Log

View recent:
```bash
tail -30 {dataPath}/ideas/session-log.md
```

Add capture:
```bash
echo -e "## $(date '+%Y-%m-%d %H:%M')\nText" >> {dataPath}/ideas/session-log.md
```

### Drafts

List: `ls {dataPath}/drafts/`
Read: `cat {dataPath}/drafts/<name>.md`

Save draft:
```bash
cat > {dataPath}/drafts/<name>.md << 'EOF'
Content
EOF
```

### Publishing

```bash
cd {dataPath} && git add . && git commit -m "content: add draft" && git push
```

## Project Activity

Read activity snapshot for strategic context:
```bash
cat {dataPath}/data/activity-snapshot.json
```

Fields:
- `daysSilent` — days since last commit
- `commitsToday/Yesterday/Week` — activity intensity
- `phase` — current state: active/momentum/cooling/silent/dormant
- `insight` — human-readable summary

**Phases:**
- `active` — commits today, project is hot
- `momentum` — yesterday active, today quiet (nudge opportunity)
- `cooling` — 2-3 days silent, losing steam
- `silent` — 3-7 days, needs attention
- `dormant` — 7+ days, paused or abandoned

Use for strategic advice:
- "sphere-777 has 10 commits today — focused there"
- "ReelStudio silent 5 days — should we address it?"

## Telegram Integration

When responding in Telegram, include inline buttons for actions.

### Send Message with Buttons

```bash
clawdbot message send --channel telegram --to "$CHAT_ID" --message "Text" \
  --buttons '[
    [{"text":"📋 Backlog","callback_data":"sb:backlog"}],
    [{"text":"✍️ Drafts","callback_data":"sb:drafts"}],
    [{"text":"💡 New Idea","callback_data":"sb:new_idea"}]
  ]'
```

### Callback Data Format

All callbacks use prefix `sb:`:
- `sb:backlog` — show ideas
- `sb:drafts` — list drafts
- `sb:new_idea` — prompt for new idea
- `sb:generate:<N>` — generate from idea N
- `sb:save_draft` — save current content as draft
- `sb:publish` — commit and push
- `sb:activity` — show project activity
- `sb:twitter` — check twitter opportunities

### Main Menu

Trigger: "menu", "start", or after completing action:
```json
[
  [{"text":"📋 Ideas","callback_data":"sb:backlog"}, {"text":"✍️ Drafts","callback_data":"sb:drafts"}],
  [{"text":"📊 Activity","callback_data":"sb:activity"}],
  [{"text":"💡 Add idea","callback_data":"sb:new_idea"}],
  [{"text":"🎯 Generate post","callback_data":"sb:generate_menu"}]
]
```

### Generation Flow

After showing backlog:
```json
[
  [{"text":"1️⃣","callback_data":"sb:generate:1"}, {"text":"2️⃣","callback_data":"sb:generate:2"}, {"text":"3️⃣","callback_data":"sb:generate:3"}],
  [{"text":"◀️ Back","callback_data":"sb:menu"}]
]
```

After generating content:
```json
[
  [{"text":"💾 Save draft","callback_data":"sb:save_draft"}],
  [{"text":"🔄 Regenerate","callback_data":"sb:regenerate"}],
  [{"text":"◀️ Menu","callback_data":"sb:menu"}]
]
```

## Content Generation Flow

1. Read backlog, find idea
2. Read `{baseDir}/prompts/content.md` for rules
3. Read `{baseDir}/prompts/profile.md` for voice
4. Generate in configured voice
5. Show buttons: Save / Regenerate / Menu

## Soul Creation

Create project personality from documentation.

Trigger: "create soul for <path>"

See `{baseDir}/references/soul-wizard.md` for full 5-step wizard:
1. Scan project .md files
2. Ask: Nature (creature/tool/guide/artist)
3. Ask: Voice (playful/technical/poetic/calm/intense)
4. Ask: Philosophy (auto-extract or custom)
5. Ask: Dreams & Pains
6. Save to `{dataPath}/data/project-souls/<name>.json`

## Language

Match user language:
- Russian input → Russian response + buttons
- English input → English response + buttons
