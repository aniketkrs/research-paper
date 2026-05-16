# Cache Protocol

How `read-research-paper` persists fetched papers locally so the same
paper isn't re-fetched, and so re-asks are instant.

> **Honest framing:** the cache is **per-installation**. Alice's cache
> doesn't help Bob unless they share the cache directory manually.
> There's no shared backend. Anything claiming otherwise would be a
> lie.

---

## 1. Location

The cache lives at:

```
~/.agents/skills/read-research-paper/cache/
```

(Override with `--cache-dir <path>` or env `READ_PAPER_CACHE_DIR`.)

Inside:

```
cache/
├── manifest.json                  # index of every cached paper
├── arxiv/
│   ├── 2403.01234.json
│   ├── 2005.11401.json
│   └── ...
├── doi/
│   ├── 10.1145_3589334.json       # `/` replaced with `_`
│   └── ...
├── url/
│   ├── <sha256-hash>.json
│   └── ...
├── text/
│   ├── <sha256-hash>.json
│   └── ...
└── topics/
    ├── retrieval-augmented-generation.json
    ├── graph-neural-networks.json
    └── ...
```

Each paper file is the canonical `paper-data.json` per
`schemas/visual-paper.json`.

---

## 2. The `manifest.json` index

Top-level cache index:

```json
{
  "version": 1,
  "skill_version": "1.0.0",
  "papers": [
    {
      "canonical_id": "arxiv:2403.01234",
      "title": "...",
      "authors": ["..."],
      "year": 2024,
      "fetched_at": "2024-05-12T10:00:00Z",
      "source": "live-fetch",
      "topics": ["retrieval-augmented-generation", "code-review"],
      "file": "arxiv/2403.01234.json",
      "size_bytes": 23541
    },
    ...
  ],
  "stats": {
    "total_papers": 47,
    "total_size_kb": 1240,
    "last_updated": "2024-05-12T10:00:00Z"
  }
}
```

Updated every time a paper is added, refreshed, or removed.

---

## 3. Cache lookup

When a paper is requested:

```
1. Compute the canonical ID from the input.
2. Check cache/<type>/<id>.json:
   - exists? → load and return (skip live fetch entirely).
   - missing? → continue to live fetch.
3. After successful live fetch, write to cache.
4. Update manifest.json.
```

For URL inputs without an arXiv ID or DOI, hash the URL with SHA-256
and store under `cache/url/<hash>.json`. Different URLs → different
hashes → different cache entries.

---

## 4. Topic indexing

The cache also indexes papers by inferred topic. When a paper is
cached, the orchestrator:

1. Extracts 3–5 topic keywords from the title + abstract.
2. Slugifies (lowercase, hyphenated).
3. Updates `cache/topics/<slug>.json`:

```json
{
  "topic": "retrieval-augmented-generation",
  "papers": [
    {"canonical_id": "arxiv:2005.11401", "title": "...", "year": 2020},
    {"canonical_id": "arxiv:2403.01234", "title": "...", "year": 2024},
    ...
  ],
  "last_updated": "2024-05-12T10:00:00Z"
}
```

When the user asks about a topic (rather than a specific paper), the
topic index is consulted **before** any live search:

> User: "explain the latest paper on retrieval-augmented generation"
>
> Skill:
> 1. Check cache/topics/retrieval-augmented-generation.json.
> 2. If found, the most recent cached paper is returned.
> 3. If not, fall through to live fetch.

This is how the cache gets richer over time per user.

---

## 5. Cache freshness

By default, papers don't expire — they're immutable artifacts.

Override:

| Flag                  | Effect                                              |
| --------------------- | --------------------------------------------------- |
| `--cache true` (default) | Use cache if present                               |
| `--cache false`        | Skip cache; force a fresh fetch                     |
| `--refresh`            | Force a re-fetch and overwrite the cached version    |
| `--no-cache`           | Skip cache AND don't write to it                     |

For arXiv preprints that get versioned: the cache stores the bare ID
without the version suffix. To pin a version, include it in the input:
`arxiv:2403.01234v2`.

---

## 6. Cache management commands

The skill exposes (via the orchestrator, not separate slash commands):

```
# List cached papers
ls ~/.agents/skills/read-research-paper/cache/arxiv/

# Show cache stats
cat ~/.agents/skills/read-research-paper/cache/manifest.json | jq '.stats'

# Clear entire cache
rm -rf ~/.agents/skills/read-research-paper/cache/

# Clear single paper
rm ~/.agents/skills/read-research-paper/cache/arxiv/2403.01234.json
```

The skill does NOT auto-clear the cache. Manual control only.

---

## 7. Cache vs. corpus (NOT the same thing)

| Concept | Lives in | Source | Updated by |
|---|---|---|---|
| **Cache** | `~/.agents/skills/.../cache/` | User's own fetches | Skill writes after every successful fetch |
| **Corpus** | `<skill>/corpus/anchor-papers.yaml` | Bundled with the skill | `git pull` updates / new releases |

The corpus is the **read-only** baseline. The cache is the **write-able**
layer that grows as the user uses the skill.

---

## 8. Privacy

The cache is **local to the user's machine**. It does not phone home,
does not sync, does not share with other users.

If the user wants to share their cache with a collaborator:

```bash
# Copy
cp -r ~/.agents/skills/read-research-paper/cache/ ./shared-cache/

# Send to collaborator
scp -r ./shared-cache/ user@host:~/.agents/skills/read-research-paper/cache/
```

This is a **manual** operation, never automatic.

---

## 9. Cache integrity

Each cached paper file includes a `cache_metadata` block:

```json
{
  "canonical_id": "arxiv:2403.01234",
  "title": "...",
  ...
  "cache_metadata": {
    "version": 1,
    "fetched_at": "2024-05-12T10:00:00Z",
    "source": "live-fetch",
    "skill_version": "1.0.0",
    "verification_trail": {
      "doi_resolves": true,
      "crossref_match": true,
      "retraction_check": "clean",
      "checked_at": "2024-05-12T10:00:01Z"
    },
    "etag_or_hash": "sha256:..."
  }
}
```

This makes the cache auditable.

---

## 10. Resilience

If the cache directory is corrupted (e.g., a partial write):

1. The skill detects malformed JSON and skips the entry.
2. It re-fetches the paper.
3. It overwrites the corrupted file with the fresh fetch.

If `manifest.json` itself is corrupted:

1. The skill rebuilds it by scanning `cache/<type>/*.json`.
2. Logs the rebuild in `Known-gaps.md`.

The cache is robust to crashes.

---

## 11. Why this matters

Without a cache, every re-ask would re-fetch — wasted bandwidth,
slow rendering, possibly hitting rate limits. With it:

- Re-asking the same paper is **instant** (< 1 second).
- Asking a topic the user has read before falls into the topic
  index — also instant.
- The skill works **offline** for any paper the user has previously
  fetched.

This is the "store it in the mind" pattern, **honestly scoped** to
the user's own machine.
