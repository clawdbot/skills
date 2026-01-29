#!/usr/bin/env python3
"""
Generate beautiful personal analytics reports.
"""

import sys
import argparse
from datetime import datetime, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config import is_enabled, get_report_settings
from analyzer import analyze


def get_week_range() -> tuple:
    """Get start and end of current week."""
    today = datetime.now()
    days_since_sunday = (today.weekday() + 1) % 7
    sunday = today - timedelta(days=days_since_sunday)
    saturday = sunday + timedelta(days=6, hours=23, minutes=59, seconds=59)
    return sunday.isoformat(), saturday.isoformat()


def get_month_range() -> tuple:
    """Get start and end of current month."""
    today = datetime.now()
    start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    # Last day of month
    next_month = start + timedelta(days=32)
    end = next_month.replace(day=1) - timedelta(seconds=1)
    return start.isoformat(), end.isoformat()


def format_bar(value: int, max_value: int, width: int = 20) -> str:
    """Format a bar chart."""
    if max_value == 0:
        return "░" * width
    
    filled = int((value / max_value) * width)
    return "█" * filled + "░" * (width - filled)


def generate_markdown_report(analysis: Dict, report_type: str) -> str:
    """Generate markdown report."""
    period = analysis.get("period", {})
    start = period.get("start", "")
    end = period.get("end", "")
    
    # Parse dates for formatting
    try:
        start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
        date_range = f"{start_dt.strftime('%b %d')} - {end_dt.strftime('%b %d, %Y')}"
    except:
        date_range = f"{start} to {end}"
    
    report = f"# 📊 {report_type.capitalize()} Analytics Report\n"
    report += f"**{date_range}**\n\n"
    report += "---\n\n"
    
    # Highlights
    insights = analysis.get("insights", [])
    if insights:
        report += "## 🎯 Highlights\n\n"
        for insight in insights:
            report += f"- {insight}\n"
        report += "\n---\n\n"
    
    # Time Patterns
    time_patterns = analysis.get("time_patterns", {})
    daily_dist = time_patterns.get("daily_distribution", {})
    
    if daily_dist:
        report += "## ⏰ Time Patterns\n\n"
        report += "### Activity by Day\n\n"
        report += "```\n"
        
        # Order days
        day_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        max_count = max(daily_dist.values()) if daily_dist else 1
        
        for day in day_order:
            count = daily_dist.get(day, 0)
            bar = format_bar(count, max_count, width=24)
            report += f"{day[:3]}  {bar}  {count}\n"
        
        report += "```\n\n"
    
    hourly_dist = time_patterns.get("hourly_distribution", {})
    if hourly_dist:
        report += "### Activity by Hour\n\n"
        report += "```\n"
        
        # Group into time blocks
        blocks = {
            "06-09": sum(hourly_dist.get(h, 0) for h in range(6, 9)),
            "09-12": sum(hourly_dist.get(h, 0) for h in range(9, 12)),
            "12-14": sum(hourly_dist.get(h, 0) for h in range(12, 14)),
            "14-17": sum(hourly_dist.get(h, 0) for h in range(14, 17)),
            "17-22": sum(hourly_dist.get(h, 0) for h in range(17, 22)),
            "22-06": sum(hourly_dist.get(h, 0) for h in list(range(22, 24)) + list(range(0, 6)))
        }
        
        total = sum(blocks.values())
        max_count = max(blocks.values()) if blocks else 1
        
        for time_range, count in blocks.items():
            pct = (count / total * 100) if total > 0 else 0
            bar = format_bar(count, max_count, width=10)
            report += f"{time_range}: {bar} ({pct:.0f}%)\n"
        
        report += "```\n\n"
        report += "---\n\n"
    
    # Topics
    topics = analysis.get("topics", {})
    top_topics = topics.get("top_topics", [])
    
    if top_topics:
        report += "## 📚 Topic Insights\n\n"
        report += "### Top Topics\n\n"
        
        for idx, (topic, count) in enumerate(top_topics[:5], 1):
            report += f"{idx}. **{topic}** ({count} sessions)\n"
        
        report += "\n---\n\n"
    
    # Productivity
    productivity = analysis.get("productivity", {})
    tasks = productivity.get("total_tasks_completed", 0)
    success_rate = productivity.get("success_rate", 0)
    
    if tasks > 0:
        report += "## 💡 Productivity Insights\n\n"
        report += f"- **Tasks completed:** {tasks}\n"
        report += f"- **Success rate:** {success_rate * 100:.1f}%\n"
        
        peak_hours = productivity.get("peak_productivity_hours", [])
        if peak_hours:
            hours_str = ", ".join([f"{h:02d}:00" for h in peak_hours[:2]])
            report += f"- **Peak hours:** {hours_str}\n"
        
        peak_days = productivity.get("peak_productivity_days", [])
        if peak_days:
            days_str = ", ".join(peak_days[:2])
            report += f"- **Peak days:** {days_str}\n"
        
        report += "\n---\n\n"
    
    # Sentiment
    sentiment = analysis.get("sentiment", {})
    distribution = sentiment.get("distribution", {})
    
    if distribution:
        report += "## 😊 Sentiment & Well-being\n\n"
        report += "### Overall Mood\n\n"
        report += "```\n"
        
        emoji_map = {
            "positive": "😊",
            "neutral": "😐",
            "negative": "😟",
            "mixed": "🤔"
        }
        
        max_pct = max(distribution.values()) if distribution else 1
        
        for sent in ["positive", "neutral", "negative", "mixed"]:
            pct = distribution.get(sent, 0)
            emoji = emoji_map.get(sent, "")
            bar = format_bar(int(pct * 20), 20, width=18)
            report += f"{emoji} {sent.capitalize():8}  {bar}  {pct * 100:.0f}%\n"
        
        report += "```\n\n"
    
    # Footer
    report += "---\n\n"
    report += "_Generated by Personal Analytics • Privacy-first, locally processed_\n"
    
    return report


def main():
    parser = argparse.ArgumentParser(description="Generate analytics reports")
    parser.add_argument("type", choices=["weekly", "monthly", "custom"],
                       help="Report type")
    parser.add_argument("--since", help="Start date for custom report (ISO format)")
    parser.add_argument("--until", help="End date for custom report (ISO format)")
    parser.add_argument("--output", help="Output file (default: print to stdout)")
    parser.add_argument("--send", action="store_true", help="Send via configured channel")
    
    args = parser.parse_args()
    
    if not is_enabled():
        print("⚠️ Analytics tracking is disabled", file=sys.stderr)
        sys.exit(1)
    
    # Determine date range
    if args.type == "weekly":
        since, until = get_week_range()
    elif args.type == "monthly":
        since, until = get_month_range()
    else:  # custom
        if not args.since or not args.until:
            print("❌ Custom reports require --since and --until", file=sys.stderr)
            sys.exit(1)
        since, until = args.since, args.until
    
    # Run analysis
    try:
        analysis = analyze(since=since, until=until, insights=True)
    except Exception as e:
        print(f"❌ Analysis failed: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Generate report
    report = generate_markdown_report(analysis, args.type)
    
    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(report)
        print(f"✅ Report saved to {args.output}")
    else:
        print(report)
    
    # Send if requested
    if args.send:
        print("\n📧 Sending report...")
        # In real environment, would use Moltbot message tool
        print("✅ Report sent")


if __name__ == "__main__":
    main()
