# Per-Paper Summary Template

A single paper's entry, used both standalone (when the user asks for a
single paper summary) and as a section in the reading list.

---

```markdown
## <<Title>>

**Cite key:** `<<cite_key>>`
**Authors:** <<First A. Last>>, <<First B. Last>>, <<et al. (when > 3)>>
**Year:** <<YYYY>>
**Venue:** <<Journal / Conference>>
**DOI:** [<<10.1234/xxxx>>](https://doi.org/<<10.1234/xxxx>>)
**arXiv:** [<<2403.01234>>](https://arxiv.org/abs/<<2403.01234>>) <<(when applicable)>>
**Quality score:** <<X>>/10 (authority <<a>>/4, rigor <<r>>/3, recency <<rc>>/3)
**Verification:** <<verified | unverified-offline | unverified | retracted>>
**Citation count:** <<N>> (Semantic Scholar; influential: <<M>>) <<(when available)>>

### Summary

<<2-4 sentences using problem → method → finding → significance
  structure per `prompts/summarization.md`. Must include the headline
  number when one exists in the abstract.>>

### Why this matters for <<Topic>>

<<One-sentence relevance anchor (only for `--depth deep`).>>

### Citation (formatted)

> <<The full reference, formatted in the user's chosen --style.>>

### Verification trail

- DOI: <<resolves | does not resolve | unchecked>>
- Crossref: <<matched | mismatched | unchecked>>
- Retraction Watch: <<no record | retracted | unchecked>>
- arXiv API: <<confirmed | not found | unchecked>>

---
```

---

## When to use this template

- **As a section** in `reading-list.md`. Every paper renders as one
  block.
- **As a standalone artifact** when the user asks for a deep dive on a
  single paper:

  ```
  /find-paper "Attention Is All You Need" --depth deep
  ```

  The skill returns a single block with the verification trail and
  formatted citation rendered.

- **As an embedded fragment** in the briefing or downstream writer
  paper (the `notes:` field of the bibliography entry is exactly the
  Summary section above).

---

## Conventions

### Citation count

Display only when available from the source. Always say "Semantic
Scholar" or "Google Scholar" so the reader knows which database
counted. The two often disagree.

### Multiple authors

| Author count | Display                                      |
| ------------ | -------------------------------------------- |
| 1            | "Smith, J."                                  |
| 2            | "Smith, J., Doe, A."                          |
| 3            | "Smith, J., Doe, A., Lee, K."                  |
| 4+           | "Smith, J., Doe, A., Lee, K., et al."          |

The full author list is always in `bibliography.yaml`. The block here
is for human readability.

### Year-of-record

For preprint-only papers: use the arXiv submission year of the latest
version.
For published papers: use the publication year (NOT the preprint year).

### Multiple identifiers

If both DOI and arXiv ID exist, show both — they're different links
serving different purposes (DOI = peer-reviewed version; arXiv = full
text and history).

---

## What NOT to put here

- **Methodology details.** Those are for the writer skill's
  methodology section.
- **Direct quotes from the abstract.** Paraphrase to reduce duplication
  risk.
- **Marketing language** ("revolutionary", "groundbreaking"). The
  reading list is for the user to decide what's important; don't
  pre-judge.
- **Raw scores beyond 0–10.** No 9.7/10 — keep to integers.

---

## Generation pipeline

This block is generated programmatically from the
`paper-result.json` schema entries:

```python
def render_paper_block(paper: dict, style: str, audience: str) -> str:
    # ... format authors per count
    # ... look up venue
    # ... compute quality string
    # ... format citation per --style
    # ... return Markdown
```

The orchestrator never edits this template by hand; if you want to
change the format, edit this file.
