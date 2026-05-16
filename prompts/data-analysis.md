# Prompt: Data Analysis

Used in `workflows/research-orchestration.md §5 Data analysis`.

---

## Step 1 — Inspect before analyzing

```
You are a data analyst. Before any inferential test, build a complete
picture of the data:

1. Load the dataset. Print shape, dtypes, and head().
2. Compute a data dictionary (every column: dtype, n_missing, n_unique,
   summary statistics).
3. Plot the distribution of every numeric variable (histogram + KDE).
4. Plot the top categories of every categorical variable (bar chart).
5. Compute a missingness matrix and report patterns (MCAR / MAR / MNAR).
6. Flag obvious data-quality issues:
   - Constant columns
   - All-missing columns
   - Duplicate rows
   - Severe outliers
   - Mixed-type columns
   - Date columns disguised as strings

If any major issue is found, report it BEFORE proceeding. The user may
want to re-export the data.

Output: analysis/data-dictionary.md, analysis/univariate-summary.md,
        analysis/missing-data.md.
```

---

## Step 2 — Pre-specified analysis plan

```
If the paper has hypotheses, write a pre-analysis plan BEFORE running
inferential tests. The plan answers:

- Which variables are IV / DV / mediators / moderators / controls?
- For each hypothesis: what test? what assumptions? what effect size?
- What multiple-comparison correction will be used?
- What sub-group / sensitivity analyses?

Save as analysis/analysis-plan.md.

If you cannot pre-register (e.g., the data has already been seen), at
least DOCUMENT the order of decisions. This is the single best safeguard
against p-hacking.
```

---

## Step 3 — Run the planned analyses

```
For each hypothesis in analysis-plan.md:

1. Subset the data to the relevant variables.
2. Check assumptions (normality, homoscedasticity, independence,
   multicollinearity). Use:
   - Shapiro-Wilk + Q-Q plot for normality
   - Levene's test for homogeneity
   - VIF for multicollinearity
   - Durbin-Watson for autocorrelation
3. If assumptions fail: try a transformation (log, sqrt, Box-Cox), then
   the non-parametric alternative. Document what you tried.
4. Run the test.
5. Compute the effect size and its 95% confidence interval.
6. Apply multiple-comparison correction if running > 1 test on the
   same family.
7. Generate the figure(s) for this hypothesis (see prompts/visualization-planning.md).
8. Write the result in the reporting template
   (references/statistical-methods.md §7).
```

---

## Step 4 — Robustness checks

```
For each main result, run at least 2 robustness checks:

- Re-run excluding outliers (Tukey 1.5*IQR rule).
- Re-run with imputed missing data (MICE for MAR, sensitivity for MNAR).
- Re-run with an alternative model specification (e.g., add / remove a
  control; switch link function).
- Bootstrap the main effect (n_boot >= 2000) for a robust CI.
- For ML: vary random seeds (>= 5) and report mean +/- SD.

Document every robustness check, even when it doesn't change the
conclusion. Especially document any that DO change the conclusion — that's
the most important finding.
```

---

## Step 5 — Honest reporting of nulls

```
If a planned test returns a null result:

- Report it. NEVER hide it.
- Reframe: not "X has no effect" but "we did not detect an effect of X".
- Compute the effect size + CI and report. A near-zero estimate with a
  narrow CI is informative.
- Consider equivalence testing (TOST) to argue for a meaningful null.
- Compute post-hoc power: if power was < 0.80, the null may reflect an
  underpowered design rather than a true absence of effect.
```

---

## Step 6 — Write the findings stub

```
Write analysis/findings.md as a SECTION-LEVEL STUB the writer agent
will expand:

# Findings

## Sample
- n = ...
- After exclusions: n = ...
- Demographics: ...

## Descriptive statistics
[Table 1: descriptive.csv]

## H1: <hypothesis>
- Statistical test: ...
- Test statistic: ..., df = ..., p = ...
- Effect size: ..., 95% CI [..., ...]
- Decision: supported / not supported / inconclusive
- Interpretation: ...
- Robustness: ...

## H2: <hypothesis>
...

## Exploratory analyses
(Clearly labeled as exploratory.)

## Anomalies / surprises
(Findings that didn't match expectations.)
```

This file is the bridge between the analysis (numbers) and the prose
(Results section). The writer agent expands it during §7 Drafting; the
analyst's job is to make sure every NUMBER in this file is correct.
