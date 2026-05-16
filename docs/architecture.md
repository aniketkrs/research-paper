# Architecture

The system architecture of `research-paper` v2.0, intended for
contributors and integrators.

---

## 1. Layered architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       USER REQUEST                              │
│  (slash command, natural-language prompt, or file attachment)    │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  L1 — ACTIVATION                                                 │
│  manifest.json (triggers) → SKILL.md (entry point)                │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  L2 — INSTRUCTIONS                                               │
│  instructions/core.md, instructions/activation.md,               │
│  instructions/multi-agent.md, instructions/voice-and-tone.md     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  L3 — ORCHESTRATION                                              │
│  orchestration/pipeline.md (master workflow)                       │
│  orchestration/routing.md (format/style/depth/mode)               │
│  orchestration/agents.md (sub-agent topology)                      │
│  orchestration/failure-handling.md (recovery matrix)               │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  L4 — WORKFLOWS                                                  │
│  workflows/full-paper.md, workflows/literature-review.md,         │
│  workflows/citation-pipeline.md, workflows/data-analysis-pipeline.md, │
│  workflows/visual-generation-pipeline.md, workflows/validation-pipeline.md │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  L5 — ENGINES + PROMPTS + TEMPLATES                              │
│                                                                   │
│  citation_engine/   visualization_engine/   methodology_engine/   │
│  prompts/           templates/               academic_formats/    │
│  style_guides/      validators/              review_pipeline/     │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  L6 — TOOLCHAINS                                                  │
│  toolchains/format_bibliography.py, toolchains/analyze_data.py,    │
│  toolchains/generate_charts.py, toolchains/validate_citations.py,  │
│  toolchains/statistical_validation.py, toolchains/extract_references.py │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  L7 — STATE                                                       │
│  Working directory: paper-spec.md, outline.md, bibliography.yaml, │
│  methodology.md, analysis/, figures/, sections/, validation/,     │
│  review/, paper-final.md, Known-gaps.md, index.md, session-state.yaml │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  L8 — QUALITY                                                     │
│  quality_control/final-gate.md, quality_control/publication-checklist.md, │
│  quality_control/known-gaps-protocol.md, rubrics/                 │
└────────────────────────────┬────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────┐
│                       DELIVERY                                   │
│      paper-final.md   |   Known-gaps.md   |   index.md             │
└─────────────────────────────────────────────────────────────────┘
```

---

## 2. Data flow

```
User request
   │
   ▼
[L1] activation
   │  → SKILL.md + manifest.json (always)
   │
   ▼
[L2] instructions
   │  → instructions/core.md (always)
   │  → instructions/activation.md (if slash command)
   │  → instructions/multi-agent.md (if --depth comprehensive)
   │  → instructions/voice-and-tone.md (during drafting)
   │
   ▼
[L3] orchestration
   │  → orchestration/routing.md → routing_decision in paper-spec.md
   │  → orchestration/pipeline.md (the 11-phase pipeline)
   │  → orchestration/agents.md (when fanning out)
   │  → orchestration/failure-handling.md (on errors)
   │
   ▼
[L4] workflows (per phase)
   │
   ▼
[L5] engines + prompts + templates (loaded by phase)
   │
   ▼
[L6] toolchains (deterministic transformations)
   │  format_bibliography.py:
   │      paper-draft.md + bibliography.yaml → paper-cited.md
   │  generate_charts.py:
   │      data + plan → figures/<id>.{png,svg}
   │  analyze_data.py:
   │      dataset → analysis/findings.md
   │  validate_citations.py:
   │      paper-cited.md → validation/citation-issues.md
   │
   ▼
[L7] state (working directory artifacts)
   │
   ▼
[L8] quality gates
   │  final-gate.md → block / pass / waive
   │  Known-gaps.md ← unresolved issues
   │
   ▼
