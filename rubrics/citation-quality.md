# Citation Quality Rubric

Used by `workflows/validation-pipeline.md` and Persona B
(domain expert) in `workflows/review-pipeline.md`. Scores 0–5 with
anchors below.

---

## 1. Coverage

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Comprehensive coverage of relevant prior work, balanced across schools, eras, and methods. |
| 4     | Comprehensive but one school / era light.                                       |
| 3     | Adequate coverage; misses one important sub-area.                                |
| 2     | Coverage skewed (recent only, single group, single sub-area).                    |
| 1     | Sparse coverage; missing landmark / canonical citations.                         |

## 2. Source quality

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | All sources peer-reviewed or reputable grey literature; mean source-quality score ≥ 8. |
| 4     | Mostly peer-reviewed; mean ≥ 7.                                                 |
| 3     | Mix of peer-reviewed and unverified preprints; mean ≥ 5.                          |
| 2     | Heavy reliance on blogs / industry marketing material.                           |
| 1     | Includes predatory or retracted sources.                                         |

## 3. Integration

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Citations are integrated into the prose: works are described, contrasted, synthesized. |
| 4     | Mostly integrated; occasional drop-in citation.                                  |
| 3     | Mixed; many drop-in citations like "(Smith, 2023) (Doe, 2022)".                   |
| 2     | Citations are mostly drop-ins.                                                  |
| 1     | Citations dropped without integration; reads like a citation list.               |

## 4. Density

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Density per section meets the floors in `references/citation-styles.md §11`.    |
| 4     | Density on track; one section light.                                             |
| 3     | Two sections under-cited.                                                        |
| 2     | Multiple sections under-cited (intro < 4 / page; lit-review < 10 / section).     |
| 1     | Skeletal citation throughout.                                                    |

## 5. Style consistency

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Single citation style applied perfectly throughout; reference list well-formatted. |
| 4     | Single style; minor formatting slips.                                            |
| 3     | Single style but several formatting issues (missing italics, wrong year placement). |
| 2     | Mixed styles or many formatting issues.                                          |
| 1     | Inconsistent styles; references list unusable.                                    |

## 6. Triangulation

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Every load-bearing claim cites ≥ 2 independent sources where possible; single-source claims explicitly framed. |
| 4     | Most load-bearing claims triangulated.                                           |
| 3     | Some load-bearing claims rely on a single source without flagging.                |
| 2     | Many single-source claims without flagging.                                      |
| 1     | Most claims hang on individual sources, often the same group's prior work.        |

## 7. Verification

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Every reference resolves (DOI / URL); zero retracted / fabricated.               |
| 4     | All resolve; one or two cite unverified preprints flagged honestly.               |
| 3     | One or two unresolved references.                                                |
| 2     | Several unresolved or inaccurate references.                                     |
| 1     | Includes fabricated references / made-up DOIs.                                   |

## 8. Self-citation balance

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Self-citation reasonable (< 20% of references); not used to inflate the contribution. |
| 4     | Slightly heavy self-citation (~25%) but justifiable.                             |
| 3     | Self-citation noticeable (~30%); some non-essential self-cites.                   |
| 2     | Self-citation heavy; the field's contributions over-attributed to this group.    |
| 1     | Self-citation dominates; obvious echo chamber.                                    |

## 9. Currency

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Recent (≤ 3 yrs) work appropriate to the field's pace, plus foundational older work. |
| 4     | Mostly recent + foundational; one missing landmark.                              |
| 3     | Slightly dated; couple of missing recent works.                                  |
| 2     | Heavily dated for a fast-moving field, or ignores foundational older work in a slow-moving field. |
| 1     | Wrong era throughout.                                                            |

## 10. Reference list completeness

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Every entry has every required field for its type; no orphans; no duplicates.    |
| 4     | One or two entries with a missing minor field.                                    |
| 3     | Multiple entries with missing fields; one orphan.                                  |
| 2     | Many incomplete entries; multiple orphans / duplicates.                            |
| 1     | Reference list unusable.                                                         |

---

## Composite

```
citation_quality_score = mean of the 10 dimensions
```

A high-severity issue (fabricated reference, retracted source, or
fundamentally inconsistent style) caps the score at 2 regardless of
other dimensions.

---

## Auto-generated audit

`scripts/validate_citations.py --rubric` computes most of the dimensions
above automatically:

- Coverage: heuristic (n_unique_authors / n_references).
- Source quality: lookup against the rubric in `references/source-evaluation.md`.
- Density: per-section count vs. floor.
- Style consistency: scanned with regex.
- Verification: DOI / URL resolution where web tools allow.
- Self-citation: requires the user to provide an author-affiliation list.
- Reference list completeness: schema check against
  `schemas/citation-schema.json`.

Manual review fills in: integration, triangulation, currency.

The output is `validation/citation-quality-report.md` with a per-
dimension score and specific revision requests per low-scoring item.
