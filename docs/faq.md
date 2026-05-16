# FAQ

---

## General

### What is `research-paper`?

A Claude Agent Skill that produces publication-ready research papers,
literature reviews, theses, whitepapers, surveys, and policy briefs.
It runs as a multi-agent orchestration over Claude Code (or any
compatible Agent Skills runtime) and combines rigorous methodology,
multi-style citations, real visualizations, and a simulated peer-
review pass.

### How is this different from "just asking Claude to write a paper"?

Without this skill, the model writes blog-quality prose with made-up
citations and no figures. With this skill:

- **Plan, not stream.** A research plan precedes any prose.
- **Evidence-first.** Every claim has a citation, dataset, or
  derivation.
- **No fabrication.** Unverifiable sources are flagged, not invented.
- **Visual-by-default.** Comparisons and trends get figures.
- **Self-review.** A simulated peer-review pass against four rubrics.
- **Hard gates.** Delivery is blocked on missing sections, malformed
  citations, or under-powered analysis.

### Is this related to `research-paper-writer` and `research-paper-engine`?

Yes — `research-paper` v2.0 is the **merged successor** of both. See
`docs/merge-report.md` for the full lineage. v2.0 is the recommended
path forward.

---

## Installation

### How do I install it?

```bash
npx @aniketkrs/research-paper install
```

Or manually:
```bash
git clone https://github.com/aniketkrs/research-paper.git
mv research-paper ~/.claude/skills/
```

See `INSTALLATION.md` and `publishing/install.md` for per-platform
details.

### Do I need Python?

No. The skill works with **just** filesystem read/write tools — it
emits Markdown tables and Mermaid diagrams as a fallback.

For real chart images and statistical validation:
```bash
pip install pandas numpy scipy statsmodels matplotlib seaborn pyyaml
```

### Do I need internet access?

No. The skill works offline. With network access, citations can be
verified against Crossref / arXiv (and retraction databases). Without,
they're marked `[UNVERIFIED — offline]` and surfaced in `Known-gaps.md`.

### Which agent runtimes does it support?

Claude Code, Claude Desktop, claude.ai (web), the Anthropic API/SDK,
OpenCode, Aider, Cline, Cursor agents, and any runtime that supports
Agent Skills + filesystem read/write tools.

---

## Activation

### How do I trigger the skill?

Either:
- Slash command: `/research "your topic" --depth standard --style ieee`
- Natural language: "Write a research paper on graph neural networks
  for fraud detection."

### Will it activate for blog posts or marketing copy?

No. The skill is explicitly excluded from those contexts. See
`manifest.json → activation.must_not_activate_for`.

### Can I scope it to a specific project?

Yes. Install with `--scope project`:
```bash
npx @aniketkrs/research-paper install --scope project
```

This installs into `./.claude/skills/` so the skill is available only
in that repository.

---

## Output

### What format does it produce?

Markdown by default, with full structure (YAML frontmatter, hierarchical
headings, tables, code blocks, Mermaid diagrams, and a properly
formatted reference list).

For PDF / DOCX / HTML: use Pandoc with the LaTeX preamble in
`assets/latex-templates/latex-preamble.tex`.

### Can I get LaTeX directly?

The skill emits Markdown that's Pandoc-ready. To produce LaTeX:

```bash
pandoc paper-final.md \
    --include-in-header=assets/latex-templates/latex-preamble.tex \
    --citeproc --bibliography=bibliography.yaml \
    --csl=ieee.csl \
    -o paper.tex
```

### Does it handle long papers (theses, surveys)?

Yes. For papers > 5,000 words, the skill switches to **multi-file
output** with each section in `sections/<NN>-<name>.md`. See
`long_context/multi-file-output.md`.

### What about images and figures?

If matplotlib is available, real PNG + SVG figures are generated. If
not, Mermaid diagrams and Markdown tables are produced. Either way,
the figure is referenced in the paper text and has a proper caption.

### What about tables?

Always Markdown tables in the paper. CSV exports go to `tables/`
for archival.

