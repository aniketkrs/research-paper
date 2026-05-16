# Data Analysis Pipeline

## Purpose
Structured process for ingesting, cleaning, analyzing, and presenting data within research papers.

---

## Pipeline Stages

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  1. INGEST  │───▶│  2. CLEAN   │───▶│ 3. EXPLORE  │───▶│ 4. ANALYZE  │───▶│ 5. PRESENT  │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
```

---

## Stage 1: Data Ingestion

### Supported Formats

```python
# CSV
import pandas as pd
df = pd.read_csv('data.csv', encoding='utf-8')

# JSON
df = pd.read_json('data.json')
# or for nested JSON:
import json
with open('data.json') as f:
    data = json.load(f)
df = pd.json_normalize(data)

# Excel
df = pd.read_excel('data.xlsx', sheet_name='Sheet1')

# Multiple sheets
all_sheets = pd.read_excel('data.xlsx', sheet_name=None)
```

### Initial Assessment Script

```python
def assess_data(df):
    """Generate initial data assessment for research paper."""
    report = {
        'shape': df.shape,
        'columns': list(df.columns),
        'dtypes': df.dtypes.to_dict(),
        'missing': df.isnull().sum().to_dict(),
        'missing_pct': (df.isnull().sum() / len(df) * 100).to_dict(),
        'numeric_summary': df.describe().to_dict(),
        'categorical_summary': {
            col: df[col].value_counts().head(10).to_dict()
            for col in df.select_dtypes(include='object').columns
        },
        'duplicates': df.duplicated().sum(),
        'memory_usage': df.memory_usage(deep=True).sum()
    }
    return report
```

---

## Stage 2: Data Cleaning

### Standard Cleaning Steps

```python
def clean_data(df):
    """Standard data cleaning pipeline."""
    
    # 1. Remove exact duplicates
    df = df.drop_duplicates()
    
    # 2. Handle missing values
    # Strategy depends on missingness mechanism and proportion
    for col in df.columns:
        missing_pct = df[col].isnull().sum() / len(df) * 100
        if missing_pct > 50:
            # Consider dropping column
            print(f"WARNING: {col} has {missing_pct:.1f}% missing")
        elif missing_pct > 0:
            if df[col].dtype in ['float64', 'int64']:
                # Numeric: median imputation (robust to outliers)
                df[col].fillna(df[col].median(), inplace=True)
            else:
                # Categorical: mode imputation or 'Unknown'
                df[col].fillna(df[col].mode()[0], inplace=True)
    
    # 3. Fix data types
    # Dates stored as strings
    date_cols = [c for c in df.columns if 'date' in c.lower()]
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # 4. Standardize text
    text_cols = df.select_dtypes(include='object').columns
    for col in text_cols:
        df[col] = df[col].str.strip().str.lower()
    
    # 5. Outlier detection (flag, don't remove by default)
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((df[col] < Q1 - 1.5*IQR) | (df[col] > Q3 + 1.5*IQR)).sum()
        if outliers > 0:
            print(f"INFO: {col} has {outliers} potential outliers")
    
    return df
```

### Missing Data Decision Tree

```
IF missing < 5%:
  → Listwise deletion OR mean/median imputation (low risk)

IF missing 5-20%:
  → Multiple imputation (mice) OR regression imputation
  → Report imputation method and assess sensitivity

IF missing 20-50%:
  → Multiple imputation with careful sensitivity analysis
  → Consider whether variable should be included
  → Report complete-case analysis alongside imputed analysis

IF missing > 50%:
  → Strongly consider dropping the variable
  → If kept: use pattern-mixture models or selection models
  → Full transparency in reporting

ALWAYS:
  → Assess missingness mechanism (MCAR/MAR/MNAR)
  → Little's MCAR test if warranted
  → Report missing data handling in methodology
```

---

## Stage 3: Exploratory Data Analysis

### Standard EDA Output

```python
def full_eda(df):
    """Complete exploratory data analysis for research paper."""
    
    # Univariate analysis
    print("=" * 60)
    print("UNIVARIATE ANALYSIS")
    print("=" * 60)
    
    # Numeric variables
    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        stats = {
            'mean': df[col].mean(),
            'median': df[col].median(),
            'std': df[col].std(),
            'min': df[col].min(),
            'max': df[col].max(),
            'skewness': df[col].skew(),
            'kurtosis': df[col].kurtosis(),
            'n_missing': df[col].isnull().sum()
        }
        print(f"\n{col}: {stats}")
    
    # Categorical variables
    cat_cols = df.select_dtypes(include='object').columns
    for col in cat_cols:
        print(f"\n{col}:")
        print(f"  Unique values: {df[col].nunique()}")
        print(f"  Top 5: {df[col].value_counts().head().to_dict()}")
    
    # Bivariate analysis
    print("\n" + "=" * 60)
    print("BIVARIATE ANALYSIS")
    print("=" * 60)
    
    # Correlation matrix
    if len(numeric_cols) >= 2:
        corr = df[numeric_cols].corr()
        print("\nCorrelation matrix:")
        print(corr.to_string())
        
        # Flag strong correlations
        for i in range(len(corr)):
            for j in range(i+1, len(corr)):
                r = corr.iloc[i, j]
                if abs(r) > 0.7:
                    print(f"  STRONG: {corr.index[i]} × {corr.columns[j]}: r={r:.3f}")
    
    return stats
