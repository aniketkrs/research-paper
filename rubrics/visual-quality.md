# Visual Quality Rubric

Used by `workflows/validation-pipeline.md §2.4` and Persona C
(reader) in the review pass. Scores 0–5 with anchors.

---

## 1. Chart-type appropriateness

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Every figure uses the optimal chart type for its data and intent (per `references/visualization-guide.md §1`). |
| 4     | All chart types defensible; one borderline choice.                              |
| 3     | One or two suboptimal choices (e.g., line where bar is better).                  |
| 2     | Multiple inappropriate types.                                                   |
| 1     | Charts actively mislead (3-D bars, pie > 4 slices, etc.).                        |

## 2. Caption quality

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Every caption is interpretive (not just descriptive), follows the four-part pattern (`§8`). |
| 4     | Most captions interpretive; one or two only describe.                           |
| 3     | About half interpretive.                                                         |
| 2     | Mostly descriptive captions ("Figure shows the results.").                       |
| 1     | Captions missing or trivially short.                                              |

## 3. Axes, units, and scales

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | All axes labeled with units; sensible scales; log axes annotated; no truncated y-axes. |
| 4     | All axes labeled; one unit missing.                                              |
| 3     | Some axes missing units or labels.                                              |
| 2     | Several issues (truncated y-axis, missing units, dual y-axis).                   |
| 1     | Charts unreadable due to axis problems.                                          |

## 4. Color and accessibility

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Colorblind-safe palette (Okabe-Ito / viridis); encoding does not rely on color alone. |
| 4     | Colorblind-safe; minor double-encoding gap.                                      |
| 3     | Some figures use rainbow / jet palettes.                                          |
| 2     | Multiple non-accessible figures.                                                 |
| 1     | Red-green only encoding throughout.                                               |

## 5. Numbering and references

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Sequential numbering; every figure / table referenced before it appears.         |
| 4     | Sequential; one or two figures referenced after appearing.                       |
| 3     | One numbering gap.                                                                |
| 2     | Multiple gaps or unreferenced figures.                                            |
| 1     | Numbering inconsistent.                                                          |

## 6. Table craft

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Caption above; numeric columns right-aligned; units in headers; best per column highlighted. |
| 4     | Most rules followed.                                                             |
| 3     | Tables present but several formatting issues.                                    |
| 2     | Tables hard to read.                                                             |
| 1     | Tables embedded as raster images.                                                |

## 7. Information density

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Each figure conveys exactly one idea; multiple ideas split across panels.       |
| 4     | Most figures focused; one over-packed.                                           |
| 3     | A couple of over-packed figures.                                                  |
| 2     | Many over-packed or under-packed figures.                                         |
| 1     | Figures unreadable due to density.                                               |

## 8. Statistical annotation

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Significance marks (`*`, `**`, `***`) explained in captions; error bars labeled (CIs). |
| 4     | Mostly annotated; one figure missing CI explanation.                            |
| 3     | Significance marks present but not explained; or error bars unlabeled.           |
| 2     | No significance marks where multiple comparisons are shown.                       |
| 1     | Error bars conflated with non-error indicators (e.g., SD presented as CI).        |

## 9. Storyboard cohesion

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | A reader looking at figures alone gets the paper's argument.                     |
| 4     | Figures cover most of the argument.                                              |
| 3     | Figures cover the results but not the argument arc.                              |
| 2     | Figures decorate rather than support the argument.                                |
| 1     | Figures unrelated to the argument.                                               |

## 10. Reproducibility of figures

| Score | Anchor                                                                         |
| ----- | ------------------------------------------------------------------------------ |
| 5     | Every figure backed by a CSV in `tables/` and a script in `scripts/`; user could regenerate. |
| 4     | Most backed by sources; one or two manually drawn.                                |
| 3     | About half backed by sources.                                                     |
| 2     | Few sources available; figures could not be regenerated.                          |
| 1     | No source provenance.                                                            |

---

## Composite

```
visual_quality_score = mean of the 10 dimensions
```

The visualization validator (`scripts/validate_charts.py` or the in-pipeline
quality pass) auto-checks dimensions 1, 3, 4, 5, 6, 8, 10. Manual review
covers 2, 7, 9.

Output: `validation/visual-quality-report.md` with per-dimension scores and
revision requests per figure.
