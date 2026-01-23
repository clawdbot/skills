#!/usr/bin/env python3
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path

def load_config(config_file):
    with open(config_file, 'r') as f:
        return json.load(f)

def load_criteria(criteria_file):
    """Load ranking criteria (the learned algorithm)"""
    with open(criteria_file, 'r') as f:
        return json.load(f)

def filter_recent(tweets, hours):
    """Filter tweets from last N hours"""
    cutoff = datetime.now() - timedelta(hours=hours)
    recent = []
    
    for tweet in tweets:
        try:
            # Parse Twitter date: "Thu Jan 22 21:14:20 +0000 2026"
            dt = datetime.strptime(tweet['createdAt'], '%a %b %d %H:%M:%S %z %Y')
            if dt.replace(tzinfo=None) >= cutoff:
                recent.append(tweet)
        except:
            continue
    
    return recent

def score_tweet(tweet, criteria):
    """Score tweet based on learned ranking criteria"""
    text = (tweet.get('text', '') + ' ' + tweet.get('user', {}).get('screenName', '')).lower()
    score = 50.0  # base
    
    # Match against all value categories
    matched_categories = []
    
    for category_name, category_data in criteria['value_categories'].items():
        weight = category_data['weight']
        keywords = category_data.get('keywords', [])
        
        # Check if any keywords match
        matches = sum(1 for kw in keywords if kw.lower() in text)
        
        if matches > 0:
            # Add weighted score
            category_boost = (weight / 100.0) * matches * 10
            score += category_boost
            matched_categories.append(category_name)
    
    # Apply engagement multipliers from criteria
    multipliers = criteria.get('engagement_multipliers', {})
    
    if tweet.get('isThread'):
        score *= multipliers.get('thread', 1.0)
    
    likes = tweet.get('favoriteCount', 0)
    if likes > 1000:
        score *= multipliers.get('high_likes', 1.0)
    
    retweets = tweet.get('retweetCount', 0)
    if retweets > 100:
        score *= multipliers.get('high_retweets', 1.0)
    
    if 'http' in text:
        score *= multipliers.get('has_link', 1.0)
    
    # Store matched categories for value analysis
    tweet['_matched_categories'] = matched_categories
    
    return round(score, 2)

def generate_markdown(ranked_tweets, output_dir, criteria):
    """Generate markdown reading list"""
    today = datetime.now().strftime('%Y-%m-%d')
    output_file = Path(output_dir) / f"twitter-reading-{today}.md"
    
    with open(output_file, 'w') as f:
        f.write(f"# Twitter Reading List - {datetime.now().strftime('%B %d, %Y')}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%I:%M %p')}\n")
        f.write(f"**Total bookmarks:** {len(ranked_tweets)}\n")
        f.write(f"**Ranking algorithm:** v{criteria.get('version', '1.0.0')}\n\n")
        f.write("---\n\n")
        
        # Group by priority
        high = [t for t in ranked_tweets if t['score'] >= 80]
        medium = [t for t in ranked_tweets if 60 <= t['score'] < 80]
        normal = [t for t in ranked_tweets if t['score'] < 60]
        
        if high:
            f.write("## 🔥 High Priority (Score 80+)\n\n")
            for t in high:
                write_tweet(f, t, criteria)
        
        if medium:
            f.write("## ⭐ Medium Priority (Score 60-79)\n\n")
            for t in medium:
                write_tweet(f, t, criteria)
        
        if normal:
            f.write("## 📌 Standard Priority (Score <60)\n\n")
            for t in normal:
                write_tweet(f, t, criteria)
    
    return str(output_file), high[:5]  # Return file and top 5

