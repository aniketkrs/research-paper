# Paper Parsing

Heuristics + LLM-assisted parsing to turn raw paper text (regardless
of source) into structured `paper-data.json`.

---

## Pipeline

```
raw text + (optional) external metadata
   │
   ▼
[1] Pre-processing:
       - Normalize whitespace
       - Detect column layout (single / two-column)
       - De-hyphenate at line breaks
       - Strip headers / footers / page numbers
   │
   ▼
[2] Metadata extraction:
       title, authors, year, venue, DOI, arXiv ID
   │
   ▼
[3] Section detection (regex + heuristics):
       per prompts/parse-paper.md
   │
   ▼
[4] Figure / table caption extraction:
       per prompts/parse-paper.md
   │
   ▼
[5] Headline-number extraction (regex on results section):
       per prompts/extract-findings.md
   │
   ▼
[6] Reference parsing:
       detect citation style; extract authors/year/title/venue
   │
   ▼
[7] LLM-assisted enrichment:
       - Generate plain-English layers (per prompts/plain-english.md)
       - Generate mind map (per prompts/generate-mindmap.md)
       - Generate visual summary (per prompts/visual-summary.md)
   │
   ▼
[8] Validate against schemas/visual-paper.json
   │
   ▼
[9] Persist
```

---

## Pre-processing tricks

### De-hyphenation

PDFs hyphenate words across line breaks: `inter-\nesting` → `interesting`.
Apply:

```python
text = re.sub(r"-\n(\w)", r"\1", text)
```

### Column merging (two-column PDFs)

When `pdfplumber` extracts text, two columns may interleave. Detect
by checking if average line length is short. Mitigation: use
pdfplumber's `extract_text(layout=True)` and post-process by x-coord.

### Header / footer stripping

Common page headers ("Smith et al., 2023, ICSE") and footers
(page numbers, copyright) appear on every page. Strip by detecting
text that recurs verbatim on > 50% of pages.

---

## Metadata extraction

| Field | Source priority |
| ----- | --------------- |
| Title | external metadata > first H1 > top-of-page-1 line in larger font |
| Authors | external metadata > arXiv API > author block under title |
| Year  | external metadata > publication-year line > arXiv submission date |
| Venue | external metadata > footer / first-page metadata > journal_ref from arXiv |
| DOI   | external metadata > arXiv API > regex on first 2 pages |
| arXiv ID | URL > footer > regex on first 2 pages |

When external metadata (Crossref, arXiv API) is available, **always
prefer it** over text-extracted values.

---

## Author parsing

Author lines have many formats:

- "Jane A. Smith, Alice Doe, Kim B. Lee"
- "Jane Smith¹, Alice Doe², Kim Lee¹,²"
- "JANE SMITH AND ALICE DOE"
- "Smith, J. A., Doe, A., Lee, K. B."

Strategy:
1. Detect format (comma-separated / "and"-separated / surname-first).
2. Strip footnote markers (`¹`, `²`, `*`, `†`).
3. Split into author tokens.
4. For each: detect `family` (last token if "Given Family", first
   token if "Family, Given").

Edge cases:
- Single-name authors → set `family`, leave `given` empty.
- Suffixes (Jr., III) → keep with family.
- Hyphenated last names → preserve.
- Organization authors → `is_organization: true`.

---

## Reference parsing

Detect citation style by sampling 5 reference entries:

| Pattern | Style |
| ------- | ----- |
| `^[\d+]\s` | IEEE numeric |
| `^\(?\d+\)?\.\s+\w+,\s+\w\.\s` | Nature numeric |
| `^\w+,\s+[A-Z]\.\s+(\d+)` | Harvard / APA |
| `^\w+,\s+[A-Z]\..*?\(\d+\)` | APA |

Once style is known, use a per-style parser:

- **IEEE numeric**: `\[(\d+)\]\s+(.+)` — split into authors, title, venue.
- **Harvard / APA**: comma-separated, parens around year.
- **Nature**: similar to APA but with `&` and bold volume numbers.

Output: array of `{cite_key, authors, year, title, venue, doi}`. For
unparseable entries, store `raw: "<original line>"` with
`parse_confidence: low`.

---

## Headline-number extraction

Run regexes against the abstract + results section:

```
\d+(?:\.\d+)?\s*(?:%|pp|percentage points?|x|times)
\d+(?:\.\d+)?\s*(?:F1|BLEU|accuracy|AUC|MAP|MRR|nDCG)
p\s*[<=]\s*\.?\d+
95\s*%\s*CI\s*\[\s*[\d\.\-]+\s*,\s*[\d\.\-]+\s*\]
Cohen.?s\s*d\s*=\s*[\d\.]+
```

For each hit, capture:
- The number itself.
- The metric label (preceding 1–4 words).
- The context (2–3 sentences containing the number).

Then rank by importance per `prompts/extract-findings.md`.

---

## Validation

After parsing, validate against `schemas/visual-paper.json`:

- `title`: required, non-empty.
- `authors`: array of ≥ 1.
- `year`: required.
- All sections have `id` from the canonical set (or `custom`).
- Cite-keys are unique across `references[]`.

If validation fails, the orchestrator surfaces the violations in
`Known-gaps.md` and proceeds with partial rendering.

---

## Anti-patterns

- ❌ Treating EVERY line over 8 words as section header.
- ❌ Inventing missing metadata (year especially).
- ❌ Stitching together a "Method" section from non-method paragraphs
  because no method header was detected.
- ❌ Discarding a paper because the parser couldn't extract sections.
  Fall back to abstract-only rendering with a flag.
- ❌ Pretending a low-confidence reference is high-confidence.

When in doubt: **partial-but-honest** beats complete-but-fabricated.
