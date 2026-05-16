# Changelog

All notable changes to **research-paper** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/) and the
project adheres to [Semantic Versioning](https://semver.org/).

## [2.1.0] — 2024-05-12

### Added — second skill: `get-research-paper`

The repo now ships **two complementary skills**:

| Skill | Purpose |
|---|---|
| `research-paper` (existing) | **Writes** research papers, lit reviews, theses, whitepapers, surveys, policy briefs |
| **`get-research-paper`** (new) | **Discovers** real existing papers — searches arXiv, Google Scholar, PubMed, Semantic Scholar; returns a curated reading list with verified DOIs |

### `get-research-paper` highlights

- **Slash commands:** `/get-research-paper`, `/get-paper`, `/find-paper`,
  `/find-papers`, `/fetch-paper`, `/papers-on`, `/scholar`.
- **Natural-language triggers:** "get research paper on [topic]",
  "find papers about [topic]", "what are the top papers on [topic]",
  "literature on [topic]", etc.
- **Multi-source search:** arXiv, Google Scholar, Semantic Scholar,
  PubMed/PMC, DBLP, ACM DL, IEEE Xplore, OpenReview — auto-routed by
  detected domain.
- **Real DOI verification** via Crossref + arXiv + Retraction Watch
  (when web tools available).
- **Three-dimensional ranking:** authority (0–4) + rigor (0–3) +
  recency-relevance (0–3) = total (0–10), with quality floor.
- **Diversity heuristics:** per-author cap, per-venue cap, ≥ 1 review,
  ≥ 1 foundational paper.
- **2–4 sentence summaries** per paper using
  problem → method → finding → significance structure.
- **Three audience registers:** academic / technical / general.
- **Working Python toolchain** (`toolchains/arxiv_search.py`) — direct
  arXiv API queries with polite ~3s pacing, parses with `feedparser`
  if available else stdlib `xml.etree`. **No required dependencies**;
  uses Python stdlib `urllib` if `requests` isn't installed.
- **Clean handoff to writer skill:** `--handoff` produces a
  `bibliography.yaml` consumable by `/research --bibliography <path>`.

### `get-research-paper` structure

```
skills/get-research-paper/
├── SKILL.md                            # Entry point
├── manifest.json                       # Metadata + triggers
├── instructions/core.md                # Operating principles
├── workflows/
│   ├── search.md                        # Master pipeline
│   ├── synthesis.md                     # Field briefing
│   └── handoff-to-writer.md             # Bridge to research-paper
├── sources/
│   ├── source-priority.md               # Per-domain decision tree
│   ├── arxiv.md                          # arXiv API guide
│   ├── google-scholar.md                  # Scholar via WebSearch
│   ├── semantic-scholar.md                # Semantic Scholar API
│   └── pubmed.md                         # PubMed / PMC via E-utilities
├── prompts/
│   ├── search-strategy.md                # Build the search plan
│   ├── summarization.md                  # 2-4 sentence summaries
│   └── ranking.md                        # 3-dim quality rubric
├── templates/
│   ├── reading-list.md                   # User-facing artifact
│   ├── paper-summary.md                  # Per-paper block
│   └── briefing.md                       # 1-3 paragraph synthesis
├── schemas/
│   └── paper-result.json                 # Output schema
├── toolchains/
│   └── arxiv_search.py                   # Direct arXiv API tool
└── examples/
    └── sample-results.md                 # End-to-end example output
```

### Updated — root README

- Now leads with the dual-skill table.
- New "End-to-end workflow" example showing how the two skills chain.
- `--skill <name>` install option for installing one skill only.

### Updated — `research-paper`

- Version bumped to 2.1.0 to match repo version.
- No functional changes; the writer skill is unchanged from v2.0.2.

### Updated — tests

- 79/79 tests pass (was 54).
- New tests cover `get-research-paper` structure, manifest, schema,
  and `arxiv_search.py` self-test.

### Verified

- Live arXiv API call returns real papers
  (e.g., "graph neural networks" → real cite key `joshi_2025_transformers`).
- `npx skills add aniketkrs/research-paper --list` will detect both
  skills.
- Direct installer (`bin/install.js`) covers both skills.

---

## [2.0.2] — 2024-05-12

### Restructured for skills.sh registry indexing

User feedback pointed out that public skill registries (skills.sh) index
skills from the `<repo>/skills/<name>/` convention used by multi-skill
collections. After cross-checking the live `npx skills find` output:

- Repos like `vercel-labs/agent-skills`, `firecrawl/firecrawl-workflows`,
  `seabbs/skills`, etc. are all indexed because they use this layout.
- My v2.0.0 / v2.0.1 layout (skill at root) worked for direct
  `npx skills add aniketkrs/research-paper` but was NOT indexed by
  `npx skills find`.

This release migrates to the registry-indexable layout:

```
research-paper/                  ← repo root
├── README.md, LICENSE, CHANGELOG.md, INSTALLATION.md, package.json
├── bin/, tests/, docs/          ← repo-level
└── skills/
    └── research-paper/           ← actual skill content
        ├── SKILL.md, manifest.json
        ├── instructions/, orchestration/, workflows/, prompts/
        ├── citation_engine/, visualization_engine/, methodology_engine/
        ├── templates/, validators/, schemas/, rubrics/
        ├── quality_control/, long_context/, memory/
        ├── academic_formats/, style_guides/, review_pipeline/
        ├── toolchains/, assets/, publishing/
        ├── examples/, datasets/
```

### Backward compatibility

- `npx skills add aniketkrs/research-paper` continues to work; the tool
  detects the new layout and installs the skill identically.
- The direct installer (`bin/install.js`) now reads from
  `<repo>/skills/research-paper/` and installs into
  `.agents/skills/research-paper/` (unchanged target).
- `npm`-based install via `npx -y github:aniketkrs/research-paper install`
  continues to work.

### Test suite

- Updated to verify the new dual-level structure (repo-level files at
  root, skill content under `skills/research-paper/`).
- 54/54 tests pass.

---

## [2.0.1] — 2024-05-12

### Changed (de-vendor-locking)

- **Description and SKILL.md** rewritten to be runtime-neutral. The
  skill is no longer described as a "Claude Agent Skill" — it's an
  "agent skill" that works with **any** of 50+ supported runtimes
  (Claude Code, OpenCode, Cursor, Cline, Codex, Aider, Amp,
  Antigravity, AiderDesk, Augment, IBM Bob, etc.).
- **Direct installer** (`bin/install.js`) now defaults to the
  runtime-neutral `.agents/skills/` directory used by the official
  `npx skills` CLI, instead of `~/.claude/skills/`. Environment override
  variable renamed `CLAUDE_SKILLS_DIR` → `AGENT_SKILLS_DIR`.
- **README and INSTALLATION** lead with the official `npx skills add`
  CLI as the recommended install path. Per-runtime manual install
  instructions kept as fallbacks.

### Verified

- `npx skills add aniketkrs/research-paper` end-to-end (clones, detects
  agents, installs into `.agents/skills/research-paper/`, symlinks to
  per-runtime locations for 50+ agents).
- `npx skills find research-paper` returns the skill metadata.
- Direct installer (`npx -y github:aniketkrs/research-paper install`)
  works as a fallback when `npx skills` isn't available.

### Why

User feedback flagged Claude-specific branding (description, install
paths, language). Investigation against the live `npx skills` CLI
confirmed:

1. The repo structure was **already correct** — `npx skills` detected
   the skill at root via `SKILL.md` (no `skills/<name>/skill.md`
   restructuring needed).
2. But the skill description, the README, and the direct installer
   were unnecessarily Claude-flavored. Fixed in this release.

The `npx skills` CLI is the runtime-neutral standard; this release
aligns the skill's documentation and direct installer with that
convention.

---

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