def analyze_value(tweet, criteria):
    """Generate value statement from matched categories"""
    matched = tweet.get('_matched_categories', [])
    
    if not matched:
        return "📌 High engagement in your interest areas"
    
    # Map categories to user-friendly value statements
    value_map = {
        'london_transition': "🎯 Relevant to your London move",
        'career_growth': "📈 Career advancement",
        'crypto_insights': "💰 Crypto work insights",
        'investment_strategy': "📊 Investment strategy",
        'founder_mindset': "🚀 Builder mindset",
        'growth_strategy': "📈 Growth/scaling",
        'relationship_dynamics': "❤️ Relationship insights",
        'psychology': "🧠 Psychology/behavior",
        'productivity_systems': "⚡ Productivity",
        'business_models': "💼 Business model",
        'technical_depth': "🔧 Technical depth"
    }
    
    values = []
    for category in matched[:3]:  # Top 3 matches
        if category in value_map:
            values.append(value_map[category])
        elif category.startswith('discovered_'):
            # Auto-discovered category
            topic = category.replace('discovered_', '').title()
            values.append(f"🔍 {topic}")
        else:
            # Use description from criteria
            desc = criteria['value_categories'].get(category, {}).get('description', category)
            values.append(f"• {desc}")
    
    return " • ".join(values) if values else "📌 Matches your interests"

def write_tweet(f, tweet, criteria):
    """Write single tweet to markdown with value analysis"""
    value_statement = analyze_value(tweet, criteria)
    
    f.write(f"### {tweet['rank']}. @{tweet['author']} (Score: {tweet['score']})\n\n")
    f.write(f"**Why this matters:** {value_statement}\n\n")
    f.write(f"{tweet['text']}\n\n")
    f.write(f"👍 {tweet['likes']} | 🔁 {tweet['retweets']}\n\n")
    f.write(f"🔗 {tweet['url']}\n\n")
    f.write("---\n\n")

def main():
    if len(sys.argv) < 5:
        print("Usage: rank.py <bookmarks.json> <config.json> <criteria.json> <output_dir>")
        sys.exit(1)
    
    bookmarks_file = sys.argv[1]
    config_file = sys.argv[2]
    criteria_file = sys.argv[3]
    output_dir = sys.argv[4]
    
    # Load data
    with open(bookmarks_file, 'r') as f:
        data = json.load(f)
    
    config = load_config(config_file)
    criteria = load_criteria(criteria_file)
    
    tweets = data['tweets']
    lookback_hours = config.get('lookback_hours', 24)  # Changed to 24h as per new spec
    
    # Filter recent
    recent = filter_recent(tweets, lookback_hours)
    print(f"Found {len(recent)} bookmarks from last {lookback_hours} hours")
    
    if not recent:
        print("No recent bookmarks to rank")
        sys.exit(0)
    
    # Score and rank using learned criteria
    for tweet in recent:
        tweet['score'] = score_tweet(tweet, criteria)
    
    ranked = sorted(recent, key=lambda t: t['score'], reverse=True)[:20]
    
    # Prepare output
    for i, tweet in enumerate(ranked, 1):
        tweet['rank'] = i
        tweet['author'] = tweet.get('user', {}).get('screenName', 'unknown')
        tweet['text'] = tweet.get('text', '')[:300]
        tweet['url'] = f"https://x.com/{tweet['author']}/status/{tweet.get('tweetId', '')}"
        tweet['likes'] = tweet.get('favoriteCount', 0)
        tweet['retweets'] = tweet.get('retweetCount', 0)
    
    # Generate markdown
    output_file, top5 = generate_markdown(ranked, output_dir, criteria)
    
    print(f"✅ Reading list saved: {output_file}")
    print(f"✅ Top 5 bookmarks (scores: {[t['score'] for t in top5]})")
    
    # Save top 5 for notification
    top5_file = Path(output_dir) / f"twitter-top5-{datetime.now().strftime('%Y-%m-%d')}.json"
    with open(top5_file, 'w') as f:
        json.dump(top5, f, indent=2)
    
    print(f"✅ Top 5 saved for notification: {top5_file}")

if __name__ == '__main__':
    main()
