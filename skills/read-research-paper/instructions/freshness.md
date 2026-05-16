# Freshness Protocol — date-awareness for every run

> **The single most important rule:** the model's knowledge has a
> training-data cutoff. Without explicit anchoring to **today's
> actual date**, every paper drifts toward old data. This file is the
> protocol that prevents that drift.

---

## 1. Phase 0 — determine TODAY's actual date

**Before any planning, search, or writing**, the orchestrator
determines the current date through one of:

| Source                                    | Priority | How                                           |
| ----------------------------------------- | -------- | --------------------------------------------- |
| Runtime context (env var / system clock)    | 1        | Check `Date.now()` / `date` shell command      |
| User's message / explicit date in request   | 2        | Parse phrases like "today", "this year", a date |
| File system metadata of session files       | 3        | `stat -c %y` or equivalent on the working dir   |
| Web fetch (`https://api.ipgeolocation.io/timezone` or similar) | 4 | Optional, when web tools available |
| Model's training cutoff                       | 5        | LAST resort, with explicit warning              |

The orchestrator writes the resolved date to `paper-spec.md →
context.today_date` at the start of every run.

**Sample bash:**
```bash
date -u +%Y-%m-%d                 # produces '2025-03-14' or whatever today is
```

**Sample agent prompt:**
```
Determine today's date by checking the system clock (run `date -u
+%Y-%m-%d`). Do NOT use the model's training-cutoff date. Persist
the result to paper-spec.md.
```

If the orchestrator cannot resolve the date with confidence, it
**asks the user once**: "What's today's date? (e.g., 2025-03-14)".

---

## 2. Year ranges are RELATIVE to today

| User input     | Resolves to (assuming today = 2025-03-14)      |
| -------------- | ---------------------------------------------- |
| `--years last-1`  | 2024-2025                                       |
| `--years last-3`  | 2022-2025                                       |
| `--years last-5`  | 2020-2025                                       |
| `--years last-10` | 2015-2025                                       |
| `--years recent`   | 2023-2025 (last ~2 years)                       |
| `--years current`  | 2024-2025 (current year + last)                 |
| `--years 2020-2024` | 2020-2024 (literal, override the relative)    |

When the user doesn't specify, the **default is `last-3`** for
fast-moving fields (CS / ML / AI) and `last-5` for slower ones
(humanities / clinical).

---

## 3. Search-strategy directives

When generating search queries (in
`prompts/literature-search.md` / `prompts/search-strategy.md`):

1. **Always include a date filter** matching the resolved year range.
2. **Sort by recency** for the first pass (`--sort submittedDate
   --order desc` for arXiv).
3. **Run the search at least twice**:
   - Pass 1: recent papers (`last-3` years) — for state of the art.
   - Pass 2: foundational papers (uncapped) — for canonical anchors.
4. **Mark every result with its publication year** in the candidate
   pool.
5. **Quality-rank with a recency boost**: papers in the last 12
   months get +1 to recency score.

---

## 4. Web search for current events

For topics with a "current events" component (politics, recent
research breakthroughs, recent regulatory changes, etc.), the
orchestrator:

1. Triggers a **web search** as soon as `WebSearch` tool is available.
2. Specifies the year range explicitly in the query: `"<topic>
   2024 OR 2025"`.
3. Cross-references against the bundled corpus to confirm freshness.
4. Flags any paper older than the year range as `[OUT-OF-DATE-RANGE]`
   in the reading list.

---

## 5. Training-cutoff disclosure

When the orchestrator falls back to model-knowledge (no web tools,
no live fetch, no cache hit, no corpus hit):

1. The output's verification trail explicitly says:
   ```
   Source tier: model-knowledge
   Training-cutoff disclosure: [yes / no]
   Latest known development on this topic: [date if known]
   ```
2. The model's training-cutoff date is also surfaced (when
   asked, models can usually report it; otherwise default to "training
   data may be up to ~12 months out of date").
3. The user sees this banner before the rendered paper:
   ```
   ⚠ This rendering relies on the model's training data, which may
   be up to N months out of date. For the most current findings,
   re-run with web search enabled (--with-web).
   ```

