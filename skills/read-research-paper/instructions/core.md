# Core Instructions

You are operating the **`read-research-paper`** skill. Your job:
**take ONE specific paper and render it as a visually engaging,
multi-layer reading experience** — never invent its contents, never
swap one paper for another, never strip the technical depth.

Read this once when activated, then follow the orchestration in
`workflows/ingestion.md`.

---

## 1. Operating posture

1. **Don't bluff.** If you can't fetch the paper, say so. Surface
   in `Known-gaps.md`. Don't substitute a different paper.
2. **Don't strip rigor.** Plain-English layers AUGMENT, not replace,
   the technical content. Both must coexist in the output.
3. **Don't oversell.** Match the paper's own certainty. If it says
   "may suggest", you say "may suggest".
4. **Visual-by-default.** Generate at minimum: 1 mind map + 1 method
   flowchart + 1 key-findings figure + 1 comparison table.
5. **Cache aggressively.** Every successfully fetched paper writes
   to the user's local cache. Future re-asks are instant.
6. **Use the corpus.** When live fetch fails, check the bundled
   `corpus/anchor-papers.yaml` before falling back to model knowledge.
7. **Never invent figures.** If the paper has a figure you can't
   extract, generate a Mermaid alternative. If you can't reconstruct
   the figure faithfully, drop it and flag in `Known-gaps.md`.
8. **Never invent citations.** The reference list comes from the
   paper itself, not from imagination.
9. **Honest provenance.** Every entry has a `source:` field —
   `live-fetch | cache | bundled-corpus | model-knowledge`. The
   user always knows where each fact came from.

---

## 2. Activation protocol

When the skill activates:

1. **Parse the input** (`workflows/ingestion.md §1`):
   - Detect type: arXiv URL / arXiv ID / DOI / DOI URL / PDF URL /
     PDF path / journal URL / pasted text.
   - Normalize to a canonical paper ID
     (`arxiv:2403.01234`, `doi:10.1145/3589334`, or `url:<sha256>`).
2. **Check the cache** (`workflows/caching.md`):
   - If `cache/<id>.json` exists and `--cache true` (default), load
     and skip to phase 5 (Render).
3. **Live fetch** (`workflows/ingestion.md §2`):
   - arXiv → `toolchains/fetch_paper.py` (uses arXiv API).
   - DOI → Crossref → resolved URL → fetch.
   - PDF → `toolchains/extract_pdf.py`.
   - URL → `WebFetch` of the page → extract paper text.
   - Pasted text → treat as the paper body.
4. **Parse structure** (`prompts/parse-paper.md`):
   - Title, authors, year, venue.
   - Abstract.
   - Sections (intro, related work, method, results, discussion, etc.).
   - Figures (when extractable).
   - Tables (when extractable).
   - Headline numbers (key findings).
   - References.
   - Persist to `paper-data.json` per `schemas/visual-paper.json`.
5. **Plan visuals** (`workflows/visualization.md`):
   - Decide which mind maps / flowcharts / infographics / tables
     to render.
6. **Render visuals** (`prompts/generate-mindmap.md`,
   `prompts/visual-summary.md`):
   - Mermaid diagrams (always).
   - matplotlib charts (when Python + pandas + matplotlib available).
   - Markdown tables (always).
7. **Generate plain-English layers** (`prompts/plain-english.md`):
   - One per section. 3–8 sentences. Flesch–Kincaid ≤ 12.
8. **Assemble** the output Markdown
   (`templates/visual-paper.md`).
9. **Cache** the result.
10. **(Optional)** If `--with-related`, dispatch `get-research-paper`
    on the key topics. If `--with-handoff`, emit `bibliography.yaml`.

---

## 3. Slash command parsing

```
/<command> <input> [--<option> <value>]...
```

Where `<input>` is one of:

| Input pattern                            | Example                                    |
| ---------------------------------------- | ------------------------------------------ |
| arXiv URL                                 | `https://arxiv.org/abs/2403.01234`         |
| arXiv ID                                  | `2403.01234` or `cs.LG/0701002`            |
| DOI                                       | `10.1145/3589334`                          |
| DOI URL                                   | `https://doi.org/10.1145/3589334`           |
| PDF URL                                   | `https://example.com/paper.pdf`             |
| Local PDF path                             | `/path/to/paper.pdf` or `./paper.pdf`       |
| Journal landing URL                        | `https://www.nature.com/articles/...`        |
| Pasted text                                | (paste the paper body / abstract directly)  |

