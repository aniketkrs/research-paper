# Visual Paper — Output Template

The headline deliverable: `paper-visual.md`. Designed to be engaging
without sacrificing rigor.

> **Layout principle:** visuals every 2–3 paragraphs. Plain-English
> alongside technical content. Never a wall of text.

---

```markdown
# <<Paper title>>

> **Source:** <<live-fetch | cache | bundled-corpus | model-knowledge>>
> **Rendered:** <<ISO timestamp>> by `read-research-paper` v<<version>>

---

## At a glance

```mermaid
<<mind map per prompts/generate-mindmap.md>>
```

### Headline numbers

| Metric | Value |
| --- | --- |
| <<metric 1>> | <<value>> |
| <<metric 2>> | <<value>> |
| <<metric 3>> | <<value>> |

### Elevator pitch

<<3-line plain-English summary of the contribution>>

> **Authors:** <<First A. Last>>, <<First B. Last>>, <<et al.>>
> **Year:** <<YYYY>>
> **Venue:** <<Venue>>
> **DOI:** [<<10.xxx/yyy>>](https://doi.org/<<10.xxx/yyy>>)

---

## TL;DR

<<5-8 sentences. Lead with the headline number. Tell the story:
problem → method → finding → significance.>>

---

## Plain-English summary

<<5-10 sentences for a smart layperson. Use analogies. Avoid jargon.
This is the version someone could read aloud at dinner.>>

---

## Section 1 — Introduction

> **In plain English:** <<3-6 sentence translation per
> prompts/plain-english.md>>
>
> **Why this matters:** <<one-line stake-setter>>

<<Original section content (verbatim or near-verbatim, with light
formatting cleanup).>>

---

## Section 2 — Related Work

> **In plain English:** <<...>>
>
> **Why this matters:** <<...>>

<<Original section content.>>

```mermaid
<<related-work timeline (if applicable, per
  workflows/visualization.md §6)>>
```

**Figure 1.** Timeline of cited prior work, by year. The dominant
pattern is <<observation>>.

---

## Section 3 — Method

> **In plain English:** <<...>>
>
> **Why this matters:** <<...>>

```mermaid
<<method flowchart per workflows/visualization.md §5>>
```

**Figure 2.** Pipeline of the proposed method. <<2-sentence
interpretation>>.

<<Original method content.>>

---

## Section 4 — Results / Findings

> **In plain English:** <<...>>
>
> **Why this matters:** <<...>>

### Key findings

![Key findings](figures/key-findings.png)
<<Or, when matplotlib unavailable:>>

| Metric | Baseline | Proposed | Δ |
| --- | --- | --- | --- |
| <<metric>> | <<value>> | **<<value>>** | <<+/-X>> |
| ... | ... | ... | ... |

**Figure 3.** Headline performance comparison. <<2-sentence
interpretation>>.

### Comparison to baselines

| Method | <<metric A>> | <<metric B>> | <<metric C>> |
| ------ | ------------ | ------------ | ------------ |
| Baseline 1 | <<...>> | <<...>> | <<...>> |
| Baseline 2 | <<...>> | <<...>> | <<...>> |
| **Proposed** | **<<...>>** | **<<...>>** | <<...>> |

**Table 1.** <<Caption from the paper, or new interpretive caption.>>

<<Original results content.>>

---

## Section 5 — Discussion

> **In plain English:** <<...>>
>
> **Why this matters:** <<...>>

<<Original discussion content.>>

---

## Section 6 — Limitations

> **In plain English:** <<plain-language statement of what the paper
> does NOT show>>

<<Original limitations content.>>

---

## Section 7 — Conclusion

> **In plain English:** <<...>>

<<Original conclusion content.>>

---

## Concept map (`--visuals max` only)

```mermaid
<<concept map per workflows/visualization.md §7>>
```

**Figure 4.** Concepts introduced or extended by this paper.

---

## Author network (`--visuals max` only)

```mermaid
<<author network per workflows/visualization.md §8>>
```

**Figure 5.** Authors and affiliations.

---

## Why this paper matters (in one paragraph)

<<Plain-language reflection. Connects the paper's findings to
real-world stakes. Honest about scope. 4-6 sentences.>>

---

## Where to read it (yourself)

- **Original PDF:** <<URL>>
- **Code repository:** <<URL when available>>
- **Author homepage:** <<URL when available>>

---

## References

<<Reference list, formatted in the user's chosen --style. Linked to
DOIs / arXiv URLs. Generated from the paper's own bibliography +
verified.>>

---

## Verification trail

| Check | Result |
| --- | --- |
| DOI resolves | ✓ / ✗ / not-checked |
| Crossref match | ✓ / ✗ / not-checked |
| Retraction Watch | clean / retracted / not-checked |
| arXiv API | confirmed / not found / not-checked |
| Source tier | <<live-fetch | cache | bundled-corpus | model-knowledge>> |

---

## Known gaps

<<Any items that couldn't be fetched / parsed / verified are listed
here. See Known-gaps.md for the full list with severity and
recommended fixes.>>

---

## Next steps

- **Read related papers:** Run `/get-research-paper "<topic>"` for
  curated reading on this area.
- **Write a paper:** Run `/research "<topic>" --bibliography <path>/bibliography.yaml`
  to build a paper that cites this one.
- **Re-render with different settings:** `--depth deep`, `--audience general`,
  `--visuals max`, etc.
```

---

## Generation rules

1. **Persist provenance.** The Source field at the top is auto-
   filled by the orchestrator (live-fetch / cache / bundled-corpus /
   model-knowledge). Never lie about provenance.
2. **Plain-English layer first.** In every section, the
   plain-English block precedes the technical content. The reader
   gets oriented before they hit jargon.
3. **Visuals interleave.** Don't dump all visuals at the end. Each
   section that warrants a visual gets one inline.
4. **Captions interpret.** Every visual has a 2-sentence interpretive
   caption.
5. **Reference cite_keys.** When the paper cites work in its
   References section, those cite_keys are linked from in-text
   mentions.
6. **No invented sections.** If the paper has no Limitations section,
   omit Section 6 from the rendering rather than fabricating one.

---

## Layout for short papers (< 5 pages)

For short papers (poster abstracts, extended abstracts, letters),
collapse:

- Combine Method + Results into one section.
- Skip the Concept map and Author network even at `--visuals max`.
- Reduce the visual budget to 2 (mind map + key findings only).

---

## Layout for very long papers (> 30 pages)

For long papers (theses, surveys with 50+ refs, monographs):

- Add a per-section TL;DR at each H2.
- Add a section index right after the visual summary.
- Render appendices in a separate `paper-visual-appendix.md`.

---

## Anti-patterns

- ❌ The whole paper as one wall of text with a mind map at the top
  and nothing else.
- ❌ Plain-English layer that strips the technical content rather
  than augments it.
- ❌ Captions that just describe ("Figure 3 shows the results")
  rather than interpret.
- ❌ Inventing a Limitations section the paper doesn't have.
- ❌ Pretending a paper from `model-knowledge` source was live-fetched.
- ❌ Cherry-picking the most flattering numbers and omitting the rest.

The rule: **honest, engaging, complete**. All three.
