# Long-Context Strategy

Strategy for producing papers that exceed the model's working context
window. The TL;DR: **persist every artifact to disk, then read only
what you need for the current step**.

---

## 1. When to switch to long-context mode

Switch when any of these is true:

- Estimated paper length > 10,000 words.
- Estimated total artifacts (paper + bibliography + analysis + sections)
  > 60% of the model's context window.
- `--depth comprehensive` was requested.
- The paper is a thesis chapter or survey paper.
- Multi-agent fan-out is active (each agent reads only its scoped slice).

The orchestrator decides this in the routing phase
(`orchestration/routing.md §6`).

---

## 2. The four invariants

Long-context discipline rests on four invariants:

1. **The working directory is the source of truth.** Every artifact
   that took non-trivial work to produce lives on disk, not in working
   memory.
2. **Never reload the whole paper.** When working on §6 Results, you
   should hold the outline + the methodology + the analysis findings +
   §5 in memory. Not §1, §2, §3, §4.
3. **Cross-section consistency is a final pass.** Don't try to maintain
   it section by section while drafting. Do a single cover-to-cover
   read at the very end.
4. **Idempotent steps.** Every workflow step should be runnable again
   without changing the output. This means a crashed run can be
   resumed.

---

## 3. The artifact graph

```
paper-spec.md           ← the contract (always kept in memory)
   │
   ▼
outline.md              ← the structure (always kept in memory)
   │
   ▼
bibliography.yaml       ← the canonical citation DB (load on demand)
   │
   ▼
methodology.md          ← static after methodology phase
   │
   ▼
analysis/               ← static after analysis phase
   findings.md          ← summary the writer reads
   data-dictionary.md   ← rarely read after analysis phase
   figures/             ← referenced by id, not loaded as text
   tables/              ← same
   │
   ▼
figures-plan.md          ← the figure manifest (loaded during drafting)
   │
   ▼
sections/                 ← per-section drafts (load only the relevant ones)
   01-introduction.md
   02-related-work.md
   03-methodology.md
   ...
   │
   ▼
paper-draft.md            ← assembled from sections (read-once)
   │
   ▼
paper-cited.md            ← citation pipeline output (read-once)
   │
   ▼
validation/               ← reports
   validation-report.md
   ...
   │
   ▼
review/                   ← reports
   review-report.md
   ...
   │
   ▼
paper-final.md            ← the deliverable
Known-gaps.md
index.md
```

Files in `analysis/figures/`, `analysis/tables/`, and the raw section
drafts are **referenced by path** in later steps, not by content.

---

## 4. Per-step working memory

| Step                       | Hold in working memory                                            |
| -------------------------- | ----------------------------------------------------------------- |
| Intake                      | request, defaults                                                  |
| Plan                        | `paper-spec.md`, `outline.md` (just-built)                         |
| Lit review                  | `paper-spec.md`, current theme, bibliography (write-only)          |
| Methodology                  | `paper-spec.md`, `outline.md` excerpt, `methodology.md` (just-built) |
| Data analysis                | `methodology.md`, dataset, current statistical test                |
| Visualization                | `outline.md`, `analysis/findings.md`, current figure plan          |
| Drafting (per section)       | `outline.md`, current `templates/<format>.md` slot, prior adjacent section, `bibliography.yaml` (relevant entries) |
| Citation pass                | `paper-draft.md`, `bibliography.yaml`                              |
| Validation                   | `paper-cited.md`, `validators/<each>.md` one at a time              |
| Review                       | `paper-cited.md`, `rubrics/<one>.md` one at a time                  |
| Final assembly               | sections list, validation summary, review summary                  |

If working memory pressure is severe, summarize each completed section
to a 100–200 word abstract and load only the abstract during cross-
section work.

---

## 5. Section-by-section streaming

When drafting in long-context mode:

1. Open `templates/<format>.md` once at the start of drafting.
2. For each section in template order:
   1. Read **only** the slot for this section from the template.
   2. Read the previous adjacent section from `sections/<NN-1>-...md`
      (for transition continuity).
   3. Load relevant bibliography entries (filter to the cite_keys
      planned for this section in `outline.md`).
   4. Draft the section.
   5. Write to `sections/<NN>-<name>.md`.
   6. **Discard the section from working memory** before starting the
      next one.

Never hold three full sections in memory at once.

---

## 6. Citation memory

The bibliography is the highest-leakage artifact in long-context work
because every section references it. Strategy:

- Keep `bibliography.yaml` on disk as the source of truth.
- When entering a new section, load only the entries whose `id` is
  used in that section (per `outline.md`).
- The citation pipeline (running once at the end on the full
  `paper-draft.md`) is the only place where the entire bibliography
  is loaded.

See `memory/citation-memory.md` for the protocol.

---

## 7. Final consistency pass

After all sections are drafted and citations formatted:

1. Open `paper-cited.md` once, top to bottom, in one pass.
2. Check:
   - Title / abstract / conclusion claim the same headline finding.
   - Numbers in the abstract match numbers in the results.
   - Section transitions are smooth.
   - No leftover `<<...>>` template placeholders.
   - No leftover `[CITATION NEEDED]` (or, if any remain, they're in
     `Known-gaps.md`).
   - Acronyms are defined on first use in each major section.
   - Plain-English summary doesn't contradict the technical body.
3. Apply fixes inline.

This is the **only** time the entire paper is held in memory at once.

---

## 8. Resumability

If the run crashes or is interrupted:

1. Restart the orchestrator.
2. The orchestrator scans the working directory.
3. Steps with their output already on disk are **skipped**.
4. Steps with partial output (e.g., a `[PARTIAL]` marker) are re-run.
5. The first incomplete step becomes the resumption point.

This is what makes the workflow safe to restart at any point.

---

## 9. Multi-agent + long-context

When both modes are active:
- Each writer agent gets one section's worth of context.
- The orchestrator never holds the full paper.
- The validator and reviewers each get the full `paper-cited.md` once
  (this is the one place full-paper context is necessary).
- For papers that exceed the validator/reviewer context, split into
  two halves and run twice with explicit instructions about what part
  to focus on.

---

## 10. Diagnostics

If the model starts hallucinating or losing coherence:

- Reload `paper-spec.md` and `outline.md` to re-anchor.
- Discard any in-memory section that isn't the current one.
- Re-read the current section's previous adjacent section.
- Reduce model temperature for the rest of drafting.

If the issue persists, switch to multi-agent fan-out (smaller per-agent
context) or downgrade to `--depth standard`.
