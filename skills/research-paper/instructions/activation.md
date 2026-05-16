# Activation Guide

How this skill integrates with Claude Code (and other Agent Skills
runtimes), and exactly when it should and should not engage.

---

## 1. Activation paths

### 1.1 Slash commands (preferred)

```
/research "<topic>" [--options]
/paper "<topic>" [--options]
/literature-review "<topic>" [--options]
/whitepaper "<topic>" [--options]
/thesis "<topic>" [--options]
/survey "<topic>" [--options]
/policy "<topic>" [--options]
```

### 1.2 Natural-language patterns

The skill activates on requests matching:

- "Write a research paper / academic paper / scientific paper on …"
- "Generate a paper / report on …"
- "Do a literature review / systematic review / scoping review on …"
- "Format this draft as IEEE / ACM / arXiv / Nature / Harvard / APA …"
- "Write a thesis chapter / dissertation chapter on …"
- "Produce a whitepaper / survey paper / policy brief on …"
- "Analyze this dataset and write up the findings as a paper."
- "Add citations / bibliography / references in <style>."
- "Peer-review my draft / validate the methodology."

### 1.3 File-type triggers

If the user supplies any of these alongside an academic intent:
`.csv`, `.json`, `.xlsx`, `.bib`, `.tex`, `.parquet`, `.md` (with
research context).

### 1.4 Context signals

Conversation containing words like *research, paper, academic, citation,
methodology, literature review, hypothesis, abstract, manuscript,
preprint, thesis, dissertation, peer review*.

---

## 2. Negative activation

Do NOT activate for:

- Blog posts, marketing copy, tweets, sales emails.
- Single-paragraph factual answers.
- Casual questions ("what's the capital of France?").
- Pure code generation requests with no academic-writing intent.
- Personal letters, fiction, scripts.

If the request is ambiguous, ask one clarifying question.

---

## 3. Command options reference

```
--style [harvard|apa|ieee|mla|chicago|nature|arxiv-numeric]
--format [arxiv|ieee|acm|nature|harvard|literature-review|thesis-chapter|whitepaper|survey-paper|policy-paper]
--depth [quick|standard|comprehensive]
--type [research|review|survey|case|whitepaper|thesis|policy|conference]
--sources [N]
--visualizations [auto|N|none]
--audience [academic|technical|executive|general]
--output [filename or directory]
--language [en-US|en-GB|other]
--anonymize [true|false]
```

Defaults are inferred from topic and request unless explicitly set.

---

## 4. CLAUDE.md integration (recommended)

Add to your project's `CLAUDE.md`:

```markdown
## Custom Skills

When asked to generate research papers, literature reviews, theses,
whitepapers, surveys, or policy briefs, use the `research-paper` skill.

**Trigger patterns:** "write a research paper", "literature review",
"whitepaper", "thesis", `/research`, `/paper`, `/literature-review`.

**Entry point:** `~/.claude/skills/research-paper/SKILL.md`.

**Default citation style:** Harvard.
**Default output format:** Markdown with Mermaid diagrams.
**Visualizations:** auto-generated.
**Plain-English summary:** enabled.
**Review pipeline:** enabled.
```

---

## 5. Module loading sequence (progressive disclosure)

Load **only what is needed** for the current step. Do NOT preload.

### When activating
1. `SKILL.md` (always — this is the entry point)
2. `instructions/core.md` (operating principles + protocol)

### Per phase
| Phase                       | Load                                                       |
| --------------------------- | ---------------------------------------------------------- |
| Intake / scoping             | `prompts/research-planning.md`                              |
| Research plan + outline      | `orchestration/pipeline.md` + relevant `templates/<format>.md` |
| Literature review            | `prompts/literature-search.md` + `workflows/literature-review-guide.md` |
| Methodology                  | `prompts/methodology-design.md` + `methodology_engine/methodology-guide.md` |
| Data analysis                | `workflows/data-analysis-pipeline.md` + `methodology_engine/statistical-methods.md` |
| Visualization                | `visualization_engine/decision-engine.md` + `workflows/visual-generation-pipeline.md` |
| Drafting                     | `prompts/writing-prompts.md` + `style_guides/writing-style-guide.md` (once) |
| Citations                    | `citation_engine/citation-styles.md` + `workflows/citation-pipeline.md` |
| Validation                   | `validators/` + `workflows/validation-pipeline.md`         |
| Review                       | `review_pipeline/three-personas.md` + `rubrics/academic-quality.md` |
| Final delivery               | `quality_control/publication-checklist.md`                 |

### Plain-English summary
`prompts/simplification-prompts.md` (once at the end of drafting).

---

## 6. Output strategies

### 6.1 Single-file (short papers)

```
output/
└── paper-final.md
```

Use for `--depth quick` or any paper ≤ 5 pages.

### 6.2 Multi-file (long papers)

```
output/<paper-name>/
├── paper-spec.md
├── outline.md
├── bibliography.yaml
├── methodology.md
├── figures-plan.md
├── analysis/
├── figures/
├── tables/
├── sections/
│   ├── 00-frontmatter.md
│   ├── 01-introduction.md
│   ├── 02-related-work.md
│   ├── 03-methodology.md
│   ├── 04-results.md
│   ├── 05-discussion.md
│   ├── 06-limitations.md
│   ├── 07-future-work.md
│   ├── 08-conclusion.md
│   └── 09-references.md
├── validation/
├── review/
├── paper-draft.md
├── paper-cited.md
├── paper-final.md
├── Known-gaps.md
└── index.md
```

Use for `--depth comprehensive` or any paper > 5 pages. See
`long_context/multi-file-output.md` for details.

---

## 7. Performance expectations

| Run type                      | Sections produced       | Wall-clock estimate    |
| ----------------------------- | ----------------------- | ---------------------- |
| Quick research paper           | Abstract + 4–6 sections  | 2–5 min                |
| Standard research paper       | Full template (≤ 15 pp) | 5–15 min               |
| Comprehensive paper           | Full + extensive review  | 15–30 min              |
| Literature review             | Search + synthesis       | 10–25 min              |
| Thesis chapter                | Full + cross-chapter ties | 15–25 min              |

Times vary with model speed and tool availability.

---

## 8. Troubleshooting

| Symptom                              | Likely cause                                 | Fix                                                  |
| ------------------------------------ | -------------------------------------------- | ---------------------------------------------------- |
| Skill never activates                 | YAML frontmatter malformed                   | Check `SKILL.md` head                                  |
| Charts come out as Markdown only      | Python deps missing                          | `pip install pandas matplotlib seaborn pyyaml`         |
| Citations malformed                   | Wrong / mixed style                          | Re-run `format_bibliography.py --style <one-style>`    |
| Model fabricated DOIs                  | Guard rails working as intended              | `[UNVERIFIED]` markers; verify offline                 |
| Output truncated mid-section          | Context pressure                             | Switch to multi-file output (§6.2)                     |
| Filesystem errors                      | Tool permissions                             | Grant read/write to working directory                  |
| "I cannot read that file"              | Filesystem tool missing                      | Provide `read_file` to the runtime                     |
