# Methodology Guide

This file is the canonical guide for selecting, designing, and reporting
research methodology. The skill consults it whenever the user asks for a
"methodology section", "how should I study X?", or "validate this study
design".

> **Golden rule:** the method must follow the research question, not the
> other way around. Pick the question first, then the method that can
> actually answer it.

---

## 1. Choosing a research approach

| Research question type                        | Approach                       | Typical methods                                  |
| ---------------------------------------------- | ------------------------------ | ------------------------------------------------ |
| "How much / how many / how often?"             | **Quantitative**               | Survey, experiment, observational study, modeling |
| "Why / how / what does it mean?"               | **Qualitative**                | Interviews, ethnography, case study, content analysis |
| "What is the state / range of work on X?"      | **Systematic literature review** | PRISMA, scoping review, meta-analysis          |
| "Does X cause Y?"                              | **Experimental / quasi-exp.**   | RCT, A/B test, difference-in-differences, RDD   |
| "Build a thing and show it works"              | **Design science / engineering** | Artifact + benchmark + ablation                |
| "Mix of why + how much"                        | **Mixed methods**              | Sequential explanatory / exploratory / convergent |
| "Synthesize many studies' effects"             | **Meta-analysis**              | Random- / fixed-effects models, forest plot     |
| "Theory-build from cases"                      | **Grounded theory / multi-case** | Open / axial / selective coding                |
| "Forecast a future trend"                      | **Modeling / simulation**       | ARIMA, agent-based, system dynamics             |
| "Compare two systems / algorithms"             | **Benchmarking**               | Controlled benchmark suites + statistical tests |

If the user request is ambiguous, the skill MUST ask one clarifying question
about the *type of question* before designing the method.

---

## 2. Quantitative method blueprint

A quantitative methodology section must specify:

1. **Research design** — descriptive / correlational / quasi-experimental /
   experimental.
2. **Population and sampling**
   - Target population
   - Sampling frame
   - Sampling method (random / stratified / cluster / convenience — declare!)
   - Sample size with **a priori power analysis**
     (target power ≥ 0.80, α = 0.05; report effect size assumption)
3. **Variables**
   - Independent / Dependent / Control / Mediator / Moderator
   - Operational definitions and units
