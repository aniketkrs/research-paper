# Voice and Tone

This file is loaded **once** during the drafting phase. It enforces the
"sounds human, reads academic, no AI tells" voice that distinguishes a
paper from a blog post.

> **The test:** a senior academic should respect the rigor; an
> undergraduate in the field should be able to follow the argument; an
> intelligent layperson should be able to read the abstract, plain-
> English summary, and conclusion without consulting another source.

---

## 1. Voice

| Section            | Voice / tense default                              |
| ------------------ | -------------------------------------------------- |
| Abstract            | Past for methods / results, present for context. Active voice OK. |
| Introduction        | Present for facts, past for prior work.            |
| Related Work        | Past tense; "Smith et al. (2023) showed …".         |
| Methodology         | Past tense ("we collected", "the model was trained"). |
| Results             | Past tense ("the system achieved").                  |
| Discussion          | Mix; present for interpretation, past for findings.  |
| Conclusion          | Present tense for take-aways.                        |

**First-person plural ("we")** is acceptable in CS / ML / engineering and
increasingly in social sciences. **Avoid passive voice** when the actor
matters; use it only when the actor is irrelevant or unknown.

Single-author papers may use "I" or "we" — match the venue.

---

## 2. Tone

- **Confident, not arrogant.** State findings as findings; flag
  uncertainty where it exists.
- **Specific, not hedged into nothingness.** One hedge is enough.
- **Calm, not breathless.** Avoid "remarkable", "striking", "dramatic"
  unless quantified.
- **Generous, not dismissive.** Engage prior work charitably even
  when disagreeing.
- **Honest about limits.** Small effect → say so. Preliminary → say so.
  Biased sample → say so.

---

## 3. Forbidden phrasings (the AI-cliché filter)

These are dead giveaways of AI-generated prose. **Strip them all** in
the review pass.

| Don't write                                       | Why                                       |
| ------------------------------------------------- | ----------------------------------------- |
| "It is well known that…" without a citation       | Cite something or remove                  |
| "In today's fast-paced / digital age / rapidly evolving landscape" | Empty filler              |
| "Recent studies have shown…" (without citing)     | Cite specific studies                     |
| "Revolutionary / groundbreaking / cutting-edge / paradigm shift" | Marketing language       |
| "Significant" without "statistically"              | Ambiguous (quantity vs. p-value)          |
| "Prove" / "proven"                                | Outside math, results don't prove things   |
| "Very", "really", "extremely"                     | Empty intensifiers                        |
| "Things", "stuff", "etc."                         | Vague; specify or omit                    |
| "I think / I believe / in my opinion"             | Without evidence, this is not a contribution |
| "Obvious / obviously / clearly"                   | Often signals an unsupported claim         |
| "Delve / delving"                                 | Overused AI tell                          |
| "Tapestry of…" / "Navigate the complexities of…"  | Marketing tells                           |
| Stacked transitions: "Furthermore… Moreover… Additionally…" | Pick one, then vary           |
| "Multifaceted approach"                           | Empty                                     |
| Three-item lists with empty adjectives             | "efficient, effective, elegant" — vapid   |

---

## 4. Sentence-level craft

- **Vary sentence length.** Short sentences land hardest. Mix with
  longer ones that build context. Avoid runs of three identical-
  length sentences.
- **One idea per sentence.** Start a new sentence rather than adding a
  third clause.
- **Topic sentence first.** Each paragraph begins with a sentence
  that states what the paragraph is about.
- **Old-information first, new-information last.** This is the
  *given–new* rule. It is what makes prose flow.
- **Use signposts.** "First, …", "By contrast, …", "Taken together,
  …", "However, …", "Crucially, …".
- **Define every technical term on first use.**
- **Spell out acronyms on first use** in each major section.

---

## 5. Paragraph structure

Standard academic paragraph (4–8 sentences):

1. **Topic sentence** — the claim.
2. **Elaboration** — what the claim means.
3. **Evidence** — citations or data.
4. **Counter-consideration** — what could be objected.
5. **Resolution** — why the position holds anyway.
6. **Linking sentence** — how this leads into the next paragraph.

Not every paragraph needs all six, but every paragraph should have a
clear job.

---

## 6. Argument craft (Toulmin)

For non-trivial arguments:

- **Claim** — what is being asserted.
- **Evidence** — data, citations, derivations.
- **Warrant** — why this evidence supports this claim.
- **Backing** — citations to first principles or methodology.
- **Qualifier** — boundary conditions ("under assumption A").
- **Rebuttal** — addressed counter-arguments.

---

## 7. Hedging calibration

Match certainty to evidence:

| Strength of evidence                     | Phrasing                                  |
| ---------------------------------------- | ----------------------------------------- |
| Mathematically proven                     | "X is true under assumptions A, B, C."     |
| Strong empirical replication              | "X is robustly observed."                  |
| Single experiment, large effect           | "X is found in our setting."                |
| Single experiment, small effect           | "We observe a small effect of X."           |
| Trend in the data                         | "Our data are consistent with X."           |
| Suggestive only                           | "X may explain Y; further evidence needed." |
| Speculative                               | "We speculate that X; this remains untested." |

Mismatched certainty (overclaiming or underclaiming) is the most common
reason a paper is rejected.

---

## 8. Citing and integrating sources

- **Cite the work, not the author's opinion.**
- **Integrate, don't drop.** Bad: "(Smith, 2023) (Doe, 2022)". Good:
  "Two recent studies (Smith, 2023; Doe, 2022) report …".
- **Compare and contrast.** "Whereas Smith (2023) found X, Doe (2022)
  reported the opposite, possibly because …".
- **Build a chain of citations.** "Early work established A (Smith,
  2018); later refinements addressed B (Doe, 2020)".
- **Don't quote what you can paraphrase.** Direct quotes are reserved
  for unique phrasings or critique.

---

## 9. Numbers, units, equations

- Spell out integers ≤ 9 ("three groups"); digits for ≥ 10
  ("12 participants"). Don't start a sentence with a number — rewrite.
- Non-breaking space between number and unit: "12 ms", "5 GB",
  "n = 240".
- SI units. Spell out unit on first use; abbreviate after.
- Equations numbered when referenced; inline when short.
- Define every variable on the same page it is introduced.

---

## 10. Inclusive and ethical language

- **Person-first** for disability ("a person with epilepsy") unless
  community preference says otherwise.
- **Gender-inclusive** ("they/them" by default).
- **Race / ethnicity / nationality** — match terminology the group
  uses for itself.
- **Anthropomorphism** in AI / ML — prefer "the model outputs" over
  "the model wants".
- Disclose conflicts of interest, AI-assisted writing, and use of
  generative tools per venue policy.

---

## 11. Self-edit checklist

Before declaring a section done:

1. Coherence — does each paragraph follow from the last?
2. Argument — is every non-trivial claim supported?
3. Citations — verifiable? styles consistent?
4. Clarity — would a colleague unfamiliar with the project follow it?
5. Concision — can any sentence be cut without losing meaning?
6. Tone — is hedging matched to evidence? AI clichés removed?
7. Plain-English version exists for the abstract / conclusion?
8. Figures / tables — referenced, captioned, interpreted?
9. Limitations — honest about what the paper does *not* show?
10. Reproducibility — could someone redo this work?

The full reviewer pass is in `review_pipeline/three-personas.md`.
