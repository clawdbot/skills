#!/usr/bin/env python3
"""
Initialize ranking criteria from USER.md profile
Creates the initial sorting algorithm optimized for Clawdbot reading
"""
import json
import sys
from datetime import datetime
from pathlib import Path

def generate_initial_criteria():
    """Generate initial ranking criteria from Patrick's profile (USER.md)"""
    
    # Based on USER.md context
    criteria = {
        "version": "1.0.0",
        "created_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "decay_rate": 0.95,  # 5% decay per day
        
        "value_categories": {
            # Career/London transition (high priority for Patrick)
            "london_transition": {
                "weight": 100,
                "last_seen": datetime.now().isoformat(),
                "keywords": ["london", "uk", "visa", "immigration", "relocation", "europe"],
                "value_type": "goal_aligned",
                "description": "Moving to London for work"
            },
            "career_growth": {
                "weight": 95,
                "last_seen": datetime.now().isoformat(),
                "keywords": ["career", "staff", "senior", "promotion", "advancement", "engineer"],
                "value_type": "skill_building",
                "description": "Career advancement pathways"
            },
            
            # Crypto/Investment (current work)
            "crypto_insights": {
                "weight": 100,
                "last_seen": datetime.now().isoformat(),
                "keywords": ["crypto", "btc", "eth", "defi", "web3", "blockchain", "token"],
                "value_type": "work_relevant",
                "description": "Direct crypto work insights"
            },
            "investment_strategy": {
                "weight": 90,
                "last_seen": datetime.now().isoformat(),
                "keywords": ["investment", "portfolio", "fund", "trading", "market", "strategy", "alpha"],
                "value_type": "work_relevant",
                "description": "Investment approaches"
            },
            
            # Building/Startup (autonomy in fund)
            "founder_mindset": {
                "weight": 85,
                "last_seen": datetime.now().isoformat(),
                "keywords": ["startup", "founder", "build", "product", "launch", "0-to-1"],
                "value_type": "mindset",
                "description": "Builder/founder thinking"
            },
            "growth_strategy": {
                "weight": 80,
                "last_seen": datetime.now().isoformat(),
                "keywords": ["growth", "scale", "gtm", "go-to-market", "distribution"],
                "value_type": "skill_building",
                "description": "Growth/scaling strategies"
            },
            
            # Relationship (Sybil context)
            "relationship_dynamics": {
                "weight": 90,
                "last_seen": datetime.now().isoformat(),
                "keywords": ["relationship", "dating", "communication", "partner", "long-distance"],
                "value_type": "personal_growth",
                "description": "Relationship insights (Sybil)"
            },
            "psychology": {
                "weight": 75,
                "last_seen": datetime.now().isoformat(),
                "keywords": ["psychology", "behavior", "mindset", "mental", "therapy", "attachment"],
                "value_type": "personal_growth",
                "description": "Understanding human behavior"
            },
            
            # Productivity (diary keeper, self-aware)
            "productivity_systems": {
                "weight": 70,
                "last_seen": datetime.now().isoformat(),
                "keywords": ["productivity", "system", "habit", "focus", "deep work", "routine"],
                "value_type": "optimization",
                "description": "Productivity optimization"
            },
            
            # Business (fund work)
            "business_models": {
                "weight": 65,
                "last_seen": datetime.now().isoformat(),
                "keywords": ["business", "revenue", "monetize", "niche", "market", "saas"],
                "value_type": "learning",
                "description": "Business models to study"
            },
            
            # Technical (student background)
            "technical_depth": {
                "weight": 60,
                "last_seen": datetime.now().isoformat(),
                "keywords": ["backend", "architecture", "code", "system design", "engineering"],
                "value_type": "skill_building",
                "description": "Technical depth"
            }
        },
        
        "engagement_multipliers": {
            "thread": 1.15,        # Threads = more substantial
            "high_likes": 1.10,    # 1000+ likes
            "high_retweets": 1.05, # 100+ retweets
            "has_link": 1.05       # Articles/resources
        },
        
        "recency_boost": {
            "last_hour": 1.0,      # No boost for recent (they're already being sorted)
            "last_day": 1.0
        }
    }
    
    return criteria

def main():
    output_file = sys.argv[1] if len(sys.argv) > 1 else "ranking-criteria.json"
    
    criteria = generate_initial_criteria()
    
    with open(output_file, 'w') as f:
        json.dump(criteria, f, indent=2)
    
    print(f"✅ Initial ranking criteria created: {output_file}")
    print(f"   Categories: {len(criteria['value_categories'])}")
    print(f"   Decay rate: {criteria['decay_rate']} (5% per day)")

if __name__ == '__main__':
    main()
