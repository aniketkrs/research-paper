# Methodology Validator

## Purpose
Ensure the methodology section is rigorous, appropriate, and reproducible.

---

## Validation Checks

### Check 1: Methodology-Question Alignment

```
FOR EACH research question:
  1. What type of answer does this question require?
     - Descriptive → descriptive methods appropriate?
     - Explanatory → experimental/quasi-experimental appropriate?
     - Exploratory → qualitative methods appropriate?
     - Comparative → comparison design appropriate?
  
  2. Does the methodology ACTUALLY answer the question?
     - Data collected is relevant to the question?
     - Analysis method produces the type of answer needed?
     - Sample/scope is appropriate for the question's generality?

  FLAG if:
  - Question asks "why" but methodology is purely quantitative
  - Question asks about causation but design is correlational
  - Question is about a population but sample is non-representative
  - Question is about change over time but design is cross-sectional
```

### Check 2: Internal Validity

```
ASSESS threats to internal validity:

□ History: Could external events explain results?
□ Maturation: Could natural change explain results?
□ Testing: Could repeated testing affect results?
□ Instrumentation: Could measurement changes explain results?
□ Regression to mean: Were extreme groups selected?
□ Selection: Are groups comparable at baseline?
□ Attrition: Is dropout non-random?
□ Diffusion: Could treatment leak between groups?

FOR EACH identified threat:
- Is it acknowledged in the paper?
- Is a mitigation strategy described?
- Could it realistically explain the findings?

FLAG: Unacknowledged threats that could plausibly explain results.
```

### Check 3: Statistical Appropriateness

```
FOR EACH statistical test used:

1. Is the test appropriate for the data type?
   - Continuous DV → parametric (or non-parametric if assumptions violated)
   - Categorical DV → chi-square family or logistic regression
   - Count DV → Poisson/negative binomial
   
2. Are assumptions met (or acknowledged)?
   - Normality tested and reported?
   - Homogeneity of variance tested?
   - Independence justified by design?
   - Sample size adequate for the test?

3. Is the test powerful enough?
   - Sample size supports detection of meaningful effects?
   - Multiple comparisons corrected?
   - Effect sizes reported alongside p-values?

FLAG:
- Parametric tests on clearly non-normal data without justification
- No assumption testing reported
- Sample size insufficient for chosen analysis
- Multiple comparisons without correction
- Absence of effect size measures
```

### Check 4: Reproducibility

```
Could another researcher replicate this study from the methodology section alone?

CHECK:
□ Data source clearly identified with access instructions
□ Time period specified
□ Inclusion/exclusion criteria stated
□ Sampling method described step-by-step
□ Instruments described or referenced (with version)
□ Analysis steps enumerated
□ Software and versions named
□ Parameters/settings specified
□ Random seeds reported (if applicable)
□ Decision rules for ambiguous cases documented

MISSING INFORMATION flagged as:
- Critical (replication impossible without this)
- Important (replication difficult without this)
- Minor (would improve precision of replication)
```

### Check 5: Ethical Compliance

```
IF human subjects involved:
□ Ethics approval mentioned (IRB/ethics committee)
□ Informed consent process described
□ Right to withdraw noted
□ Data anonymization/pseudonymization described
□ Data storage and security addressed
□ Vulnerable populations: additional protections noted
□ Incentives disclosed (if any)
□ Deception: justification and debriefing described (if any)

IF secondary data:
□ Original ethics approval scope covers this use
□ Data use agreement/license mentioned
□ No re-identification risk from analysis

IF computational/AI research:
□ Bias considerations acknowledged
□ Potential harms discussed
□ Data provenance documented
□ Consent for data use verified
```

### Check 6: Limitations Honesty

```
ASSESS the limitations section:

□ At least 3 limitations acknowledged
□ Limitations are GENUINE (not trivial "sample could be larger")
□ Each limitation notes potential impact on findings
□ Limitations are connected to methodology choices
□ No limitation completely invalidates the findings (if it does, the study shouldn't proceed)
□ Mitigation strategies mentioned where possible
□ Limitations inform future research suggestions

FLAG:
- No limitations section (unacceptable in academic work)
- Only trivial limitations ("more research needed")
- Limitations that actually invalidate the findings
- Contradictions between claims and acknowledged limitations
```

---

## Validation Output Format

```markdown
## Methodology Validation Report

### Alignment Score: [1-5]
[Research questions appropriately matched to methods: Yes/Partial/No]

### Rigor Score: [1-5]
[Statistical/analytical approach appropriate and complete: assessment]

### Reproducibility Score: [1-5]  
[Could be replicated from description alone: assessment]

### Issues
| # | Severity | Category | Issue | Recommendation |
|---|----------|----------|-------|---------------|
| 1 | Critical | Alignment | [description] | [fix] |
| 2 | Important | Validity | [description] | [fix] |
| 3 | Minor | Reproducibility | [description] | [fix] |

### Overall Assessment
[1-2 sentence summary of methodology quality and key improvements needed]
```
