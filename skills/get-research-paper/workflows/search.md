# Search Workflow

The master pipeline for the `get-research-paper` skill. Read this when
the skill activates; follow the phases sequentially; persist artifacts
to disk between phases.

---

## Phase 0 — Anchor to today's date (run FIRST)

Before building a search plan, determine today's actual date:

1. Run `date -u +%Y-%m-%d` (or check runtime context).
2. Persist to `<working-dir>/today.txt`.
3. Resolve relative year ranges against this date.

| Input         | Resolves to (today = 2025-03-14)  |
| ------------- | --------------------------------- |
| `--years last-1` | `2024-2025`                        |
| `--years last-3` | `2022-2025`                        |
| `--years last-5` | `2020-2025`                        |
| `--years recent`  | `2023-2025`                        |
| `--years current` | `2024-2025`                        |
| `--years 2020-2024` | literal (overrides relative)     |

**Default `--years` is `last-3`.** This anchors searches to actual
recent literature, not to the model's training cutoff.

Full protocol: `instructions/freshness.md`.

---

## Phase 1 — Intake and search-plan

**Goal:** turn the user's topic into a precise search plan.

1. Parse the request (topic, options).
2. Read `prompts/search-strategy.md`.
3. Build:
   - **Primary terms** (2–4 keyword combos).
   - **Secondary terms** (synonyms, related concepts).
   - **Inclusion / exclusion criteria** (date range, language,
     publication types).
   - **Source priority list** (per `sources/source-priority.md`).
   - **Target paper count** (`--n`, default 10).
   - **Quality floor** (`--quality-floor`, default 5).
4. Write `search-plan.md` to disk.

**Output:** `<working-dir>/search-plan.md`.

---

## Phase 2 — Source dispatch

**Goal:** run searches in priority order until the candidate pool is
≥ 3× target count.

For each source in `search-plan.md`:

1. Open `sources/<source>.md` for that source's specific protocol.
2. Run the searches:
   - **arXiv:** prefer `toolchains/arxiv_search.py` if Python +
     `feedparser` available; else `WebFetch` of `export.arxiv.org/api/query`.
   - **Google Scholar:** `WebSearch` with `site:scholar.google.com` +
     keywords + year filter.
   - **Semantic Scholar:** `WebFetch` of
     `api.semanticscholar.org/graph/v1/paper/search`.
   - **PubMed:** `WebFetch` of `eutils.ncbi.nlm.nih.gov/entrez/eutils/`.
   - **DBLP:** `WebFetch` of `dblp.org/search/publ/api`.
   - **OpenReview:** `WebFetch` of `api.openreview.net`.
3. Capture for each candidate:
   - title, authors, year, venue, DOI / arXiv ID, abstract (when
     available), URL.
4. Persist to `<source>-candidates.json` (one file per source).

If `web-search` / `web-fetch` are unavailable, fall back to
**model-known papers** for the topic. Mark every entry
`verification: unverified-offline`. Lower the candidate target to
`--n × 1.5`.

---

## Phase 3 — De-duplication

**Goal:** collapse candidates into a single canonical pool.

Two candidates are duplicates if ANY of:
- Same DOI.
- Same arXiv ID.
- Same first-author family name + same year + first 5 normalized
  title words match.

When a duplicate is detected:
- Prefer the **published / peer-reviewed** version over the preprint.
- Prefer the **more complete** metadata.
- Merge unique metadata fields.

Persist deduplicated pool to `candidates.json`.

---

## Phase 4 — Ranking

**Goal:** score every candidate and select the top N.

For each candidate, compute (per `prompts/ranking.md`):

- **Authority (0–4):** venue quality (top journal / top conference /
  reputable / mid-tier / preprint / other).
- **Methodological rigor (0–3):** sample size, study design,
  reproducibility signals.
- **Recency / relevance (0–3):** how fresh + topical, OR how
  foundational + canonical.
- **Total (0–10).**

Drop anything below `--quality-floor` (default 5). From what remains,
pick the top `--n` papers, with diversity heuristics:

