# research-paper

> **Enterprise-grade autonomous research paper generation skill for AI
> coding agents.** Full papers, literature reviews, theses, whitepapers,
> surveys, and policy briefs — with rigorous methodology, statistical
> validation, multi-style citations, and rich visualizations.

Runtime-neutral. Works with **Claude Code, OpenCode, Cursor, Cline,
Codex, Aider, Amp, Antigravity, AiderDesk, Augment, IBM Bob,** and 50+
other agents via the `npx skills` installer.

This skill is the merged, refactored, and upgraded successor to
[`research-paper-writer`](https://github.com/aniketkrs/research-paper-writer)
and [`research-paper-engine`](https://github.com/aniketkrs/research-paper-engine).
It takes the strongest pieces of each and adds production-grade
multi-agent orchestration, long-context handling, persistent memory,
quality gates, and deterministic citation tooling.

---

## Quick install

### One-liner (recommended)

```bash
npx skills add aniketkrs/research-paper
```

This is the official **runtime-neutral** install path. The `npx skills`
CLI auto-detects your active agents (Claude Code, OpenCode, Cursor,
Cline, Codex, Aider, etc.) and installs the skill into the universal
`.agents/skills/research-paper/` directory used by all of them.

To verify the install:

```bash
npx skills list
npx skills find research-paper
```

### Pin to a version

```bash
npx skills add aniketkrs/research-paper#v2.0.1
```

### Install globally (user-scope) instead of project-scope

```bash
npx skills add aniketkrs/research-paper --global
```

### Install to a specific agent only

```bash
npx skills add aniketkrs/research-paper --agent claude-code
npx skills add aniketkrs/research-paper --agent cursor
npx skills add aniketkrs/research-paper --agent '*'    # all agents
```

### Manual install

```bash
git clone https://github.com/aniketkrs/research-paper.git
mkdir -p .agents/skills
mv research-paper .agents/skills/
```

For per-platform manual install instructions, see
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

## Architectural pillars

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
├── SKILL.md                          # Entry point (the agent reads this)
├── manifest.json                     # Skill manifest / metadata
├── package.json                      # npm metadata (for direct npx install)
├── README.md                         # This file
├── INSTALLATION.md                   # Per-platform install
├── CHANGELOG.md                      # Versioned changes
├── LICENSE                           # MIT
├── bin/                              # Direct npx installer (alternative path)
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
├── prompts/                          # Internal sub-prompts (×9)
├── citation_engine/                  # First-class citation system
├── visualization_engine/             # Chart-selection brain
├── methodology_engine/               # Research design + stats
├── academic_formats/                 # Per-venue style notes (×5)
├── templates/                        # 10 paper templates
├── validators/                       # Mechanical validators
├── review_pipeline/                  # Simulated peer review
├── rubrics/                          # Quality rubrics (×5)
├── quality_control/                  # Hard-quality gates
├── long_context/                     # Long-paper handling
├── memory/                           # Persistent memory protocols
├── style_guides/                     # Writing voice + tone
├── schemas/                          # JSON Schemas (×6)
├── toolchains/                       # Working Python helpers (×7)
├── datasets/                         # Sample datasets
├── examples/                         # End-to-end sample papers
├── publishing/                       # Per-platform install docs
├── docs/                             # Architecture, merge-report, FAQ, etc.
├── tests/                            # Lightweight test runner (53 assertions)
└── assets/                           # LaTeX / chart / diagram helpers
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

…or on **natural-language requests** matching academic-writing intents.

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

After installing, in your agent session:

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

## Compatibility

This is a runtime-neutral agent skill. The `npx skills` installer
detects and installs into 50+ agent runtimes including:

| Universal agents | Symlink-supported agents |
|---|---|
| Amp, Antigravity, Cline, Codex, Cursor (+10 more) | AiderDesk, Augment, IBM Bob, Claude Code, OpenCode (+35 more) |

Run `npx skills add aniketkrs/research-paper --list` to see the full
list of agents detected on your machine.

---

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Issues and PRs welcome at
[github.com/aniketkrs/research-paper](https://github.com/aniketkrs/research-paper).

The merge story (how v2.0 was built from `research-paper-writer` and
`research-paper-engine`) is in
**[`docs/merge-report.md`](docs/merge-report.md)**.
