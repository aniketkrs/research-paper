# Google Scholar

Strategy for searching Google Scholar via web search.

---

## Caveats

Google Scholar **does not have an official API**. Use it via:

1. `WebSearch` with `site:scholar.google.com`.
2. Direct `WebFetch` of `scholar.google.com/scholar?q=...` (parsing
   HTML).

Both are subject to:
- Rate-limiting (Google blocks aggressive scraping).
- Result-order instability (same query, different ordering across
  sessions).
- No DOI / abstract guarantee in the snippet (you usually get title +
  authors + year + venue).

When precision matters, prefer **Semantic Scholar** (has a real API).

---

## Query construction

URL pattern:

```
https://scholar.google.com/scholar?q=<query>&as_ylo=<year_lo>&as_yhi=<year_hi>&hl=en
```

Parameters:

- `q` — keyword query (use `+` for spaces, `%22...%22` for phrases).
- `as_ylo` — year-from filter.
- `as_yhi` — year-to filter.
- `hl=en` — UI language (affects parsing; use `en` for consistency).

### Search operators

- `"exact phrase"` — exact match.
- `OR` — Boolean OR.
- `-term` — exclude term.
- `author:Name` — restrict to author (less reliable than dedicated
  author search).
- `intitle:Word` — word must be in title.
- `source:Venue` — restrict to journal / conference (best-effort).

### Examples

```
"retrieval augmented generation" "code review" 2020..2024
"large language model" software engineering survey
"graph neural network" "fraud detection" -review
```

---

## What to capture per result

For each Scholar result snippet:

- **Title** (top of the result block).
- **Authors / venue / year** (the green line: e.g., `J Smith, A Doe -
  ACM Computing Surveys, 2023`).
- **Abstract excerpt** (the grey paragraph below).
- **Link** (the title hyperlink — may be PDF, journal landing page, or
  university repository).
- **Cited-by count** (e.g., "Cited by 142") — useful for quality
  signals.
- **Versions** (e.g., "12 versions") — indicates how widely cited.

---

## Mapping to canonical metadata

```yaml
- id: <author_year_word>
  type: article-journal | article-conference | preprint
  authors: [{family: ..., given: ...}, ...]
  year: <int>
  title: "..."
  container: "..."                      # parsed from venue line
  url: "<link from snippet>"
  notes: "Cited by N (Scholar). <abstract excerpt>"
  verification: unverified              # always — Scholar metadata is unreliable
```

After capturing, **always run Crossref** on the title to:

1. Resolve the canonical DOI.
2. Confirm authors / venue / year match.
3. Upgrade `verification` to `verified` if Crossref returns a match.

---

## Best practices

- **One query, many results.** Use a broad query and let ranking
  surface the best — don't iteratively narrow without reason.
- **Use year filters.** `2020..2024` filters out older noise.
- **Cited-by ≥ 50** is a useful quality threshold for established
  topics; for new fields, drop it.
- **Cross-check author affiliations.** Scholar happily returns papers
  by people with similar names; verify via Crossref / Semantic
  Scholar.

---

## Failure modes

| Issue                                  | Recovery                                          |
| -------------------------------------- | ------------------------------------------------- |
| Captcha / rate limit                    | Switch to Semantic Scholar; mark Scholar attempts as fallback |
| No results                              | Drop adjectives; try synonyms                      |
| Snippet doesn't include venue           | Use Crossref to resolve from title                 |
| Multiple papers with same title         | Use authors + year to disambiguate                 |
| Foreign-language title                   | Skip unless `--language` allows it                  |

---

## Anti-patterns

- ❌ Treating Scholar metadata as authoritative. It's a starting point;
  always verify via Crossref.
- ❌ Citing the cited-by count in the paper itself. It's useful for
  ranking, not as a claim about the source.
- ❌ Pulling > 100 results. Scholar limits practical scraping; aim for
  20–30 per query, run multiple focused queries.
- ❌ Ignoring "versions" links. They sometimes hide the canonical
  version under a different title.

---

## Why Scholar still matters

Despite its quirks, Scholar:

- Indexes **everything** — journals, conferences, theses, books,
  reports.
- Surfaces **interdisciplinary connections** that domain-specific
  databases miss.
- Provides **citation-count signals** unavailable elsewhere.
- Often catches recent papers before they propagate to other indexes.

Use it as a **broad complement** to domain-specific sources, not as
the only source.
