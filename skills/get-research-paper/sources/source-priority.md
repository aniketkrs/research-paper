# Source Priority

The default decision tree for picking which sources to query, in what
order, for a given topic.

> **Rule of thumb:** start domain-specific, fall back to general,
> verify with Crossref + Retraction Watch.

---

## 1. Detect domain

| Topic signal                                     | Primary domain                |
| ------------------------------------------------ | ----------------------------- |
| ML / NLP / vision / RL / LLM / transformer       | CS-ML                         |
| algorithms / data structures / databases / OS     | CS-systems                    |
| HCI / UX / user study / SIGCHI                   | CS-HCI                        |
| cryptography / security / network security       | CS-security                   |
| signal processing / antennas / robotics           | engineering                   |
| physics / quantum / condensed matter              | physics                       |
| chemistry / materials                             | chemistry                     |
| biology / genomics / cell / neuroscience          | biology                       |
| medicine / clinical / RCT / pharma                | biomedical                    |
| psychology / sociology / education / management   | social-science                |
| economics / finance / policy                      | economics-policy              |
| humanities / philosophy / history                 | humanities                    |

If unclear, default to "general" and use Google Scholar + Semantic
Scholar.

---

## 2. Per-domain source priority

### CS-ML / CS-systems / CS-HCI / CS-security

1. **arXiv** (`cs.*` categories) — fast, recent, open access.
2. **Semantic Scholar** — citation graph, abstracts, often has venue
   resolution.
3. **DBLP** — canonical author / venue lists.
4. **Conference-specific repos:**
   - HCI → ACM DL.
   - Systems → USENIX, OSDI, SOSP archives.
   - Security → IEEE S&P, USENIX Security archives.
   - ML → OpenReview (NeurIPS, ICLR, ICML).
5. **Google Scholar** — broad fallback.

### Engineering / physics / math

1. **arXiv** (`eess.*`, `physics.*`, `math.*`).
2. **IEEE Xplore** (engineering).
3. **Semantic Scholar**.
4. **Google Scholar**.

### Biology / biomedical

1. **PubMed** — gold standard for biomedical literature.
2. **PubMed Central (PMC)** — open-access full text.
3. **bioRxiv** — preprints.
4. **Semantic Scholar**.
5. **Google Scholar**.
6. **Cochrane Library** — systematic reviews.
7. **ClinicalTrials.gov** — when relevant.

### Social science / business / education / psychology

1. **Google Scholar** — best coverage.
2. **Semantic Scholar**.
3. **PsycINFO / ERIC** — domain-specific (limited via free API).
4. **JSTOR** — humanities + classics.
5. **SSRN** — preprints (econ, business, law).

### Economics / policy

1. **NBER Working Papers**.
2. **SSRN**.
3. **RePEc**.
4. **Google Scholar**.
5. **Government publication portals** (when relevant): Congress.gov,
   eur-lex.europa.eu, oecd.org.

### Humanities

1. **Google Scholar**.
2. **JSTOR**.
3. **Project MUSE**.
4. **Domain-specific bibliographies** (when known).

---

## 3. Universal verification sources

Run these on every shortlisted paper, regardless of domain:

1. **Crossref API** (`api.crossref.org/works/<doi>`) — confirm DOI,
   fill in missing metadata.
2. **arXiv API** (`export.arxiv.org/api/query?id_list=<id>`) —
   confirm arXiv preprints.
3. **Retraction Watch Database** — check for retraction notices.

---

## 4. Source-priority decision tree

```
START
  │
  ▼
Detect domain (§1)
  │
  ▼
For domain, run sources in priority order (§2)
  │
  ▼
Stop when candidate pool ≥ 3× target N (or all sources exhausted)
  │
  ▼
Deduplicate (workflows/search.md §3)
  │
  ▼
Rank (prompts/ranking.md)
  │
  ▼
Verify shortlisted papers (§3)
  │
  ▼
Drop retractions; flag unverified
  │
  ▼
Output reading list, bibliography, briefing, Known-gaps.md
```

---

## 5. Source weighting in ranking

When the same paper appears in multiple sources, the **highest-quality
source** wins for metadata:

| Source                  | Weight |
| ----------------------- | ------ |
| Crossref-confirmed DOI   | 1.0    |
| Published journal version | 0.95  |
| Conference paper          | 0.90  |
| arXiv preprint            | 0.80  |
| bioRxiv / SSRN preprint   | 0.75   |
| Semantic Scholar metadata | 0.70   |
| Google Scholar metadata    | 0.65   |
| Other / unknown            | 0.50   |

Higher weight → use that source's metadata as canonical.

---

## 6. Source-specific quirks

- **arXiv:** preprints can be updated; cite the latest version unless
  the user wants a specific version.
- **Google Scholar:** results are not stable; record snapshot
  timestamp.
- **Semantic Scholar:** their API is generous but rate-limited
  (~100 / 5 min unauthenticated).
- **PubMed:** use MeSH terms for precision.
- **OpenReview:** includes reviewer comments — useful for assessing
  paper reception.
- **DBLP:** no abstracts; use it for author / venue resolution only.

Per-source full guides: `sources/<source>.md`.

---

## 7. When in doubt

If domain detection fails:
1. Run Google Scholar + Semantic Scholar in parallel.
2. Take the union, deduplicate, rank.
3. The top-ranked papers' venues will reveal the domain; switch
   to domain-specific sources for the next round.

---

## 8. Source override

The user can override the priority via `--source`:

| `--source` value         | Behavior                                  |
| ----------------------- | ----------------------------------------- |
| `arxiv`                  | arXiv only                                |
| `scholar`                | Google Scholar only                       |
| `semantic-scholar`        | Semantic Scholar only                     |
| `pubmed`                 | PubMed + PMC only                          |
| `all` (default)          | Domain-aware priority list                  |
| `peer-reviewed-only`      | Drop preprints (arXiv, bioRxiv, SSRN)      |
| `open-access-only`        | Filter to OA papers (require url)          |

---

## 9. Documentation

For per-source query construction, headers, and rate-limit handling,
see the dedicated `sources/<source>.md` files (currently: arxiv,
google-scholar, semantic-scholar, pubmed). New sources can be added
by dropping a new file and registering it in `manifest.json`.
