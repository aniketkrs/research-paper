# Data Analysis Workflow

## Purpose
Transform raw data into research-grade findings with statistical validation, appropriate visualizations, and academically rigorous interpretation.

---

## Phase 1: Data Ingestion

```
ACCEPT data formats:
- CSV files → parse with Python/pandas logic
- JSON files → flatten nested structures
- Excel files → identify relevant sheets/ranges
- Inline data → structure into tables
- Described data → work with summary statistics

INITIAL assessment:
- Number of observations (rows)
- Number of variables (columns)
- Data types (numeric, categorical, temporal, text)
- Missing data patterns
- Obvious anomalies or outliers
- Data provenance and collection method
```

## Phase 2: Exploratory Data Analysis (EDA)

```
COMPUTE descriptive statistics:
- Central tendency: mean, median, mode
- Dispersion: standard deviation, variance, IQR, range
- Distribution shape: skewness, kurtosis
- For categorical: frequency counts, proportions

ASSESS data quality:
- Missing values: count, pattern (MCAR, MAR, MNAR)
- Outliers: IQR method, Z-score method
- Duplicates: exact and near-duplicates
- Consistency: format issues, impossible values

EXPLORE relationships:
- Correlation matrix (numeric variables)
- Cross-tabulations (categorical variables)
- Group comparisons (categorical × numeric)
- Temporal patterns (if time variable exists)
```

## Phase 3: Hypothesis Testing

```
FORMULATE hypotheses:
- H0 (null hypothesis): no effect/relationship
- H1 (alternative hypothesis): specified effect/relationship
- Significance level: α = 0.05 (default, adjustable)

SELECT appropriate test:
┌─────────────────────────────────────────────────────────────────┐
│ Research Question          │ Data Type        │ Test             │
├─────────────────────────────────────────────────────────────────┤
│ Difference between 2 means│ Normal, indep.   │ Independent t    │
│ Difference between 2 means│ Normal, paired   │ Paired t         │
│ Difference between 2 means│ Non-normal       │ Mann-Whitney U   │
│ Difference among 3+ means │ Normal           │ One-way ANOVA    │
│ Difference among 3+ means │ Non-normal       │ Kruskal-Wallis   │
│ Association (2 categorical)│ Expected ≥5     │ Chi-square       │
│ Association (2 categorical)│ Expected <5     │ Fisher's exact   │
│ Correlation (2 numeric)   │ Normal           │ Pearson's r      │
│ Correlation (2 numeric)   │ Non-normal       │ Spearman's rho   │
│ Prediction (numeric DV)   │ Linear relation  │ Linear regression│
│ Prediction (binary DV)    │ Binary outcome   │ Logistic reg.    │
│ Time series trend         │ Sequential       │ Mann-Kendall     │
│ Survival analysis         │ Time-to-event    │ Kaplan-Meier     │
└─────────────────────────────────────────────────────────────────┘

CHECK assumptions:
- Normality: Shapiro-Wilk test, Q-Q plots
- Homogeneity of variance: Levene's test
- Independence: study design assessment
- Linearity: scatter plot inspection
- Multicollinearity: VIF (for regression)
```

## Phase 4: Advanced Analysis

```
REGRESSION ANALYSIS (when predicting outcomes):
- Simple linear regression: single predictor
- Multiple regression: multiple predictors
- Report: coefficients, p-values, R², adjusted R²
- Check: residual normality, homoscedasticity, linearity

CLUSTERING (when finding groups):
- K-means: when groups are spherical
- Hierarchical: when exploring structure
- DBSCAN: when groups have irregular shapes
- Report: cluster profiles, silhouette scores

TREND ANALYSIS (when temporal patterns matter):
- Moving averages
- Seasonal decomposition
- Growth rate computation
- Trend significance testing

FORECASTING (when predicting future):
- Linear extrapolation (short-term)
- Exponential smoothing
- Report: predictions with confidence intervals
- Caveat: assumptions and limitations
```

## Phase 5: Results Interpretation

```
FOR EACH statistical test:
1. State the test performed and why
2. Report test statistic and p-value
3. Report effect size (Cohen's d, η², r², odds ratio)
4. State confidence interval
5. Interpret in plain language
6. Acknowledge limitations

INTERPRETATION framework:
- Statistical significance ≠ practical significance
- Always report effect sizes alongside p-values
- Discuss confidence intervals, not just point estimates
- Acknowledge multiple comparisons (Bonferroni if needed)
- Distinguish correlation from causation
- Note sample size limitations
```

## Phase 6: Visualization Generation

```
SELECT visualization by data/finding type:

Distribution → Histogram, Box plot, Violin plot
Comparison → Bar chart, Grouped bar, Dot plot
Relationship → Scatter plot, Bubble chart
Composition → Pie chart (≤5 categories), Stacked bar
Time series → Line graph, Area chart
Correlation → Heatmap, Correlation matrix
Ranking → Horizontal bar, Lollipop chart
Flow → Sankey diagram, Alluvial plot
Geographic → Choropleth map, Bubble map

FOR EACH visualization:
- Title: descriptive and specific
- Axes: labeled with units
- Legend: clear and positioned well
- Caption: self-explanatory with source
- Color: accessible (colorblind-friendly)
- Annotation: highlight key findings
```

## Phase 7: Reporting

```
STRUCTURE findings section:
1. Overview of data characteristics
2. Key finding 1 (strongest evidence first)
   - Statistical evidence
   - Visualization
   - Interpretation
3. Key finding 2
   [continue...]
4. Unexpected findings
5. Non-significant results (important to report)
6. Summary table of all tests performed

INCLUDE:
- Summary statistics table
- Correlation matrix (if relevant)
- Regression table (if applicable)
- Effect size summary
- Confidence intervals for key estimates
```

## Statistical Reporting Standards

Follow APA statistical reporting format:
- t-test: t(df) = X.XX, p = .XXX, d = X.XX
- ANOVA: F(df1, df2) = X.XX, p = .XXX, η² = .XX
- Chi-square: χ²(df) = X.XX, p = .XXX, V = .XX
- Correlation: r(N) = .XX, p = .XXX
- Regression: β = X.XX, SE = X.XX, t = X.XX, p = .XXX

Always report to appropriate decimal places (p-values: 3; effect sizes: 2; descriptives: 2).
