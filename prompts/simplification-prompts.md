# Prompt: Simplification (Plain-English Summary)

The skill always produces dual-register output: rigorous in the body, plain
in summaries. This prompt generates the plain-English summary that appears
at the end of the abstract or as a subsection of the introduction /
conclusion (per `templates/<format>.md`).

> **The test:** an intelligent layperson with no field training should be
> able to read this and (a) understand what the paper is about, (b) walk
> away with the right intuition about the result.

---

## The prompt

```
Write a plain-English summary of the research paper described in the
following inputs:

- Title and abstract
- Introduction's contribution paragraph
- Headline result from the Results section
- One-line implication from the Discussion

Constraints:

1. 5-10 sentences total. NEVER more than 12.
2. Reading level: high-school graduate (Flesch-Kincaid grade <= 10).
3. NO jargon without immediate definition.
   Bad: "We use a transformer-based encoder."
   Good: "We use a kind of neural network called a 'transformer' that
         is good at finding patterns in long sequences of words or numbers."
4. Use ANALOGIES for hard concepts. Compare to everyday things.
5. Active voice. Short sentences. Concrete nouns.
6. Tell a STORY:
   - 1-2 sentences: what problem does the paper try to solve?
   - 1-2 sentences: what did the researchers do?
   - 1-2 sentences: what did they find? (with a number)
   - 1-2 sentences: why does it matter?
7. NO citations. NO acronyms (or define them in-line). NO equations.
8. NEVER overclaim. The plain-English summary must NOT make stronger
   claims than the technical body.

Examples of good summaries:

Example 1 (ML paper on fraud detection):
> Banks lose billions every year to fraudulent transactions. Spotting
> fraud is hard because criminals constantly invent new tricks, and the
> patterns change faster than rule-based systems can keep up. We trained
> a kind of computer model called a "graph neural network" - which is
> good at finding patterns in networks of connections - to look at how
> money moves between accounts. On a dataset of 4 million transactions,
> our model caught 23% more fraud than the previous best system, while
> raising 18% fewer false alarms. This means banks can stop more fraud
> without annoying their honest customers. The model also explains its
> decisions, so a fraud analyst can quickly check why a transaction was
> flagged.

Example 2 (medical paper on drug interaction):
> Patients with diabetes often take many medications at once, and some
> combinations can interact in dangerous ways. Until now, doctors have
> relied mostly on lists of known dangerous combinations - but these lists
> miss interactions that have not been studied yet. We built a method
> that predicts new dangerous combinations by looking at the chemical
> structures of drugs and how they affect cells in the body. In a test on
> 12,400 drug pairs, our method correctly flagged 87% of the truly
> dangerous combinations, including 14 that had never been reported
> before but were later confirmed by clinical records. This could help
> pharmacists catch unsafe combinations earlier, especially for patients
> taking new drugs.

Example 3 (policy paper on housing affordability):
> Many large cities have a housing affordability crisis: salaries have
> risen slowly while rents have doubled. Two of the most-debated policies
> to fix this are rent control and increasing housing supply. We compared
> what happened in 24 cities that tried each policy between 2010 and
> 2022. Cities that increased housing supply saw rents stabilize within
> 5 years, with the strongest effects for low-income renters. Cities that
> used rent control kept current renters in their homes but had less new
> housing built and longer waiting lists for new tenants. The two
> policies are not opposites - they target different problems. Our
> analysis suggests that the best results came from cities that combined
> targeted rent stabilization for vulnerable renters with broad
> permissions for new construction.

Output the summary as a single paragraph (or two short paragraphs if
needed for clarity). Place it at the location specified by the chosen
template (templates/<format>.md).

Then run a self-check:
- Word count: 100-250 words.
- Sentences: 5-12.
- Longest sentence: <= 25 words.
- Acronyms: 0 (or each defined inline).
- Numbers: at least 1 (the headline result).
- Reading level: aim for Flesch-Kincaid <= 10. If your draft is higher,
  rewrite shorter / simpler.
- Story arc: problem -> approach -> finding -> implication.
- Consistency: do the numbers and claims match the technical body?
```

---

## Common failure modes

- **Too technical.** Even the "simple" version uses field-specific jargon.
  Force yourself to translate every technical term. If you can't, you
  haven't simplified it.
- **Too vague.** "We made things better" is not a finding. Always include
  the headline number.
- **Marketing tone.** "Revolutionary breakthrough" is wrong here too.
  Restraint reads as competence to general audiences.
- **Burying the contribution.** A reader who quits after sentence 3
  should still know roughly what the paper does.
- **Inconsistency with the body.** If the body says "improves accuracy by
  4 percentage points", the summary cannot say "doubles accuracy".

---

## When the user asks for an "executive summary" instead

For whitepapers, theses, policy papers, the "executive summary" is
similar in spirit but:

- Longer (200-500 words).
- Includes a recommendation or a call to action.
- May use 3-5 short bullet points for the key messages.
- Targeted at decision-makers, not general public.

Use the same prompt with these adjustments:
- Increase sentence allowance to 15-25.
- Add 3-5 bullet "Key messages" before the prose.
- Add a final 1-sentence call to action.
- Reading level can rise to grade 12 (still well below technical body).
