# Prompt: Literature Search

Used in `workflows/research-orchestration.md §3 Literature review`.

---

## Phase 1 — Build the search strategy

```
You are a research librarian. Given the topic and research questions in
paper-spec.md, design a systematic literature search.

Outputs:

1. Boolean search strings (one per database / search engine), structured
   as PICO / SPIDER / CIMO components joined with AND, with synonyms inside
   each component joined with OR.

2. List of databases to consult, in priority order. Pick at least 3
   appropriate to the domain (see references/source-evaluation.md §3 for
   gold-standard sources by domain).

3. Date range, language, and other inclusion / exclusion criteria, in a
   table.

4. Quality assessment rubric to apply to each candidate paper (CASP / JBI /
   MMAT / AMSTAR-2 / custom — see references/literature-review-guide.md §5).

5. Snowballing plan: forward and backward chasing from a starter set of
   anchor papers.

Write all of this to lit-search-plan.md.
```

---

## Phase 2 — Execute (with web tools)

```
For each search string + database in lit-search-plan.md:
  1. Run the search (web_search or database API).
  2. Capture the top N results (default 50).
  3. Deduplicate by DOI and (first author, year, title prefix).
  4. For each candidate, fetch metadata (title, authors, year, venue,
     abstract, DOI, citation count).
  5. Score each with the source-evaluation rubric
     (references/source-evaluation.md §1).
  6. Drop sources scoring < 5 unless directly relevant.
  7. For each kept candidate, decide:
     - Include in main reference list
     - Include in appendix only (background / context)
     - Defer to snowballing pool

After processing all databases, output:
- bibliography.yaml (canonical metadata for kept sources)
- lit-screening-log.md (what was searched, what was found, what was kept,
  what was excluded with reasons)
- prisma-numbers.md (counts at each stage for the PRISMA flow diagram)
```

---

## Phase 3 — Execute (offline, no web tools)

```
Without web access, you must rely on your training-data knowledge of the
field. Be EXPLICIT about uncertainty:

For each topic in lit-search-plan.md:
  1. List 10-30 sources you are CONFIDENT exist (you've seen them cited
     repeatedly, you can name authors / years / venues / approximate
     contributions).
  2. For each, fill in the canonical metadata in bibliography.yaml. If you
     don't know a field (page numbers, DOI, exact volume / issue), set it to
     null and add the entry to "uncertain_fields".
  3. Mark every offline-sourced entry with verification: "unverified-offline"
     in its YAML metadata.
  4. NEVER invent: DOIs, page numbers, volumes, journal names you're not
     sure of, or coauthors you don't recall.
  5. If you can't confidently cite a source for a claim the paper needs,
     write [CITATION NEEDED — search topic: "<phrase>"] in the paper
     instead of inventing one.

Output bibliography.yaml + lit-search-offline-notes.md listing every
"unverified-offline" entry that needs human verification before
submission.
```

---

## Phase 4 — Theme extraction

```
Group the included sources by theme. Aim for 3-7 themes that organize
the field meaningfully (not just "older papers" / "newer papers").

For each theme:
  - Theme name
  - 1-2 sentence description
  - List of cite keys belonging to this theme
  - Key debates within the theme
  - Where this theme connects to the paper's contribution

Output: lit-themes.md.

This file feeds the §2 Related Work or the body of the literature review.
```

---

## Source-quality scoring template (per candidate)

```yaml
- cite_key: smith2023llm
  authority: 4    # peer-reviewed top venue
  rigor: 3        # pre-registered, code released, n large
  recency: 3      # 2023 + directly relevant
  total: 10
  decision: include
  notes: "Anchor source for the contribution chain."

- cite_key: doe2018survey
  authority: 3
  rigor: 2
  recency: 1     # 2018, but still the canonical survey of the topic
  total: 6
  decision: include-as-foundational
```

---

## What to NOT do

- **Do not** invent citations to fill density floors. If the field genuinely
  has thin coverage on a sub-topic, say so in the limitations.
- **Do not** cite Wikipedia or generic blog posts as primary sources for
  substantive claims.
- **Do not** rely on a single source for a load-bearing claim — triangulate.
- **Do not** skew toward your own (model's) most-recent training-data
  recency — older foundational papers must be included for fields with
  long histories.
