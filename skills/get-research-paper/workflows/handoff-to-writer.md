# Hand-Off to the Writer Skill

When the user wants to **find papers AND write a paper** based on
them, this workflow connects `get-research-paper` (discovery) →
`research-paper` (writing).

The handoff is **file-based**: `bibliography.yaml` is the single
artifact that crosses the boundary.

---

## When the handoff happens

Three triggers:

1. **Explicit `--handoff` flag** — user wants to chain immediately:
   ```
   /get-research-paper "topic" --handoff --style ieee --years 2020-2024
   ```
2. **Follow-up `/research`** — user runs `/research` after a discovery
   run completes; the writer auto-detects an adjacent
   `bibliography.yaml`.
3. **Explicit `--bibliography <path>` to writer** — user runs the
   writer with a manual path:
   ```
   /research "topic" --bibliography ./gnn-fraud/bibliography.yaml --style ieee
   ```

---

## The bibliography contract

The writer skill's `bibliography.yaml` follows the schema in
`../research-paper/schemas/citation-schema.json`. Every entry must
have:

```yaml
- id: <cite_key>                       # required
  type: <one of the entry types>        # required
  authors: [{family: ..., given: ...}, ...]
  year: <int>
  title: "..."
  container: "..."                       # journal / conference / book
  volume: ...
  issue: ...
  pages: "..."
  publisher: ...
  doi: "..."                              # canonical: just the DOI suffix
  url: "..."
  arxiv_id: "..."                         # optional
  verification: verified | unverified-offline | unverified | retracted
  quality_score:
    authority: 0-4
    rigor: 0-3
    recency: 0-3
    total: 0-10
  notes: "..."                            # optional summary
```

The `get-research-paper` skill produces this directly. No conversion
needed.

---

## Cite-key naming

Cite-keys are `<lower(first-author-family)>_<year>_<first-content-word-of-title>`:

- `smith_2023_llm`
- `doe_2022_codex`
- `world_2024_ai` (organization authors → use the org name)

For collisions (same author, same year, same first word):

- `smith_2023_llm`
- `smith_2023_llm_b`
- `smith_2023_llm_c`

The writer skill's deduplication accepts these names directly.

---

## Handoff command

After producing outputs, the skill prints to the user:

```
Reading list ready. To write a paper using these sources:

  /research "<topic>" \
      --style <style> \
      --bibliography ./<topic-slug>/bibliography.yaml

Or run the writer with extra options:

  /research "<topic>" \
      --style <style> \
      --depth comprehensive \
      --bibliography ./<topic-slug>/bibliography.yaml \
      --audience academic
```

Where `<topic-slug>` is the URL-safe slug derived from the topic
(e.g., `gnn-fraud-detection`).

---

## Round-trip example

```bash
# Step 1: Discovery
/get-research-paper "graph neural networks for fraud detection" \
    --n 25 --years 2020-2024 --style ieee --handoff --depth deep

# Outputs:
#   ./gnn-fraud-detection/
#   ├── search-plan.md
#   ├── candidates.json
#   ├── ranked.json
#   ├── reading-list.md
#   ├── bibliography.yaml
#   ├── briefing.md
#   └── Known-gaps.md

# Step 2: Writing (uses the bibliography from step 1)
/research "graph neural networks for fraud detection" \
    --style ieee --depth comprehensive \
    --bibliography ./gnn-fraud-detection/bibliography.yaml

# Outputs:
#   ./gnn-fraud-detection/
#   ├── (everything above) +
#   ├── outline.md
#   ├── methodology.md
#   ├── analysis/
#   ├── figures/
#   ├── sections/
#   ├── paper-final.md
#   ├── validation/
#   ├── review/
#   └── Known-gaps.md (merged)
```

The same working directory hosts both the discovery artifacts and the
written paper, with the bibliography as the bridge.

---

## What the writer does with the bibliography

When the writer is invoked with `--bibliography <path>`:

1. It loads the bibliography as the canonical source of citations.
2. **It does not re-search.** This saves time and avoids citation
   drift between discovery and writing.
3. It uses the entries' `quality_score` to inform the literature-review
   section.
4. It uses the entries' `notes` (the discovery summaries) as input to
   the related-work synthesis.
5. It treats unverified entries as off-limits for load-bearing claims;
   they're only cited as "see also" in appendices unless the user
   explicitly resolves them.

---

## Reverse handoff

If the writer detects a citation gap during drafting (a
`[CITATION NEEDED — topic: "..."]` placeholder), it can re-invoke this
skill in **gap-fill mode**:

```
/get-research-paper "<gap topic>" --n 5 --append-to ./gnn-fraud-detection/bibliography.yaml
```

The discovery skill runs a focused 5-paper search and **appends** to
the existing bibliography (preserving cite_keys, deduplicating).

This pattern keeps the writer moving without forcing it to break flow
for citation searches.

---

## Best practices

- Always run discovery FIRST for unfamiliar topics. The writer is
  better when it has a curated bibliography to work from.
- Use `--years` to control what era of the field you're surveying.
  Old foundational + new state-of-the-art is usually right.
- Use `--quality-floor 7` for high-stakes runs (theses, journal
  submissions).
- For comprehensive runs, do `--depth deep` so the briefing seeds the
  writer's discussion section.
- For quick runs, `--depth quick --n 5` is enough to get a writer
  started.

---

## What this skill does NOT do

- It does not write the paper. That's `research-paper`.
- It does not do statistical analysis on the bibliography. That's
  outside scope for both skills.
- It does not auto-update existing bibliographies on a schedule. Run
  `--append-to` manually when you need new citations.
- It does not host the bibliography in a remote database. Files only.

The bibliography is portable, version-controllable, and durable.
