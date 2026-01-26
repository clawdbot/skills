# Treatment Effect Estimation

Practical methods for estimating causal effects from observational data.

## Average Treatment Effect (ATE)

```
ATE = E[Y(1)] - E[Y(0)]
    = E[Y | do(T=1)] - E[Y | do(T=0)]
```

Where T is treatment (e.g., send_time=morning vs evening).

## Method 1: Difference in Means (Randomized)

If you can randomize (e.g., A/B test email timing):

```python
ate = mean(Y[T==1]) - mean(Y[T==0])
se = sqrt(var(Y[T==1])/n1 + var(Y[T==0])/n0)
```

**Use when:** You control the intervention and can randomize.

## Method 2: Regression Adjustment

Control for confounders via linear regression:

```python
# Y = β0 + β1*T + β2*X1 + β3*X2 + ε
# β1 is the treatment effect, adjusted for confounders X1, X2

import statsmodels.api as sm
model = sm.OLS(Y, sm.add_constant(df[['treatment', 'confounder1', 'confounder2']]))
results = model.fit()
ate = results.params['treatment']
se = results.bse['treatment']
```

**Use when:** Linear relationships, known confounders.

## Method 3: Propensity Score Matching

Match treated/control units with similar propensity scores:

```python
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import NearestNeighbors

# 1. Estimate propensity scores
ps_model = LogisticRegression().fit(X_confounders, T)
propensity = ps_model.predict_proba(X_confounders)[:, 1]

# 2. Match on propensity
treated_idx = np.where(T == 1)[0]
control_idx = np.where(T == 0)[0]

nn = NearestNeighbors(n_neighbors=1)
nn.fit(propensity[control_idx].reshape(-1, 1))
matches = nn.kneighbors(propensity[treated_idx].reshape(-1, 1))[1]

# 3. Estimate ATE from matched pairs
matched_control_idx = control_idx[matches.flatten()]
ate = mean(Y[treated_idx]) - mean(Y[matched_control_idx])
```

**Use when:** Many confounders, non-linear relationships.

## Method 4: Inverse Propensity Weighting (IPW)

Weight observations by inverse propensity:

```python
# Treated: weight = 1/P(T=1|X)
# Control: weight = 1/P(T=0|X) = 1/(1-P(T=1|X))

weights_treated = 1 / propensity[T == 1]
weights_control = 1 / (1 - propensity[T == 0])

ate = (
    np.average(Y[T == 1], weights=weights_treated) -
    np.average(Y[T == 0], weights=weights_control)
)
```

**Use when:** Want population-level estimates, can model propensity well.

## Method 5: Doubly Robust Estimation

Combines regression and IPW — consistent if either model is correct:

```python
from econml.dr import DRLearner

dr = DRLearner()
dr.fit(Y, T, X_confounders)
ate = dr.ate(X_confounders)
```

**Use when:** Uncertain about model specification, want robustness.

## Confidence Intervals

Always report uncertainty:

```python
# 95% CI
ci_lower = ate - 1.96 * se
ci_upper = ate + 1.96 * se

# For decision-making, use conservative bound
if ci_lower > 0:
    print("Confident positive effect")
elif ci_upper < 0:
    print("Confident negative effect")
else:
    print("Effect uncertain — may need more data or user confirmation")
```

## Practical Guidelines for Clawdbot

1. **Start with regression** — simple, interpretable, usually sufficient
2. **Log everything** — you need outcome data to estimate effects
3. **Wait for sufficient n** — at least 30-50 observations per treatment level
4. **Check overlap** — propensity methods fail if treatment groups don't overlap
5. **Validate with holdout** — reserve recent data for prediction validation

## Quick Decision Matrix

| Situation | Method |
|-----------|--------|
| Can randomize | Difference in means |
| Few confounders, linear | Regression |
| Many confounders | Propensity matching/IPW |
| Uncertain about model | Doubly robust |
| Time series | Interrupted time series / diff-in-diff |
