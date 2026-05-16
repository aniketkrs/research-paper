# Publication Readiness Checklist

Run this checklist as the **last** step before delivering a paper. Anything
unchecked must either be fixed or surfaced explicitly in a `Known gaps`
block at the end of the paper.

---

## A. Structural completeness

- [ ] Title is ≤ 15 words, specific, and free of clickbait
- [ ] Authors and affiliations block present (placeholders OK if user didn't supply)
- [ ] Abstract: 150–300 words, structured (background / methods / results / conclusion)
- [ ] Keywords: 4–8, controlled vocabulary if venue requires
- [ ] Plain-English summary present
- [ ] Introduction with motivation, gap, and explicit contribution list
- [ ] Background / Related work / Literature review present and integrated
- [ ] Methodology section reproducible end-to-end
- [ ] Results separated from interpretation
- [ ] Discussion ties results to prior work and to the contributions
- [ ] Limitations section honest and specific
- [ ] Future work section actionable (concrete RQs, not vague calls)
- [ ] Conclusion summarizes contributions without introducing new content
- [ ] References section properly formatted
- [ ] Appendices for derivations / extended tables / prompts / raw outputs

## B. Argument and evidence

- [ ] Every non-trivial claim is supported by a citation, dataset, equation, or derivation
- [ ] No `[CITATION NEEDED]` flags remain (or all surfaced in Known gaps)
- [ ] No `[UNVERIFIED]` flags remain (or all surfaced in Known gaps)
- [ ] Counter-evidence and contradictions are addressed, not ignored
- [ ] Hedging is matched to evidence strength (no overclaiming, no false-modest underclaiming)
- [ ] Causal language is used only where the design supports it

## C. Methodology rigor

- [ ] Research question stated explicitly
- [ ] Study type / design declared (quant / qual / mixed / SLR / design-science)
- [ ] Sampling and recruitment described
- [ ] Sample size justified (a priori power analysis where applicable)
- [ ] Variables / constructs operationalized
- [ ] Statistical methods named and assumptions checked
- [ ] Multiple-comparison correction applied where needed
- [ ] Effect sizes reported with 95% CIs
- [ ] Threats to validity (or "Threats to validity") section present
- [ ] Ethics / IRB statement present where humans / sensitive data are involved

## D. Data and reproducibility

- [ ] Dataset described (size, source, license, splits)
- [ ] Code repository linked (commit / tag) or marked as forthcoming
- [ ] Environment file (requirements.txt / Dockerfile / conda env) referenced
- [ ] Hyperparameters listed exactly
- [ ] Hardware (CPU/GPU, RAM, runtime) reported
- [ ] Random seeds reported and number of seeds ≥ 3 (≥ 5 for ML)
- [ ] Data availability statement present
- [ ] Code availability statement present

## E. Citations and references

- [ ] Citation style consistent throughout (Harvard / APA / IEEE / MLA / Chicago / Nature)
- [ ] In-text and reference list aligned (no orphan citations either direction)
- [ ] DOIs included where they exist
- [ ] URLs canonicalized (no tracking parameters)
- [ ] Access dates included for webpages in styles that require them
- [ ] No predatory / retracted / paper-mill sources
- [ ] At least 8 references for short papers; 30+ for full empirical papers; 50+ for surveys
- [ ] Every reference appears in the text at least once
- [ ] Triangulation: load-bearing claims have ≥ 2 independent sources where feasible

## F. Figures and tables

- [ ] At least 1 figure or table for any paper > 1500 words (unless purely theoretical)
- [ ] Every figure / table referenced in the text **before** it appears
- [ ] Figure / table numbers run sequentially with no gaps
- [ ] Captions interpret, not just describe
- [ ] Axis labels include units
- [ ] Colorblind-safe palette
- [ ] Error bars are CIs (or labeled otherwise)
- [ ] Sample sizes annotated where relevant
- [ ] No 3-D bar / pie charts; no truncated y-axes without annotation
- [ ] Tables have clear column headers and units; numeric columns right-aligned
- [ ] All figures available as both raster (PNG) and vector (SVG/PDF) where possible

## G. Writing quality

- [ ] No "It is well known that…" without a citation
- [ ] No empty intensifiers (very, really, extremely)
- [ ] No marketing clichés (revolutionary, cutting-edge, paradigm shift)
- [ ] Sentence-length variety (not all 25-word sentences)
- [ ] Paragraphs have clear topic sentences
- [ ] Section transitions explicit
- [ ] Acronyms defined on first use in each major section
- [ ] Numbers ≤ 9 spelled out, ≥ 10 in digits, units use non-breaking spaces
- [ ] Inclusive language (gender-neutral, person-first as appropriate)
- [ ] No anthropomorphization of models / systems beyond what the venue accepts

## H. Venue-specific (only if a venue is targeted)

- [ ] Word / page count within venue limit
- [ ] Citation style matches venue requirement
- [ ] Section ordering matches venue requirement
- [ ] Figure / table caption placement matches venue requirement
- [ ] Required artifacts present (e.g., ACM CCS concepts, NeurIPS Broader
      Impacts, Nature Methods, IEEE Index Terms)
- [ ] Anonymized version available for double-blind submission (no author
      names, no obvious self-citation in first person)
- [ ] Supplementary materials prepared as a separate file
- [ ] Cover letter / contribution statement drafted

## I. Plain-English summary

- [ ] Present in the paper (abstract, intro, or conclusion)
- [ ] Reading level ≤ grade 10 (Flesch–Kincaid)
- [ ] No jargon without immediate definition
- [ ] Tells the story: problem → method → finding → why it matters
- [ ] Does not contradict the technical sections

## J. Final review

- [ ] Read end-to-end, top to bottom, in one sitting
- [ ] Read sections in reverse order to catch logical gaps
- [ ] Re-read the abstract last (best test of self-contained intelligibility)
- [ ] Co-author / advisor read (or simulated peer-review pass via the
      review pipeline)
- [ ] Spell-check + grammar pass
- [ ] Citation pass (every cited fact found in the cited source)
- [ ] Compile / render clean (no broken refs, no missing figures)

## K. Known gaps block

If anything above is unchecked, add a `Known gaps` block at the end of the
paper with structure:

```markdown
## Known gaps

The following items are flagged for the authors / reviewers:

- **[CITATION NEEDED]** — Section 3.1, claim about <topic> needs a primary
  source. Candidates: <list>.
- **[UNVERIFIED]** — Reference [12] could not be resolved offline; please
  confirm DOI before submission.
- **[REPRODUCIBILITY GAP]** — Hyperparameters for the ablation study in
  Table 4 not yet documented; pull from training logs.
- **[POWER]** — The paired comparison in §5.3 is underpowered (n = 24,
  observed d = 0.3, post-hoc power = 0.42). Either collect more data or
  re-frame as exploratory.
```

This block is the skill's contract: nothing is silently swallowed, and the
authors always know what still needs human attention before submission.
