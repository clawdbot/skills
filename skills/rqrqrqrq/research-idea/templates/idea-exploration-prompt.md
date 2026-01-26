# Idea Exploration Template

Use this template when researching a new idea.

---

## Prompt

```
I have an idea I'd like you to explore in depth:

**Idea:** {IDEA_DESCRIPTION}

Please research and analyze this idea comprehensively. Use web_search to find real market data, competitors, and validation.

## Research Framework

### 1. Core Concept Analysis
   - Break down the core problem/opportunity
   - Key assumptions and hypothesis
   - What makes this interesting/unique?
   - First-principles thinking: Why now? Why hasn't this been done?

### 2. Market Research
   - Who would use this? (specific personas)
   - What's the market size/opportunity? (TAM/SAM/SOM with sources)
   - Existing solutions and competitors (be thorough—use web_search)
   - Market gaps this could fill
   - Trends that support or challenge this idea

### 3. Technical Implementation
   - Possible technical approaches (compare 2-3 options)
   - Key technical challenges and how to overcome them
   - Required resources/skills
   - MVP scope and complexity (what's the absolute minimum?)
   - Estimated timeline for MVP

### 4. Business Model
   - Revenue model options (which is best and why?)
   - Pricing strategy (with comparable benchmarks)
   - Unit economics (rough estimates)
   - Key business assumptions to validate

### 5. Use Cases & Value Proposition
   - Primary use cases (3-5 specific examples)
   - User personas (detailed: pain points, motivations, objections)
   - User journey/flow
   - Value proposition for each persona (quantify if possible)

### 6. Go-to-Market Strategy
   - Target customer segment (start narrow!)
   - Distribution channels (rank by feasibility)
   - Early adopter acquisition strategy
   - Pricing for launch vs. scale
   - Launch timeline and milestones

### 7. Risks & Challenges
   - Technical risks (what could kill this technically?)
   - Market risks (what if customers don't care?)
   - Competitive risks (who might crush this?)
   - Execution risks (what's hard about building/launching?)
   - Regulatory/legal risks

### 8. Validation Plan
   - What would prove this idea is worth pursuing?
   - What would disprove it?
   - Experiments to run (cheapest/fastest first)
   - Success metrics for each experiment

### 9. Verdict & Recommendations

Provide a clear verdict:

- 🟢 **STRONG YES** - Clear opportunity, pursue aggressively
  - Why this is a strong opportunity
  - First 3 actions to take
  - Timeline to first revenue
  
- 🟡 **CONDITIONAL YES** - Promising but needs validation
  - What needs to be validated first
  - How to validate it (specific experiments)
  - Decision criteria (when to go/no-go)
  
- 🟠 **PIVOT RECOMMENDED** - Core insight good, execution needs work
  - What's right about the insight
  - What needs to change
  - Alternative angles to explore
  
- 🔴 **PASS** - Too many red flags
  - Main reasons to pass
  - What would need to change to reconsider
  - Alternative ideas in similar space

### 10. Next Steps

If pursuing:
- **This week**: [immediate action]
- **This month**: [validation experiments]
- **This quarter**: [MVP goal]

If not pursuing:
- **Lessons learned**: [key insights for future ideas]
- **Related opportunities**: [adjacent ideas worth exploring]

---

## Instructions

1. **Research thoroughly**: Use web_search for competitors, market size, pricing benchmarks, etc.
2. **Be critical**: Don't just find reasons to pursue—find reasons NOT to pursue
3. **Be specific**: "Large market" → "X million potential users spending $Y annually"
4. **Save your work**: Write comprehensive markdown to `~/clawd/ideas/{IDEA_SLUG}/research.md`
5. **When complete**: Your findings will automatically return to the main session

**Save format:**
- Create directory: `~/clawd/ideas/{IDEA_SLUG}/`
- Write file: `~/clawd/ideas/{IDEA_SLUG}/research.md`
- Include metadata header: date, idea, verdict

Be thorough but practical. Focus on actionable insights.
```

---

## Variables to Replace

- `{IDEA_DESCRIPTION}`: The actual idea text
- `{IDEA_SLUG}`: URL-friendly version (e.g., "ai-powered-calendar" from "AI-Powered Calendar Assistant")
