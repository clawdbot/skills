---
name: personal-analytics
description: Analyze conversation patterns, track productivity, and surface self-knowledge insights. Use when user wants to understand their own patterns (when they chat, what topics they discuss, productivity trends, sentiment over time). Provides weekly/monthly reports, topic recommendations, and time-based insights. Privacy-first design with all analysis local.
---

# Personal Analytics

**Know thyself. Work smarter. Discover patterns you didn't know existed.**

Personal Analytics analyzes your conversation patterns to surface actionable insights about your work style, interests, and productivity—all while keeping your data completely private and local.

## Core Capabilities

1. **Session Analysis** - When you chat, for how long, productivity patterns
2. **Topic Tracking** - What subjects come up repeatedly, trending interests
3. **Sentiment Patterns** - Mood tracking over time, stress indicators
4. **Productivity Insights** - When you're most effective, optimal work times
5. **Weekly/Monthly Reports** - Beautiful summaries of your patterns
6. **Topic Recommendations** - Auto-suggest topics for proactive-research monitoring

## Privacy First

🔒 **All analysis happens locally. Nothing leaves your machine.**

- Raw conversations **never** stored
- Only aggregated statistics saved
- Opt-in design (must enable)
- Data deletion anytime
- No external APIs for analysis
- Gitignored data files

## Quick Start

```bash
# Initialize
cp config.example.json config.json

# Enable tracking
python3 scripts/enable.py

# Analyze current sessions
python3 scripts/analyze.py

# Generate report
python3 scripts/report.py weekly

# Get topic recommendations
python3 scripts/recommend.py
```

## What Gets Tracked

### Session Metadata
- Timestamp (start/end)
- Duration
- Message count
- Primary topics discussed
- Sentiment (positive/neutral/negative/mixed)
- Productivity markers (tasks completed, decisions made)

### Aggregated Stats
- Hourly activity heatmap
- Topic frequency over time
- Average session duration
- Productivity by time of day
- Sentiment trends

### What's NOT Tracked
- ❌ Raw message content
- ❌ Personal information
- ❌ Sensitive data (passwords, keys, etc.)
- ❌ Specific conversations

## Configuration

### config.json

```json
{
  "enabled": true,
  "tracking": {
    "sessions": true,
    "topics": true,
    "sentiment": true,
    "productivity": true
  },
  "privacy": {
    "min_aggregation_window_hours": 24,
    "auto_delete_after_days": 90,
    "exclude_patterns": ["password", "secret", "token", "key"]
  },
  "insights": {
    "productivity_markers": [
      "completed", "shipped", "fixed", "merged", "deployed"
    ],
    "stress_indicators": [
      "urgent", "asap", "critical", "broken", "emergency"
    ]
  },
  "reports": {
    "weekly_day": "sunday",
    "weekly_time": "20:00",
    "auto_send": false
  },
  "integrations": {
    "proactive_research": {
      "auto_suggest_topics": true,
      "suggestion_threshold": 3
    }
  }
}
```

## Scripts

### analyze.py

Analyze conversation patterns:

```bash
# Analyze all available data
python3 scripts/analyze.py

# Analyze specific time range
python3 scripts/analyze.py --since "2026-01-01" --until "2026-01-31"

# Analyze and show insights
python3 scripts/analyze.py --insights

# Verbose output
python3 scripts/analyze.py --verbose
```

**Output:**
```
📊 Personal Analytics Analysis

Period: Jan 1 - Jan 28, 2026 (28 days)

Session Summary:
  Total sessions: 145
  Total time: 18h 32m
  Avg session: 7m 40s
  Most active: Tuesday 10:00-11:00

Topics (Top 10):
  1. Python (32 sessions)
  2. FM26 (28 sessions)
  3. Dirac Live (15 sessions)
  4. ETH/crypto (12 sessions)
  5. Docker (11 sessions)
  ...

Productivity:
  High productivity: 09:00-12:00, 14:00-16:00
  Low productivity: Late night (after 22:00)
  Peak day: Wednesday
  
Sentiment:
  Positive: 62%
  Neutral: 28%
  Negative: 8%
  Mixed: 2%
```

