# research-paper

> Three agent skills for academic research, in one repo. **Find** real papers,
> **read** any paper as a visual experience, and **write** new papers grounded
> in real sources. Runtime-neutral — works with 50+ AI coding agents.

```bash
npx skills add aniketkrs/research-paper
```

After install, in any compatible agent session:

```
/research "graph neural networks for fraud detection" --style ieee
/find-paper "retrieval-augmented generation" --years last-3
/read-paper https://arxiv.org/abs/1706.03762
```

> **Date freshness:** every paper run starts by checking today's actual
> date (via `date -u +%Y-%m-%d` or runtime context). Year-range flags
> like `--years last-3` are computed from today, not from the model's
> training cutoff. The skill never silently uses stale data — see
> [`instructions/freshness.md`](skills/research-paper/instructions/freshness.md)
> in any of the three skills.

[![License: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Skills: 3](https://img.shields.io/badge/skills-3-green.svg)](#the-three-skills)
[![Tests: 116/116](https://img.shields.io/badge/tests-116%2F116-brightgreen.svg)](tests/)

---

## What this is

Three small, focused skills that work together — or independently — to
make academic-paper work fast, rigorous, and not boring.

| | Skill | One-line job |
|---|---|---|
| ✍️ | **`research-paper`** | **Writes** new papers — research papers, lit reviews, theses, whitepapers, surveys, policy briefs |
| 🔎 | **`get-research-paper`** | **Finds** real existing papers — searches arXiv, Scholar, PubMed, Semantic Scholar |
| 📖 | **`read-research-paper`** | **Reads** any paper (URL / arXiv / DOI / PDF / DOCX / PPTX / image) and renders it visually |

All three are runtime-neutral. They install with one command and work
with **Claude Code, OpenCode, Cursor, Cline, Codex, Aider, Amp,
Antigravity, AiderDesk, Augment, IBM Bob,** and 50+ other agent
runtimes via [`npx skills`](https://www.npmjs.com/package/skills).

---

## Install

### One command — all three skills, no prompts

```bash
npx skills add aniketkrs/research-paper --yes --skill '*'
```

The `--yes --skill '*'` flags install all three skills in one shot
without prompting. The installer auto-detects every agent runtime on
your machine and places the skills in the universal `.agents/skills/`
directory.

### Verify

```bash
npx skills list
```

Expected: **`research-paper`, `get-research-paper`, `read-research-paper`** all listed.

### Other install options

```bash
# Install only one skill
npx skills add aniketkrs/research-paper --yes --skill research-paper

# Pin to a version
npx skills add aniketkrs/research-paper#v2.4.0 --yes --skill '*'

# User-scope (global) instead of project-scope
npx skills add aniketkrs/research-paper --yes --skill '*' --global

# Direct from GitHub (no skills CLI; this installer also installs all skills by default)
npx -y github:aniketkrs/research-paper install
```

For per-platform manual install (Claude Desktop, claude.ai web,
Anthropic API/SDK, etc.), see
**[INSTALLATION.md](INSTALLATION.md)**.

---

## The three skills

### ✍️ research-paper — writes new papers

Produces publication-ready research papers, literature reviews,
theses, whitepapers, surveys, and policy briefs.

**Trigger it:**
```
/research "topic" --style ieee --depth comprehensive
/literature-review "topic" --systematic --sources 50
/whitepaper "topic" --audience technical
/thesis "Chapter 3: Methodology" --style harvard
/policy "topic" --depth standard
```

…or in plain English: *"write a research paper on graph neural networks
for fraud detection"*.

**Produces:**
- 10 paper formats: arXiv, IEEE, ACM, Nature, Harvard, lit-review,
  thesis chapter, whitepaper, survey, policy brief.
- 7 citation styles: Harvard, APA, IEEE, MLA, Chicago, Nature,
  arXiv-numeric. Switchable with one flag.
- Real visualizations: charts, tables, heatmaps, flowcharts, PRISMA
  diagrams, forest plots.
- Methodology section with sample-size justification and validity
  threats.
- Statistical validation with effect sizes, CIs, multiple-comparison
  correction.
- Three-persona simulated peer review (methodologist + domain expert
  + reader).
- Plain-English summary alongside the technical content.

**What it won't do:** invent citations, DOIs, or coauthors.
Unverifiable items are flagged `[UNVERIFIED]` and surfaced in
`Known-gaps.md`.

### 🔎 get-research-paper — finds papers on a topic

Searches arXiv, Google Scholar, PubMed, Semantic Scholar, DBLP,
ACM DL, IEEE Xplore, and OpenReview. Returns a curated reading list
with verified DOIs, key findings, and ready-to-cite metadata.

**Trigger it:**
```
/get-research-paper "topic" --n 25 --years 2020-2024 --depth deep
/find-paper "topic"
/papers-on "topic"
/scholar "topic"
```

…or: *"find research papers on retrieval-augmented generation"*.

**Produces:**
- A ranked reading list (`reading-list.md`) with quality scores.
- A canonical `bibliography.yaml` ready to feed the writer skill.
- A 1–3 paragraph field briefing.
- Source-quality scoring (authority + rigor + recency).
- Diversity heuristics: per-author cap, per-venue cap, ≥1 review,
  ≥1 foundational paper.
- DOI verification + retraction screening (when web tools are
  available).

### 📖 read-research-paper — reads any paper, makes it not boring

Take any paper input — arXiv URL, arXiv ID, DOI, PDF, DOCX, PPTX,
image, plain text — and render it as a visual reading experience.

**Trigger it:**
```
/read-research-paper https://arxiv.org/abs/1706.03762
/read-paper ./paper.pdf
/explain-paper https://doi.org/10.1145/3589334
/visualize-paper ./slides.pptx
/tldr-paper ./scan.png
```

…or: *"read this research paper [URL]"*, *"explain this paper"*,
*"make this paper visual"*.

**Produces a multi-layer Markdown rendering** with:
- One-page infographic at the top (mind map + headline numbers).
- TL;DR (5–8 sentences).
- Plain-English summary (5–10 sentences).
- Section-by-section walk-through with plain-English **alongside**
  the technical content (not replacing it).
- Method flowchart (Mermaid).
- Key-findings infographic (matplotlib when available, Markdown
  otherwise).
- Comparison table to baselines.
- Related-work timeline.
- "Why this matters" footer.
- Verification trail.

**Three-tier "don't bluff" cascade:** local cache → live fetch →
bundled corpus → model knowledge with `[UNVERIFIED]` flags. Source
tier is always declared in the output footer.

---

## Supported file formats

### Read (input)

The `read-research-paper` skill handles **any** of these as input:

| Format | Extensions | Always available? |
|---|---|---|
| Markdown, plain text, JSON | `.md`, `.markdown`, `.txt`, `.json` | ✅ |
| LaTeX | `.tex`, `.latex` | ✅ |
| HTML | `.html`, `.htm` | ✅ (with regex fallback) |
| CSV / TSV | `.csv`, `.tsv` | ✅ (basic) |
| RTF | `.rtf` | ✅ (with regex fallback) |
| **PDF** | `.pdf` | install `pdfplumber` or `pypdf` |
| **DOCX** | `.docx` | install `python-docx` |
| **PPTX** | `.pptx` | install `python-pptx` |
| **XLSX** | `.xlsx`, `.xls` | install `pandas` + `openpyxl` |
| **EPUB** | `.epub` | install `ebooklib` |
| **Images** (OCR) | `.png`, `.jpg`, `.tiff`, `.bmp` | install `pytesseract` + Tesseract |

One command to enable everything:

```bash
pip install pdfplumber python-docx python-pptx pandas openpyxl \
            beautifulsoup4 striprtf ebooklib pytesseract Pillow
```

### Write (output)

The `research-paper` skill produces Markdown by default. To convert
to other formats:

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

Install Pandoc (and optionally LaTeX for PDFs):

```bash
# macOS
brew install pandoc                      # base
brew install --cask mactex-no-gui         # for PDF output

# Linux
apt install pandoc                        # base
apt install texlive                        # for PDF output

# Windows
choco install pandoc                       # or scoop install pandoc
choco install miktex                        # for PDF output
```

Then:

```bash
/research "topic" --output paper.pdf
/research "topic" --output paper.docx
```

**Self-test** to see what's available on your machine:

```bash
python skills/read-research-paper/toolchains/read_any_file.py --self-test
python skills/research-paper/toolchains/convert_output.py --self-test
```

Full reference: [`skills/read-research-paper/sources/file-formats.md`](skills/read-research-paper/sources/file-formats.md).

---

## End-to-end workflow

The three skills chain cleanly:

```
┌─────────────────────────────────────────────────────────────┐
│   /find-paper "topic"                                        │
│   └─→ reading-list.md + bibliography.yaml                    │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│   /read-paper <URL>      (visualize ANY single paper)         │
│   └─→ paper-visual.md  (mind map + flowchart + plain English) │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│   /research "topic" --bibliography ./topic/bibliography.yaml  │
│   └─→ paper-final.md → convert_output → paper.pdf / .docx    │
└─────────────────────────────────────────────────────────────┘
```

Or use any one standalone — they don't require each other.

---

## Quick start

### Find papers on a topic

```
/find-paper "transformer architectures for time-series forecasting" --n 10
```

The skill returns a curated reading list with verified DOIs, key
findings per paper, and a `bibliography.yaml` ready for the writer
skill.

### Read a single paper visually

```
/read-paper https://arxiv.org/abs/1706.03762
```

The skill returns a multi-layer Markdown rendering with mind map,
flowchart, infographic, and plain-English alongside the technical
content. Cached locally so re-asking is instant.

### Write a paper using a curated bibliography

```
/research "predicting customer churn with graph neural networks" \
    --style ieee \
    --depth comprehensive \
    --bibliography ./gnn-fraud-detection/bibliography.yaml
```

The skill walks: plan → literature review → methodology → analysis →
visualization → drafting → citations → validation → review → ship.

### Convert the result to PDF / DOCX

```bash
python skills/research-paper/toolchains/convert_output.py \
    --input ./gnn-fraud-detection/paper-final.md \
    --to pdf \
    --out paper.pdf
```

---

## What "done" means

A paper is delivered only after passing every quality gate:

- ≥ 1500 words (configurable).
- ≥ 8 references with verified DOIs.
- ≥ 1 figure or table.
- All required sections present (abstract, intro, methodology,
  results, discussion, limitations, conclusion, references).
- Plain-English summary present.
- Reproducibility statement present.
- Future Work section present.
- Academic-quality rubric mean ≥ 4 / 5.
- All three reviewer personas score ≥ 3.0.
- All `[CITATION NEEDED]` and `[UNVERIFIED]` flags resolved or
  surfaced in `Known-gaps.md`.

Failures surface in `Known-gaps.md`. Never silent.

---

## Compatibility

`npx skills add` auto-detects and installs into 50+ agent runtimes:

| Universal | Symlink-supported |
|---|---|
| Amp, Antigravity, Cline, Codex, Cursor, +10 more | AiderDesk, Augment, IBM Bob, Claude Code, OpenCode, +35 more |

Run `npx skills add aniketkrs/research-paper --list` to see the full
list of agents detected on your machine.

---

## Repo structure

```
research-paper/
├── README.md, LICENSE, CHANGELOG.md, INSTALLATION.md, package.json
├── bin/install.js               ← direct npx installer
├── tests/test-runner.js         ← 116/116 tests pass
├── docs/                        ← architecture, design decisions, FAQ
└── skills/
    ├── research-paper/          ← writes papers (106 files)
    ├── get-research-paper/      ← finds papers (20 files)
    └── read-research-paper/     ← reads any paper (26 files)
```

Each skill is self-contained — manifest, instructions, prompts,
templates, schemas, toolchains, examples, sources, tests.

---

## Optional Python toolchain

The skills work with **just** filesystem read/write. They emit
Markdown tables and Mermaid diagrams as the always-available default.

To enable real charts, statistical validation, multi-format file I/O,
and Pandoc output:

```bash
# Charts + statistical validation (research-paper)
pip install pandas numpy scipy statsmodels matplotlib seaborn pyyaml

# Multi-format file reading (read-research-paper)
pip install pdfplumber python-docx python-pptx openpyxl \
            beautifulsoup4 striprtf ebooklib pytesseract Pillow

# Multi-format output (research-paper) - install Pandoc + LaTeX system-wide
# macOS:    brew install pandoc && brew install --cask mactex-no-gui
# Linux:    apt install pandoc texlive
# Windows:  choco install pandoc miktex
```

When any tool is missing, the skill detects it and falls back —
never silent failure, always a clear "install X to enable" message.

---

## Extending

The skills are modular. Each one is a folder with a clear extension
boundary.

- **Add a new venue** (e.g., LNCS): drop a template in
  `templates/<venue>.md` + register in `manifest.json`.
- **Add a new citation style**: extend
  `citation_engine/citation-styles.md` and
  `toolchains/format_bibliography.py`.
- **Add a new chart type**: extend
  `visualization_engine/decision-engine.md` and
  `toolchains/generate_charts.py`.
- **Add a new file format**: extend
  `read-research-paper/toolchains/read_any_file.py` and
  `read-research-paper/sources/file-formats.md`.

Full extension guide: [`docs/extending.md`](docs/extending.md).

---

## Tests

Lightweight test suite in `tests/test-runner.js`:

```bash
node tests/test-runner.js
```

Covers:
- File structure (every required file present).
- SKILL.md frontmatter (valid YAML).
- manifest.json (valid JSON, required fields).
- JSON Schemas (paper-schema, citation-schema, visual-paper schema, etc.).
- Python toolchain self-tests (graceful degradation).
- Citation pipeline smoke test against fixtures.

**116/116 tests pass.**

---

## Troubleshooting

| Symptom | Likely cause | Fix |
|---|---|---|
| Skill never activates | Restart your agent session after install | |
| Charts come out as Markdown only | Python plotting deps missing | `pip install pandas matplotlib seaborn` |
| Can't read a `.pdf` | PDF library missing | `pip install pdfplumber` |
| Can't read a `.docx` | DOCX library missing | `pip install python-docx` |
| Can't OCR an image | OCR not installed | `pip install pytesseract Pillow` + install Tesseract |
| Can't convert to PDF | Pandoc / LaTeX missing | install Pandoc + a LaTeX engine |
| Skill activates for unrelated requests | Trigger patterns too broad | edit `manifest.json → trigger.patterns` |
| Output truncated mid-section | Context pressure | switch to multi-file output (`--depth comprehensive`) |

---

## License

MIT — see [LICENSE](LICENSE).

## Contributing

Issues and PRs welcome at
[github.com/aniketkrs/research-paper](https://github.com/aniketkrs/research-paper).

When filing an issue, please include:
- Your runtime (Claude Code, OpenCode, etc.)
- The slash command or prompt that triggered the issue
- The contents of `Known-gaps.md` if any
- The relevant `validation-report.md` if any

---

## Versioning

| Version | Highlights |
|---|---|
| **2.3.0** | Multi-format file I/O: read PDF/DOCX/PPTX/XLSX/EPUB/images; write PDF/DOCX/HTML/LaTeX/EPUB/RTF/ODT/PPTX |
| 2.2.0 | Added `read-research-paper` skill (visual paper reading) |
| 2.1.0 | Added `get-research-paper` skill (paper discovery) |
| 2.0.x | Initial release of `research-paper` skill (paper writing) |

See [CHANGELOG.md](CHANGELOG.md) for the full history.
