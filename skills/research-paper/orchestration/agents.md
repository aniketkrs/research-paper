# Sub-Agent Topology

This is a one-page summary of the multi-agent topology described in
detail in `instructions/multi-agent.md`. Read this when you need to
**dispatch** sub-agents (multi-agent runtime) or simulate them
sequentially (single-orchestrator runtime).

---

## Overview

```
                Orchestrator (the main agent)
                          │
   ┌──────┬───────┬──────┼──────┬──────┬──────┐
   ▼      ▼       ▼      ▼      ▼      ▼      ▼
Researcher Methodologist Analyst Visualizer Writer×N Citator Validator
                          │
                          ▼
                  Reviewer (Methodologist + Domain + Reader)
                          │
                          ▼
                     Publisher (orchestrator role)
```

---

## When to fan out vs. run sequentially

| Condition                                        | Topology                       |
| ------------------------------------------------ | ------------------------------ |
| `--depth quick`                                    | Sequential single-orchestrator |
| `--depth standard`                                  | Sequential single-orchestrator |
| `--depth comprehensive` AND `agent-spawn` available | Multi-agent fan-out          |
| Validation-only intent                            | Direct to Validator + Reviewer |

In **multi-agent** mode, the Writer agents fan out (one per section, in
parallel). All other agents are sequential because their outputs feed
each other.

---

## Per-agent contracts (summary)

| Agent           | Reads (key)                                        | Writes (key)                                |
| --------------- | -------------------------------------------------- | ------------------------------------------- |
| Researcher       | `prompts/literature-search.md`                       | `bibliography.yaml`, `lit-themes.md`         |
| Methodologist    | `prompts/methodology-design.md`, `methodology_engine/*` | `methodology.md`                          |
| Analyst          | `prompts/data-analysis.md`, dataset                | `analysis/findings.md`, `analysis/figures/` |
| Visualizer       | `outline.md`, `analysis/findings.md`, `visualization_engine/*` | `figures-plan.md`, `figures/`     |
| Writer (×N)       | `outline.md`, `templates/<format>.md`, prior section + bibliography | `sections/<NN>-<name>.md`           |
| Citator          | `paper-draft.md`, `bibliography.yaml`               | `paper-cited.md`, `citation-report.md`       |
| Validator        | `paper-cited.md`, `validators/*`                    | `validation/validation-report.md`            |
| Reviewer (×3)    | `paper-cited.md`, `rubrics/*`                       | `review/<persona>-review.md`                  |
| Publisher        | reviewed paper, `quality_control/*`                  | `paper-final.md`, `Known-gaps.md`, `index.md` |

Full contracts: `instructions/multi-agent.md §3`.

---

## Coordination rules

1. Agents communicate **only through the working directory**.
2. Agents read only files in their `reads` contract.
3. Agents write only files in their `writes` contract.
4. Agents persist artifacts to disk **before reporting completion**.
5. The Orchestrator gathers, reconciles, and dispatches — no agent
   directly invokes another.

This is the research-lab pattern: each researcher produces a
deliverable; the lab head integrates them.

---

## Failure handling

If an agent fails:
1. Capture state in `validation/errors.md`.
2. Retry once with same inputs.
3. Retry once with reduced scope.
4. Fall back to single-orchestrator execution of that phase.
5. Surface in `Known-gaps.md` with a recommended fix.

See `orchestration/failure-handling.md` for the per-phase matrix.

---

## Implementation details

For runtimes WITHOUT `agent-spawn` (single-orchestrator mode):
- The orchestrator simulates each agent by loading the relevant prompts
  and running the steps inline.
- The contract is preserved: same inputs read, same outputs written,
  same quality floor enforced.

For runtimes WITH `agent-spawn`:
- The orchestrator uses the runtime's spawn primitive to dispatch each
  sub-agent with its scoped prompts and tool access.
- The orchestrator polls / waits on completion, then proceeds.

The skill ships as a **declarative description**. The runtime is
responsible for the actual dispatch mechanism.
