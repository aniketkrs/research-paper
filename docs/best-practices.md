# Best Practices and Usage Guide

## For Users of the Research Paper Engine

---

## Getting the Best Results

### 1. Be Specific in Your Request

```
WEAK: "Write a paper about AI"
STRONG: "Write a research paper analyzing the impact of large language models 
on software developer productivity, targeting IEEE format, with emphasis on 
empirical evidence from 2022-2024. Include analysis of code quality metrics, 
development speed, and developer satisfaction. Citation style: IEEE."
```

### 2. Provide Context

The more context you provide, the better the output:
- **Who is the audience?** (Academics, practitioners, executives, students)
- **What venue/format?** (arXiv, IEEE conference, journal, whitepaper, thesis)
- **What depth?** (Quick overview vs. comprehensive deep dive)
- **Any data available?** (CSV, JSON, existing research notes)
- **What citation style?** (Harvard, APA, IEEE, MLA, Chicago)
- **Any specific angles or hypotheses?** (What do you suspect the answer is?)

### 3. Iterate and Refine

The engine works best in conversation:
1. Start with a broad research question
2. Review the generated plan
3. Adjust scope, emphasis, or direction
4. Generate sections incrementally if the paper is long
5. Request specific revisions to sections

---

## Recommended Workflows

### Workflow A: Full Paper (from scratch)

```
1. /research "Your topic" --depth comprehensive
   → Engine generates research plan + structure proposal

2. Review and approve (or adjust) the plan

3. Engine generates paper section by section:
   - Literature search + synthesis
   - Methodology design
   - Data analysis (if applicable)
   - Full paper composition
   - Visualization generation
   - Quality review

4. Review output + request revisions

5. Final formatted output delivered
```

### Workflow B: Data-Driven Paper

```
1. Provide data file: "Analyze this dataset and write findings"
   → Engine ingests and performs EDA

2. Review initial findings, confirm hypotheses to test

3. Engine performs statistical analysis + generates visualizations

4. Engine writes paper framing the analysis within literature

5. Review + iterate on interpretation
```

### Workflow C: Literature Review

```
1. /literature-review "Topic" --years 2020-2024 --systematic

2. Engine proposes search strategy + inclusion criteria

3. Approve (or adjust) methodology

4. Engine conducts systematic search + synthesis

5. Outputs thematic review with gap analysis
```

### Workflow D: Quick Whitepaper

```
1. /whitepaper "Technology/approach" --audience decision-makers

2. Engine generates problem-solution-evidence structure

3. Review + request depth adjustments

4. Final output with executive summary + visuals
```

---

## Scaling Considerations

### Short Papers (< 5 pages, < 3000 words)
- Single-pass generation
- 8-12 citations sufficient
- 2-3 visualizations
- Can be generated in one interaction

### Medium Papers (5-15 pages, 3000-8000 words)
- May require 2-3 interaction rounds
- 15-25 citations
- 4-7 visualizations
- Section-by-section generation recommended

### Long Papers (15-30+ pages, 8000+ words)
- Multiple interaction sessions recommended
- 25-50+ citations
- 8-12 visualizations
- Write to files section by section
- Maintain running citation database in separate file
- Final coherence pass after all sections complete

### Context Window Strategy

For papers approaching context limits:
1. Generate and save each section to a file immediately
2. Keep a running outline showing completion status
3. Maintain citation database in a separate file
4. Reference previous sections by content (not full text) when writing later sections
5. Final assembly: read all section files and ensure coherence

---

## Extensibility Architecture

### Adding New Citation Styles
1. Create new file in `citation_engine/styles/`
2. Follow the format of existing style files
3. Include: in-text examples, reference list format, rules

### Adding New Paper Templates
1. Create new file in `templates/`
2. Follow the structure: format specs → template → guidelines
3. Reference from `manifest.json` supported_paper_types

### Adding New Visualization Types
1. Add to decision engine matrix in `visualization_engine/decision_engine.md`
2. Add code template to `visualization_engine/chart_templates.md`
3. Add caption template to `visualization_engine/caption_generator.md`

### Adding New Methodology Frameworks
1. Add to `methodology_engine/frameworks.md`
2. Update the decision tree with new options
3. Add corresponding statistical guidance if needed

---

## Common Pitfalls and How to Avoid Them

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Scope too broad | Paper tries to cover everything; shallow depth | Narrow to specific research questions |
| Overclaiming | Conclusions exceed evidence | Apply correlation-causation guard; check effect sizes |
| Citation padding | Many citations, little synthesis | Review literature section; ensure thematic organization |
| Visualization overload | Charts everywhere, unclear purpose | Apply decision engine; remove redundant visuals |
| AI voice detected | "In the realm of..." phrasing | Run anti-AI filter; rewrite flagged sentences |
| Methodology mismatch | Method doesn't answer the question | Cross-check RQ → method alignment before writing |
| Missing limitations | Paper seems unrealistically strong | Add honest limitations section (minimum 3) |
| No "so what" | Findings presented without interpretation | Ensure discussion interprets, doesn't just restate |

---

## Failure Handling

### When Sources Are Insufficient
- Acknowledge the limitation explicitly
- Reduce claims to what evidence supports
- Suggest what additional research would be needed
- Flag to user: "The available evidence on this specific question is limited"

### When Data Doesn't Support Hypothesis
- Report null findings honestly
- This IS a valid research contribution
- Discuss potential reasons for null result
- Reframe as exploratory finding
- Never manufacture significance

### When Scope is Too Ambitious
- Propose a reduced scope to user
- Identify the most impactful subset
- Suggest breaking into multiple papers
- Prioritize depth over breadth

### When Contradictory Evidence Exists
- Present both sides fairly
- Analyze methodological differences
- Acknowledge unresolved debates
- Position this paper's contribution within the debate
- Never ignore contradicting evidence

---

## Memory and Long-Context Handling

### During Generation
- Citation database persisted to file after each source is found
- Paper sections saved to files as they're completed
- Quality scores tracked incrementally
- Visualization plan updated as findings emerge

### Across Sessions
- Generated papers stored in user's working directory
- Citation databases reusable for related papers
- Research plans can be resumed

### Token Efficiency
- Prompts are compressed to essential instructions
- Templates loaded on-demand (not all held in context)
- Section-by-section generation prevents context overflow
- Final coherence pass reads only section summaries + transitions
