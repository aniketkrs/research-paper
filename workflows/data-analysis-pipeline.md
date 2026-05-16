# Data Analysis Pipeline

This pipeline turns a user-supplied dataset (CSV / Excel / JSON / Parquet)
into reportable findings: a data dictionary, summary statistics, distribution
plots, correlation analysis, hypothesis tests, and a `findings.md` stub
for the writer agent to expand. Called from `workflows/research-orchestration.md
§5`.

> **Discipline:** describe the data first, *then* test hypotheses. Don't
> peek at outcome variables before declaring the analysis plan.

---

## 1. Inputs

- A dataset file (`*.csv`, `*.xlsx`, `*.json`, `*.parquet`).
- (Optional) A research question / hypothesis specification.
- (Optional) A list of variables to focus on.

---

## 2. Steps

### 2.1 Load and validate

`scripts/analyze_data.py --input <file>`:

1. Detect format from extension; load with `pandas.read_csv` /
   `read_excel` / `read_json` / `read_parquet`.
2. Print shape (`n_rows × n_cols`), dtypes, and the first few rows.
3. Flag obvious issues: all-NA columns, mixed-type columns, duplicate rows,
   columns with > 90 % missing.

### 2.2 Build the data dictionary

For each column, record:

| Field             | Notes                                            |
| ----------------- | ------------------------------------------------ |
| name              | column name                                      |
| dtype             | inferred (numeric / categorical / datetime / text) |
| n_unique          | unique values                                    |
| n_missing         | missing count and pct                             |
| min / max         | numeric                                          |
| mean / median / sd | numeric                                         |
| skew / kurtosis    | numeric                                          |
| top categories    | for categorical: top 5 with counts                |
| range             | datetime: earliest → latest                       |
| sample values     | first 5 distinct                                 |

Output: `analysis/data-dictionary.md` and `analysis/data-dictionary.csv`.

### 2.3 Missing-data analysis

