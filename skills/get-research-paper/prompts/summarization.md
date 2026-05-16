# Summarization Prompt

How to write a 2–4 sentence summary per paper that's actually useful
for someone deciding whether to read it.

---

## The structure

Every summary follows: **problem → method → finding → significance**.

| Sentence | Job                                                  |
| -------- | ---------------------------------------------------- |
| 1        | What problem the paper addresses (or the question it asks). |
| 2        | What method / approach the paper uses.                |
| 3        | What it found — with the headline number when available. |
| 4 (deep) | Why this matters for the topic at hand.               |

Length budget:

- `--depth quick`: 2 sentences (problem + finding).
- `--depth standard`: 3 sentences (problem + method + finding).
- `--depth deep`: 4 sentences (problem + method + finding + significance).

---

## Use this prompt verbatim

```
You are summarizing a research paper for someone building a reading
list on the topic: <topic>.

Paper:
  Title: <title>
  Authors: <authors>
  Year: <year>
  Venue: <venue>
  DOI: <doi>
  Abstract: <abstract>

Audience: <academic | technical | general>

Write a <2 | 3 | 4>-sentence summary using the structure:
  - Problem the paper addresses
  - Method / approach used
  - Headline finding (with numbers when available)
  - Significance for <topic>  [only for 4-sentence summaries]

Constraints:
- Stay strictly inside the abstract. Do not infer findings not stated.
- Use precise verbs ("demonstrates", "evaluates", "proposes",
  "compares") not vague ones ("explores", "discusses", "looks at").
- Audience adjustments:
  - academic: keep field jargon; assume reader knows the area.
  - technical: define field jargon on first use; use one analogy if
    a concept is unusually dense.
  - general: plain English (Flesch-Kincaid <= 12); replace jargon
    with everyday-language equivalents.
- No hype. No "revolutionary", "groundbreaking", "cutting-edge".
- Match the certainty of the abstract. If the paper hedges, hedge.
- If the abstract has a quantitative result, INCLUDE it. Reading lists
  without numbers are vague.

Write the summary. Do not include any meta-commentary.
```

---

## Examples

### Example A — `quick`, academic audience

> Smith et al. (2023). *ACM Computing Surveys*.
>
> "Surveys 137 papers on retrieval-augmented generation in software
> engineering, finding that 87% of LLM-SE evaluations conflate
> retrieval quality with model ability, inflating reported gains by
> an estimated 8–34 percentage points."

### Example B — `standard`, technical audience

> Doe et al. (2022). *Proc. ICSE 2022*.
>
> "Tests OpenAI Codex on 4,212 real pull requests across three open-
> source projects. Uses a blinded human-rating protocol where the
> original reviewers score Codex's review comments without knowing
> they came from an AI. Finds that Codex's comments are rated 18 pp
> more useful than vanilla LLM baselines, with a 31% reduction in
> token cost."

### Example C — `deep`, general audience

> Lee (2024). *Nature*.
>
> "Studies whether large AI models can replace some kinds of medical
> diagnosis. The researchers gave the AI 12,400 chest X-rays from real
> patients and compared its diagnoses to those of board-certified
> radiologists. The AI matched the radiologists' accuracy on 87% of
> the cases — but missed 6% of urgent findings the radiologists
> caught. **For our topic on AI-assisted medical imaging,** this
> paper is the strongest evidence that AI can augment but not yet
> replace expert review in safety-critical cases."

The fourth sentence (audience-specific significance) is the value-add
for `deep` summaries.

---

## When the abstract is unavailable

If a candidate paper has no abstract (e.g., older papers, behind a
paywall):

1. Use the title + venue to construct a 1-sentence "we know it's
   about X but full details unavailable" summary.
2. Mark `summary_source: "title only"` in the bibliography.
3. Add to `Known-gaps.md` with `[INCOMPLETE METADATA]`.

Do **not** fabricate a summary from the title. Better a 1-sentence
honest summary than an invented paragraph.

---

## When the paper is a review / survey

Treat it specially. Three sentences should answer:

1. What scope does the review cover (years, n studies, methodology)?
2. What's the dominant finding / consensus identified?
3. What gaps does it identify?

Reviews are high-leverage — they often deserve a 4-sentence summary
even at `--depth standard`.

---

## When the paper has multiple findings

Pick the **most relevant to the user's topic**, not the most quoted.

Example: a paper on "transformer architectures" might also report
some fairness analysis. If the user's topic is "transformer
architectures for NLP", lead with the architecture finding.

---

## Audience-specific adjustments

### Academic

- Keep all field-specific terms.
- Cite venue / journal when notable.
- Use technical verbs ("demonstrates", "establishes", "proves").

### Technical

- Define jargon on first use.
- Use one analogy per dense concept.
- Slightly longer per sentence (15–25 words OK).

### General

- Replace jargon with plain English.
- Aim for Flesch–Kincaid grade ≤ 12.
- Use simple sentence structure (one clause).
- Don't sacrifice the headline number.

---

## Anti-patterns

- ❌ Generic sentences ("This paper discusses..."). Use precise verbs.
- ❌ Inflating findings ("This paper revolutionizes..."). Match the
  paper's own language.
- ❌ Stuffing in cite_keys ("(smith_2023)"). The cite_key lives in the
  reading-list entry header, not in the summary text.
- ❌ Three-sentence summaries that are all problem statement.
- ❌ Skipping the headline number when one exists in the abstract.

---

## Final output

The summary becomes the `notes:` field of the bibliography entry AND
the body of the reading-list entry. Same text, two locations,
single source of truth.
