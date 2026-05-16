# Changelog

All notable changes to **research-paper** are documented here.
Format follows [Keep a Changelog](https://keepachangelog.com/) and the
project adheres to [Semantic Versioning](https://semver.org/).

## [2.4.0] — 2024-05-12

### Fixed — date freshness (no more silent training-cutoff drift)

The agent was anchoring papers to its training-data cutoff (~2022 era)
instead of using current dates. Fix:

- **New `instructions/freshness.md`** in all three skills with the
  full date-anchoring protocol.
- **Phase 0 added to `research-paper/orchestration/pipeline.md`** —
  "Determine TODAY's date" runs BEFORE planning, search, or writing.
- **Phase 0 added to `get-research-paper/workflows/search.md`** —
  search plan can't be built before today's date is resolved.
- Both Phase 0 phases run `date -u +%Y-%m-%d` (or check runtime
  context, or ask) — never silently default to the training-cutoff
  date.
- **Year-range flags are now relative to today.** `--years last-3`
  resolves to `(today.year - 3, today.year)`, not to a hardcoded
  range.
- **Default `--years` for `get-research-paper` changed to `last-3`**
  (was `last-10` previously, which let too much old data in).
- **Two-pass search** (`get-research-paper`): pass 1 = recent
  (`last-3`), pass 2 = foundational (uncapped) — gets both state of
  the art AND canonical anchors.
- **Recency boost** in ranking: papers in the last 12 months get +1
  to the recency score.
- Operating principles in all three SKILL.md files now lead with
  "Anchor to TODAY's date FIRST" as principle 0.
- Validators flag papers that rely only on > 5-year-old sources
  (severity: medium).
- Outputs now declare freshness in the verification trail:
  ```
  Source tier: live-fetch / cache / bundled-corpus / model-knowledge
  Today's date: <YYYY-MM-DD>
  Latest cited paper: <YYYY-MM>
  Freshness: fresh / dated / very-dated
  ```

### Fixed — installer no longer prompts for which skills to install

`npx skills add aniketkrs/research-paper` was asking which of the
three skills to install before proceeding, which made the install
slower than necessary. Fix:

- **README and INSTALLATION** now lead with the non-interactive
  command:
  ```
  npx skills add aniketkrs/research-paper --yes --skill '*'
  ```
- **`bin/install.js` (direct installer) auto-discovers all skills
  under `skills/` and installs them in one shot by default.** No
  more hardcoded single-skill behavior.
- New `--skill <name>` flag for the direct installer when only one
  is wanted.
- New `discoverSkills()` function reads `skills/<name>/SKILL.md`
  to enumerate skills at runtime.
- `--help` output now lists discovered skills with their versions.

### Updated tests

- 123/123 tests pass (was 116).
- New tests:
  - `freshness.md` exists in all 3 skills (registered in manifests
    and present on disk).
  - `research-paper/orchestration/pipeline.md` has Phase 0 with
    "today's date" wording.
  - `get-research-paper/workflows/search.md` has Phase 0 with
    "today's date" wording.
  - `bin/install.js` auto-discovers skills (no hardcoded single
    skill name).

### Versioning

- Repo: 2.3.0 → 2.4.0
- skills/research-paper: 2.3.0 → 2.4.0
- skills/get-research-paper: 1.0.0 → 1.1.0
- skills/read-research-paper: 1.1.0 → 1.2.0

---

## [2.3.0] — 2024-05-12

### Added — multi-format file I/O

The skills can now **read** any of these as input and **write** any
of these as output, with graceful degradation when libraries aren't
installed:

#### Read (in `read-research-paper`)

| Format | Extensions | Always available? |
|---|---|---|
| Markdown, plain text, JSON | `.md`, `.markdown`, `.txt`, `.json` | yes |
| LaTeX | `.tex`, `.latex` | yes (regex de-LaTeX) |
| HTML | `.html`, `.htm` | yes (regex fallback) |
| CSV / TSV | `.csv`, `.tsv` | yes (basic via stdlib) |
| RTF | `.rtf` | yes (regex fallback) |
| **PDF** | `.pdf` | install `pdfplumber` or `pypdf` |
| **DOCX** | `.docx` | install `python-docx` |
| **PPTX** | `.pptx` | install `python-pptx` |
| **XLSX** | `.xlsx`, `.xls` | install `pandas` + `openpyxl` |
| **EPUB** | `.epub` | install `ebooklib` |
| **Images** (OCR) | `.png`, `.jpg`, `.tiff`, `.bmp` | install `pytesseract` + Tesseract |

#### Write (in `research-paper`)

| Format | Extension | Renderer |
|---|---|---|
| Markdown | `.md` | native (always) |
| HTML | `.html` | Pandoc |
| DOCX | `.docx` | Pandoc |
| LaTeX | `.tex` | Pandoc |
| **PDF** | `.pdf` | Pandoc + LaTeX engine |
| RTF | `.rtf` | Pandoc |
| EPUB | `.epub` | Pandoc |
| ODT | `.odt` | Pandoc |
| PPTX | `.pptx` | Pandoc |

### New toolchains

- **`read-research-paper/toolchains/read_any_file.py`** — universal
  file reader with format detection, graceful degradation, self-test.
- **`research-paper/toolchains/convert_output.py`** — universal output
  converter wrapping Pandoc, with explicit "install X" messages
  when dependencies are missing.

### New documentation

- **`read-research-paper/sources/file-formats.md`** — comprehensive
  reference for both read and write formats, install commands per OS,
  and self-test instructions.

### Updated SKILL.md files

- `read-research-paper/SKILL.md` now lists all 17+ supported input
  formats with one-line install commands.
- `research-paper/SKILL.md` now documents the output-conversion
  toolchain with target formats, renderers, and `--output paper.pdf`
  invocation.

### Updated manifests

- `read-research-paper/manifest.json` — `supported_input_formats`
  field added with all 17+ extensions; `python_dependencies.recommended`
  expanded to cover all readers.
- `research-paper/manifest.json` — `output_formats` expanded from 4
  to 11 formats including PDF/DOCX/EPUB/ODT/PPTX.

### Updated tests

- 116/116 tests pass (was 110).
- New tests cover `read_any_file.py --self-test`, `--list-formats`
  (verifies pdf/docx/pptx/xlsx/tex/html/epub all listed),
  `convert_output.py --self-test`, and `--list-formats`.

### Updated README

- Complete rewrite. Removed the "merged successor of …" lineage
  passage.
- New layout optimized for readability: hero install command at the
  top, three-skill table, end-to-end workflow diagram, supported file
  formats prominently displayed, troubleshooting matrix.
- Added shields/badges (license, skill count, test count).
- Quick-start section with three concrete examples.
- Compatibility matrix listing 50+ supported runtimes.
- Versioning history table.

### Verified

- Live multi-format reads tested: `.md` (with structure), `.json`
  (parsed), `.tex` (de-LaTeX'd cleanly with `[CITE]` placeholders),
  `.html` (regex fallback works without bs4).
- All 3 skills detected by `npx skills add aniketkrs/research-paper --list`.
- Both new toolchain self-tests pass on Windows (cp1252 console-safe).

### Versioning

- Repo: 2.2.0 → 2.3.0
- skills/research-paper: 2.2.0 → 2.3.0 (added `convert_output.py`)
- skills/get-research-paper: 1.0.0 (no changes)
- skills/read-research-paper: 1.0.0 → 1.1.0 (added `read_any_file.py`,
  `sources/file-formats.md`, expanded format support)

---

## [2.2.0] — 2024-05-12

### Added — third skill: `read-research-paper`

The repo now ships **three complementary skills**:

| Skill | Purpose |
|---|---|
| `research-paper` | **Writes** new papers |
| `get-research-paper` | **Finds** real existing papers on a topic |
| **`read-research-paper`** (new) | **Renders** ANY paper (URL/arXiv/DOI/PDF) as a visual reading experience |

### `read-research-paper` highlights

- **Slash commands:** `/read-research-paper`, `/read-paper`,
  `/explain-paper`, `/visualize-paper`, `/tldr-paper`.
- **Natural-language triggers:** "read this research paper [URL]",
  "explain this paper [URL]", "make this paper visual [URL]",
  "summarize this paper [URL]".
- **Universal input:** arXiv URL, arXiv ID, DOI, DOI URL, PDF URL,
  local PDF path, journal landing URL, or pasted text.
- **Multi-layer rendering:**
  - One-page infographic at the top (mind map + headline numbers)
  - TL;DR (5–8 sentences)
  - Plain-English summary (5–10 sentences)
  - Section-by-section walk-through with plain-English alongside
    technical content for every section
  - Method flowchart (Mermaid)
  - Key-findings infographic (matplotlib when available, else Markdown)
  - Comparison table to baselines
  - Related-work timeline
  - Concept map + author network (in `--visuals max` mode)
- **Three-tier fallback** so the skill never bluffs:
  1. Local cache (instant on re-asks)
  2. Live fetch (arXiv API + Crossref + WebFetch + PDF extraction)
  3. **Bundled corpus** of canonical anchor papers (offline-safe)
  4. Model knowledge with `[UNVERIFIED]` flags
  - Source tier always declared in the output footer.
- **Local cache:** persists every fetched paper at
  `~/.agents/skills/read-research-paper/cache/`. Re-asks are instant.
- **Bundled corpus:** ships with ~10 canonical anchor papers across
  major topics (Transformers, RAG, BERT, ResNet, Adam, SimCLR, RLHF,
  PRISMA, etc.). Topic-keyword index maps slugs → papers.
- **Audience modes:** `academic` / `technical` / `general` / `mixed`
  — adjusts the plain-English layer's reading level.
- **Visual modes:** `none` / `minimal` / `auto` (default) / `max`.
- **Working Python toolchains:**
  - `fetch_paper.py` — fetches arXiv (API), DOIs (Crossref), PDFs,
    URLs, pasted text. Uses `feedparser`/`requests`/`pypdf` when
    available; falls back to stdlib `urllib`/`xml.etree`. **No
    required dependencies.** Live-tested against arXiv.
  - `extract_pdf.py` — PDF text + table extraction via `pdfplumber`
    or `pypdf`. Section-header detection. Figure / table caption
    regex.
- **Clean handoffs:**
  - `--with-related` triggers `get-research-paper` for expanded
    related work.
  - `--with-handoff` produces `bibliography.yaml` for `research-paper`.

### `read-research-paper` structure

```
skills/read-research-paper/
├── SKILL.md                       # Entry point
├── manifest.json                  # Metadata + triggers
├── instructions/core.md            # Operating principles
├── workflows/
│   ├── ingestion.md                 # Master pipeline
│   ├── visualization.md             # Visual decision tree
│   └── caching.md                   # Cache protocol
├── prompts/
│   ├── parse-paper.md               # Structured parsing
│   ├── extract-findings.md           # Headline-number extraction
│   ├── generate-mindmap.md           # Mind-map generation
│   ├── plain-english.md              # Plain-English translation
│   └── visual-summary.md             # One-page top-of-doc summary
├── templates/
│   ├── visual-paper.md              # Headline deliverable format
│   ├── tldr.md                       # TL;DR section
│   └── infographic.md                # Standalone one-pager
├── sources/
│   ├── arxiv.md                      # arXiv API specifics
│   ├── pdf-extraction.md             # PDF tooling
│   └── paper-parsing.md              # Heuristic + LLM parsing
├── schemas/
│   └── visual-paper.json             # Output schema
├── toolchains/
│   ├── fetch_paper.py                # Multi-source fetcher
│   └── extract_pdf.py                # PDF extractor
├── cache/                            # Empty placeholder; populates at runtime
│   └── README.md
├── corpus/                           # Bundled fallback corpus
│   ├── README.md
│   ├── anchor-papers.yaml
│   └── topics-index.yaml
└── examples/
    └── sample-visual-output.md       # End-to-end example
```

### Architecture: the "don't bluff" cascade

The skill is designed not to bluff when sources aren't available:

- **No internet-wide crawl** — that's not what skills do. We use
  search APIs (arXiv, Crossref) plus a bundled corpus + local cache.
- **No shared backend across users** — caches are per-installation.
  Alice's cache doesn't help Bob.
- **The bundled corpus** is a curated, version-controlled set of
  canonical anchor papers that travels with the skill. Every install
  gets the same baseline; the local cache grows from there.

### Updated — `get-research-paper`

- New integration field in `manifest.json` describing how to chain
  with `read-research-paper`.
- No functional changes.

### Updated — `research-paper`

- No functional changes; version-aligned to 2.2.0.

### Updated — tests

- 100+ tests pass. New tests cover `read-research-paper` structure,
  manifest, schema, and both Python toolchains' self-tests.

### Verified

- Live arXiv API fetch returned real metadata for arxiv:1706.03762
  ("Attention Is All You Need", Vaswani et al. 2017, all 8 authors).
- Input detection works across arXiv URLs, bare IDs, DOIs, DOI URLs,
  PDFs, generic URLs, and pasted text.
- All three skills detected by `npx skills add aniketkrs/research-paper --list`.

### Versioning

- Repo: 2.1.0 → 2.2.0
- skills/research-paper: 2.1.0 → 2.2.0 (no functional changes)
- skills/get-research-paper: 1.0.0 → 1.0.1 (manifest integration field)
- skills/read-research-paper: 1.0.0 (new)

---

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

Public skill registries (skills.sh) index from the
`<repo>/skills/<name>/` convention used by multi-skill collections.
Cross-checking the live `npx skills find` output confirmed:

- Repos like `vercel-labs/agent-skills`, `firecrawl/firecrawl-workflows`,
  `seabbs/skills`, etc. are indexed because they use this layout.
- The v2.0.0 / v2.0.1 layout (skill at root) worked for direct
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

The Claude-specific branding in v2.0.0 (description, install paths,
language) didn't match the runtime-neutral nature of the skill.
Investigation against the live `npx skills` CLI confirmed:

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
