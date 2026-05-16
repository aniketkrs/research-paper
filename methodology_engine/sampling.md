# Sampling Strategies Reference

## Purpose
Guide appropriate sampling decisions for different research designs.

---

## Sampling Decision Tree

```
Is the goal to GENERALIZE to a population?
├── YES → Probability sampling
│   ├── Population is homogeneous → Simple random sampling
│   ├── Population has known subgroups → Stratified sampling
│   ├── Population is geographically dispersed → Cluster sampling
│   └── Need systematic coverage → Systematic sampling
│
└── NO → Non-probability sampling
    ├── Need specific characteristics → Purposive sampling
    │   ├── Need diverse perspectives → Maximum variation
    │   ├── Need to confirm theory → Confirming/disconfirming
    │   ├── Hard-to-reach population → Snowball sampling
    │   └── Need information-rich cases → Critical case
    ├── Exploring until patterns emerge → Theoretical sampling
    └── Access-limited → Convenience sampling (acknowledge limitation)
```

---

## Probability Sampling Methods

### Simple Random Sampling
- **When:** Population list available; population relatively homogeneous
- **How:** Assign numbers; use random number generator to select
- **Sample size:** Use power analysis (see below)
- **Report:** "Participants were selected via simple random sampling from [population frame]. Each member had equal probability of selection."

### Stratified Random Sampling
- **When:** Important subgroups exist that must be represented
- **How:** Divide population into strata; random sample within each stratum
- **Types:** Proportional (match population ratios) or disproportional (oversample small groups)
- **Report:** "Stratified random sampling was employed to ensure representation of [strata]. Participants were sampled proportionally/disproportionally within each stratum."

### Cluster Sampling
- **When:** Population is naturally grouped (schools, cities, organizations)
- **How:** Randomly select clusters; sample all (or randomly within) selected clusters
- **Note:** Less precise than simple random; need larger N to compensate
- **Report:** "A two-stage cluster sample was drawn: [N] clusters were randomly selected from [population of clusters], then [method] was used to sample within clusters."

### Systematic Sampling
- **When:** Population list exists; want coverage across the list
- **How:** Calculate interval k = N/n; start at random point; select every kth
- **Caution:** Can introduce bias if list has periodic patterns
- **Report:** "Every [k]th entry was selected from [ordered list], beginning at a randomly determined starting point."

---

## Non-Probability Sampling Methods

### Purposive Sampling
- **When:** Qualitative research; specific perspectives needed
- **Strategies:**
  - **Maximum variation:** Deliberately select diverse cases
  - **Homogeneous:** Select similar cases for focused study
  - **Critical case:** Select cases that are especially informative
  - **Typical case:** Select "average" or "representative" cases
  - **Extreme/deviant case:** Select unusual cases to understand boundaries

### Snowball Sampling
- **When:** Hard-to-reach populations; hidden populations
- **How:** Initial participants recruit others from their network
- **Limitation:** Biased toward socially connected individuals
- **Report:** "Snowball sampling was employed to access [population]. Initial participants (n = [seed]) were identified through [method], who then referred additional participants meeting criteria."

### Theoretical Sampling (Grounded Theory)
- **When:** Building theory; sampling guided by emerging analysis
- **How:** Begin sampling broadly; refine based on codes/categories emerging
- **Stop when:** Theoretical saturation reached (no new concepts emerging)
- **Report:** "Theoretical sampling guided participant selection; sampling continued until theoretical saturation was achieved at interview [N]."

---

## Sample Size Determination

### Quantitative — Power Analysis

```
Parameters needed:
- Significance level (α): typically 0.05
- Power (1 - β): typically 0.80 or 0.90
- Effect size: expected magnitude of difference/relationship
- Number of groups/predictors

COMMON SAMPLE SIZES:
┌──────────────────────────────────────────────────────┐
│ Test              │ Small effect │ Medium │ Large    │
├──────────────────────────────────────────────────────┤
│ t-test (2 groups) │ 394 per grp │ 64/grp │ 26/grp  │
│ ANOVA (3 groups)  │ 322 per grp │ 53/grp │ 22/grp  │
│ Correlation       │ 783 total   │ 85     │ 28      │
│ Regression (5 IV) │ 645 total   │ 92     │ 36      │
│ Chi-square (df=1) │ 785 total   │ 88     │ 26      │
└──────────────────────────────────────────────────────┘
(Based on α = .05, power = .80)

RULE OF THUMB when formal power analysis isn't possible:
- t-test/ANOVA: minimum 30 per group
- Regression: minimum 10-20 observations per predictor
- Factor analysis: minimum 5:1 ratio of subjects to items
- SEM: minimum 200, preferably 10:1 ratio to parameters
```

### Qualitative — Saturation

```
TYPICAL RANGES:
- Phenomenology: 5-25 participants
- Grounded theory: 20-30 participants
- Case study: 1-5 cases (with multiple data sources each)
- Ethnography: 25-50+ participants/informants
- Focus groups: 4-6 groups of 6-10 participants each
- Thematic analysis: 12-30 interviews

SATURATION INDICATORS:
- No new codes emerging from additional interviews
- Categories are well-developed with rich variation
- Relationships between categories are established
- Diminishing returns from additional data

DOCUMENT: "Data saturation was assessed by [method]. No new themes 
emerged after interview [N], with two additional interviews conducted 
to confirm saturation."
```

---

## Reporting Sampling in Methodology

```
MUST INCLUDE:
1. Population definition (who is the population of interest?)
2. Sampling method (how were participants/cases selected?)
3. Sample size (how many? justify adequacy)
4. Inclusion/exclusion criteria (who was eligible? who was not?)
5. Response rate (for surveys: invited vs. completed)
6. Sample characteristics (demographics, relevant features)

GOOD EXAMPLE:
"Participants were recruited from [population] using [method] sampling. 
Inclusion criteria required [criteria]. Exclusion criteria included 
[criteria]. Of [N] invited, [n] completed the study (response rate: X%). 
The final sample comprised [demographics summary]. A power analysis 
(G*Power; α = .05, power = .80, d = 0.50) indicated a minimum sample 
of [N] was required; our sample of [n] exceeded this threshold."
```
