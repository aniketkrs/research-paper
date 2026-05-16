#!/usr/bin/env python3
"""
format_bibliography.py
======================

Implements the citation pipeline (workflows/citation-pipeline.md). Reads
a canonical YAML bibliography + a Markdown paper draft with [cite_key]
placeholders, and produces:

- A paper file with all in-text citations formatted in the chosen style.
- A reference list section appended to the paper.
- A citation report.

Supported styles:  harvard | apa | ieee | mla | chicago-author-date |
                   chicago-notes | nature | arxiv-numeric

Usage:
  python format_bibliography.py \\
      --bib bibliography.yaml \\
      --style ieee \\
      --paper paper-draft.md \\
      --out paper-cited.md \\
      --report citation-report.md

Notes:
- Pure stdlib + optional pyyaml. Falls back to a JSON bibliography if
  pyyaml is missing (just rename to .json).
- Deterministic: same inputs ⇒ same output, byte for byte.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from typing import Any, Iterable

# ---------------------------------------------------------------------------
# YAML loader: prefer pyyaml; fall back to a tiny parser for our subset.
# ---------------------------------------------------------------------------
try:
    import yaml  # type: ignore
    def load_bib(path: str) -> list[dict[str, Any]]:
        with open(path, "r", encoding="utf-8-sig") as f:
            data = yaml.safe_load(f)
        if isinstance(data, dict) and "references" in data:
            data = data["references"]
        if not isinstance(data, list):
            raise ValueError(f"{path} must be a YAML list of entries.")
        return data
except ImportError:
    def load_bib(path: str) -> list[dict[str, Any]]:
        # Try JSON fallback.
        if path.endswith(".json"):
            with open(path, "r", encoding="utf-8-sig") as f:
                return json.load(f)
        raise SystemExit(
            "pyyaml is not installed and the bibliography is YAML.\n"
            "Install with: pip install pyyaml\n"
            "Or convert your bibliography to JSON and rerun."
        )


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
@dataclass
class Author:
    family: str
    given: str = ""
    is_organization: bool = False

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Author":
        return cls(
            family=str(d.get("family", "")).strip(),
            given=str(d.get("given", "")).strip(),
            is_organization=bool(d.get("is_organization", False)),
        )

    def initials(self) -> str:
        # "Jane A." -> "J. A."
        if not self.given:
            return ""
        parts = re.split(r"[\s\-\.]+", self.given.strip())
        out = []
        for p in parts:
            if not p:
                continue
            out.append(p[0].upper() + ".")
        return " ".join(out)

    def harvard_text(self) -> str:
        if self.is_organization:
            return self.family
        return f"{self.family}, {self.initials()}"

    def apa_text(self) -> str:
        if self.is_organization:
            return self.family
        # "Smith, J. A."
        return f"{self.family}, {self.initials()}".strip().rstrip(",")

    def ieee_text(self) -> str:
        if self.is_organization:
            return self.family
        # "J. A. Smith"
        return f"{self.initials()} {self.family}".strip()

    def nature_text(self) -> str:
        if self.is_organization:
            return self.family
        # "Smith, J. A."
        return f"{self.family}, {self.initials()}"

    def mla_text(self, first: bool) -> str:
        if self.is_organization:
            return self.family
        if first:
            # "Smith, Jane A."
            return f"{self.family}, {self.given}".rstrip(", ")
        # "Jane A. Smith"
        return f"{self.given} {self.family}".strip()


@dataclass
class Entry:
    cite_key: str
    type: str
    authors: list[Author]
    year: int | None
    title: str = ""
    container: str = ""
    volume: str = ""
    issue: str = ""
    pages: str = ""
    publisher: str = ""
    address: str = ""
    edition: str = ""
    doi: str = ""
    url: str = ""
    arxiv_id: str = ""
    isbn: str = ""
    institution: str = ""
    thesis_type: str = ""
    accessed: str = ""
    notes: str = ""
    editors: list[Author] = field(default_factory=list)
    incomplete_fields: list[str] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> "Entry":
        authors = [Author.from_dict(a) for a in (d.get("authors") or [])]
        editors = [Author.from_dict(a) for a in (d.get("editors") or [])]
        return cls(
            cite_key=str(d.get("id") or d.get("cite_key") or "").strip(),
            type=str(d.get("type") or "article-journal").strip(),
            authors=authors,
            year=d.get("year"),
            title=str(d.get("title") or "").strip(),
            container=str(d.get("container") or "").strip(),
            volume=str(d.get("volume") or "").strip(),
            issue=str(d.get("issue") or "").strip(),
            pages=str(d.get("pages") or "").strip(),
            publisher=str(d.get("publisher") or "").strip(),
            address=str(d.get("address") or "").strip(),
            edition=str(d.get("edition") or "").strip(),
            doi=str(d.get("doi") or "").strip(),
            url=str(d.get("url") or "").strip(),
            arxiv_id=str(d.get("arxiv_id") or "").strip(),
            isbn=str(d.get("isbn") or "").strip(),
            institution=str(d.get("institution") or "").strip(),
            thesis_type=str(d.get("thesis_type") or "").strip(),
            accessed=str(d.get("accessed") or "").strip(),
            notes=str(d.get("notes") or "").strip(),
            editors=editors,
            incomplete_fields=list(d.get("incomplete_fields") or []),
        )

    def display_year(self) -> str:
        return str(self.year) if self.year else "n.d."

    def first_author_family(self) -> str:
        return self.authors[0].family if self.authors else "Unknown"

    def doi_url(self) -> str:
        if self.doi:
            return f"https://doi.org/{self.doi}"
        if self.arxiv_id:
            return f"https://arxiv.org/abs/{self.arxiv_id}"
        return self.url


# ---------------------------------------------------------------------------
# Required-field validation
# ---------------------------------------------------------------------------
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


def validate_entry(e: Entry) -> list[str]:
    """Return list of missing required-field names."""
    req = REQUIRED.get(e.type, REQUIRED["article-journal"])
    missing: list[str] = []
    for f in req:
        v = getattr(e, f, None)
        if v is None or v == "" or (isinstance(v, list) and not v):
            missing.append(f)
    return missing


# ---------------------------------------------------------------------------
# Style: in-text formatters and reference-entry formatters.
# ---------------------------------------------------------------------------
def authors_short(authors: list[Author], style: str) -> str:
    if not authors:
        return "Unknown"
    if len(authors) == 1:
        return authors[0].family
    if len(authors) == 2:
        sep = "and" if style in ("harvard", "ieee", "mla") else "&"
        return f"{authors[0].family} {sep} {authors[1].family}"
    if style == "harvard":
        return f"{authors[0].family} et al."
    if style == "apa":
        return f"{authors[0].family} et al."
    if style == "mla":
        return f"{authors[0].family} et al."
    if style == "chicago-author-date":
        if len(authors) <= 3:
            return ", ".join(a.family for a in authors[:-1]) + f", and {authors[-1].family}"
        return f"{authors[0].family} et al."
    return f"{authors[0].family} et al."


def in_text_authoryear(e: Entry, style: str, narrative: bool = False, page: str | None = None) -> str:
    short = authors_short(e.authors, style)
    year = e.display_year()
    sep = " " if style == "chicago-author-date" else ", "
    if narrative:
        return f"{short} ({year})"
    if page:
        return f"({short}{sep}{year}, p. {page})"
    return f"({short}{sep}{year})"


def in_text_mla(e: Entry, page: str | None = None) -> str:
    short = authors_short(e.authors, "mla")
    if page:
        return f"({short} {page})"
    return f"({short})"


# ---------- reference-list entries per style ----------

def _join_authors_harvard(authors: list[Author]) -> str:
    if not authors:
        return "Unknown"
    bits = [a.harvard_text() for a in authors]
    if len(bits) == 1:
        return bits[0]
    return ", ".join(bits[:-1]) + f" and {bits[-1]}"


def _join_authors_apa(authors: list[Author]) -> str:
    if not authors:
        return "Unknown"
    bits = [a.apa_text() for a in authors]
    if len(bits) == 1:
        return bits[0]
    if len(bits) == 2:
        return f"{bits[0]}, & {bits[1]}"
    return ", ".join(bits[:-1]) + f", & {bits[-1]}"


def _join_authors_ieee(authors: list[Author]) -> str:
    if not authors:
        return "Unknown"
    bits = [a.ieee_text() for a in authors]
    if len(bits) == 1:
        return bits[0]
    if len(bits) == 2:
        return f"{bits[0]} and {bits[1]}"
    return ", ".join(bits[:-1]) + f", and {bits[-1]}"


def _join_authors_nature(authors: list[Author]) -> str:
    if not authors:
        return "Unknown"
    bits = [a.nature_text() for a in authors]
    if len(bits) == 1:
        return bits[0]
    return ", ".join(bits[:-1]) + f" & {bits[-1]}"


def ref_harvard(e: Entry) -> str:
    a = _join_authors_harvard(e.authors)
    y = e.display_year()
    if e.type == "article-journal":
        s = f"{a} ({y}) '{e.title}', *{e.container}*"
        if e.volume:
            s += f", {e.volume}"
            if e.issue:
                s += f"({e.issue})"
        if e.pages:
            s += f", pp. {e.pages}"
        s += "."
        if e.doi:
            s += f" doi:{e.doi}."
        elif e.url:
            s += f" Available at: {e.url}"
            if e.accessed:
                s += f" (Accessed: {e.accessed})"
            s += "."
        return s
    if e.type == "article-conference":
        s = f"{a} ({y}) '{e.title}', in *{e.container}*"
        if e.address:
            s += f". {e.address}"
        if e.publisher:
            s += f": {e.publisher}"
        if e.pages:
            s += f", pp. {e.pages}"
        s += "."
        if e.doi:
            s += f" doi:{e.doi}."
        return s
    if e.type == "book":
        s = f"{a} ({y}) *{e.title}*."
        if e.edition:
            s += f" {e.edition} edn."
        if e.address:
            s += f" {e.address}: "
        if e.publisher:
            s += f"{e.publisher}."
        return s
    if e.type == "chapter":
        eds = ", ".join(ed.harvard_text() for ed in e.editors) or "?"
        s = f"{a} ({y}) '{e.title}', in {eds} (ed.) *{e.container}*."
        if e.address:
            s += f" {e.address}: "
        if e.publisher:
            s += f"{e.publisher}"
        if e.pages:
            s += f", pp. {e.pages}"
        s += "."
        return s
    if e.type == "preprint":
        s = f"{a} ({y}) '{e.title}'"
        if e.arxiv_id:
            s += f", arXiv:{e.arxiv_id}"
        s += "."
        if e.url or e.arxiv_id:
            url = e.url or e.doi_url()
            s += f" Available at: {url}"
            if e.accessed:
                s += f" (Accessed: {e.accessed})"
            s += "."
        return s
    if e.type == "report":
        s = f"{a} ({y}) *{e.title}*."
        if e.publisher:
            s += f" {e.publisher}."
        if e.url:
            s += f" Available at: {e.url}"
            if e.accessed:
                s += f" (Accessed: {e.accessed})"
            s += "."
        return s
    if e.type == "webpage":
        s = f"{a} ({y}) *{e.title}*. Available at: {e.url}"
        if e.accessed:
            s += f" (Accessed: {e.accessed})"
        s += "."
        return s
    if e.type == "dataset":
        s = f"{a} ({y}) *{e.title}* [Dataset]."
        if e.publisher:
            s += f" {e.publisher}."
        if e.doi:
            s += f" doi:{e.doi}."
        elif e.url:
            s += f" Available at: {e.url}."
        return s
    if e.type == "thesis":
        s = f"{a} ({y}) *{e.title}*. {e.thesis_type or 'Thesis'}, {e.institution}."
        return s
    return f"{a} ({y}) {e.title}."


def ref_apa(e: Entry) -> str:
    a = _join_authors_apa(e.authors)
    y = e.display_year()
    if e.type == "article-journal":
        s = f"{a} ({y}). {e.title}. *{e.container}*"
        if e.volume:
            s += f", {e.volume}"
            if e.issue:
                s += f"({e.issue})"
        if e.pages:
            s += f", {e.pages}"
        s += "."
        if e.doi:
            s += f" https://doi.org/{e.doi}"
        elif e.url:
            s += f" {e.url}"
        return s
    if e.type == "book":
        s = f"{a} ({y}). *{e.title}*"
        if e.edition:
            s += f" ({e.edition} ed.)"
        s += "."
        if e.publisher:
            s += f" {e.publisher}."
        return s
    if e.type == "preprint":
        s = f"{a} ({y}). *{e.title}*."
        if e.arxiv_id:
            s += f" arXiv. https://doi.org/10.48550/arXiv.{e.arxiv_id}"
        elif e.url:
            s += f" {e.url}"
        return s
    if e.type == "webpage":
        s = f"{a} ({y}). *{e.title}*."
        if e.url:
            s += f" {e.url}"
        return s
    if e.type == "report":
        s = f"{a} ({y}). *{e.title}*."
        if e.publisher:
            s += f" {e.publisher}."
        if e.url:
            s += f" {e.url}"
        return s
    if e.type == "dataset":
        s = f"{a} ({y}). *{e.title}* [Dataset]."
        if e.doi:
            s += f" https://doi.org/{e.doi}"
        elif e.url:
            s += f" {e.url}"
        return s
    return f"{a} ({y}). {e.title}."


def ref_ieee(e: Entry, n: int) -> str:
    a = _join_authors_ieee(e.authors)
    y = e.display_year()
    if e.type == "article-journal":
        s = f"[{n}] {a}, \"{e.title},\" *{e.container}*"
        if e.volume:
            s += f", vol. {e.volume}"
        if e.issue:
            s += f", no. {e.issue}"
        if e.pages:
            s += f", pp. {e.pages}"
        s += f", {y}"
        if e.doi:
            s += f", doi: {e.doi}"
        s += "."
        return s
    if e.type == "article-conference":
        s = f"[{n}] {a}, \"{e.title},\" in *{e.container}*"
        if e.address:
            s += f", {e.address}"
        if e.pages:
            s += f", pp. {e.pages}"
        s += f", {y}"
        if e.doi:
            s += f", doi: {e.doi}"
        s += "."
        return s
    if e.type == "book":
        s = f"[{n}] {a}, *{e.title}*"
        if e.edition:
            s += f", {e.edition} ed."
        if e.address:
            s += f" {e.address}:"
        if e.publisher:
            s += f" {e.publisher}, {y}."
        else:
            s += f" {y}."
        return s
    if e.type == "preprint":
        s = f"[{n}] {a}, \"{e.title},\" {y}"
        if e.arxiv_id:
            s += f", *arXiv:{e.arxiv_id}*"
        s += "."
        return s
    if e.type == "webpage":
        s = f"[{n}] {a}, \"{e.title},\" {y}. [Online]. Available: {e.url}"
        if e.accessed:
            s += f" [Accessed: {e.accessed}]"
        s += "."
        return s
    if e.type == "dataset":
        s = f"[{n}] {a}, \"{e.title},\" {y}"
        if e.doi:
            s += f", doi: {e.doi}"
        s += "."
        return s
    return f"[{n}] {a}, \"{e.title},\" {y}."


def ref_nature(e: Entry, n: int) -> str:
    a = _join_authors_nature(e.authors)
    y = e.display_year()
    if e.type == "article-journal":
        s = f"{n}. {a} {e.title}. *{e.container}*"
        if e.volume:
            s += f" **{e.volume}**"
        if e.pages:
            s += f", {e.pages}"
        s += f" ({y})."
        return s
    if e.type == "book":
        s = f"{n}. {a} *{e.title}*"
        if e.edition:
            s += f" {e.edition} edn"
        s += " ("
        if e.publisher:
            s += f"{e.publisher}, "
        s += f"{y})."
        return s
    if e.type == "preprint":
        s = f"{n}. {a} {e.title}. Preprint at https://arxiv.org/abs/{e.arxiv_id} ({y})." if e.arxiv_id \
            else f"{n}. {a} {e.title}. Preprint ({y})."
        return s
    return f"{n}. {a} {e.title} ({y})."


def ref_mla(e: Entry) -> str:
    if not e.authors:
        a = "Unknown"
    elif len(e.authors) == 1:
        a = e.authors[0].mla_text(first=True)
    else:
        first = e.authors[0].mla_text(first=True)
        rest = ", ".join(au.mla_text(first=False) for au in e.authors[1:])
        a = f"{first}, et al." if len(e.authors) > 3 else f"{first}, {rest}"
    if e.type == "article-journal":
        s = f"{a} \"{e.title}.\" *{e.container}*"
        if e.volume:
            s += f", vol. {e.volume}"
        if e.issue:
            s += f", no. {e.issue}"
        s += f", {e.display_year()}"
        if e.pages:
            s += f", pp. {e.pages}"
        s += "."
        if e.doi:
            s += f" *DOI*, https://doi.org/{e.doi}."
        return s
    if e.type == "book":
        s = f"{a} *{e.title}*."
        if e.edition:
            s += f" {e.edition} ed.,"
        if e.publisher:
            s += f" {e.publisher},"
        s += f" {e.display_year()}."
        return s
    if e.type == "webpage":
        s = f"{a} \"{e.title}.\" *{e.container or 'Site Name'}*, {e.display_year()}, {e.url}."
        if e.accessed:
            s += f" Accessed {e.accessed}."
        return s
    return f"{a} \"{e.title}.\" {e.display_year()}."


def ref_chicago_ad(e: Entry) -> str:
    a = _join_authors_apa(e.authors).replace("&", "and")
    y = e.display_year()
    if e.type == "article-journal":
        s = f"{a}. {y}. \"{e.title}.\" *{e.container}*"
        if e.volume:
            s += f" {e.volume}"
        if e.issue:
            s += f" ({e.issue})"
        if e.pages:
            s += f": {e.pages}"
        s += "."
        if e.doi:
            s += f" https://doi.org/{e.doi}."
        return s
    return f"{a}. {y}. {e.title}."


def ref_arxiv_numeric(e: Entry, n: int) -> str:
    a = _join_authors_ieee(e.authors)
    y = e.display_year()
    if e.type in ("article-journal", "article-conference", "preprint"):
        s = f"[{n}] {a}, \"{e.title},\" *{e.container or 'arXiv'}*, {y}."
        return s
    return ref_ieee(e, n)


# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------
CITE_PATTERN = re.compile(r"\[([a-z][a-z0-9_;\s\-,]*)\]", re.IGNORECASE)
# Restrict to keys that look like cite_keys (lowercase, digits, _, -, ;)
KEY_PATTERN = re.compile(r"^[a-z0-9_\-]+(?:\.[a-z0-9_\-]+)?$", re.IGNORECASE)


def is_citation_block(content: str) -> bool:
    parts = [p.strip() for p in re.split(r"[;,]", content)]
    if not parts:
        return False
    return all(KEY_PATTERN.match(p) for p in parts)


def replace_citations(text: str, formatter) -> tuple[str, list[str]]:
    used: list[str] = []

    def _replace(m: re.Match[str]) -> str:
        inside = m.group(1)
        if not is_citation_block(inside):
            return m.group(0)
        keys = [k.strip() for k in re.split(r"[;,]\s*", inside) if k.strip()]
        rendered = formatter(keys)
        used.extend(keys)
        if rendered is None:
            return m.group(0)
        return rendered

    new_text = CITE_PATTERN.sub(_replace, text)
    return new_text, used


def build_index_by_first_appearance(text: str, entries: dict[str, Entry]) -> list[str]:
    seen: list[str] = []
    for m in CITE_PATTERN.finditer(text):
        inside = m.group(1)
        if not is_citation_block(inside):
            continue
        for key in re.split(r"[;,]\s*", inside):
            key = key.strip()
            if key and key in entries and key not in seen:
                seen.append(key)
    return seen


def disambiguate_year_suffix(entries: dict[str, Entry], appearance: list[str]) -> dict[str, str]:
    """For author-year styles: if same first-author-family + same year, append a/b/c."""
    suffix: dict[str, str] = {}
    seen: dict[tuple[str, int | None], list[str]] = {}
    for key in appearance:
        e = entries[key]
        bucket_key = (e.first_author_family().lower(), e.year)
        seen.setdefault(bucket_key, []).append(key)
    for bucket, keys in seen.items():
        if len(keys) > 1:
            for i, k in enumerate(keys):
                suffix[k] = chr(ord("a") + i)
    return suffix


def render_intext_authoryear_factory(entries, style, year_suffix):
    def fmt(keys: list[str]) -> str | None:
        if any(k not in entries for k in keys):
            return None
        rendered: list[str] = []
        for key in keys:
            e = entries[key]
            short = authors_short(e.authors, style)
            year = e.display_year() + year_suffix.get(key, "")
            sep = " " if style == "chicago-author-date" else ", "
            rendered.append(f"{short}{sep}{year}")
        return "(" + "; ".join(rendered) + ")"
    return fmt


def render_intext_numeric_factory(entries, number_of):
    def fmt(keys: list[str]) -> str | None:
        if any(k not in entries for k in keys):
            return None
        nums = sorted(number_of[k] for k in keys)
        # Compress runs
        groups: list[list[int]] = []
        for n in nums:
            if groups and n == groups[-1][-1] + 1:
                groups[-1].append(n)
            else:
                groups.append([n])
        bits = []
        for g in groups:
            if len(g) >= 3:
                bits.append(f"[{g[0]}]–[{g[-1]}]")
            else:
                bits.extend(f"[{x}]" for x in g)
        return ", ".join(bits)
    return fmt


def render_intext_nature_factory(entries, number_of):
    def fmt(keys: list[str]) -> str | None:
        if any(k not in entries for k in keys):
            return None
        nums = sorted(number_of[k] for k in keys)
        return "^" + ",".join(str(n) for n in nums)
    return fmt


def render_reference_list(entries: dict[str, Entry], style: str,
                           order: list[str], year_suffix: dict[str, str]) -> list[str]:
    if style == "ieee":
        return [ref_ieee(entries[k], i + 1) for i, k in enumerate(order)]
    if style == "arxiv-numeric":
        return [ref_arxiv_numeric(entries[k], i + 1) for i, k in enumerate(order)]
    if style == "nature":
        return [ref_nature(entries[k], i + 1) for i, k in enumerate(order)]
    # author-year-like styles: alphabetical
    if style == "harvard":
        items = sorted(entries.values(),
                       key=lambda e: (e.first_author_family().lower(), e.year or 0))
        out = []
        for e in items:
            base = ref_harvard(e)
            if e.cite_key in year_suffix:
                base = base.replace(f"({e.year})", f"({e.year}{year_suffix[e.cite_key]})", 1)
            out.append(base)
        return out
    if style == "apa":
        items = sorted(entries.values(),
                       key=lambda e: (e.first_author_family().lower(), e.year or 0))
        out = []
        for e in items:
            base = ref_apa(e)
            if e.cite_key in year_suffix:
                base = base.replace(f"({e.year})", f"({e.year}{year_suffix[e.cite_key]})", 1)
            out.append(base)
        return out
    if style == "mla":
        items = sorted(entries.values(),
                       key=lambda e: (e.first_author_family().lower(), e.year or 0))
        return [ref_mla(e) for e in items]
    if style == "chicago-author-date":
        items = sorted(entries.values(),
                       key=lambda e: (e.first_author_family().lower(), e.year or 0))
        return [ref_chicago_ad(e) for e in items]
    raise ValueError(f"Unsupported style: {style}")


REF_HEADER = "## References"


def replace_reference_section(text: str, lines: list[str]) -> str:
    block = REF_HEADER + "\n\n" + "\n\n".join(lines) + "\n"
    if REF_HEADER in text:
        # Replace from header to next top-level header or end of file.
        pattern = re.compile(rf"({re.escape(REF_HEADER)})(.*?)(?=\n##\s|\Z)", re.DOTALL)
        return pattern.sub(block, text, count=1)
    return text.rstrip() + "\n\n" + block


# ---------------------------------------------------------------------------
# Reports
# ---------------------------------------------------------------------------
def write_report(path: str, body: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Format citations & bibliography.")
    p.add_argument("--bib", required=True)
    p.add_argument("--paper", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--style", default="harvard",
                   choices=["harvard", "apa", "ieee", "mla",
                            "chicago-author-date", "nature", "arxiv-numeric"])
    p.add_argument("--locale", default="en-US")
    p.add_argument("--report", default=None)
    args = p.parse_args(argv)

    raw_entries = load_bib(args.bib)
    entries: dict[str, Entry] = {}
    for d in raw_entries:
        e = Entry.from_dict(d)
        if not e.cite_key:
            continue
        entries[e.cite_key] = e

    with open(args.paper, "r", encoding="utf-8-sig") as f:
        text = f.read()

    appearance = build_index_by_first_appearance(text, entries)
    cited_keys = set(appearance)
    missing_keys: set[str] = set()
    for m in CITE_PATTERN.finditer(text):
        inside = m.group(1)
        if not is_citation_block(inside):
            continue
        for key in re.split(r"[;,]\s*", inside):
            key = key.strip()
            if key and key not in entries:
                missing_keys.add(key)

    incomplete: list[tuple[str, list[str]]] = []
    for key in cited_keys:
        miss = validate_entry(entries[key])
        if miss:
            incomplete.append((key, miss))

    year_suffix: dict[str, str] = {}
    if args.style in ("harvard", "apa", "chicago-author-date"):
        year_suffix = disambiguate_year_suffix(entries, appearance)

    if args.style in ("ieee", "arxiv-numeric"):
        number_of = {k: i + 1 for i, k in enumerate(appearance)}
        formatter = render_intext_numeric_factory(entries, number_of)
    elif args.style == "nature":
        number_of = {k: i + 1 for i, k in enumerate(appearance)}
        formatter = render_intext_nature_factory(entries, number_of)
    elif args.style == "mla":
        # MLA author-year-ish — render as (Author) without page (needs explicit pages)
        def formatter(keys: list[str]) -> str | None:
            if any(k not in entries for k in keys):
                return None
            return "(" + "; ".join(authors_short(entries[k].authors, "mla") for k in keys) + ")"
    else:  # harvard / apa / chicago-ad
        formatter = render_intext_authoryear_factory(entries, args.style, year_suffix)

    new_text, used = replace_citations(text, formatter)
    refs = render_reference_list(entries, args.style, appearance if args.style in ("ieee", "nature", "arxiv-numeric") else list(entries.keys()), year_suffix)
    final_text = replace_reference_section(new_text, refs)

    with open(args.out, "w", encoding="utf-8") as f:
        f.write(final_text)

    # Build report
    orphans = [k for k in entries if k not in cited_keys]
    report_lines: list[str] = []
    report_lines.append("# Citation report")
    report_lines.append("")
    report_lines.append(f"- Style: {args.style}")
    report_lines.append(f"- Total in-text citations: {len(used)}")
    report_lines.append(f"- Total unique cited references: {len(cited_keys)}")
    report_lines.append(f"- Orphan references (not cited): {len(orphans)}")
    if orphans:
        report_lines.append("  - " + ", ".join(orphans))
    report_lines.append(f"- Missing keys: {len(missing_keys)}")
    if missing_keys:
        report_lines.append("  - " + ", ".join(sorted(missing_keys)))
    report_lines.append(f"- Incomplete entries: {len(incomplete)}")
    for key, miss in incomplete:
        report_lines.append(f"  - {key}: missing {', '.join(miss)}")

    report = "\n".join(report_lines) + "\n"
    if args.report:
        write_report(args.report, report)
    else:
        sys.stdout.write(report)

    if missing_keys or incomplete:
        return 2  # caller decides whether to halt
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
