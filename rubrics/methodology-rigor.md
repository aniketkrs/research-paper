# Methodology Rigor Rubric

Used by Persona A (the methodologist) in `workflows/review-pipeline.md`.
Each dimension is scored 0–5 with anchors below. Mean across dimensions
gives the methodology rigor score for `rubrics/academic-quality.md §2`.

---

## 1. Research design

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Design clearly matches the question; design type explicitly named (RCT / quasi-experimental / cross-sectional / SLR / design science). |
| 4     | Design appropriate; type implicit but inferable.                                |
| 3     | Design adequate but mismatched to the most ambitious claim.                     |
| 2     | Design weak (e.g., correlational data + causal claim).                          |
| 1     | No coherent design.                                                            |

## 2. Sampling and recruitment

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Sampling frame, method, and recruitment fully reported; representativeness justified. |
| 4     | Most elements present; minor gap.                                                |
| 3     | Sample described but not justified.                                              |
| 2     | Convenience sample with no acknowledgment of bias.                              |
| 1     | Sampling not described.                                                         |

## 3. Sample size and power

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | A priori power analysis with α, expected effect, target power; n meets the floor in `references/statistical-methods.md §10`. |
| 4     | Power analysis present; minor inconsistency.                                    |
| 3     | Sample size reported but not justified; n meets floor.                           |
| 2     | n below floor; no power analysis.                                                |
| 1     | n very small (e.g., < 30 for two-sample t) and unaddressed.                     |

## 4. Operationalization

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Every construct operationalized with a validated instrument or rigorous custom measure (with reliability evidence). |
| 4     | Most constructs validated; one custom measure not piloted.                      |
| 3     | Constructs operationalized but reliability not reported.                         |
| 2     | Mismatched constructs and measures (e.g., self-report for an objective construct). |
| 1     | Operationalization unclear.                                                     |

## 5. Statistical methods

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Tests appropriate; assumptions checked; multiple-comparison correction; effect sizes + 95% CIs. |
| 4     | Mostly correct; minor reporting gap.                                            |
| 3     | Tests appropriate but missing one of: assumption check, correction, effect size, CI. |
| 2     | Wrong test for the data; or assumptions clearly violated.                        |
| 1     | Statistical methods unjustifiable.                                              |

## 6. Reporting

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Every reported test follows the template in `references/statistical-methods.md §7`. |
| 4     | Most tests; one or two missing CIs or n.                                        |
| 3     | Many tests under-reported.                                                      |
| 2     | "p < .05" without effect size or n.                                             |
| 1     | Numbers reported without test names or denominators.                             |

## 7. Threats to validity

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | All four (internal / external / construct / conclusion) validity threats identified and addressed. |
| 4     | Three covered; one absent.                                                       |
| 3     | Two covered.                                                                     |
| 2     | Generic "limitations" stub without specific threats.                             |
| 1     | No threats acknowledged.                                                        |

## 8. Reproducibility

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Full reproducibility statement: code repo + commit, data URL, environment file, seeds, hyperparameters, hardware, runtime. |
| 4     | Most elements; one minor gap.                                                    |
| 3     | Code or data present, but missing seeds / hyperparameters / environment.         |
| 2     | Code "available on request" with no other detail.                                |
| 1     | No reproducibility info.                                                        |

## 9. Ethics

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | IRB / ethics approval cited; consent procedure described; anonymization detailed; conflicts of interest disclosed. |
| 4     | Most elements present; minor missing piece.                                     |
| 3     | IRB cited but no consent procedure detail.                                      |
| 2     | Ethics review absent for human-subjects work.                                   |
| 1     | Ethics not addressed where required.                                             |

## 10. Honest reporting of nulls

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Nulls are reported with the same rigor as significant findings; equivalence testing or post-hoc power discussed. |
| 4     | Nulls reported but not contextualized with power.                                |
| 3     | Some nulls reported.                                                             |
| 2     | Nulls hinted at but not quantified ("did not differ").                          |
| 1     | Nulls hidden or never tested for.                                                |

---

## Composite

```
methodology_rigor_score = mean of the 10 dimensions above
```

If any dimension scores 1, the methodologist persona must mark this as a
**high-severity** revision request regardless of mean.

---

## Worked example

For a paper that:
- States a clear RCT design (5)
- Describes n = 200 across two arms with power analysis (5)
- Uses validated scales with α reported (4)
- Uses Welch's t-tests with Holm correction, effect sizes + CIs (5)
- Reports per template (5)
- Acknowledges three of four validity threats (4)
- Has full reproducibility statement (5)
- IRB cited but no consent detail (3)
- Reports nulls with post-hoc power (5)
- Sampling described but representativeness not justified (3)

Mean = (5+3+5+4+5+5+4+5+3+5) / 10 = 4.4 → strong methodology, with two
specific revisions (sampling justification; consent procedure detail).
