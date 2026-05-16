# Full Paper Generation Workflow

## Orchestration Steps

This workflow generates a complete research paper from topic to publication-ready output.

---

## Step 1: Topic Analysis and Scoping

**Input:** User's research topic/question
**Output:** Research plan document

```
ANALYZE the topic:
- What is the core research question?
- What discipline(s) does this span?
- What is the expected contribution (novel findings, synthesis, framework, methodology)?
- What is the appropriate scope (narrow focused study vs. broad survey)?
- Who is the target audience (academics, practitioners, policymakers, general)?

DETERMINE paper type:
- Empirical research → data-driven methodology
- Theoretical → framework construction
- Literature review → systematic search methodology
- Case study → qualitative analysis
- Mixed methods → combined approach

DEFINE deliverables:
- Expected page count
- Number of visualizations
- Citation density
- Statistical rigor level
```

## Step 2: Literature Search Strategy

**Input:** Research plan
**Output:** Source database

```
SEARCH STRATEGY:
1. Define primary search terms (3-5 keyword combinations)
2. Define secondary search terms (related concepts, synonyms)
3. Define exclusion criteria (date range, language, publication type)
4. Execute searches across:
   - Academic databases (via WebSearch with scholarly terms)
   - arXiv preprints
   - Government/institutional repositories
   - Industry reports
5. Screen results for relevance (title/abstract level)
6. Deep-read selected sources (full text level)
7. Snowball: check references of key papers for additional sources
8. Record: author, year, title, journal, key findings, methodology, relevance score
```

## Step 3: Evidence Synthesis

**Input:** Source database
**Output:** Evidence map

```
FOR EACH research question:
1. Identify supporting evidence from sources
2. Identify contradicting evidence
3. Rate evidence strength (strong/moderate/weak)
4. Note methodological limitations of each source
5. Identify gaps in the literature
6. Map consensus vs. controversy

BUILD evidence matrix:
| Research Question | Supporting Sources | Contradicting Sources | Evidence Strength | Gap Identified |
```

## Step 4: Methodology Design

**Input:** Research plan + evidence map
**Output:** Methodology section draft

```
SELECT methodology based on:
- Research questions (exploratory → qualitative; confirmatory → quantitative)
- Available data
- Precedent in the field
- Practical constraints

DOCUMENT:
- Research design (experimental, quasi-experimental, observational, descriptive)
- Data collection methods
- Sampling strategy (if applicable)
- Analysis techniques
- Validity and reliability measures
- Ethical considerations
- Limitations acknowledgment
```

## Step 5: Data Analysis (if applicable)

**Input:** Datasets + methodology
**Output:** Findings + visualizations

```
EXECUTE analysis pipeline:
1. Data cleaning and preprocessing
2. Descriptive statistics
3. Inferential statistics (as appropriate)
4. Effect size calculations
5. Confidence interval computation
6. Assumption testing
7. Robustness checks

GENERATE visualizations:
- One visualization per major finding
- Supporting tables for detailed data
- Clear labeling and sourcing
```

## Step 6: Paper Composition

**Input:** All previous outputs
**Output:** Complete paper draft

```
WRITE in sequence:
1. Introduction (hook → context → gap → research questions → contribution → structure)
2. Literature Review (thematic organization → synthesis → gap identification)
3. Methodology (design → data → analysis → validity)
4. Results/Findings (organized by research question → visualizations → interpretation)
5. Discussion (answer RQs → compare with literature → implications → limitations)
6. Conclusion (summary → contributions → future work → closing statement)
7. Abstract (written LAST, summarizing the complete paper in 150-300 words)
8. References (formatted in chosen citation style)
9. Appendices (supplementary material)
```

## Step 7: Visualization Integration

**Input:** Paper draft + data
**Output:** Paper with embedded visualizations

```
FOR EACH finding that benefits from visualization:
1. Select chart type using decision engine
2. Generate visualization code
3. Write caption (Figure N: descriptive title. Source: attribution)
4. Insert in-text reference ("As shown in Figure N...")
5. Add interpretation paragraph
6. Ensure consistent numbering
```

## Step 8: Quality Review

**Input:** Complete draft
**Output:** Reviewed and improved paper

```
RUN review pipeline:
□ All research questions answered in discussion
□ Every claim has supporting citation
□ All figures referenced in text
□ Consistent citation formatting
□ No unsupported generalizations
□ Methodology matches research questions
□ Statistical tests appropriate for data type
□ Limitations honestly acknowledged
□ Academic tone maintained throughout
□ No AI-typical phrasing
□ Transitions between sections are smooth
□ Abstract accurately reflects content
□ Keywords are relevant and specific
□ Word count appropriate for paper type
```

## Step 9: Output Assembly

**Input:** Reviewed paper
**Output:** Final formatted document

```
ASSEMBLE final output:
1. YAML frontmatter
2. Title page (title, author placeholder, date, affiliation placeholder)
3. Abstract and keywords
4. Main body with all sections
5. References/Bibliography
6. Appendices
7. Generate publication readiness score
8. List any caveats or areas needing human review
```

---

## Workflow Variants

### Quick Paper (< 5 pages)
Skip steps 3, 5. Reduce citations to 8-12. Single pass composition.

### Comprehensive Paper (15-30 pages)
Full workflow. Multiple revision passes. 25+ citations. 5+ visualizations.

### Data-Driven Paper
Emphasize steps 5 and 7. Start with data exploration. Let findings drive structure.

### Theoretical Paper
Emphasize steps 2 and 3. Heavy literature engagement. Framework construction focus.
