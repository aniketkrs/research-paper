# Research Orchestration Workflow

This is the **master orchestration playbook** for producing a research paper.
Read this when the user requests any academic-writing task. Then, for each
step, read the specific file referenced.

> **Mantra:** "Plan, then execute one step at a time. Persist to disk
> between steps. Never hold the whole paper in working memory."

---

## 0. Preconditions

Before starting, make sure you have:

- A clear understanding of the user's intent (paper type, topic, format,
  data they have or don't, citation style they want).
- A working directory the skill can write to. Default to a sub-directory
  named after the paper, e.g., `./paper-llm-code-review/`.
- (Optional) Access to filesystem read/write tools and `python3`.

If any of these is missing, ask the user **once** before proceeding.

---

## 1. Intake and scoping

**Goal:** convert vague request into a precise paper specification.

**Procedure:**

1. Read `prompts/research-planning.md`.
2. Ask the user (in one consolidated message, no more than 5 questions):
   - **Format:** arXiv / IEEE / ACM / Nature / Harvard / literature review /
     thesis / whitepaper / survey / policy.
   - **Audience:** specialist / cross-disciplinary / decision-maker / general.
   - **Length:** short letter / 8–12 pages / 20+ pages / book chapter.
   - **Data:** do they have a dataset? a code base? a set of references? or
     should you research from scratch?
   - **Constraints:** deadline, venue, anonymization, language.
3. If the user answered ambiguously, infer reasonable defaults from
   `SKILL.md §4 Format selection` and proceed.
4. Write `paper-spec.md` in the working directory, capturing the answers.

**Output:** `paper-spec.md`.

---

## 2. Research plan and outline

**Goal:** produce a section-by-section outline before writing any prose.

**Procedure:**

1. Read the relevant template from `templates/<format>.md`.
2. Read `prompts/research-planning.md`.
3. Draft an **outline** that copies the template's section structure and
   fills each section with:
   - A 1–2 sentence statement of what the section will say.
   - The main figures / tables to include.
   - The citations needed (placeholders like `[smith2023llm]`).
4. Surface this outline to the user for approval **only if** the request
   is ambiguous or open-ended. For tightly-specified requests, skip
   approval and proceed.
5. Write `outline.md` to disk.

**Output:** `outline.md`.

---

## 3. Literature review

**Goal:** assemble the evidence base.

**Procedure:**

1. Read `references/literature-review-guide.md` and
   `references/source-evaluation.md`.
2. Read `prompts/literature-search.md`.
3. For the topic in `paper-spec.md`, build a **search plan**:
   - Boolean search string (per `references/literature-review-guide.md §3.2`).
   - Databases to consult.
   - Inclusion/exclusion criteria.
4. **If web search tools are available:** run the searches; collect
   candidate sources; score each with the `references/source-evaluation.md`
   rubric.
5. **If web search tools are unavailable:**
   - Build a list of citations the model knows and is confident about.
   - For each, mark `[UNVERIFIED — offline]` so the review pass can flag
     them.
   - Never invent DOIs, page numbers, or author lists.
6. Group sources by **theme** (per `references/literature-review-guide.md
   §7`).
7. Write `bibliography.yaml` in the working directory using the canonical
   metadata schema from `references/citation-styles.md §"Common metadata
   fields"`. Each entry has a `cite_key`, full metadata, and `quality_score`.

**Output:** `bibliography.yaml`, `lit-themes.md`.

---

## 4. Methodology design

**Goal:** describe how the research is/was conducted, in enough detail
that another researcher could replicate it.

**Procedure:**

1. Read `references/methodology-guide.md`.
2. Read `prompts/methodology-design.md`.
3. From `paper-spec.md`, identify the **research question type** and pick
   the matching methodology blueprint (quant / qual / mixed / SLR /
   design-science / experimental).
4. Draft the methodology section using the blueprint's required elements.
5. Run a **threats-to-validity** sweep (`references/methodology-guide.md
   §11`) and add a paragraph addressing each.
6. Write `methodology.md` to disk.

**Output:** `methodology.md`.

---

## 5. Data analysis (if a dataset is present)

**Goal:** turn raw data into reportable findings.

**Procedure:**

