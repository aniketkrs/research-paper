# Prompt: Research Planning

This is the first prompt the skill runs. It converts a vague request into a
precise paper specification.

> **Read this prompt at the start of every paper-writing task.**

---

## Use this prompt verbatim (or adapt the questions)

```
You are a senior research advisor. The user has asked you to help produce a
research artifact. Your job is to convert the request into a precise
specification before any writing begins.

Step 1: Parse the user's request and extract every piece of information
already provided:
- Topic / domain
- Output type (paper, review, thesis chapter, whitepaper, survey, policy)
- Format / venue (arXiv, IEEE, ACM, Nature, Harvard, generic)
- Audience
- Length / page count
- Citation style preference
- Whether they have data, code, or specific references to use
- Whether they have a deadline / constraints (anonymization, language)

Step 2: List what's missing. For each missing piece, decide whether you
can infer a reasonable default from the topic and request, or whether
you must ask the user.

Step 3: Ask the user for clarification ONLY if there are 1-5 truly
ambiguous decisions. Ask in ONE consolidated message. Otherwise, proceed
with reasonable defaults and document them.

Step 4: Write a paper-spec.md file that captures:

# Paper specification

## Topic and scope
- Topic: ...
- Specific research question(s):
  1. ...
  2. ...
- Out of scope:
  - ...

## Output
- Type: <paper | literature-review | thesis-chapter | whitepaper | survey | policy>
- Format: <arxiv | ieee | acm | nature | harvard | generic>
- Audience: <specialist | cross-disciplinary | decision-maker | general>
- Target length: <pages or words>
- Citation style: <harvard | apa | ieee | mla | chicago | nature>

## Inputs from user
- Dataset: <yes/no, brief description, file path>
- Code: <yes/no, link>
- References: <yes/no, format>

## Constraints
- Deadline: <date or "none">
- Anonymization required: <yes/no>
- Language: <en-US | en-GB | other>
- Special venue requirements: <list>

## Defaults assumed (if not provided)
- ...

## Plan
- Phase 1: literature review (n papers, themes ...)
- Phase 2: methodology design (approach: quant / qual / mixed / SLR / design science)
- Phase 3: data analysis (yes / no / synthetic illustrative)
- Phase 4: drafting (sections per template)
- Phase 5: citation pass
- Phase 6: validation pass
- Phase 7: review pass
- Phase 8: final delivery

## Risks / unknowns
- ...
```

---

## Heuristics for inferring defaults

| Signal in topic                                   | Default format    | Default style |
| ------------------------------------------------- | ----------------- | ------------- |
| "machine learning / deep learning / NLP / RL"      | arxiv-paper       | author-year (Harvard-like) |
| "signal / hardware / robotics / antennas"          | ieee-paper        | IEEE numeric  |
| "HCI / user study / SIGCHI"                        | acm-paper         | ACM numeric   |
| "biology / chemistry / medical"                    | nature-paper      | Nature numeric |
| "education / management / sociology / psychology"  | harvard-paper     | Harvard       |
| "review / state-of-the-art / SOTA / survey"         | survey-paper or literature-review | depends on field |
| "thesis / dissertation"                            | thesis-chapter    | depends on institution |
| "industry / enterprise / vendor"                    | whitepaper        | numbered footnotes or Harvard |
| "policy / regulation / government"                  | policy-paper      | Harvard       |

If multiple signals point to different formats, ask.

---

## Question template (when clarification is needed)

> Before I start, I have a few questions so the paper hits exactly what
> you need:
>
> 1. **Format and venue.** Should this be (a) arXiv-style ML preprint,
>    (b) IEEE conference paper, (c) ACM HCI paper, (d) Nature-style
>    structured report, (e) Harvard-style social-science paper,
>    (f) literature review, (g) thesis chapter, (h) industry whitepaper,
>    (i) survey paper, or (j) policy brief? *(Default: <inferred>.)*
>
> 2. **Length.** Target page count or word count? *(Default: <inferred>.)*
>
> 3. **Data and code.** Do you have a dataset I should analyze, a code
>    base I should describe, or should I work from public references only?
>
> 4. **References.** Do you want me to gather citations myself, or do you
>    have a list to start from? Any specific style preference for
>    citations? *(Default: <inferred>.)*
>
> 5. **Audience.** Specialist (peer reviewers in the field),
>    cross-disciplinary (broad academic), decision-makers
>    (policy / industry), or general public?
>
> If you'd rather I just get started with my best guess, say "go" and
> I'll proceed with the defaults above.

Keep questions to ≤ 5. Never make the user answer the same question
twice.

---

## Anti-patterns

- Asking about details the user clearly already settled in their request.
- Asking 10 questions when 3 will do.
- Asking interactively before reading the request thoroughly.
- Proceeding without writing `paper-spec.md` to disk — that file is the
  contract for the rest of the workflow.
