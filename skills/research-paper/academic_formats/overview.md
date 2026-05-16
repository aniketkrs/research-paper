# Academic Formats Reference

Use this file when you need to confirm the structural conventions of a target
publication style. Each section below describes section order, typography
hints, length expectations, and citation style.

> **Hierarchy of decisions:** explicit user request → venue conventions → this
> file's defaults. If the user contradicts a default, follow the user.

---

## 1. arXiv preprint

**Audience:** ML / AI / physics / CS / quantitative biology preprint readers.
**Tone:** technical, dense, low ceremony, formula-rich.

**Section order:**
1. Title
2. Authors and affiliations
3. Abstract (150–250 words, single paragraph)
4. Keywords (4–8)
5. Introduction (motivation, contributions list, paper outline)
6. Related Work *(can be §2 or §6 depending on convention)*
7. Preliminaries / Background / Notation
8. Method / Approach (the technical contribution)
9. Experiments
10. Results
11. Discussion
12. Limitations
13. Conclusion
14. References
15. Appendices (proofs, hyperparameters, extra plots)
16. Reproducibility / Broader Impacts (NeurIPS-style)

**Citation style:** Numeric `[1]` or author-year `(Smith et al., 2023)`,
depending on subfield (ML papers usually use author-year via natbib).

**Length:** 8–12 pages main body, unlimited appendix.

**Mandatory contributions block:** end of intro, bulleted list:
- *We propose …*
- *We show that …*
- *We release …*

---

## 2. IEEE conference / journal

**Audience:** engineering, signal processing, communications, hardware,
robotics, applied CS.
**Tone:** formal, precise, equation-heavy, claim-centric.

**Section order:**
1. Title (concise, no acronyms unless very common)
2. Author block with affiliations and emails
3. Abstract (≤ 250 words, one paragraph, structured implicitly:
   problem → method → results → significance)
4. Index Terms / Keywords
5. Introduction (with explicit "Contributions" paragraph)
6. Related Work
7. System Model / Problem Formulation
8. Proposed Method / Algorithm
9. Theoretical Analysis (complexity, convergence, bounds — if applicable)
10. Experimental Setup
11. Results and Discussion
12. Conclusion
13. References (IEEE numeric `[1]`)
14. Biographies (journal only)

**Citation style:** **IEEE numeric**, sorted by order of appearance.
Format:
> `[3] J. Smith, A. Doe, and K. Lee, "Title of paper," *IEEE Trans. Foo*,
> vol. 12, no. 3, pp. 45–58, Mar. 2023, doi:10.1109/xxxx.`

**Typography hints:**
- Two-column layout (the template should note this; we render single-column
  Markdown but flag it in the publication checklist).
