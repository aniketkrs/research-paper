# Prompt: Extract Findings

Pull the headline numerical results from the paper's abstract +
results section. These become the data for the key-findings
infographic and the TL;DR.

---

## Use this prompt verbatim

```
You are extracting headline numerical findings from a research paper.

Paper sections to scan:
  - Abstract:
    <<<
    <abstract text>
    >>>
  - Results / Findings section:
    <<<
    <results text>
    >>>
  - Discussion section (for context only):
    <<<
    <discussion text, optional>
    >>>

Extract the 3-5 most important numerical findings. For each, capture:

  - value: "<number with unit, e.g., '84.3%', '4.2x', '+18 pp', '0.83'>"
  - metric: "<what is being measured: 'accuracy', 'F1', 'usefulness rating', 'token cost', etc.>"
  - context: "<one sentence: under what conditions / on what dataset>"
  - direction: "increase" | "decrease" | "neutral"
  - confidence_interval: "<95% CI [...] when present, else null>"
  - p_value: "<p < .001 or similar, when present, else null>"
  - effect_size: "<Cohen's d / r / OR, when present, else null>"
  - source_section: "<abstract | results | discussion>"
  - importance_rank: 1-5 (1 = most important headline)

Selection criteria — what counts as "headline":

1. Numbers in the abstract are likely headline.
2. Numbers in the discussion's first paragraph are likely headline.
3. Numbers reported with effect sizes / CIs are likely headline.
4. Numbers compared to a baseline ("X improves over Y by Z") are
   likely headline.
5. Per-task / per-condition breakdown numbers are usually NOT
   headline (they're details).

Output as a JSON array, sorted by importance_rank ascending.

DO NOT include numbers not actually stated in the paper.
DO NOT extrapolate / compute derived numbers.
DO mark p-values as `< .001` exactly as written, not as `0.001`.
```

---

## Examples

### Example A — clear headline numbers

**Abstract excerpt:**
> "RA-Review achieves an 18-percentage-point gain in blinded reviewer-
> rated usefulness (95 % CI [14, 22]) over the strongest baseline,
> while reducing token cost per review by 31 % (95 % CI [27, 35])."

**Output:**
```json
[
  {
    "value": "+18 pp",
    "metric": "blinded reviewer-rated usefulness",
    "context": "vs. strongest LLM baseline, on 4,212 PRs",
    "direction": "increase",
    "confidence_interval": "95% CI [14, 22]",
    "p_value": null,
    "effect_size": null,
    "source_section": "abstract",
    "importance_rank": 1
  },
  {
    "value": "-31%",
    "metric": "token cost per review",
    "context": "vs. vanilla LLM baseline",
    "direction": "decrease",
    "confidence_interval": "95% CI [27, 35]",
    "p_value": null,
    "effect_size": null,
    "source_section": "abstract",
    "importance_rank": 2
  }
]
```

### Example B — implicit headline numbers

**Abstract:**
> "Our method matches state-of-the-art accuracy on three benchmarks
> while training in a fraction of the time."

**Output:**
```json
[
  {
    "value": null,
    "metric": "accuracy on three benchmarks",
    "context": "matches SOTA — qualitative claim only",
    "direction": "neutral",
    "confidence_interval": null,
    "source_section": "abstract",
    "importance_rank": 1,
    "note": "Abstract makes a qualitative claim without numbers; check Results section for quantification"
  }
]
```

When the abstract is qualitative, surface that fact rather than
inventing numbers.

---

## How findings feed downstream

The extracted findings are used by:

1. **The TL;DR** (`templates/tldr.md`) — headline numbers go in the
   first sentence of the TL;DR.
2. **The infographic** (`templates/infographic.md`) — the headline
   numbers become the central visual.
3. **The key-findings chart** (`workflows/visualization.md §6`) —
   each numerical finding becomes a bar in the chart.
4. **The plain-English summary** (`prompts/plain-english.md`) — the
   plain-English version restates them in everyday units ("about
   1 in 5 errors prevented").

---

## When findings are extra-numerical

Some papers report:

- **Confidence ranges** ("between 12% and 18%") — pick the midpoint
  with the range as `confidence_interval`.
- **Categorical findings** ("the model failed in 14 of 50 cases") —
  convert to a percentage where natural.
- **Sub-group findings** ("the effect was stronger in older
  participants") — mark `importance_rank: 4-5` and include only
  if the paper itself emphasizes them.
- **Negative / null findings** ("we did not detect a difference") —
  include with `direction: neutral` and `value: null` plus
  `note: "non-significant"`. These are important findings too.

---

## Anti-patterns

- ❌ Inventing precise numbers from vague claims.
- ❌ Reporting a number from a table that the paper itself
  doesn't emphasize.
- ❌ Missing the headline number from the abstract because it was
  also in the results section.
- ❌ Combining multiple numbers into a derived ratio not stated by
  the paper.
- ❌ Treating sub-group numbers as headline when the paper's main
  story is the overall effect.
