# Bibliography Generation Engine

## Purpose
Generate properly formatted reference lists from the citation database, respecting the chosen citation style.

---

## Generation Process

### Step 1: Collect All Cited Sources
```
1. Scan the complete paper for all in-text citations
2. Extract unique citation keys
3. Match each key to the citation database
4. Flag any unresolved keys (cited but no database entry)
5. Flag any orphaned entries (in database but never cited)
```

### Step 2: Order References

**Harvard / APA / MLA / Chicago (author-date):**
- Alphabetical by first author surname
- Same author: chronological (oldest first)
- Same author, same year: alphabetical by title → append a, b, c

**IEEE (numbered):**
- Order of first appearance in the paper
- Assign [1], [2], [3]... sequentially
- No reordering after assignment

### Step 3: Format Each Entry

```
FOR EACH citation in the database:
  1. Determine entry type (journal, book, conference, web, report, thesis, preprint)
  2. Load format template for the chosen style
  3. Map database fields to template slots
  4. Handle missing fields:
     - If DOI missing: include URL if available
     - If page numbers missing: include article number if available
     - If volume/issue missing: omit (don't write "n/a")
  5. Apply style rules:
     - Author name format (initials-first vs. surname-first)
     - Punctuation between elements
     - Italicization rules
     - Capitalization (title case vs. sentence case)
  6. Validate: does the entry contain minimum required fields?
     - Author, year, title (minimum for any entry)
     - Additional requirements vary by type
```

### Step 4: Assemble Bibliography Section

```markdown
## References

[Formatted entries, properly ordered]
[Each entry on its own line/paragraph]
[Hanging indent formatting (indicated by markdown or note)]
[Blank line between entries for readability]
```

---

## Minimum Required Fields by Type

| Type | Required | Preferred | Optional |
|------|----------|-----------|----------|
| Journal article | author, year, title, journal | volume, issue, pages, doi | url |
| Book | author, year, title, publisher | edition, city | isbn |
| Conference | author, year, title, conference | pages, publisher | doi, city |
| Website | author/org, year, title, url | accessed date | — |
| Report | author/org, year, title | report number, institution | url |
| Thesis | author, year, title, degree, university | — | url |
| Preprint | author, year, title, repository | arxiv_id | url |
| Dataset | author/org, year, title | repository, doi | version |

---

## Special Cases

### No Author
- Use organization name as author
- If no organization: use title as first element
- APA: move title to author position
- Harvard: use title in author position, alphabetize by first significant word

### No Date
- Harvard/APA: (n.d.)
- IEEE: include note "date unknown" or omit year field

### Multiple Editions
- Always cite the edition consulted
- Note edition number in reference

### Translated Works
- Include original author, translator, original publication year
- Format: Author (Year/Original Year). *Title* (Translator, Trans.). Publisher.

### Forthcoming/In Press
- Harvard/APA: (in press) or (forthcoming)
- Include as much known information as available

---

## Quality Checks for Generated Bibliography

```
□ All in-text citations have corresponding reference list entry
□ No orphaned references (in list but never cited)
□ Consistent formatting across all entries
□ Alphabetical (Harvard/APA) or sequential (IEEE) ordering
□ DOIs formatted correctly (https://doi.org/... for APA, doi: ... for IEEE)
□ No duplicate entries
□ Italicization applied correctly (journals, books)
□ Author names formatted consistently
□ Years present for all entries
□ URLs are complete and properly formatted
□ Minimum 8 references (short paper) or 20+ (comprehensive)
□ Mix of recent and foundational sources
□ Primarily peer-reviewed sources
```

---

## Example Outputs

### Harvard Style Bibliography
```
Brown, A.J. and Wilson, K.M. (2022) 'Machine learning approaches to climate 
    prediction: A systematic review', *Environmental Data Science*, 3(1), 
    pp. 45-67. doi:10.1017/eds.2022.15.

Smith, J.A., Jones, B.C. and Lee, D.R. (2023) 'Transformer architectures 
    for scientific discovery', *Nature Machine Intelligence*, 5(4), 
    pp. 234-248. doi:10.1038/s42256-023-0612-y.

World Health Organization (2023) *Global Health Statistics 2023*. Geneva: WHO.
    Available at: https://www.who.int/data (Accessed: 15 March 2024).
```

### IEEE Style Bibliography
```
[1] J. A. Smith, B. C. Jones, and D. R. Lee, "Transformer architectures 
    for scientific discovery," *Nat. Mach. Intell.*, vol. 5, no. 4, 
    pp. 234–248, Apr. 2023, doi: 10.1038/s42256-023-0612-y.

[2] A. J. Brown and K. M. Wilson, "Machine learning approaches to climate 
    prediction: A systematic review," *Environ. Data Sci.*, vol. 3, no. 1, 
    pp. 45–67, 2022.

[3] World Health Organization. "Global health statistics 2023." WHO. 
    Accessed: Mar. 15, 2024. [Online]. Available: https://www.who.int/data
```
