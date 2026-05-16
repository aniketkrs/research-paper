# Known-Gaps Protocol

The skill never fails silently. Every issue that cannot be auto-
resolved surfaces in `Known-gaps.md` at the end of the working
directory, with a fixed structure that lets the user act on each item
without further analysis.

---

## 1. Format

Every gap is a Markdown bullet with this shape:

```markdown
- **[GAP TYPE]** — Section X.Y, brief description.
  - *Severity:* high / medium / low
  - *Recommended fix:* <concrete action>
  - *Affected artifacts:* <comma-separated paths>
  - *Detected by:* <agent / validator name>
```

`Known-gaps.md` is a flat list of these bullets, grouped by severity.

---

## 2. Standard gap types

| Type                     | Meaning                                                 | Default severity |
| ------------------------ | ------------------------------------------------------- | ---------------- |
| `[CITATION NEEDED]`       | Claim without a source                                  | medium           |
| `[UNVERIFIED]`            | Citation could not be resolved (offline, dead DOI)      | medium           |
| `[INCOMPLETE METADATA]`   | Required citation field missing                          | medium           |
| `[REPRODUCIBILITY GAP]`   | Code / data / seed / environment missing                | medium           |
| `[UNDERPOWERED]`          | Sample size below floor                                  | medium           |
| `[OVERCLAIM]`             | Causal language without causal design                    | medium           |
| `[SYNTHETIC DATA]`        | Illustrative dataset substituted; replace before publishing | high          |
| `[CONTEXT LIMIT]`         | Section had to be split / truncated                      | medium           |
| `[TOOLING DEGRADED]`      | Python / web tools unavailable; fallbacks used           | low              |
| `[VENUE-SPECIFIC]`        | Venue rule could not be auto-applied                     | low              |
| `[ETHICS PLACEHOLDER]`    | Ethics statement was filled with a placeholder           | high             |
| `[STALE — RE-RUN]`        | Methodology changed; downstream artifact needs refresh    | high             |

---

## 3. Severity → action

| Severity | Orchestrator action                                                |
| -------- | ------------------------------------------------------------------ |
| **High**  | Block delivery until resolved (or explicitly waived by user).      |
| **Medium** | Surface in `Known-gaps.md`; deliver but flag in `index.md` summary. |
| **Low**   | Surface in `Known-gaps.md`; do not block.                            |

---

## 4. Auto-resolution attempts

Before adding a gap to `Known-gaps.md`, the orchestrator tries:

1. **Cheap auto-fix.** E.g., re-run the citation pipeline to fix a
   style mismatch.
2. **Reduced scope.** E.g., switch to non-parametric tests for an
   underpowered analysis.
3. **Fallback.** E.g., Mermaid diagram instead of matplotlib.

Only after these fail does the gap get surfaced.

---

## 5. User waiver protocol

If the user explicitly waives a gap (e.g., "ship it, I'll fix the DOIs
manually"), the orchestrator:

1. Marks the gap as `WAIVED` in `Known-gaps.md`.
2. Records the waiver timestamp and rationale.
3. Proceeds with delivery.

This makes it auditable.

---

## 6. Example `Known-gaps.md`

```markdown
# Known gaps

This paper passes the quality gates with the following caveats. Each
item below should be addressed before submission.

## High severity

- **[SYNTHETIC DATA]** — Section 5 (Experimental Setup), the dataset
  used is an illustrative synthetic substitute (no real-world dataset
  was supplied for this run).
  - *Recommended fix:* Re-run with the actual dataset; verify all
    quantitative results in the Findings section.
  - *Affected artifacts:* analysis/, figures/figure-2.png, sections/04-results.md
  - *Detected by:* analyst

## Medium severity

- **[UNVERIFIED]** — References [3] (smith_2018_review) and [12]
  (lee_2024_arxiv) could not be verified offline.
  - *Recommended fix:* Confirm DOIs / arXiv IDs via Crossref / arXiv
    before submission.
  - *Affected artifacts:* bibliography.yaml, paper-cited.md
  - *Detected by:* citation-validator

- **[INCOMPLETE METADATA]** — Reference doe_2022_codex is missing
  page numbers.
  - *Recommended fix:* Pull page numbers from the published version.
  - *Affected artifacts:* bibliography.yaml
  - *Detected by:* citation-validator

- **[UNDERPOWERED]** — Section 6.2 paired comparison (n = 24, observed
  d = 0.3, post-hoc power = 0.42).
  - *Recommended fix:* Either collect more data or re-frame this
    finding as exploratory.
  - *Affected artifacts:* analysis/hypothesis-tests.md, sections/04-results.md
  - *Detected by:* statistical-validator

## Low severity

- **[TOOLING DEGRADED]** — matplotlib unavailable; figures rendered as
  Mermaid diagrams and Markdown tables. The paper is fully readable;
  for journal submission, re-run with a Python environment that has
  pandas + matplotlib + seaborn installed.
  - *Recommended fix:* Install Python deps and re-run
    `toolchains/generate_charts.py`.
  - *Affected artifacts:* figures/
  - *Detected by:* visualizer
```

---

## 7. Integration with the publication checklist

The publication checklist (`quality_control/publication-checklist.md`)
runs as the final gate. Any unchecked item that cannot be auto-fixed
is automatically converted into a `Known-gaps.md` entry.

This means the user only needs to read **one file** (`Known-gaps.md`)
to see every outstanding issue.

---

## 8. Why this matters

Most papers fail at the submission stage because of small mechanical
issues (a malformed citation, a missing author affiliation, a
forgotten ethics statement). The Known-gaps protocol surfaces these
**before** the user sends the paper out — turning the skill from "AI
that writes papers" into "AI that helps the user ship papers".

This is the difference between a demo and a production system.
