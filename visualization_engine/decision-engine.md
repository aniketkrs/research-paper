# Visualization Decision Engine

## Purpose
Automatically determine when to create visualizations, what type to use, and how to implement them within the research paper context.

---

## Decision Algorithm

```
FUNCTION should_visualize(content_type, data_shape, paper_section):
    
    # MANDATORY visualization triggers
    IF content_type == "quantitative_comparison" AND items >= 3:
        RETURN true, select_chart(data_shape)
    
    IF content_type == "time_series" AND data_points >= 5:
        RETURN true, "line_chart"
    
    IF content_type == "process_or_workflow" AND steps >= 3:
        RETURN true, "flowchart"
    
    IF content_type == "system_architecture":
        RETURN true, "architecture_diagram"
    
    IF content_type == "geographic_distribution":
        RETURN true, "map_or_table"
    
    IF content_type == "correlation_matrix" AND variables >= 4:
        RETURN true, "heatmap"
    
    IF content_type == "statistical_distribution":
        RETURN true, "histogram_or_boxplot"
    
    # RECOMMENDED visualization triggers
    IF content_type == "comparison" AND dimensions >= 3:
        RETURN recommended, "radar_or_table"
    
    IF content_type == "hierarchy" AND levels >= 2:
        RETURN recommended, "tree_diagram"
    
    IF content_type == "composition" AND parts >= 3:
        RETURN recommended, "pie_or_stacked_bar"
    
    # SKIP visualization
    IF data_points <= 2:
        RETURN false, "use_inline_text"
    
    IF content_type == "single_metric":
        RETURN false, "use_inline_text"
    
    IF redundant_with_existing_figure:
        RETURN false, "already_visualized"
    
    RETURN evaluate_case_by_case
```

---

## Chart Selection Matrix

### By Communication Goal

| Goal | Best Chart | Alternative | Avoid |
|------|-----------|-------------|-------|
| Compare values | Bar chart | Dot plot | Pie chart |
| Show trend | Line chart | Area chart | Bar chart |
| Show distribution | Histogram | Box plot | Pie chart |
| Show composition | Stacked bar | Treemap | 3D charts |
| Show relationship | Scatter | Bubble | Bar chart |
| Show flow | Sankey | Flowchart | Pie chart |
| Show hierarchy | Tree | Sunburst | Flat charts |
| Show change | Slope chart | Waterfall | Area chart |
| Show parts of whole | Pie (≤5 parts) | Donut | Bar |
| Show ranking | Horizontal bar | Lollipop | Pie chart |

### By Data Characteristics

| Variables | Data Type | N (items) | Recommended |
|-----------|----------|-----------|-------------|
| 1 numeric | Distribution | Any | Histogram |
| 1 categorical | Frequency | ≤7 | Bar chart |
| 1 categorical | Frequency | 8+ | Horizontal bar |
| 2 numeric | Relationship | ≤50 | Scatter plot |
| 2 numeric | Relationship | 50+ | Density plot |
| 1 cat + 1 num | Comparison | 2-7 | Bar chart |
| 1 cat + 1 num | Comparison | 8+ | Horizontal bar |
| 2 cat | Association | Few × Few | Grouped bar |
| Many numeric | Correlation | 4-12 vars | Heatmap |
| Time + numeric | Trend | 5+ points | Line chart |
| Time + categories | Composition | — | Stacked area |

---

## Implementation Templates

### Mermaid (for diagrams, flows, architectures)

```markdown
​```mermaid
graph TD
    A[Step 1: Data Collection] --> B[Step 2: Preprocessing]
    B --> C{Quality Check}
    C -->|Pass| D[Step 3: Analysis]
    C -->|Fail| E[Step 2b: Clean Data]
    E --> C
    D --> F[Step 4: Visualization]
    F --> G[Step 5: Interpretation]
​```
```

Best for: Workflows, decision trees, system architectures, sequence diagrams, state machines.

### Python Code Block (for data visualizations)

```python
import matplotlib.pyplot as plt
import numpy as np

# Data
categories = ['Category A', 'Category B', 'Category C', 'Category D']
values = [42, 67, 35, 89]

# Create figure
fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(categories, values, color=['#2196F3', '#4CAF50', '#FF9800', '#9C27B0'],
              edgecolor='white', linewidth=0.8)

# Styling
ax.set_ylabel('Metric (units)', fontsize=11)
ax.set_title('Comparison of Categories by Metric', fontsize=13, fontweight='bold', pad=15)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.set_ylim(0, max(values) * 1.15)

# Value labels
for bar, val in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1.5,
            f'{val}', ha='center', va='bottom', fontsize=10)

plt.tight_layout()
plt.savefig('figure_N.png', dpi=300, bbox_inches='tight', facecolor='white')
```

Best for: Bar charts, line graphs, scatter plots, histograms, heatmaps, box plots.

### ASCII/Text (for inline simple visualizations)

```
Market Share Distribution (2024)
┌─────────────────────────────────────────────────────┐
│ Company A  ██████████████████████████████████  42%   │
│ Company B  ████████████████████████           28%   │
│ Company C  ███████████████                    18%   │
│ Company D  ████████                           12%   │
└─────────────────────────────────────────────────────┘
```

Best for: Simple comparisons when figures aren't needed, inline demonstrations, quick overviews.

### Markdown Table (for detailed structured data)

```markdown
| Approach | Accuracy | Latency (ms) | Memory (GB) | Cost ($/hr) |
|----------|:--------:|:------------:|:-----------:|:-----------:|
| Method A | **94.2%** | 12.3 | 2.1 | 0.45 |
| Method B | 91.8% | **8.7** | 3.4 | 0.62 |
| Method C | 93.5% | 15.1 | **1.8** | **0.31** |

*Bold indicates best-in-class for each metric.*
```

Best for: Multi-dimensional comparisons, exact values, detailed results, configuration comparisons.

---

## Visualization Budget per Paper Type

| Paper Type | Min Figures | Max Figures | Min Tables | Diagrams |
|-----------|:-----------:|:-----------:|:----------:|:--------:|
| Short paper (4-6 pages) | 2 | 4 | 1-2 | 0-1 |
| Full paper (8-12 pages) | 3 | 7 | 2-4 | 1-2 |
| Comprehensive (15-30 pages) | 5 | 12 | 3-6 | 2-3 |
| Literature review | 2 | 5 | 2-4 | 1-2 |
| Whitepaper | 4 | 10 | 3-5 | 2-4 |
| Thesis chapter | 4 | 8 | 2-5 | 1-3 |

---

## Anti-Patterns (Never Do)

- 3D charts (distort perception)
- Pie charts with >5 slices
- Dual y-axes (confusing)
- Truncated y-axes without clear marking
- Rainbow color schemes
- Charts without axis labels
- Figures without captions
- Visualizations that duplicate what the text says without adding insight
- Decorative charts (no analytical value)
- Overly complex visualizations when simple ones suffice
