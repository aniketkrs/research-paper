# Session State Protocol

How to make a long paper-generation run **resumable** — restartable
from any crashed or interrupted state without losing work.

---

## 1. The state file

The orchestrator maintains a `session-state.yaml` in the working
directory:

```yaml
session_id: <uuid>
started_at: <ISO timestamp>
last_updated: <ISO timestamp>
paper_spec: paper-spec.md

phase_status:
  intake: complete
  plan: complete
  literature_review: complete
  methodology: complete
  data_analysis: complete
  visualization: in_progress
  drafting: pending
  citations: pending
  validation: pending
  review: pending
  delivery: pending

artifacts:
  paper_spec_md: { written: true, path: paper-spec.md }
  outline_md: { written: true, path: outline.md }
  bibliography_yaml: { written: true, path: bibliography.yaml, n_entries: 47 }
  methodology_md: { written: true, path: methodology.md }
  analysis_dir: { written: true, path: analysis/ }
  figures_plan_md: { written: true, path: figures-plan.md, n_figures: 6 }
  figures: { written: 4, total: 6 }
  sections: { written: 0, total: 9 }
  paper_draft: { written: false }
  paper_cited: { written: false }
  paper_final: { written: false }

agents_dispatched:
  - { name: researcher, status: complete, started: ..., ended: ... }
  - { name: methodologist, status: complete, started: ..., ended: ... }
  - { name: analyst, status: complete, started: ..., ended: ... }
  - { name: visualizer, status: in_progress, started: ... }

errors_encountered: []

next_step: visualizer.figure-5
```

The orchestrator updates this file after every meaningful step.

---

## 2. Resumption protocol

When the orchestrator starts in a directory with an existing
`session-state.yaml`:

1. Read the state.
2. Check that `paper-spec.md` matches the current request (no scope
   change). If different, ask the user before proceeding.
3. Find the first phase / step that is `in_progress` or the first
   `pending` after the last `complete`.
4. **Skip completed phases** — their artifacts are on disk.
5. Resume from the determined step.

This makes the workflow safe to restart at any point.

---

## 3. Idempotent steps

Every phase / step is **idempotent**:

| Step                              | Idempotent because…                                 |
| --------------------------------- | --------------------------------------------------- |
| Lit review                        | Output is `bibliography.yaml`; running again at most adds entries (deduplicated). |
| Methodology design                | Output is `methodology.md`; deterministic given same paper-spec. |
| Data analysis                     | Output is `analysis/`; re-run on same data with same seed produces same numbers. |
| Visualization                     | Output is `figures/<id>.{png,svg,mmd}`; re-run with same data produces same files. |
| Drafting                          | Output is `sections/<NN>.md`; re-run with same inputs produces same prose (modulo model determinism). |
| Citation pipeline                 | Deterministic given paper-draft.md + bibliography.yaml. |
| Validation                        | Pure function of inputs.                             |
| Review                            | Three personas; each is a pure function.             |

Re-running a step produces the same artifact (or a strict superset).

---

## 4. Crash recovery

If the orchestrator crashes mid-step:

1. The artifacts produced before the crash are on disk.
2. The artifact being produced is partial (or absent).
3. On restart:
   - The orchestrator detects the partial / missing artifact.
   - It marks that step as `in_progress → pending` and re-runs.
   - All other completed steps are skipped.

If a crash leaves the working directory inconsistent:
- The user can delete the offending step's artifact and restart.
- The orchestrator re-creates it from upstream artifacts.

---

## 5. Multi-agent state

When multi-agent fan-out is active, the state file tracks each agent:

```yaml
agents_dispatched:
  - name: writer-01-introduction
    section: 01-introduction
    status: complete
    started: 2024-05-12T10:00:00Z
    ended:   2024-05-12T10:03:42Z
    output:  sections/01-introduction.md
    word_count: 1240
  - name: writer-02-related-work
    section: 02-related-work
    status: in_progress
    started: 2024-05-12T10:00:05Z
  - name: writer-03-methodology
    section: 03-methodology
    status: complete
    ...
```

The orchestrator polls each writer; failed writers are retried per
the failure-handling protocol.

---

## 6. Cross-session state

If the user pauses mid-run and returns the next day:

1. The orchestrator opens the working directory and finds
   `session-state.yaml`.
2. It reads `paper-spec.md` to confirm scope hasn't changed.
3. It resumes from the next pending step.
4. Stale artifacts (e.g., a methodology change) are detected and
   re-run in dependency order.

---

## 7. State file maintenance

Update the state file at these checkpoints:

- After every phase boundary (completion of one, start of next).
- After every agent dispatch (multi-agent mode).
- After every artifact write (figures, sections).
- After every error (with the error captured).

This is cheap (small YAML file) and makes recovery trivial.

---

## 8. State file vs. index file

| File                  | Purpose                                          |
| --------------------- | ------------------------------------------------ |
| `session-state.yaml`   | Internal state for resume / recovery              |
| `index.md`             | User-facing summary at delivery                   |

Both exist. The state file is consumed by the orchestrator; the index
is consumed by the user.

---

## 9. Privacy / data hygiene

The state file contains paths and timestamps but no paper content. It
can safely be committed to git or shared between users without
exposing the paper itself.

If the user wants to share the working directory but not the audit
trail, they can delete `session-state.yaml`, `validation/`, `review/`,
and any backup files before sharing — `paper-final.md` and supporting
artifacts (figures, tables, bibliography) are sufficient on their own.

---

## 10. Long-term archival

After delivery, the user may archive the working directory. To make
the archive self-describing:

1. The `index.md` already lists every artifact.
2. `paper-spec.md` records the original request.
3. `methodology.md` change log records every methodology revision.
4. `Known-gaps.md` records every unresolved item.

Together these make the directory a complete, reproducible
research artifact.
