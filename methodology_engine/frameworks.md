# Research Methodology Frameworks

## Purpose
Provide structured methodology selection and design for different research paradigms.

---

## Framework Selection Decision Tree

```
START: What is the research objective?

├─ EXPLORE (understand a phenomenon)
│  ├─ Little existing theory → Grounded Theory
│  ├─ Understand lived experience → Phenomenology
│  ├─ Understand culture/group → Ethnography
│  ├─ Understand a bounded system → Case Study
│  └─ Understand a process → Narrative Research
│
├─ DESCRIBE (characterize a phenomenon)
│  ├─ Population characteristics → Survey Research
│  ├─ Current state → Cross-sectional Study
│  ├─ Change over time → Longitudinal Study
│  └─ Content analysis → Content/Discourse Analysis
│
├─ EXPLAIN (test hypotheses)
│  ├─ Causal relationship → Experimental Design
│  │  ├─ Full control → True Experiment (RCT)
│  │  ├─ Partial control → Quasi-experimental
│  │  └─ No control → Pre-experimental
│  ├─ Relationships between variables → Correlational
│  └─ Prediction → Regression/ML models
│
├─ EVALUATE (assess effectiveness)
│  ├─ Program/intervention → Program Evaluation
│  ├─ Usability/design → Design Research
│  └─ Policy → Policy Analysis
│
└─ SYNTHESIZE (aggregate knowledge)
   ├─ Quantitative synthesis → Meta-analysis
   ├─ Qualitative synthesis → Meta-synthesis
   ├─ Comprehensive overview → Systematic Review
   └─ Scope mapping → Scoping Review
```

---

## Quantitative Research Framework

```
1. POSITIVIST PARADIGM
   Ontology: Objective reality exists
   Epistemology: Knowledge through measurement
   Methodology: Hypothesis testing, statistical analysis

2. DESIGN TYPES:
   ┌─────────────────────────────────────────────────────┐
   │ Experimental                                         │
   │ • True experiment (random assignment)                │
   │ • Quasi-experiment (non-random groups)               │
   │ • Pre-experimental (no control group)                │
   ├─────────────────────────────────────────────────────┤
   │ Non-experimental                                     │
   │ • Correlational (relationships)                      │
   │ • Causal-comparative (group differences)             │
   │ • Descriptive (current state)                        │
   │ • Longitudinal (change over time)                    │
   │ • Cross-sectional (snapshot)                         │
   └─────────────────────────────────────────────────────┘

3. DATA COLLECTION:
   • Surveys (Likert, multiple choice, ranking)
   • Tests and assessments
   • Physiological measures
   • Behavioral observation (structured)
   • Secondary datasets
   • Sensor/log data

4. SAMPLING:
   • Probability: simple random, stratified, cluster, systematic
   • Power analysis for sample size determination
   • Minimum n varies by analysis (rule of thumb: 30+ per group)

5. ANALYSIS PROGRESSION:
   Descriptive → Assumption testing → Inferential → Effect sizes → Post-hoc
```

---

## Qualitative Research Framework

```
1. INTERPRETIVIST PARADIGM
   Ontology: Multiple constructed realities
   Epistemology: Knowledge through understanding meaning
   Methodology: Interpretation, thick description

2. APPROACHES:
   ┌─────────────────────────────────────────────────────┐
   │ Grounded Theory                                      │
   │ • Goal: Generate theory from data                    │
   │ • Process: Open → Axial → Selective coding           │
   │ • Output: Substantive theory                         │
   ├─────────────────────────────────────────────────────┤
   │ Phenomenology                                        │
   │ • Goal: Understand lived experience                  │
   │ • Process: Bracketing → Description → Essence        │
   │ • Output: Essence of experience                      │
   ├─────────────────────────────────────────────────────┤
   │ Case Study                                           │
   │ • Goal: Deep understanding of bounded system         │
   │ • Process: Context → Description → Themes            │
   │ • Output: Rich description + cross-case patterns     │
   ├─────────────────────────────────────────────────────┤
   │ Ethnography                                          │
   │ • Goal: Understand cultural group                    │
   │ • Process: Immersion → Observation → Interpretation  │
   │ • Output: Cultural description                       │
   ├─────────────────────────────────────────────────────┤
   │ Narrative Research                                    │
   │ • Goal: Understand experience through stories        │
   │ • Process: Collection → Restorying → Themes          │
   │ • Output: Narrative account                          │
   └─────────────────────────────────────────────────────┘

3. DATA COLLECTION:
   • In-depth interviews (semi-structured, unstructured)
   • Focus groups
   • Participant observation
   • Document analysis
   • Visual methods (photo elicitation, video)
   • Diaries/journals

4. SAMPLING:
   • Purposive (criterion, maximum variation, snowball, theoretical)
   • Data saturation as endpoint (typically 12-30 interviews)

5. ANALYSIS:
   • Thematic analysis (Braun & Clarke)
   • Content analysis
   • Discourse analysis
   • Narrative analysis
   • Framework analysis
```

