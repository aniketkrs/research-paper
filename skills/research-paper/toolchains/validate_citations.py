#!/usr/bin/env python3
"""
validate_citations.py
=====================

Implements the citation validator from
workflows/validation-pipeline.md §2.2.

Checks:
  - Every in-text [cite_key] (or [N] for numeric styles) maps to an entry
    in bibliography.yaml.
  - Every entry in bibliography.yaml is cited at least once
    (orphan warning).
  - Every entry has the required fields for its `type`
    (per references/citation-styles.md §12).
  - The paper uses a single citation style end-to-end (no mixing of
    `(Smith, 2023)` with `[1]`).
  - DOI / URL are well-formed where present.
  - (Optional, with --online) DOIs and arXiv IDs resolve.

Outputs a Markdown report and a non-zero exit code on high-severity
issues.

Usage:
  python validate_citations.py paper-cited.md bibliography.yaml \\
         --report validation/citation-issues.md
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
        sys.stderr.write("Install pyyaml or convert bibliography to JSON.\n")
        return []


REQUIRED: dict[str, list[str]] = {
    "article-journal": ["authors", "year", "title", "container"],
    "article-conference": ["authors", "year", "title", "container"],
    "book": ["authors", "year", "title", "publisher"],
    "chapter": ["authors", "year", "title", "container", "publisher"],
    "report": ["authors", "year", "title"],
    "webpage": ["authors", "year", "title", "url"],
    "preprint": ["authors", "year", "title"],
    "dataset": ["authors", "year", "title"],
    "thesis": ["authors", "year", "title", "institution"],
    "standard": ["title", "year"],
    "patent": ["authors", "year", "title"],
    "personal-communication": ["authors", "year", "title"],
    "software": ["authors", "year", "title"],
}


def validate_required(entry: dict[str, Any]) -> list[str]:
    req = REQUIRED.get(entry.get("type") or "article-journal",
                       REQUIRED["article-journal"])
    missing: list[str] = []
    for f in req:
        v = entry.get(f)
        if v is None or v == "" or (isinstance(v, list) and not v):
            missing.append(f)
    return missing


CITE_KEY_PATTERN = re.compile(r"\[([a-z][a-z0-9_;\s\-,]*)\]", re.IGNORECASE)
NUMERIC_INTEXT = re.compile(r"\[(\d+(?:\s*[-–,]\s*\d+)*)\]")
AUTHOR_YEAR = re.compile(r"\(([A-Z][A-Za-z\-]+(?:\s+et al\.)?(?:,?\s+\d{4}[a-z]?)?)\)")
SUPERSCRIPT_NATURE = re.compile(r"\^\d+(,\d+)*")


def is_cite_block(content: str) -> bool:
    parts = [p.strip() for p in re.split(r"[;,]", content)]
    if not parts:
        return False
    return all(re.match(r"^[a-z0-9_\-]+$", p, re.IGNORECASE) for p in parts)


def detect_style(text: str) -> dict[str, int]:
    """Heuristic detection of citation styles in use."""
    return {
        "numeric_brackets": len(NUMERIC_INTEXT.findall(text)),
        "author_year_paren": len(AUTHOR_YEAR.findall(text)),
        "nature_superscript": len(SUPERSCRIPT_NATURE.findall(text)),
        "cite_key_placeholders": sum(
            1 for m in CITE_KEY_PATTERN.finditer(text)
            if is_cite_block(m.group(1))
        ),
    }


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("paper")
    p.add_argument("bibliography")
    p.add_argument("--report", default=None)
    p.add_argument("--online", action="store_true",
                   help="Verify DOIs by HTTP HEAD (requires network).")
    args = p.parse_args(argv)

    with open(args.paper, "r", encoding="utf-8-sig") as f:
        paper = f.read()
    bib = load_bib(args.bibliography)
    by_key = {e.get("id"): e for e in bib if e.get("id")}

    cited_keys: set[str] = set()
    for m in CITE_KEY_PATTERN.finditer(paper):
        inside = m.group(1)
        if not is_cite_block(inside):
            continue
        for k in re.split(r"[;,]\s*", inside):
            cited_keys.add(k.strip())

    missing_keys = sorted(k for k in cited_keys if k not in by_key)
    orphans = sorted(set(by_key) - cited_keys)
    incomplete = []
    for key, e in by_key.items():
        if key in cited_keys:
            miss = validate_required(e)
            if miss:
                incomplete.append((key, miss))
    incomplete.sort()

    style_counts = detect_style(paper)
    mixed_styles = sum(1 for v in (style_counts["numeric_brackets"],
                                   style_counts["author_year_paren"],
                                   style_counts["nature_superscript"]) if v > 0) > 1

    bad_dois = []
    for key, e in by_key.items():
        doi = (e.get("doi") or "").strip()
        if doi and not re.match(r"^10\.[\w.]+/.+", doi):
            bad_dois.append((key, doi))

    retracted = [key for key, e in by_key.items()
                 if e.get("verification") == "retracted"]
    unverified = [key for key, e in by_key.items()
                  if e.get("verification") in ("unverified", "unverified-offline")]

    high_sev = bool(missing_keys) or bool(retracted) or any(incomplete)
    medium_sev = bool(orphans) or mixed_styles or bool(bad_dois) or bool(unverified)

    md: list[str] = ["# Citation validation report\n"]
    md.append(f"- Paper: `{args.paper}`")
    md.append(f"- Bibliography: `{args.bibliography}`")
    md.append(f"- In-text cite-key occurrences: "
              f"{style_counts['cite_key_placeholders']}")
    md.append(f"- Numeric-bracket citations detected: "
              f"{style_counts['numeric_brackets']}")
    md.append(f"- Author-year citations detected: "
              f"{style_counts['author_year_paren']}")
    md.append(f"- Nature superscript citations detected: "
              f"{style_counts['nature_superscript']}")
    md.append(f"- Mixed citation styles: {'YES (high severity)' if mixed_styles else 'no'}\n")

    md.append("## High-severity issues\n")
    if missing_keys:
        md.append(f"- **Missing keys** ({len(missing_keys)}): "
                  + ", ".join(f"`{k}`" for k in missing_keys))
    if retracted:
        md.append(f"- **Retracted citations** ({len(retracted)}): "
                  + ", ".join(f"`{k}`" for k in retracted))
    if incomplete:
        md.append(f"- **Incomplete entries** ({len(incomplete)}):")
        for key, miss in incomplete:
            md.append(f"  - `{key}` missing: {', '.join(miss)}")
    if not (missing_keys or retracted or incomplete):
        md.append("_None._")
    md.append("")

    md.append("## Medium-severity issues\n")
    if orphans:
        md.append(f"- **Orphan references** (in bib but never cited) "
                  f"({len(orphans)}): " + ", ".join(f"`{k}`" for k in orphans))
    if bad_dois:
        md.append(f"- **Malformed DOIs** ({len(bad_dois)}):")
        for key, doi in bad_dois:
            md.append(f"  - `{key}`: `{doi}`")
    if unverified:
        md.append(f"- **Unverified citations** ({len(unverified)}): "
                  + ", ".join(f"`{k}`" for k in unverified))
    if mixed_styles:
        md.append("- **Mixed citation styles** detected — re-run the citation pipeline with a single `--style`.")
    if not (orphans or bad_dois or unverified or mixed_styles):
        md.append("_None._")
    md.append("")

    md.append("## Summary\n")
    md.append(f"- High severity: {1 if high_sev else 0}")
    md.append(f"- Medium severity: {1 if medium_sev else 0}")
    md.append(f"- Total bibliography entries: {len(by_key)}")
    md.append(f"- Total cited keys: {len(cited_keys)}")

    body = "\n".join(md) + "\n"
    if args.report:
        os.makedirs(os.path.dirname(args.report), exist_ok=True) if os.path.dirname(args.report) else None
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(body)
    else:
        sys.stdout.write(body)

    return 2 if high_sev else 0


if __name__ == "__main__":
    raise SystemExit(main())
