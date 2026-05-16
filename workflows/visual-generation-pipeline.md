# Visual Generation Pipeline

This pipeline turns "I want this paper" into "this paper has the right
figures and tables, in the right places, with the right captions". It is
called from `workflows/research-orchestration.md §6`.

> **Two-phase rule:** PLAN every figure / table before generating any of
> them. Otherwise you'll waste tokens on charts the paper doesn't need.

---

## Phase 1 — Plan

### 1.1 Scan the outline

Walk through `outline.md` section by section. For each section, ask the
**chart-selection decision tree** from `references/visualization-guide.md
§1`. The output is a planned figure / table per section that needs one.

### 1.2 Build `figures-plan.md`

Format:

```yaml
- id: figure-1
  section: 4. Method
  type: architecture-diagram
  source: described in section 4.1
  caption: "System architecture: input → preprocessor → encoder →
    classifier → output. The dashed arrow indicates an optional
    reranker (Section 4.4)."
  generation: mermaid

- id: figure-2
  section: 6.1 Main results
  type: grouped-bar-chart
  source: analysis/main-results.csv
  caption: "Mean accuracy by model size on three reasoning benchmarks
    over 5 seeds. Error bars are bootstrap 95 % CIs (n_boot = 2000).
    Stars indicate paired-bootstrap p < .01 vs. the next-smaller
    model after Holm–Bonferroni correction."
  generation: python
  script: scripts/generate_charts.py
  args:
    - --type grouped-bar
    - --input analysis/main-results.csv
    - --x model_size --y accuracy --hue benchmark
    - --ci 95 --n_boot 2000
    - --out figures/figure-2

- id: table-1
  section: 5.1 Datasets
  type: comparison-table
  source: outline of datasets in §5.1
  caption: "Datasets used in this study."
  generation: markdown
```

### 1.3 Sanity checks before generating

- Every section that **discusses** a comparison, trend, distribution, flow,
  process, or geography has at least one planned figure or table.
- No section has more than 3 figures / tables (split or move otherwise).
- Total figures + tables: typically 4–10 for an 8-page paper, 8–20 for a
  thesis chapter, 15–40 for a survey.
- Numbering is sequential and matches in-text references.

---

## Phase 2 — Generate

### 2.1 Pick the renderer

For each item in `figures-plan.md`:

| `generation` | Renderer                                                |
| ------------ | ------------------------------------------------------- |
| `python`     | `scripts/generate_charts.py` (matplotlib / seaborn / plotly) |
| `mermaid`    | Inline Mermaid block in the Markdown                     |
| `markdown`   | Inline Markdown table                                    |
| `latex`      | LaTeX figure / table block (when output target is LaTeX) |
| `image`      | User-supplied image; copy to `figures/`                 |

### 2.2 If Python is available

Run `scripts/generate_charts.py` per figure. Each call writes
`figures/<id>.png` and `figures/<id>.svg` and prints a Markdown snippet to
embed:

```markdown
![Figure 2 caption text](figures/figure-2.png)

**Figure 2.** <interpretive caption>
```

### 2.3 If Python is unavailable (graceful fallback)

| Original plan          | Fallback                                       |
| ---------------------- | ---------------------------------------------- |
| Bar / line / scatter    | Markdown table + ASCII bar (textual sparklines) |
| Distribution / violin   | Summary stats in a table + Markdown            |
| Heatmap                  | Markdown table with cell-shading via emoji or `█` blocks |
| Architecture / flowchart | Mermaid `flowchart`                            |
| PRISMA flow              | Mermaid `flowchart TD`                         |
| Timeline / Gantt          | Mermaid `gantt`                               |
| Mind-map                 | Mermaid `mindmap`                              |
| Geographic map            | Markdown table grouped by region (or skip with note) |

The fallback **never** silently drops the visualization. The paper always
has a figure or table where one was planned.

### 2.4 Captions

Every caption follows the four-part pattern from
`references/visualization-guide.md §8`:

> **Figure N.** [What it shows]. [Method note]. [Interpretation].
> [Reference to discussion section, optional].

The script auto-generates a draft caption from the plan; the writer agent
refines it during §7 Drafting.

### 2.5 In-text references

For every figure / table generated, the orchestrator's writer agent must
insert a forward reference in the prose **before** the figure appears:

> "As Figure 3 shows, …" or "(Figure 3)" or "see Table 1".

The validation pass flags any figure / table with no in-text reference.

