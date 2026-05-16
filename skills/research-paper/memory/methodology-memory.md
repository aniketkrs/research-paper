# Methodology Memory Protocol

How to persist methodology decisions across drafting, validation,
review, and revision so they remain consistent end-to-end.

---

## 1. The methodology contract

After the methodology phase, the orchestrator writes
`methodology.md`. This file is the **frozen contract** for everything
downstream. It contains:

```markdown
# Methodology

## 1. Research design
- Type: <quantitative | qualitative | mixed | systematic-review | design-science>
- Sub-type: <RCT | case-study | grounded-theory | meta-analysis | ...>
- Justification: <why this design fits the question>

## 2. Sampling
- Population: ...
- Frame: ...
- Method: <random | stratified | cluster | convenience>
- Size: n = ...
- Power calculation: <a priori, alpha=0.05, power=0.80, expected d=0.5>

## 3. Variables / constructs
- IV: ...
- DV: ...
- Controls: ...
- Mediators / moderators: ...

## 4. Instruments / measures
| Construct | Items | Source | Cronbach's α |
| --- | --- | --- | --- |
| X | 6 | Smith (2018) | .87 |
| ... | ... | ... | ... |

## 5. Procedure
1. Step 1
2. Step 2
...

## 6. Statistical analysis plan
- Pre-registered: <yes | no | partial>
- Primary tests: ...
- Assumption checks: ...
- Multiple-comparison correction: ...
- Effect size + 95% CI: required

## 7. Threats to validity
- Internal: ...
- External: ...
- Construct: ...
- Conclusion: ...

## 8. Reproducibility
- Code: <URL or "available on request">
- Data: <URL or "available on request">
- Environment: <requirements.txt | Dockerfile | conda env>
- Seeds: [13, 17, 23, 31, 37]
- Hardware: <CPU, GPU, RAM>
- Wall-clock estimate: ...

## 9. Ethics
- IRB approval: <number or "not required">
- Consent: ...
- Anonymization: ...
- Conflicts of interest: ...
```

---

## 2. Why "frozen"

After methodology is finalized:

- The Analyst executes per the analysis plan in §6.
- The Writer cites the methodology section verbatim.
- The Validator checks results against the assumption checks.
- The Reviewer verifies threats-to-validity coverage.

If the methodology changes mid-run, all downstream artifacts may
become inconsistent. So changes are **explicitly tracked**:

```markdown
## Methodology change log
- 2024-05-12T14:30: Switched primary test from t-test to Welch's t-test
  after Levene's test indicated heteroscedasticity. Effect size
  recomputed: d unchanged.
- 2024-05-12T15:42: Excluded 4 participants for missing pre-scores
  per §10 of the analysis plan. n_A: 119, n_B: 117.
```

The orchestrator appends to this log; never silently overwrites.

---

## 3. Loading patterns

| Phase             | What's loaded                                       |
| ----------------- | --------------------------------------------------- |
| Methodology       | Read full + write                                   |
| Data analysis     | Read full (the analyst executes per §6)             |
| Visualization     | Read §1, §3, §6 (for what to plot and how)           |
| Drafting (Methodology section) | Read full (for prose generation)            |
| Drafting (Results section)     | Read §6 + §7 + analysis findings              |
| Drafting (Discussion)          | Read §3, §7 + §8 (validity, reproducibility)  |
| Validation        | Read full                                          |
| Review            | Read full                                          |

---

## 4. Cross-paper continuity

For thesis chapters or paper series sharing a methodology:

```
thesis/
├── methodology.md                    ← parent methodology
├── chapter-1/
│   ├── methodology.md               ← chapter-specific overrides
│   └── ...
├── chapter-2/
│   ├── methodology.md
│   └── ...
└── ...
```

The orchestrator detects parent / child layout and reads the parent
first, then overlays the child overrides. Conflicts are resolved by
preferring the child's value (most specific wins).

---

## 5. Methodology validation hooks

The methodology file is checked at three points:

1. **Authoring** — by the Methodologist agent against
   `methodology_engine/frameworks.md` and the question type.
2. **Pre-analysis** — by the Validator that the analysis plan is
   complete and the tests are defensible
   (`validators/methodology-validator.md`).
3. **Final review** — by the Methodologist persona of the reviewer
   (`review_pipeline/three-personas.md`).

Each hook reads `methodology.md` and produces a per-phase verdict.

---

## 6. When the methodology has to change

Real-world reasons a methodology might need post-hoc revision:

- Assumption-check failures (e.g., normality violation).
- Sample size insufficient → switch to non-parametric.
- Pre-registered analysis isn't executable (e.g., predictor lacks
  variation).
- Reviewer flags a critical flaw.

When this happens:

1. Append to the methodology change log (§2 above).
2. Update the affected sub-section in `methodology.md`.
3. Re-run downstream phases that depend on the change:
   - If statistical method changed → re-run analysis.
   - If sample size changed → re-run power analysis + analysis.
   - If validity threats changed → re-write threats subsection.
4. Regenerate `paper-cited.md` and re-validate.

The change log makes this auditable.

---

## 7. Honest reporting of changes

If methodology changed during a run, the paper itself must say so.
Add to the Limitations section:

> "Note: the analysis plan was modified after data collection. Specifically,
> [description of change]. The original plan called for [original]; this
> was adjusted because [reason]. The change is documented in the
> methodology change log (Appendix X)."

This is the difference between honest method evolution and HARKing
(Hypothesizing After Results are Known).

---

## 8. Frozen artifacts that depend on methodology

These all become "stale" if methodology changes:

- `analysis/findings.md`
- `analysis/hypothesis-tests.md`
- `paper-cited.md` (sections §3 and §6 specifically)
- `validation/statistical-issues.md`
- `review/methodologist-review.md`

The orchestrator marks each with a `[STALE — re-run after methodology change]`
flag and re-runs them in dependency order.
