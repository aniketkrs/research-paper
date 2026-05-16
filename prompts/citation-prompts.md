# Prompt: Citations

Used in `workflows/citation-pipeline.md` and during `§7 Drafting`.

---

## When drafting (writer agent)

```
You are inserting in-text citations as you write. You have access to
bibliography.yaml as the single source of truth.

Rules:

1. INSERT placeholders only. Use [cite_key] format. The citation pipeline
   will format them later. Examples:
     "Recent work [smith2023llm] has shown..."
     "Two studies [smith2023llm; doe2022codex] report..."

2. NEVER invent a cite_key. Use only keys present in bibliography.yaml.
   If you need a citation but no entry exists:
   - First, check if a relevant entry already exists under a different key.
   - If not, write [CITATION NEEDED — topic: "<short description>"].
   - The literature-search pipeline will fill these in later.

3. NEVER fabricate metadata. Don't invent DOIs, page numbers, journal
   volumes, or coauthor names. If you don't know a field, leave it null
   in bibliography.yaml.

4. Match citation density to the section
   (references/citation-styles.md §11):
   - Introduction: 6-15 per page
   - Related Work: 15-40 per section
   - Method: 0-5 (cite when adopting a known method)
   - Results: 0-2
   - Discussion: 5-10
   - Conclusion: 0-2

5. Integrate citations into prose. Bad: "(Smith, 2023) (Doe, 2022)".
   Good: "Two recent studies (Smith, 2023; Doe, 2022) report ...".

6. Cite the WORK, not the AUTHOR's opinion. Bad: "Smith says LLMs are
   great." Good: "Smith (2023) reports a 12% accuracy gain on benchmark X."

7. Triangulate load-bearing claims. For any claim that the paper's
   argument depends on, cite >= 2 independent sources. If only one exists,
   present the claim accordingly: "In one recent study, X was observed
   (Smith, 2023); replication is needed."

8. Read the source before citing. Don't cite a paper for a claim it
   doesn't make. (This is the single most common citation error.) If you
   are not 100% sure the source supports the claim, mark
   [VERIFICATION NEEDED — claim: "<claim>"; source: smith2023llm].
```

---

## When formatting the bibliography (citation pipeline)

```
Read references/citation-styles.md for the EXACT rules of the chosen style.
Then run scripts/format_bibliography.py:

  python scripts/format_bibliography.py \
    --bib bibliography.yaml \
    --style <harvard|apa|ieee|mla|chicago-author-date|chicago-notes|nature|arxiv-numeric> \
    --locale <en-US|en-GB> \
    --paper paper-draft.md \
    --out paper-cited.md \
    --report citation-report.md

The script:
- Replaces every [cite_key] with the styled in-text citation.
- Builds the reference list section.
- Numbers references for numeric styles in order of first appearance.
- Disambiguates same-author-same-year (a, b, c).
- De-duplicates by DOI and (author, year, title).
- Reports unresolved keys, missing fields, duplicates.

Then read citation-report.md. If errors:
- Missing keys: add to bibliography.yaml or replace the citation.
- Incomplete entries: fill in required fields.
- Duplicates: merge.
- Orphans: keep with justification or remove.

Re-run the formatter until the report is clean.
```

---

## Style-switching prompt

```
The user wants to change citation style from <FROM> to <TO>.

Procedure:
1. DO NOT edit citations by hand. Re-run the citation pipeline with
   --style <TO>.
2. The script regenerates ALL in-text citations and the entire reference
   list deterministically from bibliography.yaml.
3. Verify the citation-report.md after the switch.
4. Skim the paper to confirm transitions still read well after style
   change (numeric styles read very differently from author-year).

Common gotcha: in author-year styles, narrative use ("Smith (2023)
argued") looks natural; switching to IEEE numeric makes "[3] argued"
which doesn't read - rewrite those sentences to "Smith et al. [3]
argued".

The pipeline flags such cases for the writer to fix.
```

---

## When the user supplies a list of references

```
The user has provided a reference list as text or a BibTeX file.

Procedure:
1. Convert each entry to the canonical YAML schema
   (references/citation-styles.md §"Common metadata fields").
2. Assign a cite_key: <lower(family)>_<year>_<first-content-word>.
3. Validate required fields per type. Fill in DOI / URL where possible.
4. Save to bibliography.yaml.
5. Now you can use [cite_key] placeholders during drafting.

If the user supplies BibTeX:
  python scripts/format_bibliography.py --import-bibtex refs.bib --out bibliography.yaml

If the user supplies plain text:
  Parse manually: extract authors, year, title, venue, DOI. Be cautious
  - if a field is ambiguous, leave it null and surface in Known gaps.
```

---

## When the user supplies an existing paper to cite

```
The user has uploaded a PDF or paper text. Extract the metadata to add
to bibliography.yaml:

1. Title, authors, year, venue from the paper's first page.
2. DOI from the paper if printed; otherwise from a Crossref lookup.
3. arXiv ID if it's a preprint.
4. Pull a 1-3 sentence summary of the contribution to add as 'notes'.

Then use [cite_key] in the draft.
```

---

## Anti-patterns

- Citing a paper to support a claim that paper doesn't actually make.
- Citing only your own group's work (echo chamber).
- Citing only the last 2 years (ignoring foundational work).
- Citing >= 5 papers in one bracket without saying anything about the
  group ("[1, 2, 3, 4, 5]" is meaningless).
- Citation laundering: citing a source you haven't read.
- Inventing DOIs / arXiv IDs to make a fake citation look real.
- Mixing styles in one paper (some [1], some (Smith, 2023)).
- Skipping the de-duplication step (same paper cited under two keys).