---

## Phase 3 — Quality gates

For each generated figure, verify:

- [ ] Caption is interpretive, not just descriptive.
- [ ] Axis labels include units.
- [ ] Sample sizes annotated.
- [ ] Error bars labeled (CI vs. SE vs. SD).
- [ ] Colorblind-safe palette.
- [ ] Sequential numbering with in-text reference.
- [ ] No 3-D bars / pie charts with > 4 slices.
- [ ] No truncated y-axis without explicit annotation.

For each generated table:

- [ ] Clear column headers, units in headers when relevant.
- [ ] Numeric columns right-aligned.
- [ ] Best per column highlighted (bold) when comparing methods.
- [ ] N per row / column visible.
- [ ] Caption above the table.

Failures are emitted to `figures-plan.md` `issues:` block; the orchestrator
either re-renders or surfaces the issue in `Known gaps`.

---

## Phase 4 — Special cases

### 4.1 PRISMA flow (literature reviews)

Always rendered as Mermaid:

~~~mermaid
flowchart TD
    A[Records identified<br/>n = 2,341] --> B[Duplicates removed<br/>n = 412]
    B --> C[Title/abstract screened<br/>n = 1,929]
    C -->|excluded n = 1,724| D
    C --> E[Full-text reviewed<br/>n = 205]
    E -->|excluded n = 142<br/>with reasons| F[Studies included<br/>n = 63]
~~~

### 4.2 Forest plot (meta-analysis)

Generated by `scripts/generate_charts.py --type forest`. Required columns
in the input CSV: `study, year, n, effect, ci_lower, ci_upper, weight`.
The script computes the pooled estimate via random-effects (REML).

### 4.3 Architecture diagrams

Default to Mermaid `flowchart LR` (or `TD`) for portability. Reserve
`graphviz` / `tikz` for cases where Mermaid can't express the layout.

Pattern:

~~~mermaid
flowchart LR
    subgraph Input
      A[Document]
      B[Metadata]
    end
    subgraph Pipeline
      C[Tokenizer] --> D[Encoder]
      D --> E[Reranker]
    end
    A --> C
    B --> E
    E --> F[Top-k Output]
~~~

### 4.4 Geographic maps

If `geopandas` is available, render via `scripts/generate_charts.py --type
choropleth --geo <shapefile>`. Otherwise emit a Markdown table grouped by
region. Maps **must** declare projection in the caption.

### 4.5 Comparative summary table

For survey papers, the comparison table can become unwieldy. The script
supports `--type comparison-table --collapse` to produce a long-form
Markdown table that's still readable, plus an SVG cheat-sheet version for
the figures appendix.

### 4.6 Algorithms

Render as a fenced code block with line numbers. Counted alongside figures
in the numbering scheme (`Algorithm 1`, `Algorithm 2`).

### 4.7 Equations

Inline equations: `$E = mc^2$`. Display equations: numbered, right-aligned:

```
L(θ) = E_{(x,y)~D} [ ℓ(f_θ(x), y) ] + λ · R(θ)        (1)
```

Numbered equations referenced in text as "Eq. (1)".

---

## Phase 5 — Persistence and cleanup

After Phase 2:

- All raster figures live in `figures/<id>.png`.
- All vector figures live in `figures/<id>.svg`.
- All Mermaid sources live in `figures/<id>.mmd`.
- All table CSVs live in `tables/<id>.csv`.
- The `figures-plan.md` is updated with the actual paths and any issues.

The final paper references figures by relative path
(`figures/figure-2.png`); the writer agent ensures the alt-text matches
the caption.

---

## Phase 6 — Decision engine summary

**The skill picks a chart automatically** by walking this decision sequence
on the section's content:

```
Step 1 — What is the section's primary intent?
        ↓
        compare | trend | distribute | relate | flow | structure | locate | enumerate
        ↓
Step 2 — How many items / categories?
        ↓
Step 3 — Is the data continuous, ordinal, or categorical?
        ↓
Step 4 — Is there a temporal axis?
        ↓
Step 5 — Are confidence intervals or error needed?
        ↓
Step 6 — Pick the chart from the matrix in
         references/visualization-guide.md §1.
        ↓
Step 7 — Pick renderer (python / mermaid / markdown).
        ↓
Step 8 — Generate. Verify. Number. Reference.
```

This decision is logged in `figures-plan.md → reasoning` so the choice is
auditable.
