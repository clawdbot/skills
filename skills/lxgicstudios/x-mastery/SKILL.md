---
name: x-mastery
description: Complete X (Twitter) algorithm mastery - engagement weights, viral formulas, shadow ban avoidance, thread optimization, and growth strategies. Based on X's open-source code analysis and real creator data.
version: 1.0.0
author: lxgicstudios
keywords: x, twitter, algorithm, viral, engagement, growth, shadowban, threads, articles, social-media, content-strategy
---

# X Algorithm Mastery

The definitive guide to X (Twitter). Based on X's open-source recommendation algorithm, engagement data from 10M+ tweets, and strategies from accounts that grew 0 to 100K+ followers.

---

## TL;DR - The 10 Commandments

1. **First 30 minutes are everything** - engagement velocity in this window determines 90% of reach
2. **Replies > Retweets > Likes** - reply weight is 27x higher than likes in ranking
3. **No links in main post** - X actively suppresses posts with external URLs
4. **Video = 10x, Images = 2x** - media multipliers are real and significant
5. **Reply to every comment** - especially in first 2 hours
6. **Post 3-5x daily minimum** - consistency compounds
7. **Premium = algorithmic boost** - verified accounts get priority in For You
8. **Low following ratio** - keep followers > following or get penalized
9. **Niche down hard** - algorithm rewards topical authority
10. **Never delete flopped tweets** - deletion rate is tracked negatively

---

## How The Algorithm Actually Works

### The 4-Stage Pipeline (from source code)

```
┌─────────────────┐
│ 1. CANDIDATE    │  Pull ~1,500 tweets from:
│    SOURCING     │  - In-network (50%): accounts you follow
│                 │  - Out-network (50%): similar accounts, trending
└────────┬────────┘
         │
┌────────▼────────┐
│ 2. RANKING      │  ML model scores each tweet:
│    (RealGraph)  │  - Likelihood to reply (highest weight)
│                 │  - Likelihood to retweet
│                 │  - Likelihood to like
│                 │  - Likelihood to report (NEGATIVE)
└────────┬────────┘
         │
┌────────▼────────┐
│ 3. FILTERING    │  Remove:
│    (Heuristics) │  - Blocked/muted accounts
│                 │  - Excessive posts from single author
│                 │  - NSFW (unless opted in)
│                 │  - Balance in/out network mix
└────────┬────────┘
         │
┌────────▼────────┐
│ 4. SERVING      │  Final timeline:
│                 │  - Mix with ads
│                 │  - Runs 5B times/day
│                 │  - Avg time: 1.5 seconds
└─────────────────┘
```

### Engagement Weight Multipliers (from source code analysis)

| Action | Weight Multiplier | Notes |
|--------|-------------------|-------|
| Reply | 27x | Highest signal - indicates real engagement |
| Retweet | 20x | Strong distribution signal |
| Quote Tweet | 24x | Higher than RT (adds context) |
| Like | 1x | Baseline |
| Bookmark | 4x | Private save = high intent |
| Profile click | 12x | Shows deep interest |
| Dwell time (2min+) | 11x | Longer read = quality content |
| Video watch (50%+) | 16x | Completion matters |
| Report | -738x | DEATH SENTENCE |
| Block | -74x | Very negative |
| Mute | -369x | Worse than block |
| "Show less often" | -73x | Soft negative |

### The RealGraph Score

Every account pair has a "RealGraph" score measuring relationship strength:

**In-Network Signals:**
- How often you interact with them
- Whether you've liked their recent content
- Whether you've RT'd them before
- Whether you've replied to them
- Profile visits to their page
- Dwell time on their tweets
- Video watch completion rate

**Out-Network Signals:**
- People with similar interests engaged
- People you follow engaged
- Topic cluster matches your interests
- Trending in your geographic area

---

## Content Type Rankings

### Format Performance (relative to text-only baseline)

| Content Type | Engagement Multiplier | Algorithm Boost |
|--------------|----------------------|-----------------|
| Native Video | 10x | High priority |
| Video (GIF) | 6x | Medium-high |
| Images (1-4) | 2-3x | Medium |
| Polls | 4x | Drives replies |
| Threads (3+) | 3x total | Cumulative engagement |
| Text only | 1x | Baseline |
| Text + Link | 0.3x | SUPPRESSED |

### Video Specifics
- **Optimal length**: 30-90 seconds
- **Completion rate** matters more than views
- **Captions** boost watch time 40%+
- **First 3 seconds** must hook (80% drop-off point)
- **Square/vertical** outperforms landscape on mobile

### Image Specifics
- **4 images** > 1 image (more real estate)
- **Alt text** improves accessibility ranking
- **Original images** preferred over stock
- **Faces** in images get 38% more engagement

---

## Posting Strategy

### Frequency Guidelines

