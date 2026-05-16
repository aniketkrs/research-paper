# PDF Extraction

How `read-research-paper` turns a PDF (URL or local path) into
structured `paper-data.json`.

---

## The tooling

`toolchains/extract_pdf.py` provides text + table extraction. It works
in three tiers:

| Tier | Library | Capability |
| ---- | ------- | ---------- |
| 1    | `pdfplumber` | Best — extracts text, tables, layout. |
| 2    | `pypdf`      | Basic — extracts text, metadata.       |
| 3    | (none)       | Falls through to model-knowledge with a clear error. |

Install one of the libraries to enable PDF mode:

```bash
pip install pdfplumber  # recommended
# or
pip install pypdf        # lighter, no table extraction
```

The skill detects which is available via `--self-test`.

---

## Pipeline

```
PDF (path or URL)
   │
   ▼
[1] Download (if URL) → bytes
   │
   ▼
[2] Open via pdfplumber / pypdf
   │
   ▼
[3] Extract per page:
       text          ← page.extract_text()
       tables (pdfplumber only) ← page.extract_tables()
   │
   ▼
[4] Run section-header detection on full text
   │
   ▼
[5] Run figure / table caption regex
   │
   ▼
[6] Map detected sections to canonical IDs
       (introduction / related-work / method / results / discussion /
        limitations / conclusion / references / appendix)
   │
   ▼
[7] Persist to paper-data.json
```

---

## Section detection heuristics

A line is a candidate section header if:

- It is short (≤ 80 characters).
- It starts with an optional number (`1.`, `1`, `I.`, `Section 3:`).
- It matches one of the canonical-section regexes
  (`prompts/parse-paper.md §"Section detection heuristics"`).

When detection is uncertain, the skill flags
`inferred_from_text: true` on the section so the user knows it was
heuristic.

---

## Figure / table extraction

Two patterns:

1. **Layout-based (pdfplumber)**: `pdfplumber` returns table objects
   with cell coordinates. Reliable for clean two-column papers.
2. **Caption-based (regex)**: scan for lines matching
   `^Figure N. ...` or `^Table N. ...` and pair captions with the
   preceding/following content.

When the actual figure image can't be extracted, the visualization
phase generates a Mermaid alternative based on the caption.

---

## What can go wrong

| Issue                                | Behavior                                              |
| ------------------------------------ | ----------------------------------------------------- |
| Encrypted PDF                          | Detect, fail with "PDF is encrypted" + Known-gaps entry |
| Scanned-image-only PDF (no text layer)  | Extract empty text → fail honestly                  |
| Multi-column layout                    | pdfplumber handles OK; pypdf may interleave columns   |
| Heavy LaTeX with custom fonts           | Some characters may be lost / misread                  |
| Equations as images                     | Lost; flag in Known-gaps                                |
| Tables as images                        | Lost; render as "see paper Table N"                     |
| Very large PDFs (>50 MB)                | Cap pages at 200 (configurable); flag                  |

---

## Best practices

- **For clean papers (arXiv-style two-column with text layer):**
  `pdfplumber` produces excellent results.
- **For old PDFs / journal papers without text layer:**
  consider OCR (`pytesseract`) — not bundled by default; user opts in.
- **For LaTeX-heavy math papers:** prefer the arXiv source tarball
  over PDF extraction (per `sources/arxiv.md`).

---

## Failure handling

If extraction returns < 500 chars of text:

1. Likely a scanned image PDF.
2. Mark `extraction_quality: "poor"` in `paper-data.json`.
3. Render whatever metadata we have (title, authors, abstract from
   external source like Crossref).
4. Skip section walk-through; render abstract-only.
5. Flag in `Known-gaps.md`:
   `[PDF EXTRACTION FAILED]` — recommend OCR or alternate source.

The skill never silently skips a PDF — failure is always surfaced.
