# Prompt: Methodology Design

Used in `workflows/research-orchestration.md §4 Methodology`.

---

## Step 1 — Match question to method

```
Read paper-spec.md. Classify the primary research question type:

- HOW_MUCH       → quantitative
- WHY_HOW         → qualitative
- WHAT_STATE_OF_FIELD → systematic literature review
- DOES_X_CAUSE_Y   → experimental / quasi-experimental
- BUILD_AND_SHOW   → design science
- MIX_OF_WHY_AND_HOW_MUCH → mixed methods
- SYNTHESIZE_EFFECTS → meta-analysis
- THEORY_BUILD_FROM_CASES → grounded theory / multi-case
- FORECAST          → modeling / simulation
- COMPARE_SYSTEMS   → benchmarking

Justify the classification in 2-3 sentences. If multiple types fit,
declare a primary and a secondary method.

Then read references/methodology-guide.md and pick the matching
blueprint section.
```

---

## Step 2 — Fill the blueprint

For each blueprint, fill every required field. Below are templates per
question type.

### Quantitative

```
1. Research design: <descriptive | correlational | quasi-experimental | experimental>
2. Population: ...
3. Sampling frame: ...
4. Sampling method: <random | stratified | cluster | convenience>; justify.
5. Sample size: n = ...; a priori power analysis showing power=0.80, alpha=0.05,
   expected effect size = ... (cite source for effect size assumption).
6. Variables:
   - IV: ...
   - DV: ...
   - Controls: ...
   - Mediators / moderators: ...
7. Instruments: ... (Cronbach's alpha, CFA fit indices)
8. Procedure: ...
9. Data analysis plan:
   - Descriptive stats
   - Assumption checks: ...
   - Inferential test: ... (with multiple-comparison correction)
   - Effect size + 95% CI
   - Sensitivity analyses: ...
10. Ethics: IRB approval ref, consent, anonymization, data retention.
```

### Qualitative

```
1. Paradigm: <interpretivist | constructivist | critical | pragmatist>
2. Methodological tradition: <phenomenology | ethnography | grounded theory |
   case study | narrative | discourse analysis>
3. Researcher positionality: ...
4. Sampling: <purposive | theoretical | snowball>; saturation criterion.
5. Data collection: ... (interview / observation / document protocols)
6. Analysis: coding scheme; software; inter-rater reliability if multi-coder.
7. Trustworthiness: credibility, transferability, dependability,
   confirmability — methods for each (Lincoln & Guba 1985).
8. Ethics: consent, anonymization, sensitive-topic handling.
```

### Mixed methods

```
1. Design: <convergent parallel | sequential explanatory | sequential exploratory | embedded>
2. QUAN strand: full quantitative blueprint (above).
3. QUAL strand: full qualitative blueprint (above).
4. Integration strategy: <joint display | narrative weaving | data transformation>.
5. Why mixed: what does each strand contribute that the other can't?
```

### Systematic literature review (PRISMA)

```
1. Protocol registration: <PROSPERO | OSF | none, justify>
2. RQs (PICO / SPIDER format)
3. Search strategy:
   - Databases (>= 3)
   - Boolean search string per database
   - Date range
   - Languages
4. Inclusion / exclusion criteria (table)
5. Screening: dual reviewer, kappa target.
6. Quality assessment: <CASP | JBI | MMAT | AMSTAR-2 | custom>
7. Data extraction form (publish in appendix)
8. Synthesis: <narrative | thematic | meta-analytic>
9. PRISMA flow diagram (rendered as Mermaid)
```

### Experimental / RCT (CONSORT)

```
1. Design: <parallel | crossover | factorial>
2. Participants: eligibility, recruitment, setting, n per arm.
3. Interventions: detailed protocol.
4. Outcomes: primary + secondary (pre-specified).
5. Sample size: power calculation.
6. Randomization: sequence generation, allocation concealment.
7. Blinding: who is blinded.
8. Statistical methods: pre-specified primary analysis.
9. Threats to validity: internal / external / construct / conclusion.
```

### Design science / engineering

```
1. Problem statement: what is broken
2. Requirements: functional + non-functional
3. Design: architecture diagram, key decisions w/ trade-offs.
4. Implementation: stack, key components, repo URL.
5. Evaluation:
   - Performance benchmarks (>= 3 baselines, including SOTA)
   - Ablation study (each component removed)
   - User study or case study (if human-facing)
   - Comparison table to SOTA
6. Threats to validity.
7. Reproducibility: code + data + env file + seeds + hardware.
```

### Modeling / simulation

```
1. Purpose: what question.
2. Model type: <analytical | agent-based | discrete-event | system dynamics |
   Monte Carlo>.
3. Conceptual model: diagram of agents/state/flow.
4. Parameters: source, value, range, distribution.
5. Validation: face / internal / external validity.
6. Sensitivity analysis: one-at-a-time + Sobol.
7. Uncertainty quantification: Monte Carlo runs with CIs.
8. Reproducibility: seeds, code, parameter file.
```

---

## Step 3 — Threats-to-validity sweep

```
After drafting the methodology, run the validity-threats checklist
(references/methodology-guide.md §11):

- Internal validity: ...
- External validity: ...
- Construct validity: ...
- Conclusion validity: ...
- Ecological validity: ...
- Researcher bias: ...

For each, write 1-2 sentences acknowledging the threat and describing
the mitigation. Place these in a "Threats to validity" subsection at the
end of the methodology.
```

---

## Step 4 — Reproducibility statement

```
Add a Reproducibility statement covering:

| Item                | Required               |
| ------------------- | ---------------------- |
| Code repo            | URL + commit hash      |
| Data                 | URL or "on request"    |
| Environment          | requirements / Docker  |
| Random seeds         | List                   |
| Hardware             | CPU/GPU/RAM            |
| Wall-clock runtime    | Per experiment         |
| Hyperparameters       | Final values           |
| HP search budget      | Trials, search space   |
| Model checkpoints     | URL or hash            |

If any item is unknown, mark as "TBD" and surface in Known gaps.
```

---

## Step 5 — Output

Write `methodology.md` with the filled blueprint. The drafting phase
(`workflows/research-orchestration.md §7`) will pull this file into the
relevant section of the paper.

---

## Common pitfalls to avoid

- HARKing: don't write hypotheses post-hoc.
- p-hacking: list every test you ran, not just the significant ones.
- Underpowered: report power and acknowledge if n is below floor.
- Cherry-picked baselines: include the strongest available, not just easy ones.
- Causal language without causal design: don't say "X causes Y" from
  observational data.
- Sample of one: any "case study" with n = 1 must be framed as
  illustrative, not generalizable.
