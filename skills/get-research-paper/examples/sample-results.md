# Example Run — `/get-research-paper "retrieval-augmented code review" --n 5 --depth standard --style ieee`

This is what the skill produces end-to-end for a sample query. All
papers in this example are illustrative — the skill verifies real
papers when run against a live web environment.

---

## Generated working directory

```
retrieval-augmented-code-review/
├── search-plan.md            # Phase 1 output
├── candidates.json           # Phases 2-3 (raw + dedup)
├── ranked.json               # Phase 4 (ranked + scored)
├── reading-list.md            # Phase 7 (user-facing)
├── bibliography.yaml          # Phase 7 (writer-skill ready)
├── briefing.md                # Phase 7 (skipped at standard depth)
└── Known-gaps.md              # Phase 7 (this run: 0 high-severity)
```

---

## reading-list.md (sample)

```markdown
# Reading list — Retrieval-augmented code review

Generated: 2024-05-12T14:23:00Z
Source: get-research-paper skill v1.0.0
Working directory: ./retrieval-augmented-code-review/

5 papers ranked 5/10 or higher, drawn from arXiv + Semantic Scholar.
Year range: 2020–2024.

> TL;DR briefing: skipped at --depth standard. Re-run with
> --depth deep or --briefing true to generate.

## Paper 1 — Retrieval-Augmented Generation for Code-Review Comments

**Cite key:** `smith_2023_retrieval`
**Authors:** Smith, J. A., Doe, A., Lee, K. B.
**Year:** 2023
**Venue:** Proceedings of ICSE 2023
**DOI:** [10.1109/ICSE.2023.00123](https://doi.org/10.1109/ICSE.2023.00123)
**Quality score:** 9/10 (authority 4/4, rigor 3/3, recency 2/3)
**Verification:** verified

> Addresses the question of whether retrieval-augmented LLMs can
> produce more useful code-review comments than vanilla LLMs. Evaluates
> a four-source retrieval pipeline (style guides, prior PRs, commit
> messages, design docs) on 4,212 real pull requests across three
> open-source repositories. Reports an 18-percentage-point gain in
> blinded reviewer-rated usefulness over the strongest baseline, with
> a 31% reduction in token cost.

## Paper 2 — A Critique of LLM-Code Review Benchmarks

**Cite key:** `thompson_2023_critique`
**Authors:** Thompson, R.
**Year:** 2023
**Venue:** Empirical Software Engineering
**DOI:** [10.1007/s10664-023-10312-9](https://doi.org/10.1007/s10664-023-10312-9)
**Quality score:** 8/10 (authority 3/4, rigor 3/3, recency 2/3)
**Verification:** verified

> Argues that existing LLM-code-review benchmarks systematically
> conflate retrieval quality with model ability. Re-runs three
> published benchmarks with controlled retrieval pipelines and finds
> that ablation reduces the LLM-only contribution by 8–34 percentage
> points. Calls for mandatory retrieval ablation in future evaluations.

## Paper 3 — Codex Evaluation in Production

**Cite key:** `doe_2022_codex`
**Authors:** Doe, A., Lee, K.
**Year:** 2022
**Venue:** ICSE 2022
**DOI:** [10.1145/9999.9999](https://doi.org/10.1145/9999.9999)
**Quality score:** 7/10 (authority 4/4, rigor 2/3, recency 1/3)
**Verification:** verified

> Tests OpenAI Codex on 1,200 real pull requests using a blinded
> human-rating protocol. Finds 11-percentage-point usefulness gains
> over a vanilla LLM baseline; identifies "convention misalignment"
> as the most common failure mode in 28% of low-rated comments.

## Paper 4 — Retrieval-Augmented Generation for Knowledge-Intensive NLP

**Cite key:** `lewis_2020_rag`
**Authors:** Lewis, P., Perez, E., Piktus, A., et al.
**Year:** 2020
**Venue:** NeurIPS 2020
**DOI:** [10.48550/arXiv.2005.11401](https://doi.org/10.48550/arXiv.2005.11401)
**Quality score:** 8/10 (authority 4/4, rigor 3/3, recency 1/3 + foundational)
**Verification:** verified

> Introduces the foundational RAG architecture, combining a parametric
> generator with non-parametric retrieval over Wikipedia. Demonstrates
> state-of-the-art performance on three knowledge-intensive NLP tasks
> with retrieval contributing roughly 70% of the gain on open-domain QA.

## Paper 5 — A Survey of LLMs in Software Engineering

**Cite key:** `nguyen_2023_survey`
**Authors:** Nguyen, M.
**Year:** 2023
**Venue:** ACM Computing Surveys
**DOI:** [10.1145/3589334](https://doi.org/10.1145/3589334)
**Quality score:** 7/10 (authority 4/4, rigor 2/3, recency 2/3)
**Verification:** verified

> Surveys 137 papers on LLMs in software engineering across six task
> categories (code generation, code review, bug repair, documentation,
> test generation, configuration). Identifies retrieval-augmentation
> as the dominant technique in 41 of those papers but flags that
> only 11% perform retrieval ablations.

---

## Source breakdown

| Source            | Candidates examined | Kept |
| ----------------- | -------------------- | ---- |
| arXiv              | 32                  | 2    |
| Semantic Scholar    | 28                  | 3    |
| Google Scholar      | 14                  | 0    |

## Notes

- Diversity heuristics applied: 1 review (paper 5), 1 foundational
  (paper 4), per-author cap held (max 1 per first-author).
- All papers verified via Crossref DOI lookup.
- 0 retracted papers in candidate pool.
```

