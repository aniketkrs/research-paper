# Statistical Methods Reference

This file is the canonical guide for choosing, applying, and reporting
statistical tests. Every statistical claim in the paper is checked against
this file by the validation pipeline (`workflows/validation-pipeline.md` →
`scripts/statistical_validation.py`).

> **Reporting standard:** every statistical statement in the paper must
> include a test name, a test statistic, degrees of freedom (where applicable),
> a p-value (with the correction method if multiple tests), an effect size
> with its 95% confidence interval, and a sample size.

---

## 1. Choosing the right test

### 1.1 Comparing means

| Question                                     | Data shape           | Default test                    | Non-parametric alternative |
| -------------------------------------------- | -------------------- | ------------------------------- | -------------------------- |
| One sample vs. known mean                     | continuous, ~normal  | One-sample t-test               | Wilcoxon signed-rank       |
| Two independent groups                        | continuous, ~normal  | Welch's t-test (default over Student's) | Mann–Whitney U     |
| Paired / repeated measures (2 timepoints)     | continuous, ~normal  | Paired t-test                   | Wilcoxon signed-rank       |
| 3+ independent groups                         | continuous, ~normal  | One-way ANOVA + Tukey HSD       | Kruskal–Wallis + Dunn      |
| 3+ paired / repeated measures                 | continuous, ~normal  | Repeated-measures ANOVA         | Friedman + Nemenyi         |
| Two factors                                   | continuous, ~normal  | Two-way ANOVA                   | ART ANOVA                  |
| Mixed within / between                        | continuous, ~normal  | Mixed ANOVA / linear mixed model | —                         |

> **Default to Welch's t-test, not Student's** — it's robust to unequal
> variances and is now the recommended default in many statistics texts.

### 1.2 Comparing proportions / counts

| Question                                  | Default test                     |
| ----------------------------------------- | -------------------------------- |
| One proportion vs. known                   | One-sample binomial test         |
| Two independent proportions                | Two-proportion z-test / Fisher's exact (small n) |
| 2x2 paired                                 | McNemar's test                   |
| RxC contingency                            | Chi-squared test (or Fisher's exact for small expected counts) |
| Odds ratio between two groups              | Logistic regression              |
| Counts (Poisson)                           | Poisson regression / negative binomial |

### 1.3 Relationships

| Question                                  | Default                          |
| ----------------------------------------- | -------------------------------- |
| Two continuous, linear                     | Pearson's r                      |
| Two continuous, monotonic but not linear   | Spearman's ρ                     |
| Two ordinal                                | Spearman's ρ or Kendall's τ      |
| Many continuous predictors → continuous Y  | Multiple linear regression       |
| Many predictors → binary Y                 | Logistic regression              |
| Many predictors → categorical Y            | Multinomial logistic regression  |
| Time-to-event                              | Cox proportional hazards         |
| Hierarchical / clustered data              | Mixed-effects models             |
| Latent constructs                          | SEM / CFA                        |

### 1.4 Causal questions

| Setting                                   | Method                           |
| ----------------------------------------- | -------------------------------- |
| Random assignment                          | RCT analysis (ITT, per-protocol) |
| Quasi-experimental, time-based              | Difference-in-differences        |
| Threshold / cutoff assignment              | Regression discontinuity         |
| Observational + good controls              | Propensity score matching / IPTW |
| Observational + instrument                 | Instrumental variables (2SLS)    |
| Causal graph + observational data          | Pearl-style do-calculus / DAGs   |

---

## 2. Assumption checks (always run them)

Before reporting a parametric test, check:

| Test                  | Required assumptions                                    | How to check                                |
| --------------------- | ------------------------------------------------------- | ------------------------------------------- |
| t-test                | normality (large n: CLT covers), independence           | Shapiro–Wilk, Q–Q plot                      |
| ANOVA                 | normality, homogeneity of variance, independence        | Levene's test, Q–Q plot                     |
| Linear regression     | linearity, normal residuals, homoscedasticity, independence, no multicollinearity | residual plots, VIF, Durbin–Watson |
| Pearson's r            | linearity, bivariate normality, no extreme outliers     | scatterplot, Q–Q                            |
| Logistic regression    | linearity in logit, independence, no multicollinearity, sufficient events per predictor (≥ 10) | Box–Tidwell, VIF |

If assumptions fail: switch to the non-parametric alternative or apply a
transformation (log, Box–Cox) and report it.

---

## 3. Effect sizes (mandatory)

Never report a p-value without an effect size.

| Test family              | Effect size                                  | Small / Medium / Large |
| ------------------------ | -------------------------------------------- | ---------------------- |
| Two-group means          | Cohen's d (or Hedges' g for small n)         | 0.2 / 0.5 / 0.8        |
| Paired means             | Cohen's d_z                                  | 0.2 / 0.5 / 0.8        |
| ANOVA                    | η² (eta-squared) or partial η²; ω² is less biased | 0.01 / 0.06 / 0.14 |
| Correlation              | Pearson's r                                  | 0.1 / 0.3 / 0.5        |
| Chi-squared 2×2          | φ (phi)                                      | 0.1 / 0.3 / 0.5        |
| Chi-squared RxC          | Cramér's V                                   | small / medium / large depend on df |
| Logistic regression      | Odds ratio (with 95% CI)                     | depends on context     |
| Linear regression        | R², adjusted R², standardized β              | 0.02 / 0.13 / 0.26 (R²) |

