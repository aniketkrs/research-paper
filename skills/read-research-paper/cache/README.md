# Cache Directory

This directory exists at install time as an empty placeholder. It
gets populated as the user fetches papers.

The runtime cache lives at:

```
~/.agents/skills/read-research-paper/cache/
```

(NOT inside the skill's git repo — that would re-clone every install.)

The cache stores:
- `manifest.json` — index of every cached paper.
- `arxiv/<bare-id>.json` — papers fetched from arXiv.
- `doi/<doi-with-slash-replaced>.json` — papers fetched via Crossref.
- `pdf/<sha256>.json` — papers fetched as PDF.
- `url/<sha256>.json` — papers fetched from generic URLs.
- `text/<sha256>.json` — papers parsed from pasted text.
- `topics/<topic-slug>.json` — topic → cached papers index.

Schema: `schemas/visual-paper.json`.

Full protocol: `workflows/caching.md`.

---

## Manual operations

```bash
# Show cache size
du -sh ~/.agents/skills/read-research-paper/cache/

# List cached papers
ls ~/.agents/skills/read-research-paper/cache/arxiv/

# Show stats from the manifest
cat ~/.agents/skills/read-research-paper/cache/manifest.json | jq '.stats'

# Clear the entire cache
rm -rf ~/.agents/skills/read-research-paper/cache/

# Clear a single paper
rm ~/.agents/skills/read-research-paper/cache/arxiv/2403.01234.json
```

The skill never auto-clears the cache.
