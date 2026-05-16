# Statistical Tests Reference

## Purpose
Guide selection and reporting of appropriate statistical tests for research papers.

---

## Test Selection Quick Reference

### Comparing Groups

| Scenario | Parametric Test | Non-parametric Alternative |
|----------|----------------|---------------------------|
| 2 independent groups, continuous DV | Independent t-test | Mann-Whitney U |
| 2 related groups, continuous DV | Paired t-test | Wilcoxon signed-rank |
| 3+ independent groups, continuous DV | One-way ANOVA | Kruskal-Wallis |
| 3+ related groups, continuous DV | Repeated measures ANOVA | Friedman |
| 2+ groups, 2+ DVs | MANOVA | — |
| 2+ IVs, continuous DV | Factorial ANOVA | — |
| Covariate to control | ANCOVA | — |

### Relationships and Predictions

| Scenario | Test |
|----------|------|
| 2 continuous variables, linear | Pearson's r |
| 2 continuous variables, non-linear/ordinal | Spearman's rho |
| 2 ordinal variables | Kendall's tau |
| Predict continuous DV from 1 IV | Simple linear regression |
| Predict continuous DV from multiple IVs | Multiple regression |
| Predict binary DV | Logistic regression |
| Predict ordinal DV | Ordinal regression |
| Predict count DV | Poisson regression |
| Time-to-event | Cox proportional hazards |
| Mediation | Baron & Kenny / bootstrapping |
| Moderation | Interaction terms in regression |

### Categorical Data

| Scenario | Test |
|----------|------|
| 2 categorical variables, expected counts ≥ 5 | Chi-square test of independence |
| 2 categorical variables, expected counts < 5 | Fisher's exact test |
| Goodness of fit (observed vs. expected) | Chi-square goodness of fit |
| Paired categorical data | McNemar's test |
| 2×2 table, effect size | Odds ratio / relative risk |

---

## Assumptions and How to Test Them

### Normality
**Tests:**
- Shapiro-Wilk (preferred for N < 50)
- Kolmogorov-Smirnov (larger samples)
- Q-Q plot (visual inspection)
- Skewness and kurtosis (|value| < 2 generally acceptable)

**If violated:**
- Use non-parametric alternative
- Transform data (log, square root, reciprocal)
- If N > 30, invoke Central Limit Theorem (for means)
- Use bootstrapping

### Homogeneity of Variance
**Tests:**
- Levene's test (robust to non-normality)
- Bartlett's test (requires normality)

**If violated:**
- Welch's t-test (instead of Student's t)
- Welch's ANOVA
- Games-Howell post-hoc (instead of Tukey)
- Report both if results differ

### Independence
**Assessment:**
- Study design evaluation (are observations independent?)
- Durbin-Watson test (for autocorrelation in regression residuals)

**If violated:**
- Mixed/multilevel models (for nested data)
- Repeated measures designs
- Time series approaches (for temporal dependence)

### Linearity
**Assessment:**
- Scatter plot of residuals vs. predicted values
- Component-plus-residual plots
- Polynomial terms significance

**If violated:**
- Polynomial regression
- Non-linear transformation
- Non-parametric regression (LOESS)

### Multicollinearity (for regression)
**Assessment:**
- Variance Inflation Factor (VIF > 10 problematic)
- Tolerance (< 0.1 problematic)
- Correlation matrix between predictors

**If violated:**
- Remove redundant predictors
- Combine correlated predictors (PCA/factor analysis)
- Ridge regression / regularization

---

## Effect Size Measures

### For Group Differences
| Test | Effect Size | Small | Medium | Large |
|------|------------|-------|--------|-------|
| t-test | Cohen's d | 0.2 | 0.5 | 0.8 |
| ANOVA | η² (eta-squared) | 0.01 | 0.06 | 0.14 |
| ANOVA | ω² (omega-squared) | 0.01 | 0.06 | 0.14 |
| ANOVA | partial η² | 0.01 | 0.06 | 0.14 |

### For Relationships
| Test | Effect Size | Small | Medium | Large |
|------|------------|-------|--------|-------|
| Correlation | r | 0.1 | 0.3 | 0.5 |
| Regression | R² | 0.02 | 0.13 | 0.26 |
| Chi-square | Cramér's V | 0.1 | 0.3 | 0.5 |
| Chi-square | Phi (φ) | 0.1 | 0.3 | 0.5 |
| Odds ratio | OR | 1.5 | 2.5 | 4.3 |

---

## Reporting Templates

### t-test
```
An independent samples t-test revealed a [significant/non-significant] 
difference in [DV] between [group 1] (M = X.XX, SD = X.XX) and [group 2] 
(M = X.XX, SD = X.XX), t(df) = X.XX, p = .XXX, d = X.XX, 95% CI [X.XX, X.XX].
```

### ANOVA
```
A one-way ANOVA indicated a [significant/non-significant] effect of [IV] on 
[DV], F(df_between, df_within) = X.XX, p = .XXX, η² = .XX. Post-hoc comparisons 
using [Tukey's HSD/Bonferroni/Games-Howell] revealed that [group comparison results].
```

### Chi-square
```
A chi-square test of independence revealed a [significant/non-significant] 
association between [variable 1] and [variable 2], χ²(df) = X.XX, p = .XXX, 
V = .XX.
```

### Correlation
```
[Pearson's/Spearman's] correlation analysis revealed a [significant/non-significant] 
[positive/negative] [strong/moderate/weak] correlation between [var 1] and [var 2], 
r(N-2) = .XX, p = .XXX.
```

### Regression
```
A [multiple linear/logistic] regression was conducted to predict [DV] from 
[IVs]. The model explained X.X% of variance in [DV], F(df1, df2) = X.XX, 
p = .XXX, R² = .XX, adjusted R² = .XX. [IV name] significantly predicted 
[DV] (β = X.XX, p = .XXX), indicating that [interpretation].
```

### Mann-Whitney U
```
A Mann-Whitney U test indicated that [DV] was [significantly/not significantly] 
[higher/lower] for [group 1] (Mdn = X.XX) than for [group 2] (Mdn = X.XX), 
U = XXXX, p = .XXX, r = .XX.
```

---

## Common Mistakes to Avoid

1. **Reporting p = .000** → Always report as p < .001
2. **Only reporting significance** → Always include effect size
3. **Dichotomizing p at .05** → Report exact p-value, discuss effect size
4. **Multiple comparisons without correction** → Apply Bonferroni, Holm, or FDR
5. **Using parametric tests on clearly non-normal data** → Check and report assumptions
6. **Ignoring effect size** → A significant p with tiny effect is not meaningful
7. **Confusing statistical and practical significance** → Discuss both
8. **Not reporting confidence intervals** → Always provide CI for key estimates
9. **Misinterpreting non-significance as "no effect"** → It means "insufficient evidence"
10. **Using correlation to imply causation** → Explicitly state this limitation
