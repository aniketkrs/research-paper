# IEEE Style Guide

Concise venue-specific style notes. Read together with
`templates/ieee-paper.md`.

## Front matter

- **Title:** Title Case. No acronyms unless universally known.
- **Authors:** "First M. Last" with member status: "John A. Smith,
  *Member, IEEE*". List affiliation, city, country, email below.
- **Abstract:** ≤ 250 words, single paragraph, NO citations, NO equations.
- **Index Terms:** alphabetical, lowercase except proper nouns,
  comma-separated, immediately after the abstract.

## Sectioning

- Use **Roman numerals** for top-level sections (I., II., III.).
- Use **uppercase letters** for second-level (I.A., I.B.).
- Use **arabic numerals with parens** for third-level (I.A.1) ).
- Section titles in Title Case ("Related Work", not "Related work").
- "Introduction" is §I; references at the end (no trailing § number).

## Citations

- **IEEE numeric**: `[1]`, `[2]`. References numbered in order of first
  appearance.
- Multiple citations in one bracket: `[1], [3], [5]` or `[1]–[3]` for runs.
- In-sentence usage: "as in [3]" or "the authors of [3] showed that …".
- Reference list sorted by appearance number, not alphabetically.

## Equations

- Numbered with right-aligned parens: `(1)`, `(2)`.
- Reference as "(1)" or "Eq. (1)" — be consistent.
- In display, center the equation; keep the number flush right.
- Define every symbol on first use; consider a Notation table.

## Figures and tables

- Figures: caption **below**, "Fig. 1." (note the period and italics for
  the caption).
- Tables: caption **above**, "TABLE I" (uppercase, Roman numeral, no
  period). Table titles in **small caps** when typeset.
- Two-column layout: figures sized for either single-column or full-width
  spans.
- Use **300 DPI** raster minimum; vector preferred for plots.

## Algorithms

- Use the `algorithm` LaTeX package. In Markdown drafts, label
  "Algorithm 1: <Name>".
- Number lines.

## Notation

- Vectors and matrices typically italic bold; scalars italic.
- Use ` ` (\boldsymbol) in LaTeX, **boldface** in Markdown.

## Common abbreviations

- "Fig." for "Figure" — always.
- "vs." for "versus".
- "i.e.," and "e.g.," with commas after.
- Two-letter US state codes for cities: "Boston, MA, USA".
- "doi:" prefix for DOIs in references.

## Reproducibility

- IEEE doesn't mandate a reproducibility checklist for all venues, but
  IEEE Trans. journals increasingly require code/data availability
  statements. Include a brief paragraph before References.

## Acknowledgments

- Section before References.
- Format: "The authors thank …" — no first-person plural here.
- Funding: list grants by number ("This work was supported in part by the
  NSF under Grant XYZ-1234.").

## Page limits

- IEEE conferences: usually 6–8 pages, sometimes with overlength fees.
- IEEE Trans.: usually 12–16 pages.
- Check the venue's specific CFP.

## Reference format example

> [1] J. A. Smith, A. Doe, and K. B. Lee, "Large language models in
> software engineering: A systematic survey," *IEEE Trans. Softw. Eng.*,
> vol. 49, no. 7, pp. 1–37, Jul. 2023, doi: 10.1109/TSE.2023.xxxxxxx.

Italics for journal name (`*Journal*`), volume in number, no italics for
title.
