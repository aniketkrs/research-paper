# IEEE-Style Paper Template

Use this template for IEEE conferences (ICRA, INFOCOM, ICASSP, etc.) and
IEEE Transactions journals. Two-column layout is venue-rendered; we author
in single-column Markdown and the publisher's LaTeX class re-flows it.

> Replace every `<<...>>`. Keep section numbering and the IEEE numeric
> citation style.

---

```markdown
# <<Title — concise, no acronyms unless very common>>

**Authors:** <<First Last, *Member, IEEE*¹; First Last, *Senior Member, IEEE*²>>
**Affiliations:** ¹<<Institution, City, Country, email>>;
                  ²<<Institution, City, Country, email>>

## Abstract

<<≤ 250 words, single paragraph. Implicit structure: problem → method →
results → significance. No citations in the abstract.>>

**Plain-English summary.** <<5–10 sentences for non-specialists.>>

**Index Terms** — <<term 1, term 2, term 3, term 4>> (alphabetical, lower
case except proper nouns).

---

## I. Introduction

<<Establish the problem and its importance. Cite seminal and recent work.>>

<<State the gap or limitation in existing work.>>

<<Summarize the proposed approach.>>

**Contributions of this paper:**
1. <<Specific contribution>>.
2. <<Specific contribution>>.
3. <<Specific contribution>>.

The rest of this paper is organized as follows. Section II reviews related
work. Section III formulates the problem. Section IV presents the proposed
method. Section V reports the experimental setup, and Section VI presents
the results. Section VII discusses implications. Section VIII concludes.

---

## II. Related Work

<<Group prior work by theme. Cite IEEE numeric: [1], [2], [3]. End with
explicit positioning.>>

### A. <<Theme 1>>

<<Synthesis of prior work in this area [1]–[5].>>

### B. <<Theme 2>>

<<...>>

### C. Position of this work

Unlike [1] and [4], which <<difference>>, our method <<contribution>>.
Compared to [7], we <<contribution>>.

---

## III. System Model and Problem Formulation

### A. System model

<<Describe the system, agents, signals, channels. Include a system diagram
as Fig. 1.>>

**Fig. 1.** <<System architecture / signal flow.>>

### B. Notation

| Symbol | Meaning                  | Units |
| ------ | ------------------------ | ----- |
| `x`    | <<signal vector>>        | <<unit>> |
| `H`    | <<channel matrix>>       | —     |
| ...    | ...                      | ...   |

### C. Problem statement

We aim to find `θ*` that minimizes `J(θ)`:

```
θ* = argmin_θ  J(θ) = ‖y − Hf_θ(x)‖² + λ‖θ‖²    (1)
```

subject to <<constraints>>.

---

## IV. Proposed Method

### A. Overview

<<High-level description.>>

> *Plain-English version:* <<analogy / simple explanation>>.

**Fig. 2.** <<Method block diagram.>>

### B. <<Component 1>>

<<Detailed description with equations.>>

### C. <<Component 2>>

<<...>>

### D. Algorithm

```
Algorithm 1: <<Algorithm name>>
Input:  <<inputs>>
Output: <<outputs>>
1: <<step>>
2: <<step>>
   ...
```

### E. Complexity analysis

The time complexity of Algorithm 1 is `O(n log n)`. Memory complexity is
`O(n)`. <<Derivation in Appendix A.>>

---

## V. Experimental Setup

### A. Dataset / testbed

<<Describe data, setup, hardware.>>

### B. Baselines

<<List the comparison methods, citing each: [3], [7], [12].>>

### C. Metrics

<<Define each metric formally.>>

### D. Implementation

<<Framework, hardware, training procedure, parameters.>>

---

## VI. Results

### A. Main results

**Table I.** <<Main comparison. Best in bold.>>

| Method     | Metric A | Metric B | Metric C |
| ---------- | -------- | -------- | -------- |
| Baseline [3] | <<x>>  | <<x>>  | <<x>>  |
| Baseline [7] | <<x>>  | <<x>>  | <<x>>  |
| Proposed   | **<<x>>** | **<<x>>** | <<x>>  |

<<Interpret in 1–2 paragraphs.>>

**Fig. 3.** <<Bar chart of main results.>>

### B. Ablation study

**Table II.** <<Ablation results.>>

### C. Robustness analysis

<<Vary noise / load / parameters; report.>>

**Fig. 4.** <<Sensitivity curve.>>

### D. Computational cost

<<Latency / throughput / energy if relevant.>>

---

## VII. Discussion

<<Interpret findings. Compare to prior work [1], [4], [7]. Discuss
implications.>>

---

## VIII. Conclusion and Future Work

<<Summarize contributions. List 2–3 future directions.>>

---

## Acknowledgments

<<Funding sources, individuals.>>

---

## Reproducibility

- **Code:** <<URL>>
- **Data:** <<URL>>
- **Hardware:** <<spec>>
- **Seeds:** <<list>>

---

## References

[1] J. Smith, "Title," *Journal*, vol. X, no. Y, pp. P1–P2, Mon. Year, doi: ...

[2] A. Doe and K. Lee, "Title," in *Proc. Conf. Name*, City, Year, pp. P1–P2, doi: ...

[3] <<...>>

---

## Appendix A. Derivation of Equation (X)

<<Full proof / derivation deferred from main text.>>

## Appendix B. Additional results

<<Tables / figures not in the main paper.>>
```

---

## Skill-specific instructions for this template

1. Use **IEEE numeric citation style** (`[1]`, `[2]`) with references in
   order of first appearance.
2. Section numbering is **Roman numerals** at level 1, **uppercase letters**
   at level 2 ("I.", "I.A.", "I.A.1)").
3. Figures: caption *below* figure, "Fig. 1." (with period). Tables: caption
   *above* table, "Table I." in Roman numerals.
4. The publication-checklist requires "Index Terms" (not "Keywords") for
   IEEE.
5. Maintain a strict separation between Results (§VI) and Discussion (§VII).
6. Algorithms use a separate `Algorithm` block with numbered steps.
7. Equations are numbered `(1)`, `(2)`, in parentheses, right-aligned.
8. The acknowledgment section must be present (or marked "None.") before
   References.
