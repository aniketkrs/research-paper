# Literature Review Workflow

## Purpose
Generate systematic, comprehensive literature reviews that identify patterns, gaps, contradictions, and trajectories in a body of research.

---

## Phase 1: Protocol Definition

```
DEFINE review protocol:
- Research question(s) driving the review
- Inclusion criteria:
  • Date range (default: last 10 years unless topic requires broader)
  • Language (default: English)
  • Publication types (journals, conferences, preprints, reports)
  • Minimum quality threshold (peer-reviewed preferred)
- Exclusion criteria:
  • Irrelevant disciplines
  • Non-empirical opinion pieces (unless reviewing theoretical discourse)
  • Retracted papers
  • Predatory journal publications
- Search databases and sources
- Quality assessment framework
```

## Phase 2: Systematic Search

```
EXECUTE search:
1. Construct search strings:
   - Primary: "exact topic" AND "key concept"
   - Secondary: synonyms, related terms, alternative spellings
   - Tertiary: broader category terms for context

2. Search sources (via WebSearch):
   - "[topic] site:arxiv.org"
   - "[topic] research paper [year range]"
   - "[topic] systematic review"
   - "[topic] meta-analysis"
   - "[topic] empirical study"

3. Record for each result:
   - Title, authors, year, venue
   - Methodology used
   - Key findings
   - Sample size / scope
   - Relevance score (1-5)
   - Quality score (1-5)

4. Apply inclusion/exclusion criteria
5. Document: sources found → screened → included (PRISMA flow)
```

## Phase 3: Thematic Analysis

```
IDENTIFY themes:
1. Read all included sources
2. Extract key concepts, findings, methodologies
3. Code findings into categories
4. Identify recurring themes
5. Map relationships between themes
6. Note evolution of themes over time

ORGANIZE thematically (NOT chronologically unless specifically requested):
- Theme 1: [Core concept area]
  - Sub-theme 1a
  - Sub-theme 1b
- Theme 2: [Related concept area]
- Theme 3: [Methodological approaches]
- Theme 4: [Emerging directions]
```

## Phase 4: Critical Synthesis

```
FOR EACH theme:
1. What do the sources collectively show?
2. Where do sources agree?
3. Where do sources contradict?
4. What methodological patterns emerge?
5. What are the strongest/weakest evidence bases?
6. What remains unexplored?

SYNTHESIS outputs:
- Consensus statements (supported by N sources)
- Debate areas (source A argues X, source B argues Y)
- Evolution narrative (how understanding has changed)
- Gap identification (what nobody has studied)
- Methodological critique (what approaches dominate, what's missing)
```

## Phase 5: Gap Analysis

```
IDENTIFY gaps:
- Topics mentioned but not studied
- Populations not represented
- Methodologies not applied
- Time periods not covered
- Geographic regions excluded
- Intersections not explored
- Practical applications not tested

PRIORITIZE gaps by:
- Significance to the field
- Feasibility of addressing
- Potential impact of findings
- Alignment with current research trends
```

## Phase 6: Composition

```
STRUCTURE:
1. Introduction
   - Why this review is needed
   - Research questions
   - Scope and boundaries

2. Methodology
   - Search strategy (databases, terms, dates)
   - Inclusion/exclusion criteria
   - Quality assessment approach
   - PRISMA flow diagram

3. Findings (organized by theme)
   - Theme 1: synthesis of findings
   - Theme 2: synthesis of findings
   - [Continue for all themes]
   - Cross-cutting observations

4. Discussion
   - Answer research questions
   - State of the field assessment
   - Critical evaluation of evidence quality
   - Implications for theory
   - Implications for practice

5. Future Research Directions
   - Prioritized gap list
   - Suggested methodologies for each gap
   - Expected contributions of future work

6. Conclusion
   - Key takeaways
   - Recommendations
```

## Phase 7: Visualization

```
GENERATE:
- PRISMA flow diagram (Mermaid)
- Thematic map (showing relationships between themes)
- Timeline of key publications
- Evidence strength matrix
- Geographic distribution of studies (if relevant)
- Methodology comparison table
- Citation network visualization (conceptual)
```

## Quality Criteria for Literature Reviews

- [ ] Clear, focused research question(s)
- [ ] Reproducible search methodology
- [ ] Transparent inclusion/exclusion criteria
- [ ] Sufficient source coverage (minimum 15 for narrow, 30+ for broad)
- [ ] Thematic (not just summary) organization
- [ ] Critical evaluation, not just description
- [ ] Gaps clearly identified and justified
- [ ] Implications drawn for theory and practice
- [ ] Future directions are specific and actionable
- [ ] PRISMA or equivalent reporting framework used
