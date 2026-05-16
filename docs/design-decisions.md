# Design Decisions

The "why" behind the architecture. For contributors who want to
understand the rationale before changing things.

---

## 1. Why progressive disclosure?

**Decision:** `SKILL.md` is the only file always in the model's context.
Everything else is loaded on demand.

**Why:**
- Total skill content is ~700 KB (>100 files). Putting it all in
  context wastes tokens and crowds out the user's content.
- Modular loading lets the model be efficient: it reads only the
  files relevant to the current step.
- Adding new content doesn't blow up the context budget.

**Alternative considered:** monolithic instructions. **Rejected**
because of context cost and the need for thousand-line system prompts.

---

## 2. Why a single canonical bibliography?

**Decision:** All citation metadata lives in one `bibliography.yaml`.
The paper draft contains only `[cite_key]` placeholders.

**Why:**
- Citation style switching becomes a one-line change.
- Deduplication is centralized.
- The paper itself is shorter and more reviewable.
- The citation pipeline is a deterministic projection from the
  bibliography to the paper, making it auditable.

**Alternative considered:** inline citation metadata next to each
in-text reference. **Rejected** because it makes style switching and
deduplication painful, and because the paper text becomes cluttered.

---

## 3. Why three engines, not one?

**Decision:** Citation, visualization, and methodology each get their
own engine folder.

**Why:**
- These three concerns have distinct decision logic and distinct
  domain knowledge.
- Separating them means a venue change (citation style) doesn't
  perturb chart rendering, and vice versa.
- Each engine has a clean extension boundary (per-style file,
  per-chart-type renderer, per-methodology blueprint).

**Alternative considered:** monolithic `engine/` with everything mixed.
**Rejected** because it makes contributions harder and obscures the
architectural clarity.

---

## 4. Why explicit per-agent contracts?

**Decision:** Each sub-agent has a documented `reads`, `writes`, and
`quality_floor` contract.

**Why:**
- Without contracts, sub-agents stomp on each other or silently
  produce unusable outputs.
- Contracts make the multi-agent topology debuggable: you can trace
  exactly which agent produced which artifact.
- Contracts make parallelism safe: no two writers can write the same
  section file.

**Alternative considered:** implicit communication via shared global
context. **Rejected** because it doesn't scale and breaks under
parallelism.

---

## 5. Why the working directory IS the state?

**Decision:** Every meaningful artifact is persisted to disk; agents
communicate only through the file system.

**Why:**
- Resumability: a crash mid-run doesn't lose work.
- Auditability: every output is on disk and reviewable.
- Determinism: re-running a step produces the same artifact.
- Multi-agent coordination: no race conditions, no synchronization
  primitives needed.

**Alternative considered:** in-memory state. **Rejected** because it
loses everything on a crash and forces the orchestrator to hold the
entire state.

---

## 6. Why slash commands AND natural language?

**Decision:** Activate on both `/research` slash commands and natural
language patterns ("write a research paper on…").

**Why:**
- Slash commands are explicit and unambiguous — power users prefer them.
- Natural language is friendlier for first-time users.
- Supporting both meets users where they are.

**Alternative considered:** slash commands only. **Rejected** because
some agent runtimes don't support slash commands well.

---

## 7. Why deterministic citation pipeline?

**Decision:** `format_bibliography.py` is a pure function: same inputs
→ same output, byte for byte.

**Why:**
- Style switching produces the exact same output every time.
- Bug reports become reproducible.
- The pipeline can be hand-checked.
- It removes a class of "the model mis-formatted my citation" issues.

**Alternative considered:** model-generated citations from the
bibliography. **Rejected** because models drift, especially on long
reference lists.

---

## 8. Why graceful degradation?

**Decision:** Every toolchain script works without optional Python
dependencies, falling back to Markdown / Mermaid.

**Why:**
- Not every environment has matplotlib / pandas.
- The skill should produce a usable paper even on a fresh laptop with
  only Python stdlib.
- Failing gracefully > failing loudly.

**Alternative considered:** require Python deps as preconditions.
**Rejected** because it makes the skill brittle and frustrating in
restricted environments.

---

## 9. Why the Known-gaps protocol?

**Decision:** Every unresolved issue surfaces in `Known-gaps.md` with
severity, recommended fix, and affected artifacts.

**Why:**
- Real journal submissions fail because of small mechanical issues
  (a malformed citation, a missing affiliation, a forgotten ethics
  statement).
- Surfacing these issues turns the skill from "AI that writes
  drafts" into "AI that helps the user ship papers".
- A single file (`Known-gaps.md`) is enough to convert "draft" into
  "submission-ready" with focused human work.

**Alternative considered:** silent failure. **Rejected** as
unprofessional and dangerous.

---

## 10. Why no LaTeX-first output?

**Decision:** Default output is Markdown; LaTeX export is via Pandoc.

**Why:**
- Markdown is portable across renderers (GitHub, GitLab, Obsidian,
  VS Code, Pandoc).
- LaTeX is venue-specific; the model would have to choose a class
  file (`acmart`, `IEEEtran`, `lncs`, etc.) up front.
- Markdown + Pandoc decouples authoring from typesetting.

