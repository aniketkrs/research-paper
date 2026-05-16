# Citation Memory Protocol

How to manage the citation database in a way that scales from 5 to
500+ entries without exhausting working memory.

---

## 1. The single source of truth

All citations live in **one canonical file**:

```
bibliography.yaml
```

(or `bibliography/index.yaml` plus per-theme files for very large
bibliographies — see `long_context/chunking.md §6`).

Every other file in the working directory references citations by
**cite_key**, never by inlined metadata. This means:

- The drafter writes `[smith2023llm]`, not "Smith et al. (2023)".
- The validator looks up cite_keys against `bibliography.yaml`.
- The citation pipeline expands cite_keys into formatted strings at
  the very end.

This separation is what enables citation memory to scale.

---

## 2. The schema

Every entry follows `schemas/citation-schema.json`:

```yaml
- id: smith_2023_llm
  type: article-journal
  authors:
    - {family: Smith, given: Jane A.}
    - {family: Doe,   given: Alice}
  year: 2023
  title: "Large language models in software engineering: A systematic survey"
  container: "ACM Computing Surveys"
  volume: 55
  issue: 4
  pages: "1-37"
  doi: "10.1145/3589334"
  verification: verified | unverified | unverified-offline | retracted
  quality_score:
    authority: 4   # 0-4
    rigor: 3       # 0-3
    recency: 3     # 0-3
    total: 10
```

Required fields per type are enforced by the citation validator.

---

## 3. Cite-key naming

Cite-keys follow:

```
<lower(first-author-family)>_<year>_<first-content-word-of-title>
```

Examples:
- `smith_2023_llm`
- `doe_2022_codex`
- `world_2024_ai` (for organization authors)

For same-author/same-year/same-first-word collisions:

```
smith_2023_llm
smith_2023_llm_b
smith_2023_llm_c
```

The deduplication pipeline auto-detects and resolves these.

---

## 4. Loading patterns

### 4.1 During drafting (per section)

```
# In the writer agent's working memory:
section_cite_keys = parse_outline(section)["cite_keys"]
relevant_entries = [
    entry
    for entry in load_yaml("bibliography.yaml")
    if entry["id"] in section_cite_keys
]
# Pass relevant_entries (not full bibliography) to the writer prompt.
```

This way each section's drafting touches only ~10–30 entries even when
the full bibliography has hundreds.

### 4.2 During citation pipeline (one-shot)

```
# At the end, the citation pipeline reads:
- bibliography.yaml (full)
- paper-draft.md (full)
# It outputs:
- paper-cited.md (with formatted citations)
- citation-report.md
```

This is the only time the full bibliography is loaded.

### 4.3 During validation

```
# The validator reads:
- paper-cited.md
- bibliography.yaml (full, but read-only and parsed once)
- validators/citation-validator.md
```

The validator caches the bibliography in memory for the duration of
the validation pass.

---

## 5. Adding a new citation mid-draft

If the writer agent needs to cite something not yet in the bibliography:

1. The writer writes:
   `[CITATION NEEDED — topic: "<short description of what's needed>"]`.
2. The orchestrator collects all `[CITATION NEEDED]` flags from
   `sections/*.md`.
3. After drafting, the orchestrator dispatches the Researcher agent to
   resolve each flag (find a real source, add to `bibliography.yaml`).
4. The orchestrator does a search-and-replace in the affected sections
   to swap `[CITATION NEEDED — ...]` for the new cite_key.

This pattern keeps the writer agent moving without forcing it to
break flow for citation searches.

---

## 6. Verification states

Every entry has a `verification` field:

| State                  | Meaning                                                |
| ---------------------- | ------------------------------------------------------ |
| `verified`              | DOI / URL resolves; metadata confirmed                  |
| `unverified`            | Provided by user; not yet checked                       |
| `unverified-offline`    | Model-known but cannot verify (no web tools)            |
| `retracted`             | Confirmed retracted (per Retraction Watch); must not be cited |

The validator flags retracted entries as **high severity** and
unverified entries as **medium severity** (surface in `Known gaps`).

---

## 7. Deduplication

When adding a new entry:

1. Check the new entry against existing entries:
   - Same DOI? → duplicate.
   - Same arxiv_id? → duplicate.
   - Same first-author family + year + first 5 normalized title words?
     → likely duplicate.
2. If duplicate detected:
   - Keep the more complete entry.
   - Merge unique metadata.
   - Update affected cite_keys in all sections.
3. If not duplicate, assign a fresh cite_key.

Implementation: `citation_engine/deduplication.md`.

---

## 8. Persistence after drafting

After the citation pipeline runs, `bibliography.yaml` is **frozen** for
the rest of the run. Any further changes (e.g., from the reviewer
agents finding a missing citation) force a re-run of the citation
pipeline — never an in-place edit of `paper-cited.md`.

This invariant is what makes the citation pipeline deterministic and
the citation report reliable.

---

## 9. Cross-paper bibliography reuse

If the user is writing a sequence of papers (e.g., a thesis with
multiple chapters), they can share `bibliography.yaml` across runs:

```
thesis/
├── bibliography.yaml              ← shared across chapters
├── chapter-1/
│   ├── paper-spec.md
│   ├── outline.md
│   ├── ...
│   └── paper-final.md
├── chapter-2/
│   ├── paper-spec.md
│   ├── ...
│   └── paper-final.md
└── ...
```

The orchestrator detects a parent `bibliography.yaml` and uses it as
the source of truth across all chapters. New citations added in
chapter 2 become available to chapter 1 on re-run.

---

## 10. Performance bounds

| Bibliography size | Strategy                                                    |
| ------------------ | ----------------------------------------------------------- |
| ≤ 50 entries        | Single file, full load fine                                  |
| 50–200 entries     | Single file, per-section filtered loading                    |
| 200–500 entries     | Per-theme split (`bibliography/<theme>.yaml`)                |
| 500+ entries        | Index + theme files + lazy loading per cite_key              |

Most papers fit in the first two tiers. Theses and surveys hit the
third or fourth.