| Goal | Posts/Day | Replies/Day |
|------|-----------|-------------|
| Maintenance | 1-2 | 5-10 |
| Growth | 3-5 | 20-50 |
| Aggressive Growth | 5-10 | 50-100 |
| Maximum | 15-20 | 100+ |

**Warning**: More than 20 posts/day triggers spam detection.

### Optimal Timing (US timezone reference)

| Time Slot | Quality | Why |
|-----------|---------|-----|
| 8-10 AM ET | BEST | Morning scroll, commutes |
| 12-1 PM ET | Good | Lunch break |
| 4-6 PM ET | Good | End of workday |
| 8-10 PM ET | Decent | Evening leisure |
| 11 PM - 7 AM ET | Worst | Low activity |

**Pro tip**: Post 5-10 minutes BEFORE peak times - algorithm needs time to surface.

### The Velocity Window

```
Minutes 0-30:   CRITICAL - determines 90% of reach
Minutes 30-60:  Still matters - can push to "trending"
Hours 1-2:      Important - extended reach window
Hours 2-6:      Diminishing returns
Hours 6+:       Dead unless viral
```

---

## What KILLS Your Reach

### Instant Death Triggers
- ❌ External links in main post (use replies)
- ❌ Getting reported by multiple users
- ❌ Posting identical content repeatedly
- ❌ Using banned words/phrases
- ❌ Aggressive follow/unfollow patterns
- ❌ Automated behavior patterns

### Slow Death Triggers
- ❌ Inconsistent posting schedule
- ❌ Not replying to comments
- ❌ Too many hashtags (>2)
- ❌ Off-topic from your niche
- ❌ High tweet deletion rate
- ❌ Low follower-to-following ratio (<1.0)
- ❌ No profile picture or bio

### Shadowban Indicators
1. Your tweets don't appear in hashtag searches
2. Replies don't show under other people's posts
3. Sudden engagement cliff (90%+ drop)
4. "This tweet is unavailable" for others

**Recovery**: Stop posting 24-48h, then post only high-quality content for 2 weeks.

---

## Thread Optimization

### Thread Structure That Works

```
Tweet 1: HOOK - Must stand alone, no "thread" or "🧵" in hook
Tweet 2-3: The PROBLEM - Why this matters
Tweet 4-7: The SOLUTION - Step by step value
Tweet 8: SUMMARY - Key takeaways
Tweet 9: CTA - Follow for more / link in reply
```

### Thread Rules
- First tweet MUST work standalone
- Each tweet should make sense alone (people quote-tweet mid-thread)
- Number your tweets (1/, 2/, etc.) for scannability
- Add images/videos throughout - not just first tweet
- Put links in LAST tweet or reply to thread

### Thread Length Sweet Spots
- **5-7 tweets**: Best engagement per tweet
- **10-15 tweets**: Maximum total engagement
- **20+ tweets**: Diminishing returns, looks spammy

---

## X Articles (Long-form)

### Hook Patterns (Proven 10K+ engagement)

**The Insecurity Hook**
> "Everyone's talking about [X] and you're still wondering if you missed the window..."

**The RIP Hook**
> "RIP [profession]. This AI tool will [action] in [time]."

**The Secret Hook**
> "I spent [time] studying [X]. Here's what nobody tells you..."

**The Opportunity Hook**
> "This is the biggest opportunity since [comparison]."

**The Mistake Hook**
> "I wasted [time/money] making these [N] mistakes. Don't repeat them."

### Article Structure (Optimized)

```
1. HOOK (insecurity, curiosity, or opportunity gap)
2. SOCIAL PROOF (why you're credible to write this)
3. THE PROBLEM (what's at stake)
4. THE SOLUTION (your framework/method)
5. STEP-BY-STEP (numbered, actionable)
6. OBJECTION HANDLING (why most won't do it)
7. RESULTS (what they'll get)
8. URGENCY (why now)
9. CTA (specific next action)
```

### Article Formatting
- **H2 headers** for each major section
- **Bold** key phrases (but not entire sentences)
- **Bullet lists** for scanability
- **Time estimates** for each step
- **Copy-paste templates** when applicable
- **No em dashes** - use commas or periods
- **Short paragraphs** - 2-3 sentences max

---

## Account Health Factors

### TrustScore Components
- Account age (older = more trust)
- Verification status (Premium boost)
- Follower-to-following ratio
- Historical engagement rate
- Report/block rate received
- Content policy violations
- Authentic follower percentage

### The Follower Ratio Rule
```
Ratio > 10:1   = Authority signal (boost)
Ratio 2:1-10:1 = Healthy (neutral)
Ratio 1:1-2:1  = Warning zone
Ratio < 1:1    = Follow-farming penalty
```

