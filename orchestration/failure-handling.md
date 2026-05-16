# Failure Handling

Every phase of the orchestration has expected failure modes. This file
documents the failure matrix and the recovery protocol for each.

> **Posture:** never fail silently. Every failure either auto-recovers
> or surfaces in `Known-gaps.md` with a recommended fix.

---

## 1. Universal recovery protocol

For any failure:

1. **Capture context.** Write the error, the inputs, and the agent's
   state to `validation/errors.md`.
2. **Try one safe retry.** Re-run the failing step with the same inputs.
3. **Try a degraded retry.** Reduce scope (smaller chunk, fewer
   sources, simpler chart) and re-run.
4. **Persist what you have.** Save partial output to disk with a
   `[PARTIAL]` marker.
5. **Surface to user.** Add a `Known-gaps.md` entry with the failure,
   the partial state, and a concrete fix.

Never abandon a run mid-orchestration without writing `Known-gaps.md`.

---

## 2. Phase-by-phase failure matrix

### 2.1 Intake / scoping

| Failure                                | Recovery                                                |
| -------------------------------------- | ------------------------------------------------------- |
| Request fundamentally ambiguous        | Ask user **once**, then proceed with best guess.       |
| Out-of-scope request                   | Narrow to a focused paper; list dropped sub-topics in `Future work`. |
| Conflicting instructions               | Surface conflict; pick the more specific instruction.   |

### 2.2 Literature review

| Failure                                | Recovery                                                |
| -------------------------------------- | ------------------------------------------------------- |
| Web search unavailable                  | Use model-known citations; mark every entry `[UNVERIFIED — offline]`; surface in `Known gaps`. |
| Search returns < target count          | Lower minimum, document in methodology, add to `Known gaps`. |
| All sources are old (> 5 years)         | Note the field-pace mismatch; add an "Open challenge" sub-section. |
| Sources contradict                     | Add explicit "Contradictions in the literature" sub-section. |
| Found a retracted paper                 | Drop it; replace with a non-retracted source; flag in report. |

### 2.3 Methodology

| Failure                                | Recovery                                                |
| -------------------------------------- | ------------------------------------------------------- |
| Method doesn't match question          | Re-pick from `methodology_engine/frameworks.md`.        |
| n below floor                          | Document as limitation; switch to non-parametric tests if applicable; mark `[UNDERPOWERED]`. |
| Required ethics statement missing       | Add placeholder; flag in `Known gaps`.                  |
| Unable to reach reproducibility minimums | Mark `[REPRODUCIBILITY GAP]`; surface specifically.    |

### 2.4 Data analysis

| Failure                                | Recovery                                                |
| -------------------------------------- | ------------------------------------------------------- |
| Dataset corrupted / unreadable         | Stop; ask user to re-export.                            |
| Outcome variable not in data           | Stop; suggest closest column names.                     |
| Statistical assumptions violated        | Try transformation; switch to non-parametric; report what was tried. |
| n very small                           | Switch to non-parametric defaults; mark `[UNDERPOWERED]`. |
| Severe missingness (> 50%)              | Warn; recommend dropping variable or using MI.          |
| Python deps missing                    | Fall back to Markdown tables; flag in `Known gaps`.     |
| Hypothesis test fails / null result     | Report null honestly; add post-hoc power calculation.    |

### 2.5 Visualization

| Failure                                | Recovery                                                |
| -------------------------------------- | ------------------------------------------------------- |
| matplotlib unavailable                 | Render Mermaid diagram or Markdown table; flag and continue. |
| Geographic data missing                | Skip choropleth; use a region-grouped table; flag.      |
| Too many categories for chart          | Switch to long-form table; flag.                        |
| Figure caption inferred poorly         | Auto-generate placeholder; the writer agent refines it. |

### 2.6 Drafting

