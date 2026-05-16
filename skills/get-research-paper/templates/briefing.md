# Briefing Template

The 1–3 paragraph synthesis written when `--depth deep` (or
`--briefing true`). Generated after the reading list is finalized.

---

```markdown
# Field briefing — <<Topic>>

Generated: <<ISO timestamp>>
Based on <<n>> papers (quality ≥ <<floor>>/10) drawn from <<sources>>.
Year range: <<lo>>–<<hi>>.

## State of the field

<<Paragraph 1 — consensus, dominant approach, headline finding.

Cite cite_keys inline so the briefing is auditable. Every claim
references a paper from the reading list. Adjust audience tone:

  - academic: keep field jargon; cite densely.
  - technical: define jargon on first use; one analogy per concept.
  - general: plain English, FK ≤ 12, no jargon, simple sentences.

Avoid hype. Match the certainty of the literature.>>

## Tensions and open problems

<<Paragraph 2 — disagreements, gaps, contested claims.

Identify at least 2 tensions when present. Cite the disagreeing
papers explicitly so the user can read both sides:

  > "X has been reported (smith_2023, doe_2022) but failed to replicate
  >  in larger samples (lee_2024); the difference may be explained by
  >  selection bias in the original studies (zhang_2023a)."

Open problems are concrete: name what isn't yet known.>>

## Trajectory <<(deep only — drop section for standard depth)>>

<<Paragraph 3 — where the field is heading.

Look for signals in the reading list:
  - Recent preprints suggesting new methods.
  - Survey papers calling out future directions.
  - Papers introducing benchmarks (often define the next 3 years).
  - Multi-author position papers / roadmaps.

Avoid speculation that isn't grounded in cited papers.>>

---

## Key papers to read first

Three reading orders, depending on the user's goal:

### If you want the foundations

1. <<oldest_high_quality_cite_key>> — <<one-line why>>
2. <<second_oldest>> — <<one-line why>>
3. <<third_oldest>> — <<one-line why>>

### If you want the state of the art

1. <<newest_top_score>> — <<one-line why>>
2. <<second_newest>> — <<one-line why>>
3. <<third_newest>> — <<one-line why>>

### If you want the open problems

1. <<survey_or_position_paper>> — identifies the gaps
2. <<contested_claim_paper>> — represents one side
3. <<contested_claim_paper_other_side>> — represents the other

---

## Methodological notes

<<One short paragraph if relevant. Examples:

  > "All but two papers in this list use observational data; causal
  >  claims should be qualified accordingly."

  > "Six of these papers benchmark on a single dataset (D); cross-
  >  dataset generalization remains under-tested."

  > "The field has converged on a small set of evaluation metrics
  >  (M1, M2); replication studies have not yet broken with this
  >  consensus."

If no methodological pattern stands out, omit this section.>>

---

## Limitations of this briefing

<<2-3 sentences honestly stating:
  - What sources were and weren't searched.
  - Whether the search was offline (model knowledge only).
  - Whether the topic spans multiple disciplines, only one of which
    was covered.
  - Whether the year range may have missed recent or foundational
    work.>>

---

## Next steps

- Read the curated reading list: `reading-list.md`.
- Use the bibliography for paper-writing:

  ```
  /research "<<Topic>>" --bibliography <<path>>/bibliography.yaml --style <<style>>
  ```

- Resolve any unverified items: see `Known-gaps.md`.
- For deeper coverage, re-run with a higher `--n` or `--depth deep`.
```

---

## Generation rules

1. **Cite-key validation.** Every cite_key in the briefing must appear
   in `bibliography.yaml`. The orchestrator validates this at emission
   time.
2. **Audience adjustment.** The orchestrator passes `--audience` into
   the briefing prompt; the language register is set there.
3. **Length budget.** Strictly enforced (1 paragraph for `standard`;
   3 paragraphs for `deep`). If the model produces more, trim by
   dropping the trajectory section first, then the methodological
   notes.
4. **Reading-level check.** For `--audience general`, run a Flesch–
   Kincaid check; reject and retry if grade > 12.
5. **No new sources.** The briefing only cites papers in the reading
   list. Hallucinated sources are flagged in `Known-gaps.md` and the
   briefing is regenerated.

---

## Anti-patterns

- ❌ Listing papers one by one. The briefing is a synthesis, not a
  list.
- ❌ Three-item lists with empty adjectives ("efficient, effective,
  elegant"). Be specific.
- ❌ "More research is needed" without naming the specific gap.
- ❌ Ending with a forward-looking grand claim. Keep the trajectory
  paragraph grounded in cited papers.
- ❌ Citing the cited-by count or quality score in the briefing prose.
  Those are metadata; the briefing is about content.
