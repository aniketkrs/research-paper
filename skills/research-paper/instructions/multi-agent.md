# Multi-Agent Orchestration

For comprehensive papers (`--depth comprehensive`, > 8,000 words, or
high parallelism), the skill operates as a **coordinated agent
ensemble**. This document defines the topology, contracts, and
synchronization rules.

---

## 1. Topology

```
                        ┌─────────────────────┐
                        │     ORCHESTRATOR    │
                        │ (you, the main agent) │
                        └──────────┬──────────┘
                                   │
        ┌──────────┬──────────┬────┴─────┬──────────┬──────────┐
        ▼          ▼          ▼          ▼          ▼          ▼
  ┌──────────┐┌──────────┐┌─────────┐┌─────────┐┌─────────┐┌─────────┐
  │Researcher││Methodol- ││ Analyst ││Visualizer│ Writer  │ Citator │
  │          ││  ogist   ││         ││         ││ (×N)    │         │
  └────┬─────┘└────┬─────┘└────┬────┘└────┬────┘└────┬────┘└────┬────┘
       │           │           │          │          │          │
       └───────────┴───────────┴──────────┴──────────┴──────────┘
                                   │
                                   ▼
                        ┌─────────────────────┐
                        │      Validator      │
                        └──────────┬──────────┘
                                   │
                                   ▼
                  ┌────────────────┴───────────────┐
                  ▼                                ▼
        ┌───────────────────┐           ┌───────────────────┐
        │ Reviewer (×3)     │           │ Publisher         │
        │ Methodologist /    │           │ (final assembly +  │
        │ Domain expert /    │           │  publication      │
        │ Reader             │           │  checklist)       │
        └───────────────────┘           └───────────────────┘
```

The Orchestrator owns the **shared state** (the working directory) and
fans work out / collects results. Sub-agents are stateless beyond the
working directory.

---

## 2. Agent contracts

Every agent has the same contract:

```yaml
agent: <role>
inputs:
  required: [<files the agent must read>]
  optional: [<files it may read>]
outputs:
  required: [<files the agent must write>]
  may_write: [<files it can write>]
must_not:
  - read files outside its inputs
  - write files outside its outputs
  - block on other agents (use the working dir to communicate)
must:
  - persist all artifacts to disk
  - report completion explicitly
  - flag known gaps
  - never fabricate data / citations / numbers
```

This separation is what enables parallelism without races.

---

## 3. Per-agent contracts

### 3.1 Researcher

Responsible for: literature search, source quality scoring, theme
extraction.

```yaml
agent: researcher
reads:
  required:
    - paper-spec.md
    - prompts/literature-search.md
    - workflows/literature-review-guide.md
    - citation_engine/source-evaluation.md
    - citation_engine/credibility-scoring.md
writes:
  required:
    - bibliography.yaml
    - lit-themes.md
  may_write:
    - lit-search-plan.md
    - lit-screening-log.md
    - prisma-numbers.md
quality_floor:
  - >= --sources entries scored 5+
  - all entries follow schemas/citation-schema.json
  - no fabricated DOIs
```

### 3.2 Methodologist

Responsible for: research-question framing, study design, validity
threats, reproducibility.

```yaml
agent: methodologist
reads:
  required:
    - paper-spec.md
    - prompts/methodology-design.md
    - methodology_engine/frameworks.md
    - methodology_engine/sampling.md
    - methodology_engine/statistical-tests.md
    - methodology_engine/methodology-guide.md
writes:
  required:
    - methodology.md
quality_floor:
  - method matches research question
  - sampling justified
  - power analysis (or reasoning) present
  - validity threats addressed
  - reproducibility statement filled
```

### 3.3 Analyst

Responsible for: data ingestion, EDA, statistical tests, robustness
checks.

```yaml
agent: analyst
reads:
  required:
    - paper-spec.md
    - methodology.md
    - prompts/data-analysis.md
    - workflows/data-analysis-pipeline.md
    - methodology_engine/statistical-methods.md
optional:
    - <user-supplied dataset>
writes:
  required:
    - analysis/data-dictionary.md
    - analysis/findings.md
    - analysis/hypothesis-tests.md
  may_write:
    - analysis/missing-data.md
    - analysis/univariate-summary.md
    - analysis/bivariate-summary.md
    - analysis/figures/*.png
    - analysis/tables/*.csv
quality_floor:
  - assumption checks documented
  - effect sizes + 95% CIs reported
  - multiple-comparison correction applied
  - robustness checks performed
```

### 3.4 Visualizer

Responsible for: planning, generating, and captioning every figure / table.

```yaml
agent: visualizer
reads:
  required:
    - outline.md
    - methodology.md
    - analysis/findings.md
    - prompts/visualization-planning.md
    - visualization_engine/decision-engine.md
    - visualization_engine/visualization-guide.md
    - visualization_engine/caption-generator.md
writes:
  required:
    - figures-plan.md
    - figures/<id>.{png,svg,mmd}
    - tables/<id>.csv (where applicable)
quality_floor:
  - every section needing a figure has one
  - colorblind-safe palette
  - units in axis labels
  - interpretive caption (not just descriptive)
  - every figure referenced in text BEFORE it appears
```

### 3.5 Writer (×N)

Responsible for prose. Multiple writers can run in parallel — each owns
ONE section.

