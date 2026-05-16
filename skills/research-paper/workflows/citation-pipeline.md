# Citation Pipeline

This pipeline takes a paper draft with `[cite_key]` placeholders and a
`bibliography.yaml` file and produces a fully cited paper in the chosen
style with a properly formatted reference list. Called from
`workflows/research-orchestration.md §8`.

> **Single source of truth:** `bibliography.yaml`. The paper draft only
> contains `[cite_key]` placeholders. The script generates the styled
> in-text citations and reference list deterministically.

---

## 1. Inputs

- `paper-draft.md` — Markdown draft with `[cite_key]` placeholders, e.g.
  `[smith2023llm]`, `[doe2022codex]`. Multiple keys allowed:
  `[smith2023llm; doe2022codex; lee2021gpt]`.
- `bibliography.yaml` — every cited work, in canonical metadata schema
  (see `references/citation-styles.md §"Common metadata fields"`).
- `--style` — one of `harvard`, `apa`, `ieee`, `mla`, `chicago-author-date`,
  `chicago-notes`, `nature`, `arxiv-numeric`.
- `--locale` — e.g. `en-GB` or `en-US` (affects punctuation: "ed." vs.
  "edn.", `"` vs. `"`).

---

## 2. Steps

### 2.1 Parse the bibliography

Load every entry from `bibliography.yaml`. Validate each entry has the
required fields for its `type` (see `references/citation-styles.md §12`).
Entries missing required fields are flagged `[INCOMPLETE]` and the cite
key is held in an error list.

### 2.2 Scan the draft for cite keys

Walk through `paper-draft.md`. Every `[cite_key]` occurrence is recorded
with its position. Multi-key citations like `[k1; k2]` are split.

Validate that:
- Every cite key in the draft has an entry in `bibliography.yaml`.
- Every entry in `bibliography.yaml` is cited at least once. If not,
  warn (orphan reference) — the user may want to keep it for completeness
  or remove it.

### 2.3 Build the citation order index

For numeric styles (IEEE, Nature, arxiv-numeric), assign each entry a
number based on **first appearance** in the draft. Multi-key citations
preserve the order the user wrote.

### 2.4 Disambiguate same-author-same-year

If two entries by the same first author have the same year, suffix `a`,
`b`, `c` to the year in the order of first in-text appearance. Update both
the in-text citations and the reference entry.

### 2.5 Format in-text citations

For each `[cite_key]` (or `[k1; k2]`), produce the styled string per
`references/citation-styles.md`. Replace the placeholder in the draft.

Examples per style:

| `[smith2023llm]` |  |
|-|-|
| **Harvard**         | `(Smith, 2023)` |
| **APA**              | `(Smith, 2023)` |
| **IEEE**             | `[1]` (where 1 is the assigned number) |
| **MLA**              | `(Smith 23)` (with page if present) |
| **Chicago a-d**       | `(Smith 2023, 23)` |
| **Nature**           | `^1`        |
| **arxiv-numeric**     | `[1]`       |

Multi-key in IEEE: `[1], [3]` or `[1]–[3]` for runs. In Harvard: `(Smith,
2023; Doe, 2022)`.

### 2.6 Format the reference list

Sort:
- **Numeric styles** (IEEE / Nature / arxiv-numeric): by assigned number
  (= order of first appearance).
- **Author–year styles** (Harvard / APA / Chicago a-d): alphabetical by
  family name, then year.
- **MLA**: alphabetical by family name (Works Cited).
- **Chicago notes**: footnotes in citation order; bibliography
  alphabetical.

For each entry, project the canonical metadata into the styled reference
text per `references/citation-styles.md §1–§7`. Punctuation, italics, and
capitalization are deterministic.

### 2.7 Insert the reference list into the paper

Find or create the `## References` section of `paper-draft.md` and replace
its contents with the formatted list. For Chicago notes-style, also emit
the footnotes inline (using `[^N]` Markdown footnote syntax).

### 2.8 Quality checks