---

## Citations

### Which citation styles are supported?

Harvard, APA, IEEE, MLA, Chicago (author–date and notes-bibliography),
Nature numeric superscript, and arXiv-style numeric. See
`citation_engine/citation-styles.md`.

### Will the skill make up citations?

**No.** The skill is explicitly designed not to fabricate citations.
Unverifiable references are flagged `[UNVERIFIED]` and surfaced in
`Known-gaps.md`. Missing citations are flagged `[CITATION NEEDED]`
with a description of what's needed.

### Can I switch citation style after drafting?

Yes — re-run the citation pipeline:

```bash
python toolchains/format_bibliography.py \
    --bib bibliography.yaml \
    --paper paper-draft.md \
    --style apa \
    --out paper-cited.md
```

The bibliography is the single source of truth; styles are deterministic
projections.

### How does deduplication work?

- DOI match → duplicate.
- arXiv ID match → duplicate.
- Same first-author family + same year + same first-five-title-words
  → likely duplicate.

Duplicates are merged (more complete metadata wins). See
`citation_engine/deduplication.md`.

---

## Methodology

### What methodologies does it support?

Quantitative (RCT, quasi-experimental, correlational, cross-sectional,
longitudinal), qualitative (phenomenology, ethnography, grounded theory,
case study, narrative), mixed methods (convergent / sequential
explanatory / exploratory / embedded), systematic literature review
(PRISMA), design science / engineering, modeling / simulation, survey
research, meta-analysis.

See `methodology_engine/frameworks.md` for the decision tree.

### How does it handle statistical validation?

Every reported test gets:
- Test name and statistic
- Degrees of freedom
- p-value (with correction method if multiple tests)
- Effect size with 95% CI
- Sample size

Assumption checks are documented. Underpowered analyses are flagged
`[UNDERPOWERED]` with post-hoc power calculations.

See `methodology_engine/statistical-methods.md` and
`toolchains/statistical_validation.py`.

### Does it work for non-empirical (theoretical) papers?

Yes. For theoretical / conceptual / argumentative papers, the
methodology section becomes a "theoretical framework" or "conceptual
approach" subsection, and the analysis phase is replaced with
formal derivation.

---

## Visualizations

### What kinds of figures can it produce?

Bar / grouped-bar / horizontal-bar, line / multi-line, scatter,
histogram, violin, box plot, correlation heatmap, Sankey, flowchart,
mind map, treemap, sunburst, choropleth, point map, timeline, Gantt,
forest plot, comparative table, architecture diagram. See
`visualization_engine/decision-engine.md`.

### How does it pick the right chart?

A decision tree based on the section's communication goal:
- Compare categories → bar
- Trend over time → line
- Distribution → histogram / violin
- Relationship → scatter
- Correlation among many → heatmap
- Flow → Sankey
- Architecture → flowchart
- Geography → choropleth

See `visualization_engine/decision-engine.md` for the full tree.

### What about colorblind safety?

Default palette is **Okabe–Ito** (8 colors), colorblind-safe across
the major types of color vision deficiency. Sequential palette is
**viridis** (perceptually uniform). Diverging palette is **RdBu_r**
(zero-centered).

### Can I customize the chart style?

Yes — edit the defaults in `toolchains/generate_charts.py`. The
defaults section is documented inline.

---

## Quality

### What quality gates does the skill enforce?

- ≥ 1500 words
- ≥ 8 references
- ≥ 1 figure or table
- All required sections present
- Plain-English summary present
- Reproducibility statement present
- Future Work section present
- Academic-quality rubric mean ≥ 4 / 5
- Three reviewer personas all ≥ 3 / 5

See `quality_control/final-gate.md` for the full set.

### What if the paper doesn't pass?

Failures surface in `Known-gaps.md` with severity, recommended fix,
and affected artifacts. The user can either fix the issues or
explicitly waive them (recorded in the same file).

### Does it really simulate peer review?

