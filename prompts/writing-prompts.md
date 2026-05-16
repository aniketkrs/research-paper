# Prompt: Writing

Used in `workflows/research-orchestration.md §7 Drafting`. Reused by the
writer agent for every section.

> **One section at a time.** Persist each section to disk before starting
> the next. Cross-section consistency is enforced via the outline, not by
> holding everything in working memory.

---

## Generic per-section prompt

```
You are a senior academic writer producing the <SECTION NAME> for the paper
described in paper-spec.md, using the template in templates/<format>.md.

Inputs (load only these — do not re-read other sections unless needed):
- paper-spec.md
- outline.md (for the cross-section context)
- templates/<format>.md (find the slot for this section)
- references/writing-style-guide.md (read once at the start of drafting)
- bibliography.yaml (cite only keys present here)
- methodology.md (if writing the Method section)
- analysis/findings.md (if writing the Results section)
- figures-plan.md (for figure / table references)
- previous adjacent sections (if cross-section dependencies exist)

Output: sections/<NN>-<name>.md

Rules:
1. Follow the template's slot structure exactly.
2. Use the writing-style-guide.md voice (academic, evidence-first,
   no AI cliches).
3. Insert in-text citations as [cite_key] placeholders. Use ONLY keys that
   are in bibliography.yaml. Never invent.
4. Reference figures and tables by ID (Figure 3, Table 1) - the IDs are
   defined in figures-plan.md.
5. Every non-trivial claim has a citation, dataset, equation, or
   derivation. If evidence is missing, write [CITATION NEEDED — topic:
   "<short description>"].
6. Match hedging to evidence (references/writing-style-guide.md §12).
7. Maintain dual register: keep technical depth in the body, but write
   accessibly. Plain-English summaries are produced separately
   (prompts/simplification-prompts.md).
8. Sentence-length variety: short for emphasis, long for context. Avoid
   stacks of identical-length sentences.
9. Topic sentence first. One idea per sentence.
10. Persist the draft to disk before reporting completion.
```

---

## Section-specific guidance

### Title

```
- <= 15 words
- Specific, not clickbait
- Mention the contribution AND the domain
- No acronyms unless universally understood
- Examples:
  GOOD: "Contrastive Pretraining Improves Zero-Shot Diagnosis on
        Chest X-rays"
  BAD:  "AI for Medical Imaging: A Revolutionary New Approach"
```

### Abstract

```
150-300 words, single paragraph (or sub-paragraphed for Harvard style).
Implicit structure:
  1-2 sentences of context
  1 sentence of gap
  1-2 sentences of approach
  2-3 sentences of key results (with one quantitative number)
  1 sentence of implication

NO citations in the abstract (rare exceptions: Nature). NO new acronyms.
Numbers must match those in the body.

After drafting, run:
  - Word count check
  - Reading-level check (target Flesch-Kincaid <= 14)
  - Cover-paragraph test: does the abstract by itself tell a coherent
    story?
```

### Plain-English summary

```
See prompts/simplification-prompts.md.
Place at end of abstract, start of intro, or as a subsection of conclusion
(per template).
```

### Keywords

```
4-8 keywords. Use:
- Domain terms a librarian would index by
- Method terms (e.g., "transformer", "logistic regression")
- Application terms
- Avoid generic terms ("AI", "data") that index nothing.
```

### Introduction

```
Structure:
  1. Broad context (1 paragraph)
  2. Specific gap (1 paragraph)
  3. Approach summary (1 paragraph)
  4. Contribution list (bulleted)
  5. Paper outline (1 short paragraph)

Citation density: 6-15 per page (references/citation-styles.md §11).

The contribution list is the most-read part. Each bullet is concrete:
  - "We propose <method>, a <type> for <problem>."
  - "We empirically demonstrate <quantitative result> on <benchmark>."
  - "We release <artifact> at <URL>."
```

### Related Work / Literature Review

```
Group by THEME, not by paper. 3-5 themes typical for a paper section;
3-7 for a standalone review.

For each theme:
  - 1 sentence stating the theme
  - 4-8 papers synthesized with comparison/contrast
  - Identify points of agreement, disagreement, gaps

End with a "Position of this work" paragraph that states explicitly how
this paper differs from / builds on the cited work.

Citation density: 15-40 per section.
```

