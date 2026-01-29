#!/usr/bin/env python3
"""
Personal Analytics Analyzer

Analyzes conversation patterns and generates insights.
"""

import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from collections import defaultdict, Counter
from typing import Dict, List, Tuple

sys.path.insert(0, str(Path(__file__).parent))

from config import load_data, is_enabled


def parse_datetime(dt_str: str) -> datetime:
    """Parse datetime string."""
    return datetime.fromisoformat(dt_str.replace('Z', '+00:00'))


def filter_sessions(sessions: List[Dict], since: str = None, until: str = None) -> List[Dict]:
    """Filter sessions by date range."""
    if not since and not until:
        return sessions
    
    filtered = []
    since_dt = parse_datetime(since) if since else None
    until_dt = parse_datetime(until) if until else None
    
    for session in sessions:
        session_dt = parse_datetime(session.get("start", ""))
        
        if since_dt and session_dt < since_dt:
            continue
        if until_dt and session_dt > until_dt:
            continue
        
        filtered.append(session)
    
    return filtered


def calculate_total_time(sessions: List[Dict]) -> int:
    """Calculate total time in seconds."""
    return sum(s.get("duration_seconds", 0) for s in sessions)


def format_duration(seconds: int) -> str:
    """Format duration as human-readable string."""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        minutes = seconds // 60
        return f"{minutes}m {seconds % 60}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"


def analyze_time_patterns(sessions: List[Dict]) -> Dict:
    """Analyze time-based patterns."""
    hourly = Counter()
    daily = Counter()
    
    for session in sessions:
        start_dt = parse_datetime(session.get("start", ""))
        
        # Hour
        hour = start_dt.hour
        hourly[hour] += 1
        
        # Day of week
        day = start_dt.strftime("%A")
        daily[day] += 1
    
    # Find peak hour
    peak_hour = max(hourly.items(), key=lambda x: x[1]) if hourly else (0, 0)
    
    # Find peak day
    peak_day = max(daily.items(), key=lambda x: x[1]) if daily else ("Unknown", 0)
    
    return {
        "hourly_distribution": dict(hourly),
        "daily_distribution": dict(daily),
        "peak_hour": peak_hour[0],
        "peak_day": peak_day[0]
    }


def analyze_topics(sessions: List[Dict]) -> Dict:
    """Analyze topic patterns."""
    topic_counter = Counter()
    topic_sessions = defaultdict(list)
    
    for session in sessions:
        topics = session.get("topics", [])
        session_id = session.get("id")
        
        for topic in topics:
            topic_counter[topic] += 1
            topic_sessions[topic].append(session_id)
    
    # Top topics
    top_topics = topic_counter.most_common(10)
    
    return {
        "top_topics": top_topics,
        "total_unique_topics": len(topic_counter),
        "topic_sessions": dict(topic_sessions)
    }


def analyze_productivity(sessions: List[Dict]) -> Dict:
    """Analyze productivity patterns."""
    hourly_productivity = defaultdict(list)
    daily_productivity = defaultdict(list)
    
    total_tasks = 0
    successful_sessions = 0
    
    for session in sessions:
        start_dt = parse_datetime(session.get("start", ""))
        productivity_score = session.get("productivity_score", 0)
        tasks_completed = session.get("tasks_completed", 0)
        
        hour = start_dt.hour
        day = start_dt.strftime("%A")
        
        hourly_productivity[hour].append(productivity_score)
        daily_productivity[day].append(productivity_score)
        
        total_tasks += tasks_completed
        if productivity_score > 0.5:
            successful_sessions += 1
    
    # Calculate averages
    hourly_avg = {
        hour: sum(scores) / len(scores)
        for hour, scores in hourly_productivity.items()
    }
    
    daily_avg = {
        day: sum(scores) / len(scores)
        for day, scores in daily_productivity.items()
    }
    
    # Find peak productivity times
    peak_hours = sorted(hourly_avg.items(), key=lambda x: x[1], reverse=True)[:3]
    peak_days = sorted(daily_avg.items(), key=lambda x: x[1], reverse=True)[:3]
    
    return {
        "total_tasks_completed": total_tasks,
        "successful_sessions": successful_sessions,
        "success_rate": successful_sessions / len(sessions) if sessions else 0,
        "peak_productivity_hours": [h[0] for h in peak_hours],
        "peak_productivity_days": [d[0] for d in peak_days],
        "hourly_productivity": hourly_avg,
        "daily_productivity": daily_avg
    }


def analyze_sentiment(sessions: List[Dict]) -> Dict:
    """Analyze sentiment patterns."""
    sentiment_counter = Counter()
    sentiment_by_hour = defaultdict(list)
    sentiment_by_day = defaultdict(list)
    
    sentiment_map = {
        "positive": 1.0,
        "neutral": 0.0,
        "negative": -1.0,
        "mixed": 0.5
    }
    
    for session in sessions:
        sentiment = session.get("sentiment", "neutral")
        start_dt = parse_datetime(session.get("start", ""))
        
        sentiment_counter[sentiment] += 1
        
        hour = start_dt.hour
        day = start_dt.strftime("%A")
        
        sentiment_score = sentiment_map.get(sentiment, 0)
        sentiment_by_hour[hour].append(sentiment_score)
        sentiment_by_day[day].append(sentiment_score)
    
    # Calculate averages
    hourly_avg = {
        hour: sum(scores) / len(scores)
        for hour, scores in sentiment_by_hour.items()
    }
    
    daily_avg = {
        day: sum(scores) / len(scores)
        for day, scores in sentiment_by_day.items()
    }
    
    total = sum(sentiment_counter.values())
    distribution = {
        sentiment: count / total
        for sentiment, count in sentiment_counter.items()
    } if total > 0 else {}
    
    return {
        "distribution": distribution,
        "sentiment_by_hour": hourly_avg,
        "sentiment_by_day": daily_avg,
        "overall_score": sum(sentiment_map[s] * c for s, c in sentiment_counter.items()) / total if total > 0 else 0
    }


