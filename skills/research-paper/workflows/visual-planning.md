# Visual Planning Workflow

## Purpose
Intelligently determine when, what, and how to visualize data and concepts within research papers. Every visualization must serve a clear communicative purpose.

---

## Decision Engine: When to Visualize

```
ALWAYS visualize when:
- Presenting quantitative comparisons (3+ items)
- Showing trends over time (5+ data points)
- Illustrating relationships between variables
- Displaying geographic distributions
- Explaining complex processes or architectures
- Summarizing large datasets
- Showing statistical distributions

NEVER visualize when:
- Only 2 data points (use inline text comparison)
- Data is better served by a simple sentence
- The visualization would be trivially simple (single bar)
- Redundant with a table already present
- No clear insight is gained from visual form

PREFER tables over charts when:
- Exact values matter more than patterns
- Many variables for few observations
- Reader needs to look up specific values
- Comparing text/categorical attributes
```

## Chart Type Selection Matrix

```
┌────────────────────────────────────────────────────────────────────────────┐
│ Communication Goal        │ Data Shape              │ Recommended Chart     │
├────────────────────────────────────────────────────────────────────────────┤
│ Compare categories        │ Few categories (≤7)     │ Vertical bar chart    │
│ Compare categories        │ Many categories (8+)    │ Horizontal bar chart  │
│ Compare categories        │ 2 groups × categories   │ Grouped bar chart     │
│ Show composition          │ Parts of whole (≤5)     │ Pie/donut chart       │
│ Show composition          │ Parts of whole (6+)     │ Stacked bar chart     │
│ Show composition over time│ Time × categories       │ Stacked area chart    │
│ Show trend                │ Time series (single)    │ Line chart            │
│ Show trend                │ Time series (multiple)  │ Multi-line chart      │
│ Show relationship         │ 2 continuous vars       │ Scatter plot          │
│ Show relationship         │ 3 continuous vars       │ Bubble chart          │
│ Show relationship         │ Many × many vars        │ Correlation heatmap   │
│ Show distribution         │ Single continuous var   │ Histogram             │
│ Show distribution         │ Groups × continuous     │ Box plot / violin     │
│ Show flow/process         │ Sequential steps        │ Flowchart (Mermaid)   │
│ Show flow/transfer        │ Source → destination    │ Sankey diagram        │
│ Show hierarchy            │ Tree structure          │ Tree diagram          │
│ Show geography            │ Location data           │ Map / choropleth      │
│ Show timeline             │ Events over time        │ Timeline diagram      │
│ Show architecture         │ System components       │ Architecture diagram  │
│ Show ranking              │ Ordered values          │ Lollipop / bar chart  │
│ Show change               │ Before → after          │ Slope chart           │
│ Show network              │ Nodes and connections   │ Network diagram       │
└────────────────────────────────────────────────────────────────────────────┘
```

## Visualization Implementation

### Mermaid Diagrams (for flowcharts, architectures, sequences)

```markdown
​```mermaid
graph TD
    A[Start] --> B{Decision}
    B -->|Yes| C[Action 1]
    B -->|No| D[Action 2]
    C --> E[End]
    D --> E
​```
```

### Python/Matplotlib Code Blocks (for data charts)

```python
import matplotlib.pyplot as plt
import numpy as np

# Generate visualization
fig, ax = plt.subplots(figsize=(10, 6))
ax.bar(categories, values, color='steelblue', edgecolor='white')
ax.set_xlabel('Category', fontsize=12)
ax.set_ylabel('Value', fontsize=12)
ax.set_title('Descriptive Title', fontsize=14, fontweight='bold')
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
plt.tight_layout()
plt.savefig('figure_1.png', dpi=300, bbox_inches='tight')
```

### ASCII/Text Visualizations (for inline representation)

```
Revenue by Quarter (2024, in $M)
Q1  ████████████████████ 45.2
Q2  ██████████████████████████ 58.1
Q3  ████████████████████████████████ 71.3
Q4  ██████████████████████████████████████ 84.6
```

### Markdown Tables (for structured comparisons)

```markdown
| Metric | Group A | Group B | Difference | p-value |
|--------|---------|---------|------------|---------|
| Mean   | 42.3    | 38.1    | 4.2        | 0.023*  |
| SD     | 8.7     | 9.2     | —          | —       |
| N      | 156     | 148     | —          | —       |

*p < 0.05
```

## Caption Writing Protocol

```
FORMAT: Figure [N]: [Descriptive title]. [Method/source]. [Key takeaway].

EXAMPLES:
- Figure 1: Distribution of response times across experimental conditions. 
  Box plots show median (line), IQR (box), and outliers (dots). 
  Source: experimental data (N=240).

- Figure 2: Year-over-year growth in global AI patent filings (2015-2024). 
  Data sourced from WIPO Global Patent Database. 
  Note the acceleration beginning in 2020 coinciding with transformer architecture adoption.

- Table 1: Comparison of model architectures by parameter count, training cost, 
  and benchmark performance. Values represent mean ± standard deviation across 
  three independent training runs.
```

## Figure Numbering and Cross-Referencing

```
RULES:
1. Number all figures sequentially: Figure 1, Figure 2, Figure 3...
2. Number all tables sequentially (separate from figures): Table 1, Table 2...
3. Reference BEFORE the figure appears: "As illustrated in Figure 3..."
4. Never say "the figure below" or "the following chart" — always use the number
5. Group related figures: Figure 4a, Figure 4b (if showing related views)

REFERENCE phrases:
- "Figure N illustrates..."
- "As shown in Figure N..."
- "The relationship depicted in Figure N..."
- "Table N summarizes..."
- "Comparing columns in Table N reveals..."
```

## Color and Accessibility Guidelines

```
USE:
- Colorblind-friendly palettes (avoid red-green only distinctions)
- Sequential palettes for ordered data (light to dark)
- Diverging palettes for data with meaningful center (e.g., positive/negative)
- Categorical palettes for unordered groups (distinct hues)

ENSURE:
- Sufficient contrast between elements
- Labels readable without relying on color alone
- Patterns/shapes as secondary encoding
- Grayscale legibility for print
```

## Visualization Quality Checklist

- [ ] Clear, descriptive title
- [ ] Labeled axes with units
- [ ] Legend present (if multiple series)
- [ ] Source attribution in caption
- [ ] Self-explanatory caption
- [ ] Referenced in text before appearance
- [ ] Interpretation provided after figure
- [ ] Appropriate chart type for data
- [ ] Not redundant with other figures
- [ ] Colorblind accessible
- [ ] Consistent style with other figures in paper
