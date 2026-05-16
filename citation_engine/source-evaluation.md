# Source Evaluation

This file is the canonical guide for judging whether a source is trustworthy
enough to cite. Every reference produced by this skill is scored against the
rubric below, and low-scoring sources are flagged.

> **Rule:** A paper that cites strong sources can be wrong. A paper that
> cites weak sources is rarely right.

---

## 1. Source-quality scoring (0–10)

Each candidate source is scored on three dimensions:

### 1.1 Authority (0–4)

| Score | Indicator                                                         |
| ----- | ----------------------------------------------------------------- |
| 4     | Top-tier peer-reviewed venue (Nature, Science, NeurIPS, ICML, CHI, ACM Trans., IEEE Trans.) |
| 3     | Reputable peer-reviewed venue (well-indexed Q1/Q2 journal, mid-tier conference) |
| 2     | Workshop / lower-tier conference / non-flagship journal             |
| 1     | Pre-print without peer review (arXiv only) **OR** technical report from reputable lab |
| 0     | Blog, press release, marketing material, anonymous source          |

### 1.2 Methodological rigor (0–3)

| Score | Indicator                                                         |
| ----- | ----------------------------------------------------------------- |
| 3     | Pre-registered, reproducible (code + data), large + diverse sample, sound stats |
| 2     | Reproducible *or* large sample *or* sound stats — but missing one  |
| 1     | Limited methods detail / small or unrepresentative sample / weak stats |
| 0     | Anecdotal / methodologically opaque / discredited                  |

### 1.3 Recency and relevance (0–3)

| Score | Indicator                                                         |
| ----- | ----------------------------------------------------------------- |
| 3     | ≤ 3 years old AND directly relevant **OR** seminal foundational work cited universally |
| 2     | ≤ 5 years old AND directly relevant                                |
| 1     | > 5 years old but still relevant; OR recent but tangential         |
| 0     | Outdated AND tangential                                           |

**Total score:** 0–10. Acceptable for citation: ≥ 5 by default; ≥ 7 for any
load-bearing claim. Sources < 5 should be replaced or removed.

---

## 2. Source hierarchy (preferences)

When multiple sources support the same claim, prefer in this order:

1. **Peer-reviewed meta-analyses** in top venues
2. **Peer-reviewed systematic reviews** in top venues
3. **Peer-reviewed empirical studies** in top venues
4. **Reputable government / NGO reports** with primary data (WHO, OECD,
   World Bank, Eurostat, US Census, NIST)
5. **Reputable peer-reviewed empirical studies** in mid-tier venues
6. **Pre-prints with strong methodology** (arXiv with code, replicated)
7. **Industry research reports** with disclosed methodology (Gartner,
   McKinsey, Pew, ACM/IEEE technical reports)
8. **Standards documents** (ISO, IEEE, RFC) — for technical specs
9. **Reputable textbooks** — for foundational background
10. **Pre-prints without methodology / replication** — flag as `[UNVERIFIED]`
11. **High-quality journalism** with named sources — only for current events,
    flagged as journalistic
12. **Blogs / personal websites** — only for primary statements by the
    individual themselves (e.g., a researcher's blog explaining their own
    paper)

---

## 3. Domain-specific gold-standard sources

Use these as anchor sources before searching elsewhere:

### Computer Science / ML
- **Venues:** NeurIPS, ICML, ICLR, CVPR, ICCV, ECCV, ACL, EMNLP, NAACL,
  AAAI, IJCAI, KDD, SIGGRAPH, OSDI, SOSP, USENIX, IEEE S&P, CCS, ICSE,
  FSE, CHI, ACM Trans. *, IEEE Trans. *
- **Repositories:** arXiv (cs.*), DBLP, Papers With Code

### Biomedical
- **Databases:** PubMed/MEDLINE, Cochrane Library, EMBASE, PsycINFO
- **Top journals:** *Nature*, *Science*, *Cell*, *NEJM*, *Lancet*, *JAMA*, *BMJ*

### Social Sciences
- **Databases:** Web of Science, Scopus, JSTOR, ProQuest, EconLit
- **Top journals (econ):** *AER*, *QJE*, *JPE*, *Econometrica*, *RES*
- **Top journals (psych):** *Psych. Science*, *Psych. Review*, *JPSP*
- **Top journals (mgmt):** *AMJ*, *AMR*, *ASQ*, *SMJ*, *MISQ*, *ISR*

