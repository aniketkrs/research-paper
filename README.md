# research-paper

> **Enterprise-grade Claude Agent Skill for autonomous, publication-ready
> research paper generation.** Full papers, literature reviews, theses,
> whitepapers, surveys, and policy briefs — with rigorous methodology,
> statistical validation, multi-style citations, and rich visualizations.

This skill is the merged, refactored, and upgraded successor to
[`research-paper-writer`](https://github.com/aniketkrs/research-paper-writer)
and [`research-paper-engine`](https://github.com/aniketkrs/research-paper-engine).
It takes the strongest pieces of each and adds production-grade
multi-agent orchestration, long-context handling, persistent memory,
quality gates, and an installable npm package.

---

## Quick install

### One-liner

```bash
npx @aniketkrs/research-paper install
```

This drops the skill into your active skills directory
(`~/.claude/skills/` for Claude Code, `~/.config/opencode/skills/` for
OpenCode, etc.). Restart your session and the skill activates on
academic-writing requests.

### Pin a version

```bash
npx @aniketkrs/research-paper@2.0.0 install
```

### Project-scope install

```bash
npx @aniketkrs/research-paper install --scope project
```

### Manual install

```bash
git clone https://github.com/aniketkrs/research-paper.git
mkdir -p ~/.claude/skills
mv research-paper ~/.claude/skills/
```

For per-platform instructions (Claude Desktop, claude.ai, the Anthropic
API/SDK, OpenCode, Aider, Cursor, Cline), see
**[`publishing/install.md`](publishing/install.md)**.

---

## What you get

The instant the skill is installed, requests like these activate it:

- `/research "Retrieval-augmented code review" --style ieee --depth comprehensive`
- `/literature-review "Transformer architectures 2017–2024" --systematic --sources 40`
- `/whitepaper "Vector databases for RAG" --audience technical --length 15-pages`
- `/thesis "Chapter 3: Methodology" --style harvard`
- `/policy "Open-source AI governance" --depth standard`
- "Write a research paper on graph neural networks for fraud detection."
- "Format this draft as an IEEE conference paper with proper citations."
- "Analyze this CSV and produce an academic-style findings report."
- "Peer-review my thesis chapter and tighten the methodology."

What it produces:

- **Full papers** in arXiv / IEEE / ACM / Nature / Harvard styles plus
  literature reviews, theses, whitepapers, survey papers, policy briefs.
- **Rigorous methodology** with sample-size justification, validity
  threats, and reproducibility statements.
- **Statistical validation** with effect sizes, confidence intervals,
  multiple-comparison correction, and assumption checks.
- **Real visualizations** (charts, tables, heatmaps, flowcharts, PRISMA
  diagrams, forest plots, geographic maps).
- **Citation engine** for Harvard, APA, IEEE, MLA, Chicago (author–date
  and notes-bibliography), Nature numeric, and arXiv-style — switchable
  with one flag.
- **Plain-English summary** alongside every paper for non-specialist
  readers.
- **Three-persona simulated peer review** (methodologist + domain
  expert + reader) with consolidated revision report.
- **Publication checklist** as the final gate.
- **Known gaps block** that surfaces every unresolved issue.

What it does **not** do:

- It does not invent citations, DOIs, page numbers, or coauthors.
  Unverifiable sources are flagged `[UNVERIFIED]` and surfaced in
  `Known-gaps.md` — never silently fabricated.

---

## What's new in v2.0.0

This is a major refactor. The skill is now built around four explicit
architectural pillars:

### 1. Multi-agent orchestration

For comprehensive runs, the orchestrator dispatches specialist
sub-agents (Researcher, Methodologist, Analyst, Visualizer, Writer,
Citator, Validator, three Reviewer personas, Publisher) with strict
read / write contracts that communicate only through the working
directory. See **[`instructions/multi-agent.md`](instructions/multi-agent.md)**.

### 2. Modular engines

Three first-class engines:

- **Citation engine** (`citation_engine/`) — styles, deduplication,
  bibliography generation, source credibility scoring.
- **Visualization engine** (`visualization_engine/`) — decision tree,
  chart templates, caption generator, accessibility defaults.
- **Methodology engine** (`methodology_engine/`) — frameworks,
  sampling, statistical tests, full reporting templates.

### 3. Long-context discipline

Production-ready handling of papers that exceed the model's working
context window:
- Persist every artifact to disk (paper-spec, outline, bibliography,
  methodology, analysis, sections, validation, review).
- Read only what's needed for the current step.
- Resumable runs with a `session-state.yaml` ledger.
- Multi-file output for long papers.

See **[`long_context/`](long_context/)** and **[`memory/`](memory/)**.

### 4. Quality gates and known-gaps protocol

The skill never fails silently. A final gate
(`quality_control/final-gate.md`) blocks delivery on hard-quality
violations. Anything that can't be auto-resolved surfaces in
**`Known-gaps.md`** with severity, recommended fix, and affected
artifacts.

---

## Folder structure

```
research-paper/
├── SKILL.md                          # Entry point (Claude reads this)
├── manifest.json                     # Skill manifest / metadata
├── package.json                      # npm packaging for npx install
├── README.md                         # This file
├── INSTALLATION.md                   # Per-platform install
├── CHANGELOG.md                      # Versioned changes
├── LICENSE                           # MIT
├── bin/                              # npx installer
│   └── install.js
├── instructions/                     # Core operating instructions
│   ├── core.md
│   ├── activation.md
│   ├── multi-agent.md
│   └── voice-and-tone.md
├── orchestration/                    # The brain
│   ├── pipeline.md                   # The 11-phase master pipeline
│   ├── agents.md                     # Sub-agent topology summary
│   ├── routing.md                    # Format / style / depth routing
│   └── failure-handling.md           # Per-phase recovery matrix
├── workflows/                        # Phase-specific playbooks
│   ├── full-paper.md
│   ├── literature-review.md
│   ├── data-analysis-pipeline.md
│   ├── visual-generation-pipeline.md
│   ├── citation-pipeline.md
│   ├── validation-pipeline.md
│   └── ... (more)
├── prompts/                          # Internal sub-prompts
│   ├── research-planning.md
│   ├── literature-search.md
│   ├── methodology-design.md
│   ├── data-analysis.md
│   ├── visualization-planning.md
│   ├── writing-prompts.md
│   ├── citation-prompts.md
│   ├── review-prompts.md
│   └── simplification-prompts.md
├── citation_engine/                  # First-class citation system
│   ├── citation-styles.md
│   ├── bibliography-generation.md
│   ├── deduplication.md
│   ├── credibility-scoring.md
│   ├── source-evaluation.md
│   └── styles/
│       ├── harvard.md, apa.md, ieee.md, mla-chicago.md
├── visualization_engine/             # Chart-selection brain
│   ├── decision-engine.md
│   ├── chart-templates.md            # Python templates
│   ├── caption-generator.md
│   └── visualization-guide.md
├── methodology_engine/               # Research design + stats
│   ├── frameworks.md
│   ├── sampling.md
│   ├── statistical-tests.md
│   ├── methodology-guide.md
│   └── statistical-methods.md
├── academic_formats/                 # Per-venue style notes
│   ├── overview.md
│   ├── arxiv.md, ieee.md, acm.md, nature.md, harvard.md
├── templates/                        # 10 paper templates
│   ├── arxiv-paper.md
│   ├── ieee-paper.md
│   ├── acm-paper.md
│   ├── nature-paper.md
│   ├── harvard-paper.md
│   ├── literature-review.md
│   ├── thesis-chapter.md
│   ├── whitepaper.md
│   ├── survey-paper.md
│   └── policy-paper.md
├── validators/                       # Mechanical validators
│   ├── citation-validator.md
│   ├── methodology-validator.md
│   └── quality-rubric.md
├── review_pipeline/                  # Simulated peer review
│   ├── three-personas.md
│   └── peer-review.md
├── rubrics/                          # Quality rubrics
│   ├── academic-quality.md
│   ├── methodology-rigor.md
│   ├── citation-quality.md
│   ├── visual-quality.md
│   └── publication-readiness.md
├── quality_control/                  # Hard-quality gates
│   ├── publication-checklist.md
│   ├── known-gaps-protocol.md
│   └── final-gate.md
├── long_context/                     # Long-paper handling
│   ├── strategy.md
│   ├── chunking.md
│   └── multi-file-output.md
├── memory/                           # Persistent memory protocols
│   ├── citation-memory.md
│   ├── methodology-memory.md
│   └── session-state.md
├── style_guides/                     # Writing style + voice
│   ├── academic-tone.md
│   └── writing-style-guide.md
├── schemas/                          # JSON Schemas
│   ├── paper-schema.json
│   ├── citation-schema.json
│   ├── citation-database-schema.json
│   ├── figure-schema.json
│   ├── table-schema.json
│   └── dataset-schema.json
├── toolchains/                       # Working Python helpers
│   ├── format_bibliography.py        # Citation pipeline (deterministic)
│   ├── validate_citations.py         # Citation validator
│   ├── extract_references.py         # Orphan / missing detector
│   ├── analyze_data.py               # Data-analysis pipeline
│   ├── generate_charts.py            # Chart renderer (matplotlib + Mermaid fallback)
│   ├── statistical_validation.py     # Statistical-claim auditor
│   └── generate_paper.py             # Project bootstrapper
├── datasets/                         # Sample datasets
│   └── sample-analysis-data.csv
├── examples/                         # End-to-end sample papers
│   ├── sample-paper-arxiv.md
│   ├── sample-literature-review.md
│   ├── sample-data-analysis.md
│   ├── sample-paper-excerpt.md
│   ├── bibliography.example.yaml
│   └── sample-visualizations/
├── publishing/                       # Per-platform install docs
│   └── install.md
├── docs/                             # Extended documentation
│   ├── architecture.md
│   ├── merge-report.md               # How v2.0 was built
│   ├── extending.md
│   ├── design-decisions.md
│   ├── faq.md
│   └── best-practices.md
├── tests/                            # Lightweight test runner
│   ├── README.md
│   ├── test-runner.js
│   ├── fixtures/
│   └── golden-outputs/
└── assets/                           # LaTeX / chart / diagram helpers
    └── latex-templates/
        └── latex-preamble.tex
```

---

## Activation

The skill activates on **slash commands** (preferred):

| Command                     | What it does                              |
| --------------------------- | ----------------------------------------- |
| `/research <topic>`          | Full empirical research paper             |
| `/paper <topic>`             | Same as `/research`                       |
| `/literature-review <topic>` | Systematic / scoping / narrative review   |
| `/whitepaper <topic>`        | Industry / technical whitepaper            |
| `/thesis <topic>`            | Thesis / dissertation chapter             |
| `/survey <topic>`            | State-of-the-art / survey paper            |
| `/policy <topic>`            | Policy brief or full policy paper          |

…or on **natural-language requests** matching academic-writing intents
("write a research paper on …", "do a literature review on …",
"format this as IEEE …", "analyze this CSV and write up findings").

It does **not** activate for blog posts, tweets, marketing copy, or
single-paragraph answers.

---

## Quality gates

A paper is **not done** until it passes:

- ≥ 1500 words (configurable in `manifest.json`)
- ≥ 8 references with DOIs / URLs
- ≥ 1 figure or table
- All `must_include_sections` present (abstract, intro, methodology,
  results, discussion, limitations, conclusion, references)
- `must_include_blocks`: plain_english_summary, reproducibility_statement,
  future_work
- `rubrics/academic-quality.md` mean score ≥ 4 / 5
- All three reviewer personas score ≥ 3.0
- All `[CITATION NEEDED]` and `[UNVERIFIED]` flags resolved or surfaced
  in `Known-gaps.md`

Failures surface in `Known-gaps.md` — never silently swallowed.

---

## Optional Python toolchain

The skill emits Markdown tables + Mermaid diagrams by default (works
everywhere). To enable real chart images and statistical validation:

```bash
python -m pip install --upgrade \
    pandas numpy scipy statsmodels \
    matplotlib seaborn plotly scikit-learn pyyaml
```

Verify:

```bash
python toolchains/generate_charts.py --self-test
python toolchains/analyze_data.py --self-test
node tests/test-runner.js
```

---

## Try it

After installing, in your Claude / agent session:

> `/research "Graph neural networks for fraud detection" --style ieee --depth comprehensive`

> `/literature-review "Retrieval-augmented generation in software engineering" --systematic --sources 50`

> "Analyze this CSV and write a findings report. [data.csv attached]"

You'll see the orchestrator walk through plan → research → analyze →
visualize → draft → cite → validate → review → ship and produce a
complete, publication-grade artifact.

---

## Extending

The skill is modular:

- **Add a venue:** drop a template in `templates/<venue>.md`, add
  style notes in `academic_formats/<venue>.md`, register the trigger
  in `manifest.json` and `SKILL.md §4`.
- **Add a citation style:** extend `citation_engine/citation-styles.md`
  and `toolchains/format_bibliography.py`.
- **Add a chart type:** extend `visualization_engine/decision-engine.md`
  and `toolchains/generate_charts.py`.
- **Add a sub-agent:** extend `instructions/multi-agent.md` with the
  new agent's contract.

See **[`docs/extending.md`](docs/extending.md)** for the full guide.

---

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Issues and PRs welcome at
[github.com/aniketkrs/research-paper](https://github.com/aniketkrs/research-paper).

The merge story (how v2.0 was built from `research-paper-writer` and
`research-paper-engine`) is in
**[`docs/merge-report.md`](docs/merge-report.md)**.