- Total missingness per column.
- Missingness pattern (MCAR / MAR / MNAR — visual via missing matrix and
  Little's MCAR test).
- Recommendation per variable: drop / impute / model the missingness.

Output: `analysis/missing-data.md`, `analysis/missing-matrix.png`.

### 2.4 Univariate distributions

For each numeric column:
- Histogram + KDE.
- Summary stats (M, Mdn, SD, IQR, n).
- Skewness / kurtosis interpretation.
- Outlier flag (Tukey 1.5 × IQR rule).

For each categorical column:
- Bar chart of top categories.
- Counts + percentages table.

Output: `analysis/figures/dist_<col>.png` per column;
`analysis/univariate-summary.md`.

### 2.5 Bivariate analysis

If the user has specified an outcome variable `Y`:

- For each numeric predictor `X`:
  - Scatter plot `Y vs. X` with regression line and 95% CI.
  - Pearson's r (or Spearman if non-linear).
- For each categorical predictor `X`:
  - Box / violin of `Y` by `X`.
  - One-way ANOVA or Kruskal–Wallis.

If no outcome is specified:
- Correlation matrix among numerics → heatmap.
- Pairs of categorical → χ² with Cramér's V.

Output: `analysis/figures/bivariate_*.png`,
`analysis/bivariate-summary.md`.

### 2.6 Hypothesis testing

If hypotheses (H1, H2, …) were declared in `paper-spec.md` or by the user:

For each hypothesis:
1. Identify the relevant variables (IV / DV / mediator / moderator).
2. Pick the test from `references/statistical-methods.md §1`.
3. Check assumptions (`§2`).
4. Run the test.
5. Compute the effect size + 95% CI (`§3`).
6. Apply multiple-comparison correction if needed (`§5`).
7. Output a one-line result in the reporting template (`§7`).

Output: `analysis/hypothesis-tests.md` — one block per hypothesis with the
full reporting line, including:

> **H1:** Test = Welch's t; t(157.6) = 4.78; p < .001; Cohen's d = 0.76,
> 95 % CI [0.43, 1.08]; n = 80 per group. **Decision:** H1 supported.

### 2.7 Modeling (optional)

If the analysis plan calls for modeling:
- **Linear regression**: report `R²`, adjusted `R²`, β with SE and 95% CI,
  diagnostic plots (residuals, Q–Q, scale-location, leverage).
- **Logistic regression**: report ORs with 95% CI, Nagelkerke `R²`,
  AUROC + AUPRC, calibration plot.
- **Mixed-effects**: report fixed effects with CIs, random-effects variance,
  ICC.
- **Cox PH**: hazard ratios with CIs, Schoenfeld residuals test for PH.
- **PCA / clustering**: scree plot, silhouette score, cluster sizes,
  cluster-profile heatmap.
- **Time series**: STL decomposition, ACF / PACF, ARIMA / Prophet fit,
  forecast with prediction interval.

Output: `analysis/models/<model_name>/`.

### 2.8 Sub-group / sensitivity analyses

- Sub-group analyses on key moderators (with multiple-comparison
  correction).
- Sensitivity: run the main analysis excluding outliers, with imputation,
  with alternative model specifications.
- Bootstrap the main effect (≥ 2000 resamples) for a robust CI.

### 2.9 Generate the findings stub

`analysis/findings.md` is a Markdown stub the writer agent fills in:

```markdown
# Findings — auto-generated by analyze_data.py

## Sample
- n = <<>>
- After exclusions: n = <<>>
- Demographics: <<>>

## Descriptive statistics
[Table 1 below — see analysis/tables/descriptive.csv]

## H1: <<hypothesis statement>>
- Test: <<>>
- Statistic: <<>>
- p-value: <<>>
- Effect size: <<>>, 95% CI [<<>>, <<>>]
- Decision: supported / not supported / inconclusive

## H2: <<...>>
...

## Robustness checks
...

## Open questions / anomalies
...
```

The writer agent uses this file in §7 Drafting to write the Results section.

---

## 3. CLI

```bash
python scripts/analyze_data.py \
    --input data/study1.csv \
    --outcome y \
    --hypotheses paper-spec.md \
    --out ./analysis/ \
    --seed 42
```

Optional flags:
- `--predictors x1,x2,x3` to focus the analysis.
- `--moderator z` for moderation analysis.
- `--exclude-cols id,timestamp` to drop housekeeping columns.
- `--n-bootstrap 5000` to set bootstrap resamples.

---

## 4. Outputs

```
analysis/
├── data-dictionary.md
├── data-dictionary.csv
├── missing-data.md
├── missing-matrix.png
├── univariate-summary.md
├── bivariate-summary.md
├── hypothesis-tests.md
├── findings.md                 ← writer agent expands this
├── figures/
│   ├── dist_<col>.png
│   ├── bivariate_<x>_<y>.png
│   ├── corr-heatmap.png
│   └── ...
├── tables/
│   ├── descriptive.csv
│   ├── correlations.csv
│   ├── hypothesis-tests.csv
│   └── ...
└── models/
    └── <model>/
        ├── summary.txt
        ├── coefficients.csv
        └── diagnostics.png
```

---

## 5. Reproducibility

- The script logs every command, library version, and random seed to
  `analysis/run-log.txt`.
- A `requirements.txt` is generated capturing the exact package versions
  used.
- A summary of compute resources (cores, RAM, runtime) is appended.
- The user can re-run with `python scripts/analyze_data.py --resume
  ./analysis/` to skip already-completed steps.

---

## 6. Failure modes

| Issue                              | Behavior                                              |
| ---------------------------------- | ----------------------------------------------------- |
| Python deps missing                 | Print a clear install command; stop.                |
| Dataset unreadable                  | Print error; ask user to convert / re-export.       |
| Outcome variable not in data        | Stop; suggest closest column names.                 |
| All-categorical with numeric outcome | Auto-fall-back to ANOVA / Kruskal–Wallis.           |
| n < 30                              | Warn "small sample"; switch to non-parametric defaults. |
| Severe missingness (> 50 %)         | Warn; recommend dropping the variable or using MI.  |
| Constant column (zero variance)     | Drop with a warning.                                  |
| Duplicate rows                      | Report count; ask the user to confirm before dropping. |

The script never silently masks these — the writer agent will surface
them in `Known gaps` if not addressed.

---

## 7. Connection to the writer agent

After §2.9 emits `analysis/findings.md`, the writer agent (in §7 Drafting)
reads that file to write the **Results** section. Each `[Table N below]`
or figure reference in `findings.md` is resolved to the actual generated
artifact. This separation of "the numbers" from "the prose" keeps results
exact and prose readable.
