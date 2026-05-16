# Writing Style Guide

This file is the canonical guide for academic prose style in every paper this
skill produces. It enforces the **dual register**: rigorous and citation-heavy
in the body, plain-English-accessible in summaries and conclusions.

> **The test:** a senior academic should respect this paper's rigor; an
> undergraduate in the field should be able to follow its argument; an
> intelligent layperson should be able to read the abstract, plain-English
> summary, and conclusion without consulting another source.

---

## 1. Voice and tense

| Section         | Voice / tense default                           |
| --------------- | ----------------------------------------------- |
| Abstract         | Past tense for methods / results, present for context. Active voice OK. |
| Introduction     | Present tense for facts ("LLMs are…"), past for prior work ("Smith showed…"). |
| Related work     | Past tense; use "Smith et al. (2023) showed…" |
| Methodology      | Past tense ("we collected…", "the model was trained…"). |
| Results          | Past tense ("the system achieved…"). |
| Discussion       | Mix; present for interpretation, past for what was found. |
| Conclusion       | Present tense for take-aways. |

**First person plural ("we") is acceptable** in CS, ML, engineering, and
increasingly in social sciences. **Avoid "the author"** unless explicitly
required by the venue. Single-author papers can use "I" or "we" (style
varies by field — match the venue).

**Avoid passive voice** when the actor matters ("we collected" beats "data
were collected"). Use passive only when the actor is irrelevant or unknown.

---

## 2. Tone

- **Confident, not arrogant.** State findings as findings; flag uncertainty
  where it exists.
- **Specific, not hedged into nothingness.** Avoid stacking hedges like
  "may potentially possibly suggest". One hedge is enough.
- **Calm, not breathless.** Avoid "remarkable", "striking", "dramatic"
  unless quantified.
- **Generous, not dismissive.** Engage with prior work charitably even when
  disagreeing.
- **Honest about limits.** If the result is small, say so; if it's
  preliminary, say so; if the sample is biased, say so.

---

## 3. Forbidden phrasings

| Don't write                              | Why                                        |
| ---------------------------------------- | ------------------------------------------ |
| "It is well known that…"                  | Cite something or remove.                  |
| "Recent studies have shown…" (without citing) | Always cite specific studies.        |
| "In the digital age / today's fast-paced world…" | Empty filler.                       |
| "Revolutionary / groundbreaking / cutting-edge" | Marketing language.                  |
| "Significant" without "statistically"     | Ambiguous (quantity vs. p-value).          |
| "Prove" / "proven"                        | Outside math, results don't prove things — they support hypotheses. |
| "Very", "really", "extremely"             | Empty intensifiers.                        |
| "Things", "stuff", "etc."                 | Vague; specify or omit.                    |
| "I think / I believe / in my opinion"     | Without evidence, this is not a contribution. |
| "Obvious / obviously / clearly"           | Often signals an unsupported claim.        |

---

## 4. Sentence-level craft

- **Vary sentence length.** Short, declarative sentences land hardest. Mix
  with longer ones that build context. Avoid runs of three identical-length
  sentences.
- **One idea per sentence.** If you find yourself writing a third clause,
  start a new sentence.
- **Topic sentence first.** Each paragraph begins with a sentence that
  states what the paragraph is about.
- **Old-information first, new-information last.** This is the
  *given–new* rule; it is what makes prose flow.
- **Use signposts.** "First, …", "By contrast, …", "Taken together, …",
  "However, …", "Crucially, …".
- **Define every technical term on first use.** Even if you think the reader
  knows it.
- **Spell out acronyms on first use** in each major section.

---

## 5. Paragraph structure

A standard academic paragraph has 4–8 sentences arranged as:

1. **Topic sentence** — the claim.
2. **Elaboration** — what the claim means.
3. **Evidence** — citations or data.
4. **Counter-consideration** — what could be objected.
5. **Resolution** — why your position holds anyway.
6. **Linking sentence** — how this leads into the next paragraph.

Not every paragraph needs all six, but every paragraph should have a clear
**job to do** that you could state in one sentence.

---

## 6. Building an argument

Across a section, the argument should follow a **claim–evidence–warrant**
chain:

- **Claim** — what you're asserting.
- **Evidence** — data, citations, derivations.
- **Warrant** — why this evidence supports this claim.
- **Backing** — citations to first principles or methodology.
- **Qualifier** — boundary conditions ("under assumption A").
- **Rebuttal** — addressed counter-arguments.

This is Toulmin's model and it works. The skill should enforce it for any
non-trivial argument in the discussion.

---

## 7. The "dual register"

Every paper this skill produces includes a **Plain-English summary** placed
either:
- At the end of the abstract, or
- As the first subsection of the introduction, or
- As a separate subsection in the conclusion.

The plain-English summary follows different rules:

- Sentences ≤ 20 words.
- Reading level: high-school graduate (Flesch–Kincaid grade ≤ 10).
- No jargon without immediate definition.
- Active voice.
- Use analogies for hard concepts.
- Tell a story: "Here's the problem. Here's what we did. Here's what we
  found. Here's why it matters."

> **Example:**
> *Technical sentence:* "We propose a contrastive masked autoencoder pretrained
> on heterogeneous medical imaging modalities to enable zero-shot diagnostic
> prediction."
>
> *Plain-English version:* "We trained a model to fill in deliberately hidden
> parts of medical images. After this training, the model can suggest
> diagnoses for new images it has never seen before — even from scan types
> it wasn't directly trained on."

---

## 8. Transitions between sections

| Where                            | Transition pattern                                        |
| -------------------------------- | --------------------------------------------------------- |
| End of intro → related work       | "We position this work in the existing literature next."  |
| End of related work → method      | "Building on these foundations, we now present our approach." |
| End of method → results           | "We now report the results of applying this approach to <data>." |
| End of results → discussion       | "We turn now to interpreting these findings."             |
| End of discussion → limitations    | "Several limitations qualify these conclusions."          |
| End of limitations → future work   | "These limitations motivate the following directions for further research." |
| End of future work → conclusion    | "We conclude by summarizing the main contributions."     |

These are templates — vary the wording — but every section boundary should
have an explicit hand-off.

---

## 9. Citing and integrating sources

- **Cite the work, not the author's opinion.** Bad: "Smith says LLMs are
  great." Good: "Smith (2023) reports a 12 % accuracy gain on benchmark X."
- **Integrate, don't drop.** Bad: "(Smith, 2023) (Doe, 2022)". Good:
  "Two recent studies (Smith, 2023; Doe, 2022) report …".
- **Compare and contrast.** "Whereas Smith (2023) found X, Doe (2022)
  reported the opposite, possibly because <reason>."
- **Build a chain of citations.** "Early work established A (Smith, 2018);
  later refinements addressed B (Doe, 2020) and C (Lee, 2022)."
- **Don't quote what you can paraphrase.** Direct quotes are reserved for
  unique phrasings or to set up critique.

---

## 10. Numbers, units, and equations

- Spell out integers ≤ 9 in prose ("three groups"), use digits for ≥ 10
  ("12 participants") *unless* a number starts a sentence ("Twelve
  participants…") — but rewrite to avoid this.
- Use **non-breaking spaces** between numbers and units: "12 ms",
  "5 GB", "n = 240".
- Use SI units. Spell out the unit on first use; abbreviate after
  ("milliseconds (ms)").
- Equations: **numbered** when referenced, **inline** when short, **display**
  when ≥ ~10 characters or important.
- **Define every variable** introduced in an equation, on the same page.

---

## 11. Figures and tables in prose

- Reference every figure / table **before** it appears: "As Figure 3 shows…"
  or "(Table 2)".
- Don't merely describe what the figure shows ("Figure 3 shows the
  results"); **interpret** ("Figure 3 shows that accuracy plateaus at 33 B
  parameters, suggesting…").
- Don't put information *only* in the figure — readers may skip it.
  Summarize the takeaway in prose.

---

## 12. Hedging and certainty

Match certainty to evidence. A rough scale:

| Strength of evidence                | Phrasing                          |
| ----------------------------------- | --------------------------------- |
| Mathematically proven                | "X is true under assumptions A, B, C." |
| Strong empirical replication         | "X is robustly observed."         |
| Single experiment, large effect      | "X is found in our setting."      |
| Single experiment, small effect      | "We observe a small effect of X." |
| Trend in the data                    | "Our data are consistent with X." |
| Suggestive only                      | "X may explain Y; further evidence is needed." |
| Speculative                          | "We speculate that X; this remains untested." |

Mismatched certainty (overclaiming) is the most common reason a paper gets
rejected. The validation pipeline checks for it.

---

## 13. Inclusive and ethical language

- Use **person-first** language for disability ("a person with epilepsy",
  not "an epileptic") unless community preference says otherwise.
- Use **gender-inclusive** language: "they/them" by default; "the
  participant" rather than "he"; "humanity" rather than "mankind".
- Be careful with **race, ethnicity, nationality** — capitalize per current
  conventions; describe groups using the terminology they use for themselves.
- For AI / ML: avoid metaphors that anthropomorphize models in ways that
  mislead ("the model wants", "the model decides"). Prefer "the model
  outputs", "the model assigns probability".
- Disclose **conflicts of interest**, **AI-assisted writing**, and any
  use of generative tools per venue policy.

---

## 14. Anti-AI-cliché filter

LLM-generated prose has tells. Edit them out:

- "It's important to note that…"
- "In conclusion, …" (at the start of *every* paragraph)
- "Delve / delving" (overused)
- "Furthermore, … Moreover, … Additionally, …" stacked
- "Navigate the complexities of…"
- "Tapestry of…"
- "In today's rapidly evolving landscape…"
- "Cutting-edge / state-of-the-art" without quantifying
- "Multifaceted approach"
- Three-item lists for everything ("efficient, effective, and elegant")

If a paragraph reads like marketing copy, rewrite it. The skill explicitly
prefers concrete nouns and specific verbs over generic adjectives.

---

## 15. Self-edit pass (always run before delivery)

Run through these in order:

1. **Coherence** — does each section follow from the last?
2. **Argument** — is every non-trivial claim supported?
3. **Citations** — is every cited fact verifiable? are styles consistent?
4. **Clarity** — would a colleague unfamiliar with the project follow it?
5. **Concision** — can any sentence be cut without losing meaning?
6. **Tone** — is hedging matched to evidence? any AI clichés left?
7. **Plain-English** — does the summary work for a non-specialist?
8. **Figures / tables** — referenced, captioned, interpreted?
9. **Limitations** — honest about what the paper does *not* show?
10. **Reproducibility** — can someone redo this work?

The full review pipeline is in `workflows/review-pipeline.md`.