### report.py

Generate beautiful reports:

```bash
# Weekly report
python3 scripts/report.py weekly

# Monthly report
python3 scripts/report.py monthly

# Custom range
python3 scripts/report.py custom --since "2026-01-01" --until "2026-01-31"

# Export to file
python3 scripts/report.py weekly --output report.md

# Send via Telegram
python3 scripts/report.py weekly --send
```

**Report Format:**

```markdown
# 📊 Weekly Analytics Report
**Jan 22 - Jan 28, 2026**

## 🎯 Highlights

- **Most productive day:** Wednesday (4 tasks completed)
- **Peak hours:** 09:00-11:00 (3h 45m focused work)
- **Emerging topic:** Rust (mentioned 12 times, +200% from last week)
- **Mood trend:** ↗️ Improving (78% positive, up from 65%)

## ⏰ Time Patterns

### Activity Heatmap
```
Mon  ████░░░░░░░░░░░░░░░░░░░░  4h
Tue  ██████████░░░░░░░░░░░░░░  6h 30m
Wed  ████████████░░░░░░░░░░░░  8h 15m  ← Peak
Thu  ██████░░░░░░░░░░░░░░░░░░  5h
Fri  ████░░░░░░░░░░░░░░░░░░░░  3h 45m
Sat  ██░░░░░░░░░░░░░░░░░░░░░░  1h 30m
Sun  ░░░░░░░░░░░░░░░░░░░░░░░░  45m
```

### Hourly Distribution
```
06-09: ██░░░░░░░░ (12%)
09-12: ████████░░ (38%)  ← Peak productivity
12-14: ███░░░░░░░ (15%)
14-17: █████░░░░░ (24%)
17-22: ██░░░░░░░░ (11%)
```

## 📚 Topic Insights

### Top Topics This Week
1. **Python Development** (32 sessions)
   - Focus: FastAPI, async, testing
   - Trend: Steady
   - Suggestion: Monitor "Python 3.13 features"

2. **FM26** (28 sessions)
   - Focus: Tactics, transfers, editor
   - Trend: ↗️ +15%
   - Suggestion: Already monitoring "FM26 patches" ✓

3. **Audio Engineering** (15 sessions)
   - Focus: Dirac Live, room correction, bass management
   - Trend: 🆕 New topic
   - Suggestion: Monitor "Dirac Live updates"

### Emerging Topics
- **Rust** (12 mentions, first appearance)
- **Kubernetes** (8 mentions, +300%)
- **Machine Learning** (6 mentions)

## 💡 Productivity Insights

### Task Completion
- Total tasks: 23 completed
- Success rate: 87%
- Best day: Wednesday (6 tasks)
- Best time: Morning (09:00-12:00)

### Focus Sessions
- Long sessions (>30m): 8
- Average focus time: 18m
- Longest session: 1h 42m (Wed 10:15)

### Problem-Solving Speed
- Quick wins (<15m): 14 problems
- Complex issues (>1h): 3 problems
- Average: 24m per problem

## 😊 Sentiment & Well-being

### Overall Mood
```
😊 Positive  ████████████████░░  78%  (↗️ +13%)
😐 Neutral   ████░░░░░░░░░░░░░░  18%
😟 Negative  ██░░░░░░░░░░░░░░░░   4%
```

### Stress Indicators
- High stress: 3 sessions (down from 7)
- Urgent keywords: 5 (down from 12)
- Late-night work: 2 sessions (down from 8)

**Insight:** Stress levels decreasing. Good work-life balance this week! 🎉

## 🎯 Recommendations

### For Proactive Research
Based on your interests this week, consider monitoring:
1. **Rust language updates** (mentioned 12x, new interest)
2. **Dirac Live releases** (mentioned 15x, active problem-solving)
3. **Kubernetes security** (mentioned 8x, DevOps focus)

### Productivity Tips
- **Schedule deep work 09:00-11:00** (your peak productivity)
- **Batch meetings after lunch** (14:00-16:00 is secondary peak)
- **Avoid late-night sessions** (22% slower problem-solving)

### Topics to Explore
Based on your current interests, you might enjoy:
- Async Rust patterns (combines Rust + async focus)
- Kubernetes observability (combines K8s + monitoring)
- Audio DSP with Python (combines audio + Python)

---

_Generated by Personal Analytics • Privacy-first, locally processed_
```

