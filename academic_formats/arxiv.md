# arXiv Style Guide

Concise venue-specific style notes. Read together with
`templates/arxiv-paper.md`.

## Front matter

- **Title:** Title Case for major words, lowercase for prepositions / articles.
- **Authors:** comma-separated; affiliations linked with superscript numerals.
- **Abstract:** single paragraph, 150–250 words. No citations (arXiv allows
  citations but prefer none for crispness).
- **Keywords:** include 4–8 indexable terms.

## Sectioning

- Numbered sections (1, 2, 3, …) with sub-numbering (1.1, 1.2, …).
- Section titles use sentence case ("Related work", not "Related Work").
- The first section after the abstract is "Introduction".
- "Related Work" can be §2 or §6 depending on subfield convention.

## Citations

- Author–year (Harvard-like) is most common in ML/AI subfields. Numeric
  brackets `[1]` are common in CV / systems subfields.
- Don't switch styles mid-paper.
- For ML preprints, **natbib `\citep` and `\citet`** is standard in LaTeX:
  - `\citet{smith2023}` → "Smith et al. (2023) showed …"
  - `\citep{smith2023}` → "(Smith et al., 2023)"

## Equations

- Numbered display equations are the norm. Reference as "Eq. (1)" or "(1)".
- Define every symbol on first use.
- Keep equations on one line when possible; break with `\\` only when
  necessary.

## Figures and tables

- Figures: caption below; numbered "Figure 1.".
- Tables: caption above; numbered "Table 1.".
- Subfigures lettered (a), (b), (c). Reference as "Figure 1(a)".
- Use vector formats (PDF / SVG) for line drawings; PNG ≥ 300 DPI for
  raster.

## Algorithms

- Use the `algorithm` / `algorithmicx` LaTeX package. In Markdown drafts,
  use a fenced code block titled `Algorithm 1: <name>`.
- Number lines.
- Specify Input and Output explicitly.

## Notation

- Vectors lowercase bold (`x`), matrices uppercase bold (`A`),
  scalars lowercase italic (`α`).
- Define a notation block in §3 if the paper has many symbols.

## Reproducibility

- Include code repo URL in footnote on the first page **or** in a
  Reproducibility section before References.
- For NeurIPS / ICML / ICLR submissions: also include a Reproducibility
  Checklist.

## Broader Impacts

- Required for NeurIPS-style submissions (a 1–2 paragraph subsection
  before References).

## Word / page limits

- arXiv: no limit.
- NeurIPS / ICML / ICLR: 8–9 pages main + unlimited appendix; check the
  current year's CFP.
- ACL / EMNLP: 8 pages main + unlimited appendix.
- CVPR / ICCV / ECCV: 8 pages main + unlimited appendix.

## Submission hygiene

- Anonymize for double-blind venues: remove author names, "we" can stay
  but avoid first-person revealing self-citations ("In our prior work
  [4] …" → "Prior work [4] …").
- Double-check the references list compiles cleanly in BibTeX.
- Compile once with `--strict` to catch undefined references.
