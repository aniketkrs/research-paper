# ACM Style Guide

Concise venue-specific style notes. Read together with
`templates/acm-paper.md`.

## Front matter

- **Title:** Title Case. HCI papers often use a benefit / question framing.
- **Authors:** "First Last" with affiliations on separate lines, email,
  city, country.
- **Abstract:** 150–200 words.
- **CCS Concepts:** required. Pick from the ACM CCS taxonomy
  (https://dl.acm.org/ccs); format as
  `<concept_id>~Concept name`.
- **Keywords:** comma-separated, lowercase except proper nouns.
- **ACM Reference Format:** include the canonical citation string at the
  start of the paper.

## Sectioning

- **Arabic numerals** (1, 1.1, 1.1.1).
- Section titles in Title Case.
- "References" is unnumbered.

## Citations

- **ACM Reference Format**: numeric `[1]`, in-text by number.
- References in numeric order of first appearance.
- Multiple in one bracket: `[1, 3, 5]` (with commas, no spaces in some
  templates) — match the ACM template you're using.
- Reference example:
  > [12] Jane Smith, Alice Doe, and Kim Lee. 2024. Title of paper. In
  > *Proceedings of the 2024 CHI Conference (CHI '24)*. ACM, New York,
  > NY, USA, 1–14. https://doi.org/10.1145/xxxxxxx.xxxxxxx

## Equations

- Numbered as `(1)` right-aligned.
- Display equations in `equation` or `align` LaTeX environments.

## Figures and tables

- Figures: caption below; "Figure 1." prefix; sentence-case caption.
- Tables: caption above; "Table 1." prefix.
- ACM templates support two-column layout; figures can span single or
  double columns.

## HCI-specific conventions

- **Participant quotes:** italicized, attributed by ID (P1, P2…). Use
  curly quotes (" ").
- **Codebook excerpts:** appendix; use a table.
- **Inter-rater reliability** (Cohen's κ) reported when multiple coders.
- **Demographics table:** standard for user studies.
- **NASA-TLX** and **SUS** scores reported with per-item breakdowns.
- **Open-coding stages:** describe (open / axial / selective if grounded
  theory).

## Systems-specific conventions

- **Performance numbers**: include hardware / OS / load conditions.
- **Benchmarks**: declare the version / commit hash.
- **Reproducibility artifact**: ACM has an artifact-evaluation track —
  include a "Reproducibility" section pointing to the artifact.

## Acknowledgments

- Section before References.
- Funding by grant number.
- Anonymize for double-blind submission.

## Page / word limits

- CHI: 14 pages excluding references; 8 pages for shorter formats.
- SIGGRAPH: 10 pages.
- USENIX / OSDI: 12 pages.
- Check current venue CFP.

## Submission hygiene

- ACM requires the "ACM Reference Format" string in the camera-ready.
- Include CCS concepts in the metadata block.
- Double-check `\thanks{}` for authorship anonymization.
- Use the official `acmart` LaTeX class with the correct sub-template
  (manuscript / sigconf / sigchi / sigplan).