```yaml
agent: writer
reads:
  required:
    - outline.md
    - templates/<format>.md
    - bibliography.yaml
    - methodology.md
    - analysis/findings.md (if applicable)
    - figures-plan.md
    - prompts/writing-prompts.md
    - style_guides/writing-style-guide.md
    - style_guides/academic-tone.md
    - <previous adjacent sections>
writes:
  required:
    - sections/<NN>-<name>.md
quality_floor:
  - every claim has [cite_key] or [CITATION NEEDED] flag
  - every figure / table referenced before appearing
  - no AI-cliché phrases
  - sentence-length variety
  - acronyms defined on first use
section_assignments:
  - 01: introduction
  - 02: related-work or literature-review
  - 03: methodology
  - 04: results / findings
  - 05: discussion
  - 06: limitations
  - 07: future-work
  - 08: conclusion
```

### 3.6 Citator

Responsible for converting `[cite_key]` placeholders to formatted
citations and producing the reference list.

```yaml
agent: citator
reads:
  required:
    - paper-draft.md
    - bibliography.yaml
    - citation_engine/citation-styles.md
    - workflows/citation-pipeline.md
writes:
  required:
    - paper-cited.md
    - citation-report.md
quality_floor:
  - 0 missing keys
  - 0 incomplete entries
  - 0 mixed-style citations
  - <= configured orphan count
tooling:
  - toolchains/format_bibliography.py --style <style> (deterministic)
```

### 3.7 Validator

Responsible for mechanical correctness (citations, structure, stats,
visuals, AI-clichés).

```yaml
agent: validator
reads:
  required:
    - paper-cited.md
    - bibliography.yaml
    - figures-plan.md
    - analysis/ (if applicable)
    - validators/*.md
writes:
  required:
    - validation/citation-issues.md
    - validation/statistical-issues.md
    - validation/visual-issues.md
    - validation/structural-issues.md
    - validation/style-issues.md
    - validation/validation-report.md
behavior:
  - High-severity issues halt the pipeline
  - Medium / low go to Known gaps
tooling:
  - toolchains/validate_citations.py
  - toolchains/statistical_validation.py
  - toolchains/extract_references.py
```

### 3.8 Reviewer (×3)

Three reviewer personas, run independently:

```yaml
agent: reviewer
personas:
  - methodologist  (validity, stats, reproducibility)
  - domain-expert  (framing, novelty, prior work)
  - reader         (clarity, narrative, accessibility)
reads:
  required:
    - paper-cited.md
    - validation/validation-report.md
    - rubrics/academic-quality.md
    - rubrics/methodology-rigor.md
    - rubrics/citation-quality.md
    - rubrics/visual-quality.md
    - prompts/review-prompts.md
writes:
  required:
    - review/<persona>-review.md
quality_floor:
  - 5 strengths + 5 weaknesses per persona
  - 3-5 specific revision requests with severity / effort / impact
  - per-dimension scores (1-5) with evidence
```

The orchestrator aggregates all three into `review/review-report.md`,
applies auto-fixable revisions, and reruns the validator before
declaring the paper done.

### 3.9 Publisher (orchestrator role at the end)

```yaml
agent: publisher (orchestrator)
reads:
  required:
    - paper-cited.md (post-revision)
    - review/review-report.md
    - quality_control/publication-checklist.md
writes:
  required:
    - paper-final.md
    - Known-gaps.md
    - index.md
quality_floor:
  - all publication-checklist items either checked or flagged
  - paper meets manifest.json quality_gates
```

---

## 4. Synchronization

The orchestrator runs phases sequentially **except** for the writer
fan-out. Specifically:

- Phases 1–6 (intake → visualization) are sequential.
- Phase 7 (drafting) can fan out: one Writer agent per section, parallel.
- Phases 8–11 (citations → validation → review → ship) are sequential.

For runtimes that don't support parallel agent dispatch, fall back to a
sequential single-orchestrator loop. The contracts above still hold —
they just execute serially.

---

## 5. Communication protocol

Agents do **not** call each other directly. They communicate through
the working directory (the file system). This means:

- Agents ARE allowed to write files listed in their `writes` contract.
- Agents are NOT allowed to read files outside their `reads` contract.
- The orchestrator is the only agent that reads the entire working
  directory.
- Every agent's output is a verifiable, persisted artifact.

This is the **research-lab pattern**: each researcher produces a
deliverable, the lab head integrates them. It is also what makes the
system robust to retries, restarts, and partial failures.

---

## 6. Failure handling

If an agent fails (timeout, error, low-quality output):

1. The orchestrator captures the failure in `Known-gaps.md`.
2. The agent is **retried at most twice** with the same inputs.
3. If still failing, the orchestrator falls back to a synchronous
   single-agent execution of that phase.
4. If even that fails, the issue is surfaced to the user in
   `Known-gaps.md` with a recommended fix.

See `orchestration/failure-handling.md` for the full matrix.

---

## 7. When NOT to dispatch sub-agents

Use single-orchestrator (no sub-agent fan-out) when:

- Paper is < 8,000 words / `--depth quick` or `standard`.
- Runtime doesn't support `agent-spawn` tools.
- Cost / latency is more important than throughput.
- The user explicitly asked for a single-pass run.

The contracts in §3 still apply — they're enforced as the orchestrator
loops through phases. The only thing changing is the parallelism.

---

## 8. Testing the topology

Run a smoke-test of the multi-agent pipeline:

```
/research "smoke test of multi-agent dispatch" --depth quick
```

Expected: a 2-page paper with 8 citations, 1 figure, all artifacts
persisted, validator report clean.