Common options listed in `SKILL.md §1`.

Unknown options should not abort — fall back to defaults and proceed.

---

## 4. Three-tier fallback (the "don't bluff" pattern)

```
Cache hit? ──── yes ──→ instant return (with `source: cache`)
   │
   no
   ▼
Live fetch? ─── yes ──→ render + cache (with `source: live-fetch`)
   │
   no
   ▼
Bundled corpus? ─ yes ──→ render + flag (with `source: bundled-corpus`)
   │
   no
   ▼
Model knowledge?
   │
   ├─ Confident → render + flag every fact `[UNVERIFIED]`
   │             (with `source: model-knowledge`)
   │
   └─ Not confident → fail honestly with Known-gaps entry
                      (no rendering)
```

**Every transition is logged in `Known-gaps.md`.** The user always
knows what tier the rendering came from.

---

## 5. The "make it engaging" rule

A paper rendered by this skill is **never boring**. Achieve this via:

1. **One-page infographic at the top** — even before the abstract.
   Headline number, mind map, who did it, when, what's new.
2. **Plain-English layer alongside every section** — not at the end,
   not buried, alongside.
3. **Visuals every 2–3 paragraphs** — break the wall of text.
4. **"Why this matters" sections** — connect to real-world stakes.
5. **Quirky-but-respectful asides** when warranted — e.g., "The
   authors call this counter-intuitive — it surprised them too."
6. **Color-coded sections** (using emoji headers when appropriate)
   for visual scanability.

Never sacrifice technical accuracy for engagement. The rule is BOTH —
not either.

---

## 6. Audience modes

`--audience` controls language register **only of the plain-English
layers** — the technical content is unchanged.

| Mode          | Plain-English layer behavior                              |
| ------------- | --------------------------------------------------------- |
| `academic`    | Minimal plain-English; one-line section summaries only      |
| `technical`   | 3–4 sentence plain-English per section, defines field jargon |
| `general`     | Full plain-English alongside; no jargon; analogies; FK ≤ 10  |
| `mixed` (default) | Full plain-English + technical, both first-class           |

---

## 7. Visual mode

`--visuals` controls how heavy the visuals are:

| Mode         | What gets rendered                                         |
| ------------ | ---------------------------------------------------------- |
| `none`       | No visuals — text only (rare, opt-in)                        |
| `minimal`    | 1 mind map + 1 method flowchart only                          |
| `auto` (default) | Mind map + flowchart + key-findings + comparison table     |
| `max`        | All of the above + concept map + author network + timeline   |

The decision tree is in `workflows/visualization.md §2`.

---

## 8. Cache lifecycle

| Action           | Cache effect                                          |
| ---------------- | ----------------------------------------------------- |
| First fetch       | Write to `cache/<type>/<id>.json`. Update manifest.    |
| Re-ask same paper  | Read from cache (instant). Don't re-fetch.            |
| Cache TTL          | None by default; papers don't change. Manual refresh: `--no-cache`. |
| Cache size limit    | None by default. Each cached paper is ~10–100 KB.    |
| User clears cache    | Delete the cache directory. Skill regenerates on demand. |

Cache schema: `workflows/caching.md`.

---

## 9. Bundled corpus

The corpus (`corpus/anchor-papers.yaml`) ships ~30 canonical papers
across major topics. When the user provides a paper that's in the
corpus (matching arXiv ID or DOI), or asks a topic-style query that
matches, the corpus is consulted first.

The corpus is **not** a knowledge graph — it's a curated set of
high-quality fallbacks. Every entry has full structured metadata so
rendering works without any web access.

To extend: drop new entries into `corpus/user/`. They're loaded
alongside the bundled ones.

---

## 10. Where to look next

- **Plan an ingestion** → `workflows/ingestion.md`
- **Plan visuals** → `workflows/visualization.md`
- **Cache protocol** → `workflows/caching.md`
- **Plain-English** → `prompts/plain-english.md`
- **Mind maps** → `prompts/generate-mindmap.md`
- **Output format** → `templates/visual-paper.md`
- **Bundled corpus** → `corpus/`
- **Fetch tools** → `toolchains/fetch_paper.py`,
  `toolchains/extract_pdf.py`

Always prefer reading the *specific* file you need over re-reading
this one.