Delivery: paper-final.md + Known-gaps.md + index.md
```

---

## 3. Core invariants

These design invariants are enforced throughout:

1. **Single source of truth.** `bibliography.yaml` is THE bibliography.
   The paper draft contains only `[cite_key]` placeholders.
2. **Determinism.** Citation formatting, validator output, and chart
   rendering are pure functions of their inputs.
3. **Idempotence.** Every step produces the same output if rerun with
   the same inputs (modulo model determinism for prose).
4. **Persist before continue.** Every meaningful artifact is on disk
   before the next phase starts.
5. **Read only what you need.** Progressive disclosure end-to-end.
6. **Surface all gaps.** Issues that can't be auto-resolved go to
   `Known-gaps.md` — never silently swallowed.

---

## 4. Extension points

| Want to add…                          | Edit                                                       |
| ------------------------------------- | ---------------------------------------------------------- |
| New paper format (e.g., LNCS)          | `templates/lncs-paper.md` + `academic_formats/lncs.md` + register in `manifest.json`, `SKILL.md §4`, `orchestration/routing.md` |
| New citation style                     | `citation_engine/styles/<style>.md` + extend `toolchains/format_bibliography.py` + `citation_engine/citation-styles.md` |
| New chart type                         | `visualization_engine/decision-engine.md` (decision tree) + `toolchains/generate_charts.py` (renderer) + `visualization_engine/chart-templates.md` (template) |
| New methodology framework              | `methodology_engine/frameworks.md` + add detector in `orchestration/routing.md` |
| New rubric dimension                   | `rubrics/<rubric>.md` (anchors + scoring) + plug into `review_pipeline/three-personas.md` |
| New validator                          | `validators/<name>.md` (rules) + corresponding `toolchains/validate_<thing>.py` (implementation) + plug into `workflows/validation-pipeline.md` |
| New sub-agent                          | `instructions/multi-agent.md` (contract) + `orchestration/agents.md` (topology) + relevant prompt in `prompts/` |
| New language / locale                  | `academic_formats/<locale>.md` (style adjustments) + extend `toolchains/format_bibliography.py` (locale options) |
| New trigger pattern                    | `manifest.json → trigger.patterns` + `orchestration/routing.md` |
| New Python dependency                   | `manifest.json → python_dependencies.recommended` + use it in the relevant `toolchains/*.py` |

See **`docs/extending.md`** for the full guide.

---

## 5. Test architecture

```
tests/
├── test-runner.js          # Lightweight Node.js runner (no deps)
├── README.md
├── fixtures/                # Inputs for tests
│   ├── small-bibliography.json
│   └── small-paper-draft.md
└── golden-outputs/          # Expected outputs for regression
    └── (filled as needed)
```

Test categories:
1. **Structure** — required files exist.
2. **Schemas** — JSON files parse and validate.
3. **Frontmatter** — SKILL.md has valid YAML frontmatter.
4. **Toolchain self-tests** — Python scripts report dependency status.
5. **Pipeline smoke test** — citation pipeline produces expected
   output against fixtures.

CI integration via GitHub Actions (`.github/workflows/test.yml` —
template in `tests/README.md`).

---

## 6. Performance characteristics

| Run type                     | Phases run            | Wall-clock estimate    | Output size   |
| ---------------------------- | --------------------- | ---------------------- | ------------- |
| `--depth quick`              | All 11, abbreviated   | 2–5 min                | 2–4 pages     |
| `--depth standard`           | All 11, full          | 5–15 min               | 5–15 pages    |
| `--depth comprehensive` (single agent) | All 11, full | 15–30 min          | 15–40 pages   |
| `--depth comprehensive` (multi-agent) | All 11, parallel writers | 8–18 min  | 15–40 pages   |
| Validation-only              | 9, 10                  | 1–3 min                | (revision report) |
| Literature review only       | 1, 2, 3, 6, 7, 8, 9, 10 | 10–25 min            | 8–30 pages    |

Times scale roughly with model speed and source count.

---

## 7. Security model

- The skill never has direct network access; web search / fetch is
  optional and only used when the runtime exposes those tools.
- Toolchain scripts read / write only inside the working directory.
- No telemetry, no phone-home, no external service calls.
- All Python code is reviewable and self-contained.
- Bibliography YAML is the only place citation metadata lives —
  there's no implicit "remember this citation" state.
- Session state (`session-state.yaml`) is local; it can be deleted
  without affecting deliverables.

---

## 8. Compatibility

| Runtime                    | Compatibility                          |
| -------------------------- | -------------------------------------- |
| Claude Code (CLI)          | Native — slash commands, filesystem tools |
| Claude Desktop              | Native — drag-and-drop install         |
| claude.ai (web)             | Native — zip upload                    |
| Anthropic API / SDK         | Programmatic — see `publishing/install.md §5` |
| OpenCode                    | Native — drop in `~/.config/opencode/skills/` |
| Aider, Cline, Cursor agents | Compatible — drop in skills folder; provide read_file / write_file |
| Custom LangGraph / LlamaIndex agents | Compatible — load SKILL.md as system prompt |
| Pure terminal (no agent)    | Use `toolchains/*.py` directly         |