- Every in-text citation has a matching reference entry.
- Every reference entry has at least one in-text citation (warn on orphans).
- No duplicate references (DOI-deduplicated in §2.9).
- Style is consistent end-to-end.

### 2.9 De-duplication

Two entries are duplicates if:
- Same DOI, OR
- Same `(first-author family, year, normalized-title-prefix)`.

When detected, merge into one entry, preferring the more complete metadata
(more fields populated). Update all cite keys in the draft to the canonical
form.

### 2.10 Emit the citation report

`citation-report.md` — for the validator and human review:

```markdown
# Citation report

- Style: ieee
- Total in-text citations: 142
- Total unique references: 47
- Numbered (IEEE) range: [1]–[47]
- Orphan references: 2 (lee2018; brown2019) — consider removal or use
- Missing keys: 0
- Duplicates merged: 1 (smith2023a + smith2023b → smith2023llm)
- Incomplete entries: 0
- Style switch warnings: 0
```

If the report shows `Missing keys > 0` or `Incomplete entries > 0`, the
pipeline exits with an error and prompts the user / writer agent to fix
the bibliography.

---

## 3. Output

- `paper-cited.md` — paper with all in-text citations formatted and the
  reference section populated.
- `citation-report.md` — summary of the conversion.
- `bibliography.yaml` — possibly updated (a/b/c suffixes, merged
  duplicates, normalized cite keys).

---

## 4. Edge cases

### 4.1 Missing field but cite still wanted

If a reference is essential but lacks a required field (e.g., page numbers
not yet available), include it with `[INCOMPLETE]` flags on the missing
fields and surface in `Known gaps`.

### 4.2 Secondary citation

User wrote `[jones1990|via:smith2023]`. The script renders as:
- Harvard: `(Jones, 1990, cited in Smith, 2023)`
- APA: `(Jones, 1990, as cited in Smith, 2023)`
- IEEE: `[Jones, 1990, cited in [3]]` (rare; usually rewrite to cite
  primary)

### 4.3 Personal communications

`[pers-comm:lee2024]` with metadata `type: personal-communication`. Per
APA: cited in-text only, not in the reference list. Per Harvard: same.
Per Chicago: cited in a footnote.

### 4.4 Same author, same year, same title (republication)

Distinguish via `version: 'preprint' | 'published'` and prefer the
published version for citation.

### 4.5 Style switch mid-paper

Forbidden — the pipeline rejects this. If the user changes style after
drafting, re-run from §2.1 with the new `--style` and regenerate the
whole reference section.

---

## 5. Citation-density audit

After the pipeline runs, audit per-section citation density against the
floors in `references/citation-styles.md §11`:

| Section                            | Floor citations    |
| ---------------------------------- | ------------------ |
| Introduction                        | 6 per page        |
| Related Work                        | 15 per page       |
| Methodology                         | 0 (cite when adopting a known method) |
| Results                             | 0–2 per page      |
| Discussion                          | 5 per page        |
| Conclusion                          | 0–2               |

Sections far below the floor are flagged in `validation-report.md`
("Insufficient citations in §X — current density: <n> per page; floor:
<n>").

---

## 6. Tools

- `scripts/format_bibliography.py` — implements §2.1–§2.7.
- `scripts/extract_references.py` — checks consistency in §2.8.
- `scripts/validate_citations.py` — full validation including DOI
  resolution if web tools are available.

CLI:

```bash
python scripts/format_bibliography.py \
    --bib bibliography.yaml \
    --style ieee \
    --locale en-US \
    --paper paper-draft.md \
    --out paper-cited.md \
    --report citation-report.md
```

Returns non-zero on `Missing keys > 0` or `Incomplete entries > 0`.

---

## 7. Why a single canonical bibliography

The skill always uses one canonical `bibliography.yaml`. This means:

- Style switching is a one-line change.
- The same bibliography can produce multiple output formats (arXiv +
  IEEE + Nature submissions of the same work).
- De-duplication is centralized.
- Citation traceability ("which sources support which claim?") becomes a
  pure function of the bibliography + draft.

This is the citation analog of "single source of truth" software design.