- Figure captions below figures, table captions above tables.
- Algorithm pseudocode uses `\begin{algorithm}` blocks (or fenced ``` blocks
  in Markdown).

---

## 3. ACM (SIGCHI / SIGGRAPH / SIGCOMM / etc.)

**Audience:** HCI, systems, networking, graphics, security.
**Tone:** formal but story-driven; HCI papers especially privilege narrative.

**Section order:**
1. Title (often a benefit / question phrasing)
2. Authors with ACM-style affiliations and emails
3. Abstract (150–200 words)
4. CCS Concepts (`<concept_id>`) — pick from the ACM CCS taxonomy
5. Keywords
6. Introduction
7. Related Work
8. (Optional) Formative Study / Background
9. System / Method / Study Design
10. Implementation (systems papers) **or** Procedure (HCI / user study)
11. Evaluation
12. Findings / Results
13. Discussion (including design implications for HCI)
14. Limitations and Future Work
15. Conclusion
16. Acknowledgments
17. References (ACM Reference Format — numeric)
18. Appendices

**Citation style:** ACM Reference Format (numeric). Example:
> `[12] Jane Smith, Alice Doe, and Kim Lee. 2024. Title of paper. In
> *Proceedings of the 2024 CHI Conference (CHI '24)*. ACM, New York, NY,
> USA, 1–14. https://doi.org/10.1145/xxxxxxx.xxxxxxx`

---

## 4. Nature / Science (structured report)

**Audience:** broad scientific audience; high-impact biology, chemistry,
physics, interdisciplinary.
**Tone:** narrative, accessible to non-specialists, tightly word-budgeted.

**Section order (Nature Article):**
1. Title (≤ 15 words, declarative finding)
2. Authors and affiliations
3. **Abstract** (150–200 words, structured implicitly:
   context → gap → approach → key result → implication)
4. **Main text** (no "Introduction" header — opens with context paragraph)
5. **Results** (with subheadings)
6. **Discussion**
7. **Methods** (online methods, separately formatted, more detailed)
8. **References** (Nature numeric, max 50 in main text for Articles)
9. **Acknowledgments**
10. **Author contributions** (CRediT taxonomy)
11. **Competing interests**
12. **Data availability**
13. **Code availability**
14. **Extended Data figures and tables**
15. **Supplementary Information** (separate file)

**Citation style:** **Nature numeric superscript** in text (`…shown earlier^3,7`),
references listed in order of appearance.

**Word limits:**
- Article: ~3,000 words main text + ~50 references
- Letter: ~1,500 words + ~30 references

---

## 5. Harvard-style social science / business / humanities

**Audience:** social sciences, business, education, humanities.
**Tone:** discursive, argument-driven, theory-grounded.

**Section order:**
1. Title page
2. Abstract (150–250 words)
3. Keywords
4. Introduction
5. Theoretical / Conceptual Framework
6. Literature Review
7. Research Questions / Hypotheses
8. Methodology (with positionality / reflexivity if qualitative)
9. Findings / Analysis
10. Discussion
11. Implications (theoretical, practical, policy)
12. Limitations
13. Conclusion
14. References (Harvard author-year)
15. Appendices

**Citation style:** **Harvard (author, year)** in text, alphabetical reference
list. Example:
> "Recent work has challenged this view (Smith and Doe, 2023, p. 45)."

Reference entry:
> `Smith, J. and Doe, A. (2023) 'Title of article', *Journal Name*, 12(3),
> pp. 45–58. doi:10.1234/xxxx.`

---

## 6. Literature review (standalone)

See `references/literature-review-guide.md` for the full methodology. Section
order:

1. Title
2. Abstract (structured: background, objectives, methods, results, conclusions)
3. Keywords
4. Introduction (problem, scope, research questions)
5. Methodology (search strategy, inclusion / exclusion, screening,
   quality assessment — PRISMA flow diagram if systematic)
6. Conceptual map / taxonomy of the field
7. Thematic synthesis (one section per theme)
8. Cross-cutting observations
9. Gaps and open problems
10. Future research agenda
11. Conclusion
12. References
13. Appendices (search strings, PRISMA checklist, included-studies table)

---

## 7. Thesis / dissertation chapter

Section order varies by institution; default to:

1. Chapter title
2. Chapter abstract (1 paragraph)
3. Introduction to the chapter (link to thesis arc)
4. Background specific to the chapter
5. Method
6. Results
7. Discussion
8. Chapter summary (link forward to next chapter)
9. References (consolidated at end of thesis or per-chapter, follow institution)

---

## 8. Technical whitepaper (industry)

**Audience:** practitioners, decision-makers, technical leadership.
**Tone:** authoritative but accessible; less formal than journal papers.

**Section order:**
1. Cover page (title, version, date, authors, organization)
2. Executive summary (½–1 page)
3. Introduction / Problem statement
4. Background and context
5. Approach / Solution architecture
6. Implementation details
7. Case studies / Benchmarks
8. Comparative analysis (vs. alternatives)
9. Risk and limitations
10. Best practices / Recommendations
11. Roadmap / Future work
12. Conclusion
13. References
14. About the authors / About the organization
15. Appendices

**Citation style:** Author-year (Harvard) or numbered footnotes — pick one and
be consistent.

---

## 9. Survey paper / state-of-the-art review

**Audience:** researchers entering or surveying a field.
**Tone:** organizing, taxonomic, comparative.

**Section order:**
1. Title (often "A Survey of …" or "A Comprehensive Review of …")
2. Abstract
3. Keywords
4. Introduction (scope, what the survey covers and excludes, how it was done)
5. Background and notation
6. **Taxonomy** (the core contribution — a classification of methods)
7. One section per category in the taxonomy
8. Comparative analysis (large summary table is canonical)
9. Datasets and benchmarks
10. Open challenges and research directions
11. Conclusion
12. References (often 100–300 entries)

---

## 10. Policy brief / policy paper

**Audience:** policymakers, civil servants, advocacy groups.
**Tone:** concise, recommendation-driven, evidence-cited.

**Section order:**
1. Title
2. Issue summary (1 paragraph)
3. Key messages (3–5 bullets)
4. Background / Context
5. Analysis of the current situation
6. Policy options (compared in a table)
7. Recommended option with justification
8. Implementation considerations
9. Risks and mitigations
10. Conclusion
11. References / Sources
12. About / Disclaimer

**Length:** 4–8 pages typical.

---

## 11. Universal mandatory blocks

Regardless of format, the skill always emits:

- **Plain-English summary** (after the abstract or at the start of the intro).
- **Limitations** section.
- **Future work** section.
- **Reproducibility statement** (data, code, environment, prompts).
- **Known gaps** block at the very end if any `[CITATION NEEDED]` or
  `[UNVERIFIED]` markers remain.

These can be relabeled to suit the venue (e.g., "Threats to validity" in
software engineering, "Boundary conditions" in management research) but the
content must be present.