def generate_insights(analysis: Dict) -> List[str]:
    """Generate human-readable insights."""
    insights = []
    
    # Time insights
    time_patterns = analysis.get("time_patterns", {})
    peak_hour = time_patterns.get("peak_hour")
    peak_day = time_patterns.get("peak_day")
    
    if peak_hour is not None:
        insights.append(f"Most active hour: {peak_hour:02d}:00")
    if peak_day:
        insights.append(f"Most active day: {peak_day}")
    
    # Productivity insights
    productivity = analysis.get("productivity", {})
    peak_hours = productivity.get("peak_productivity_hours", [])
    
    if peak_hours:
        hours_str = ", ".join([f"{h:02d}:00" for h in peak_hours[:2]])
        insights.append(f"Peak productivity: {hours_str}")
    
    # Topic insights
    topics = analysis.get("topics", {})
    top_topics = topics.get("top_topics", [])
    
    if top_topics:
        top_topic = top_topics[0]
        insights.append(f"Top topic: {top_topic[0]} ({top_topic[1]} sessions)")
    
    # Sentiment insights
    sentiment = analysis.get("sentiment", {})
    overall_score = sentiment.get("overall_score", 0)
    
    if overall_score > 0.5:
        insights.append("Overall mood: Positive 😊")
    elif overall_score < -0.2:
        insights.append("Overall mood: Challenging 😟")
    else:
        insights.append("Overall mood: Balanced 😐")
    
    return insights


def analyze(since: str = None, until: str = None, insights: bool = False, verbose: bool = False) -> Dict:
    """Main analysis function."""
    if not is_enabled():
        print("⚠️ Analytics tracking is disabled", file=sys.stderr)
        return {}
    
    # Load data
    data = load_data()
    sessions = data.get("sessions", [])
    
    if not sessions:
        print("⚠️ No session data available", file=sys.stderr)
        return {}
    
    # Filter by date range
    filtered_sessions = filter_sessions(sessions, since=since, until=until)
    
    if not filtered_sessions:
        print("⚠️ No sessions in specified range", file=sys.stderr)
        return {}
    
    # Run analyses
    analysis = {
        "period": {
            "start": since or filtered_sessions[0].get("start"),
            "end": until or filtered_sessions[-1].get("end"),
            "session_count": len(filtered_sessions)
        },
        "time_patterns": analyze_time_patterns(filtered_sessions),
        "topics": analyze_topics(filtered_sessions),
        "productivity": analyze_productivity(filtered_sessions),
        "sentiment": analyze_sentiment(filtered_sessions)
    }
    
    # Generate insights
    if insights:
        analysis["insights"] = generate_insights(analysis)
    
    return analysis


def print_analysis(analysis: Dict, verbose: bool = False):
    """Print analysis results."""
    period = analysis.get("period", {})
    
    print("\n📊 Personal Analytics Analysis\n")
    print(f"Period: {period.get('start', 'N/A')} to {period.get('end', 'N/A')}")
    print(f"Sessions: {period.get('session_count', 0)}\n")
    
    # Time patterns
    time_patterns = analysis.get("time_patterns", {})
    print("⏰ Time Patterns:")
    print(f"  Peak hour: {time_patterns.get('peak_hour', 'N/A'):02d}:00")
    print(f"  Peak day: {time_patterns.get('peak_day', 'N/A')}\n")
    
    # Topics
    topics = analysis.get("topics", {})
    top_topics = topics.get("top_topics", [])
    print(f"📚 Top Topics ({len(top_topics)}):")
    for idx, (topic, count) in enumerate(top_topics[:5], 1):
        print(f"  {idx}. {topic} ({count} sessions)")
    print()
    
    # Productivity
    productivity = analysis.get("productivity", {})
    print("💡 Productivity:")
    print(f"  Tasks completed: {productivity.get('total_tasks_completed', 0)}")
    print(f"  Success rate: {productivity.get('success_rate', 0) * 100:.1f}%")
    peak_hours = productivity.get("peak_productivity_hours", [])
    if peak_hours:
        hours_str = ", ".join([f"{h:02d}:00" for h in peak_hours[:2]])
        print(f"  Peak hours: {hours_str}")
    print()
    
    # Sentiment
    sentiment = analysis.get("sentiment", {})
    distribution = sentiment.get("distribution", {})
    print("😊 Sentiment:")
    for sent, pct in distribution.items():
        emoji = {"positive": "😊", "neutral": "😐", "negative": "😟", "mixed": "🤔"}.get(sent, "")
        print(f"  {emoji} {sent.capitalize()}: {pct * 100:.1f}%")
    print()
    
    # Insights
    if "insights" in analysis:
        print("💡 Insights:")
        for insight in analysis["insights"]:
            print(f"  • {insight}")
        print()


def main():
    parser = argparse.ArgumentParser(description="Analyze conversation patterns")
    parser.add_argument("--since", help="Start date (ISO format)")
    parser.add_argument("--until", help="End date (ISO format)")
    parser.add_argument("--insights", action="store_true", help="Generate insights")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--json", action="store_true", help="Output JSON")
    
    args = parser.parse_args()
    
    try:
        analysis = analyze(
            since=args.since,
            until=args.until,
            insights=args.insights,
            verbose=args.verbose
        )
        
        if args.json:
            import json
            print(json.dumps(analysis, indent=2))
        else:
            print_analysis(analysis, verbose=args.verbose)
    
    except Exception as e:
        print(f"❌ Analysis failed: {e}", file=sys.stderr)
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
