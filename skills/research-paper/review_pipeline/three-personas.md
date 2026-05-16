# Review Pipeline

Final pass before delivery. Simulates a multi-reviewer peer review using
three personas. Called from `workflows/research-orchestration.md §10`.

> **Posture:** generous but uncompromising. Engage the paper charitably;
> assume the authors meant the best version; then identify what would
> actually make it stronger.

---

## 1. Inputs

- `paper-cited.md` — paper after validation.
- `validation-report.md` — known mechanical issues already flagged.
- `paper-spec.md` — original brief.
- `rubrics/*.md` — quality rubrics.

---

## 2. Three reviewer personas

Run **each** persona through the paper sequentially. Each persona:
1. Reads the abstract and section headings only.
2. Reads section by section.
3. Scores against `rubrics/academic-quality.md` and the persona-specific
   rubric.
4. Lists 3–5 most-impactful improvement suggestions.

### 2.1 Persona A — The methodologist

**Lens:** validity, rigor, statistics, reproducibility.

**Rubric used:** `rubrics/methodology-rigor.md`.

**Reads with these questions:**
- Is the research question well-defined?
- Is the design appropriate for the question?
- Is the sample adequate (size, representativeness)?
- Are statistical methods correct, with assumptions checked?
- Are effect sizes and CIs reported?
- Are threats to validity addressed?
- Is the work reproducible from the description?

**Output:** `review/methodologist-review.md` — 5 strengths, 5 weaknesses,
3–5 specific revision requests.

### 2.2 Persona B — The domain expert

**Lens:** framing, prior work, contribution, novelty.

**Rubric used:** `rubrics/academic-quality.md` (framing + contribution
sections).

**Reads with these questions:**
- Is the contribution clearly stated and significant?
- Is the related work coverage appropriate (no major gaps, no orphan
  citations)?
- Is the comparison to prior work fair and complete?
- Are the results convincing in light of what the field already knows?
- Is the claimed novelty actually novel?

**Output:** `review/domain-expert-review.md` — 5 strengths, 5 weaknesses,
3–5 specific revision requests, including missing-citation suggestions.

### 2.3 Persona C — The reader

**Lens:** clarity, narrative, accessibility, writing.

**Rubric used:** `rubrics/academic-quality.md` (clarity + writing
sections).

**Reads with these questions:**
- Could a competent non-specialist follow the argument?
- Are the figures readable and informative?
- Is the abstract self-contained?
- Are transitions between sections smooth?
- Are limitations honest?
- Does the plain-English summary actually work?

**Output:** `review/reader-review.md` — 5 strengths, 5 weaknesses, 3–5
specific revision requests.

---

## 3. Aggregate

`review/review-report.md`:

```markdown
# Review report

## Reviewer scores

| Dimension                | Methodologist | Domain Expert | Reader | Mean |
| ------------------------ | ------------- | ------------- | ------ | ---- |
| Question / motivation     | 4 / 5         | 5 / 5         | 5 / 5  | 4.7  |
| Methodology               | 3 / 5         | 4 / 5         | 4 / 5  | 3.7  |
| Results                   | 4 / 5         | 4 / 5         | 4 / 5  | 4.0  |
| Discussion / contribution | 4 / 5         | 3 / 5         | 4 / 5  | 3.7  |
| Limitations / honesty     | 5 / 5         | 4 / 5         | 5 / 5  | 4.7  |
| Citations / prior work    | 4 / 5         | 3 / 5         | 4 / 5  | 3.7  |
| Figures / tables          | 4 / 5         | 4 / 5         | 4 / 5  | 4.0  |
| Writing / clarity         | 4 / 5         | 4 / 5         | 5 / 5  | 4.3  |
| Reproducibility           | 3 / 5         | 4 / 5         | 4 / 5  | 3.7  |
| **Overall**               | **3.9**       | **3.9**       | **4.4** | **4.06** |

## Top revision priorities (cross-reviewer consensus)

1. **Methodology** (Methodologist & Reader): the sample size justification
   is missing. Add an a priori power analysis to §5.2.
   *Effort:* small. *Impact:* high.

2. **Contribution framing** (Domain Expert): the contribution paragraph
   lists three items, but only two are differentiated from Smith (2023).
   Reframe contribution #2 to emphasize the novel mechanism.
   *Effort:* medium. *Impact:* high.

3. **Citation gaps** (Domain Expert): the related-work section misses
   Doe (2022) and Lee (2024), both directly relevant. Add and integrate.
   *Effort:* medium. *Impact:* high.

4. **Figure 3 caption** (Reader): caption describes the figure but doesn't
   interpret it. Rewrite to highlight the plateau at 33 B parameters.
   *Effort:* small. *Impact:* medium.

5. **Reproducibility** (Methodologist): no random seed list. Add seeds and
   a `requirements.txt` reference.
   *Effort:* small. *Impact:* medium.

## Suggested revisions (full list)

(... per persona, 3–5 items each ...)

## Decision (simulated)

- If overall ≥ 4.0 and zero high-severity items: **Accept with minor revisions**.
- If overall 3.0–4.0 or any high-severity item: **Major revision required**.
- If overall < 3.0: **Reject**.
```

---

## 4. Apply revisions

The orchestrator applies the **top revision priorities** in order:

1. Read each suggested revision.
2. Decide: auto-fixable (e.g., add citations, fix caption, add seed list)
   vs. requires human input (e.g., add new analysis).
3. Apply auto-fixable ones.
4. Surface human-input ones in `Known gaps`.
5. After applying revisions, re-run the **validation pipeline**
   (`workflows/validation-pipeline.md`) to confirm no regressions.

---

## 5. Final check: read top-to-bottom

Before declaring the paper done, perform one **final cover-to-cover read**:

- Title → abstract → conclusion: are they consistent? Does the abstract
  promise things the body delivers? Does the conclusion claim more than
  the body shows?
- Numbers in the abstract match numbers in the results.
- Section transitions are smooth.
- No leftover `<<...>>` or `[CITATION NEEDED]` placeholders (or, if any
  remain, they are listed in `Known gaps`).
- Word count meets the target.

---

## 6. Output

- `review/review-report.md` — the consolidated review.
- Updated `paper-cited.md` (now ready as `paper-final.md`).
- Updated `validation/validation-report.md` if revisions were applied.

---

## 7. Reviewer prompts

The detailed prompts each reviewer uses are in
`prompts/review-prompts.md`. They are deliberately distinct from each other
to avoid the three reviewers converging on the same suggestions.

---

## 8. When to involve the human

The skill is designed to be **autonomous up to a point**. It involves the
human user (or asks them to involve a domain advisor) when:

- A **high-severity** issue requires substantive judgment (e.g., choosing
  between two methodologies for a re-analysis).
- The paper depends on **unverifiable claims** that the model cannot
  resolve offline.
- The paper crosses a **discipline-specific** ethical boundary (medical
  claims, legal claims, claims about identifiable individuals).

In those cases the orchestrator delivers the paper with `Known gaps`
fully populated and a clear request: "Please address [list] before
submission."
