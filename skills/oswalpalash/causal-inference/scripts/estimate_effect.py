#!/usr/bin/env python3
"""
Estimate treatment effects from the causal action log.

Usage:
    python estimate_effect.py --treatment send_time --outcome reply_received \
        --values morning,evening --log-path memory/causal/action_log.jsonl
"""

import argparse
import json
from collections import defaultdict
from pathlib import Path
import math

DEFAULT_LOG_PATH = "memory/causal/action_log.jsonl"


def load_actions(log_path: str):
    """Load all actions from the log file."""
    path = Path(log_path)
    if not path.exists():
        return []
    
    actions = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                actions.append(json.loads(line))
    return actions


def extract_variable(action: dict, var_name: str):
    """Extract a variable from action, context, pre_state, or post_state."""
    if var_name in action:
        return action[var_name]
    for section in ["context", "pre_state", "post_state"]:
        if section in action and var_name in action[section]:
            return action[section][var_name]
    return None


def estimate_ate(actions: list, treatment_var: str, outcome_var: str, values: list):
    """Estimate average treatment effect between two treatment values."""
    if len(values) != 2:
        raise ValueError("Need exactly 2 treatment values for ATE estimation")
    
    groups = defaultdict(list)
    
    for action in actions:
        treatment = extract_variable(action, treatment_var)
        outcome = extract_variable(action, outcome_var)
        
        if treatment is None or outcome is None:
            continue
        
        # Convert outcome to numeric if boolean
        if isinstance(outcome, bool):
            outcome = 1.0 if outcome else 0.0
        elif isinstance(outcome, str):
            outcome = 1.0 if outcome.lower() in ("true", "yes", "1", "positive") else 0.0
        
        if str(treatment) in values:
            groups[str(treatment)].append(float(outcome))
    
    # Calculate means and standard errors
    results = {}
    for value in values:
        outcomes = groups[value]
        if outcomes:
            n = len(outcomes)
            mean = sum(outcomes) / n
            variance = sum((x - mean) ** 2 for x in outcomes) / n if n > 1 else 0
            se = math.sqrt(variance / n) if n > 0 else 0
            results[value] = {"mean": mean, "n": n, "se": se}
        else:
            results[value] = {"mean": None, "n": 0, "se": None}
    
    # Calculate ATE
    if results[values[0]]["mean"] is not None and results[values[1]]["mean"] is not None:
        ate = results[values[0]]["mean"] - results[values[1]]["mean"]
        # Pooled SE for ATE
        se1, se0 = results[values[0]]["se"], results[values[1]]["se"]
        ate_se = math.sqrt(se1**2 + se0**2) if se1 and se0 else None
    else:
        ate = None
        ate_se = None
    
    return {
        "treatment_var": treatment_var,
        "outcome_var": outcome_var,
        "groups": results,
        "ate": ate,
        "ate_se": ate_se,
        "interpretation": interpret_ate(ate, ate_se, values),
    }


def interpret_ate(ate, se, values):
    """Generate human-readable interpretation."""
    if ate is None:
        return "Insufficient data to estimate effect."
    
    if se is None or se == 0:
        return f"Effect of {values[0]} vs {values[1]}: {ate:.3f} (uncertainty unknown)"
    
    ci_lower = ate - 1.96 * se
    ci_upper = ate + 1.96 * se
    
    if ci_lower > 0:
        return f"Positive effect of {values[0]} vs {values[1]}: {ate:.3f} (95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]) — confident"
    elif ci_upper < 0:
        return f"Negative effect of {values[0]} vs {values[1]}: {ate:.3f} (95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]) — confident"
    else:
        return f"Uncertain effect of {values[0]} vs {values[1]}: {ate:.3f} (95% CI: [{ci_lower:.3f}, {ci_upper:.3f}]) — need more data"


def main():
    parser = argparse.ArgumentParser(description="Estimate treatment effects")
    parser.add_argument("--treatment", "-t", required=True, help="Treatment variable name")
    parser.add_argument("--outcome", "-o", required=True, help="Outcome variable name")
    parser.add_argument("--values", "-v", required=True, help="Treatment values to compare (comma-separated)")
    parser.add_argument("--log-path", "-l", default=DEFAULT_LOG_PATH, help="Action log path")
    
    args = parser.parse_args()
    values = [v.strip() for v in args.values.split(",")]
    
    actions = load_actions(args.log_path)
    if not actions:
        print("No actions found in log.")
        return
    
    result = estimate_ate(actions, args.treatment, args.outcome, values)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
