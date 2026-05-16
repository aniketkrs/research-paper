# arXiv-Style Paper Template

Use this template for ML / AI / CS / physics / quantitative-bio preprints.
Most ML conferences (NeurIPS, ICML, ICLR, ACL, EMNLP, CVPR) accept this
structure with minor venue-specific tweaks.

> Replace every `<<...>>` with content. Keep section numbering. The skill
> uses this template literally — every section heading must appear, in this
> order, in the final paper.

---

```markdown
# <<Title — specific, ≤ 15 words, no marketing words>>

**Authors:** <<First Last¹, First Last²>>
**Affiliations:** ¹<<Institution>>, ²<<Institution>>
**Contact:** <<email>>
**Preprint version:** <<v1, YYYY-MM-DD>>

## Abstract

<<150–250 words. One paragraph. Implicit structure: 1–2 sentences of
context; 1 sentence of gap; 1–2 sentences of approach; 2–3 sentences of
key results with one quantitative number; 1 sentence on implication.>>

**Plain-English summary.** <<5–10 sentences. No jargon. Tell a story:
problem → approach → finding → why it matters.>>

**Keywords:** <<keyword 1, keyword 2, keyword 3, keyword 4, keyword 5>>

---

## 1. Introduction

<<Open with the broad context of the problem (1 paragraph).>>

<<State the specific gap or open question that motivates the paper
(1 paragraph).>>

<<Briefly describe the proposed approach (1 paragraph).>>

<<State the contributions explicitly:>>

**Contributions.**
- We propose <<method name>>, a <<approach type>> for <<problem>>.
- We <<theoretical contribution / proof / new framework>>.
- We empirically demonstrate that <<key quantitative result>> on
  <<benchmark(s)>>, outperforming <<baseline>> by <<margin>>.
- We release <<code, data, models>> at <<URL>>.

<<Outline the rest of the paper:>>
The remainder of the paper is organized as follows. Section 2 reviews
related work. Section 3 introduces notation and background. Section 4
presents the proposed method. Section 5 describes the experimental setup.
Section 6 reports results, and Section 7 discusses their implications.
Section 8 outlines limitations, and Section 9 concludes.

---

## 2. Related Work

<<Group related work by theme, not by paper. 3–5 themes typical.>>

**<<Theme 1>>.** <<Synthesize 4–8 papers, contrast with our approach.>>
(Smith et al., 2023; Doe et al., 2022; Lee, 2021)

**<<Theme 2>>.** <<...>>

**<<Theme 3>>.** <<...>>

**Position of this work.** <<1 short paragraph stating exactly how this
paper differs from and builds on the work above.>>

---

## 3. Preliminaries and Background

### 3.1 Notation

<<Define all symbols used in the rest of the paper.>>

| Symbol | Meaning            | Domain   |
| ------ | ------------------ | -------- |
| `x`    | input vector       | ℝᵈ       |
| `y`    | target label       | {0, 1}   |
| `θ`    | model parameters   | ℝᵖ       |
| ...    | ...                | ...      |

### 3.2 Problem formulation

<<Define the problem rigorously. State assumptions explicitly.>>

We consider <<problem class>>: given <<input>>, predict <<output>>, under
assumptions <<A1, A2, ...>>.

### 3.3 Background on <<key concept>>

<<Briefly review the technical foundation the reader needs to follow §4.
Cite primary sources for foundational results.>>

---

## 4. Method

### 4.1 Overview

<<1–2 paragraphs explaining the high-level idea before any math.>>

> *Plain-English version:* <<Explain the core idea using an analogy,
> 2–3 sentences, suitable for an undergraduate.>>

**Figure 1.** <<Architecture diagram showing input → method → output. Use
Mermaid `flowchart LR` or a rendered image.>>

### 4.2 <<Component 1>>

<<Detailed exposition. State equation(s) explicitly.>>

The objective is

```
L(θ) = E_{(x,y)~D} [ ℓ(f_θ(x), y) ] + λ · R(θ)         (1)
```

where `ℓ` is <<loss function>> and `R` is <<regularizer>>.

### 4.3 <<Component 2>>

<<...>>

### 4.4 Algorithm

```
Algorithm 1: <<Algorithm name>>
Input:  <<inputs>>
Output: <<outputs>>

