# PubMed

The gold standard for biomedical literature. Free, well-documented,
extensive metadata.

---

## Endpoints

PubMed uses the NCBI E-utilities:

- **Search:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi`
- **Fetch:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi`
- **Summary:** `https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi`

PMC (full-text open access):

- **Search:** same `esearch.fcgi` with `db=pmc`.
- **Fetch full text:** `efetch.fcgi?db=pmc&id=<PMC_ID>&rettype=xml`.

---

## Workflow: search → ID list → fetch

### Step 1 — esearch (returns PMIDs)

```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi
    ?db=pubmed
    &term=<query>
    &retmax=<int>
    &sort=relevance | pub+date
    &mindate=YYYY/MM/DD
    &maxdate=YYYY/MM/DD
    &retmode=json
```

Response:
```json
{
  "esearchresult": {
    "count": "1842",
    "idlist": ["38123456", "38098765", ...]
  }
}
```

### Step 2 — efetch (full metadata for PMIDs)

```
GET https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi
    ?db=pubmed
    &id=38123456,38098765,...
    &rettype=abstract
    &retmode=xml
```

Returns rich XML with title, authors, affiliations, abstract, MeSH
terms, journal info, DOI, etc.

---

## MeSH (Medical Subject Headings)

PubMed's controlled vocabulary. Use MeSH for **precision**:

- `term=...[MeSH]` to match a MeSH term.
- `term=...[MeSH Major Topic]` to match papers where the term is a
  primary topic.

### Examples

```
term=("Neural Networks, Computer"[MeSH] AND "Drug Discovery"[MeSH])
term=("COVID-19"[MeSH Major Topic] AND "Vaccines"[MeSH])
```

When the user's topic isn't a MeSH term, fall back to keyword search:

```
term=large+language+model[Title/Abstract]
```

---

## Field tags

Restrict where to search:

- `[Title/Abstract]` — title or abstract
- `[Author]`
- `[Journal]`
- `[Affiliation]`
- `[MeSH]`, `[MeSH Major Topic]`
- `[PT]` — publication type (e.g., `Review[PT]`, `Randomized
  Controlled Trial[PT]`)
- `[Language]`

### Date filtering

```
&mindate=2020/01/01&maxdate=2024/12/31&datetype=pdat
```

(`pdat` = publication date.)

---

## Mapping to canonical metadata

From the efetch XML:

```yaml
- id: <author_year_word>
  type: article-journal
  authors:
    - {family: "Smith", given: "Jane A."}
    - ...
  year: <int>
  title: "<ArticleTitle>"
  container: "<Journal Title>"
  volume: "<Volume>"
  issue: "<Issue>"
  pages: "<Pagination/MedlinePgn>"
  doi: "<ELocationID with EIdType=doi>"
  url: "https://pubmed.ncbi.nlm.nih.gov/<PMID>/"
  notes: "<AbstractText, truncated to 600 chars>"
  pmid: "<PMID>"
  pmc_id: "<PMCID if available>"
  verification: verified
```

---

## Publication-type filtering

Useful filters:

- `Randomized Controlled Trial[PT]` — strongest evidence.
- `Meta-Analysis[PT]`.
- `Systematic Review[PT]`.
- `Review[PT]`.
- `Practice Guideline[PT]` — clinical guidelines.
- `Comparative Study[PT]`.

For evidence-graded queries, prefer reviews and meta-analyses first.

---

## Best practices

- **Use MeSH when possible** — it's far more precise than keyword
  search for biomedical topics.
- **Filter by publication type** for evidence-quality queries.
- **Date filter** — biomedical papers age differently than CS papers;
  10-year window is reasonable, 20+ years for foundational topics.
- **Pull abstracts** in efetch — PubMed has near-universal abstract
  coverage.
- **Check PMC** when full text matters; many recent papers are OA via
  PMC.

---

## Failure modes

| Issue                                  | Recovery                                          |
| -------------------------------------- | ------------------------------------------------- |
| esearch returns 0                       | Drop MeSH tag; widen to keyword search             |
| efetch returns malformed XML            | Reduce batch size (try 10 PMIDs at a time)         |
| Rate limit (3 req/s without API key)    | Insert sleeps; consider NCBI API key for ≤ 10 req/s |
| Paper has PMID but no DOI               | Use the PubMed URL as canonical                    |
| Foreign-language paper                   | Skip unless `--language` allows                     |

---

## NCBI API key

Free with an NCBI account. Increases rate limit from 3/s to 10/s.
Pass via:

```
&api_key=<your-key>
```

The skill works without a key; with a key, biomedical-heavy runs are
~3× faster.

---

## Anti-patterns

- ❌ Treating PubMed as a full-text source. It's an index; PMC is the
  full-text counterpart for OA.
- ❌ Ignoring publication type. A case report and a systematic review
  on the same topic deserve very different treatment.
- ❌ Running unbounded queries. PubMed has 35M+ papers; always
  date-filter.
- ❌ Using only PubMed for clinical questions — Cochrane Library has
  higher-quality systematic reviews for many topics.