### recommend.py

Get topic recommendations for proactive-research:

```bash
# Get recommendations
python3 scripts/recommend.py

# Show reasoning
python3 scripts/recommend.py --explain

# Auto-add to proactive-research
python3 scripts/recommend.py --auto-add

# Set threshold (minimum mentions)
python3 scripts/recommend.py --threshold 5
```

**Output:**
```
💡 Topic Recommendations for Proactive Research

Based on your conversation patterns:

1. Rust Language Updates
   Mentioned: 12 times this week (new topic)
   Reason: Emerging interest, high engagement
   Suggested query: "Rust language updates releases"
   Suggested frequency: weekly
   
2. Dirac Live Updates
   Mentioned: 15 times this week
   Reason: Active problem-solving, technical depth
   Suggested query: "Dirac Live update release"
   Suggested frequency: daily
   
3. FM26 Patches
   Mentioned: 28 times this week
   Reason: Consistent interest over time
   NOTE: Already monitoring! ✓

Would you like to add these topics to proactive-research? [y/N]
```

### session_tracker.py

Track individual sessions (called by Moltbot):

```bash
# Log session start
python3 scripts/session_tracker.py start --channel telegram

# Log session end
python3 scripts/session_tracker.py end --session-id <id>

# Log message (topics, sentiment)
python3 scripts/session_tracker.py message --session-id <id> \
  --topics "Python,Docker" \
  --sentiment positive
```

This script is designed to be called by Moltbot hooks, not manually.

### enable.py / disable.py

Manage tracking:

```bash
# Enable tracking
python3 scripts/enable.py

# Disable tracking
python3 scripts/disable.py

# Show status
python3 scripts/status.py
```

## Integration with Moltbot

Personal Analytics can integrate with Moltbot session lifecycle:

### Hook Points

1. **Session Start** - Log timestamp, channel
2. **Session End** - Calculate duration, save stats
3. **Message Received** - Extract topics (lightweight), detect sentiment

### Recommended Setup

Add to Moltbot SOUL.md:

```markdown
## Personal Analytics Integration

After each session ends, if personal-analytics is enabled:
1. Extract primary topics discussed (max 5)
2. Determine overall sentiment
3. Detect productivity markers (tasks completed)
4. Log to personal-analytics via session_tracker.py
```

## Data Storage

### .analytics_data.json

Aggregated statistics only:

```json
{
  "sessions": [
    {
      "id": "session_uuid",
      "start": "2026-01-28T10:00:00Z",
      "end": "2026-01-28T10:15:00Z",
      "duration_seconds": 900,
      "channel": "telegram",
      "topics": ["Python", "Docker"],
      "sentiment": "positive",
      "productivity_score": 0.8,
      "tasks_completed": 1
    }
  ],
  "topic_stats": {
    "Python": {
      "total_mentions": 145,
      "last_seen": "2026-01-28T10:15:00Z",
      "trend": "stable"
    }
  },
  "time_stats": {
    "hourly_distribution": {
      "09": 23, "10": 45, "11": 38, ...
    },
    "daily_distribution": {
      "monday": 120, "tuesday": 98, ...
    }
  },
  "sentiment_stats": {
    "positive": 145,
    "neutral": 62,
    "negative": 18,
    "mixed": 5
  }
}
```

### .topic_cache.json

Topic extraction cache (temporary):

```json
{
  "hash_12345": ["Python", "FastAPI", "testing"],
  "hash_67890": ["FM26", "tactics"]
}
```