```

---

## Stage 4: Statistical Analysis

### Analysis Selection Logic

```python
def select_analysis(research_question, iv_type, dv_type, n_groups=None, paired=False):
    """Select appropriate statistical test based on research design."""
    
    if dv_type == 'continuous':
        if iv_type == 'categorical':
            if n_groups == 2:
                if paired:
                    return 'paired_t_test', 'wilcoxon_signed_rank'
                else:
                    return 'independent_t_test', 'mann_whitney_u'
            elif n_groups >= 3:
                if paired:
                    return 'repeated_measures_anova', 'friedman'
                else:
                    return 'one_way_anova', 'kruskal_wallis'
        elif iv_type == 'continuous':
            return 'pearson_correlation', 'spearman_correlation'
        elif iv_type == 'multiple_continuous':
            return 'multiple_regression', 'robust_regression'
    
    elif dv_type == 'binary':
        if iv_type == 'categorical':
            return 'chi_square', 'fisher_exact'
        elif iv_type == 'continuous':
            return 'logistic_regression', 'logistic_regression'
    
    elif dv_type == 'ordinal':
        return 'ordinal_regression', 'mann_whitney_u'
    
    elif dv_type == 'count':
        return 'poisson_regression', 'negative_binomial'
    
    return 'consult_statistician', 'non_standard_case'
```

### Results Formatting

```python
def format_result(test_name, statistic, df, p_value, effect_size, ci_lower, ci_upper, n):
    """Format statistical result for academic paper."""
    
    # Determine significance
    if p_value < 0.001:
        p_str = "p < .001"
    else:
        p_str = f"p = {p_value:.3f}"
    
    # Format by test type
    templates = {
        'independent_t_test': f"t({df}) = {statistic:.2f}, {p_str}, d = {effect_size:.2f}, 95% CI [{ci_lower:.2f}, {ci_upper:.2f}]",
        'one_way_anova': f"F({df[0]}, {df[1]}) = {statistic:.2f}, {p_str}, η² = {effect_size:.3f}",
        'chi_square': f"χ²({df}) = {statistic:.2f}, {p_str}, V = {effect_size:.2f}",
        'pearson_correlation': f"r({n-2}) = {statistic:.3f}, {p_str}",
        'mann_whitney_u': f"U = {statistic:.0f}, {p_str}, r = {effect_size:.2f}",
    }
    
    return templates.get(test_name, f"statistic = {statistic:.3f}, {p_str}")
```

---

## Stage 5: Presentation

### Output Formats for Paper

```
DESCRIPTIVE STATISTICS TABLE:
| Variable | N | Mean | SD | Median | Min | Max |
|----------|---|------|-------|--------|-----|-----|
| [data]   |   |      |       |        |     |     |

COMPARISON TABLE:
| Variable | Group A (n=X) | Group B (n=X) | Test Statistic | p | Effect Size |
|----------|---------------|---------------|---------------|---|-------------|
| [data]   | M (SD)        | M (SD)        | t/F/U         |   | d/η²/r      |

REGRESSION TABLE:
| Predictor | B | SE | β | t | p | 95% CI |
|-----------|---|----|----|---|---|--------|
| (Constant)| X | X  | —  | X | X | [X, X] |
| Variable 1| X | X  | X  | X | X | [X, X] |
| Variable 2| X | X  | X  | X | X | [X, X] |
| R² = .XX, F(df1, df2) = X.XX, p < .001 |

CORRELATION MATRIX:
|   | Var1 | Var2 | Var3 | Var4 |
|---|------|------|------|------|
| Var1 | —  | .XX* | .XX  | .XX**|
| Var2 |    | —    | .XX* | .XX  |
| Var3 |    |      | —    | .XX* |
| Var4 |    |      |      | —    |
*p < .05, **p < .01
```

---

## Data Credibility Assessment

```
SCORE data credibility (1-10):

10: Gold standard (RCT, large N, validated instruments, published dataset)
 9: High quality (large sample, established methodology, institutional source)
 8: Good quality (adequate sample, standard methodology, reputable source)
 7: Acceptable (moderate sample, reasonable methodology)
 6: Adequate (smaller sample but appropriate for analysis)
 5: Marginal (limitations that may affect interpretation)
 4: Questionable (significant methodological concerns)
 3: Weak (small sample, poor methodology, or biased collection)
 2: Very weak (major validity concerns)
 1: Unreliable (cannot draw meaningful conclusions)

REPORT credibility score in methodology section with justification.
```
