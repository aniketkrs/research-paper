# Visualization Guide

This file is the chart-selection brain for the skill. Every figure decision
follows the rules below. The actual chart rendering happens in
`scripts/generate_charts.py`; the orchestration is in
`workflows/visual-generation-pipeline.md`.

> **Mantra:** "If it's worth saying twice, draw it once." A figure earns its
> place by communicating something prose cannot — a shape, a comparison, a
> distribution, a flow.

---

## 1. The chart-selection decision tree

```
What is the section trying to communicate?
│
├── Compare discrete categories
│   ├── 2–7 categories          → Bar chart (horizontal if labels are long)
│   ├── 7–20 categories         → Sorted horizontal bar chart
│   └── > 20 categories         → Lollipop chart or table; consider grouping
│
├── Show a trend over time
│   ├── 1 series                → Line chart
│   ├── 2–5 series              → Multi-line chart, distinct colors + markers
│   ├── > 5 series              → Small multiples (faceted), or interactive
│   └── Cumulative / total       → Stacked area chart
│
├── Show a distribution
│   ├── 1 variable, n < 100     → Strip plot or jittered dot plot
│   ├── 1 variable, n ≥ 100     → Histogram + KDE
│   ├── Compare distributions   → Violin plot (preferred over box plot)
│   └── Bivariate density        → 2-D histogram or contour
│
├── Show a relationship between two continuous vars
│   ├── n ≤ 200                 → Scatter plot + regression line + 95% CI
│   ├── n > 1,000               → Hex-bin or 2-D density
│   └── With a third dimension   → Color or size encoding (avoid 3D)
│
├── Show correlation among many variables
│   ├── 3–25 variables           → Correlation heatmap with values
│   ├── > 25 variables           → Cluster the heatmap, hide labels
│   └── With p-values            → Annotate cells; mark non-sig with stripes
│
├── Show parts of a whole
│   ├── 2–4 categories           → Stacked bar (NOT pie chart)
│   ├── Composition over time    → Stacked area / streamgraph
│   └── Hierarchy                 → Treemap or sunburst
│
├── Show flow / transformation
│   └── Sources → Sinks          → Sankey diagram
│
├── Show structure / pipeline / architecture
│   ├── Linear pipeline          → Block diagram with arrows
│   ├── DAG                       → Layered diagram
│   └── Layered system            → Tiered architecture diagram
│
├── Show a process / decision
│   └── States and transitions    → Flowchart (Mermaid)
│
├── Show geography
│   ├── Region-level metric      → Choropleth map
│   ├── Point events              → Point map (with cluster if dense)
│   └── Flows between regions     → Flow map / arc map
│
├── Show timeline of events
│   ├── Project / milestones      → Timeline / Gantt
│   └── Historical events         → Annotated timeline
│
├── Show conceptual structure
│   ├── Hierarchy                 → Tree / mind map
│   └── Network                    → Graph (force-directed)
│
└── Compare metrics side-by-side
    └── Many metrics × few items   → Comparative table (often best!)
```

---

## 2. The "table vs. figure" decision

Use a **table** when:
- The reader needs **exact values** (benchmark numbers, n, p-values).
- There are **few categories** and **multiple metrics** per category.
- The shape of the data is irregular and cannot be honestly visualized.

Use a **figure** when:
- The reader needs to perceive a **shape** (trend, distribution, cluster).
- The number of data points is too large for a table.
- A pattern is the point — not an exact number.

Many papers benefit from **both**: a figure for perception, a table in the
appendix for the numbers.

---

## 3. Universal figure standards

Every figure produced by this skill must satisfy:

1. **Caption that interprets, not just describes.** Bad: "Figure 2.
   Accuracy by model." Good: "Figure 2. Accuracy by model size on the
   reasoning benchmark. Larger models scale predictably until 33 B, after
   which gains plateau (cf. §4.2)."
2. **Axis labels with units.** "Latency (ms)", "Accuracy (%)", "Year".
3. **Sensible scale.** Linear by default; log when the dynamic range
   spans > 2 orders of magnitude. **State** when an axis is logarithmic.
4. **Colorblind-safe palette.** Default to **Okabe–Ito** (8 colors) or
   **viridis** for sequential. Never use red/green as the only distinction.
