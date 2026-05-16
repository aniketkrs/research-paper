# Extending the Skill

How to add new venues, citation styles, chart types, methodologies,
sub-agents, or languages — without breaking existing functionality.

---

## 1. Add a new paper format / venue

Suppose you want to add **LNCS** (Lecture Notes in Computer Science).

### Step 1: Create the template

Create `templates/lncs-paper.md` modeled on `templates/ieee-paper.md`,
adjusting:
- Section ordering per LNCS guidelines.
- Author block format.
- LNCS-specific abstract length (200 words).

### Step 2: Document venue conventions

Create `academic_formats/lncs.md` with:
- Section ordering
- Citation style rules (LNCS uses Springer numeric)
- Figure / table caption conventions
- Word and page limits

### Step 3: Register the trigger

Edit `manifest.json`:

```json
{
  "supported_formats": [..., "lncs"],
  "trigger": {
    "patterns": [..., "format as LNCS", "Springer LNCS"]
  }
}
```

### Step 4: Update routing

Edit `orchestration/routing.md`:

```
| LNCS / Springer / CS-conference (LNCS) | templates/lncs-paper.md |
```

### Step 5: Update SKILL.md

Edit `SKILL.md §4 Format selection` to include LNCS.

### Step 6: Add an example (optional but recommended)

Drop a short LNCS-style example in `examples/sample-paper-lncs.md`.

### Step 7: Test

Run:
```
/research "Test LNCS format" --format lncs --depth quick
```

---

## 2. Add a new citation style

Suppose you want to add **Vancouver** (numbered, biomedical).

### Step 1: Add per-style file

Create `citation_engine/styles/vancouver.md` documenting:
- In-text citation format (e.g., `(1)`, `(1,2)`)
- Reference list format with examples per type
- Disambiguation rules

### Step 2: Add to citation pipeline

Edit `citation_engine/citation-styles.md` to include a Vancouver section.

### Step 3: Implement in toolchain

In `toolchains/format_bibliography.py`:
- Add `vancouver` to the `--style` choices.
- Add an `in_text_vancouver()` formatter.
- Add a `ref_vancouver()` formatter for each entry type.

### Step 4: Test

```bash
python toolchains/format_bibliography.py \
    --bib examples/bibliography.example.yaml \
    --paper examples/sample-paper-arxiv.md \
    --style vancouver \
    --out /tmp/test.md
```

---

## 3. Add a new chart type

Suppose you want to add **streamgraph**.

### Step 1: Document the decision

Edit `visualization_engine/decision-engine.md` decision tree:

```
IF content_type == "composition_over_time" AND data_points >= 10:
    RETURN true, "streamgraph"
```

### Step 2: Add a chart template

Add a Python template to `visualization_engine/chart-templates.md`.

### Step 3: Implement renderer

In `toolchains/generate_charts.py`:
- Add `streamgraph` to `CHARTS_PYTHON`.
- Implement `chart_streamgraph(data, args, plt, sns, np, pd)`.

### Step 4: Add caption template

In `visualization_engine/caption-generator.md`, add a streamgraph
caption template.

### Step 5: Test

```bash
python toolchains/generate_charts.py \
    --type streamgraph --input data.csv \
    --x year --y value --hue category \
    --out figures/test
```

---

## 4. Add a new methodology framework

Suppose you want to add **Action Research**.

### Step 1: Add to the framework decision tree

Edit `methodology_engine/frameworks.md`:

```
├── EVALUATE (assess effectiveness)
│  ├── Program/intervention → Program Evaluation
│  └── Practice / community-engaged → Action Research   ← NEW
```

### Step 2: Add a blueprint

In `methodology_engine/methodology-guide.md`, add an "Action Research
blueprint" section with required elements (cycles, participants,
reflection, dissemination).

### Step 3: Add a routing detector

Edit `orchestration/routing.md` to detect intent ("action research",
"participatory research") and route to the new blueprint.

### Step 4: Test

```
/research "Action research on agile adoption in a manufacturing team"
```

---

## 5. Add a new sub-agent

Suppose you want to add a **Translator** sub-agent for multilingual
papers.

### Step 1: Define the contract

In `instructions/multi-agent.md` add:

