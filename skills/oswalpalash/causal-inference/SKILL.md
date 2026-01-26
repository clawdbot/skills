---
name: causal-inference
description: Add causal reasoning to agent actions. Use when planning interventions (email timing, scheduling, follow-ups), debugging why workflows failed, predicting action outcomes, or when the agent needs to answer "what happens if I do X?" with real predictions instead of correlations. Enables intervention-grade planning, counterfactual debugging, and principled safety checks.
---

# Causal Inference

A lightweight causal layer for predicting action outcomes, not by pattern-matching correlations, but by modeling interventions and counterfactuals.

## Core Invariant

**Every action must be representable as an explicit intervention on a causal model, with predicted effects + uncertainty + a falsifiable audit trail.**

Plans must be *causally valid*, not just plausible.

## When to Use

1. **Intervention planning** — "If I reschedule meeting A, will it cascade?" / "If I send follow-ups at 9am vs 6pm, which gets more replies?"
2. **Counterfactual debugging** — "Why did this workflow fail?" → "Which causal link broke?" → "What minimal intervention would fix it?"
3. **Distribution-shift robustness** — When APIs/tools change, causal models generalize better than correlational predictors
4. **Safety decisions** — Quantify expected harm before acting; refuse when uncertainty is high

## Architecture

### A. Action Log (required)

Every executed action emits a structured event:

```json
{
  "action": "send_followup",
  "context": {"recipient_type": "warm_lead", "prior_touches": 2},
  "time": "2025-01-26T10:00:00Z",
  "pre_state": {"days_since_last_contact": 7},
  "post_state": {"reply_received": true, "reply_delay_hours": 4},
  "outcome": "positive_reply"
}
```

Store in `memory/causal/action_log.jsonl`.

### B. Causal Graphs (per domain)

Start with 10-30 observable variables per domain.

**Email domain example:**
```
send_time → reply_prob
subject_style → open_rate
recipient_type → reply_prob
followup_count → reply_prob (diminishing)
time_since_last → reply_prob
```

**Calendar domain example:**
```
meeting_time → attendance_rate
attendee_count → slip_risk
conflict_degree → reschedule_prob
buffer_time → focus_quality
```

Store graph definitions in `memory/causal/graphs/`.

### C. Estimation

For each "knob" (intervention variable), estimate treatment effects:

```python
# Pseudo: effect of morning vs evening sends
effect = mean(reply_prob | send_time=morning) - mean(reply_prob | send_time=evening)
uncertainty = std_error(effect)
```

Use simple regression or propensity matching first. Graduate to do-calculus when graphs are explicit and identification is needed.

### D. Decision Policy

Before executing actions:

1. Identify intervention variable(s)
2. Query causal model for expected outcome distribution
3. Compute expected utility + uncertainty bounds
4. If uncertainty > threshold OR expected harm > threshold → refuse or escalate to user
5. Log prediction for later validation

## Workflow

### Planning an Action

```
1. User request → identify candidate actions
2. For each action:
   a. Map to intervention(s) on causal graph
   b. Predict P(outcome | do(action))
   c. Estimate uncertainty
   d. Compute expected utility
3. Rank by expected utility, filter by safety
4. Execute best action, log prediction
5. Observe outcome, update model
```

### Debugging a Failure

```
1. Identify failed outcome
2. Trace back through causal graph
3. For each upstream node:
   a. Was the value as expected?
   b. Did the causal link hold?
4. Identify broken link(s)
5. Compute minimal intervention set that would have prevented failure
6. Log counterfactual for learning
```

## Quick Start: Email Follow-ups

The simplest domain to instrument. Variables to track:

| Variable | Type | Source |
|----------|------|--------|
| send_time | categorical (morning/afternoon/evening) | action |
| day_of_week | categorical | action |
| recipient_type | categorical (cold/warm/hot) | context |
| subject_has_question | boolean | action |
| prior_thread_length | int | context |
| reply_received | boolean | outcome |
| reply_delay_hours | float | outcome |

After ~50-100 logged actions, estimate:
- Effect of send_time on reply_prob
- Effect of subject_has_question on reply_prob
- Interaction: recipient_type × send_time

Use estimates to recommend optimal follow-up timing.

## Safety Constraints

Define "protected variables" that require explicit user approval:

```yaml
protected:
  - delete_email
  - cancel_meeting
  - send_to_new_contact
  - financial_transaction

thresholds:
  max_uncertainty: 0.3  # don't act if P(outcome) uncertainty > 30%
  min_expected_utility: 0.1  # don't act if expected gain < 10%
```

## Files

- `memory/causal/action_log.jsonl` — all logged actions with outcomes
- `memory/causal/graphs/` — domain-specific causal graph definitions
- `memory/causal/estimates/` — learned treatment effects
- `memory/causal/config.yaml` — safety thresholds and protected variables

## References

- See `references/do-calculus.md` for formal intervention semantics
- See `references/estimation.md` for treatment effect estimation methods