| Failure                                | Recovery                                                |
| -------------------------------------- | ------------------------------------------------------- |
| Section drifts off-spec                | Reject; re-prompt the writer with stricter constraints. |
| AI clichés detected                    | Apply the AI-cliché filter from `instructions/voice-and-tone.md`. |
| Section length way off target          | Re-prompt with explicit word budget.                   |
| Cross-section inconsistency             | Run a final cover-to-cover pass; reconcile.             |
| Hits context limit mid-section         | Switch to multi-file output; persist what you have.     |
| Hits context limit across paper         | See `long_context/strategy.md`.                         |

### 2.7 Citations

| Failure                                | Recovery                                                |
| -------------------------------------- | ------------------------------------------------------- |
| Missing cite_keys in draft              | Halt; surface to user / writer agent for correction.    |
| Mixed citation styles detected          | Re-run citation pipeline with single `--style`.         |
| Duplicate references                    | Auto-merge per `citation_engine/deduplication.md`.      |
| Incomplete entry                       | Mark `[INCOMPLETE]`; flag missing fields.               |
| DOI fails to resolve                    | Mark `[UNVERIFIED]`; suggest manual verification.       |

### 2.8 Validation

| Failure                                | Recovery                                                |
| -------------------------------------- | ------------------------------------------------------- |
| **High** severity issue (test mismatch, retracted citation, missing key) | Halt; route back to the relevant agent with the error. |
| **Medium** severity issue              | Auto-fix where possible; surface the rest in `Known gaps`. |
| **Low** severity issue                 | Surface only; let the reviewer decide.                   |

### 2.9 Review

| Failure                                | Recovery                                                |
| -------------------------------------- | ------------------------------------------------------- |
| Reviewer score < 3.0 overall           | Block delivery; apply revisions; re-validate; re-review.|
| Reviewers disagree fundamentally        | Surface the disagreement; let the user decide.          |
| One persona produces an unusable review | Re-run that persona with stricter rubric anchors.       |

### 2.10 Final assembly

| Failure                                | Recovery                                                |
| -------------------------------------- | ------------------------------------------------------- |
| Pandoc / LaTeX export fails            | Deliver Markdown only; flag the export issue.            |
| Image asset missing                     | Use Mermaid fallback; flag.                              |
| Index file generation fails             | Generate basic listing; flag.                            |

---

## 3. Catastrophic recovery

If the orchestration crashes mid-run:

1. The working directory is the source of truth — every artifact is
   already on disk.
2. Restart the orchestration; it will detect existing artifacts and
   skip completed phases (`workflows/` files are idempotent).
3. If the working directory is corrupted, the user can re-run from
   `paper-spec.md`.

---

## 4. The `Known-gaps.md` contract

This file is the **single place** where unresolved issues are surfaced
to the user. Every gap entry has the form:

```markdown
- **[GAP TYPE]** — Section X.Y, brief description.
  *Severity:* high / medium / low.
  *Recommended fix:* <concrete action>.
  *Affected artifacts:* <list of files>.
```

Standard gap types:
- `[CITATION NEEDED]` — claim without a source.
- `[UNVERIFIED]` — citation could not be resolved.
- `[INCOMPLETE METADATA]` — required field missing.
- `[REPRODUCIBILITY GAP]` — code / data / seed missing.
- `[UNDERPOWERED]` — n below floor.
- `[OVERCLAIM]` — causal language without causal design.
- `[SYNTHETIC DATA]` — illustrative dataset substituted.
- `[CONTEXT LIMIT]` — section had to be split / shortened.
- `[TOOLING DEGRADED]` — Python / web tools unavailable.
- `[VENUE-SPECIFIC]` — venue rule could not be auto-applied.

The user reviews `Known-gaps.md` and addresses each item before
submission.

---

## 5. When to ask the user

The skill should ask the user **only** when:

1. The intent is fundamentally ambiguous (multiple plausible formats /
   styles).
2. A required input is missing (e.g., dataset path was promised but
   not provided).
3. The path forward involves a decision the user must own (e.g.,
   "do we drop this contradicting source or include it?").
4. A high-severity failure cannot be auto-recovered.

Default to **proceeding with best guesses** and surfacing the choices
in `paper-spec.md → defaults_assumed`. Constant clarification requests
break the autonomous experience.
