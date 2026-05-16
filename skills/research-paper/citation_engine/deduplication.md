# Citation Deduplication Logic

## Purpose
Prevent duplicate references in the bibliography and maintain clean citation databases across long papers.

---

## Deduplication Rules

### Exact Match Detection
Two references are duplicates if ALL of the following match:
- First author surname
- Publication year
- First 10 words of title (case-insensitive)

### Fuzzy Match Detection
Two references are LIKELY duplicates if:
- Same first author AND same year AND Levenshtein distance of titles < 5
- Same DOI (definitive — always a duplicate)
- Same arXiv ID (definitive — always a duplicate)

### Version Handling
These are NOT duplicates (keep both if both are cited):
- Preprint version AND published journal version (cite the published version preferentially)
- Conference paper AND extended journal version (cite both, noting the relationship)
- Different editions of the same book (cite the edition actually consulted)

### Merge Strategy
When duplicates detected:
1. Keep the entry with MORE complete metadata (DOI, page numbers, volume, issue)
2. Keep the MORE RECENT version (published over preprint, later edition over earlier)
3. Merge unique metadata from both entries into one
4. Update all in-text citation references to point to the surviving entry
5. If using numbered citations (IEEE), renumber after deduplication

---

## Implementation in Paper Generation

### During Source Gathering
```
FOR EACH new source found:
  1. Extract: first_author, year, title, doi
  2. CHECK against existing citation database:
     - doi match? → DUPLICATE (skip)
     - arxiv_id match? → DUPLICATE (skip)
     - author+year+title_prefix match? → LIKELY DUPLICATE (flag)
  3. If likely duplicate:
     - Compare metadata completeness
     - Keep the more complete entry
     - Log the merge decision
  4. If not duplicate:
     - Add to citation database
     - Assign citation key: authorYear (e.g., smith2023)
     - For conflicts: smith2023a, smith2023b (alphabetical by title)
```

### During Paper Assembly
```
BEFORE final output:
  1. Scan all in-text citations
  2. Check each resolves to exactly one reference list entry
  3. Check no reference list entries are orphaned (never cited)
  4. Verify citation keys are unique
  5. For numbered styles: ensure sequential numbering with no gaps
  6. Report: total sources, any unresolved references, any orphans
```

---

## Citation Database Schema

```json
{
  "citation_key": "smith2023",
  "authors": [
    {"given": "John", "family": "Smith"},
    {"given": "Jane", "family": "Doe"}
  ],
  "year": 2023,
  "title": "Title of the paper",
  "container_title": "Journal Name",
  "volume": "45",
  "issue": "2",
  "pages": "123-145",
  "doi": "10.1000/xyz123",
  "arxiv_id": null,
  "url": "https://...",
  "type": "article-journal",
  "accessed_date": "2024-01-15",
  "relevance_score": 4,
  "credibility_score": 5,
  "key_findings": "Brief summary of what this source contributes",
  "cited_in_sections": ["introduction", "literature_review", "discussion"]
}
```