**Alternative considered:** generate LaTeX directly. **Rejected**
because of the brittleness of LaTeX class compatibility and the
proliferation of venue-specific style files.

---

## 11. Why three reviewer personas, not one?

**Decision:** Methodologist + Domain expert + Reader, each independent.

**Why:**
- Real peer review is multi-reviewer.
- Different reviewers catch different issues: methodologists find
  validity flaws; domain experts find missing literature; readers
  find clarity issues.
- Three independent perspectives produce more useful revision
  requests than one super-reviewer.

**Alternative considered:** single super-reviewer. **Rejected**
because it converges on a single style of feedback and misses
orthogonal issues.

---

## 12. Why a final gate, not just a checklist?

**Decision:** `quality_control/final-gate.md` is a hard gate that
blocks delivery on serious problems.

**Why:**
- Without a gate, the model "delivers" papers that don't actually
  meet the contract.
- A hard gate forces revision when revision is needed.
- The gate-vs-checklist distinction:
  - Checklist: a list of things to remember.
  - Gate: a precondition for delivery.

**Alternative considered:** soft checklist that only warns.
**Rejected** because it would let mediocre papers slip through.

---

## 13. Why a separate `Known-gaps.md` for waivers?

**Decision:** When the user explicitly waives a gap, the waiver is
recorded in `Known-gaps.md` with timestamp and rationale.

**Why:**
- Waivers should be auditable.
- The waiver itself becomes part of the deliverable history.
- A user who later asks "did I really waive this?" can check.

**Alternative considered:** delete waived items. **Rejected** because
it loses the audit trail.

---

## 14. Why `kebab-case.md` and `snake_case.py`?

**Decision:** Markdown files use kebab-case; Python files use
snake_case.

**Why:**
- Kebab-case is friendlier for URLs and matches typical Markdown
  conventions (GitHub, MkDocs).
- Snake_case is the Python convention.
- Keeping them distinct makes the file type immediately recognizable.

**Alternative considered:** uniform snake_case. **Rejected** because
GitHub URLs with underscores look ugly and many conventions favor
kebab-case for content files.

---

## 15. Why npm packaging?

**Decision:** Ship as `@aniketkrs/research-paper` on npm with a
`bin/install.js` script.

**Why:**
- `npx` is the most universally available "run-this-once" tool across
  developer environments.
- Installing a skill should be one command.
- npm versioning gives users a way to pin and roll back.

**Alternative considered:** GitHub release zip only. **Rejected**
because manual install is friction; `npx` is friction-free.

---

## 16. Why the multi-agent topology is optional?

**Decision:** Multi-agent fan-out runs only when `--depth comprehensive`
AND `agent-spawn` is available; otherwise the orchestrator runs
sequentially.

**Why:**
- Most papers don't need parallelism.
- Sequential execution is simpler and more predictable.
- Parallel execution should be an optimization, not a requirement.
- This keeps the skill compatible with runtimes that don't support
  agent dispatch.

**Alternative considered:** always parallel. **Rejected** because
it would break runtimes without `agent-spawn`.

---

## 17. Why the dual register (technical + plain-English)?

**Decision:** Every paper carries both a rigorous technical body and
a plain-English summary.

**Why:**
- Academic rigor and accessibility aren't mutually exclusive.
- Funders, policymakers, and adjacent-field readers benefit from a
  plain-English version.
- Many journals (Nature) now require it explicitly.

**Alternative considered:** technical only. **Rejected** because it
limits the paper's reach and is increasingly out-of-step with
publishing norms.

---

## 18. Why explicit failure-handling?

**Decision:** `orchestration/failure-handling.md` documents recovery
for every phase.

**Why:**
- Real systems fail; documenting failures is a sign of maturity.
- Most failures are recoverable (retry, fallback) — the matrix
  encodes those recoveries.
- Documenting failure modes also documents the system's edge cases,
  which is useful for users.

**Alternative considered:** generic "retry on failure". **Rejected**
because it loses the per-phase nuance (a citation failure is very
different from a chart failure).

---

## 19. Why is the skill not a chatbot?

**Decision:** The skill produces deliverables (papers, reviews,
analyses), not conversational responses.

**Why:**
- Research papers are artifacts, not conversations.
- The user wants the deliverable; the skill should optimize for
  that, not for chat.
- Conversational ambiguity hurts research outputs.

**Alternative considered:** chatty step-by-step interaction.
**Rejected** because most users want the result, not the journey.

---

## 20. Why bother with all this rigor?

**The user's quality bar:** "an enterprise AI research operating
system… professional academic tooling ecosystem."

The combined rigor of:
- Progressive disclosure (manageable context)
- Modular engines (clean extension)
- Per-agent contracts (safe parallelism)
- Working-directory state (resumability)
- Deterministic toolchains (auditable outputs)
- Quality gates (no junk delivered)
- Known-gaps protocol (no silent failures)
- Tests + npm packaging (reliability + distribution)

…is what distinguishes a real production system from a demo. Each of
these decisions carries its own weight. Together, they make the
skill ready to ship into production environments where someone's
actual thesis or actual whitepaper depends on it.
