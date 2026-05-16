# Academic Quality Rubric

Used by `workflows/review-pipeline.md` to score papers across nine
dimensions on a 1–5 scale. Each dimension has explicit anchors so scoring
is reproducible across reviewers (and personas).

| Score | General meaning            |
| ----- | -------------------------- |
| 5     | Exemplary — model paper     |
| 4     | Strong — minor improvements |
| 3     | Acceptable — needs revision |
| 2     | Weak — major revision        |
| 1     | Insufficient — likely reject |

A paper passes the quality gate when the **mean score ≥ 4.0** with **no
dimension scoring < 3** and **no high-severity validation issues open**.

---

## 1. Question / motivation

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | The research question is precise, important, and clearly framed against a substantive gap with explicit citations. |
| 4     | The question is clear and the gap is named; framing could be sharper.           |
| 3     | The question is identifiable but stated only implicitly; the gap is generic.    |
| 2     | The question is vague or buried; the motivation is restated platitudes.         |
| 1     | No clear research question; the paper feels like a deliverable, not a study.    |

## 2. Methodology rigor

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Method matches the question; sampling, instruments, analyses pre-specified; assumptions checked; threats to validity addressed. |
| 4     | Method is sound; one or two minor gaps (e.g., effect-size justification light). |
| 3     | Method is broadly appropriate but missing one important element (power analysis, validity threats, or assumption checks). |
| 2     | Method has serious flaws (mismatched test, no sample-size justification, missing controls). |
| 1     | Method is unjustifiable for the question or unreproducible from the description. |

## 3. Results

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Results are clear, statistically sound, with effect sizes + CIs, and well-supported figures / tables. Robustness checks present. |
| 4     | Results are clear with most statistical reporting; minor missing pieces.        |
| 3     | Results are interpretable but one or more findings lack effect size, CI, or robustness check. |
| 2     | Results are confusing or rely on a single underpowered test; no robustness checks. |
| 1     | Results are unsupported by the analysis or contradict the figures.              |

## 4. Discussion / contribution

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Discussion connects findings to prior work, theory, and practice; contribution is concrete and novel. |
| 4     | Contribution clear; comparison to prior work could go further.                  |
| 3     | Contribution stated but not differentiated sharply from existing work.          |
| 2     | Contribution overclaimed or ill-defined; comparison to prior work superficial.  |
| 1     | No clear contribution; the paper restates findings without interpretation.      |

## 5. Limitations / honesty

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | At least three specific limitations, each with assessed impact and mitigation pointers; null findings honestly framed. |
| 4     | Several specific limitations; minor over-claim or under-claim noted.             |
| 3     | Generic limitations ("more work needed") rather than specific ones.             |
| 2     | Limitations buried, downplayed, or absent for obvious threats.                  |
| 1     | Overclaiming throughout; the paper hides weaknesses.                             |

## 6. Citations / prior work

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Comprehensive, balanced, integrated citation; landmark and recent work both present; no citation laundering. |
| 4     | Comprehensive; minor missing related work or one cite-laundering smell.          |
| 3     | Coverage adequate but skewed (one school, one timeframe).                        |
| 2     | Important related work missing; citations dropped rather than integrated.         |
| 1     | Bare or fabricated bibliography; key prior work absent.                          |

## 7. Figures / tables

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Figures and tables tell the story on their own; captions interpret; all standards in `references/visualization-guide.md` met. |
| 4     | Figures effective; minor caption / labeling issues.                              |
| 3     | Figures present but under-interpreted; some standards violated (axis units missing, palette not colorblind-safe). |
| 2     | Figures decorative rather than informative; many standards violated.             |
| 1     | Figures missing, broken, or actively misleading (truncated y-axes, 3-D bars, pie > 4 slices). |

## 8. Writing / clarity

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Reads cleanly end-to-end; transitions explicit; jargon defined; voice consistent; no AI clichés. |
| 4     | Reads well; occasional dense passage or stacked clichés.                         |
| 3     | Mostly readable but several confusing sections, undefined acronyms, or stacked clichés. |
| 2     | Frequent confusing passages; voice inconsistent; reader has to work hard.        |
| 1     | Hard to follow; AI-generated tells throughout; reader gives up.                  |

## 9. Reproducibility

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Code, data, environment, seeds, hyperparameters, and hardware all documented; another researcher could replicate. |
| 4     | Most elements documented; one or two minor gaps.                                  |
| 3     | Significant gap (no environment file, or no seeds, or no hyperparameter table). |
| 2     | Multiple gaps; replication would be hard even with author help.                  |
| 1     | No reproducibility information; effectively unreplicable.                        |

---

## Aggregate score

```
overall = mean(question, methodology, results, discussion, limitations,
               citations, figures, writing, reproducibility)
```

**Decision rule** (mirrors `workflows/review-pipeline.md`):

- Mean ≥ 4.0 AND no dim < 3 AND no high-severity validation issue → **Accept with minor revisions**.
- Mean 3.0–4.0 OR any dim < 3 OR any high-severity validation issue → **Major revision required**.
- Mean < 3.0 → **Reject**.

---

## How to score during review

1. Read the paper end-to-end first. Do not score on the fly.
2. For each dimension, write **2–3 evidence sentences** before scoring,
   citing specific section / line numbers.
3. Score from the anchors, not from a global "how do I feel about this"
   sense.
4. If between two scores, take the lower one and explain in the evidence.
5. Save evidence in `review/<persona>-evidence.md` so the score is
   auditable.

---

## Anti-gaming

- A paper cannot earn a 5 in a dimension while also having a high-severity
  validation issue in that dimension.
- The reviewer must produce **at least one specific, actionable revision
  request** even for a 5-scoring dimension (something to make it even
  better).
- The reviewer must produce **at least two specific revision requests**
  for any dimension scoring ≤ 3.
- Suggestions of "needs more work" without specificity are rejected by
  the aggregator.
