# Prompt: Visualization Planning

Used in `workflows/research-orchestration.md §6 Visualization`.

---

## Step 1 — Walk the outline

```
Read outline.md. For every section, ask the chart-selection decision tree
(references/visualization-guide.md §1):

  What is this section trying to communicate?
    - compare        → bar / lollipop / table
    - trend          → line / area
    - distribute     → histogram / violin
    - relate         → scatter / heatmap
    - flow           → Sankey / flowchart
    - structure      → architecture / tree
    - locate         → choropleth / point map
    - sequence       → timeline / Gantt
    - hierarchy      → mindmap / tree
    - enumerate      → comparative table

For each section, propose 0-3 figures or tables.

Sections that PURELY describe (intro context paragraphs, abstract,
acknowledgments) usually need no figures. Sections that COMPARE, TREND,
DISTRIBUTE, RELATE, FLOW, or LOCATE almost always need at least one.
```

---

## Step 2 — Build figures-plan.md

```
For each planned figure / table, write a YAML block:

- id: figure-1
  section: 4. Method
  type: <one of: bar, line, scatter, histogram, violin, heatmap, sankey,
        flowchart, mindmap, choropleth, gantt, forest, comparison-table,
        architecture-diagram, prisma-flow, ...>
  source: <data file or "described in section X.Y">
  caption: <one-sentence draft caption — the writer agent will refine>
  generation: <python | mermaid | markdown | latex | image>
  script: <if python> scripts/generate_charts.py
  args:
    - --type <type>
    - --input <path>
    - <additional args>
  reasoning: <one sentence: why this chart, why not the alternatives>

Cross-check with the visualization-guide.md anti-patterns (§7) before
finalizing each. NO 3D bars. NO pie charts > 4 slices. NO truncated y-axes.
```

---

## Step 3 — Numbering

```
Walk through outline.md in order. Assign:
- Figure 1, Figure 2, Figure 3, ... in order of in-text appearance.
- Table 1, Table 2, Table 3, ... independently.
- Algorithm 1, Algorithm 2, ... if present.
- Equations: (1), (2), (3), ... if numbered display equations exist.

Update figures-plan.md with the assigned numbers. Verify in-text
references in the outline match the numbering.
```

---

## Step 4 — Render plan

```
For each entry in figures-plan.md, decide HOW to render:

- If Python is available AND the source is a CSV / dataframe → run
  scripts/generate_charts.py with the args above. Produces both PNG
  and SVG into figures/<id>.{png,svg}.

- If Python is unavailable OR the source is conceptual (architecture,
  flowchart, timeline, PRISMA) → emit Mermaid:

    ```mermaid
    flowchart LR
      A[...] --> B[...]
    ```

- If the figure is a table → emit Markdown table directly in the section.

- If the user supplied an image → copy to figures/ with the assigned id
  as filename.

Save Mermaid sources to figures/<id>.mmd as well so they can be rendered
elsewhere.
```

---

## Step 5 — Caption pattern

```
Every caption follows the four-part pattern:

  Figure N. <What it shows>. <Method note: data source, n, what bars/
  lines/colors mean>. <Interpretation in 1-2 sentences>. <Reference to
  discussion section, optional>.

Auto-generate a draft from the planning data; the writer agent refines
during §7 Drafting.

Example:
  Figure 4. Per-task accuracy of four LLMs on the GSM8K math benchmark
  across five random seeds. Bars show mean accuracy; error bars are
  bootstrap 95% CIs (n = 1,319 per task). The 70 B model significantly
  outperforms the 13 B and 7 B variants on every task; the gap to the
  33 B variant is statistically inconclusive (see Section 5.2).
```

---

## Step 6 — Quality gates

```
Before finalizing the plan, run the per-figure quality checklist
(references/visualization-guide.md §3):

[ ] Caption interprets, not just describes
[ ] Axis labels include units
[ ] Sensible scale (linear by default; log only when justified)
[ ] Colorblind-safe palette (Okabe-Ito or viridis)
[ ] Sufficient resolution (>=300 DPI; SVG for vector)
[ ] No chart-junk
[ ] Significance marks where comparisons are made
[ ] N annotated
[ ] Error bars labeled (CIs by default)
[ ] Sequential numbering with in-text reference
[ ] No 3D / pie > 4 / truncated y / dual y / rainbow palette

Failures: revise the plan and re-render.
```

---

## Step 7 — Tables

```
Tables follow their own quality rules:

- Caption ABOVE the table, "Table N." prefix.
- Column headers clear; units in headers when relevant.
- Numeric columns right-aligned.
- Ordering: by a meaningful axis (size, time, alphabetical, performance).
- Best-per-column highlighted in bold for comparison tables.
- N visible (per row, per column, or in the caption).
- For long tables: split between main text (summary) and appendix (full).
- Markdown tables for inline rendering; CSV in tables/ for archival.
```

---

## Step 8 — Special-case figures

For these specific cases, use the dedicated templates:

- **Architecture diagrams** → Mermaid `flowchart` (preferred) or
  `graphviz`. Include subgraphs to group components. Show data direction
  with arrowheads.

- **PRISMA flow** → Mermaid `flowchart TD` with the four standard stages
  (Identification, Screening, Eligibility, Included).

- **Forest plots** → `scripts/generate_charts.py --type forest`. Required
  CSV columns: study, year, n, effect, ci_lower, ci_upper, weight.

- **Geographic maps** → choropleth via `geopandas` if available; otherwise
  table grouped by region.

- **Mind-maps / hierarchies** → Mermaid `mindmap`.

- **Timelines / Gantt** → Mermaid `gantt`.

- **Algorithm pseudocode** → fenced code block with line numbers, captioned
  "Algorithm N. <name>." above the block.

- **Equations** → numbered display blocks; reference inline as "Eq. (1)".
```

---

## Step 9 — Storyboard the figures (optional)

```
For papers > 8 pages, write a "figure storyboard": a one-paragraph
narrative that walks a reader who looks ONLY at the figures (no body
text) through the paper. If that paragraph doesn't tell the story, the
figures are incomplete. Add or rearrange figures until it does.
```

This is the highest-impact pre-write check. Most papers fail it — and the
fix is usually one missing summary figure.
