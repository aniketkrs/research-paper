# ACM-Style Paper Template

Use this template for SIGCHI, SIGCOMM, SIGGRAPH, SIGSOFT, SIGSAC, SIGMOD,
SOSP, OSDI, and ACM Transactions journals.

> Replace every `<<...>>`. Citation style: ACM Reference Format
> (numeric `[1]`).

---

```markdown
# <<Title — often a benefit / question framing for HCI>>

**Authors:** <<First Last¹, First Last²>>
**Affiliations:** ¹<<University, City, Country, email>>; ²<<...>>

## Abstract

<<150–200 words. Implicit structure for HCI: problem → approach → study →
findings → contribution.>>

**Plain-English summary.** <<5–10 sentences for non-specialists.>>

**CCS Concepts:** • <<Top-level taxon>> → <<sub-taxon>>; • <<...>>

**Keywords:** <<keyword 1, keyword 2, keyword 3, keyword 4>>

**ACM Reference Format:**
First Last, First Last. YYYY. <<Title>>. In *Proceedings of the YYYY ACM Conf.
on <<Conference>> (CONF '<<YY>>)*. ACM, New York, NY, USA, <<n>> pages.
https://doi.org/10.1145/<<doi>>

---

## 1 Introduction

<<Open with a vivid scenario or problem (HCI papers often start with a
narrative).>>

<<State the gap and the contribution.>>

**Contributions:**
- A <<artifact / framework / study>> that <<contribution>>.
- An evaluation showing <<finding>>.
- Design implications for <<area>>.

---

## 2 Related Work

### 2.1 <<Theme 1>>

<<Cite numerically: prior work [1, 4, 7] has explored …>>

### 2.2 <<Theme 2>>

<<...>>

---

## 3 Background and Formative Study (HCI papers)

<<Pre-study, interviews, formative observations that motivate the design.
Skip for systems papers.>>

---

## 4 System / Design

### 4.1 Design goals

<<DG1, DG2, DG3 — derived from the formative study or prior work.>>

### 4.2 System architecture

**Figure 1.** <<Architecture diagram.>>

### 4.3 Key design decisions

<<Each decision: what was chosen, what alternatives were considered, why.>>

### 4.4 Implementation

<<Framework, languages, deployment.>>

---

## 5 Evaluation

### 5.1 Research questions

- **RQ1.** <<...>>
- **RQ2.** <<...>>

### 5.2 Study design

<<Within / between subjects, conditions, counterbalancing.>>

### 5.3 Participants

<<n, demographics, recruitment, compensation, IRB approval.>>

### 5.4 Procedure

<<Step-by-step, replicable.>>

### 5.5 Measures

<<Quant: task time, errors, NASA-TLX, SUS. Qual: think-aloud, semi-structured
interview.>>

### 5.6 Analysis

<<Stats for quant; thematic analysis with κ for qual.>>

---

## 6 Findings / Results

### 6.1 Quantitative findings

**Table 1.** <<Quantitative results, mean ± SD, with statistical tests.>>

**Figure 2.** <<Bar chart with error bars (95% CIs).>>

### 6.2 Qualitative findings

#### 6.2.1 Theme 1: <<...>>

<<Quote-evidence-warrant pattern. Use *italics* for participant quotes,
attributed by ID (P3, P11).>>

> *"<<participant quote>>"* — P3.

#### 6.2.2 Theme 2: <<...>>

<<...>>

---

## 7 Discussion

### 7.1 Interpreting the findings

<<...>>

### 7.2 Design implications

- **DI1.** <<...>>
- **DI2.** <<...>>

### 7.3 Connections to prior work

<<...>>

---

## 8 Limitations

<<Sample size, ecological validity, novelty effects, generalizability.>>

---

## 9 Future Work

<<Concrete RQs.>>

---

## 10 Conclusion

<<3–5 sentences summarizing the contribution.>>

---

## Acknowledgments

<<Funding, participants, reviewers.>>

---

## References

[1] First Last and First Last. YYYY. <<Title>>. In *Proceedings of CONF '<<YY>>*.
    ACM, New York, NY, USA, <<pp>>. https://doi.org/...

[2] First Last. YYYY. <<Title>>. ACM Trans. on <<Foo>> 12, 3 (Mar. YYYY),
    <<pp>>. https://doi.org/...

[3] <<...>>

---

## Appendices

**A. Interview protocol.**

**B. Survey instrument.**

**C. Codebook.**

**D. Additional figures.**
```

---

## Skill-specific instructions for this template

1. Use ACM Reference Format (numeric `[1]`).
2. Use **arabic numerals** for sections (1, 1.1, 1.1.1).
3. CCS Concepts are mandatory — pick from
   [ACM CCS taxonomy](https://dl.acm.org/ccs).
4. For HCI papers, the **formative study** section (§3) is conventional.
5. For systems papers, replace §3 with **Background**.
6. Quote attribution uses participant IDs (P1, P2, …), italicized quotes.
7. Codebook for thematic analysis goes in the appendix.
8. Inter-rater reliability (κ) is reported when multiple coders are used.
9. ACM mandates an **acknowledgments** section before references.
