# Routing

Decision logic for routing every incoming request to the correct
template, citation style, depth profile, and execution mode.

> **The orchestrator runs this routing step at the very start, before
> any planning or writing happens.**

---

## 1. Detect intent

Match the request against these intent classes (in priority order):

| Intent class               | Triggers                                                            |
| -------------------------- | ------------------------------------------------------------------- |
| `slash-command`             | Message starts with `/research`, `/paper`, `/literature-review`, `/whitepaper`, `/thesis`, `/survey`, `/policy` |
| `format-conversion`         | "format as IEEE / ACM / arXiv / Nature / Harvard"                  |
| `lit-review`                | "literature review", "systematic review", "scoping review", "meta-analysis" |
| `thesis-chapter`            | "thesis chapter", "dissertation chapter"                            |
| `whitepaper`                | "whitepaper", "technical paper", "industry report"                 |
| `survey`                    | "survey paper", "state of the art", "comprehensive review of"       |
| `policy`                    | "policy paper", "policy brief", "regulatory analysis"               |
| `data-analysis-paper`       | "analyze [data] and write", or `.csv`/`.json`/`.xlsx` attached    |
| `general-research-paper`    | "research paper", "scientific paper", "academic paper"              |
| `validation-only`           | "peer review this draft", "validate the methodology"                |

If the request matches more than one class, the highest-priority class
in the table above wins. If unclear, ask **once**.

---

## 2. Pick the format / template

```
intent class             →   default template
------------------------     -----------------------------
slash-command (parsed)        templates/<--format>-paper.md
format-conversion             templates/<requested-format>-paper.md
lit-review                    templates/literature-review.md
thesis-chapter                templates/thesis-chapter.md
whitepaper                    templates/whitepaper.md
survey                        templates/survey-paper.md
policy                        templates/policy-paper.md
data-analysis-paper           templates/<inferred>-paper.md
general-research-paper        infer from topic (see SKILL.md §4)
validation-only               (skip drafting; jump to validators/)
```

If the request is ambiguous between two formats, infer from topic
keywords:

| Topic keyword                                 | Template                       |
| --------------------------------------------- | ------------------------------ |
| ML / AI / NLP / vision / LLM / preprint        | `arxiv-paper.md`               |
| signal / hardware / robotics / antennas        | `ieee-paper.md`                |
| HCI / user study / SIGCHI / SIGGRAPH           | `acm-paper.md`                 |
| biology / medicine / chemistry / clinical      | `nature-paper.md`              |
| business / education / sociology / psychology  | `harvard-paper.md`             |

---

## 3. Pick the citation style

```
domain                     →   default style
-------------------------      -----------------------------
CS / engineering / physics      ieee
ML / AI / preprint              harvard (or apa)
biomedical / Nature             nature
social science / business       harvard
law / history                   chicago-notes
literature review              follow venue
```

User-specified style always wins.

---

## 4. Pick the depth profile

| Signal                                  | Depth          | Output sizing                   |
| --------------------------------------- | -------------- | ------------------------------- |
| `--depth quick` or "short paper"        | quick           | 2–4 pages, 8–12 citations, 1–3 figures |
| Default / unspecified                    | standard        | 5–15 pages, 15–25 citations, 3–6 figures |
| `--depth comprehensive` or "thesis chapter" | comprehensive | 15–40 pages, 30+ citations, 6+ figures |
| Survey / literature review               | comprehensive   | 100–500 references typical        |

---

## 5. Pick the execution mode

| Condition                                    | Mode                              |
| -------------------------------------------- | --------------------------------- |
| Depth = quick                                  | Single orchestrator (sequential)  |
| Depth = standard                                | Single orchestrator (sequential)  |
| Depth = comprehensive AND `agent-spawn` available | Multi-agent fan-out             |
| Depth = comprehensive AND no `agent-spawn`     | Single orchestrator (sequential, multi-file output) |
| Validation-only                                | Direct to `validators/` and `review_pipeline/` |

See `instructions/multi-agent.md` for the multi-agent topology.

---

## 6. Pick the output structure

```
words estimate    →   structure
-----------------     ------------------------------------
< 5,000              single-file (paper-final.md)
5,000 – 15,000        multi-file with sections/, but one paper-final.md
> 15,000             full multi-file per long_context/multi-file-output.md
```

The orchestrator writes the chosen structure to `paper-spec.md → output_structure`.

---

## 7. Pick the language / locale

| Source                                    | Default                         |
| ----------------------------------------- | ------------------------------- |
| User-specified `--language`                | use it                          |
| User wrote in en-GB-flavored prose         | en-GB                           |
| Anything else                              | en-US                           |

Locale affects: spelling, punctuation, "edition" vs. "edn.", quotes
("..." vs. "..."), and date formats.

---

## 8. Detect anonymization needs

Triggers anonymized output:

- `--anonymize true`
- "double-blind submission"
- "submit to NeurIPS / ICML / ICLR / ACL / etc." (most are double-blind)

In anonymized mode:
- Strip author names from the title block.
- Avoid first-person revealing self-citation ("In our prior work [4]…"
  → "Prior work [4]…").
- Replace organization names with placeholders.

---

## 9. Detect data-analysis path

If the user supplied a `.csv`, `.json`, `.xlsx`, or `.parquet` file, OR
the request says "analyze … and write up":

1. Set `data_path` in `paper-spec.md`.
2. Activate the data-analysis pipeline
   (`workflows/data-analysis-pipeline.md`).
3. Add an "Analyst" agent if running multi-agent.
4. Allocate at least 2–3 figures derived from the data.

---

## 10. Detect literature-review path

If the request says "literature review", "systematic review", "scoping
review", "meta-analysis", OR uses the `/literature-review` slash:

1. Use `templates/literature-review.md`.
2. Run `workflows/literature-review.md` instead of `workflows/full-paper.md`.
3. Generate a PRISMA flow diagram (Mermaid) by default.
4. Build a search strategy (search strings, databases, inclusion /
   exclusion).
5. Include a quality-assessment table.
6. Set minimum-citations floor higher (50+ for systematic, 100+ for
   surveys).

---

## 11. Persist the routing decision

Once routed, write the routing decision to
`paper-spec.md → routing_decision`:

```yaml
routing_decision:
  intent: general-research-paper
  template: templates/ieee-paper.md
  citation_style: ieee
  depth: standard
  execution_mode: single-orchestrator
  output_structure: multi-file
  language: en-US
  anonymized: false
  has_data: true
  data_path: ./customer-churn.csv
  is_literature_review: false
  reason: "Topic 'predicting customer churn' + IEEE-style request from user."
```

This makes the choice auditable and debuggable.
