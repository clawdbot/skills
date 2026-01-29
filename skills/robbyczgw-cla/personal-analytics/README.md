# Personal Analytics

**Know thyself. Work smarter. Discover patterns you didn't know existed.**

Personal Analytics analyzes your conversation patterns to surface actionable insights about your work style, interests, and productivity—all while keeping your data completely private and local.

## Features

- ⏰ **Time Pattern Analysis** - When you chat, for how long, productivity peaks
- 📚 **Topic Tracking** - What you discuss most, emerging interests
- 😊 **Sentiment Monitoring** - Mood trends, stress indicators
- 💡 **Productivity Insights** - Task completion, optimal work times
- 📊 **Beautiful Reports** - Weekly/monthly summaries
- 🔗 **Proactive Research Integration** - Auto-suggest monitoring topics
- 🔒 **Privacy First** - All local, no external data, opt-in design

## Quick Start

```bash
# 1. Setup
cp config.example.json config.json

# 2. Enable tracking
python3 scripts/enable.py

# 3. Analyze (after some sessions)
python3 scripts/analyze.py --insights

# 4. Generate weekly report
python3 scripts/report.py weekly

# 5. Get topic recommendations
python3 scripts/recommend.py --explain
```

## Privacy Guarantee

🔒 **Your data never leaves your machine.**

- Raw conversations NOT stored
- Only aggregated statistics saved
- All analysis happens locally
- No external APIs for analysis
- Data files are gitignored
- Delete anytime with one command

## What Gets Tracked

### ✅ Tracked (Aggregated Only)
- Session timestamps and duration
- Topic frequencies
- Sentiment distribution
- Productivity markers
- Time-of-day patterns

### ❌ NOT Tracked
- Raw message content
- Personal information
- Sensitive data (passwords, keys)
- Specific conversation details

## Use Cases

### 📈 Optimize Your Schedule
Discover when you're most productive and schedule deep work accordingly.

**Example Insight:**
> "Your peak productivity is 09:00-11:00 on Wednesdays. Task completion is 68% faster during this window."

### 🎯 Focus on What Matters
Identify topics you're spending time on and decide if they align with your goals.

**Example Insight:**
> "You've discussed 'Docker deployment' 23 times this month. Consider monitoring 'Docker security updates' proactively."

### 😊 Track Well-being
Monitor stress indicators, late-night work, and mood trends.

**Example Insight:**
> "Stress keywords decreased 40% this week. Work-life balance improving! 🎉"

### 💡 Discover Hidden Interests
Surface emerging topics you didn't realize you cared about.

**Example Insight:**
> "New interest detected: 'Rust' (12 mentions this week, 0 last week). Want to monitor Rust language updates?"

## Commands

### Enable/Disable

```bash
# Enable tracking
python3 scripts/enable.py

# Disable tracking
python3 scripts/disable.py

# Check status
python3 scripts/status.py
```

### Analyze

```bash
# Analyze all data
python3 scripts/analyze.py

# Analyze date range
python3 scripts/analyze.py --since "2026-01-01" --until "2026-01-31"

# With insights
python3 scripts/analyze.py --insights

# JSON output
python3 scripts/analyze.py --json
```

### Reports

```bash
# Weekly report
python3 scripts/report.py weekly

# Monthly report
python3 scripts/report.py monthly

# Custom range
python3 scripts/report.py custom --since "2026-01-01" --until "2026-01-31"

# Save to file
python3 scripts/report.py weekly --output report.md

# Send via Telegram
python3 scripts/report.py weekly --send
```

### Recommendations

```bash
# Get topic recommendations
python3 scripts/recommend.py

# With explanations
python3 scripts/recommend.py --explain

# Set threshold (min mentions)
python3 scripts/recommend.py --threshold 5

# Auto-add to proactive-research
python3 scripts/recommend.py --auto-add
```

## Sample Report

```markdown
# 📊 Weekly Analytics Report
**Jan 22 - Jan 28, 2026**

## 🎯 Highlights

- **Most productive day:** Wednesday (6 tasks completed)
- **Peak hours:** 09:00-11:00
- **Emerging topic:** Rust (+1200%)
- **Mood trend:** ↗️ 78% positive (up from 65%)

## ⏰ Time Patterns

Mon  ████░░░░░░░░  4h
Tue  ██████░░░░░░  6h 30m
Wed  ████████░░░░  8h 15m  ← Peak
Thu  ██████░░░░░░  5h
Fri  ████░░░░░░░░  3h 45m

## 📚 Top Topics

1. **Python** (32 sessions)
2. **FM26** (28 sessions)
3. **Audio Engineering** (15 sessions)

## 💡 Recommendations

- Schedule deep work 09:00-11:00 (your peak)
- Monitor "Rust updates" (new interest)
- Avoid late-night sessions (22% slower)
```

## Integration

### Proactive Research

Personal Analytics automatically suggests topics for monitoring:

```bash
python3 scripts/recommend.py --auto-add
```

**Flow:**
1. Analyze conversation patterns
2. Identify frequently discussed topics
3. Suggest adding to proactive-research
4. One-click setup

### Moltbot Session Hooks

For automated tracking, integrate with Moltbot:

```python
# On session end
python3 /path/to/personal-analytics/scripts/session_tracker.py \
  message \
  --session-id <id> \
  --topics "Python,Docker" \
  --sentiment positive
```

## Configuration

See [SKILL.md](SKILL.md) for complete configuration options.

### Key Settings

```json
{
  "enabled": true,
  "privacy": {
    "auto_delete_after_days": 90,
    "exclude_patterns": ["password", "secret"]
  },
  "insights": {
    "productivity_markers": ["completed", "shipped", "fixed"],
    "stress_indicators": ["urgent", "critical", "broken"]
  }
}
```

## Data Storage

### .analytics_data.json

Aggregated statistics only (privacy-safe):

```json
{
  "sessions": [{
    "id": "uuid",
    "start": "2026-01-28T10:00:00Z",
    "duration_seconds": 900,
    "topics": ["Python", "Docker"],
    "sentiment": "positive",
    "productivity_score": 0.8
  }],
  "topic_stats": {
    "Python": {
      "total_mentions": 145,
      "trend": "stable"
    }
  }
}
```

## Requirements

- Python 3.8+
- Optional: proactive-research skill (for recommendations)

## FAQ

**Q: Is my data shared?**
> No. Everything stays on your machine. No external APIs for analysis.

**Q: Can I see the raw data?**
> Yes. Check `.analytics_data.json` - only aggregated stats, no message content.

**Q: How do I delete everything?**
> `rm .analytics_data.json .topic_cache.json`

**Q: Does this slow down my assistant?**
> No. Analysis runs separately, doesn't affect chat performance.

## License

MIT

## Credits

Built for ClawdHub by the Moltmates team. Privacy-first design inspired by Quantified Self movement.