---

## Mixed Methods Framework

```
1. PRAGMATIST PARADIGM
   Ontology: Whatever works for the research question
   Epistemology: Multiple ways of knowing
   Methodology: Combine quantitative and qualitative

2. DESIGNS:
   ┌─────────────────────────────────────────────────────┐
   │ Convergent (parallel)                                │
   │ QUAN + QUAL → Compare/Merge → Interpretation         │
   │ • Both collected simultaneously                      │
   │ • Equal priority                                     │
   │ • Integration at interpretation stage                │
   ├─────────────────────────────────────────────────────┤
   │ Explanatory Sequential                               │
   │ QUAN → qual → Interpretation                         │
   │ • Quantitative first (dominant)                      │
   │ • Qualitative explains quantitative results          │
   │ • Sequential timing                                  │
   ├─────────────────────────────────────────────────────┤
   │ Exploratory Sequential                               │
   │ QUAL → quan → Interpretation                         │
   │ • Qualitative first (builds instrument)              │
   │ • Quantitative tests/generalizes qual findings       │
   │ • Sequential timing                                  │
   ├─────────────────────────────────────────────────────┤
   │ Embedded                                             │
   │ QUAN(qual) or QUAL(quan)                             │
   │ • One approach nested within the other               │
   │ • Secondary approach addresses different question    │
   └─────────────────────────────────────────────────────┘

3. INTEGRATION STRATEGIES:
   • Merging (compare/contrast results)
   • Connecting (one informs the next)
   • Embedding (one supports the other)
   • Joint display tables (qual and quan side by side)
```

---

## Systematic Review Framework (PRISMA)

```
1. PROTOCOL:
   • Register protocol (PROSPERO or OSF)
   • Define PICO(S): Population, Intervention, Comparison, Outcome, Study design

2. SEARCH:
   • Minimum 3 databases
   • Documented search strings
   • Date restrictions justified
   • Grey literature included (if applicable)
   • Reference list checking (snowballing)

3. SCREENING:
   • Title/abstract screening (2 reviewers independently)
   • Full-text screening (2 reviewers)
   • Disagreement resolution protocol
   • PRISMA flow diagram documenting process

4. QUALITY ASSESSMENT:
   • Tool selection: CASP, Newcastle-Ottawa, Cochrane RoB, GRADE
   • Independent assessment by 2 reviewers
   • Quality score does not exclude but contextualizes

5. DATA EXTRACTION:
   • Standardized form
   • Pilot tested on 3-5 papers
   • Double extraction on subset for reliability

6. SYNTHESIS:
   • Narrative synthesis (thematic)
   • Meta-analysis (if homogeneous enough)
   • Sensitivity analysis
   • Subgroup analysis
   • Publication bias assessment (funnel plot)

7. REPORTING:
   • PRISMA checklist completed
   • Protocol deviations documented
   • Strength of evidence rated (GRADE)
```

---

## Data Science / Computational Research Framework

```
1. PROBLEM DEFINITION:
   • Clear prediction/classification/clustering objective
   • Success metric defined before analysis
   • Baseline established

2. DATA:
   • Source documentation
   • Preprocessing pipeline documented
   • Train/validation/test split defined
   • Data leakage prevention measures

3. METHODOLOGY:
   • Algorithm selection justified
   • Hyperparameter search strategy documented
   • Cross-validation scheme defined
   • Feature engineering explained

4. EVALUATION:
   • Multiple metrics reported
   • Comparison with baselines
   • Statistical significance of differences
   • Ablation study (component contribution)
   • Error analysis

5. REPRODUCIBILITY:
   • Random seeds set and reported
   • Environment/version documented
   • Code availability
   • Data availability or generation script
```
