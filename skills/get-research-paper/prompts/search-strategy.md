# Search Strategy

How to turn a user's topic into a precise multi-source search plan.

---

## Use this prompt verbatim (or adapt the questions)

```
You are a research librarian. The user has asked for research papers
on the following topic:

  Topic: <user's topic>
  Number of papers: <--n, default 10>
  Year range: <--years, default last-10>
  Source preference: <--source, default all>
  Quality floor: <--quality-floor, default 5>
  Audience: <--audience, default academic>
  Citation style: <--style, default harvard>

Build a search plan that:

1. Identifies the DOMAIN of the topic
   (CS / biomedical / engineering / social-science / humanities / etc.)
   per sources/source-priority.md §1.

2. Lists 2-4 PRIMARY search-term combinations using the topic's
   essential keywords. Use Boolean operators where supported.

3. Lists 4-8 SECONDARY search-term combinations using:
   - Synonyms ("retrieval-augmented" / "RAG" / "knowledge retrieval")
   - Related concepts (the topic's parent + sibling concepts)
   - Domain jargon (the field's term-of-art for the topic)
   - Adjacent technique names (when applicable)

4. Defines INCLUSION criteria:
   - Date range: <years>
   - Languages: English (unless otherwise specified)
   - Publication types (peer-reviewed only? include preprints?)
   - Minimum quality (per source-evaluation rubric)

5. Defines EXCLUSION criteria:
   - Off-topic (operationalize the topic boundary explicitly)
   - Predatory venues (per Beall's List)
   - Retracted papers
   - Editorials / opinion pieces (unless the topic is the discourse itself)

6. Picks the SOURCE PRIORITY ORDER per
   sources/source-priority.md §2 — a list of 3-5 sources to query in
   sequence.

Output as YAML to <working-dir>/search-plan.md:

---
topic: "<the user's topic, slug-form ok>"
domain: "<detected domain>"
date_range: { from: <YYYY>, to: <YYYY> }
languages: ["en"]
target_n: <--n>
quality_floor: <--quality-floor>

primary_terms:
  - 'AND combo: "..." AND "..."'
  - 'AND combo: "..." AND "..."'
  - ...

secondary_terms:
  - "synonym/related/adjacent term combo"
  - "..."

include_publication_types:
  - "journal article"
  - "conference paper"
  - "preprint"   # only if --include-preprints true (default)

exclude_publication_types:
  - "editorial"
  - "letter"
  - "commentary"

source_priority:
  - 1: arxiv          # if domain matches
  - 2: semantic-scholar
  - 3: pubmed         # if biomedical
  - 4: google-scholar # broad fallback
  - 5: crossref       # verification only
---
```

---

## Examples

### Example A — ML / NLP topic

> "Get research papers on prompt-injection attacks in LLM-powered
> agents."

```yaml
topic: "prompt injection attacks in LLM agents"
domain: "CS-security/CS-ML"
date_range: { from: 2022, to: 2024 }
target_n: 15

primary_terms:
  - '"prompt injection" AND ("agent" OR "LLM agent")'
  - '"prompt injection attack" AND "language model"'

secondary_terms:
  - '"adversarial prompt" AND "language model"'
  - '"jailbreak" AND "LLM agent"'
  - '"indirect prompt injection"'
  - '"prompt-based attack"'
  - '"agent hijacking" AND "LLM"'
  - '"tool use vulnerabilities" AND "AI agent"'

source_priority:
  - 1: arxiv
  - 2: semantic-scholar
  - 3: openreview      # for ML conferences
  - 4: google-scholar
```

### Example B — Biomedical topic

> "Find research papers on GLP-1 receptor agonists and weight loss."

```yaml
topic: "GLP-1 receptor agonists for weight loss"
domain: "biomedical"
date_range: { from: 2018, to: 2024 }
target_n: 20

primary_terms:
  - '"GLP-1 receptor agonists"[MeSH] AND ("weight loss"[MeSH] OR "obesity"[MeSH])'
  - '"semaglutide" AND ("weight" OR "obesity")'
  - '"tirzepatide" AND ("weight" OR "obesity")'

secondary_terms:
  - '"GLP-1 agonists" AND "BMI reduction"'
  - '"liraglutide" AND "obesity"'
  - '"incretin mimetics" AND "weight"'
  - '"glucagon-like peptide-1" AND "obesity"'

source_priority:
  - 1: pubmed
  - 2: cochrane     # for systematic reviews
  - 3: semantic-scholar
  - 4: clinicaltrials.gov  # for ongoing trials
```

### Example C — Social science topic

> "Find papers on remote work and team productivity."

```yaml
topic: "remote work and team productivity"
domain: "social-science / management"
date_range: { from: 2020, to: 2024 }   # post-COVID
target_n: 15

primary_terms:
  - '"remote work" AND "team productivity"'
  - '"telework" AND ("productivity" OR "performance")'

secondary_terms:
  - '"work from home" AND "team performance"'
  - '"hybrid work" AND "productivity"'
  - '"distributed teams" AND "collaboration"'
  - '"virtual teams" AND "performance"'

source_priority:
  - 1: google-scholar
  - 2: semantic-scholar
  - 3: ssrn
```

---

## Boolean syntax notes

Different sources use different syntax:

| Source            | AND          | OR           | Phrase           | Field-restrict |
| ----------------- | ------------ | ------------ | ---------------- | -------------- |
| arXiv             | `AND` or `+`  | `OR`         | `%22…%22`        | `ti:`, `au:`, `abs:`, `cat:` |
| Semantic Scholar   | (whitespace)  | (no native OR — run multiple queries and merge) | (whitespace) | `fieldsOfStudy=` |
| Google Scholar     | (whitespace)  | `OR`         | `"…"`            | `intitle:`, `author:`, `source:` |
| PubMed             | `AND`         | `OR`         | `"…"`            | `[MeSH]`, `[Title/Abstract]`, etc. |

The orchestrator translates the canonical search plan into per-source
syntax in the source dispatch phase (`workflows/search.md §2`).

---

## When to ask the user

Ask **once** if any of:

- The topic is ambiguous between two domains (e.g., "neural networks"
  could mean ML or biological neuroscience).
- The topic is too broad for the target N (e.g., "machine learning"
  with `--n 10` — not useful).
- The topic could be interpreted with very different scopes
  (e.g., "obesity" — clinical? metabolic? social?).

Otherwise, proceed with best-guess defaults and surface assumptions in
`search-plan.md → assumptions:` block.

---

## Anti-patterns

- ❌ Single search-term query. Always 2+ primary, 4+ secondary.
- ❌ No year filter (the field gets flooded with old, off-topic
  results).
- ❌ Skipping domain detection (then querying CS-only sources for a
  biomedical topic).
- ❌ Mixing Boolean syntax across sources without translation.
- ❌ Asking the user a clarifying question before doing any work.
  If the request is reasonable, take a swing first.
