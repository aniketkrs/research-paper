# Source Credibility Scoring Engine

## Purpose
Assess the reliability, authority, and relevance of each source used in the paper.

---

## Credibility Score (1-10)

### Scoring Criteria

| Dimension | Weight | Evaluation |
|-----------|--------|-----------|
| Publication venue quality | 25% | Impact factor, reputation, peer review rigor |
| Author authority | 20% | Expertise, citation count, institutional affiliation |
| Methodology rigor | 20% | Study design, sample size, replicability |
| Recency | 15% | How current relative to field's pace of change |
| Relevance | 15% | Direct applicability to the current research question |
| Corroboration | 5% | Whether findings are supported by other independent sources |

---

## Venue Quality Rubric

| Score | Venue Type |
|-------|-----------|
| 10 | Top-tier journals (Nature, Science, Lancet, JACM, JMLR) |
| 9 | High-impact field-specific journals (IEEE TPAMI, VLDB, etc.) |
| 8 | Well-established journals with rigorous review (2+ reviewers, low acceptance) |
| 7 | Reputable conferences (NeurIPS, ICML, CHI, AAAI, SIGMOD, top-tier) |
| 6 | Solid mid-tier journals and conferences; government reports |
| 5 | Professional organization publications; institutional reports |
| 4 | Working papers from reputable institutions; arXiv with high citations |
| 3 | arXiv preprints (recent, limited citations); industry reports |
| 2 | Theses/dissertations; non-peer-reviewed publications |
| 1 | Blog posts; media articles; unverified online content |

---

## Author Authority Assessment

```
SIGNALS of high authority:
- Multiple publications in the specific topic area
- High citation count (h-index proxy)
- Affiliation with recognized research institution
- Leading research group/lab in the field
- Invited keynotes or panels at major venues
- Editorial board membership for relevant journals

SIGNALS of lower authority (not disqualifying, but weight accordingly):
- First or early publication in the area
- No established track record
- Affiliation unclear or non-academic
- Self-published without peer review
- Conflicts of interest (industry funding for industry-favorable findings)
```

---

## Recency Scoring

```
FIELD-DEPENDENT recency expectations:

FAST-MOVING fields (AI/ML, tech, social media):
- <1 year: 10
- 1-2 years: 8
- 3-4 years: 6
- 5-7 years: 4
- 8+ years: 2 (unless seminal/foundational)

MODERATE fields (business, education, health):
- <2 years: 10
- 3-5 years: 8
- 6-10 years: 6
- 11-15 years: 4
- 15+ years: 2 (unless seminal)

SLOW-MOVING fields (philosophy, history, mathematics):
- <5 years: 10
- 5-10 years: 9
- 10-20 years: 7
- 20-50 years: 5
- 50+ years: 3 (unless foundational)

EXCEPTION: Seminal/foundational papers are always scored 8+ regardless of age.
A paper is "seminal" if it introduced a concept, framework, or method that
is still foundational to the field (>1000 citations or universally referenced).
```

---

## Relevance Assessment

```
SCORE relevance to the current paper:

10: Directly addresses the same research question with similar methodology
 9: Addresses same topic with findings directly applicable
 8: Addresses closely related topic; findings clearly relevant
 7: Related topic; requires some inference to connect
 6: Same field; tangentially relevant
 5: Adjacent field; provides useful context
 4: Different field; methodological relevance only
 3: Provides general background context
 2: Only peripherally related
 1: Included for completeness but adds minimal value

MINIMUM relevance to include: 4+
FLAG for removal: score of 1-3 unless providing essential methodological
or definitional foundation.
```

---

## Contradiction and Consensus Detection

```
WHEN multiple sources address the same question:

CONSENSUS (3+ sources agree):
- Flag as "established finding"
- Cite all supporting sources
- Weight: HIGH confidence

MAJORITY (most agree, 1-2 dissent):
- Present majority view as primary
- Acknowledge dissenting view
- Explain possible reason for disagreement
- Weight: MODERATE-HIGH confidence

DIVIDED (roughly equal disagreement):
- Present both positions fairly
- Analyze methodological differences that may explain divergence
- Do not take a position unless own data supports one side
- Weight: LOW confidence — flag as "contested"

CONTRADICTORY (strong evidence on both sides):
- Dedicated paragraph explaining the controversy
- Evaluate each side's methodology
- Acknowledge the unresolved nature
- May be a key contribution if this paper resolves it
- Weight: UNCERTAIN — opportunity for contribution

SINGLETON (only one source):
- Flag as "limited evidence base"
- Cannot be treated as established fact
- Hedging language required
- Suggest replication as future work
```

---

## Source Validation Workflow

```
FOR EACH potential source:

1. IDENTIFY
   - What is the publication venue?
   - Who are the authors?
   - When was it published?
   - What type of publication is it?

2. SCORE
   - Venue quality: [1-10]
   - Author authority: [1-10]
   - Methodology rigor: [1-10]
   - Recency: [1-10]
   - Relevance: [1-10]
   - COMPOSITE SCORE: weighted average

3. DECIDE
   - Score ≥ 7: Include with confidence
   - Score 5-6: Include with context (note limitations)
   - Score 3-4: Include only if no better source exists for this point
   - Score 1-2: Exclude (or cite only to refute)

4. DOCUMENT
   - Record score and rationale
   - Note any caveats about the source
   - Track which claims this source supports
```

---

## Red Flags (Automatic Low Score)

- Predatory journal (check against Beall's List indicators)
- No peer review process
- Author has retracted papers on same topic
- Obvious conflicts of interest undisclosed
- Sample size absurdly small for claims made
- Results "too good to be true" (100% accuracy, zero variance)
- Publication from known misinformation source
- Cannot verify the source actually exists (fabricated reference)
