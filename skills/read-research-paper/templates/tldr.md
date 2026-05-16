# TL;DR Template

The 5–8 sentence quick summary that appears right after the visual
summary block. The reader who only reads the TL;DR should still walk
away with the core contribution.

---

```markdown
## TL;DR

<<Sentence 1: The headline number / contribution. Lead with it.>>

<<Sentence 2: The problem being addressed.>>

<<Sentence 3: The method / approach.>>

<<Sentence 4-5: The key findings (with numbers).>>

<<Sentence 6-7: The implications. (Optional sentence 7-8 for
significance.)>>
```

---

## Examples

### Example A — empirical paper, 6 sentences

```markdown
## TL;DR

Retrieval — not just bigger LLMs — is what makes AI-generated code
review comments useful. The paper studies 4,212 real pull requests
across three open-source projects to test whether retrieval-augmented
review beats vanilla LLM review. The proposed pipeline retrieves
context from four sources: style guides, prior pull requests, commit
messages, and design docs. Comments rated by the original reviewers
were 18 percentage points more useful with retrieval, while using 31%
fewer tokens. Ablation showed two of the four retrieval sources —
style guides and prior PRs — drive most of the gain. The results
suggest that comparative LLM-code-review evaluations should always
report the retrieval pipeline, not just the model.
```

### Example B — survey paper, 5 sentences

```markdown
## TL;DR

Retrieval-augmented generation in software engineering is a
productive but methodologically uneven field. The paper systematically
reviews 137 studies published 2020–2024 across six task categories
(code generation, code review, bug repair, documentation, test
generation, configuration). Only 11% of studies perform retrieval
ablations and 32% release reproducibility artifacts. The dominant
gap: most evaluations conflate retrieval quality with model ability,
inflating reported gains by an estimated 8–34 percentage points. The
authors propose eight concrete research questions to address these
gaps.
```

### Example C — theoretical paper, 5 sentences

```markdown
## TL;DR

This paper proves that any neural network architecture in a class
defined by <conditions> can be transformed into an equivalent
representation under <transformation>, generalizing earlier results
that applied only to <subclass>. The proof proceeds by <approach>,
introducing <new lemma> as the core technical contribution. The main
implication is that practical implementations using <subclass> can
extend their applicability to <broader class> with <complexity
caveat>. The authors discuss two limitations: the proof requires
<assumption> and the constructive transformation has <runtime>.
This work matters because it bridges <gap> in the theoretical
foundations of <field>.
```

---

## Length budget

| Paper type    | TL;DR length    |
| ------------- | --------------- |
| Short paper / extended abstract | 3-4 sentences |
| Standard paper                   | 5-7 sentences |
| Long / comprehensive paper        | 7-9 sentences |
| Survey / review                    | 6-8 sentences |
| Thesis chapter                     | 7-10 sentences |

Beyond 10 sentences, it stops being a TL;DR.

---

## Audience adjustment

The TL;DR adapts to `--audience`:

| Audience  | Tone                                                |
| --------- | --------------------------------------------------- |
| academic  | Technical terms intact; targeted at peers           |
| technical | Define jargon on first use                          |
| general   | Plain English; one analogy if needed                 |
| mixed     | Plain-English first sentence + technical follow-up    |

The skill produces ONE TL;DR. To get versions for multiple audiences,
re-run with each `--audience`.

---

## Position in the output

The TL;DR appears RIGHT AFTER the visual summary, so the layout is:

```
1. Visual summary (mind map + numbers + pitch)
2. TL;DR (5-8 sentences)
3. Plain-English summary (5-10 sentences, slightly more detailed)
4. Section walk-through (the body)
```

This three-tier opening gives the reader 30 seconds (visual), 1 minute
(TL;DR), and 3 minutes (plain-English summary) of progressively richer
context before they hit the technical sections.

---

## Anti-patterns

- ❌ Repeating the abstract verbatim. The TL;DR is **for the user**,
  not a paraphrase of the paper's own self-summary.
- ❌ Saying "this paper proposes..." instead of stating what was
  proposed.
- ❌ Burying the headline number after sentence 4.
- ❌ Long sentences (> 30 words) that the reader has to re-read.
- ❌ Marketing words ("revolutionary", "cutting-edge").
- ❌ "More research is needed" in the closing sentence. End with the
  significance, not a generic call.

---

## When the paper itself is a TL;DR

For very short papers (1-2 page extended abstracts, conference
posters), the TL;DR is essentially the abstract. In that case:

1. Use the abstract as the TL;DR.
2. Skip the standalone TL;DR section and merge with Plain-English
   summary.
3. Make the visual summary do more of the heavy lifting.
