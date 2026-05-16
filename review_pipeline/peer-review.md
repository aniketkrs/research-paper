# Internal Peer Review Pipeline

## Purpose
Simulate an academic peer review process to identify weaknesses before the paper is finalized.

---

## Review Stages

### Stage 1: Structural Review (Editor's Desk Check)

```
VERIFY basic requirements:
□ Title is informative and specific
□ Abstract present and within word limit
□ All required sections present for paper type
□ Word count within acceptable range
□ Formatting matches chosen template
□ Reference list present and populated
□ Figures and tables present (if applicable)

REJECT at desk if:
- Missing abstract
- Missing methodology
- Fewer than 5 references
- No clear research question
- Paper type doesn't match content
```

### Stage 2: Content Review (Reviewer 1 — Subject Matter)

```
EVALUATE:

SIGNIFICANCE:
- Is the research question important to the field?
- Does this paper add something new?
- Would the target audience care about these findings?

NOVELTY:
- What is genuinely new here?
- How does it differ from existing work?
- Is the claimed contribution accurate?

COMPLETENESS:
- Are all claims supported?
- Is the literature review sufficient?
- Are results fully presented?
- Are limitations acknowledged?

ACCURACY:
- Are facts correct (spot-check key claims)?
- Are statistics properly calculated and reported?
- Are citations correctly attributed?
- Are interpretations justified by the data?

OUTPUT: Specific comments with page/section references.
Rate: Accept / Minor Revisions / Major Revisions / Reject
```

### Stage 3: Methodology Review (Reviewer 2 — Methods Expert)

```
EVALUATE:

APPROPRIATENESS:
- Does methodology match research questions?
- Is the design suitable for the claims made?
- Are statistical tests appropriate for data types?

RIGOR:
- Are assumptions checked?
- Is sample size adequate?
- Are controls in place?
- Is there potential for bias?
- Are threats to validity addressed?

REPRODUCIBILITY:
- Could this be replicated from the description?
- Are all parameters specified?
- Is the analysis pipeline clear?

REPORTING:
- Are effect sizes reported?
- Are confidence intervals provided?
- Are exact p-values given?
- Are non-significant results reported?

OUTPUT: Methodological critique with specific suggestions.
Rate: Methodologically Sound / Minor Issues / Major Issues / Fundamentally Flawed
```

### Stage 4: Writing Review (Reviewer 3 — Communication)

```
EVALUATE:

CLARITY:
- Can the argument be followed without re-reading?
- Are technical terms defined?
- Is the writing accessible to the stated audience?

FLOW:
- Do sections connect logically?
- Are transitions smooth?
- Does each paragraph advance the argument?

TONE:
- Is it appropriately academic?
- Is it free of AI-typical phrasing?
- Is confidence calibrated to evidence?

PRECISION:
- Are claims specific rather than vague?
- Are numbers and data cited accurately?
- Is language unambiguous?

ENGAGEMENT:
- Does the introduction hook the reader?
- Is the narrative compelling?
- Does the conclusion leave a lasting impression?

OUTPUT: Line-level and section-level feedback.
Rate: Publication Ready / Light Editing / Substantial Editing / Rewrite Needed
```

---

## Review Decision Matrix

```
               │ Reviewer 1    │ Reviewer 2    │ Reviewer 3    │
               │ (Content)     │ (Methods)     │ (Writing)     │
───────────────┼───────────────┼───────────────┼───────────────┤
Accept         │ Accept        │ Sound         │ Ready         │ → PUBLISH
Minor Revision │ Minor Rev     │ Minor Issues  │ Light Edit    │ → REVISE (quick)
Major Revision │ Major Rev     │ Major Issues  │ Substantial   │ → REVISE (deep)
Reject         │ Reject        │ Flawed        │ Rewrite       │ → START OVER

DECISION RULES:
- All three Accept → Publish immediately
- Any one Reject → Major restructuring needed
- Mix of Minor/Major → Address all Major concerns, then reassess
- Two Majors → Likely needs significant rework
```

---

## Revision Response Protocol

```
WHEN issues identified:

FOR EACH issue:
1. Classify: Critical / Important / Minor / Cosmetic
2. Determine fix:
   - Critical: Must fix before output (blocks publication)
   - Important: Should fix, improves quality significantly
   - Minor: Fix if time allows, doesn't affect conclusions
   - Cosmetic: Fix for polish (typos, formatting)
3. Implement fix
4. Verify fix doesn't introduce new issues
5. Document what was changed and why

REVISION PRIORITY:
1. Methodological flaws (invalidate findings)
2. Unsupported claims (damage credibility)
3. Missing citations (academic integrity)
4. Logical gaps (confuse readers)
5. Writing issues (reduce impact)
6. Formatting (professionalism)
```

---

## Common Review Feedback and Fixes

| Common Feedback | Fix Strategy |
|----------------|-------------|
| "Contribution unclear" | Rewrite intro paragraph 5-6; add explicit contribution statement |
| "Methodology insufficient" | Add 2-3 paragraphs of detail; specify parameters |
| "Results unsupported" | Add citations; add effect sizes; add confidence intervals |
| "Discussion disconnected" | Explicitly connect each finding to literature review |
| "Literature review too thin" | Add 5-10 more sources; increase synthesis |
| "Claims too strong" | Add hedging language; acknowledge limitations |
| "Needs more visualization" | Apply visualization decision engine; add 2-3 figures |
| "Writing too generic" | Apply anti-AI filter; add specific examples and data |
| "Missing limitations" | Add limitations subsection with 3-5 honest limitations |
| "Conclusion just summarizes" | Add implications, future directions, significance |

---

## Review Timing

```
FULL PAPER REVIEW: Applied after complete draft is generated
- Run all three review stages
- Implement Critical and Important fixes
- Re-run quality rubric
- Output final score

SECTION REVIEW: Applied during generation (lightweight)
- Quick coherence check after each section
- Citation coverage spot-check
- Tone consistency check
- Flag issues for full review later

FINAL PASS: Applied after all revisions
- Read for flow and coherence
- Verify all fixes implemented correctly
- Confirm no new issues introduced
- Generate publication readiness score
```