1. Read `workflows/data-analysis-pipeline.md`.
2. If the user provided a CSV/Excel/JSON file:
   - Run `scripts/analyze_data.py --input <file> --out ./analysis/`.
   - The script produces: data dictionary, summary stats, missing-data
     report, distribution plots, correlation matrix, and a `findings.md`
     stub.
3. If the user did not provide data but the paper is empirical:
   - Generate a **synthetic illustrative dataset** clearly labeled as such.
   - The validation pass will surface this in `Known gaps`.
4. If the paper is theoretical / review-only: skip this step.
5. For statistical claims, run `scripts/statistical_validation.py` against
   the dataset to verify reported test statistics.

**Output:** `analysis/findings.md`, `analysis/data-dictionary.md`,
`analysis/figures/*.{png,svg}`, `analysis/tables/*.csv`.

---

## 6. Visualization planning

**Goal:** decide which figures and tables go in which sections.

**Procedure:**

1. Read `workflows/visual-generation-pipeline.md` and
   `references/visualization-guide.md`.
2. For each section in `outline.md`, ask:
   - Is there a comparison? → bar / line.
   - Is there a distribution? → histogram / violin.
   - Is there a relationship? → scatter / heatmap.
   - Is there a flow / process? → Sankey / flowchart.
   - Is there geography? → map.
   - Is there a structure? → architecture / tree diagram.
3. Build `figures-plan.md` listing every planned figure / table with:
   - ID (`Figure 1`, `Table 2`, …).
   - Section.
   - Type.
   - Source data.
   - Caption sketch.
   - Generation method (script / Mermaid / table only).
4. For each figure: invoke `scripts/generate_charts.py` (if Python
   available) or emit Mermaid / Markdown table.

**Output:** `figures-plan.md`, `figures/*.{png,svg,mmd,md}`.

---

## 7. Drafting

**Goal:** write the prose.

**Procedure (per section, in template order):**

1. Read `prompts/writing-prompts.md` and the relevant section's prompt.
2. Read `references/writing-style-guide.md` once at the start.
3. For each section:
   1. Open the template and locate this section's `<<...>>` slots.
   2. Read the relevant chunk of `bibliography.yaml`, `methodology.md`,
      `analysis/findings.md`, and `figures-plan.md`.
   3. Draft the section, applying the writing-style rules.
   4. Insert in-text citations as `[cite_key]` placeholders — the citation
      pipeline will format them later.
   5. Reference figures / tables by ID (`Figure 3`, `Table 1`).
   6. **Persist the section to disk** (`sections/<NN>-<name>.md`) before
      moving on.
4. After all sections are drafted, concatenate them into `paper-draft.md`
   in template order.

**Output:** `sections/*.md`, `paper-draft.md`.

> **Long-context strategy:** never hold more than 3 sections in working
> memory at once. Persist completed sections to disk and reload only when
> needed for cross-section consistency checks.

---

## 8. Citation pass

**Goal:** convert `[cite_key]` placeholders into the chosen citation style
and produce the reference list.

**Procedure:**

1. Read `workflows/citation-pipeline.md`.
2. Read `references/citation-styles.md` for the chosen style's exact rules.
3. Run `scripts/format_bibliography.py --bib bibliography.yaml --style <style>
   --paper paper-draft.md --out paper-cited.md`.
4. The script:
   - Replaces every `[cite_key]` with the styled in-text citation.
   - Builds the reference list section.
   - Numbers references (for IEEE / Nature / numeric styles) in order of
     first appearance.
   - Disambiguates same-author-same-year (Smith 2023a / 2023b).
   - Reports any unresolved cite keys, missing fields, or duplicates.
5. Manually review the script's report; resolve any errors.

**Output:** `paper-cited.md`, `citation-report.md`.

---

## 9. Validation pass

**Goal:** catch errors before review.

**Procedure:**

1. Read `workflows/validation-pipeline.md`.
2. Run the four validators in sequence:
   - `scripts/validate_citations.py paper-cited.md bibliography.yaml`
   - `scripts/statistical_validation.py paper-cited.md`
   - `scripts/extract_references.py paper-cited.md`
   - Reading-level check (Flesch–Kincaid for plain-English summaries).
