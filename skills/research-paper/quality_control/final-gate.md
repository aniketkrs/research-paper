# Final Gate

The single, authoritative pre-delivery checkpoint. The orchestrator
runs this **after** validation, **after** the three-persona review,
and **after** any revisions. If any of the gates here fail, the paper
goes back into revision; if they all pass (or fail in a way that's
explicitly waived in `Known-gaps.md`), the paper is delivered.

---

## 1. Gate 1: Hard quality gates

These are encoded in `manifest.json → quality_gates`. The paper must
satisfy ALL of:

- [ ] **Word count** ≥ `minimum_word_count` (default 1500).
- [ ] **References** ≥ `minimum_references` (default 8).
- [ ] **Figures or tables** ≥ `minimum_figures_or_tables` (default 1).
- [ ] **Academic-quality rubric mean** ≥ `academic_quality_min`
       (default 4.0).
- [ ] All `must_include_sections` present.
- [ ] All `must_include_blocks` present
      (plain_english_summary, reproducibility_statement, future_work).

If any FAIL → block delivery; revise; re-run.

---

## 2. Gate 2: Citation integrity

- [ ] Citation report shows 0 missing keys.
- [ ] Citation report shows 0 incomplete entries.
- [ ] Citation report shows 0 retracted citations.
- [ ] No mixed citation styles.
- [ ] Every reference list entry is cited at least once
       (orphans surfaced but not blocking).

If any FAIL → block; re-run citation pipeline; revise.

---

## 3. Gate 3: Reviewer consensus

- [ ] All three reviewer personas scored ≥ 3.0 overall.
- [ ] No persona flagged a HIGH-severity revision request that wasn't
       addressed in the revision pass.

If a high-severity request remains:
- Either revise to address it, OR
- Explicitly waive it in `Known-gaps.md` (the user's choice).

If any FAIL without waiver → block; revise; re-run.

---

## 4. Gate 4: Validator clean (or waived)

- [ ] All HIGH-severity validation issues resolved or waived.
- [ ] Medium and low issues surfaced in `Known-gaps.md`.

If any HIGH unresolved without waiver → block.

---

## 5. Gate 5: Publication checklist

Run `quality_control/publication-checklist.md` end-to-end. Every
unchecked item must be either:
- Fixed in the paper, OR
- Surfaced in `Known-gaps.md`.

The checklist itself never blocks — it adds to `Known-gaps.md`.

---

## 6. Gate 6: Output contract

The skill's universal output contract (per `SKILL.md §8`):

- [ ] Title (≤ 15 words, specific, no clickbait)
- [ ] Authors / affiliation block (real or placeholder)
- [ ] Abstract (150–300 words, structured)
- [ ] Keywords (4–8)
- [ ] Plain-English summary
- [ ] Numbered sections per template
- [ ] ≥ 1 figure or table
- [ ] In-text citations
- [ ] Full reference list with DOIs / URLs
- [ ] Limitations section
- [ ] Future Work section
- [ ] Reproducibility statement
- [ ] Appendices for supporting material

If any FAIL → block; revise; re-run.

---

## 7. Gate 7: File integrity

- [ ] `paper-final.md` exists, is non-empty, parses as valid Markdown.
- [ ] `bibliography.yaml` exists and validates against
       `schemas/citation-schema.json`.
- [ ] All referenced figure / table files exist on disk.
- [ ] `Known-gaps.md` exists (even if empty).
- [ ] `index.md` exists and lists every artifact.

If any FAIL → block; regenerate.

---

## 8. Gate 8: Integrity of the run

- [ ] No `<<...>>` template placeholders remain in `paper-final.md`.
- [ ] No `[CITATION NEEDED]` markers without entries in `Known-gaps.md`.
- [ ] No `[UNVERIFIED]` markers without entries in `Known-gaps.md`.
- [ ] No partial-section markers (`[PARTIAL]`).
- [ ] No `[STALE — re-run]` markers (everything refreshed).

If any FAIL → block.

---

## 9. The waiver mechanism

For HIGH-severity issues that the user explicitly accepts (e.g.,
"this is a draft, ship it as-is"), record a waiver in
`Known-gaps.md`:

```markdown
## Waivers

- **Waived:** `[REPRODUCIBILITY GAP]` (no code release planned).
  - *Reason:* "Internal draft; not for external publication."
  - *Date:* 2024-05-12
```

Waived items unblock the gate but stay surfaced in the index.

---

## 10. Delivery

Once every gate is satisfied (or explicitly waived):

1. The orchestrator writes `index.md` with the full artifact summary
   and the quality-gate report.
2. The user receives:
   - `paper-final.md` (the deliverable)
   - `Known-gaps.md` (caveats)
   - `index.md` (overview of artifacts)
3. The orchestrator marks the session `delivered` in
   `session-state.yaml`.

Anything that didn't pass and wasn't waived stays in `Known-gaps.md`
with severity `high` so the user knows the paper is not yet
submission-ready.

---

## 11. Why this gate exists

Without a final gate, the skill would deliver work that looks
publication-ready but isn't (a missing reproducibility statement, a
malformed reference, an underpowered analysis). Real journals reject
papers for these exact reasons.

The final gate is the bridge between "draft" and "deliverable", and
the difference between a demo and a production system.
