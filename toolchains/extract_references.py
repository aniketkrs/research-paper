#!/usr/bin/env python3
"""
extract_references.py
=====================

Reads a paper (Markdown or LaTeX) and the bibliography. Cross-checks:
  - Cite keys used in the paper that are missing from the bibliography
  - Bibliography entries never cited in the paper (orphans)
  - Optionally, exports a clean cite-key list that can be diffed across
    drafts to track what was added / removed.

Usage:
  python extract_references.py paper-cited.md --bib bibliography.yaml \\
         --report validation/orphan-and-missing.md
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any


def load_bib(path: str) -> list[dict[str, Any]]:
    try:
        import yaml  # type: ignore
        with open(path, "r", encoding="utf-8-sig") as f:
            data = yaml.safe_load(f)
        if isinstance(data, dict) and "references" in data:
            data = data["references"]
        return data if isinstance(data, list) else []
    except ImportError:
        if path.endswith(".json"):
            with open(path, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        sys.stderr.write("Install pyyaml or use a JSON bibliography.\n")
        return []


CITE_KEY = re.compile(r"\[([a-z][a-z0-9_;\s\-,]*)\]", re.IGNORECASE)


def cite_block(s: str) -> bool:
    parts = [p.strip() for p in re.split(r"[;,]", s)]
    return all(re.match(r"^[a-z0-9_\-]+$", p, re.IGNORECASE) for p in parts) and bool(parts)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("paper")
    p.add_argument("--bib", required=True)
    p.add_argument("--report", default=None)
    p.add_argument("--export-keys", default=None,
                   help="Write the cited-keys list to this path.")
    args = p.parse_args(argv)

    with open(args.paper, "r", encoding="utf-8-sig") as f:
        text = f.read()
    bib = load_bib(args.bib)
    by_key = {e.get("id"): e for e in bib if e.get("id")}

    cited: list[str] = []
    seen: set[str] = set()
    for m in CITE_KEY.finditer(text):
        inside = m.group(1)
        if not cite_block(inside):
            continue
        for k in re.split(r"[;,]\s*", inside):
            k = k.strip()
            if k and k not in seen:
                seen.add(k)
                cited.append(k)

    missing = [k for k in cited if k not in by_key]
    orphan = sorted(set(by_key) - set(cited))

    md = ["# Reference cross-check\n",
          f"- Paper: `{args.paper}`",
          f"- Bibliography: `{args.bib}`",
          f"- Cited keys: {len(cited)}",
          f"- Bibliography entries: {len(by_key)}",
          f"- Missing keys (cited but not in bib): {len(missing)}",
          f"- Orphan entries (in bib but never cited): {len(orphan)}\n"]

    if missing:
        md.append("## Missing keys\n")
        for k in missing:
            md.append(f"- `{k}`")
        md.append("")

    if orphan:
        md.append("## Orphan entries\n")
        for k in orphan:
            e = by_key[k]
            md.append(f"- `{k}` — {e.get('title', '')[:80]}")
        md.append("")

    body = "\n".join(md) + "\n"
    if args.report:
        os.makedirs(os.path.dirname(args.report) or ".", exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(body)
    else:
        sys.stdout.write(body)

    if args.export_keys:
        with open(args.export_keys, "w", encoding="utf-8") as f:
            for k in cited:
                f.write(k + "\n")

    return 2 if missing else 0


if __name__ == "__main__":
    raise SystemExit(main())