Auto-deleted after 7 days.

## Insights & Patterns

### Time-Based Insights

**Productivity by Hour:**
- Analyzes task completion rate by hour
- Identifies peak productivity windows
- Suggests optimal work scheduling

**Day of Week Patterns:**
- Activity levels per day
- Best days for deep work
- Meeting-heavy vs focus-heavy days

### Topic Insights

**Topic Clustering:**
- Groups related topics
- Identifies emerging interests
- Detects topic trends (rising, falling, stable)

**Depth Analysis:**
- Surface-level mentions vs deep dives
- Problem-solving topics vs casual chat
- Technical vs non-technical ratio

### Sentiment Insights

**Mood Tracking:**
- Overall sentiment trends
- Correlation with time of day
- Stress indicator detection

**Well-being Metrics:**
- Late-night work frequency
- Urgent/stress keywords
- Work-life balance indicators

## Privacy Controls

### Exclusion Patterns

Automatically exclude sensitive data:

```json
{
  "privacy": {
    "exclude_patterns": [
      "password", "token", "key", "secret",
      "credit card", "ssn", "api key"
    ]
  }
}
```

### Data Retention

Auto-delete old data:

```json
{
  "privacy": {
    "auto_delete_after_days": 90,
    "keep_aggregated_stats": true
  }
}
```

### Manual Deletion

```bash
# Delete all data
python3 scripts/delete_data.py --all

# Delete specific date range
python3 scripts/delete_data.py --since "2026-01-01" --until "2026-01-31"

# Delete specific topics
python3 scripts/delete_data.py --topics "topic1,topic2"
```

## Advanced Features

### Custom Productivity Markers

Define what "productivity" means for you:

```json
{
  "insights": {
    "productivity_markers": [
      "completed", "shipped", "merged", "deployed",
      "fixed", "resolved", "closed", "published"
    ]
  }
}
```

### Topic Suggestions for Proactive Research

Automatically suggest topics based on:
- Frequency threshold (mentioned N+ times)
- Trend detection (rising interest)
- Problem-solving patterns (technical depth)
- Temporal patterns (regular discussions)

### Report Customization

```json
{
  "reports": {
    "include_sections": [
      "time_patterns",
      "topic_insights",
      "productivity",
      "sentiment",
      "recommendations"
    ],
    "exclude_topics": ["personal", "family"],
    "min_session_count": 5
  }
}
```

## Use Cases

### 🎯 Optimize Work Schedule
Discover your peak productivity hours and schedule deep work accordingly.

### 📚 Track Learning Journey
See which topics you're exploring, how deeply, and identify knowledge gaps.

### 🧘 Monitor Well-being
Track stress indicators, late-night work, and mood trends.

### 🔍 Discover Patterns
Surface interests you didn't realize were important.

### 🤝 Improve Collaboration
Understand when you're most responsive and schedule meetings accordingly.

### 💡 Generate Content Ideas
Your most-discussed topics are content goldmines.

## Best Practices

1. **Run weekly reports** - Set up auto-generated reports every Sunday
2. **Review recommendations** - Check topic suggestions monthly
3. **Adjust privacy settings** - Start conservative, adjust as comfortable
4. **Use with proactive-research** - Turn insights into automated monitoring
5. **Don't over-optimize** - Insights are guides, not rules

## Troubleshooting

**No data collected:**
- Verify tracking is enabled: `python3 scripts/status.py`
- Check Moltbot integration is active
- Run manual analysis: `python3 scripts/analyze.py --verbose`

**Inaccurate sentiment:**
- Sentiment detection is heuristic-based
- Adjust if needed in future versions

**Missing topics:**
- Topic extraction uses keyword matching
- Lower threshold in config if too restrictive

**Privacy concerns:**
- Review `.analytics_data.json` - only aggregated stats
- Delete data anytime: `python3 scripts/delete_data.py --all`
- Disable tracking: `python3 scripts/disable.py`

## Credits

Built for ClawdHub. Privacy-first design inspired by Quantified Self movement.
