# Bundled Corpus

This directory contains the **shipped fallback layer** for the
`read-research-paper` skill.

When a user requests a paper that:
1. Isn't in their local cache, AND
2. Couldn't be fetched live (no internet, paywall, dead URL),

…the skill checks here BEFORE falling back to model-knowledge. Every
entry is a complete `paper-data.json` record that can be rendered
without any web access.

---

## What's bundled

`anchor-papers.yaml` ships with a small set of **canonical anchor
papers** across major topics — papers so foundational that asking
about their topic should always succeed. As of v1.0.0:

| Topic                            | Anchor paper                                                |
| -------------------------------- | ----------------------------------------------------------- |
| Transformers / attention          | Vaswani et al., "Attention Is All You Need" (2017)           |
| Language model pretraining        | Devlin et al., "BERT" (2018)                                  |
| Retrieval-augmented generation    | Lewis et al., "RAG for Knowledge-Intensive NLP" (2020)         |
| Image recognition / deep CNNs     | He et al., "Deep Residual Learning" (2015)                    |
| GoogLeNet / Inception              | Szegedy et al., "Going Deeper with Convolutions" (2014)       |
| Optimization                       | Kingma & Ba, "Adam" (2014)                                    |
| Contrastive self-supervised        | Chen et al., "SimCLR" (2020)                                  |
| RLHF / instruction tuning           | Ouyang et al., "InstructGPT" (2022)                            |
| Systematic-review methodology       | Page et al., "PRISMA 2020" (BMJ)                               |

---

## How it's used

When the orchestrator hits the corpus tier:

1. Match by `canonical_id` (preferred): if the input is
   `arxiv:1706.03762` and the corpus has that ID, render from corpus.
2. Match by topic: if the user asks "explain transformers" and
   `topics-index.yaml` maps `transformers` to anchor papers, return
   the most relevant one with a flag.
3. Otherwise fall through to model-knowledge.

The rendered output's footer always declares
`source: bundled-corpus` so the user knows the data came from the
shipped corpus, not a live fetch.

---

## Schema

Each entry must include at minimum:

```yaml
- canonical_id: "arxiv:<id>" | "doi:<doi>"
  title: "..."
  authors: [{family: "...", given: "..."}, ...]
  year: <int>
  venue: "..."
  url: "..."
  abstract: "..."   # optional but recommended
  topics: [<list of topic slugs>]
  cache_metadata:
    version: 1
    source: "bundled-corpus"
    skill_version: "1.0.0"
```

For richer rendering (mind maps, infographics, plain-English layers),
also include:

```yaml
  contribution_list: [...]
  limitations: [...]
  headline_numbers: [{value, metric, context, ...}, ...]
  sections: [{id, title, text, ...}, ...]
```

The schema is the same as `cache/<type>/<id>.json` — see
`schemas/visual-paper.json`.

---

## Extending the corpus

### Per-user extension

Drop new YAML files under `corpus/user/`:

```
~/.agents/skills/read-research-paper/corpus/user/
└── my-papers.yaml
```

The skill loads `corpus/user/*.yaml` alongside the bundled corpus.
User entries take **precedence** over bundled entries with the same
`canonical_id` — useful for personal notes / re-renderings.

### Per-project extension

For shared use within a team / project, drop the YAML files into:

```
<project>/.agents/skills/read-research-paper/corpus/
```

The project-level corpus is loaded last; project entries take
precedence over user-level which take precedence over bundled.

Precedence order (highest first):
1. `<project>/.agents/skills/read-research-paper/corpus/`
2. `~/.agents/skills/read-research-paper/corpus/user/`
3. `<skill>/corpus/anchor-papers.yaml` (bundled)

---

## Why a bundled corpus AT ALL?

The user's request was: *"so when ever any other person will ask
about that topic then instead of bluffing it should fetch that data
and show about that topic"*.

That request can be satisfied two ways:

1. **A shared backend service** — Alice's fetched paper helps Bob.
   This is **not how skills work**. Skills run locally on each user's
   machine. There's no shared backend to share into.

2. **A bundled corpus** — every user who installs the skill gets the
   same baseline of high-quality anchor papers. When they ask about
   one of those topics, the skill can answer **even offline**, even
   on first use, without bluffing or making up content.

The bundled corpus is the **honest version** of the user's intent.
It's not infinite — it's curated and shipped via the GitHub repo.
But it's a **real, version-controlled, auditable** baseline that
travels with the skill.

---

## Updating the corpus

The corpus is updated via GitHub releases. To bump:

1. Edit `corpus/anchor-papers.yaml` and `corpus/topics-index.yaml`.
2. Update `corpus/CHANGELOG.md` (this file's section).
3. Bump skill version in `manifest.json`.
4. Tag and release.

Users get the new corpus by re-running:

```
npx skills update read-research-paper
```

---

## Limits of the corpus

The corpus is intentionally small:

- ~10–30 papers across major topics.
- Heavy on foundational / canonical work; light on niche / recent.
- Best-effort metadata (not every entry has full sections).

For broader coverage, the user's local cache fills in over time as
they actually fetch papers. Or they extend the corpus with
`corpus/user/`.

This is the **honest, scalable, local-first** version of "store it in
the mind".