Always report the **95% confidence interval** of the effect size, not just
the point estimate.

---

## 4. Power analysis

Every quantitative study needs an a priori power analysis. The skill
performs / reports:

- **Target power:** 0.80 (or 0.90 for high-stakes / high-cost studies)
- **α:** 0.05 (or 0.01 / 0.001 for high-stakes)
- **Expected effect size:** justified by prior literature or a meta-analytic
  estimate. **Never assume "medium"** without justification.
- **Required N:** computed via `pwr` / `statsmodels` / G*Power.

Report:
> "An a priori power analysis (G*Power 3.1) indicated that detecting a
> medium effect (Cohen's d = 0.5) with α = 0.05 and power = 0.80 in a
> two-sample t-test required n = 64 per group."

---

## 5. Multiple comparison corrections

When running > 1 test on the same family:

| Approach              | When to use                                  |
| --------------------- | -------------------------------------------- |
| **Bonferroni**        | Few tests (≤ 5), strict family-wise control  |
| **Holm–Bonferroni**   | Default replacement for Bonferroni, more powerful |
| **Tukey HSD**         | Post-hoc after ANOVA, all pairwise comparisons |
| **Dunnett**           | Comparing each group to one control          |
| **Benjamini–Hochberg (FDR)** | Many tests (e.g., genomics, NLP benchmarks) — controls false discovery rate |

Report the correction method explicitly. **Adjusted p-values** are reported,
not raw ones.

---

## 6. Bayesian alternatives

When the user asks for Bayesian analysis or when prior information matters:

- **Bayes factors** (BF₁₀): evidence for H₁ vs. H₀.
  - BF₁₀ < 1: evidence for H₀
  - 1–3: anecdotal for H₁
  - 3–10: moderate
  - 10–30: strong
  - 30–100: very strong
  - > 100: extreme
- **Posterior distributions** with 95% **credible intervals** (not confidence
  intervals — they are different).
- **Prior justification** is mandatory: weakly informative by default; cite
  the source of any informative prior.
- Tools: PyMC, Stan, JASP.

---

## 7. Reporting templates

### 7.1 Welch's t-test
> "Group A (M = 12.4, SD = 3.1, n = 80) scored higher than Group B
> (M = 10.1, SD = 2.9, n = 80) on the benchmark. The difference was
> statistically significant, t(157.6) = 4.78, p < .001, Cohen's d = 0.76,
> 95% CI [0.43, 1.08]."

### 7.2 One-way ANOVA + post-hoc
> "A one-way ANOVA revealed a significant effect of model size on accuracy,
> F(3, 156) = 14.21, p < .001, η² = 0.21, 95% CI [0.10, 0.30]. Tukey HSD
> showed that the 70 B model significantly outperformed the 7 B
> (Δ = 5.2 pp, p < .001) and 13 B (Δ = 3.8 pp, p = .003) models, but did
> not differ from the 33 B model (Δ = 0.9 pp, p = .42)."

### 7.3 Multiple regression
> "A multiple regression model predicting code-quality score from team size,
> commit frequency, and test coverage was significant, F(3, 96) = 21.4,
> p < .001, R² = .40, adjusted R² = .39. Test coverage was the strongest
> predictor (β = 0.52, t = 6.1, p < .001), followed by commit frequency
> (β = 0.21, t = 2.4, p = .018). Team size was not a significant predictor
> (β = 0.08, t = 0.9, p = .37)."

### 7.4 Chi-squared
> "A 3×2 chi-squared test of independence showed an association between
> framework choice and project success rate, χ²(2, N = 240) = 12.6,
> p = .002, Cramér's V = 0.23 (small-to-medium effect)."

### 7.5 Logistic regression
> "Test coverage independently predicted release-without-rollback, OR = 1.04
> per percentage point, 95% CI [1.02, 1.07], p < .001, controlling for team
> size and code-review intensity (Nagelkerke R² = .31)."

### 7.6 Correlation
> "Repository age correlated negatively with bug density, r(58) = −.34,
> 95% CI [−.55, −.10], p = .008."

### 7.7 Non-parametric (Mann–Whitney U)
> "Group A produced more accepted PRs (Mdn = 14, IQR = 8–22, n = 50) than
> Group B (Mdn = 9, IQR = 5–13, n = 50), Mann–Whitney U = 1842,
> Z = 3.21, p = .001, rank-biserial r = 0.47, 95% CI [0.20, 0.69]."

---

## 8. Common statistical errors the skill must catch

- Reporting only `p < .05` (need exact p, test stat, df, effect, CI, n).
- Dichotomizing continuous variables ("median split") — almost always wrong.
- Using Pearson's r when the relationship is clearly non-linear.
- Treating **non-significant** as **proves the null** — re-frame as
  "we did not detect an effect"; consider equivalence testing (TOST).
- Double-dipping (tuning hyperparameters on the test set).
- Reporting accuracy on imbalanced classes (use precision / recall / F1 /
  AUROC / AUPRC).
- Forgetting to correct for multiple comparisons in benchmark tables.
- Reporting standard error as if it were standard deviation (or vice versa).
- Using SD of a single training run (use multiple seeds for ML papers).
- Comparing means with overlapping confidence intervals as if that proves
  equality (it doesn't).

---

## 9. ML-specific reporting (since this is common)

For benchmark / model papers:

- Report **mean ± SD over ≥ 3 random seeds** (5 is better).
- Use a **paired statistical test** when comparing models on the same
  examples (e.g., paired bootstrap, McNemar for binary classification,
  Wilcoxon signed-rank for ranking metrics).
- Show **per-task** results, not just averages.
- Include **calibration** (ECE) when the model produces probabilities.
- Report **inference cost** (latency, FLOPs, memory) alongside accuracy.
- Report **dataset details**: size, splits, contamination check vs. training.
- Report **failure modes** with examples (qualitative section).
- For LLMs: report **prompt template**, **decoding parameters**, and
  **n-shot count** verbatim.

---

## 10. Sample size sanity floors

Below these numbers, results are exploratory at best:

| Test                          | Minimum n        |
| ----------------------------- | ---------------- |
| Two-group t-test, d = 0.5      | 64 / group       |
| One-way ANOVA, k = 3, f = 0.25 | 159 total        |
| Pearson's r for r = 0.3        | 84               |
| Multiple regression, k = 3      | 10–20 per predictor (50+ for stable β) |
| SEM                            | 200 typical, 100 minimum |
| Logistic regression             | 10 events per predictor |
| Chi-squared                    | All expected counts ≥ 5  |

If the actual n is below the floor, the validation pipeline flags
"underpowered".

---

## 11. Reporting confidence intervals

- Always report the **95% CI** alongside any point estimate.
- CIs are **more informative than p-values** — show them in tables and
  forest plots.
- For bootstrapped CIs: report **bootstrap method** (percentile, BCa) and
  **number of resamples** (≥ 1000 for percentile, ≥ 10,000 for BCa tails).

---

## 12. Visual statistics

The visualization pipeline auto-generates these when statistics are present:

| Statistic                        | Default visualization                  |
| -------------------------------- | -------------------------------------- |
| Group means + CIs                 | Bar chart with error bars (CIs, not SE) |
| Distribution comparison           | Violin plot + overlaid box             |
| Correlation matrix                | Heatmap                                |
| Regression fit                    | Scatter + fit line + 95% CI band       |
| Survival                          | Kaplan–Meier curves                    |
| Meta-analysis                     | Forest plot                            |
| Multiple-test results              | Volcano plot or BH-adjusted bar plot   |
| Power curves                      | Line plot of power vs. effect size / n |

See `references/visualization-guide.md` for the full chart-selection logic.
