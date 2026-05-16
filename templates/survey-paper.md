# Survey Paper Template

Use for "A Survey of …" or "A Comprehensive Review of …" papers — the
kind that organize a research field with a taxonomy and a comparison table.
Differs from a literature review by emphasizing **field-organization** over
**evidence synthesis**.

---

```markdown
# A <<Comprehensive|Survey of>> <topic>

**Authors:** <<…>>
**Affiliations:** <<…>>

## Abstract

<<200–300 words. Implicit structure: 1–2 sentences of context; 1–2 sentences
of why a survey is needed now; 1–2 sentences of contributions; 2–3 sentences
of the taxonomy / coverage; 1 sentence on open challenges.>>

**Plain-English summary.** <<5–10 sentences>>.

**Keywords:** <<…>>

---

## 1. Introduction

### 1.1 Motivation

<<Why does this field need a survey now? What's changed since the last one?>>

### 1.2 Existing surveys

<<Acknowledge prior surveys; explain why a new one is warranted (recency,
scope, taxonomy difference).>>

### 1.3 Scope

<<What this survey covers and explicitly excludes. Time range. Venues.>>

### 1.4 Methodology of the survey

<<How papers were collected — search strategy, databases, snowballing.
Light reference to PRISMA-style methodology when applicable.>>

### 1.5 Contributions

- A taxonomy of <<topic>> across <<n>> dimensions.
- Coverage of <<n>> papers from <<YYYY>> to <<YYYY>>.
- A unifying comparison table (Table <<>>).
- A discussion of open challenges and research directions.

### 1.6 Paper organization

<<Roadmap of sections.>>

---

## 2. Background and Notation

<<Concise foundational background needed to read the rest of the paper.
Define common notation in a single table.>>

| Symbol | Meaning   | Notes |
| ------ | --------- | ----- |
| <<…>>  | <<…>>     | <<…>> |

---

## 3. A Taxonomy of <<topic>>

<<This is the **central contribution**. State the dimensions of the
taxonomy explicitly.>>

**Figure 1.** <<Taxonomy tree / mind-map of the field.>>

### 3.1 Dimension A: <<criterion>>

<<Categories within this dimension.>>

### 3.2 Dimension B: <<criterion>>

<<…>>

### 3.3 Dimension C: <<criterion>>

<<…>>

---

## 4. Category 1: <<Name from taxonomy>>

### 4.1 Overview

<<What unites this category? What problem does it solve?>>

### 4.2 Representative methods

<<3–8 representative papers; for each: 1–2 paragraphs of summary,
strengths, weaknesses, key insight.>>

#### 4.2.1 Method <<X>> (Smith et al., 2023)

<<Description, strengths, weaknesses.>>

#### 4.2.2 Method <<Y>> (Doe et al., 2022)

<<…>>

### 4.3 Discussion of the category

<<Patterns, trade-offs, when to use this category.>>

---

## 5. Category 2: <<…>>

<<…>>

---

## 6. Category 3: <<…>>

<<…>>

---

## 7. Comparative Analysis

**Table 1.** <<The headline summary table — rows = methods, columns =
dimensions of the taxonomy + key properties.>>

| Method (Year)         | Cat. | Cat. | Property | Property | Property |
| --------------------- | ---- | ---- | -------- | -------- | -------- |
| <<Method 1>> (2023)    | A    | i    | <<…>>    | <<…>>    | <<…>>    |
| <<Method 2>> (2022)    | A    | ii   | <<…>>    | <<…>>    | <<…>>    |
| <<Method 3>> (2024)    | B    | i    | <<…>>    | <<…>>    | <<…>>    |
| …                     | …    | …    | …        | …        | …        |

**Figure 2.** <<Heatmap or scatter plot showing the field on two key
dimensions — e.g., performance vs. cost.>>

---

## 8. Datasets and Benchmarks

<<Catalogue of datasets / benchmarks used in the field.>>

**Table 2.** <<Datasets used by methods in this survey.>>

| Dataset | Domain | Size | Splits | License | Citation |
| ------- | ------ | ---- | ------ | ------- | -------- |
| <<…>>   | <<…>>  | <<…>> | <<…>>  | <<…>>   | <<…>>    |

---

## 9. Applications

<<Where the methods in this survey have been applied. Industries, use
cases, deployments.>>

---

## 10. Open Challenges and Research Directions

<<The "what's next" section. Be specific.>>

- **Challenge 1.** <<…>>
- **Challenge 2.** <<…>>
- **Challenge 3.** <<…>>

For each challenge, suggest:
- *Why it's open*
- *Why it's hard*
- *Possible approaches*

---

## 11. Conclusion

<<3–5 sentences. State of the field, the survey's organizing contribution,
and the future trajectory.>>

---

## References

<<100–500 entries typical. Citation style: IEEE / Harvard depending on venue.>>

---

## Appendices

**A. Search strategy.**

**B. Full classification of all surveyed papers.**

**C. Code / artifact links per method.**
```

---

## Skill-specific instructions

1. The **taxonomy** (§3) is the contribution — invest the most effort here.
2. The **comparison table** (Table 1) is the most-cited artifact of a
   survey. Make it deeply informative, with consistent column definitions.
3. Coverage: surveys typically cite **100–500** papers. Smaller is OK if
   the field is young; declare the cutoff.
4. **Honest acknowledgment** of prior surveys (§1.2) is mandatory — readers
   will check.
5. Provide a **bibliometric overview** (publications by year, top venues)
   in §1 or as Figure 0.
6. The "Open Challenges" section (§10) should not be vague — give the
   reader research directions they could actually start tomorrow.