Yes — three independent personas:
- **Methodologist** (validity, statistics, reproducibility)
- **Domain expert** (framing, novelty, prior work)
- **Reader** (clarity, narrative, accessibility)

Each scores against `rubrics/academic-quality.md` and produces 3–5
specific revision requests. The orchestrator aggregates and applies.

See `review_pipeline/three-personas.md`.

---

## Multi-agent

### When does the multi-agent mode activate?

Automatically for `--depth comprehensive` runs when the runtime
supports `agent-spawn`. Otherwise the orchestrator runs sequentially.

### What if my runtime doesn't support sub-agents?

The skill detects this and falls back to single-orchestrator
execution. The contracts and quality floors are still enforced;
they just run serially.

### Can I see the agent topology?

`instructions/multi-agent.md` and `orchestration/agents.md`. The
topology shows 8 specialist agents + 3 reviewer personas + the
orchestrator/publisher.

---

## Performance

### How long does a run take?

| Run                          | Estimate              |
| ---------------------------- | --------------------- |
| `--depth quick` paper         | 2–5 minutes           |
| `--depth standard` paper       | 5–15 minutes          |
| `--depth comprehensive` (single-agent) | 15–30 minutes |
| `--depth comprehensive` (multi-agent) | 8–18 minutes  |
| Literature review            | 10–25 minutes         |
| Validation-only              | 1–3 minutes           |

Times scale with model speed and source count.

### Can I run it in parallel for multiple papers?

Yes. Each paper has its own working directory, so multiple runs
are independent. The orchestrator detects the directory and uses it
as the state.

### What's the largest paper it can produce?

In multi-file mode, there's no fundamental upper limit. Theses of
40+ pages and surveys with 300+ references are routine.

---

## Reproducibility

### Is the output reproducible?

The toolchain scripts (citation pipeline, validators, statistical
checks) are deterministic — same inputs produce the same outputs.

Prose generation is model-dependent and not bit-exact, but the
**outputs the model produces** (structure, content, citations) are
constrained by the templates, prompts, and hard quality gates.

### Can I share the working directory with collaborators?

Yes. The directory is self-contained and includes:
- The paper itself
- The bibliography
- Every figure and table
- The validation reports
- The review reports
- The session state for resumability

### Can I commit it to version control?

Yes. The `.gitignore` in the working directory should exclude
`session-state.yaml` (run-specific) but include everything else.

---

## Troubleshooting

### "The skill never activates."

Check:
1. `SKILL.md` has valid YAML frontmatter (the runtime parses it).
2. The skill is in your runtime's skills directory.
3. The trigger pattern in your message matches `manifest.json →
   trigger.patterns` or `trigger.commands`.

### "Charts come out as Markdown only."

Install Python plotting deps:
```bash
pip install pandas matplotlib seaborn pyyaml
```

Then verify:
```bash
python toolchains/generate_charts.py --self-test
```

### "Citations are formatted weirdly."

Make sure exactly one `--style` is in use. Re-run the citation
pipeline with the desired style:

```bash
python toolchains/format_bibliography.py \
    --bib bibliography.yaml \
    --paper paper-draft.md \
    --style ieee \
    --out paper-cited.md
```

### "The model fabricated DOIs."

It shouldn't — the skill is explicitly designed not to. If you see
this, check that the references have `verification: unverified-offline`
or `unverified` set, and surface them in `Known-gaps.md`. File an
issue if the fabrication persists.

### "Output truncated mid-section."

You hit context pressure. Switch to multi-file output (the orchestrator
should auto-detect this for `--depth comprehensive`). Or split the
paper into chapters / sub-papers.

---

## Contributing

### How do I add a new venue / style / chart?

See `docs/extending.md`.

### How do I file a bug?

Open an issue at
[github.com/aniketkrs/research-paper/issues](https://github.com/aniketkrs/research-paper/issues).
Include:
- Your runtime (Claude Code, OpenCode, etc.)
- The slash command or prompt that triggered the issue
- The contents of `Known-gaps.md` if any
- The relevant `validation-report.md` if any

### License?

MIT. See `LICENSE`.