5. **Sufficient resolution.** ≥ 300 DPI for print, vector (SVG / PDF) for
   submission when possible.
6. **Readable type.** Axis labels ≥ 8 pt at final print size, tick labels
   ≥ 7 pt.
7. **No chart-junk.** Drop 3-D bars, drop shadows, gradient backgrounds,
   gridlines that don't aid reading.
8. **Significance marks.** When showing comparisons, mark significance
   explicitly (`*` p < .05, `**` p < .01, `***` p < .001) and explain in
   the caption.
9. **N in the figure.** Sample sizes annotated (e.g., `n = 80` per bar).
10. **Error bars are CIs**, not SE, by default — and the caption says so.
11. **Figure number** in caption, **referenced in the text** before it
    appears.

---

## 4. Chart-specific guidance

### 4.1 Bar charts
- Sort by value (descending) unless an inherent order exists (time, size,
  ordinal categories).
- Start the y-axis at zero. **Always.**
- Horizontal bars when category labels are long.
- Avoid "stacked-and-grouped" combinations — they're hard to read.
- Annotate values on bars when there are < 10.

### 4.2 Line charts
- Use distinct line styles + markers when printing in B&W is possible.
- Don't connect the dots when the x-axis is categorical — use a bar.
- Smooth lines only with explicit justification (LOWESS / spline);
  raw data should also be visible.

### 4.3 Scatter plots
- Add a regression line + 95% CI band (Pearson / robust regression).
- Use transparency (`alpha`) when n > 200 to reveal density.
- Call out interesting points by labeling, not by garish colors.

### 4.4 Histograms
- Use ≥ 20 and ≤ 100 bins; Freedman–Diaconis rule by default.
- Overlay a KDE only if it doesn't obscure the histogram.
- Show summary stats (M, Mdn, SD, n) in the caption or annotation.

### 4.5 Box / violin plots
- Prefer **violin** with overlaid box — shows distribution and summary.
- Annotate n per group.
- Mark significant pairwise differences with brackets.

### 4.6 Heatmaps
- Use a **diverging** palette (RdBu) when the data has a meaningful zero
  (e.g., correlations centered at 0).
- Use a **sequential** palette (viridis) when the data has a natural
  ordering from low to high.
- Annotate cells with values when ≤ 100 cells.
- Cluster rows / columns when the order isn't inherent.

### 4.7 Geographic maps
- **Choropleth**: normalize by population / area before coloring.
  Raw counts on choropleths are almost always wrong.
- **Equal-area projection** (Albers / Equal Earth) for analytic maps;
  Mercator only when geography is local enough that distortion is small.
- Provide a **legend** with units and a clear scale.
- Hide the basemap detail that doesn't help the reader.

### 4.8 Flow / Sankey
- Order nodes by total flow (largest at top).
- Use no more than 5–7 distinct flow colors.
- Annotate values on the largest flows.

### 4.9 Diagrams (architecture / process)
- Render with **Mermaid** by default — it's portable across renderers.
- Group related blocks into subgraphs.
- Show data direction with arrowheads, control direction with dashed lines.
- Caption with a 1–2 sentence interpretation.

### 4.10 Forest plots (meta-analysis)
- One row per study, point estimate as a square (size = weight),
  horizontal line = 95% CI.
- Diamond at the bottom = pooled estimate.
- Vertical line at no-effect (1 for OR/RR, 0 for SMD).
- Heterogeneity stats (`I²`, `τ²`, `Q`) in the caption.

---

## 5. Numbering and references

- **Figures:** `Figure 1`, `Figure 2`, … numbered in order of in-text
  appearance.
- **Tables:** `Table 1`, `Table 2`, … same convention.
- **Algorithms:** `Algorithm 1`, … same convention.
- Every figure / table MUST be referenced in the text **before** it appears,
  using "Figure 3" or "Table 1" (no "the figure below" — bad cross-platform
  rendering).
- Equations are numbered `(1)`, `(2)`, … and referenced as "Eq. (3)".

---

## 6. Defaults the skill enforces

When `scripts/generate_charts.py` runs without explicit style, it uses:

