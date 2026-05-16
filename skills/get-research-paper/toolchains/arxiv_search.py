#!/usr/bin/env python3
"""
arxiv_search.py
===============

Direct arXiv API search for the get-research-paper skill.

Queries the public arXiv export API and returns parsed candidate
papers in the canonical schema (`schemas/paper-result.json`).
Implements polite ~3s delays per arXiv's rate-limit policy.

Designed for graceful degradation:
  - Works with `feedparser` if installed (best parsing).
  - Falls back to stdlib `xml.etree` if not.
  - Falls back to `requests` if installed; uses stdlib `urllib` if not.

Usage:
  python arxiv_search.py --query "graph neural network fraud detection" \\
                          --max-results 30 \\
                          --year-from 2020 \\
                          --year-to 2024 \\
                          --out candidates.json

  python arxiv_search.py --self-test
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

ARXIV_API = "https://export.arxiv.org/api/query"
USER_AGENT = "research-paper-skill/1.0 (https://github.com/aniketkrs/research-paper)"


# ---------------------------------------------------------------------------
# Optional imports
# ---------------------------------------------------------------------------
def _try_imports():
    try:
        import feedparser  # type: ignore
    except ImportError:
        feedparser = None
    try:
        import requests  # type: ignore
    except ImportError:
        requests = None
    return feedparser, requests


# ---------------------------------------------------------------------------
# HTTP fetch with polite delay
# ---------------------------------------------------------------------------
_LAST_REQUEST_TIME = [0.0]


def fetch(url: str, timeout: int = 30, requests_lib=None) -> str:
    """Fetch URL with polite 3-second pacing between calls to arXiv."""
    elapsed = time.time() - _LAST_REQUEST_TIME[0]
    if elapsed < 3.0:
        time.sleep(3.0 - elapsed)
    _LAST_REQUEST_TIME[0] = time.time()

    if requests_lib is not None:
        resp = requests_lib.get(
            url, timeout=timeout,
            headers={"User-Agent": USER_AGENT}
        )
        resp.raise_for_status()
        return resp.text

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8")


# ---------------------------------------------------------------------------
# Query construction
# ---------------------------------------------------------------------------
def build_search_query(query: str,
                       categories: list[str] | None = None,
                       phrase: bool = True) -> str:
    """Build an arXiv search_query string."""
    parts: list[str] = []

    # Use 'all:' field for broad matching, with quoted phrases.
    q = query.strip()
    if phrase and " " in q and not (q.startswith('"') and q.endswith('"')):
        # Wrap multi-word query in quotes for exact-phrase matching.
        parts.append(f'all:"{q}"')
    else:
        parts.append(f"all:{q}")

    if categories:
        cat_clause = " OR ".join(f"cat:{c}" for c in categories)
        parts.append(f"({cat_clause})")

    return " AND ".join(parts)


def build_url(search_query: str,
              max_results: int = 30,
              start: int = 0,
              sort_by: str = "relevance",
              sort_order: str = "descending") -> str:
    params = {
        "search_query": search_query,
        "start": str(start),
        "max_results": str(max_results),
        "sortBy": sort_by,
        "sortOrder": sort_order,
    }
    return f"{ARXIV_API}?{urllib.parse.urlencode(params)}"


# ---------------------------------------------------------------------------
# Parsers
# ---------------------------------------------------------------------------
def parse_with_feedparser(xml: str) -> list[dict[str, Any]]:
    import feedparser  # type: ignore
    feed = feedparser.parse(xml)
    out: list[dict[str, Any]] = []
    for entry in feed.entries:
        # arxiv id like "http://arxiv.org/abs/2403.01234v2"
        full_id = entry.id
        m = re.search(r"abs/([\d\.]+v?\d*)$", full_id)
        arxiv_id = m.group(1) if m else full_id
        # Drop version suffix for canonical id; keep full version optional
        bare_id = re.sub(r"v\d+$", "", arxiv_id)

        authors = []
        for a in entry.get("authors", []):
            name = a.get("name", "").strip()
            family, given = split_name(name)
            authors.append({"family": family, "given": given})

        published = entry.get("published", "")
        year = int(published[:4]) if published[:4].isdigit() else None

        primary_category = ""
        if "tags" in entry and entry.tags:
            primary_category = entry.tags[0].get("term", "")

        doi = ""
        journal_ref = ""
        for k, v in entry.items():
            if k.endswith("doi"):
                doi = v
            if k.endswith("journal_ref"):
                journal_ref = v

        out.append({
            "arxiv_id": bare_id,
            "arxiv_id_versioned": arxiv_id,
            "title": entry.title.strip().replace("\n", " "),
            "authors": authors,
            "year": year,
            "summary": entry.get("summary", "").strip(),
            "primary_category": primary_category,
            "doi": doi,
            "journal_ref": journal_ref,
            "url": full_id,
            "published": published,
            "updated": entry.get("updated", ""),
        })
    return out


def parse_with_etree(xml: str) -> list[dict[str, Any]]:
    """Stdlib XML parser fallback when feedparser is unavailable."""
    import xml.etree.ElementTree as ET
    ns = {
        "atom": "http://www.w3.org/2005/Atom",
        "arxiv": "http://arxiv.org/schemas/atom",
    }
    root = ET.fromstring(xml)
    out = []
    for entry in root.findall("atom:entry", ns):
        full_id = (entry.findtext("atom:id", default="", namespaces=ns) or "").strip()
        m = re.search(r"abs/([\d\.]+v?\d*)$", full_id)
        arxiv_id = m.group(1) if m else full_id
        bare_id = re.sub(r"v\d+$", "", arxiv_id)

        title = (entry.findtext("atom:title", default="", namespaces=ns) or "").strip().replace("\n", " ")
        summary = (entry.findtext("atom:summary", default="", namespaces=ns) or "").strip()
        published = (entry.findtext("atom:published", default="", namespaces=ns) or "").strip()
        updated = (entry.findtext("atom:updated", default="", namespaces=ns) or "").strip()
        year = int(published[:4]) if published[:4].isdigit() else None

        authors = []
        for au in entry.findall("atom:author", ns):
            name = (au.findtext("atom:name", default="", namespaces=ns) or "").strip()
            family, given = split_name(name)
            authors.append({"family": family, "given": given})

        primary_category = ""
        pc = entry.find("arxiv:primary_category", ns)
        if pc is not None:
            primary_category = pc.attrib.get("term", "")

        doi_el = entry.find("arxiv:doi", ns)
        doi = (doi_el.text if doi_el is not None else "") or ""
        jr_el = entry.find("arxiv:journal_ref", ns)
        journal_ref = (jr_el.text if jr_el is not None else "") or ""

        out.append({
            "arxiv_id": bare_id,
            "arxiv_id_versioned": arxiv_id,
            "title": title,
            "authors": authors,
            "year": year,
            "summary": summary,
            "primary_category": primary_category,
            "doi": doi,
            "journal_ref": journal_ref,
            "url": full_id,
            "published": published,
            "updated": updated,
        })
    return out


def split_name(full_name: str) -> tuple[str, str]:
    """Split 'Jane A. Smith' -> ('Smith', 'Jane A.'). Robust to edge cases."""
    name = full_name.strip()
    if not name:
        return ("", "")
    if "," in name:
        # already in 'Family, Given' form
        family, _, given = name.partition(",")
        return (family.strip(), given.strip())
    parts = name.split()
    if len(parts) == 1:
        return (parts[0], "")
    return (parts[-1], " ".join(parts[:-1]))


# ---------------------------------------------------------------------------
# Filter and rank
# ---------------------------------------------------------------------------
def filter_year(entries: list[dict[str, Any]],
                year_from: int | None,
                year_to: int | None) -> list[dict[str, Any]]:
    out = []
    for e in entries:
        y = e.get("year")
        if y is None:
            continue
        if year_from and y < year_from:
            continue
        if year_to and y > year_to:
            continue
        out.append(e)
    return out


def to_canonical(e: dict[str, Any], rank: int, query: str) -> dict[str, Any]:
    """Convert raw arXiv entry into the canonical schema."""
    authors = e.get("authors", [])
    family = authors[0]["family"].lower() if authors else "unknown"
    family = re.sub(r"[^a-z0-9]+", "", family) or "unknown"
    title_word = re.split(r"[\s\-:;]+", e.get("title", ""))[0]
    title_word = re.sub(r"[^a-zA-Z0-9]+", "", title_word).lower() or "paper"
    cite_key = f"{family}_{e.get('year', 0)}_{title_word[:12]}"

    return {
        "id": cite_key,
        "type": "preprint" if not e.get("journal_ref") else "article-journal",
        "authors": authors,
        "year": e.get("year"),
        "title": e.get("title", ""),
        "container": e.get("journal_ref") or "arXiv",
        "doi": e.get("doi", ""),
        "arxiv_id": e.get("arxiv_id", ""),
        "url": e.get("url", ""),
        "discovery": {
            "source": "arxiv",
            "search_query": query,
            "rank": rank,
            "tldr": e.get("summary", "")[:300],
        },
        "summary": e.get("summary", "").strip(),
        "verification": "verified",
        "verification_trail": {
            "arxiv_confirmed": True,
            "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
        },
    }


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------
def search(query: str,
           max_results: int = 30,
           year_from: int | None = None,
           year_to: int | None = None,
           categories: list[str] | None = None) -> list[dict[str, Any]]:
    feedparser, requests_lib = _try_imports()
    sq = build_search_query(query, categories=categories, phrase=True)
    url = build_url(sq, max_results=max_results)

    xml = fetch(url, requests_lib=requests_lib)

    if feedparser is not None:
        raw = parse_with_feedparser(xml)
    else:
        raw = parse_with_etree(xml)

    raw = filter_year(raw, year_from, year_to)
    canonical = [to_canonical(e, i + 1, query) for i, e in enumerate(raw)]
    return canonical


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Direct arXiv search for the get-research-paper skill.")
    p.add_argument("--query", help="Search query string.")
    p.add_argument("--max-results", type=int, default=30)
    p.add_argument("--year-from", type=int, default=None)
    p.add_argument("--year-to", type=int, default=None)
    p.add_argument("--categories", default=None,
                   help="Comma-separated arXiv categories (e.g., 'cs.LG,cs.CL').")
    p.add_argument("--out", default=None,
                   help="Write JSON to this path (default: stdout).")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)

    if args.self_test:
        feedparser, requests_lib = _try_imports()
        print("feedparser available:", feedparser is not None)
        print("requests available:", requests_lib is not None)
        print("urllib stdlib:", True)
        print("xml.etree stdlib:", True)
        return 0

    if not args.query:
        p.error("--query is required (or use --self-test)")

    cats = None
    if args.categories:
        cats = [c.strip() for c in args.categories.split(",") if c.strip()]

    try:
        results = search(
            args.query,
            max_results=args.max_results,
            year_from=args.year_from,
            year_to=args.year_to,
            categories=cats,
        )
    except urllib.error.URLError as e:
        sys.stderr.write(f"Network error: {e}\n")
        return 2
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        return 3

    payload = json.dumps(results, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(payload)
        print(f"Wrote {len(results)} entries to {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(payload + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
