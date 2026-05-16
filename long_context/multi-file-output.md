# Multi-File Output Protocol

For long papers, the skill writes a structured directory of artifacts
instead of a single Markdown file. This document defines the layout
and the assembly rules.

---

## 1. When to use multi-file output

Use multi-file output when ANY of:

- Estimated paper length > 5,000 words.
- `--depth comprehensive` was requested.
- Paper type is thesis chapter, survey, or systematic review.
- Multi-agent fan-out is active.
- The user explicitly requested it (`--output ./paper-name/`).

Otherwise use single-file output (a single `paper-final.md` in the
working directory).

---

## 2. Layout

```
<paper-name>/
├── paper-spec.md                     # The contract (YAML-ish)
├── outline.md                        # Section structure with status
├── bibliography.yaml                 # Canonical citation database
├── methodology.md                    # Methodology section
├── figures-plan.md                   # Figure / table manifest
├── analysis/
│   ├── data-dictionary.md
│   ├── data-dictionary.csv
│   ├── missing-data.md
│   ├── univariate-summary.md
│   ├── bivariate-summary.md
│   ├── hypothesis-tests.md
│   ├── findings.md
│   ├── figures/
│   │   ├── dist_<col>.png
│   │   ├── corr-heatmap.png
│   │   └── ...
│   └── tables/
│       ├── descriptive.csv
│       └── ...
├── figures/
│   ├── figure-1.png
│   ├── figure-1.svg
│   ├── figure-1.mmd
│   ├── figure-2.png
│   └── ...
├── tables/
│   ├── table-1.csv
│   ├── table-1.md
│   └── ...
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
│   ├── 09-references.md
│   └── 10-appendices.md
├── validation/
│   ├── citation-issues.md
│   ├── statistical-issues.md
│   ├── visual-issues.md
│   ├── structural-issues.md
│   ├── style-issues.md
│   └── validation-report.md
├── review/
│   ├── methodologist-review.md
│   ├── domain-expert-review.md
│   ├── reader-review.md
│   └── review-report.md
├── paper-draft.md                    # All sections concatenated
├── paper-cited.md                    # After citation pipeline
├── paper-final.md                    # Reviewed + revised
├── citation-report.md
├── Known-gaps.md
└── index.md                          # Top-level summary
```

---

## 3. The `paper-spec.md` contract

Generated at the start; updated only when scope changes:

```markdown
# Paper specification

Generated: <ISO timestamp>

## Topic and scope
- Topic: <user's topic>
- Specific research question(s):
  1. ...

## Output
- Type: <research_paper | literature_review | thesis_chapter | ...>
- Format: <arxiv | ieee | acm | nature | harvard | ...>
- Audience: <academic | technical | executive | general>
- Target length: <pages or words>
- Citation style: <harvard | apa | ieee | mla | chicago | nature>
- Output structure: multi-file
- Working directory: ./<paper-name>/

## Inputs from user
- Dataset: <yes/no, brief description, file path>
- Code: <yes/no, link>
- References: <yes/no, format>

## Routing decision
- Intent: ...
- Template: templates/<format>-paper.md
- Execution mode: multi-agent | single-orchestrator
- Multi-file output: true
- Language: en-US
- Anonymized: false

## Defaults assumed
- ...

## Plan (phase status tracking)
- Phase 1: planning           [completed]
- Phase 2: literature review  [in-progress]
- ...

## Risks / unknowns
- ...
```

---

## 4. The `outline.md` contract

Generated after the routing decision. The orchestrator updates section
statuses as drafting progresses:

```markdown
# Outline

## 1. Introduction
- Status: complete
- Word target: 800
- Word actual: 824
- Cite keys: [smith2023, doe2022, lee2021, vaswani2017, ...]
- Figures: []
- Tables: []
- File: sections/01-introduction.md

## 2. Related Work
- Status: complete
- Word target: 1200
- Word actual: 1167
- Cite keys: [...]
- Figures: [figure-1]
- Tables: []
- File: sections/02-related-work.md

## 3. Methodology
- Status: in-progress
- Word target: 1500
...

## 4. Results
- Status: pending
...
```

---

## 5. The `index.md` contract

The single-page summary of every artifact, generated at delivery:

```markdown
# Paper artifacts index

Title: <paper title>
Date: <YYYY-MM-DD>

## Final deliverables
- Paper: paper-final.md
- Bibliography: bibliography.yaml
- Known gaps: Known-gaps.md

## Intermediate artifacts
- Paper spec: paper-spec.md
- Outline: outline.md
- Methodology: methodology.md
- Figures plan: figures-plan.md

## Sections
- 01: sections/01-introduction.md (824 words)
- 02: sections/02-related-work.md (1167 words)
- 03: sections/03-methodology.md (1502 words)
- ...

## Figures
- Figure 1: figures/figure-1.png (architecture diagram)
- Figure 2: figures/figure-2.png (main results bar chart)
- ...

## Tables
- Table 1: tables/table-1.csv (datasets)
- ...

## Analysis
- Findings: analysis/findings.md
- Hypothesis tests: analysis/hypothesis-tests.md
- ...

## Validation
- Validation report: validation/validation-report.md

## Review
- Review report: review/review-report.md

## Quality summary
- Word count: 8,421
- Citations: 47
- Figures: 6
- Tables: 4
- Academic-quality score: 4.2 / 5
- Known gaps: 3 (medium)
```

---

## 6. Assembly

`paper-draft.md` is generated by **concatenating** all sections in
template order. The citation pipeline then reads `paper-draft.md` and
produces `paper-cited.md`. After review and revision, the result is
saved as `paper-final.md`.

The user delivers `paper-final.md`. The rest of the directory is the
audit trail.

---

## 7. Pandoc export

To convert `paper-final.md` to PDF / DOCX / HTML:

```bash
pandoc paper-final.md \
    --include-in-header=../assets/latex-templates/latex-preamble.tex \
    --citeproc --bibliography=bibliography.yaml \
    --csl=ieee.csl \
    -o paper-final.pdf
```

A wrapper script lives at `toolchains/pandoc_export.sh` (when shipped).

---

## 8. Cleanup

After delivery, the user may keep the entire directory (recommended,
audit trail) or just `paper-final.md`. The skill does not auto-clean.

For multi-paper sessions, suggest a top-level `papers/` directory with
one sub-directory per paper.