```python
DEFAULTS = {
    "palette": "okabe_ito",          # categorical, colorblind-safe
    "sequential_palette": "viridis", # for heatmaps
    "diverging_palette": "RdBu_r",   # for correlation heatmaps
    "context": "paper",              # seaborn context
    "font_scale": 1.0,
    "figure_dpi": 300,
    "save_format": ["png", "svg"],   # both rasterized and vector
    "axis_grid": "y",                # subtle horizontal grid only
    "spine_top_right": False,        # remove top and right spines
    "ci": 95,                        # default confidence interval
    "n_bootstrap": 2000,
}
```

These are tuned for paper-figure quality. They can be overridden per-figure.

---

## 7. Anti-patterns (the skill must refuse / replace)

- **3-D bar / pie / scatter charts.** Replace with 2-D equivalents.
- **Pie charts with > 4 slices.** Replace with a sorted bar chart.
- **Truncated y-axes** to exaggerate differences. Always start at zero
  unless the user explicitly requests otherwise *and* the figure annotates
  the truncation.
- **Dual y-axes** with mismatched scales. Replace with two stacked panels.
- **Rainbow / jet palettes.** Replace with viridis (perceptually uniform).
- **Embedded raster screenshots** of tables. Replace with a real Markdown
  / LaTeX table.
- **Gridlines on every tick.** Use sparingly; they should support, not
  decorate.
- **Bar charts with no zero baseline.** Re-anchor to zero.

---

## 8. Caption pattern (mandatory)

Every caption follows this structure:

> **Figure N.** *[What it shows]*. *[Method note: data source, n, what the
> bars / lines / colors mean]*. *[Interpretation in 1–2 sentences]*.
> *[Reference to where it is discussed in the text, optional]*.

Example:
> **Figure 4.** Per-task accuracy of four LLMs on the GSM8K math benchmark
> across five random seeds. Bars show mean accuracy; error bars are
> bootstrap 95 % CIs (n = 1,319 per task). The 70 B model significantly
> outperforms the 13 B and 7 B variants on every task; the gap to the
> 33 B variant is statistically inconclusive (see §5.2).

---

## 9. Accessibility checklist (per figure)

- [ ] Colorblind-safe palette (Okabe–Ito or viridis-family).
- [ ] Encoding does not rely on color alone (use shape / linestyle / pattern).
- [ ] Sufficient contrast (≥ 4.5:1 for text, ≥ 3:1 for large text).
- [ ] All text is selectable (vector format) when possible.
- [ ] Alt-text for the figure provided as the caption (see §8).
- [ ] No flicker / animation in static papers.

---

## 10. Mermaid templates (for environments without Python)

Architecture diagram:
~~~mermaid
flowchart LR
    A[Input] --> B{Preprocess}
    B -->|tokenize| C[Encoder]
    B -->|filter| D[Cleaner]
    C --> E[Decoder]
    D --> E
    E --> F[Output]
~~~

PRISMA flow:
~~~mermaid
flowchart TD
    A[Records identified<br/>n = 2,341] --> B[Duplicates removed<br/>n = 412]
    B --> C[Title/abstract screened<br/>n = 1,929]
    C -->|excluded n = 1,724| D
    C --> E[Full-text reviewed<br/>n = 205]
    E -->|excluded n = 142<br/>with reasons| F[Studies included<br/>n = 63]
~~~

Timeline:
~~~mermaid
gantt
    title Project Timeline
    dateFormat  YYYY-MM-DD
    section Design
    Literature review     :a1, 2024-01-01, 30d
    Protocol drafting     :a2, after a1, 21d
    section Data
    Recruitment           :b1, 2024-02-15, 60d
    Data collection       :b2, after b1, 90d
    section Analysis
    Statistical analysis  :c1, after b2, 30d
    Drafting              :c2, after c1, 45d
~~~

Concept hierarchy:
~~~mermaid
mindmap
  root((Research Topic))
    Theory
      Foundations
      Recent advances
    Methods
      Quantitative
      Qualitative
      Mixed
    Applications
      Healthcare
      Education
      Industry
~~~

Always wrap Mermaid diagrams in a Markdown caption block exactly as in §8.