- Cap papers per first-author at 2 (avoid one-lab dominance).
- Cap papers per venue at 30% of the list.
- Ensure ≥ 1 review / survey if any exist in the pool.
- Ensure ≥ 1 foundational paper (≥ 7 years old) if the topic has one.

Persist ranked list to `ranked.json`.

---

## Phase 5 — Verification

**Goal:** confirm every chosen paper exists and is not retracted.

When web tools are available:
1. **Resolve DOIs** via `https://doi.org/<doi>` (HEAD request).
2. **Confirm metadata** via Crossref (`api.crossref.org/works/<doi>`).
3. **Check Retraction Watch** (`retractionwatch.com/database`) for the DOI.
4. For arXiv-only entries, confirm via `export.arxiv.org/api/query?id_list=<id>`.

When web tools are unavailable:
- Mark every entry `verification: unverified-offline`.
- Surface in `Known-gaps.md`.

For verified entries: mark `verification: verified`.
For retracted entries: drop from list; add to `Known-gaps.md` with
the retraction notice URL.

---

## Phase 6 — Summarization

**Goal:** produce 2–4 sentence summaries per paper.

Read `prompts/summarization.md`. For each paper:

1. Use the abstract (if available) as the source of truth.
2. Compose a summary in **problem → method → finding → significance**
   structure.
3. Keep to 2–4 sentences (`quick`: 2; `standard`: 3; `deep`: 4).
4. Avoid jargon when `--audience` is general; preserve technical terms
   when `academic`.
5. Add a "Why it matters for `<topic>`" one-liner (the relevance
   anchor).

Persist summaries inside the paper objects in `ranked.json`.

---

## Phase 7 — Assembly

**Goal:** emit user-facing outputs.

1. **`reading-list.md`** (always) — per `templates/reading-list.md`.
2. **`bibliography.yaml`** (always) — per
   `workflows/handoff-to-writer.md`.
3. **`briefing.md`** (default ON for `--depth deep`, opt-in
   otherwise via `--briefing true`) — per `workflows/synthesis.md`.
4. **`Known-gaps.md`** (always; may be empty if no issues) — same
   format as the `research-paper` skill.

---

## Phase 8 — Handoff (optional)

If `--handoff` was set, also emit a follow-up command for the user:

```markdown
## Next step (writer skill)

```
/research "<topic>" \
    --style <style> \
    --bibliography <working-dir>/bibliography.yaml
```
```

The user runs this command; the writer skill reads the bibliography
directly.

---

## Multi-source orchestration

For `--depth deep` runs with `agent-spawn` available, fan out:

```
Orchestrator
   ├── arXiv-agent       → arxiv-candidates.json
   ├── Scholar-agent     → scholar-candidates.json
   ├── Semantic-agent    → semantic-candidates.json
   ├── PubMed-agent      → pubmed-candidates.json
   └── DBLP-agent        → dblp-candidates.json
                              │
                              ▼
                       Merge + de-dupe
                              │
                              ▼
                          Rank, verify, summarize
                              │
                              ▼
                       Assemble outputs
```

Each agent reads only its source-specific module and writes only its
own candidates file. The orchestrator gathers and proceeds.

---

## Failure handling

| Phase                  | Failure                                  | Recovery                                              |
| ---------------------- | ---------------------------------------- | ----------------------------------------------------- |
| Search-plan             | Topic too broad / narrow                  | Ask one clarifying question; default to standard scope |
| Source dispatch         | Web tools missing                         | Use model-known papers; mark unverified                |
| Source dispatch         | Source returns nothing                    | Broaden query; try synonyms                            |
| Source dispatch         | Source rate-limited                        | Backoff + retry once; skip if persistent               |
| Verification            | DOI fails to resolve                      | Mark unverified; flag in Known-gaps                    |
| Verification            | Retraction detected                        | Drop from list; flag in Known-gaps                     |
| Summarization           | No abstract available                     | Construct from title + venue; flag in Known-gaps       |
| Assembly                | Reading-list shorter than `--n`           | Surface honestly; deliver what was found                |

Never silently fail. `Known-gaps.md` is the contract.
