# Prompt: Parse Paper

Take a fetched paper (raw text from arXiv, PDF, URL, or pasted) and
produce a structured `paper-data.json` per `schemas/visual-paper.json`.

---

## Use this prompt verbatim

```
You are parsing a research paper into structured data.

Input:
  Source type: <arxiv | pdf | url | text>
  Raw content:
  <<<
  <full paper text or extracted content>
  >>>

Optional metadata (from arXiv API / Crossref):
  <pre-fetched fields>

Extract the following into a JSON object:

  title          : string
  authors        : [{family, given, affiliation?}, ...]
  year           : int
  venue          : string ("arXiv", journal name, conference name)
  doi            : string (when present)
  arxiv_id       : string (when applicable)
  abstract       : string (verbatim)
  keywords       : [string] (when listed)

  sections       : [
                     {
                       id: "introduction" | "related-work" | "method" |
                           "results" | "discussion" | "limitations" |
                           "conclusion" | "appendix" | "<custom>",
                       title: "<original section title>",
                       text: "<verbatim or near-verbatim section content>",
                       subsections: [{...same shape...}, ...]
                     },
                     ...
                   ]

  figures        : [
                     {
                       number: 1,
                       caption: "<original caption>",
                       extractable: true | false,
                       file: "figures/extracted/figure-1.png" (when extractable),
                       described_in_section: "method"
                     },
                     ...
                   ]

  tables         : [
                     {
                       number: 1,
                       caption: "<original caption>",
                       headers: [string],
                       rows: [[cell, ...], ...],
                       file: "tables/table-1.csv"
                     },
                     ...
                   ]

  headline_numbers : [
                      {
                        value: "84.3%",
                        metric: "accuracy",
                        context: "GSM8K benchmark, 70B model",
                        confidence_interval: "95% CI [82.1, 86.5]"
                      },
                      ...
                    ]

  references     : [
                     {
                       cite_key: "author_year_word",
                       authors: [...],
                       year: int,
                       title: string,
                       venue: string,
                       doi: string (when present)
                     },
                     ...
                   ]

  limitations    : [string]   # extracted from a "Limitations" section
                              # or from "threats to validity"

  contribution_list : [string] # extracted from intro's
                                # "we propose / we show / we release"

Constraints:
- DO NOT invent. If a field is absent, use null or empty array.
- For arXiv-API-fetched papers, prefer the API's metadata over
  inferred values.
- For PDF-extracted papers, the section detection may be noisy;
  flag uncertain sections with `inferred_from_text: true`.
- Keep `text` of each section to ≤ 1000 words. If longer, set
  `text_excerpt` to a 500-word excerpt and note the truncation.
- Headline numbers: pull only what's actually stated. Don't compute
  derived numbers.
- References: parse what's present; if the format is unclear, leave
  as a single `raw: "..."` field.

Output ONLY the JSON object. No surrounding prose.
```

---

## Section detection heuristics

For PDF-extracted text where structure isn't tagged:

1. **Headers**: lines that are short (≤ 10 words), title-cased or
   numbered (`1. Introduction`, `1 Introduction`).
2. **Canonical mapping**: map detected headers to canonical IDs:
   - "Introduction" / "Background" / "Motivation" → `introduction`
   - "Related Work" / "Prior Work" / "Background" → `related-work`
   - "Method" / "Approach" / "System" / "Architecture" → `method`
   - "Experiments" / "Experimental Setup" → `experiments` (sub-section
     of method or results)
   - "Results" / "Evaluation" / "Findings" → `results`
   - "Discussion" / "Implications" → `discussion`
   - "Limitations" / "Threats to Validity" → `limitations`
   - "Conclusion" / "Future Work" → `conclusion`
   - "References" / "Bibliography" → `references` (handled separately)
   - Numbered sections after main body → `appendix`
3. **Boundaries**: a section ends at the next detected header.

If no headers are detected (e.g., extended abstract), set
`structure_inferred: true` and split heuristically by paragraph
breaks.

---

## Figure extraction

Three tiers:

1. **arXiv source available**: download `<id>.tar.gz`, extract figure
   files (`.eps`, `.pdf`, `.png`).
2. **PDF only**: use `pypdf` / `pdfplumber` / `pdfminer` to pull
   embedded images. Match to captions by proximity.
3. **Neither**: mark `extractable: false`. The visualization phase
   will generate Mermaid alternatives.

When extracting, preserve the figure number and caption verbatim.

---

## Table extraction

Two tiers:

1. **HTML / arXiv source**: parse `<table>` tags directly.
2. **PDF only**: heuristic detection (rows of aligned text). May fail
   on multi-column layouts; fall back to inline-text rendering.

Always store the parsed table as both Markdown (in
`paper-data.json → tables[].markdown`) and CSV (`tables/<n>.csv`).

---

## Reference parsing

Patterns to recognize:

- IEEE numeric: `[1] J. Smith, "Title," ...`
- Harvard: `Smith, J. (2023) 'Title', ...`
- APA: `Smith, J. (2023). Title. ...`
- Nature numeric: `1. Smith, J. ... *Journal* 12, 1-10 (2023).`

For each, extract: authors, year, title, venue, DOI / URL. Generate
a `cite_key` as
`<lowercase-first-author-family>_<year>_<first-content-word>`.

If the format is unclear, store `raw: "<original line>"` and set
`parse_confidence: low`.

---

## Anti-patterns

- ❌ Inventing fields not present in the paper.
- ❌ Truncating section text without flagging.
- ❌ Mapping a detected "Discussion" section to `conclusion` because
  it's near the end.
- ❌ Missing headline numbers from the abstract because they were in
  Results too — list both occurrences.
- ❌ Treating a one-sentence paragraph as a section.
- ❌ Parsing 30 references but missing the 4 most-cited.

When in doubt, **partial-but-honest** beats complete-but-wrong.
