# Ingestion Workflow

The master pipeline for `read-research-paper`. Read when activated;
follow phases in order; persist artifacts between phases.

---

## Phase 1 — Input detection

Detect the input type by pattern matching:

```
input → type
─────────────
"https://arxiv.org/abs/<id>"            → arxiv-url
"https://arxiv.org/pdf/<id>.pdf"        → arxiv-pdf
bare arxiv id (e.g., "2403.01234")       → arxiv-id
"10.<...>/<...>"                          → doi
"https://doi.org/..."                     → doi-url
"<...>.pdf" (URL or path)                  → pdf
"https://www.nature.com/...", etc.        → journal-url
"https://...", any other URL                → generic-url
text without URL pattern                     → pasted-text
```

Normalize to canonical paper ID:

| Type                  | Canonical ID                   |
| --------------------- | ------------------------------ |
| arxiv (any)           | `arxiv:<bare-id>`              |
| doi (any)             | `doi:<doi-string>`             |
| pdf URL or path        | `url:<sha256-of-bytes>`        |
| pasted text            | `text:<sha256-of-content>`     |

Persist `paper-id.txt` containing the canonical ID. This is what
the cache keys on.

---

## Phase 2 — Fetch (with three-tier fallback)

```
1. Cache lookup:
   if cache/<type>/<id>.json exists AND --cache true (default):
     load → skip to Phase 5 (Render).
   else: continue to live fetch.

2. Live fetch:
   arxiv-id   → toolchains/fetch_paper.py (arXiv API)
   doi        → Crossref → resolved URL → fetch
   pdf        → toolchains/extract_pdf.py
   url        → WebFetch → extract paper text
   text       → use as paper body directly

3. Bundled corpus:
   if live fetch failed AND --use-corpus true (default):
     check corpus/anchor-papers.yaml for matching arxiv_id / doi.
     if hit: load → flag source as `bundled-corpus`.

4. Model knowledge fallback:
   if all of the above failed:
     ask the model if it has high confidence on this paper.
     if yes: render with every fact flagged [UNVERIFIED — offline].
     if no: fail honestly with a Known-gaps entry.
```

Every tier transition is logged in `Known-gaps.md` with the timestamp
and the reason for falling back.

---

## Phase 3 — Parse structure

Read `prompts/parse-paper.md`. Extract:

- **Title** — from arXiv API / Crossref / DOI metadata / first H1.
- **Authors** — from arXiv API authors / Crossref authors / first
  author block in the paper.
- **Year** — from publication date / arXiv submission year.
- **Venue** — journal / conference / preprint server.
- **Abstract** — from `<abstract>` / arXiv API summary / first paragraph
  after title.
- **Sections** — H2-level (or numbered) sections in the paper. Map
  to canonical names: `introduction`, `related-work`, `method`,
  `results`, `discussion`, `limitations`, `conclusion`,
  `references`, `appendices`.
- **Figures** — `<figure>` tags / Figure N captions in PDFs.
  When the figure image is extractable (via PDF extraction with
  `pypdf` or `pdfplumber`), save to `figures/`. When not, plan a
  Mermaid alternative.
- **Tables** — `<table>` tags / Table N in PDFs. Save the table data
  as `tables/<n>.csv`.
- **Headline numbers** — find the 3–5 most quoted numerical
  results. Pattern-match for `\d+(\.\d+)?\s*%`, `±`, `p < `, etc.,
  in the abstract and results section.
- **References** — extract the reference list. Parse each into the
  citation schema if possible.

Persist to `paper-data.json` per `schemas/visual-paper.json`.

---

## Phase 4 — Plan visuals

Read `workflows/visualization.md`. Decide which visuals to render
based on:

- `--visuals` mode (`none` / `minimal` / `auto` / `max`).
- What's actually present in the paper:
  - Has a method section → flowchart.
  - Has a comparison table → preserve / re-render.
  - Has a results section with numbers → infographic.
  - Has > 5 references → related-work timeline.
  - Has > 1 author → author network (only if `max`).

Persist `visuals-plan.md` listing every planned visual.

---

## Phase 5 — Render

For each planned visual:

1. Mermaid sources (always) → `figures/<name>.mmd`.
2. matplotlib renders (when Python available) → `figures/<name>.png`
   + `.svg`.
