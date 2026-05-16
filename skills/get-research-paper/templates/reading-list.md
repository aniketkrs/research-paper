# Reading List Template

The user-facing artifact this skill produces. Drop into the working
directory as `reading-list.md`.

> Replace every `<<...>>` slot. The template is rendered programmatically
> from the ranked + summarized paper objects.

---

```markdown
# Reading list — <<Topic>>

Generated: <<ISO timestamp>>
Source: `get-research-paper` skill v<<version>>
Working directory: `<<path>>`

**<<N>> papers** ranked <<min_score>>/10 or higher, drawn from <<source list>>.
Year range: <<lo>>–<<hi>>.

> **TL;DR briefing.** See `briefing.md` for a 1–3 paragraph synthesis
> of the field. Bibliography-ready file: `bibliography.yaml`.
> Unverified items: `Known-gaps.md`.

---

## How to use this list

- **Cite keys** (the lowercase `author_year_word` IDs) are ready to
  drop into a paper draft as `[cite_key]` placeholders.
- **DOIs** are verified; if a DOI is marked `[UNVERIFIED]`, the paper
  was found in your training data but couldn't be confirmed online.
- **Quality scores** are 0–10 per the rubric in
  `prompts/ranking.md`.
- **For paper writing** (next step), run:

  ```
  /research "<<Topic>>" --bibliography <<path>>/bibliography.yaml --style <<style>>
  ```

---

## Paper 1 — <<Title>>

**Cite key:** `<<cite_key>>`
**Authors:** <<First A. Last>>, <<First B. Last>>, <<et al.>>
**Year:** <<YYYY>>
**Venue:** <<Journal / Conference>>
**DOI:** [<<10.1234/xxxx>>](https://doi.org/<<10.1234/xxxx>>)
**Quality score:** <<X>>/10 (authority <<a>>/4, rigor <<r>>/3, recency <<rc>>/3)
**Verification:** <<verified | unverified-offline>>

> <<Two-to-four-sentence summary using the
>  problem → method → finding → significance structure
>  (per `prompts/summarization.md`).>>

---

## Paper 2 — <<Title>>

**Cite key:** `<<cite_key>>`
**Authors:** <<...>>
**Year:** <<...>>
**Venue:** <<...>>
**DOI:** <<...>>
**Quality score:** <<...>>/10
**Verification:** <<...>>

> <<Summary.>>

---

## Paper 3 — <<Title>>

(... continued for each paper ...)

---

## Notes

- Papers below the quality floor (<<floor>>/10) were dropped.
- Diversity heuristics applied: per-author cap (max 2), per-venue cap
  (max <<X>>%), at least one review (if available), at least one
  foundational paper (if available).
- For papers with multiple findings, the summary leads with the most
  relevant to the topic.

## Source breakdown

| Source                | Candidates examined | Kept |
| --------------------- | -------------------- | ---- |
| arXiv                  | <<n>>               | <<m>> |
| Semantic Scholar       | <<n>>               | <<m>> |
| Google Scholar         | <<n>>               | <<m>> |
| PubMed                 | <<n>>               | <<m>> |
| ...                    | ...                  | ...  |

## Known gaps

See `Known-gaps.md` for any unverified entries, retracted papers
excluded, or fields the skill couldn't fill.
```

---

## Skill-specific instructions

When the orchestrator emits this file:

1. Sort papers by `quality_score.total` descending.
2. For each paper, render the block exactly as above.
3. Use Markdown blockquotes (`>`) for the summary so it's visually
   distinct from the metadata.
4. DOI is rendered as a clickable Markdown link to `https://doi.org/<doi>`.
5. The "Source breakdown" section is auto-generated from the search
   logs.
6. The "Notes" section is generated from which diversity heuristics
   actually fired during ranking.
7. The "How to use this list" section explains the handoff
   automatically — even when `--handoff` was not set, this footer
   reminds the user the option exists.

---

## Reading-list density

- **Quick** (`--depth quick`, n=5): 5 papers, 2-sentence summaries each.
- **Standard** (`--depth standard`, n=10): 10 papers, 3-sentence
  summaries each.
- **Deep** (`--depth deep`, n=20+): 20+ papers, 4-sentence summaries
  + a "Why this matters for `<topic>`" line each.

The reading list grows roughly linearly with `--n`. Above n=30,
consider splitting by sub-theme.