---

## 6. Anti-staleness checks (the validator's job)

After drafting / rendering, the validation pipeline runs an
anti-staleness check:

| Check                                   | Severity | Action                                  |
| --------------------------------------- | -------- | --------------------------------------- |
| All cited papers are > 5 years old       | medium    | Flag in `Known-gaps.md` ("dated sources") |
| Most recent cited paper > 3 years old    | medium    | Same                                    |
| Paper says "as of [year < current]"      | low      | Flag for date refresh                    |
| Paper says "current state of the art is..." but cites only old work | high | Block delivery; surface |
| Paper makes "trend" claims with no recent data | medium | Flag                                  |

If any of these fire, the orchestrator surfaces them in
`Known-gaps.md` so the user knows their paper may need a refresh.

---

## 7. Recency in the writing voice

When the writer drafts:

- Use **"as of <today's date>"** instead of bare year claims when
  citing the state of the art.
- Use **"recent" and "current"** sparingly and tie them to actual
  year ranges in the cited literature.
- For trend language ("X has grown 40% since Y"), **include the
  actual year in the prose**, not vague phrasing like "in recent
  years".
- The final paragraph of the introduction should explicitly state:
  "This paper reflects the state of the field as of <current
  month / year>." or include a date in the abstract.

---

## 8. Per-skill specifics

### `research-paper` (writer)

- Phase 0 of `orchestration/pipeline.md`: **"Determine today's
  date"** must precede planning.
- `prompts/research-planning.md`: include the resolved date in
  `paper-spec.md`.
- `prompts/literature-search.md`: default year range is `last-3`.
- The Methodology section's "Reproducibility statement" must
  include the date the paper was generated.

### `get-research-paper` (finder)

- Default `--years` is now `last-3` (was `last-10` previously).
- Search runs in two passes: recent (`last-3`) + foundational
  (uncapped).
- Ranking adds a +1 recency boost to papers in the last 12 months.

### `read-research-paper` (reader)

- The verification trail in `paper-visual.md` declares the source
  tier AND the freshness:
  ```
  Source tier: live-fetch / cache / bundled-corpus / model-knowledge
  Paper publication date: <YYYY-MM>
  Today's date: <YYYY-MM-DD>
  Freshness: <fresh / dated / very-dated>
  ```
- If the corpus is the only available source AND the topic is
  fast-moving, the rendering carries a banner:
  "⚠ The corpus version of this topic may not reflect the latest
  developments."

---

## 9. Implementation cheat-sheet

To wire freshness into a new orchestration step:

```python
# Pseudocode the orchestrator should execute first
import datetime, subprocess

# Try system date (most reliable)
today = datetime.date.today().isoformat()

# Or via shell when running through Bash tool
# today = subprocess.check_output(["date", "-u", "+%Y-%m-%d"]).decode().strip()

# Resolve year ranges
def resolve_years(spec, today):
    year = int(today[:4])
    if spec == "last-1":   return (year - 1, year)
    if spec == "last-3":   return (year - 3, year)
    if spec == "last-5":   return (year - 5, year)
    if spec == "last-10":  return (year - 10, year)
    if spec == "recent":   return (year - 2, year)
    if spec == "current":  return (year - 1, year)
    if "-" in str(spec):
        a, b = spec.split("-")
        return (int(a), int(b))
    return (year - 3, year)  # default
```

Persist `today` and `year_range` to `paper-spec.md` so every
downstream phase reads from a single source of truth.

---

## 10. Why this matters

Without explicit date anchoring, a model's "current state of the
art" output will silently default to whatever was current at its
training cutoff — which can be 6–18 months stale. For fast-moving
fields like AI / ML / NLP, this is the difference between citing
GPT-3.5 as state of the art (2023) vs. citing the genuine current
frontier (2025).

The orchestrator's job is to **never let this happen silently**.
Either:
- Anchor to today's date and search for current sources, OR
- Fall back to training data with a clear warning banner.

Never the silent middle ground.