### Methodology

```
Read methodology.md (already produced by §4) and turn it into prose.
Every required field from references/methodology-guide.md must appear.

Tense: past for what was done.
Voice: first-person plural ("we") OK in CS / sciences; passive in
       formal / venue-specific contexts.

Include figures: system architecture (Figure 1 typical), study design
diagram if multi-arm.

End with the Threats to Validity / Limitations preview, full Limitations
goes at the end of paper.
```

### Results / Findings

```
Read analysis/findings.md and expand each finding into 1-3 paragraphs.

Pattern per finding:
  1. State what was tested.
  2. Report the test (statistic, df, p, effect, CI, n) inline.
  3. Reference the figure / table.
  4. Interpret quantitatively.
  5. Compare to prior work briefly (deeper comparison goes in Discussion).

Include all planned figures and tables, with in-text references that
PRECEDE the figure / table in the rendered output.

Be honest about nulls: "we did not detect an effect" not "X had no
effect".
```

### Discussion

```
Structure:
  1. Restate findings in plain terms (1-2 paragraphs)
  2. Relate to prior work (compare and contrast, cite specific papers)
  3. Theoretical implications (if applicable)
  4. Practical implications
  5. Threats to validity / limitations preview (full Limitations is its
     own section)

Citation density: 5-10 per page.

Do NOT introduce new results in the Discussion. Re-interpret only.
```

### Limitations

```
3-5 specific limitations. For each:
  - State the limitation concretely.
  - Explain its likely impact on conclusions.
  - State what would address it (sets up Future Work).

Honest > defensive. Reviewers respect candor.

Avoid generic limitations ("more work is needed", "larger samples would
help"). Be specific.
```

### Future Work

```
Concrete RQs, not vague calls. For each:
  - RQ-N: "<specific question>"
  - Why it matters
  - Suggested method
  - Expected challenges

3-5 items typical.
```

### Conclusion

```
3-5 sentences. Restate:
  - the contribution
  - the headline result (with the quantitative number)
  - the broader implication

NO new content. NO new citations. NO calls to action longer than one
sentence.
```

### References

```
Generated by the citation pipeline (workflows/citation-pipeline.md).
The writer agent does not write this section by hand.
```

### Appendices

```
Defer technical material here:
  - Proofs / derivations
  - Full hyperparameter tables
  - Per-task / per-condition breakdowns
  - Verbatim prompts (LLM papers)
  - Failure cases with analysis
  - Search strings (literature reviews)
  - PRISMA checklist
  - Survey instruments
  - Codebooks (qualitative)
```

---

## After drafting any section

```
Run a self-check on the section:
[ ] All [cite_key] placeholders use keys present in bibliography.yaml
[ ] No [CITATION NEEDED] flags left WITHOUT a description
[ ] Every figure / table referenced exists in figures-plan.md
[ ] Every figure / table referenced is mentioned BEFORE it appears
[ ] No AI-cliché phrases (references/writing-style-guide.md §14)
[ ] Section length proportional to template expectation
[ ] Acronyms defined on first use
[ ] Numbers / units consistent with rest of paper
[ ] Topic sentences open every paragraph

Then SAVE to sections/<NN>-<name>.md before moving on.
```

---

## Voice tips for specific sub-tasks

- **Setting up a contribution claim:** name the gap first ("Despite this
  progress, no work has X."), then the contribution ("We address this by
  Y.").
- **Comparing to prior work:** prior-work-then-ours order ("Whereas Smith
  (2023) does X with cost C, our method does Y with cost C/10.").
- **Reporting a null:** state the test, the n, and the post-hoc power.
  ("We did not detect a significant difference (t(78) = 0.4, p = .69,
  d = 0.09, 95% CI [-0.36, 0.54]; n = 80; post-hoc power = 0.21).
  This null is consistent with no effect or with insufficient power to
  detect a small effect.")
- **Caveating a strong claim:** "<claim>, under <assumption>". Surface
  the assumption explicitly, then defend it.
- **Citing a paper for the first time:** integrate the contribution
  ("Smith (2023) introduced <thing> by <method>."), not just append
  the cite.
- **Citing a paper for the second+ time:** "(Smith, 2023)" is fine; no
  need to keep introducing.