```yaml
agent: translator
reads:
  required:
    - paper-final.md (English)
    - language-target.md
writes:
  required:
    - paper-final-<lang>.md
quality_floor:
  - terminology consistency
  - cite_keys preserved exactly
  - figure / table captions translated
  - reference list NOT translated (only abstract / body / methods)
```

### Step 2: Add to topology

Edit `orchestration/agents.md` topology diagram.

### Step 3: Add to pipeline

Edit `orchestration/pipeline.md` to add a "Phase 12: Translation
(optional)" after delivery.

### Step 4: Add a prompt

Create `prompts/translation.md` with the translation protocol.

### Step 5: Update manifest

Add `multi-language-output` to capabilities and document the
`--target-language` option.

---

## 6. Add a new language / locale

Suppose you want en-CA (Canadian English).

### Step 1: Add locale file

Create `academic_formats/en-CA.md` with locale-specific rules
(date format, spelling preferences, comma usage).

### Step 2: Update toolchain

In `toolchains/format_bibliography.py`, add `en-CA` to `--locale`
choices and apply the relevant adjustments (e.g., "edn." vs. "ed.").

### Step 3: Update style guides

Note any en-CA conventions in `style_guides/writing-style-guide.md`.

---

## 7. Add a new trigger pattern

Useful when your audience uses domain-specific phrasing
("write a clinical case report on…").

### Step 1: Add the pattern

Edit `manifest.json`:

```json
"trigger": {
  "patterns": [..., "clinical case report on", "case report of"]
}
```

### Step 2: Route it

Edit `orchestration/routing.md` to recognize the new intent and
pick the right template (probably a custom `templates/case-report.md`
you've also added).

---

## 8. Add a new Python toolchain

Useful when you want a new validator or analysis script.

### Step 1: Create the script

Drop `toolchains/<your_script>.py` with:
- A clear CLI (argparse).
- A `--self-test` flag.
- Graceful degradation if optional deps are missing.
- UTF-8 BOM tolerance (`encoding="utf-8-sig"` when reading).

### Step 2: Register

- Add to `manifest.json → files.toolchains`.
- Add to `tests/test-runner.js` (a test that runs `--self-test`).
- Document in `toolchains/README.md` (if it exists; otherwise inline
  in the script's docstring).

### Step 3: Hook into a workflow

Edit the relevant `workflows/<phase>.md` to mention the new tool.

---

## 9. Add a new rubric

Suppose you want a "narrative quality" rubric.

### Step 1: Create the rubric

Create `rubrics/narrative-quality.md` with 5–10 anchored dimensions.

### Step 2: Hook into the review pipeline

Edit `review_pipeline/three-personas.md` to give the Reader persona
a new dimension to score.

### Step 3: Hook into the final gate

Edit `quality_control/final-gate.md` if narrative quality should
be a hard gate (likely it shouldn't — it's subjective).

---

## 10. Add a new schema

For a new structured artifact (e.g., a per-section metadata file):

### Step 1: Create the JSON Schema

Create `schemas/<artifact>-schema.json` per JSON Schema 2020-12.

### Step 2: Validate in tests

Add a test in `tests/test-runner.js` that loads the schema and
confirms it's valid.

### Step 3: Use it

The orchestrator can validate any artifact against its schema before
declaring the artifact "complete".

---

## 11. Tracking your changes

For any change above:

1. Bump `manifest.json → version` (semver).
2. Add a `## [version] — date` block to `CHANGELOG.md`.
3. Run `node tests/test-runner.js` and ensure it passes.
4. Update `README.md` if the change is user-facing.
5. Open a PR with the change and a short rationale.

---

## 12. What NOT to do

- **Don't** add files outside the documented folders. The folder
  structure IS the architecture.
- **Don't** mix concerns. Citation logic stays in `citation_engine/`,
  not in `prompts/`.
- **Don't** hardcode values that should be configurable. Use
  `manifest.json → configuration` for tunable parameters.
- **Don't** invent new file naming conventions. Stick to
  `kebab-case.md` and `snake_case.py`.
- **Don't** silently change existing behavior. Document, version,
  and changelog every change.
- **Don't** break progressive disclosure. New content goes in a new
  module, not appended to `SKILL.md`.
