# arXiv

Strategy for searching arXiv via API.

---

## Endpoint

```
https://export.arxiv.org/api/query
```

Returns Atom XML. The Python toolchain (`toolchains/arxiv_search.py`)
handles parsing via `feedparser`; if Python is unavailable, parse the
XML directly via `WebFetch`.

---

## Query construction

Parameters:

- `search_query` — Boolean expression with field prefixes.
- `start` — pagination offset.
- `max_results` — page size (≤ 2000).
- `sortBy` — `relevance` (default) | `submittedDate` | `lastUpdatedDate`.
- `sortOrder` — `ascending` | `descending`.

### Field prefixes

- `ti:` title
- `au:` author
- `abs:` abstract
- `cat:` category (e.g., `cs.LG`, `stat.ML`, `physics.optics`)
- `id:` arXiv ID
- `all:` all fields

### Boolean operators

- `AND` (default if omitted)
- `OR`
- `ANDNOT`
- Parentheses for grouping
- `%22...%22` for phrases (URL-encoded quotes)

---

## Examples

### Standard topic search

```
search_query=all:%22graph+neural+network%22+AND+all:%22fraud+detection%22&max_results=30&sortBy=relevance&sortOrder=descending
```

### Recent CS-ML papers only

```
search_query=cat:cs.LG+AND+all:%22retrieval+augmented%22&max_results=20&sortBy=submittedDate&sortOrder=descending
```

### Author-focused

```
search_query=au:%22Yann+LeCun%22+AND+ti:%22deep+learning%22&max_results=10
```

### Multi-category

```
search_query=(cat:cs.LG+OR+cat:cs.CL)+AND+all:%22few-shot+prompting%22
```

---

## Pagination

arXiv enforces **no more than ~2000 results per query** and a polite
**3 s delay** between successive queries. The toolchain
(`toolchains/arxiv_search.py`) implements this delay automatically.

---

## Result fields

Each entry in the Atom feed has:

- `<id>` — arXiv URL with abs ID (e.g., `http://arxiv.org/abs/2403.01234v2`)
- `<title>` — paper title
- `<author>` — multiple, each with `<name>`
- `<summary>` — abstract
- `<published>` — first submission date
- `<updated>` — last revision date
- `<arxiv:primary_category>` — primary subject category
- `<arxiv:doi>` — published DOI (if available)
- `<arxiv:journal_ref>` — journal reference (if published)

---

## Mapping to canonical metadata

```yaml
- id: <author_year_word>
  type: preprint                 # or "article-journal" if journal_ref present
  authors: [{family: ..., given: ...}, ...]
  year: <int from published>
  title: "<title>"
  arxiv_id: "<2403.01234>"        # without 'v' suffix unless pinning
  doi: "<from arxiv:doi if present>"
  url: "https://arxiv.org/abs/<id>"
  container: "arXiv"               # or journal_ref if published
  notes: "<short summary derived from abstract>"
  verification: verified
```

---

## Categories worth knowing

| Category code | Field                                         |
| ------------- | --------------------------------------------- |
| `cs.LG`       | Machine Learning                               |
| `cs.CL`       | Natural Language Processing                    |
| `cs.CV`       | Computer Vision                                |
| `cs.AI`       | Artificial Intelligence                        |
| `cs.IR`       | Information Retrieval                          |
| `cs.CR`       | Cryptography & Security                        |
| `cs.DB`       | Databases                                      |
| `cs.DC`       | Distributed Computing                          |
| `cs.HC`       | Human-Computer Interaction                     |
| `cs.SE`       | Software Engineering                           |
| `stat.ML`     | Machine Learning (statistics)                  |
| `q-bio.*`     | Quantitative Biology                           |
| `physics.*`   | Physics subfields                              |
| `math.*`      | Mathematics subfields                          |
| `econ.*`      | Economics                                      |
| `eess.*`      | Electrical Engineering & Systems Science       |

---

## Best practices

- **Start broad, narrow with categories.** Run `all:<keywords>` first
  to see what categories the topic spans, then re-query with
  `cat:<category>` for precision.
- **Use exact phrases for multi-word terms.** `%22graph+neural+network%22`
  beats `graph+neural+network`.
- **Sort by relevance** for general searches; **submittedDate** for
  "what's new" queries.
- **Always cite the version** when the paper was last updated (use the
  `v` suffix in `arxiv_id`).
- **Prefer the journal version** over the arXiv preprint when both
  exist (per `sources/source-priority.md §5`).

---

## Failure modes

| Issue                                  | Recovery                                          |
| -------------------------------------- | ------------------------------------------------- |
| Query returns 0 results                  | Drop adjectives; try synonyms; broaden category   |
| Query returns thousands                  | Add a category filter; add a year filter           |
| arXiv API timeout                        | Retry once after 5 s; fall back to Semantic Scholar |
| arXiv ID won't resolve                   | Check the version suffix; try without it           |
| Paper has DOI but no journal_ref         | Use Crossref to resolve venue                       |

---

## Privacy / etiquette

arXiv is run by Cornell on a thin budget. Be polite:

- Insert ≥ 3 s delay between requests (toolchain does this).
- Don't crawl bulk; query with specific terms.
- Identify your client via a `User-Agent` header when possible.

The toolchain `toolchains/arxiv_search.py` follows these conventions.
