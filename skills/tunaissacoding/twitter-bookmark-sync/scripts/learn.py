#!/usr/bin/env python3
"""
Learn from bookmarks and update ranking criteria
Analyzes bookmarks, categorizes by topic+value, updates weights with time decay
"""
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
import re

def load_criteria(criteria_file):
    """Load existing ranking criteria"""
    with open(criteria_file, 'r') as f:
        return json.load(f)

def apply_time_decay(criteria):
    """Apply time decay to all category weights"""
    now = datetime.now()
    decay_rate = criteria['decay_rate']
    
    for category, data in criteria['value_categories'].items():
        last_seen = datetime.fromisoformat(data['last_seen'])
        days_since = (now - last_seen).days
        
        if days_since > 0:
            # Apply exponential decay
            decay_factor = decay_rate ** days_since
            data['weight'] = data['weight'] * decay_factor
            
            # Minimum weight floor
            if data['weight'] < 10:
                data['weight'] = 10
    
    return criteria

def categorize_bookmark(tweet):
    """
    Categorize bookmark by topic and value type
    Returns: (category_name, value_type, confidence)
    """
    text = (tweet.get('text', '') + ' ' + tweet.get('user', {}).get('description', '')).lower()
    
    # Extract topics and determine value
    categories = []
    
    # Career/Professional
    if any(kw in text for kw in ['london', 'uk', 'visa', 'europe', 'immigration']):
        categories.append(('london_transition', 'goal_aligned', 0.9))
    if any(kw in text for kw in ['career', 'staff', 'senior', 'promotion', 'engineer']):
        categories.append(('career_growth', 'skill_building', 0.8))
    
    # Crypto/Finance
    if any(kw in text for kw in ['crypto', 'btc', 'eth', 'defi', 'web3', 'blockchain']):
        categories.append(('crypto_insights', 'work_relevant', 0.9))
    if any(kw in text for kw in ['investment', 'portfolio', 'fund', 'trading', 'market']):
        categories.append(('investment_strategy', 'work_relevant', 0.8))
    
    # Building/Growth
    if any(kw in text for kw in ['startup', 'founder', 'build', 'product', 'launch']):
        categories.append(('founder_mindset', 'mindset', 0.8))
    if any(kw in text for kw in ['growth', 'scale', 'gtm', 'distribution', 'acquisition']):
        categories.append(('growth_strategy', 'skill_building', 0.7))
    
    # Personal
    if any(kw in text for kw in ['relationship', 'dating', 'communication', 'partner']):
        categories.append(('relationship_dynamics', 'personal_growth', 0.8))
    if any(kw in text for kw in ['psychology', 'behavior', 'mindset', 'mental', 'therapy']):
        categories.append(('psychology', 'personal_growth', 0.7))
    
    # Productivity/Systems
    if any(kw in text for kw in ['productivity', 'system', 'habit', 'focus', 'deep work']):
        categories.append(('productivity_systems', 'optimization', 0.7))
    
    # Business
    if any(kw in text for kw in ['business', 'revenue', 'monetize', 'niche', 'saas']):
        categories.append(('business_models', 'learning', 0.7))
    
    # Technical
    if any(kw in text for kw in ['backend', 'architecture', 'code', 'engineering', 'system design']):
        categories.append(('technical_depth', 'skill_building', 0.7))
    
    # Discover new categories from engagement
    if not categories and tweet.get('favoriteCount', 0) > 500:
        # High engagement but no match - potential new category
        # Extract main topic heuristically
        words = re.findall(r'\b[a-z]{4,}\b', text)
        if words:
            top_word = max(set(words), key=words.count)
            categories.append((f'discovered_{top_word}', 'unknown', 0.5))
    
    return categories if categories else [('general_interest', 'unknown', 0.3)]

def update_criteria_from_bookmarks(criteria, bookmarks):
    """
    Update criteria weights based on new bookmarks
    Reinforces categories seen, reduces decay for active interests
    """
    now = datetime.now()
    category_updates = {}
    
    for tweet in bookmarks:
        categories = categorize_bookmark(tweet)
        
        for category_name, value_type, confidence in categories:
            if category_name not in category_updates:
                category_updates[category_name] = {
                    'count': 0,
                    'total_confidence': 0,
                    'value_type': value_type,
                    'engagement': 0
                }
            
            category_updates[category_name]['count'] += 1
            category_updates[category_name]['total_confidence'] += confidence
            category_updates[category_name]['engagement'] += tweet.get('favoriteCount', 0)
    
    # Apply updates to criteria
    for category_name, update_data in category_updates.items():
        if category_name in criteria['value_categories']:
            # Existing category - reinforce and reset decay
            cat = criteria['value_categories'][category_name]
            
            # Boost weight based on frequency and confidence
            boost = update_data['count'] * (update_data['total_confidence'] / update_data['count']) * 5
            cat['weight'] = min(cat['weight'] + boost, 100)  # Cap at 100
            
            # Reset last_seen (reduces future decay)
            cat['last_seen'] = now.isoformat()
            
        elif category_name.startswith('discovered_'):
            # New discovered category
            criteria['value_categories'][category_name] = {
                'weight': 40,  # Start moderate
                'last_seen': now.isoformat(),
                'keywords': [category_name.replace('discovered_', '')],
                'value_type': update_data['value_type'],
                'description': f"Auto-discovered from bookmarks ({update_data['count']} instances)"
            }
    
    return criteria

def normalize_weights(criteria):
    """Normalize weights to maintain relative proportions"""
    weights = [cat['weight'] for cat in criteria['value_categories'].values()]
    
    if not weights:
        return criteria
    
    max_weight = max(weights)
    
    # Keep top category at 100, scale others proportionally
    if max_weight > 0:
        scale_factor = 100.0 / max_weight
        for cat in criteria['value_categories'].values():
            cat['weight'] = round(cat['weight'] * scale_factor, 2)
    
    return criteria

def main():
    if len(sys.argv) < 3:
        print("Usage: learn.py <bookmarks.json> <criteria.json>")
        sys.exit(1)
    
    bookmarks_file = sys.argv[1]
    criteria_file = sys.argv[2]
    
    # Load data
    with open(bookmarks_file, 'r') as f:
        bookmarks_data = json.load(f)
    
    bookmarks = bookmarks_data.get('tweets', [])
    
    criteria = load_criteria(criteria_file)
    
    print(f"Learning from {len(bookmarks)} bookmarks...")
    
    # Step 1: Apply time decay
    print("Applying time decay to existing weights...")
    criteria = apply_time_decay(criteria)
    
    # Step 2: Categorize and update from new bookmarks
    print("Categorizing new bookmarks...")
    criteria = update_criteria_from_bookmarks(criteria, bookmarks)
    
    # Step 3: Normalize weights
    print("Normalizing weights...")
    criteria = normalize_weights(criteria)
    
    # Update metadata
    criteria['last_updated'] = datetime.now().isoformat()
    criteria['version'] = str(float(criteria.get('version', '1.0.0')) + 0.1)
    
    # Save updated criteria
    with open(criteria_file, 'w') as f:
        json.dump(criteria, f, indent=2)
    
    print(f"✅ Criteria updated: {criteria_file}")
    print(f"   Version: {criteria['version']}")
    print(f"   Active categories: {len(criteria['value_categories'])}")
    
    # Show top categories
    sorted_cats = sorted(
        criteria['value_categories'].items(),
        key=lambda x: x[1]['weight'],
        reverse=True
    )[:5]
    
    print("\n   Top 5 categories:")
    for name, data in sorted_cats:
        print(f"     - {name}: {data['weight']:.1f}")

if __name__ == '__main__':
    main()