### Government / NGO
- **Statistics:** Eurostat, OECD.Stat, World Bank Open Data, IMF, US Census,
  BLS, Office for National Statistics (UK)
- **Health:** WHO, CDC, ECDC
- **Standards:** ISO, IEEE Standards, RFCs (IETF), NIST

---

## 4. Red flags (auto-reject)

A source is **rejected** if any of:

- **Predatory journal** — appears on Beall's List, no real peer review.
- **Retracted** — listed on Retraction Watch (always check load-bearing
  citations).
- **Sponsored content** disguised as research without disclosure.
- **AI-generated paper mill** content.
- **Single-source claim** that contradicts strong consensus, with no
  replication.
- **Anonymous / pseudonymous** for substantive claims (acceptable for
  technical specs in some contexts).
- **Unverifiable** — DOI / URL doesn't resolve, source can't be found.

The validation pipeline checks each citation against these red flags.

---

## 5. Triangulation

For any claim that load-bears the paper's argument, **cite at least two
independent sources**. Independent means:

- Different research groups
- Different methods (e.g., one survey + one experiment)
- Different time periods
- Different populations / settings

If only one source supports the claim, present it as such ("In one recent
study, X was observed (Smith, 2023); replication is needed.") rather than
as established fact.

---

## 6. Conflict-of-interest awareness

Mark sources where the authors have a stake in the conclusion:

- Industry-funded studies of that industry's product (tobacco, pharma, AI
  benchmarks by a model's authors).
- Government reports defending a current policy.
- Advocacy-group reports — useful for context, weak for "objective" facts.

These can still be cited but should be **balanced** with independent sources.

---

## 7. Currency and supersession

Always check whether a cited finding has been:

- **Replicated** — strengthens citation.
- **Failed to replicate** — weakens; cite the failure too.
- **Superseded** by a later, better study — cite the newer one as primary,
  the older one as historical background.
- **Retracted** — must not be cited (or only as a cautionary example).

For ML benchmarks: cite the **leaderboard standard** (currently leading
result with replication) rather than a snapshot from a year-old paper.

---

## 8. Verification workflow

When web tools are available, the skill verifies each citation:

1. Resolve the DOI or URL.
2. Confirm the title, author list, year match the metadata.
3. Check Retraction Watch for the DOI.
4. (Optional) Pull the abstract and check it actually supports the claim
   it's cited for.

If web tools are **unavailable**, every citation that wasn't supplied
verbatim by the user is marked `[UNVERIFIED — offline]` and surfaced in the
review pass. The skill never silently invents citations.

---

## 9. Grey-literature handling

Government reports, NGO white papers, industry analyses, theses, working
papers, and policy briefs can be **grey literature** — not formally peer
reviewed but often essential. To cite them:

- Confirm the **publishing organization** is reputable.
- Confirm the **author / authoring body** is named.
- Confirm a **stable URL** (preferably with a **publisher-issued report
  number**).
- Note **methodology** if the source is making empirical claims.
- Disclose the **limitation** of the source in the discussion if it's
  load-bearing.

---

## 10. Wikipedia, blogs, social media

| Source                         | When to cite                                                 |
| ------------------------------ | ------------------------------------------------------------ |
| Wikipedia                       | **Never** for substantive claims. Cite the underlying source linked from Wikipedia instead. |
| Personal / lab blog            | Only if it's a primary statement by the named author about their own work. |
| Twitter / X / Mastodon          | Only for documenting public communications themselves (e.g., a CEO's announcement). Always include archived URL. |
| Documentation / README          | Acceptable for software / API specifications.                |
| Stack Overflow / GitHub issues  | Acceptable for documenting bugs / behaviors observed; weak for general claims. |

---

## 11. Output: the source-quality table

The skill produces a **source-quality appendix** for any paper with > 30
references. The table has columns:

| Cite key | Authority (0–4) | Method (0–3) | Recency (0–3) | Total (0–10) | Notes |
| -------- | --------------- | ------------ | ------------- | ------------ | ----- |

This makes the paper's evidence base auditable. For systematic reviews this
is mandatory; for other papers it's optional but recommended.

---

## 12. The two questions to ask before citing anything

1. **Is this source credible?** (See §1–§4.)
2. **Does it actually say what I'm citing it for?** (Read it. The single
   most common citation error is citing a source for a claim it doesn't
   make.)

If either answer is no, find a different source — or remove the claim.
