# arXiv (read-research-paper edition)

For complete arXiv-API protocol, see
`../get-research-paper/sources/arxiv.md`. This file documents the
**fetch-and-render** specifics for `read-research-paper`.

---

## Endpoint

Single-paper fetch:

```
https://export.arxiv.org/api/query?id_list=<bare-id>&max_results=1
```

The `id_list` form returns a single paper deterministically — use this
instead of `search_query` when you have an exact ID.

---

## What the skill captures

For every arXiv paper, the skill captures (via
`toolchains/fetch_paper.py`):

| Field | Source                                     |
| ----- | ------------------------------------------ |
| Title  | `<title>` element                          |
| Authors | `<author>/<name>` elements                 |
| Year   | `<published>` (first 4 chars)              |
| Abstract | `<summary>` element                       |
| Categories | `<arxiv:primary_category>`               |
| DOI    | `<arxiv:doi>` (when published)             |
| Journal ref | `<arxiv:journal_ref>` (when published)  |
| URL    | `<id>` (canonical abstract URL)            |

Sections, figures, tables, references — the arXiv API doesn't return
those directly. To extract them, the skill needs:

1. The **PDF** (always available at `arxiv.org/pdf/<id>`).
2. OR the **arXiv source tarball** (often gives LaTeX, with figures
   as separate files).

The skill prefers the source tarball when available (cleaner figures);
falls back to PDF extraction otherwise.

---

## Source-tarball extraction (advanced)

```
GET https://export.arxiv.org/e-print/<arxiv-id>
```

Returns a `.tar.gz` containing:
- `*.tex` — the LaTeX source.
- `*.bib` — the bibliography source.
- `*.png` / `*.pdf` / `*.eps` — figures.

For papers where source extraction is supported, this gives the
cleanest possible rendering. Without it, the skill falls back to
PDF extraction (`toolchains/extract_pdf.py`).

The skill auto-detects whether the tarball is available and adapts.

---

## Versioning

arXiv preprints can be updated. The bare ID (`2403.01234`) without
version always resolves to the latest. To pin:

- `arxiv:2403.01234v2` — version 2 specifically.

The cache stores the bare ID by default; users can force a versioned
re-fetch with `--refresh`.

---

## Pacing

Per arXiv's policy: ≤ 1 request per 3 seconds. The skill enforces this
in `toolchains/fetch_paper.py` automatically.

---

## Failure modes

| Issue                                  | Recovery                                          |
| -------------------------------------- | ------------------------------------------------- |
| arXiv API timeout                       | Retry once after 5s; fall back to corpus → cache → model-knowledge |
| Bare-ID format invalid                  | Try canonicalization (strip "arxiv:" prefix, etc.) |
| Paper found but PDF unparseable        | Use abstract-only rendering; flag in Known-gaps   |
| Source tarball denied                   | Fall back to PDF                                  |
| No `<arxiv:doi>`                        | Mark as preprint, no DOI cross-check                |
