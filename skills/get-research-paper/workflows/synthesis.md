# Synthesis Workflow

How to turn a ranked, verified list of papers into a **field briefing**
that helps the user understand the topic, not just the papers.

---

## When to run synthesis

- Default ON for `--depth deep`.
- Opt-in for `standard` (`--briefing true`).
- Skipped for `quick` (the reading list itself is the deliverable).

---

## What the briefing contains

A 1–3 paragraph synthesis structured as:

### Paragraph 1 — State of the field

- What is the consensus / dominant approach?
- What are the major schools of thought (if multiple)?
- What is the headline finding most papers converge on?

### Paragraph 2 — Tensions and open problems

- Where do papers disagree?
- What's contested?
- What's missing from the literature?

### Paragraph 3 — Trajectory (optional, for `deep` only)

- Where is the field heading?
- What new subtopics are emerging?
- What might the next 2–3 years of research look like?

Cite specific cite_keys inline so the briefing is verifiable:

> "Recent work converges on X (smith_2023, doe_2022, lee_2024), though
> the question of whether Y holds in adversarial settings remains
> contested (zhang_2023a vs. wang_2024)."

---

## Structure rules

- **One paragraph per theme.** Don't string together unrelated points.
- **Every claim cites a paper from the reading list.** No new sources.
- **Use the cite_keys** that are also in `bibliography.yaml`. Same
  IDs across files.
- **No marketing words** ("revolutionary", "groundbreaking",
  "paradigm-shifting"). Match the certainty of the literature.
- **Acknowledge limits** — if the field is young, say "this is an
  emerging area with limited replication"; if old, "well-established
  but still active".

---

## Length budget

| Depth      | Target length  |
| ---------- | --------------- |
| `quick`    | (no briefing)   |
| `standard` | 1 paragraph (≤ 150 words) |
| `deep`     | 3 paragraphs (300–500 words) |

If the briefing wants to grow longer, the user probably needs a
literature review (`/literature-review`) instead.

---

## Audience adjustment

- `--audience academic` → assume field-specific terms; cite densely.
- `--audience technical` → define field jargon on first use; include
  one analogy per paragraph.
- `--audience general` → plain English (Flesch–Kincaid ≤ 12); avoid
  jargon entirely; use analogies.

The skill produces ONE briefing, audience-tuned. To get multiple,
run twice with different `--audience`.

---

## Output file

Write to `<working-dir>/briefing.md`:

```markdown
# Field briefing — <topic>

Generated: <ISO timestamp>
Based on <n> papers ranked 5+/10 from <source list>.

## State of the field

<paragraph 1>

## Tensions and open problems

<paragraph 2>

## Trajectory (deep only)

<paragraph 3>

---

**Reading list:** see `reading-list.md`.
**Bibliography:** see `bibliography.yaml`.
```

---

## Synthesis prompt template

```
You are a senior researcher synthesizing the field of <topic>. You have
been given <N> ranked papers (their summaries are in <ranked.json>).

Write a <length-budget> briefing structured as:
1. State of the field — consensus, dominant approach, headline finding.
2. Tensions and open problems — disagreements, gaps, contested claims.
3. (Deep only) Trajectory — where the field is heading.

Constraints:
- Cite cite_keys inline, e.g., (smith_2023, doe_2022).
- Every claim must come from a paper in the reading list.
- Do NOT introduce new sources.
- Match the certainty of the literature; no overclaiming.
- <audience-specific tone instructions>

Write the briefing now.
```

---

## Post-processing

After the model produces the briefing:

1. Parse all cite_keys; verify each appears in
   `bibliography.yaml`. Flag any orphan cite in `Known-gaps.md`.
2. Compute reading level (Flesch–Kincaid). If `--audience general`
   and grade > 12, request a rewrite.
3. Length check against the budget. Trim or expand to fit.
4. Write to `briefing.md`.

---

## Why the briefing matters

A reading list is a starting point. A briefing gives the user enough
context to know **why** to read those papers and **in what order**.
For `--handoff` runs, the briefing also seeds the writer skill's
"Position of this work" paragraph.

---

## Anti-patterns

- ❌ Listing the papers one by one ("Smith 2023 found X. Doe 2022
  found Y…"). That's the reading list, not a synthesis.
- ❌ Summarizing the field at the abstract level ("AI is changing
  research"). Too vague.
- ❌ Citing papers not in the reading list. Hallucination risk.
- ❌ Three-item lists for everything. Vary structure.
- ❌ Concluding with "more research is needed" without specifics.
  If the briefing identifies a gap, name the gap concretely.
