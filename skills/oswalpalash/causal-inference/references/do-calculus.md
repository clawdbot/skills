# Do-Calculus Reference

Pearl's do-calculus distinguishes **seeing** from **doing**.

## Core Distinction

- `P(Y | X=x)` — probability of Y given we **observed** X=x
- `P(Y | do(X=x))` — probability of Y if we **intervene** to set X=x

These differ when confounders exist.

## Example: Email Timing

**Observation:** People who send emails at 6am get more replies.  
**Confounder:** Early senders are also more organized/persistent.

`P(reply | observed_send_time=6am)` ≠ `P(reply | do(send_time=6am))`

The intervention effect may be smaller (or zero) once you account for the confounder.

## Three Rules of Do-Calculus

Given causal graph G:

1. **Insertion/deletion of observations:**  
   `P(Y | do(X), Z, W) = P(Y | do(X), W)` if Z is d-separated from Y given X, W in G_X̄

2. **Action/observation exchange:**  
   `P(Y | do(X), do(Z), W) = P(Y | do(X), Z, W)` if Z is d-separated from Y given X, W in G_X̄Z̲

3. **Insertion/deletion of actions:**  
   `P(Y | do(X), do(Z), W) = P(Y | do(X), W)` if Z is d-separated from Y given X, W in G_X̄Z̄(W)

## Practical Application

For most Clawdbot use cases, full do-calculus isn't needed. Use:

1. **Randomization** — if you can randomize the intervention, `P(Y | do(X)) = P(Y | X)` in the experiment
2. **Backdoor adjustment** — control for confounders: `P(Y | do(X)) = Σ_z P(Y | X, Z=z) P(Z=z)`
3. **Instrumental variables** — when direct adjustment isn't possible

## When to Escalate

Use full do-calculus when:
- Multiple confounders with complex relationships
- Need to prove identifiability
- High-stakes decisions requiring formal guarantees

For email timing and scheduling, backdoor adjustment usually suffices.

## Resources

- Pearl, J. (2009). *Causality: Models, Reasoning, and Inference*
- [Introduction to Causal Inference](https://www.bradyneal.com/causal-inference-course) — free online course
