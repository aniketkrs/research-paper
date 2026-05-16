# Literature Review Guide

This file is the canonical playbook for any kind of literature review the
skill produces — whether as a standalone paper, the §2 "Related Work" of an
empirical paper, or a chapter of a thesis.

> **A literature review is a study, not a list.** It must have a research
> question, a method, and a contribution beyond enumeration.

---

## 1. Choose the type of review

| Type                       | Goal                                          | Method anchor                |
| -------------------------- | --------------------------------------------- | ---------------------------- |
| **Narrative review**        | Provide an expert overview of a field         | Author judgment              |
| **Scoping review**          | Map the size and breadth of literature         | JBI / Arksey & O'Malley      |
| **Systematic review**       | Answer a specific question rigorously         | PRISMA 2020 + protocol        |
| **Meta-analysis**           | Quantitatively synthesize effect sizes        | PRISMA + statistical pooling |
| **Critical review**         | Evaluate / challenge dominant assumptions     | Theoretical lens              |
| **Realist review**          | Explain *what works for whom under what conditions* | RAMESES                |
| **Umbrella review**         | Synthesize prior systematic reviews           | PRIOR / AMSTAR-2             |
| **State-of-the-art (SOTA)** | Snapshot of recent advances (CS / ML common)   | Cut-off date + search        |
| **Theoretical review**      | Build / refine theory                         | Concept analysis             |
| **Survey paper**            | Field-organizing taxonomy with broad coverage  | Inductive taxonomy           |

If the user just says "literature review", default to a **scoping** or
**systematic** review depending on whether they want a *map* or an *answer*.

---

## 2. Define the research question

Use a structured framework for clarity:

| Framework | Components                                           | Best for                  |
| --------- | ---------------------------------------------------- | ------------------------- |
| **PICO**   | Population, Intervention, Comparator, Outcome         | Clinical / experimental   |
| **PEO**    | Population, Exposure, Outcome                        | Observational             |
| **SPIDER** | Sample, Phenomenon of Interest, Design, Evaluation, Research type | Qualitative |
| **CIMO**   | Context, Intervention, Mechanism, Outcome            | Management / realist      |

Write the question first, then design search strings to mirror its components.

---

## 3. Search strategy

### 3.1 Databases (pick at least 3)

- **CS / engineering / ML:** Scopus, Web of Science, IEEE Xplore, ACM DL,
  arXiv, DBLP, Google Scholar
- **Biomed:** PubMed, EMBASE, Cochrane, Scopus
- **Social sciences:** Scopus, Web of Science, PsycINFO, ERIC, JSTOR
- **Business / management:** Business Source Premier, ABI/INFORM, Scopus
- **Grey literature:** Google Scholar, OpenGrey, government / NGO reports

### 3.2 Build a Boolean search string

Mirror your PICO/SPIDER components, joined with AND. Within each component,
use synonyms joined with OR. Wildcards (`*`) for stems. Quotation marks for
multi-word phrases.

Example for "LLM-based code review":

```
("large language model*" OR "LLM*" OR "GPT*" OR "transformer*"
 OR "foundation model*")
AND
("code review*" OR "pull request*" OR "PR review*"
 OR "merge request*")
AND
(evaluat* OR "user study" OR experiment* OR benchmark*)
```

Document the exact string per database — different databases require slightly
different syntax.

### 3.3 Snowballing

After the database search, do **forward** (papers that cite included papers)
and **backward** (papers cited by included papers) snowballing. Two iterations
typical.

### 3.4 Reproducibility

The exact search strings, dates, databases, and number of hits per database
go in an **appendix table** so another researcher can reproduce the search.

---

## 4. Screening and selection (PRISMA)

### 4.1 PRISMA flow stages

```
Identification    → number of records from each source, duplicates removed
Screening         → titles + abstracts screened, n excluded
Eligibility       → full-text review, n excluded with reasons
Included          → final n
```

The skill always renders the PRISMA flow as a Mermaid diagram (see
`references/visualization-guide.md §10`).

### 4.2 Inclusion / exclusion criteria

Document explicitly **before** screening starts. Common criteria:

- Date range (e.g., 2018–2024)
- Language (e.g., English only, with limitation noted)
- Publication venue (peer-reviewed only? include preprints?)
- Study type (empirical only? exclude opinion / editorial?)
- Topic match (operational definition)
- Sample / setting

Keep criteria **mutually exclusive** and **collectively exhaustive** so every
paper is unambiguously in or out.

### 4.3 Inter-rater reliability

For systematic reviews, two reviewers screen independently. Compute
Cohen's κ on the title/abstract phase; target ≥ 0.7. Resolve disagreements
by discussion or a third reviewer.

---

## 5. Quality assessment

Every included paper gets a quality score. Pick a rubric:

| Tool             | For                                          |
| ---------------- | -------------------------------------------- |
| **CASP**         | Qualitative, RCT, cohort, case-control       |
| **JBI critical-appraisal checklists** | Cross-method               |
| **MMAT**         | Mixed methods                                |
| **AMSTAR-2**     | Systematic reviews                           |
| **GRADE**        | Strength of evidence per outcome             |
| **Custom rubric** | When standard tools don't fit (define + cite) |