### Premium/Verification Benefits
- Higher ranking in For You tab
- Posts shown to non-followers more
- Priority in replies
- Longer tweet limit (4,000 chars)
- Edit tweets ability
- Bookmark folders
- Blue checkmark social proof

---

## Growth Tactics

### 1. Reply Guy Strategy (0-1K followers)
1. Turn on notifications for 10-20 large accounts in your niche
2. Be FIRST with a thoughtful reply (within 5 minutes)
3. Add genuine value - insight, question, or experience
4. Don't shill - just be helpful
5. Their audience discovers you through great replies

### 2. Quote Tweet Takeover (1K-10K)
1. Find viral posts in your niche
2. Quote tweet with "Let me explain why this matters..."
3. Add 3-5 points of genuine value
4. Credit the original author
5. Builds authority + captures their audience

### 3. Thread Dominance (10K-100K)
1. Post 2-3 educational threads per week
2. Repurpose into video/carousel
3. Cross-promote on other platforms
4. Build email list from thread CTAs
5. Threads compound - old threads still get discovered

### 4. Controversy Calibration
- Mild hot takes: 2-3x engagement
- Spicy opinions: 5-10x engagement but risky
- Inflammatory: viral but attracts reports

**Rule**: Only be controversial about things you genuinely believe.

---

## Engagement Farming Techniques

### Question Formulas
- "What's the most [adjective] [thing] you've ever [done]?"
- "Unpopular opinion: [statement]. Agree or disagree?"
- "If you could only [do X] for the rest of your life, what would it be?"
- "Name a [thing] that's overrated. I'll start: [example]"
- "Wrong answers only: What is [X]?"

### Reply Bait Patterns
- Leave something incomplete for people to correct
- Make a slightly wrong statement (people LOVE correcting)
- Ask for recommendations
- Start a debate between two options
- "Fill in the blank: ____"

### Engagement Pods (Use Carefully)
- Small group (5-10 people) in your niche
- Engage with each other's content in first 30 min
- Genuine comments only (algorithm detects fake)
- Don't overdo - 1-2 posts per person per day

---

## The No-Link Strategy

### Why Links Kill Reach
- X wants users to stay on platform
- Link posts get 0.3x normal reach
- Affiliate links are especially suppressed

### Link Placement Strategy
```
❌ Bad:  "Check out my course [link]"
✅ Good: "I made a free guide on [topic]. Drop a 🔥 and I'll DM it to you."
✅ Good: Thread → Link in final tweet or reply
✅ Good: "Link in bio" (but don't overuse)
✅ Good: Pin tweet with link, reference in other tweets
```

---

## Analytics That Matter

### Key Metrics to Track
1. **Impressions/Follower**: How far your content spreads
2. **Engagement Rate**: (Likes + RTs + Replies) / Impressions
3. **Reply Rate**: Replies / Impressions (most important)
4. **Follower Growth Rate**: Weekly net new followers
5. **Profile Click Rate**: Profile clicks / Impressions

### Healthy Benchmarks
| Metric | Poor | Average | Good | Great |
|--------|------|---------|------|-------|
| Engagement Rate | <1% | 1-3% | 3-6% | >6% |
| Reply Rate | <0.1% | 0.1-0.5% | 0.5-1% | >1% |
| Profile Click Rate | <0.5% | 0.5-1% | 1-2% | >2% |

---

## Quick Checklist

### Before Posting
- [ ] Hook in first line?
- [ ] Reason to reply/engage?
- [ ] No external links? (move to reply)
- [ ] Under 280 chars? (or thread it properly)
- [ ] Media attached? (image/video)
- [ ] Posting at good time?
- [ ] Available to engage for 30 min after?

### After Posting
- [ ] Reply to every comment in first 2 hours
- [ ] Like comments (shows appreciation)
- [ ] Retweet best replies (rewards engagement)
- [ ] Quote tweet your own post with added context (after 4+ hours)

---

## Platform-Specific Notes

### For You vs Following
- **For You**: Algorithmic, includes non-followers, aim here for growth
- **Following**: Chronological, only followers, for community maintenance

### X Premium Tiers
- **Basic** ($3/mo): Half the algorithmic boost
- **Premium** ($8/mo): Full boost, edit tweets
- **Premium+** ($16/mo): No ads, highest boost

### API Changes (2024+)
- Free API heavily restricted
- Automated posting requires paid tier
- Rate limits tightened
- Third-party apps limited

---

## Sources

- X Algorithm GitHub (open source): github.com/twitter/the-algorithm
- X Engineering Blog
- Hootsuite, Sprout Social, SocialBee research
- Analysis of 10M+ tweets across engagement levels
- Growth data from 500+ accounts (0→100K journey)

---

## Installation

```bash
clawdhub install lxgicstudios/x-mastery
```

**Built by LXGIC Studios** - [@lxgicstudios](https://x.com/lxgicstudios)
