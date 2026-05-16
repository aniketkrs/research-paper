# Ranking Prompt

How to score every candidate paper and pick the top N for the reading
list. Mirrors the writer skill's `citation_engine/source-evaluation.md`,
extended with the diversity heuristics specific to discovery.

---

## Score per paper (0–10)

```
total = authority + rigor + recency_relevance
```

### Authority (0–4) — venue quality

| Score | Indicator                                                        |
| ----- | ---------------------------------------------------------------- |
| 4     | Top-tier (Nature, Science, NeurIPS, ICML, ICLR, CVPR, ACL, EMNLP, CHI, ACM Trans., IEEE Trans., NEJM, Lancet, JAMA, BMJ) |
| 3     | Reputable peer-reviewed (Q1/Q2 journal, mid-tier conference)      |
| 2     | Workshop / lower-tier conference / non-flagship journal           |
| 1     | Pre-print without peer review (arXiv, bioRxiv, SSRN)              |
| 0     | Blog / press release / marketing / unverified                       |

### Methodological rigor (0–3)

Use proxies based on what's available:

| Score | Indicator                                                         |
| ----- | ----------------------------------------------------------------- |
| 3     | Strong signals: large n, replicated, code/data released, pre-registered |
| 2     | Adequate methodology; one of the rigor signals missing             |
| 1     | Limited methods description / small or unrepresentative sample      |
| 0     | Anecdotal / methodologically opaque                                |

When the abstract gives only top-line numbers (no method details),
default to 2 unless venue quality compensates.

### Recency / relevance (0–3)

Field-pace dependent:

**Fast-moving (AI/ML, tech, social media):**
| Years old | Score |
|-----------|-------|
| ≤ 1       | 3     |
| 2–3       | 2     |
| 4–5       | 1     |
| > 5       | 0 (unless seminal/canonical) |

**Moderate (business, education, health):**
| Years old | Score |
|-----------|-------|
| ≤ 3       | 3     |
| 4–7       | 2     |
| 8–12      | 1     |
| > 12      | 0 (unless seminal/canonical) |

**Slow-moving (philosophy, history, mathematics):**
| Years old | Score |
|-----------|-------|
| Any age, on-topic | 3 |
| Tangential        | 1 |

Add **+1 to the recency score** for foundational / canonical papers
(papers cited > 100× in the field, or papers that introduced the
core concept). Cap total at 3.

### Total

Sum to 0–10. Drop anything below `--quality-floor` (default 5).

---

## Use this prompt verbatim

```
You are scoring research-paper candidates for a reading list on:
  Topic: <topic>

For each candidate, you have:
  - Title, authors, year, venue
  - Abstract (when available)
  - DOI / arXiv ID
  - Source (which database it came from)
  - Citation count (when available — Semantic Scholar / Scholar)
  - Tldr / summary signals (when available)

Score each candidate on three dimensions per the rubric in
ranking.md (above). Be conservative — when in doubt, score lower.

For each candidate, output:

  - cite_key: <derived>
    authority: <0-4>
    rigor: <0-3>
    recency_relevance: <0-3>
    total: <sum>
    rationale: "<one sentence justifying the score>"

Drop anything scoring below <--quality-floor>.
```

---

## Diversity heuristics — applied AFTER scoring

After scoring, when picking the top N from the surviving pool, apply:

### 1. Cap papers per first-author at 2

If a single first author has > 2 papers in the candidate pool, keep
the 2 highest-scoring and drop the rest. This avoids one-lab
dominance.

### 2. Cap papers per venue at 30% of N

If too many papers in the pool come from the same venue, keep the
top-scoring (`0.3 × N`) and drop the rest.

### 3. Ensure ≥ 1 review / survey if any exists

Reviews and surveys are high-leverage starting points. If the candidate
pool contains any (papers with "Survey", "Review", or "Systematic
Review" in the title, or `Review[PT]` from PubMed), include the
highest-scoring one.

### 4. Ensure ≥ 1 foundational paper

If the field has a foundational paper (≥ 7 years old, with > 100
citations) and one is in the candidate pool, include the
highest-scoring one. This anchors the list temporally.

### 5. Geographic / institutional diversity (best-effort)

If the candidate pool has affiliation data, prefer a mix of
institutions. This is best-effort — don't trade quality for
diversity.

---

## Diversity adjustments

After applying the heuristics, the final list may have papers
scoring slightly below the cutoff if they're the only review or
foundational paper available. That's OK; flag with a `notes` field:

```yaml
- cite_key: foundational_2017_attention
  ...
  total: 4
  notes: "Below quality floor (4 < 5) but kept for foundational coverage."
```

---

## Edge cases

### Tied papers

When two papers tie on total score, prefer:

1. The one with the higher **influentialCitationCount** (Semantic
   Scholar) over raw citation count.
2. The published version over the preprint.
3. The more recent one (within 1 year).
4. The one in the more cited venue.

### Single-source pool

If only one source returned anything (e.g., arXiv only), be honest
about coverage limits:

```markdown
[note in briefing] This reading list is drawn primarily from arXiv;
peer-reviewed venues for this topic should be cross-checked.
```

### Sparse pool

If the pool has < N candidates after scoring + diversity:

1. Lower `--quality-floor` by 1 and re-rank.
2. Loosen year filter and re-search.
3. Honestly deliver fewer papers than requested with an explanation.

Never fill the list with garbage to hit the requested N.

---

## Anti-patterns

- ❌ Inflating scores for arXiv preprints "because they're recent".
- ❌ Trusting raw citation counts as a quality stamp. Field-norm them.
- ❌ Picking 10 papers from the same lab even if all are relevant.
- ❌ Excluding all preprints from a fast-moving field. State of the
  art is often on arXiv first.
- ❌ Surfacing the rubric scores in the user-facing reading list. They
  go in the bibliography metadata, not the prose summary.