3. Each validator produces a report. Aggregate into `validation-report.md`.
4. Fix high-severity issues; surface medium / low issues to user or in
   `Known gaps`.

**Output:** `validation-report.md`.

---

## 10. Review pass

**Goal:** simulated peer review against quality rubrics.

**Procedure:**

1. Read `workflows/review-pipeline.md`.
2. Read `rubrics/academic-quality.md`, `rubrics/methodology-rigor.md`,
   `rubrics/citation-quality.md`, `rubrics/visual-quality.md`.
3. Run the **simulated reviewer** prompt from `prompts/review-prompts.md`
   in three personas:
   - **The methodologist** — looks at validity, sample size, statistical
     methods.
   - **The domain expert** — looks at framing, prior work, theoretical
     contribution.
   - **The reader** — looks at clarity, narrative, accessibility.
4. Each persona scores against the rubric and lists 3–5 concrete suggestions.
5. Apply the suggestions in priority order (severity × ease).
6. Re-run validation if material changes were made.

**Output:** `review-report.md`, updated `paper-cited.md`.

---

## 11. Final delivery

**Goal:** ship the paper.

**Procedure:**

1. Read `references/publication-checklist.md`.
2. Run through every check.
3. For any unchecked item, add to a `Known gaps` block at the end of the
   paper.
4. Output the final paper as `paper-final.md` (and as `.tex` / `.docx` /
   `.pdf` if the user requested and tooling is available).
5. Output an `index.md` summarizing the artifacts produced:
   - `paper-spec.md`
   - `outline.md`
   - `bibliography.yaml`
   - `methodology.md`
   - `analysis/` directory
   - `figures-plan.md` and `figures/`
   - `sections/`
   - `paper-draft.md`, `paper-cited.md`, `paper-final.md`
   - `validation-report.md`, `review-report.md`
   - `Known gaps` block (if any).

---

## 12. Multi-agent execution (optional)

If the runtime supports parallel sub-agents, the orchestrator can dispatch:

- **Researcher agent** → §3 Literature review.
- **Methodologist agent** → §4 Methodology.
- **Analyst agent** → §5 Data analysis.
- **Visualizer agent** → §6 Visualization.
- **Writer agent** → §7 Drafting (one per section).
- **Citation agent** → §8 Citation pass.
- **Validator agent** → §9 Validation pass.
- **Reviewer agents (×3)** → §10 Review pass.

The orchestrator gathers the outputs and reconciles. Otherwise execute
sequentially as above.

---

## 13. Memory and long-context strategy

For papers over ~10,000 words:

1. **Persist every artifact to disk** (`paper-spec.md`, `outline.md`,
   `sections/*.md`, etc.) before moving to the next step.
2. **Read only what's needed.** In §7 Drafting, when writing §6 Results,
   load only `outline.md`, `methodology.md`, `analysis/findings.md`, and
   the previous section's draft — not the whole paper.
3. **Cross-section consistency** is enforced by:
   - The skeleton in `outline.md` (referenced when writing each section).
   - A final consistency pass (read the whole paper top-to-bottom once).
4. If context pressure is severe, summarize each completed section to a
   200-word abstract and load only the abstract during cross-section work.

---

## 14. Failure handling

- **User abandons mid-flow.** Persist whatever is on disk; offer to resume.
- **Web search returns nothing.** Mark as `[UNVERIFIED — offline]`, proceed
  with model-known citations.
- **Python missing.** Switch all charts to Mermaid / Markdown tables; never
  drop figures silently.
- **Dataset corrupted.** Stop, ask the user, or generate synthetic data
  clearly labeled.
- **Methodology unclear.** Default to the most defensible blueprint and
  surface the choice in `Known gaps`.
- **Out-of-scope request.** Narrow to a focused paper; list dropped
  sub-topics in Future Work.

---

## 15. Output contract reminder

A paper is **not done** until:

- Every section in the chosen template is present.
- Every figure / table referenced in text exists.
- Every in-text citation has a matching reference.
- The publication checklist is run, and any unchecked items are surfaced
  in `Known gaps`.
- A plain-English summary is present.
- A reproducibility statement is present.
- Limitations and future work sections are present.

If any of these is false, the paper is a draft, not a deliverable. Say so.