Report quality scores in a table; consider sensitivity analyses excluding
low-quality studies.

---

## 6. Data extraction

For each included paper, extract a standardized record:

| Field                        | Notes                                            |
| ---------------------------- | ------------------------------------------------ |
| Citation key                  | e.g., `smith2023llm`                             |
| Authors, year, venue          | Full bibliographic data                          |
| Country / setting             |                                                  |
| Study type                    | empirical / theoretical / review / case study    |
| Population / sample           | n, demographics                                  |
| Intervention / phenomenon     | what was studied                                 |
| Method                        | quantitative / qualitative / mixed; specifics    |
| Key findings                  | bullet points                                    |
| Effect sizes (if quantitative) | with CIs                                        |
| Limitations stated by authors  |                                                  |
| Quality score                  | per chosen rubric                                |
| Theoretical framing            | if relevant                                      |
| Notes / quotes                 | freeform                                         |

The full extraction table goes in the appendix; a *summarized* table goes in
the main text.

---

## 7. Synthesis approaches

### 7.1 Narrative synthesis

Group studies by **theme**, then within each theme, weave a story that:
- Identifies points of agreement
- Identifies points of disagreement and possible reasons
- Highlights gaps
- Cites every claim

### 7.2 Thematic synthesis

Bottom-up coding of findings into themes. Used heavily in qualitative
synthesis. Output: a thematic map (mind-map figure) + a section per theme.

### 7.3 Meta-analysis

When studies report comparable effect sizes:

1. **Standardize effect sizes** (SMD, log OR, Fisher z).
2. **Pool** with a random-effects model (DerSimonian–Laird or REML).
3. **Heterogeneity** — report I², τ², Q, prediction interval.
4. **Forest plot** as the headline figure.
5. **Funnel plot + Egger's test** for publication bias.
6. **Sub-group / meta-regression** to explain heterogeneity.

### 7.4 Taxonomic / framework synthesis

Build a **taxonomy** of the field. The taxonomy is the contribution.
Render as a tree / mind-map; provide a comparative table mapping each paper
to the taxonomy nodes it fills.

### 7.5 Realist synthesis

Generate **CMO configurations** (Context-Mechanism-Outcome): "In context C,
mechanism M produces outcome O." Tabulate them and trace evidence to each.

---

## 8. Writing the review (structure)

```
1. Title
2. Abstract (structured: background / objectives / methods / results / conclusions)
3. Keywords
4. Introduction
   4.1 Why this review now
   4.2 Research question(s)
   4.3 Scope and contributions
5. Methods
   5.1 Type of review
   5.2 Search strategy
   5.3 Inclusion / exclusion criteria
   5.4 Screening procedure (with PRISMA diagram)
   5.5 Quality assessment
   5.6 Data extraction and synthesis
6. Overview of included studies
   - Summary table of n studies (year / venue / method / sample / topic)
   - Bibliometric overview (publication count over time, top venues, etc.)
7. Findings (one section per theme / category)
   For each theme: what the literature agrees on, what it disagrees on,
   gaps, and key papers.
8. Cross-cutting observations
9. Gaps and open problems  ← critical contribution
10. Future research agenda  ← organized as concrete RQs
11. Limitations of this review
12. Conclusion
13. References
14. Appendices
    - A. Search strings per database
    - B. PRISMA checklist
    - C. Full data-extraction table
    - D. Quality assessment scores
```

---

## 9. Common literature-review pitfalls

- **List-style review.** "X did A. Y did B. Z did C." This is not synthesis.
  Group by theme, not by paper.
- **Citation laundering.** Citing a source you haven't read because someone
  else cited it. Always read the original.
- **Recency bias.** Only citing the last 3 years. Field-defining older work
  must be included.
- **Author bias.** Only citing your own group / advisor. Diversify.
- **Confirmation bias.** Excluding contradicting evidence. Include it and
  discuss.
- **Geographic / language bias.** English-only is fine but must be declared
  as a limitation.
- **Vague inclusion criteria.** "Relevant papers" is not a criterion.
- **Missing PRISMA flow.** For systematic reviews, this is non-negotiable.

---

## 10. Citation density expectations

| Section                | Typical citations          |
| ---------------------- | -------------------------- |
| Standalone review       | 50–300                    |
| Survey paper             | 100–500                  |
| §"Related Work" of empirical paper | 20–60        |
| Thesis chapter (review)  | 100–200                  |
| Policy brief             | 10–40                    |

If a section is far below the typical floor, the validator flags it.

---

## 11. Bibliometric / scientometric appendix (recommended)

For systematic and survey papers, include:

- Publication count by year (line chart)
- Top venues (bar chart)
- Top first authors (bar chart)
- Co-authorship network (force-directed graph) — optional
- Keyword co-occurrence map (network or word cloud) — optional
- Country / institution distribution (choropleth) — optional

These give the reader an instant feel for the field's shape.

---

## 12. From review to research agenda

A good review ends with a **concrete research agenda**, not vague calls for
"more research". For each gap, write:

- **RQ-N**: "<Specific question>"
- *Why it matters:* <1–2 sentences>
- *Suggested method:* <method type>
- *Expected challenges:* <1–2 sentences>

This turns the review into a launchpad for follow-on work — the highest form
of contribution a review can make.