1: Initialize θ₀ ~ <<dist>>
2: for t = 1, ..., T do
3:    sample minibatch B from D
4:    g_t ← ∇_θ L(θ_{t-1}; B)
5:    θ_t ← Optimizer(θ_{t-1}, g_t, lr_t)
6: end for
7: return θ_T
```

### 4.5 Theoretical analysis (optional)

<<Convergence, complexity, bounds. State theorem(s); proof in appendix.>>

**Theorem 1.** <<Statement of theorem.>> *Proof in Appendix A.*

---

## 5. Experimental Setup

### 5.1 Datasets

<<For each dataset: name, size, splits, license, source. Note any
preprocessing.>>

| Dataset | Train | Val   | Test  | Source / License            |
| ------- | ----- | ----- | ----- | --------------------------- |
| <<D1>>  | <<n>> | <<n>> | <<n>> | <<citation>>, <<license>>   |
| <<D2>>  | <<n>> | <<n>> | <<n>> | <<citation>>, <<license>>   |

### 5.2 Baselines

<<List the strongest available baselines. Include vanilla, SOTA, and at
least one ablation. Cite each.>>

### 5.3 Metrics

<<Name each metric, define it formally if non-standard, justify the choice.>>

### 5.4 Implementation details

<<Framework, hardware, training time, hyperparameter search, final
hyperparameters in a table.>>

### 5.5 Statistical methodology

<<Number of seeds, statistical tests for paired comparisons, multiple
comparison correction, error bars convention. Default: ≥ 5 seeds, paired
bootstrap or Wilcoxon signed-rank, Holm–Bonferroni.>>

---

## 6. Results

### 6.1 Main results

<<Headline table: rows = methods, columns = datasets / metrics, values =
mean ± SD over seeds, best in bold, statistically tied with best
underlined.>>

**Table 1.** <<Main benchmark results. Mean ± SD over <<k>> seeds.
**Bold:** best per column. <u>Underlined:</u> not significantly different
from best at p < .05 (paired bootstrap, Holm–Bonferroni corrected).>>

| Method       | <<D1 metric>>  | <<D2 metric>>  | <<D3 metric>>  | Mean   |
| ------------ | -------------- | -------------- | -------------- | ------ |
| Baseline A   | <<x ± y>>      | <<x ± y>>      | <<x ± y>>      | <<x>>  |
| Baseline B   | <<x ± y>>      | <<x ± y>>      | <<x ± y>>      | <<x>>  |
| Ours         | **<<x ± y>>**  | **<<x ± y>>**  | <<x ± y>>      | **<<x>>** |

<<Interpret the table in 1–2 paragraphs. Quantify the gain.>>

**Figure 2.** <<Main result visualization — usually a grouped bar chart
or line plot if there's a scaling axis.>>

### 6.2 Ablation studies

<<Remove each component of the method and measure. One row per
ablation in a table.>>

### 6.3 Sensitivity / scaling analysis

<<Vary key hyperparameters / data scale / model size; show trends.>>

### 6.4 Qualitative analysis

<<Show 2–4 representative inputs and outputs. Describe both successes and
failures honestly.>>

---

## 7. Discussion

<<Connect findings back to §1's contributions. 4–8 paragraphs:>>

- *What worked and why.* <<...>>
- *Where the method falls short.* <<...>>
- *Comparison to prior work.* <<...>>
- *Implications for the field.* <<...>>

---

## 8. Limitations

<<Be honest. List at least 3 limitations:>>

- *Sample / dataset.* <<...>>
- *Method.* <<...>>
- *Generalization.* <<...>>
- *Compute / cost.* <<...>>

---

## 9. Future Work

<<Concrete follow-on questions, not vague calls.>>

- **RQ1.** <<Specific question>> — <<why it matters, suggested method>>.
- **RQ2.** <<...>>

---

## 10. Conclusion

<<3–5 sentences. Restate the contribution, the headline result, and the
broader implication. No new content.>>

---

## Reproducibility statement

- **Code:** <<URL>> (commit `<<hash>>`)
- **Data:** <<URL or "available on request">>
- **Environment:** <<requirements.txt / Dockerfile / conda env URL>>
- **Hardware:** <<GPU / CPU model, RAM, total compute estimate>>
- **Seeds:** <<list>>
- **Hyperparameters:** see Appendix B

---

## Broader impacts (NeurIPS / ICML style — when required)

<<Foreseeable benefits and harms. Mitigations. Honest about uncertainty.>>

---

## References

<<Use the citation style chosen for the venue (default: author–year for
ML, IEEE numeric for systems / signal). Generated by
`scripts/format_bibliography.py` from the canonical YAML metadata.>>

1. <<Reference 1>>
2. <<Reference 2>>
...

---

## Appendix A. Proofs

<<Theorem proofs deferred from §4.5.>>

## Appendix B. Hyperparameters

<<Full hyperparameter tables for each experiment.>>

## Appendix C. Additional results

<<Per-task breakdowns, additional ablations, extra figures.>>

## Appendix D. Prompts and templates (LLM papers)

<<Verbatim prompts used in any LLM-based experiment.>>

## Appendix E. Failure cases

<<2–4 representative failure examples with analysis.>>
```

---

## Skill-specific instructions for this template

When the orchestrator (`workflows/research-orchestration.md`) selects this
template:

1. Confirm the venue with the user (NeurIPS / ICML / ICLR / ACL / generic
   arXiv) — different venues have minor section-naming preferences.
2. Default citation style: **author–year (Harvard / APA-compatible)**.
3. Always emit Section 4.1 figure (architecture) — propose Mermaid if no
   image rendering available.
4. Always emit Table 1 (main results) — even if values are placeholders /
   illustrative.
5. Emit Reproducibility, Broader Impacts (when applicable), and Appendix B
   (hyperparameters) — these are venue gates.
6. Sections 8–10 (Limitations, Future Work, Conclusion) are mandatory.
