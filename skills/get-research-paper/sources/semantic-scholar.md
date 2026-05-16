# Semantic Scholar

The most useful general-purpose API for this skill. Free, generous
rate limits, well-documented, and includes citation-graph data.

---

## Endpoint

```
https://api.semanticscholar.org/graph/v1/paper/search
```

Returns JSON. No authentication required for basic use (rate limit
~100 / 5 min); API key bumps it to ~1 req / sec.

---

## Query construction

```
GET https://api.semanticscholar.org/graph/v1/paper/search
    ?query=<topic>
    &limit=<int>           # default 10, max 100
    &offset=<int>           # pagination
    &year=<lo>-<hi>         # year range filter
    &fieldsOfStudy=<csv>    # e.g., Computer Science,Mathematics
    &fields=<csv>           # which fields to return (see below)
```

### Useful `fields`

Comma-separated list. Pick what you actually need to avoid bloat:

- `paperId` — Semantic Scholar's internal ID
- `title`
- `abstract`
- `authors` (object array with `name`)
- `year`
- `venue`
- `publicationVenue` (more structured)
- `journal`
- `externalIds` (DOI, arXiv ID, MAG, PubMed)
- `citationCount`
- `referenceCount`
- `influentialCitationCount` — high-quality citations only
- `openAccessPdf` — direct OA URL when available
- `tldr` — Semantic Scholar's auto-generated 1-line summary
- `fieldsOfStudy`

Recommended fields for our skill:

```
title,abstract,authors,year,venue,publicationVenue,externalIds,citationCount,influentialCitationCount,openAccessPdf,tldr,fieldsOfStudy
```

---

## Example query

```
GET https://api.semanticscholar.org/graph/v1/paper/search
    ?query=retrieval+augmented+code+review
    &limit=30
    &year=2020-2024
    &fieldsOfStudy=Computer+Science
    &fields=title,abstract,authors,year,venue,externalIds,citationCount,tldr
```

---

## Response shape

```json
{
  "total": 142,
  "offset": 0,
  "next": 30,
  "data": [
    {
      "paperId": "abc123...",
      "title": "...",
      "abstract": "...",
      "authors": [{"authorId": "...", "name": "Jane A. Smith"}, ...],
      "year": 2023,
      "venue": "ACM Computing Surveys",
      "publicationVenue": {"id": "...", "name": "...", "type": "journal"},
      "externalIds": {
        "DOI": "10.1145/3589334",
        "ArXiv": "2301.12345",
        "PubMed": "...",
        "MAG": "..."
      },
      "citationCount": 247,
      "influentialCitationCount": 31,
      "openAccessPdf": {"url": "..."},
      "tldr": {"text": "Auto-generated 1-line summary..."},
      "fieldsOfStudy": ["Computer Science"]
    },
    ...
  ]
}
```

---

## Mapping to canonical metadata

```yaml
- id: <derived from authors[0].name + year + first-content-word>
  type: article-journal | article-conference | preprint
  authors:
    - {family: "Smith", given: "Jane A."}
    - ...
  year: <int>
  title: "..."
  container: "<venue>"
  doi: "<externalIds.DOI>"
  arxiv_id: "<externalIds.ArXiv>"
  url: "https://www.semanticscholar.org/paper/<paperId>"
  notes: "<tldr.text>. Cited by <citationCount> (influential: <influentialCitationCount>)."
  quality_score:
    authority: <derive from venue tier>
    rigor: <derive from citationCount + influentialCitationCount>
    recency: <derive from year>
    total: <sum>
  verification: verified  # Semantic Scholar is reliable
```

---

## Author parsing

`authors[i].name` is a single string (e.g., "Jane A. Smith"). Split as:

- **family** = last whitespace-delimited token, minus trailing
  punctuation.
- **given** = everything before the family name.

Edge cases:
- Single-word authors → `family` = the whole name, `given` = "".
- Affiliations like "Smith, J. A." → split at ", ".
- Suffixes like "Jr.", "III" → keep with family name.

---

## Citation-graph features

Semantic Scholar uniquely provides:

- **Cited-by lookup:** `/paper/<paperId>/citations` — papers citing
  this one. Useful for finding follow-ups.
- **References lookup:** `/paper/<paperId>/references` — papers this
  one cites. Useful for finding foundational work (snowballing
  backward).
- **Recommendations:** `/recommendations/v1/papers/forpaper/<paperId>`
  — papers similar to this one.

Use these for **second-pass enrichment** after the initial search.

---

## Best practices

- Always pass `fieldsOfStudy` when domain is known — it dramatically
  improves precision.
- Use `influentialCitationCount` over raw `citationCount` for quality
  signals (it filters out passing-mention citations).
- The `tldr` field is auto-generated — it's a useful seed for your
  summary but should not be the final summary verbatim. Refine it.
- Pagination uses `offset + limit`; max `offset = 1000` for free tier.

---

## Failure modes

| Issue                                  | Recovery                                          |
| -------------------------------------- | ------------------------------------------------- |
| Rate-limit (HTTP 429)                   | Backoff exponentially; retry up to 3×              |
| 0 results                                | Drop adjectives; try `query` with different terms  |
| Field missing in response                | Re-query with explicit `fields` parameter           |
| `paperId` resolves but fields incomplete  | Cross-check with Crossref via DOI                   |
| `externalIds.DOI` is null                | Paper may be preprint-only; mark as preprint        |

---

## API key (optional)

For ≤ 1 req/sec rate limit, request a free key at
`https://www.semanticscholar.org/product/api/`. Pass via header:

```
x-api-key: <your-key>
```

The skill works without a key; with a key, `--depth deep` runs are
~3× faster.

---

## Anti-patterns

- ❌ Trusting `tldr` as the final summary. It's a starting point.
- ❌ Treating `citationCount` as an automatic quality stamp. New
  papers have low counts; old papers have high counts. Normalize by
  age.
- ❌ Ignoring `openAccessPdf`. When present, it's the best link to
  the paper; preferable over a paywalled DOI.
- ❌ Pulling > 100 fields. Bandwidth + parse cost grows fast.