4. **Instruments / measures**
   - Validated scales (cite Cronbach's α, CFA results)
   - Or constructed measures (justify, pilot, report reliability)
5. **Procedure** — chronological steps, IRB approval if humans involved.
6. **Data analysis plan** — pre-registered if possible
   - Descriptive statistics
   - Assumption checks (normality, homoscedasticity, independence,
     multicollinearity)
   - Inferential tests (with α-level and corrections for multiple comparisons)
   - Effect size reporting (Cohen's d, η², r, OR)
   - Sensitivity / robustness checks
7. **Ethics** — consent, anonymization, data security, IRB number.

---

## 3. Qualitative method blueprint

A qualitative methodology section must specify:

1. **Paradigm / epistemology** — interpretivist / constructivist / critical /
   pragmatist.
2. **Methodological tradition** — phenomenology / ethnography / grounded theory
   / case study / narrative / discourse analysis.
3. **Researcher positionality** — who you are, your relationship to the
   subject, biases acknowledged.
4. **Sampling** — purposive / theoretical / snowball; saturation criterion.
5. **Data collection**
   - Interview protocol (semi-structured / unstructured)
   - Observation protocol
   - Document corpus
   - Length, frequency, recording, transcription
6. **Data analysis**
   - Coding scheme (open / axial / selective for grounded theory)
   - Software (NVivo, Atlas.ti, Dedoose) — or hand coding
   - Inter-rater reliability (Cohen's κ ≥ 0.7) if multiple coders
7. **Trustworthiness** (Lincoln & Guba, 1985):
   - Credibility (member checks, triangulation)
   - Transferability (thick description)
   - Dependability (audit trail)
   - Confirmability (reflexive journal)
8. **Ethics** — informed consent, anonymization, sensitive topics protocol.

---

## 4. Mixed-methods blueprint

Specify the **design type** explicitly:

| Design                       | When to use                                 | Sequence            |
| ---------------------------- | ------------------------------------------- | ------------------- |
| Convergent parallel           | Triangulate findings on the same question  | QUAL + QUAN simultaneous, then merge |
| Sequential explanatory        | Quantitative results need qualitative explanation | QUAN → QUAL  |
| Sequential exploratory        | Build a quantitative instrument from qualitative findings | QUAL → QUAN |
| Embedded                      | One method supports the other              | One inside the other |

Then specify each strand's design per §2 / §3 above, plus the **integration
strategy** (joint display table, narrative weaving, transformation).

---

## 5. Systematic literature review (SLR) blueprint

Follow **PRISMA 2020** for systematic reviews.

1. **Protocol** — register on PROSPERO / OSF before searching when feasible.
2. **Research questions** — phrased PICO (Population, Intervention,
   Comparator, Outcome) or SPIDER for qualitative.
3. **Search strategy**
   - Databases (Scopus, Web of Science, IEEE Xplore, ACM DL, arXiv,
     PubMed, Google Scholar — list all)
   - Search string (Boolean) — list verbatim
   - Date range
   - Language filter
4. **Inclusion / exclusion criteria** — explicit, in a table.
5. **Screening**
   - Title/abstract screening (two reviewers, conflicts resolved)
   - Full-text screening
   - Inter-rater agreement (κ)
6. **Quality assessment** — CASP / MMAT / AMSTAR / custom rubric.
7. **Data extraction** — standardized form (publish in appendix).
8. **Synthesis**
   - Narrative
   - Thematic
   - Meta-analytic (if comparable effect sizes)
9. **PRISMA flow diagram** — REQUIRED.

The skill renders the PRISMA flow as a Mermaid diagram by default; see
`workflows/visual-generation-pipeline.md`.

---

## 6. Experimental / RCT blueprint

CONSORT-style reporting:

1. **Study design** — parallel / crossover / factorial; randomization unit.
2. **Participants / units** — eligibility, recruitment, setting.
3. **Interventions** — exact protocol (replicable).
4. **Outcomes** — primary, secondary; pre-specified.
5. **Sample size** — power calculation.
6. **Randomization** — sequence generation, allocation concealment.
7. **Blinding** — who is blinded.
8. **Statistical methods** — primary analysis pre-specified.
9. **Threats to validity** — internal, external, construct, conclusion.

---

## 7. Design science / engineering blueprint

For papers that *build* something (algorithm, system, framework):

1. **Problem statement** — what is broken in the world.
2. **Requirements** — functional and non-functional.
3. **Design** — architecture diagram, key design decisions with trade-offs.
4. **Implementation** — stack, key components, repository.
5. **Evaluation strategy**
   - **Performance benchmarks** vs. baselines (be honest about which baselines)
   - **Ablation studies** — remove each component and re-measure
   - **Case study / user study** if the artifact is human-facing
   - **Comparison to state of the art** with a clear table
6. **Threats to validity** — construct, internal, external, conclusion.
7. **Reproducibility** — link to code, data, environment file (Dockerfile,
   conda env, exact seeds), checkpoint hashes.

---

## 8. Survey research blueprint

1. **Survey design** — cross-sectional / longitudinal / panel.
2. **Instrument design**
   - Question wording (avoid double-barreled, leading)
   - Scale (Likert anchors, neutral midpoint decision)
   - Order randomization
   - Attention checks
3. **Pilot study** — n ≥ 10–20, refine.
4. **Sampling and recruitment** — Prolific / MTurk / panel / convenience —
   declare and justify.
5. **Response quality controls** — speeders, straight-liners, attention
   failures.
6. **Sample size** — consider effect size + complexity of model (e.g., 10
   responses per parameter for SEM).
7. **Analysis** — descriptive, factor structure (EFA/CFA), regression / SEM.
8. **Limitations** — self-report bias, social desirability, non-response.

---

## 9. Modeling / simulation blueprint

1. **Model purpose** — what question does the model answer.
2. **Model type** — analytical / agent-based / discrete-event / system
   dynamics / Monte Carlo / DES.
3. **Conceptual model** — diagram of agents/state/flow.
4. **Parameters** — sources, values, ranges, distributions.
5. **Validation**
   - Face validity (expert review)
   - Internal validity (extreme-condition tests, dimensional consistency)
   - External validity (compare against real-world data)
6. **Sensitivity analysis** — one-at-a-time and global (Sobol).
7. **Uncertainty quantification** — Monte Carlo runs with confidence
   intervals.
8. **Reproducibility** — seeds, code, parameter files.

---

## 10. Hypothesis structure (when relevant)

State each hypothesis as:

> **H1:** [Direction] [IV] [verb] [DV] when [condition].
>
> Example: "H1: Increased model size positively affects benchmark accuracy
> on reasoning tasks when training compute is held constant."

Then for each hypothesis, list:
- The **rationale** (1–2 sentences with citations)
- The **operationalization** (how it will be tested)
- The **expected effect size** (small / medium / large with citation)
- The **statistical test** that will be used

---

## 11. Validity threats checklist

Run this at the end of every methodology section:

- [ ] **Internal validity** — could something other than the IV explain the
  result? (history, maturation, selection, regression to mean, instrumentation)
- [ ] **External validity** — does the result generalize? (population,
  setting, time)
- [ ] **Construct validity** — do the measures capture the constructs?
  (mono-operation, mono-method, social desirability)
- [ ] **Conclusion validity** — are the statistical conclusions sound?
  (low power, fishing, violated assumptions, error rates)
- [ ] **Ecological validity** (HCI / field studies) — does the setting reflect
  real use?
- [ ] **Researcher bias** — confirmation bias, expectancy effects, allegiance
  effects.

For software-engineering papers, use Wohlin et al.'s four threat categories
(construct, internal, external, conclusion).

---

## 12. Reproducibility requirements

The skill enforces a **Reproducibility statement** in every paper. Minimum:

| Item                              | Required                              |
| --------------------------------- | ------------------------------------- |
| Code repository                   | URL with tag/commit hash              |
| Data                              | URL or "available on request" with reason |
| Environment                       | requirements.txt / Dockerfile / conda env |
| Random seeds                      | Listed                                |
| Hardware                          | CPU/GPU model, RAM                    |
| Wall-clock runtime                | Per-experiment estimate               |
| Hyperparameters                   | Exact final values                    |
| Hyperparameter search budget      | Number of trials, search space        |
| Model checkpoints                 | URL or hash                           |

A paper without these answers gets a `[REPRODUCIBILITY GAP]` warning.

---

## 13. Ethics requirements

For research involving humans, animals, sensitive data, or high-stakes
deployment:

- IRB / ethics committee approval reference
- Informed consent procedure
- Anonymization / pseudonymization
- Data retention and destruction
- Compensation (if any)
- Harms analysis (especially for AI / ML papers — see NeurIPS Broader Impacts)
- Conflicts of interest

---

## 14. Common methodological errors the skill must catch

- HARKing (Hypothesizing After Results are Known) — separate hypotheses from
  exploratory analyses.
- p-hacking — pre-register or report all tests run.
- Over-fitting to a benchmark — hold out a final test set.
- Cherry-picked baselines — compare against the strongest available.
- Conflating correlation with causation — flag whenever a causal claim lacks
  experimental or quasi-experimental design.
- Self-selection bias in surveys — declare and discuss.
- Unsupported generalization — check sample → population logic.
- Ignored confounds — list at least three plausible alternatives in the
  Discussion.

If the skill detects any of these in a draft, surface them in the review pass.