---

## bibliography.yaml (sample)

```yaml
references:
  - id: smith_2023_retrieval
    type: article-conference
    authors:
      - {family: Smith, given: Jane A.}
      - {family: Doe, given: Alice}
      - {family: Lee, given: Kim B.}
    year: 2023
    title: "Retrieval-Augmented Generation for Code-Review Comments"
    container: "Proceedings of the 45th International Conference on Software Engineering (ICSE)"
    pages: "123-134"
    publisher: "IEEE"
    doi: "10.1109/ICSE.2023.00123"
    verification: verified
    quality_score: { authority: 4, rigor: 3, recency_relevance: 2, total: 9 }
    notes: "Addresses the question of whether retrieval-augmented LLMs can produce more useful code-review comments than vanilla LLMs. Evaluates a four-source retrieval pipeline on 4,212 real pull requests; reports an 18-pp gain in blinded reviewer-rated usefulness with 31% token-cost reduction."

  - id: thompson_2023_critique
    type: article-journal
    authors: [{family: Thompson, given: R.}]
    year: 2023
    title: "A Critique of LLM-Code Review Benchmarks"
    container: "Empirical Software Engineering"
    volume: 28
    issue: 4
    pages: "95-112"
    doi: "10.1007/s10664-023-10312-9"
    verification: verified
    quality_score: { authority: 3, rigor: 3, recency_relevance: 2, total: 8 }
    notes: "Argues that existing LLM-code-review benchmarks systematically conflate retrieval quality with model ability. Re-running three benchmarks with controlled retrieval reduces LLM-only contribution by 8-34 pp. Calls for mandatory retrieval ablation."

  - id: doe_2022_codex
    type: article-conference
    authors:
      - {family: Doe, given: Alice}
      - {family: Lee, given: Kim}
    year: 2022
    title: "Codex Evaluation in Production"
    container: "Proceedings of the 44th International Conference on Software Engineering (ICSE '22)"
    pages: "1245-1256"
    doi: "10.1145/9999.9999"
    verification: verified
    quality_score: { authority: 4, rigor: 2, recency_relevance: 1, total: 7 }
    notes: "Tests OpenAI Codex on 1,200 real pull requests using a blinded human-rating protocol; 11-pp usefulness gain over vanilla LLM baseline; identifies convention misalignment as most common failure mode (28%)."

  - id: lewis_2020_rag
    type: article-conference
    authors:
      - {family: Lewis, given: Patrick}
      - {family: Perez, given: Ethan}
      - {family: Piktus, given: Aleksandra}
    year: 2020
    title: "Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks"
    container: "Advances in Neural Information Processing Systems"
    volume: 33
    pages: "9459-9474"
    arxiv_id: "2005.11401"
    doi: "10.48550/arXiv.2005.11401"
    verification: verified
    quality_score: { authority: 4, rigor: 3, recency_relevance: 1, total: 8 }
    notes: "Introduces the foundational RAG architecture, combining parametric generator with non-parametric retrieval; SOTA on three knowledge-intensive NLP tasks; retrieval contributes ~70% of gains on open-domain QA."

  - id: nguyen_2023_survey
    type: article-journal
    authors: [{family: Nguyen, given: M.}]
    year: 2023
    title: "A Survey of LLMs in Software Engineering"
    container: "ACM Computing Surveys"
    volume: 55
    issue: 4
    pages: "1-37"
    doi: "10.1145/3589334"
    verification: verified
    quality_score: { authority: 4, rigor: 2, recency_relevance: 2, total: 8 }
    notes: "Surveys 137 papers on LLMs in software engineering across six task categories. Identifies retrieval-augmentation as dominant technique in 41 papers; flags that only 11% perform retrieval ablations."
```

---

## Handoff to writer skill

After this run, the user can hand off cleanly:

```bash
/research "retrieval-augmented code review" \
    --style ieee \
    --bibliography ./retrieval-augmented-code-review/bibliography.yaml \
    --depth standard
```

The writer skill reads the curated bibliography directly and uses it
to draft a paper without re-searching. The 5 papers above seed the
related-work section, the methodology comparisons, and the discussion.

---

## Known gaps (sample)

```markdown
# Known gaps

This run completed cleanly. No high-severity issues.

## Medium severity

(none in this example run)

## Low severity

- **[TOOLING DEGRADED]** — Google Scholar returned 14 candidates but
  the verification step couldn't reach Crossref for 2 of them
  (timeouts). Both have arXiv IDs and were ranked from those, but
  cross-check before submission.
  - Affected: `(none made it into the final list)`
```

---

## What this example shows

1. The skill produces both human-readable (`reading-list.md`) and
   machine-readable (`bibliography.yaml`) outputs from a single run.
2. Diversity heuristics fire (1 review, 1 foundational, no author
   dominance).
3. Quality scores explain why each paper was kept.
4. Verification trail is recorded per paper.
5. Handoff to the writer skill is one command away.
6. `Known-gaps.md` is the contract: if anything was unverifiable, it's
   surfaced — never silent.
