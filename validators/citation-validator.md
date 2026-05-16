# Citation Validator

## Purpose
Validate citation completeness, formatting consistency, and source quality throughout the paper.

---

## Validation Checks

### Check 1: Citation Coverage

```
SCAN the paper for uncited claims:

REQUIRES CITATION:
- Any factual statement not common knowledge
- Statistics, numbers, percentages
- Definitions from specific sources
- Findings from other studies
- Theoretical frameworks or models
- Methodological approaches attributed to others
- Contested or controversial claims
- Specific dates or historical events (beyond very well-known)

DOES NOT REQUIRE CITATION:
- Common knowledge in the field ("The internet has transformed communication")
- Author's own analysis of their own data (in Results section)
- Logical deductions from presented evidence
- Future research suggestions (author's own)
- General methodological descriptions (e.g., "A t-test was used")

OUTPUT:
- List of sentences that appear to need citations but lack them
- Severity: Critical (factual claim) / Important (attribution) / Minor (context)
```

### Check 2: Citation-Reference Matching

```
CROSS-REFERENCE:
1. Extract all in-text citation keys
2. Extract all reference list entries
3. Compare:
   - Every in-text citation MUST appear in reference list → flag orphan citations
   - Every reference entry SHOULD appear in text → flag orphan references
   - Citation key format must be consistent (author-year vs. numbers)

OUTPUT:
- Orphan citations (cited but no reference entry): [list]
- Orphan references (in list but never cited): [list]
- Formatting mismatches: [list]
```

### Check 3: Format Consistency

```
FOR the chosen citation style, verify:

HARVARD/APA:
□ Author names consistent (same author always spelled same way)
□ "et al." used correctly (3+ authors in-text)
□ Year always present
□ Ampersand vs. "and" used correctly for style
□ Multiple citations separated by semicolons and ordered correctly
□ Direct quotes include page numbers
□ Reference list: alphabetical order maintained
□ Reference list: hanging indent format
□ Reference list: italicization correct (journals, books)
□ Reference list: DOIs formatted correctly

IEEE:
□ Numbers in brackets [N]
□ Numbers sequential (order of appearance)
□ Same source always same number
□ No gaps in numbering
□ Reference list ordered by number
□ Author initials before surname
□ Journal names abbreviated correctly
□ "et al." used for 6+ authors
□ Commas and periods in correct positions
```

### Check 4: Source Quality Assessment

```
FOR EACH cited source, assess:

TIER 1 (Highest quality):
- Peer-reviewed journal articles in reputable journals
- Published books from academic presses
- Government/institutional reports from established bodies
- Systematic reviews and meta-analyses

TIER 2 (Good quality):
- Conference papers from reputable venues
- Working papers from known institutions
- Pre-prints with substantial citations
- Edited book chapters

TIER 3 (Acceptable with caution):
- Non-peer-reviewed reports
- Industry white papers
- News articles from reputable outlets
- Dissertations/theses

TIER 4 (Use sparingly, flag):
- Blog posts (even from experts)
- Wikipedia (never cite directly — use as source-finding tool)
- Social media posts
- Unverified online content
- Opinion pieces without evidence

QUALITY REPORT:
- % of citations that are Tier 1: [target: >50%]
- % of citations that are Tier 1+2: [target: >80%]
- Any Tier 4 citations: [flag for review]
- Recency: % of citations from last 5 years [target: >40%]
```

### Check 5: Citation Density

```
MEASURE citation density per section:

EXPECTED DENSITY:
- Introduction: 4-8 citations per page
- Literature Review: 8-15 citations per page
- Methodology: 2-5 citations per page (methods references)
- Results: 0-2 citations per page (mostly own data)
- Discussion: 5-10 citations per page (comparing with literature)
- Conclusion: 0-3 citations (summarizing)

FLAG:
- Sections with zero citations where they're expected
- Paragraphs making multiple claims with no citations
- Over-citation (every sentence cited) — may indicate insufficient synthesis
```

### Check 6: Self-Citation and Bias

```
CHECK for:
- Excessive self-citation (>20% of references = flag)
- Over-reliance on single source (cited >5 times = flag)
- Citation bias (all sources from one perspective)
- Geographic bias (all sources from one region)
- Temporal bias (all sources old, or all very new)
- Gender bias in citations (if assessable)

RECOMMEND:
- Diversify sources if bias detected
- Include opposing viewpoints
- Balance foundational (older) with recent sources
```

---

## Validation Output Format

```markdown
## Citation Validation Report

### Summary
- Total in-text citations: [N]
- Total reference list entries: [N]
- Match status: [All matched / N orphan citations / N orphan references]
- Format consistency: [Pass / N issues found]
- Citation density: [Adequate / Sparse in sections: X, Y]
- Source quality: [Tier 1: X%, Tier 2: X%, Tier 3: X%, Tier 4: X%]

### Issues Found
1. [Critical] [Description] — [Location in paper]
2. [Important] [Description] — [Location]
3. [Minor] [Description] — [Location]

### Recommendations
- [Specific actionable suggestions]
```
