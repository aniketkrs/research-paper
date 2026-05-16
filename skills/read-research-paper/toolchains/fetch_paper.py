#!/usr/bin/env python3
"""
fetch_paper.py
==============

Fetches a research paper given a URL, arXiv ID, DOI, or local PDF
path, and returns the parsed structure as JSON per
schemas/visual-paper.json.

Designed for graceful degradation:
  - feedparser (arXiv parsing) - optional, falls back to xml.etree.
  - requests - optional, falls back to urllib.
  - pypdf - optional, PDF mode only.
  - pyyaml - optional for the corpus.

Usage:
  python fetch_paper.py --input "https://arxiv.org/abs/2403.01234" \\
                         --out paper-data.json

  python fetch_paper.py --input "10.1145/3589334" \\
                         --type doi \\
                         --out paper-data.json

  python fetch_paper.py --input ./paper.pdf --type pdf

  python fetch_paper.py --self-test
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from typing import Any

USER_AGENT = "research-paper-skill/read-research-paper-1.0"
ARXIV_API = "https://export.arxiv.org/api/query"
CROSSREF_API = "https://api.crossref.org/works"


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
    try:
        import pypdf  # type: ignore
    except ImportError:
        pypdf = None
    return feedparser, requests, pypdf


# ---------------------------------------------------------------------------
# HTTP fetch
# ---------------------------------------------------------------------------
_LAST = [0.0]


def fetch(url: str, timeout: int = 30, requests_lib=None) -> str:
    elapsed = time.time() - _LAST[0]
    if elapsed < 1.0:
        time.sleep(1.0 - elapsed)
    _LAST[0] = time.time()

    if requests_lib is not None:
        resp = requests_lib.get(
            url, timeout=timeout,
            headers={"User-Agent": USER_AGENT, "Accept": "application/json, text/xml, text/html, */*"}
        )
        resp.raise_for_status()
        return resp.text

    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


# ---------------------------------------------------------------------------
# Input detection
# ---------------------------------------------------------------------------
ARXIV_URL = re.compile(r"arxiv\.org/(abs|pdf)/([\w\.\-/]+?)(?:v\d+)?(?:\.pdf)?$", re.IGNORECASE)
ARXIV_BARE_NEW = re.compile(r"^\d{4}\.\d{4,5}(v\d+)?$")
ARXIV_BARE_OLD = re.compile(r"^[a-z\-]+/\d{7}(v\d+)?$")
DOI_PATTERN = re.compile(r"^10\.[\d\.]+/.+$")
DOI_URL = re.compile(r"doi\.org/(10\..+)$", re.IGNORECASE)


def detect_input_type(s: str) -> tuple[str, str]:
    """Return (type, normalized_id_or_url)."""
    s = s.strip()

    # arXiv URL
    m = ARXIV_URL.search(s)
    if m:
        return ("arxiv", re.sub(r"v\d+$", "", m.group(2)))

    # bare arXiv ID
    if ARXIV_BARE_NEW.match(s) or ARXIV_BARE_OLD.match(s):
        return ("arxiv", re.sub(r"v\d+$", "", s))

    # DOI URL
    m = DOI_URL.search(s)
    if m:
        return ("doi", m.group(1))

    # bare DOI
    if DOI_PATTERN.match(s):
        return ("doi", s)

    # Local PDF path
    if (s.endswith(".pdf") and (os.path.exists(s) or "/" in s or "\\" in s)) or \
            (s.lower().endswith(".pdf") and s.startswith(("http://", "https://"))):
        return ("pdf", s)

    # URL fallback
    if s.startswith(("http://", "https://")):
        return ("url", s)

    # Otherwise: pasted text
    return ("text", s)


def canonical_id(input_type: str, value: str) -> str:
    if input_type == "arxiv":
        return f"arxiv:{value}"
    if input_type == "doi":
        return f"doi:{value}"
    if input_type == "pdf":
        h = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
        return f"pdf:{h}"
    if input_type == "url":
        h = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
        return f"url:{h}"
    h = hashlib.sha256(value.encode("utf-8")).hexdigest()[:16]
    return f"text:{h}"


# ---------------------------------------------------------------------------
# arXiv fetch
# ---------------------------------------------------------------------------
def fetch_arxiv(arxiv_id: str, requests_lib=None, feedparser_lib=None) -> dict[str, Any]:
    url = f"{ARXIV_API}?id_list={urllib.parse.quote(arxiv_id)}&max_results=1"
    xml = fetch(url, requests_lib=requests_lib)
    if feedparser_lib is not None:
        feed = feedparser_lib.parse(xml)
        if not feed.entries:
            raise RuntimeError(f"arXiv returned no entries for {arxiv_id}")
        entry = feed.entries[0]
        return _parse_arxiv_entry(entry, arxiv_id)
    return _parse_arxiv_xml(xml, arxiv_id)


def _parse_arxiv_entry(entry, arxiv_id: str) -> dict[str, Any]:
    authors = []
    for a in entry.get("authors", []):
        family, given = _split_name(a.get("name", ""))
        authors.append({"family": family, "given": given})
    published = entry.get("published", "")
    year = int(published[:4]) if published[:4].isdigit() else None
    doi = ""
    journal_ref = ""
    for k, v in entry.items():
        if k.endswith("doi"):
            doi = v
        if k.endswith("journal_ref"):
            journal_ref = v
    return {
        "canonical_id": f"arxiv:{arxiv_id}",
        "title": entry.title.strip().replace("\n", " "),
        "authors": authors,
        "year": year,
        "venue": journal_ref or "arXiv",
        "doi": doi,
        "arxiv_id": arxiv_id,
        "url": entry.id,
        "abstract": entry.get("summary", "").strip(),
        "sections": [
            {
                "id": "abstract",
                "title": "Abstract",
                "text": entry.get("summary", "").strip(),
                "inferred_from_text": False,
            }
        ],
        "figures": [],
        "tables": [],
        "headline_numbers": [],
        "references": [],
        "limitations": [],
        "contribution_list": [],
        "cache_metadata": {
            "version": 1,
            "fetched_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "source": "live-fetch",
            "skill_version": "1.0.0",
            "verification_trail": {
                "doi_resolves": None,
                "crossref_match": None,
                "retraction_check": "not-checked",
                "arxiv_confirmed": True,
                "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            },
        },
        "incomplete_fields": [],
    }


def _parse_arxiv_xml(xml: str, arxiv_id: str) -> dict[str, Any]:
    """Minimal XML parsing fallback."""
    import xml.etree.ElementTree as ET
    ns = {"atom": "http://www.w3.org/2005/Atom",
          "arxiv": "http://arxiv.org/schemas/atom"}
    root = ET.fromstring(xml)
    entry = root.find("atom:entry", ns)
    if entry is None:
        raise RuntimeError(f"arXiv returned no entries for {arxiv_id}")

    title = (entry.findtext("atom:title", default="", namespaces=ns) or "").strip().replace("\n", " ")
    summary = (entry.findtext("atom:summary", default="", namespaces=ns) or "").strip()
    published = (entry.findtext("atom:published", default="", namespaces=ns) or "").strip()
    full_id = (entry.findtext("atom:id", default="", namespaces=ns) or "").strip()
    year = int(published[:4]) if published[:4].isdigit() else None
    authors = []
    for au in entry.findall("atom:author", ns):
        name = (au.findtext("atom:name", default="", namespaces=ns) or "").strip()
        family, given = _split_name(name)
        authors.append({"family": family, "given": given})
    doi_el = entry.find("arxiv:doi", ns)
    doi = (doi_el.text if doi_el is not None else "") or ""
    jr_el = entry.find("arxiv:journal_ref", ns)
    journal_ref = (jr_el.text if jr_el is not None else "") or ""

    return {
        "canonical_id": f"arxiv:{arxiv_id}",
        "title": title,
        "authors": authors,
        "year": year,
        "venue": journal_ref or "arXiv",
        "doi": doi,
        "arxiv_id": arxiv_id,
        "url": full_id,
        "abstract": summary,
        "sections": [{"id": "abstract", "title": "Abstract", "text": summary, "inferred_from_text": False}],
        "figures": [],
        "tables": [],
        "headline_numbers": [],
        "references": [],
        "limitations": [],
        "contribution_list": [],
        "cache_metadata": {
            "version": 1,
            "fetched_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "source": "live-fetch",
            "skill_version": "1.0.0",
            "verification_trail": {
                "doi_resolves": None, "crossref_match": None,
                "retraction_check": "not-checked", "arxiv_confirmed": True,
                "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            },
        },
        "incomplete_fields": [],
    }


# ---------------------------------------------------------------------------
# DOI / Crossref fetch
# ---------------------------------------------------------------------------
def fetch_doi(doi: str, requests_lib=None) -> dict[str, Any]:
    url = f"{CROSSREF_API}/{urllib.parse.quote(doi)}"
    body = fetch(url, requests_lib=requests_lib)
    obj = json.loads(body)
    msg = obj.get("message", {})

    title = (msg.get("title") or [""])[0]
    abstract = msg.get("abstract", "")
    abstract = re.sub(r"<[^>]+>", "", abstract).strip() if abstract else ""

    authors = []
    for a in msg.get("author", []):
        authors.append({
            "family": a.get("family", ""),
            "given": a.get("given", ""),
            "affiliation": (a.get("affiliation") or [{}])[0].get("name", ""),
        })

    year = None
    for k in ("published", "published-online", "published-print", "issued"):
        v = msg.get(k, {})
        parts = v.get("date-parts", [[None]])
        if parts and parts[0] and parts[0][0]:
            year = int(parts[0][0])
            break

    venue = (msg.get("container-title") or [""])[0]

    return {
        "canonical_id": f"doi:{doi}",
        "title": title.strip(),
        "authors": authors,
        "year": year,
        "venue": venue,
        "doi": doi,
        "arxiv_id": "",
        "url": f"https://doi.org/{doi}",
        "abstract": abstract,
        "sections": [{"id": "abstract", "title": "Abstract", "text": abstract, "inferred_from_text": False}] if abstract else [],
        "figures": [],
        "tables": [],
        "headline_numbers": [],
        "references": [],
        "limitations": [],
        "contribution_list": [],
        "cache_metadata": {
            "version": 1,
            "fetched_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "source": "live-fetch",
            "skill_version": "1.0.0",
            "verification_trail": {
                "doi_resolves": True, "crossref_match": True,
                "retraction_check": "not-checked", "arxiv_confirmed": None,
                "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            },
        },
        "incomplete_fields": [] if abstract else ["abstract"],
    }


# ---------------------------------------------------------------------------
# PDF fetch
# ---------------------------------------------------------------------------
def fetch_pdf(path_or_url: str, requests_lib=None, pypdf_lib=None) -> dict[str, Any]:
    if pypdf_lib is None:
        raise RuntimeError("pypdf not installed; install with: pip install pypdf")
    # download if URL
    if path_or_url.startswith(("http://", "https://")):
        # binary fetch
        if requests_lib is not None:
            resp = requests_lib.get(path_or_url, timeout=60,
                                    headers={"User-Agent": USER_AGENT})
            resp.raise_for_status()
            data = resp.content
        else:
            req = urllib.request.Request(path_or_url, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(req, timeout=60) as r:
                data = r.read()
        import io
        reader = pypdf_lib.PdfReader(io.BytesIO(data))
    else:
        reader = pypdf_lib.PdfReader(path_or_url)

    text_parts = []
    for page in reader.pages[:200]:  # cap at 200 pages
        try:
            text_parts.append(page.extract_text() or "")
        except Exception:
            text_parts.append("")
    full_text = "\n".join(text_parts)

    title = ""
    if reader.metadata:
        title = reader.metadata.get("/Title", "") or ""

    h = hashlib.sha256(path_or_url.encode("utf-8")).hexdigest()[:16]

    return {
        "canonical_id": f"pdf:{h}",
        "title": title or path_or_url.rsplit("/", 1)[-1],
        "authors": [],
        "year": None,
        "venue": "",
        "doi": "",
        "arxiv_id": "",
        "url": path_or_url,
        "abstract": "",
        "sections": [{"id": "custom", "title": "Full text", "text": full_text[:30000], "inferred_from_text": True}],
        "figures": [],
        "tables": [],
        "headline_numbers": [],
        "references": [],
        "limitations": [],
        "contribution_list": [],
        "cache_metadata": {
            "version": 1,
            "fetched_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            "source": "live-fetch",
            "skill_version": "1.0.0",
            "verification_trail": {
                "doi_resolves": None, "crossref_match": None,
                "retraction_check": "not-checked", "arxiv_confirmed": None,
                "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
            },
        },
        "incomplete_fields": ["authors", "year", "venue", "doi", "abstract", "sections"],
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _split_name(name: str) -> tuple[str, str]:
    name = name.strip()
    if not name:
        return ("", "")
    if "," in name:
        family, _, given = name.partition(",")
        return (family.strip(), given.strip())
    parts = name.split()
    if len(parts) == 1:
        return (parts[0], "")
    return (parts[-1], " ".join(parts[:-1]))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Fetch a research paper.")
    p.add_argument("--input", help="URL / arXiv ID / DOI / PDF path / pasted text.")
    p.add_argument("--type", default="auto",
                   choices=["auto", "arxiv", "doi", "pdf", "url", "text"])
    p.add_argument("--out", default=None, help="Output JSON path.")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)

    feedparser_lib, requests_lib, pypdf_lib = _try_imports()

    if args.self_test:
        print("feedparser available:", feedparser_lib is not None)
        print("requests available:", requests_lib is not None)
        print("pypdf available:", pypdf_lib is not None)
        print("urllib stdlib:", True)
        print("xml.etree stdlib:", True)
        # smoke-test detection logic
        cases = [
            "https://arxiv.org/abs/2403.01234",
            "2403.01234",
            "10.1145/3589334",
            "https://doi.org/10.1145/3589334",
            "./paper.pdf",
            "https://example.com/page",
            "Some pasted abstract text...",
        ]
        for c in cases:
            t, v = detect_input_type(c)
            print(f"  detect: {c!r:60s} -> ({t}, {v[:40]!r})")
        return 0

    if not args.input:
        p.error("--input is required (or use --self-test)")

    input_type = args.type
    value = args.input
    if input_type == "auto":
        input_type, value = detect_input_type(args.input)

    try:
        if input_type == "arxiv":
            result = fetch_arxiv(value, requests_lib, feedparser_lib)
        elif input_type == "doi":
            result = fetch_doi(value, requests_lib)
        elif input_type == "pdf":
            result = fetch_pdf(value, requests_lib, pypdf_lib)
        elif input_type == "url":
            # delegate to crossref if URL contains DOI; else fail honestly
            m = DOI_URL.search(value)
            if m:
                result = fetch_doi(m.group(1), requests_lib)
            else:
                sys.stderr.write(
                    f"URL fetch without DOI extraction is not supported by this script.\n"
                    f"Use the agent's WebFetch tool instead, then pipe the text to --type text.\n"
                )
                return 4
        elif input_type == "text":
            cid = canonical_id("text", value)
            result = {
                "canonical_id": cid,
                "title": (value.split("\n", 1)[0])[:120].strip() or "Untitled",
                "authors": [],
                "year": None,
                "venue": "",
                "doi": "",
                "arxiv_id": "",
                "url": "",
                "abstract": value[:2000],
                "sections": [{"id": "custom", "title": "Full text", "text": value, "inferred_from_text": True}],
                "figures": [],
                "tables": [],
                "headline_numbers": [],
                "references": [],
                "limitations": [],
                "contribution_list": [],
                "cache_metadata": {
                    "version": 1,
                    "fetched_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                    "source": "live-fetch",
                    "skill_version": "1.0.0",
                    "verification_trail": {
                        "doi_resolves": None, "crossref_match": None,
                        "retraction_check": "not-checked", "arxiv_confirmed": None,
                        "checked_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
                    },
                },
                "incomplete_fields": ["title", "authors", "year", "venue", "doi"],
            }
        else:
            sys.stderr.write(f"Unsupported input type: {input_type}\n")
            return 5
    except urllib.error.URLError as e:
        sys.stderr.write(f"Network error: {e}\n")
        return 2
    except Exception as e:
        sys.stderr.write(f"Error: {e}\n")
        return 3

    payload = json.dumps(result, indent=2, ensure_ascii=False)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(payload)
        print(f"Wrote paper-data.json to {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(payload + "\n")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
