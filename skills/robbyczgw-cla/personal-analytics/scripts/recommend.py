#!/usr/bin/env python3
"""
Topic recommendations for proactive-research integration.

Analyzes conversation patterns and suggests topics to monitor.
"""

import sys
import argparse
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(__file__).parent))

from config import load_data, get_integration_settings, is_enabled


def get_recommendations(threshold: int = 3, explain: bool = False) -> list:
    """Get topic recommendations based on conversation patterns."""
    data = load_data()
    sessions = data.get("sessions", [])
    
    if not sessions:
        return []
    
    # Count topics
    topic_counter = Counter()
    topic_first_seen = {}
    topic_last_seen = {}
    
    for session in sessions:
        topics = session.get("topics", [])
        timestamp = session.get("start", "")
        
        for topic in topics:
            topic_counter[topic] += 1
            
            if topic not in topic_first_seen:
                topic_first_seen[topic] = timestamp
            topic_last_seen[topic] = timestamp
    
    # Get integration settings
    integration = get_integration_settings("proactive_research")
    min_sessions = integration.get("min_sessions_for_suggestion", 5)
    
    # Build recommendations
    recommendations = []
    
    for topic, count in topic_counter.items():
        if count < threshold:
            continue
        
        # Calculate metrics
        first_seen = topic_first_seen.get(topic)
        last_seen = topic_last_seen.get(topic)
        
        # Determine reason
        if count >= min_sessions * 2:
            reason = "High frequency, strong consistent interest"
            priority = "high"
        elif count >= min_sessions:
            reason = "Consistent interest over time"
            priority = "medium"
        else:
            reason = "Emerging topic"
            priority = "low"
        
        # Suggest frequency based on count
        if count >= 20:
            frequency = "hourly"
        elif count >= 10:
            frequency = "daily"
        else:
            frequency = "weekly"
        
        # Build recommendation
        rec = {
            "topic": topic,
            "count": count,
            "reason": reason,
            "priority": priority,
            "suggested_query": f"{topic} updates news releases",
            "suggested_frequency": frequency,
            "first_seen": first_seen,
            "last_seen": last_seen
        }
        
        if explain:
            rec["explanation"] = f"Mentioned {count} times. {reason}."
        
        recommendations.append(rec)
    
    # Sort by count
    recommendations.sort(key=lambda x: x["count"], reverse=True)
    
    return recommendations


def check_existing_topics(recommendations: list) -> list:
    """Check which topics are already being monitored."""
    # Try to load proactive-research config
    pr_config_path = Path(__file__).parent.parent.parent / "proactive-research" / "config.json"
    
    if not pr_config_path.exists():
        return recommendations
    
    try:
        import json
        with open(pr_config_path) as f:
            pr_config = json.load(f)
        
        existing_topics = set()
        for topic_config in pr_config.get("topics", []):
            # Extract keywords to match
            keywords = topic_config.get("keywords", [])
            existing_topics.update([k.lower() for k in keywords])
        
        # Mark existing
        for rec in recommendations:
            topic_name = rec["topic"].lower()
            if topic_name in existing_topics:
                rec["already_monitored"] = True
            else:
                rec["already_monitored"] = False
    
    except Exception:
        pass
    
    return recommendations


def print_recommendations(recommendations: list, explain: bool = False):
    """Print recommendations in human-readable format."""
    if not recommendations:
        print("No recommendations at this time.")
        return
    
    print("\n💡 Topic Recommendations for Proactive Research\n")
    print("Based on your conversation patterns:\n")
    
    for idx, rec in enumerate(recommendations, 1):
        topic = rec["topic"]
        count = rec["count"]
        reason = rec["reason"]
        query = rec["suggested_query"]
        frequency = rec["suggested_frequency"]
        already_monitored = rec.get("already_monitored", False)
        
        print(f"{idx}. **{topic}**")
        print(f"   Mentioned: {count} times")
        print(f"   Reason: {reason}")
        
        if explain:
            print(f"   Explanation: {rec.get('explanation', '')}")
        
        if already_monitored:
            print(f"   ✓ Already monitoring")
        else:
            print(f"   Suggested query: \"{query}\"")
            print(f"   Suggested frequency: {frequency}")
        
        print()


def auto_add_topics(recommendations: list) -> int:
    """Auto-add topics to proactive-research."""
    pr_manage_script = Path(__file__).parent.parent.parent / "proactive-research" / "scripts" / "manage_topics.py"
    
    if not pr_manage_script.exists():
        print("❌ proactive-research skill not found", file=sys.stderr)
        return 0
    
    added = 0
    
    for rec in recommendations:
        if rec.get("already_monitored", False):
            continue
        
        topic = rec["topic"]
        query = rec["suggested_query"]
        frequency = rec["suggested_frequency"]
        
        # Ask for confirmation
        response = input(f"Add '{topic}' to proactive-research? [y/N]: ").strip().lower()
        
        if response not in ("y", "yes"):
            continue
        
        # Add via manage_topics.py
        import subprocess
        try:
            result = subprocess.run(
                [
                    "python3", str(pr_manage_script), "add", topic,
                    "--query", query,
                    "--keywords", topic,
                    "--frequency", frequency,
                    "--importance", "medium",
                    "--context", f"Auto-suggested by personal-analytics (mentioned {rec['count']} times)"
                ],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                print(f"✅ Added '{topic}' to proactive-research")
                added += 1
            else:
                print(f"❌ Failed to add '{topic}': {result.stderr}", file=sys.stderr)
        
        except Exception as e:
            print(f"❌ Error adding '{topic}': {e}", file=sys.stderr)
    
    return added


def main():
    parser = argparse.ArgumentParser(description="Get topic recommendations")
    parser.add_argument("--threshold", type=int, default=3,
                       help="Minimum mentions to suggest (default: 3)")
    parser.add_argument("--explain", action="store_true",
                       help="Show detailed explanations")
    parser.add_argument("--auto-add", action="store_true",
                       help="Interactively add topics to proactive-research")
    parser.add_argument("--json", action="store_true",
                       help="Output JSON")
    
    args = parser.parse_args()
    
    if not is_enabled():
        print("⚠️ Analytics tracking is disabled", file=sys.stderr)
        sys.exit(1)
    
    # Get recommendations
    recommendations = get_recommendations(threshold=args.threshold, explain=args.explain)
    recommendations = check_existing_topics(recommendations)
    
    if args.json:
        import json
        print(json.dumps(recommendations, indent=2))
    else:
        print_recommendations(recommendations, explain=args.explain)
    
    # Auto-add if requested
    if args.auto_add and recommendations:
        print("\n" + "="*60)
        added = auto_add_topics(recommendations)
        print(f"\n✅ Added {added} topic(s) to proactive-research")


if __name__ == "__main__":
    main()
