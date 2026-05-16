# Validation Pipeline

Last automated gate before human / simulated peer review. Catches the
**fixable** errors so the review pipeline can focus on argument and
contribution. Called from `workflows/research-orchestration.md §9`.

> **Posture:** be pedantic. Better to flag a false positive than miss a
> real problem. Every flag includes a severity (**high / medium / low**)
> and a recommended fix.

---

## 1. Inputs

- `paper-cited.md` — the cited paper (output of citation pipeline).
- `bibliography.yaml` — single source of truth for references.
- `analysis/` — data analysis outputs (if present).
- `figures-plan.md` — what figures / tables were planned.
- `paper-spec.md`, `outline.md` — the original plan to compare against.

---

## 2. Validators (run sequentially)

### 2.1 Structural validator

Checks the paper has every section required by the chosen template:

- Read template from `templates/<format>.md`.
- Confirm every numbered section / subsection in the template has a
  corresponding heading in `paper-cited.md`.
- Confirm the `must_include_sections` from `manifest.json` are all present.
- Flag missing sections as **high severity**.

### 2.2 Citation validator (`scripts/validate_citations.py`)

For each in-text citation:
- The cite key (or `[N]`) maps to a reference list entry.
- The reference entry has the minimum required fields for its type.
- DOI / URL is well-formed (and resolves, if web tools available).
- The citation style is consistent throughout (no mixing of `(Smith, 2023)`
  with `[1]`).

For each reference list entry:
- It is cited at least once in the body (otherwise: orphan, **medium**).
- It is not a duplicate (otherwise: **high**, merge required).
- Authors / year / title are populated.

Outputs `validation/citation-issues.md`.

### 2.3 Statistical validator (`scripts/statistical_validation.py`)

Scans the paper for statistical claims and re-checks them against the
analysis output.

Pattern matches:
- `t(<df>) = <stat>, p = <pval>` → confirm against `analysis/hypothesis-tests.csv`.
- `F(<df1>, <df2>) = <stat>, p = <pval>` → ANOVA result lookup.
- `r = <stat>, p = <pval>` → correlation lookup.
- `χ²(<df>) = <stat>, p = <pval>` → chi-squared lookup.
- `OR = <stat>, 95% CI [<lo>, <hi>]` → odds-ratio lookup.

For each match:
- Verify the test stat, df, p, and effect size match the analysis output
  within rounding tolerance.
- If the paper reports a p-value but no effect size, flag **medium**
  ("missing effect size — see `references/statistical-methods.md §3`").
- If the paper reports an effect size but no CI, flag **medium**.
- If a paired test is used but the analysis script ran an unpaired test,
  flag **high** ("test mismatch").

Also runs:
- **Power audit**: for every reported test, if n is below the floor in
  `references/statistical-methods.md §10`, flag **medium** ("underpowered").
- **Multiple-comparison audit**: count the number of p-values reported in
  each table. If > 1 and no correction is mentioned, flag **medium**.

Outputs `validation/statistical-issues.md`.

### 2.4 Visualization validator

For each figure / table referenced in the paper:
- The figure / table exists in `figures/` or `tables/`.
- The numbering is sequential (no gaps, no duplicates).
- It is referenced in the text **before** it appears.
- The caption is interpretive (not just descriptive — heuristic: caption
  contains a verb like "shows", "indicates", "outperforms", and is
  ≥ 2 sentences).
- For figures with axes: alt-text / caption mentions axis labels and units.

Outputs `validation/visual-issues.md`.

### 2.5 Reading-level validator

- Compute Flesch–Kincaid grade for the **plain-English summary**.
- Target: ≤ grade 10. If higher, flag **medium** with suggested rewrite.
- Also compute reading level for the abstract (target: ≤ grade 14).
- Compute readability for each section; flag any section with grade > 18
  ("too dense") or grade < 8 ("too informal for academic prose").

Outputs `validation/readability-issues.md`.

### 2.6 Consistency validator

- Acronyms: every acronym is defined on first use in each major section.
- Numbers: integers ≤ 9 spelled out vs. ≥ 10 in digits — consistent.
- Units: SI vs. imperial — consistent. Non-breaking spaces between
  numerals and units.
- Terminology: variant spellings of the same term flagged ("preprocess"
  vs. "pre-process"; "data set" vs. "dataset" — pick one).
- Figure / table / equation numbering: sequential.

Outputs `validation/consistency-issues.md`.

### 2.7 AI-cliché / weak-prose detector