3. Markdown tables (always) → embedded in `paper-visual.md`.

Read:
- `prompts/generate-mindmap.md` — for the mind map.
- `prompts/extract-findings.md` — for the key-findings infographic.
- `prompts/visual-summary.md` — for the one-page top-of-doc summary.

---

## Phase 6 — Plain-English layers

Read `prompts/plain-english.md`. For each section:

- Generate a 3–8 sentence plain-English version.
- Reading-level target (Flesch–Kincaid grade):
  - `--audience academic` → ≤ 16
  - `--audience technical` → ≤ 14
  - `--audience general` → ≤ 10
  - `--audience mixed` (default) → produce both layers (technical +
    plain) side-by-side.
- Include 1 analogy per section when the concept is unusually dense.
- Include a **"Why this matters"** one-liner at the end of each
  section.

Persist `plain-english.md` (one block per section).

---

## Phase 7 — Assemble

Read `templates/visual-paper.md`. Concatenate:

1. **Top infographic** (mind map + headline numbers + key metadata).
2. **TL;DR** (5–8 sentences).
3. **Plain-English summary** (5–10 sentences).
4. **Section walk-through** (for each section: visual aid + plain-
   English + technical content).
5. **Key findings infographic** (charts).
6. **Comparison table** (when applicable).
7. **Related-work timeline** (when applicable).
8. **Concept map** (when `--visuals max`).
9. **Author network** (when `--visuals max`).
10. **"Why this matters"** footer.
11. **Reference list** (linked DOIs / URLs).
12. **Verification trail** (which tier the rendering came from).

Output: `paper-visual.md`.

---

## Phase 8 — Cache

Read `workflows/caching.md`. Write:

- `cache/<type>/<canonical-id>.json` — the parsed paper data.
- Update `cache/manifest.json` with the new entry's metadata.
- Update `cache/topics/<topic-slug>.json` if the topic was inferred.

If the paper was loaded from cache in phase 2, this is a no-op.

---

## Phase 9 — Optional handoffs

### `--with-related`

Dispatch the `get-research-paper` skill on the paper's primary topic:

```
/get-research-paper "<derived topic>" --n 10 --depth standard
```

The result becomes a new "Related work expanded" section in
`paper-visual.md` and is added to the bibliography.

### `--with-handoff`

Emit `bibliography.yaml` containing this paper + its references in
the canonical format. The user can then run:

```
/research "<topic>" --bibliography <path>/bibliography.yaml
```

…to write a new paper that builds on this one.

---

## Phase 10 — Failure handling

| Phase             | Failure                                  | Recovery                                                |
| ----------------- | ---------------------------------------- | ------------------------------------------------------- |
| Input detection    | Unparseable input                          | Ask user once; default to `pasted-text` mode           |
| Live fetch         | arXiv API unreachable                       | Fall to corpus → model knowledge                       |
| Live fetch         | DOI doesn't resolve                         | Fall to corpus → model knowledge                       |
| Live fetch         | PDF extraction fails                         | Use abstract only; flag in Known-gaps                  |
| Live fetch         | URL scrape returns paywall                  | Try arXiv mirror; fall to corpus → model knowledge      |
| Parse              | Sections couldn't be detected               | Render the abstract + best-guess structure              |
| Parse              | No figures extractable                      | Generate Mermaid alternatives                            |
| Render             | matplotlib unavailable                      | Mermaid + Markdown table fallback                        |
| Render             | Mind map too dense                          | Reduce levels; flag                                     |
| Plain-English      | Reading level above target                  | Re-prompt with stricter rules                            |
| Cache              | Write fails (permissions)                   | Continue without caching; flag                          |

Never silently fail. `Known-gaps.md` is the contract.

---

## Multi-agent variant

For long papers (> 30 pages), dispatch sub-agents per phase:

```
Orchestrator
   ├── Fetcher        → paper-data.json (raw)
   ├── Parser         → paper-data.json (structured)
   ├── Visualizer     → figures/, tables/
   ├── Translator     → plain-english.md
   └── Assembler      → paper-visual.md
```

For short papers (< 10 pages), run inline.

---

## Persistence checkpoint

After each phase, write the artifact to disk **before** starting the
next. This is what makes the skill resumable on crash and inspectable
mid-flow.
