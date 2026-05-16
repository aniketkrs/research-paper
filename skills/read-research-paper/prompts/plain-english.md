# Prompt: Plain-English Translation

Generate the plain-English layer that runs alongside every section of
the technical paper. The goal: an intelligent layperson can follow
the paper without needing the technical content.

> **The rule:** plain-English **augments**, never **replaces**, the
> technical layer. Both coexist in the output.

---

## The structure (per section)

For each section in the paper:

1. **One-sentence section summary** — what is this section about?
2. **3–6 sentence walk-through** — what's actually being said?
3. **One analogy** (optional) — for unusually dense concepts.
4. **"Why this matters"** — one-liner connecting to real-world stakes.

---

## Reading-level targets

| `--audience` mode | Flesch–Kincaid grade target |
| ----------------- | --------------------------- |
| `academic`        | ≤ 16                        |
| `technical`       | ≤ 14                        |
| `general` / `mixed` | ≤ 10                       |

If the first draft exceeds the target, the prompt re-runs with
"shorter sentences, simpler words" instructions until it fits.

---

## Use this prompt verbatim

```
You are translating a research-paper section into plain English for
a smart layperson, while preserving every fact.

Section: <section name>
Technical content of the section:
<<<
<full section text or extracted summary>
>>>

Audience: <academic | technical | general | mixed>
Target reading level: Flesch-Kincaid grade <= <target>.

Write a plain-English walk-through with this structure:

1. Section summary (1 sentence): what is this section about?
2. Walk-through (3-6 sentences): what is actually being said?
3. Analogy (1 sentence, OPTIONAL): only if the concept is dense
   enough to benefit from one. Use everyday objects/situations.
4. Why this matters (1 sentence): real-world stakes.

Constraints:
- Stay STRICTLY inside what the section says. Don't add facts.
- Replace jargon with plain English. If a term is unavoidable
  ("regression"), define it on first use.
- Use precise verbs. "demonstrates", "compares", "measures" — not
  "explores", "looks at".
- Match the paper's certainty. If it hedges, you hedge.
- Active voice, simple sentence structure.
- No "in conclusion", "it is important to note", "in today's
  fast-paced world", or other AI-cliché phrases.
- One idea per sentence.

Output ONLY the plain-English walk-through. No meta-commentary.
```

---

## Examples

### Example A — Method section, audience: general

**Original (technical):**

> "We use a contrastive masked autoencoder pretrained on heterogeneous
> medical imaging modalities (chest X-ray, CT, MRI) to enable zero-shot
> diagnostic prediction. The encoder is initialized with weights from
> a vision transformer pretrained on ImageNet-21k and fine-tuned with
> a multi-modal contrastive objective."

**Plain-English version (general, FK grade ≤ 10):**

> **Section summary.** The researchers describe how they trained their
> AI model.
>
> **Walk-through.** They taught the model to fill in deliberately
> hidden parts of medical images — like guessing the missing piece of
> a puzzle. They used three kinds of medical images at once: chest
> X-rays, CT scans, and MRIs. Before this, they pre-trained the model
> on a much larger collection of everyday photos so it had a head
> start at recognizing visual patterns. The training also rewarded the
> model for matching images of the same patient across different scan
> types.
>
> **Analogy.** It's like teaching someone to recognize people by
> showing them many photos with the faces hidden — over time they
> learn to recognize someone from a hand or a sleeve.
>
> **Why this matters.** This pre-training step is what allows the model
> to make diagnoses on scan types it has never seen before.

### Example B — Results section, audience: mixed

**Original (technical):**

> "On the GSM8K benchmark, our 70 B model achieves 84.3 % accuracy
> (95 % CI [82.1, 86.5]), outperforming the strongest 33 B baseline
> by 5.2 percentage points (paired bootstrap p < .001 after Holm
> correction)."

**Plain-English version (mixed):**

> **Section summary.** The model's accuracy on a math benchmark.
>
> **Walk-through.** The 70-billion-parameter version of the model
> answered the GSM8K math problems correctly 84.3 % of the time. This
> beat the next-strongest model (33 billion parameters) by about 5
> percentage points. The improvement is statistically significant —
> meaning it's very unlikely to be a fluke of random testing.
>
> **Why this matters.** Larger models continue to improve at math
> reasoning at this scale, suggesting more capacity → more
> reasoning ability for now.

---

## Per-section tips

### Introduction

- Translate the gap statement plainly: "Until now, X has been hard
  because Y."
- Translate contributions as: "This paper does three things…"

### Related Work

- Don't translate every cited paper. Translate the *themes*.
- "Several earlier studies tried X (citation_a, citation_b), but they
  ran into the problem that Y."

### Method

- Most likely to need an analogy.
- Walk through the pipeline as a story: input → step → step → output.
- Avoid mathematical formulas in the plain-English layer; reference
  them: "see equation (3) in the paper" rather than restating.

### Results

- Always include the headline number(s).
- Translate effect sizes: "Cohen's d = 0.5 is a medium-sized effect
  — meaningful but not enormous."
- Translate p-values: "p < .001 means the result is very unlikely to
  be a coincidence."

### Discussion

- Match the paper's hedging carefully.
- Surface limitations honestly.

### Conclusion

- The plain-English version of the conclusion often becomes the
  TL;DR. Don't duplicate verbatim — adapt for the TL;DR position.

---

## Reading-level enforcement

After generating, check Flesch–Kincaid grade:

```python
import textstat
fk = textstat.flesch_kincaid_grade(text)
```

If the grade is over target by > 2:

1. Identify the longest sentences. Split them.
2. Identify polysyllabic jargon. Replace.
3. Re-run the check.

If still over: reduce the target by audience mode (e.g., from 10 to
12) and document in the section header. Honest is better than fake-
simple.

---

## Anti-patterns

- ❌ Stripping the technical content entirely. Plain-English layer
  AUGMENTS the technical layer.
- ❌ Inventing analogies for concepts the paper itself doesn't draw
  analogies for, in ways that distort the meaning.
- ❌ Adding facts not in the original section.
- ❌ Vague verbs ("explores", "discusses", "looks at").
- ❌ Empty intensifiers ("really", "very", "quite").
- ❌ Three-item lists with no real differentiation.
- ❌ Plain-English so dumbed down that the result misrepresents the
  paper's nuance.

---

## What to do when the section is itself unclear

If the original section is opaque (badly written, missing context),
don't pretend it's clear. Honest options:

1. Translate what you can; flag the unclear parts in `Known-gaps.md`.
2. Note in the plain-English layer: "The paper does not explicitly
   state X; this is our interpretation."
3. For genuinely opaque math/notation, point to the equation: "Eq. (3)
   formalizes this; the plain-English description above approximates
   it."

Never invent clarity that isn't in the source.
