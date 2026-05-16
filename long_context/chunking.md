# Chunking Protocol

How to split work into chunks small enough to fit in working memory
without losing coherence.

---

## 1. Chunk types

| Chunk type     | Granularity                  | Working-memory cost   |
| -------------- | ---------------------------- | --------------------- |
| Paper          | Whole paper                  | High                  |
| Section         | One numbered section         | Medium                |
| Subsection      | One H3-level subsection      | Small                 |
| Paragraph       | One paragraph                | Tiny                  |
| Citation        | One bibliography entry       | Tiny                  |
| Figure / table  | One figure / one table        | Small                 |
| Hypothesis test  | One statistical test         | Small                 |

The skill operates at **section-level granularity** by default and
drops to **subsection-level** when a section approaches 2,000 words.

---

## 2. Section-level chunking

For each section in the outline:

1. Read the section's row in `outline.md`.
2. Read the relevant slot from `templates/<format>.md`.
3. Read the previous adjacent section's draft (for transition).
4. Load only the bibliography entries used in this section.
5. Load only the figures-plan entries that appear in this section.
6. Draft.
7. Write to `sections/<NN>-<name>.md`.
8. Discard.

---

## 3. Subsection-level chunking

When a section is forecast to exceed 2,000 words:

1. Subdivide the section into subsections in `outline.md`.
2. Each subsection becomes its own draft step.
3. Persist subsection drafts to
   `sections/<NN>-<name>/<NNN>-<sub>.md`.
4. After all subsections are drafted, concatenate (in order) into
   `sections/<NN>-<name>.md` and discard the per-subsection files.

---

## 4. Paragraph-level chunking

Rarely needed. Use only when:

- A specific paragraph requires very heavy citation density (10+
  citations) and the bibliography load is large.
- A specific paragraph is mathematically dense and the equations
  require careful working memory.

Otherwise paragraph-level is overkill and breaks narrative flow.

---

## 5. Bibliography chunking

The bibliography is loaded **per-section**:

1. Read `outline.md` to find the cite_keys planned for this section.
2. Load only those entries from `bibliography.yaml`.
3. After section drafting, discard.

The full bibliography is loaded only by the citation pipeline at the
end (one read, one write).

---

## 6. Multi-file citation database

If the bibliography exceeds 100 entries, split it:

```
bibliography/
├── theme-1.yaml
├── theme-2.yaml
├── theme-3.yaml
└── index.yaml        ← maps cite_keys to theme files
```

Loading is then:

1. Read `bibliography/index.yaml` (small).
2. For each cite_key needed, look up its theme file.
3. Load only the theme files containing this section's cite_keys.

The format-bibliography toolchain auto-detects this layout.

---

## 7. Figure / table chunking

Figures and tables are referenced by ID, not by content. The drafter
sees only:

```yaml
- id: figure-3
  number: 3
  type: bar
  caption: "Mean accuracy by model size on three benchmarks (n = 5 seeds)."
```

…and references it as "(Figure 3)" or "As shown in Figure 3, …". The
actual rendered file lives in `figures/figure-3.png` and is not loaded
into the drafter's working memory.

---

## 8. Cross-section consistency

To preserve coherence across chunks:

1. Every chunk reads `paper-spec.md` and `outline.md` (cheap).
2. Every chunk reads the previous adjacent chunk's output.
3. The final consistency pass (one cover-to-cover read) catches what
   the chunking missed.

Do NOT try to maintain consistency by holding all sections in memory.
That defeats the purpose of chunking.

---

## 9. When chunking fails

If a section cannot be drafted in one chunk even after subsection
splitting:

1. Revisit the outline — the section is probably trying to do too much.
2. Split it into two sections.
3. Update `outline.md` and re-route.

This is almost always the right answer for sections > 4,000 words.

---

## 10. Tracking chunk completion

The orchestrator maintains a chunk-completion register in `index.md`:

```yaml
sections:
  - id: "01-introduction"
    status: complete
    word_count: 1240
    cite_keys_used: [smith2023, doe2022, lee2021]
  - id: "02-related-work"
    status: complete
    word_count: 2150
    cite_keys_used: [...]
  - id: "03-methodology"
    status: in-progress
  ...
```

This makes resumption trivial after a crash.
