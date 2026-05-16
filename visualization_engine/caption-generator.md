# Academic Caption Generator

## Purpose
Generate proper academic captions for all figures and tables that are self-explanatory, properly numbered, and include source attribution.

---

## Caption Structure

### Figures

```
Figure [N]: [Descriptive title in sentence case]. [Method/visualization type]. 
[Key observation or data source]. [Sample size or time period if relevant].
```

### Tables

```
Table [N]: [Descriptive title in sentence case]
[Table content]
Note: [Explanations of abbreviations, significance markers, special notations].
Source: [Data attribution if from external source].
```

---

## Caption Templates by Chart Type

### Bar Chart
```
Figure [N]: Comparison of [metric] across [categories] ([time period/context]). 
Bars represent [what bars show]; error bars indicate [standard deviation / 95% CI / SEM]. 
[Key finding highlighted]. Data source: [source] (N = [sample size]).
```

### Line Chart
```
Figure [N]: Temporal trend in [metric] from [start year] to [end year]. 
[Solid/dashed] line represents [what]; shaded region indicates [95% confidence interval / 
prediction interval]. [Notable trend or inflection point]. 
Source: [data source].
```

### Scatter Plot
```
Figure [N]: Relationship between [X variable] and [Y variable] (N = [sample size]). 
Each point represents [unit of observation]. Dashed line shows linear regression fit 
(R² = [value], p [< or =] [value]). [Key observation about the relationship].
```

### Heatmap / Correlation Matrix
```
Figure [N]: [Pearson/Spearman] correlation matrix for [variables described]. 
Color intensity represents correlation strength; values range from -1 (strong negative) 
to +1 (strong positive). Correlations significant at p < .05 are marked with *.
```

### Box Plot
```
Figure [N]: Distribution of [metric] across [groups]. Box boundaries represent 
interquartile range (IQR); horizontal line indicates median; whiskers extend to 
1.5 × IQR; dots represent outliers. [Group with highest/lowest median noted].
N per group: [group1] = [n], [group2] = [n], [group3] = [n].
```

### Pie / Donut Chart
```
Figure [N]: Composition of [total entity] by [category dimension] ([year/context]). 
Percentages represent [proportion of what]. Total: [N or amount with units]. 
Source: [data source].
```

### Flowchart / Process Diagram
```
Figure [N]: [Process/workflow/methodology] [name or description]. 
[What each shape represents]. [Direction of flow described]. 
[Decision points or branching logic noted if not self-evident].
```

### Architecture Diagram
```
Figure [N]: System architecture of [system name]. Components are organized by 
[layer/function/data flow]. Arrows indicate [data flow / control flow / dependencies]. 
[Key design decision or constraint noted].
```

### Timeline
```
Figure [N]: Timeline of [events/developments] in [domain] ([start year]–[end year]). 
[Selection criteria for included events]. [Key turning points or clusters noted].
```

### Map / Geographic Visualization
```
Figure [N]: Geographic distribution of [phenomenon] across [region/scope] ([year/period]). 
Color intensity represents [metric]; [classification method if choropleth]. 
Data source: [source]. [Notable geographic pattern highlighted].
```

---

## Caption Quality Rules

1. **Self-sufficiency**: A reader should understand the figure from the caption alone, without reading surrounding text.

2. **What, not why**: Captions describe what is shown, not why it matters (interpretation goes in the text).

3. **Technical precision**: Include statistical details (N, CI, p-values) when relevant.

4. **Source attribution**: Always credit external data sources.

5. **Abbreviation definitions**: Define any abbreviation used in the figure within the caption.

6. **Significance markers**: Explain asterisks or other markers in a note below tables.

---

## Table Notes Convention

```
Table [N]: [Title]

| Col A | Col B | Col C | Col D |
|-------|-------|-------|-------|
| data  | data  | data* | data  |
| data  | data  | data  | data**|

Note: *p < .05; **p < .01; ***p < .001. 
SD = standard deviation; CI = confidence interval; OR = odds ratio.
Bold values indicate statistical significance at α = .05.
Source: [Attribution if external data].
```

---

## Numbering and Cross-Reference Protocol

```
RULES:
- Figures: sequential Arabic numerals (Figure 1, Figure 2, Figure 3...)
- Tables: separate sequence (Table 1, Table 2, Table 3...)
- Sub-figures: lowercase letters (Figure 3a, Figure 3b)
- Equations: parenthetical Arabic numerals (1), (2), (3)

IN-TEXT REFERENCES (appear BEFORE the figure):
- "As illustrated in Figure 3, the relationship between..."
- "Table 2 summarizes the demographic characteristics..."
- "The workflow (Figure 5) consists of three phases..."
- "Results are presented in Figure 4 and Table 3."

NEVER:
- "The figure below shows..."
- "As seen in the following chart..."
- "The above table..."
(Always use the figure/table number for unambiguous reference)
```
