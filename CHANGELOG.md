# Changelog

All notable changes to **research-paper** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/) and the
project adheres to [Semantic Versioning](https://semver.org/).

## [2.0.0] — 2024-05-12

### Major refactor and merge

This is a major version. v2.0 merges, refactors, and upgrades two
predecessor skills into a single enterprise-grade system:

- **From `research-paper-writer`** (previously v1.0): the spine —
  comprehensive references, 10 paper templates, all 9 prompts, 4
  rubrics, 5 venue style guides, 7 working Python toolchain scripts,
  3 end-to-end example papers, deterministic citation pipeline.
- **From `research-paper-engine`** (previously v1.0): the architecture —
  modular engines (citation_engine, methodology_engine,
  visualization_engine), explicit slash-command activation, multi-agent
  orchestration model, source credibility scoring, citation
  deduplication, peer-review pipeline stages, sample dataset.

See **[`docs/merge-report.md`](docs/merge-report.md)** for the full
analysis.

### Added (genuinely new in v2.0)

- **Slash command activation**: `/research`, `/paper`,
  `/literature-review`, `/whitepaper`, `/thesis`, `/survey`, `/policy`.
- **Multi-agent topology** with explicit per-agent read/write contracts
  (`instructions/multi-agent.md`). 8 specialist agents + 3 reviewer
  personas + orchestrator/publisher.
- **Routing engine** (`orchestration/routing.md`) for format / style /
  depth / execution-mode selection.
- **Failure-handling matrix** (`orchestration/failure-handling.md`)
  for every phase.
- **Long-context discipline**: `long_context/strategy.md`, `chunking.md`,
  `multi-file-output.md`. Resumable runs via `session-state.yaml`.
- **Memory protocols** (`memory/`): citation memory, methodology memory,
  session state.
- **Quality control**: `final-gate.md`, `known-gaps-protocol.md`.
- **Final gate**: hard quality gates that block delivery on serious
  problems and surface waivable issues to `Known-gaps.md`.
- **Test suite**: `tests/test-runner.js` exercises structure, schemas,
  Python toolchain self-tests, and the citation pipeline against
  fixtures.
- **npm packaging**: `package.json` + `bin/install.js`. Installable via
  `npx @aniketkrs/research-paper install`.
- **Publishing docs** (`publishing/install.md`) for Claude Code,
  Claude Desktop, claude.ai, Anthropic API/SDK, OpenCode, etc.
- **Extended docs**: `docs/architecture.md`, `docs/merge-report.md`,
  `docs/extending.md`, `docs/design-decisions.md`, `docs/faq.md`,
  `docs/best-practices.md`.
- **`Known-gaps.md` protocol**: every unresolved issue is surfaced
  with severity, recommended fix, and affected artifacts. Never
  silent.

### Reorganized (modular layout)

- Citation logic consolidated under `citation_engine/` (was split
  across `references/citation-styles.md`, `references/source-evaluation.md`,
  and `scripts/format_bibliography.py`).
- Visualization logic consolidated under `visualization_engine/`
  (was in `references/visualization-guide.md` only).
- Methodology logic consolidated under `methodology_engine/`
  (was in `references/methodology-guide.md` and `references/statistical-methods.md`).
- Orchestration spine moved to `orchestration/pipeline.md`
  (was `workflows/research-orchestration.md`).
- Validators moved to a dedicated `validators/` folder
  (was inline in workflows).
- Per-venue style guides moved to `academic_formats/`
  (was `style_guides/`).
- Python helpers renamed to `toolchains/` (was `scripts/`).
- Quality control split between `quality_control/` (the gates) and
  `rubrics/` (the scoring rubrics).
- Single-source-of-truth manifest with `quality_gates`, `memory_strategy`,
  `trigger`, and full file inventory.

### Improved

- **SKILL.md** is significantly tighter while retaining the entire
  navigation surface — pure progressive disclosure.
- **Manifest** now declares slash commands, output formats, paper
  types, citation styles, capabilities, dependencies, and quality
  gates explicitly (was implicit in v1).
- **Citation pipeline** is now deterministic across all 7 styles
  (Harvard, APA, IEEE, MLA, Chicago author–date, Nature, arXiv-numeric)
  with a Python implementation (B had no working scripts).
- **Visualization pipeline** combines A's Python rendering with B's
  decision-tree pseudocode and B's chart-template library.
- **Methodology pipeline** combines A's exhaustive blueprint coverage
  with B's framework decision tree and B's statistical-test selection
  matrix.
- **Review pipeline** combines A's three-persona simulated review
  with B's editor + reviewer-1 + reviewer-2 staged process.
- **Source credibility scoring** (from B) is now first-class in
  `citation_engine/credibility-scoring.md` and feeds the citation-quality
  rubric.
- **Citation deduplication** (from B) is now first-class in
  `citation_engine/deduplication.md` and integrated with the citation
  pipeline.
- **Examples** include both A's three end-to-end papers AND B's
  24-KB sample paper excerpt, plus B's sample dataset.

### Removed (intentionally)

- Duplicated citation-style content (was in both A's `references/citation-styles.md`
  and B's `citation_engine/styles/`). Single source of truth in v2:
  `citation_engine/citation-styles.md` + `citation_engine/styles/<style>.md`
  per-style detail.
- Duplicated visualization guide (was in both repos). Consolidated to
  `visualization_engine/visualization-guide.md` + `decision-engine.md`.
- Duplicated methodology content. Consolidated to `methodology_engine/`.
- Several broken / redundant intermediate files (e.g., A's
  `references/literature-review-guide.md` overlap with B's
  `workflows/literature_review.md` — now `workflows/literature-review.md`
  is the playbook and `workflows/literature-review-guide.md` is the deep
  reference).

### Migration notes

- For users of `research-paper-writer` v1: the install path is the
  same (`~/.claude/skills/research-paper-writer`), but the new package
  is `research-paper` (drop the `-writer` suffix). Slash commands
  (`/research`, etc.) are the recommended invocation in v2.
- For users of `research-paper-engine` v1: the install path is the
  same (`~/.claude/skills/research-paper-engine`), but the new package
  is `research-paper`. The previous flat-file layout has been
  reorganized — see the new folder map in `README.md`.
- Both predecessors are retained as historical reference; v2.0 is
  the single recommended path going forward.

---

## Predecessors

The full v1.0 changelogs are at:
- https://github.com/aniketkrs/research-paper-writer/blob/main/CHANGELOG.md
- (research-paper-engine — see commit history)