Scans for:
- "It is well known that"
- "In today's fast-paced / digital age / rapidly evolving"
- "Revolutionary / groundbreaking / cutting-edge / paradigm shift"
- "Delve / delving"
- "Tapestry"
- Stacks of "Furthermore, …; Moreover, …; Additionally, …"
- "Multifaceted approach"
- "Navigate the complexities of"
- Three-item lists with empty adjectives ("efficient, effective, elegant")

Each occurrence flagged **low** with a rewrite hint.

Outputs `validation/style-issues.md`.

### 2.8 Hedging audit

For every causal claim, check whether the methodology supports causal
inference:
- Pure observational data + claim of "causes" / "leads to" / "results in"
  → flag **high** ("causal language without causal design").
- Single experiment + sweeping generalization → flag **medium**
  ("over-generalization").

Conversely, for every weakly hedged finding:
- "may potentially possibly suggest" → flag **low** ("over-hedging — pick
  one hedge").

Outputs `validation/hedging-issues.md`.

### 2.9 Fabrication / hallucination audit

If web tools are available:
- Resolve every DOI; flag unresolved ones **high**.
- Confirm titles / authors match Crossref / arXiv metadata.
- Cross-check Retraction Watch.

If web tools are not available:
- Every citation marked `[UNVERIFIED — offline]` is listed in
  `validation/unverified.md` for the user to verify before submission.

Outputs `validation/fabrication-issues.md`.

### 2.10 Reproducibility validator

Confirm presence of:
- Data availability statement.
- Code availability statement (URL or "available on request").
- Random seeds reported.
- Hyperparameters listed.
- Hardware reported.
- Environment file referenced.

Each missing item flagged **medium**.

Outputs `validation/reproducibility-issues.md`.

---

## 3. Aggregation

`validation/validation-report.md` is the consolidated report:

```markdown
# Validation report

Generated: 2024-05-12 14:23 UTC
Paper: paper-cited.md
Bibliography: bibliography.yaml

## Summary

| Severity | Count |
| -------- | ----- |
| High     | 2     |
| Medium   | 7     |
| Low      | 14    |
| Total    | 23    |

## High-severity issues

1. **Statistical test mismatch (§5.3, H1)** — paper reports paired t-test
   but `analysis/hypothesis-tests.csv` shows independent t-test was run.
   *Fix:* re-run the correct test or correct the paper.

2. **Citation [smith2018llm] resolves to a retracted paper** —
   Retraction Watch entry: …
   *Fix:* remove the citation or replace with a non-retracted source.

## Medium-severity issues

(... 7 items ...)

## Low-severity issues

(... 14 items ...)
```

---

## 4. Auto-fix vs. surface-only

| Issue type                          | Action                                |
| ----------------------------------- | ------------------------------------- |
| Missing effect size next to a p     | Compute from analysis output and insert; flag if not derivable. |
| Inconsistent acronym capitalization  | Auto-fix to first-use spelling.       |
| AI-cliché phrase                     | Surface a rewrite suggestion; let writer agent apply. |
| Citation in wrong style              | Auto-fix via re-run of citation pipeline. |
| Unsupported causal claim              | Surface only; requires human/writer judgment. |
| Retracted citation                    | Surface only; requires replacement decision. |
| Underpowered analysis                 | Surface only; cannot retroactively add data. |

Auto-fixes are logged in `validation/auto-fixes.md` so they're auditable.

---

## 5. CLI

```bash
python scripts/validate_citations.py     paper-cited.md bibliography.yaml \
       --report validation/citation-issues.md

python scripts/statistical_validation.py paper-cited.md \
       --analysis analysis/ \
       --report validation/statistical-issues.md

python scripts/extract_references.py     paper-cited.md \
       --bib bibliography.yaml \
       --report validation/orphan-and-missing.md
```

A wrapper script `scripts/validate_all.sh` (or `.ps1`) runs every validator
and aggregates into `validation/validation-report.md`.

---

## 6. Exit conditions

- Any **high-severity** issue: the orchestrator halts and prompts the
  writer agent / user.
- Only **medium / low** issues: the orchestrator may proceed to the review
  pass, but copies the unresolved items into the paper's `Known gaps`
  block.
- Zero issues: proceed to review pass.

---

## 7. Why this is separate from the review pass

The validator catches **mechanical** errors (missing fields, wrong tests,
broken numbering, fabricated references). The review pass (next workflow)
evaluates **substantive** quality (argument, contribution, framing). Mixing
them produces noisy feedback. The validator runs first; the reviewer reads
a paper that's already mechanically clean.
