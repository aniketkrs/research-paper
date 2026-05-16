#!/usr/bin/env python3
"""
extract_pdf.py
==============

Extract text + tables + (best-effort) figure references from a PDF.
Used by fetch_paper.py for PDF inputs and as a standalone utility.

Designed for graceful degradation:
  - pypdf - best-effort text + metadata.
  - pdfplumber (optional, better tables) - if available.
  - Without any PDF library, reports the limitation clearly.

Usage:
  python extract_pdf.py --input paper.pdf --out paper-text.txt
  python extract_pdf.py --self-test
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys


def _try_imports():
    try:
        import pypdf  # type: ignore
    except ImportError:
        pypdf = None
    try:
        import pdfplumber  # type: ignore
    except ImportError:
        pdfplumber = None
    return pypdf, pdfplumber


def extract_with_pypdf(path: str) -> dict:
    import pypdf  # type: ignore
    reader = pypdf.PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages):
        try:
            pages.append({"page": i + 1, "text": page.extract_text() or ""})
        except Exception as e:
            pages.append({"page": i + 1, "text": "", "error": str(e)})
    metadata = {}
    if reader.metadata:
        for k, v in reader.metadata.items():
            metadata[k.lstrip("/")] = str(v)
    return {
        "extractor": "pypdf",
        "n_pages": len(reader.pages),
        "metadata": metadata,
        "pages": pages,
        "full_text": "\n\n".join(p["text"] for p in pages),
    }


def extract_with_pdfplumber(path: str) -> dict:
    import pdfplumber  # type: ignore
    pages = []
    tables = []
    with pdfplumber.open(path) as pdf:
        for i, page in enumerate(pdf.pages):
            txt = page.extract_text() or ""
            pages.append({"page": i + 1, "text": txt})
            for j, t in enumerate(page.extract_tables() or []):
                tables.append({"page": i + 1, "n_on_page": j + 1, "rows": t})
        return {
            "extractor": "pdfplumber",
            "n_pages": len(pdf.pages),
            "metadata": dict(pdf.metadata or {}),
            "pages": pages,
            "tables": tables,
            "full_text": "\n\n".join(p["text"] for p in pages),
        }


def detect_section_headers(text: str) -> list[dict]:
    """Heuristic section-header detection."""
    canonical = {
        "introduction": r"^\s*(?:\d+\.?\s*)?introduction\b",
        "background": r"^\s*(?:\d+\.?\s*)?background\b",
        "related-work": r"^\s*(?:\d+\.?\s*)?(?:related work|prior work|literature review)\b",
        "method": r"^\s*(?:\d+\.?\s*)?(?:method|methods|methodology|approach|system|architecture)\b",
        "experiments": r"^\s*(?:\d+\.?\s*)?(?:experiments?|experimental setup)\b",
        "results": r"^\s*(?:\d+\.?\s*)?(?:results?|findings|evaluation)\b",
        "discussion": r"^\s*(?:\d+\.?\s*)?discussion\b",
        "limitations": r"^\s*(?:\d+\.?\s*)?(?:limitations|threats to validity)\b",
        "conclusion": r"^\s*(?:\d+\.?\s*)?(?:conclusion|conclusions|future work|conclusion and future work)\b",
        "references": r"^\s*(?:\d+\.?\s*)?(?:references?|bibliography)\b",
        "appendix": r"^\s*(?:\d+\.?\s*)?(?:appendix|appendices)\b",
    }
    found = []
    for line_no, line in enumerate(text.split("\n")):
        clean = line.strip()
        if not clean or len(clean) > 80:
            continue
        for canon_id, pattern in canonical.items():
            if re.match(pattern, clean, re.IGNORECASE):
                found.append({
                    "id": canon_id,
                    "title": clean,
                    "line_no": line_no,
                })
                break
    return found


def extract_figures_and_tables(text: str) -> dict:
    """Find Figure / Table references in text."""
    figures = []
    tables = []
    for m in re.finditer(r"(?im)^\s*figure\s+(\d+)\s*[\.:]\s*(.+?)(?=\n\s*(?:figure|table)\s+\d+|\Z)",
                         text, re.DOTALL):
        figures.append({
            "number": int(m.group(1)),
            "caption": m.group(2).strip()[:500],
        })
    for m in re.finditer(r"(?im)^\s*table\s+(\d+)\s*[\.:]\s*(.+?)(?=\n\s*(?:figure|table)\s+\d+|\Z)",
                         text, re.DOTALL):
        tables.append({
            "number": int(m.group(1)),
            "caption": m.group(2).strip()[:500],
        })
    return {"figures": figures, "tables": tables}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--input", help="Path to a PDF file.")
    p.add_argument("--out", default=None, help="Write extracted JSON to this path.")
    p.add_argument("--text-out", default=None, help="Write plain text to this path.")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)

    pypdf, pdfplumber = _try_imports()

    if args.self_test:
        print("pypdf available:", pypdf is not None)
        print("pdfplumber available:", pdfplumber is not None)
        print("re stdlib:", True)
        if not pypdf and not pdfplumber:
            print("(install pypdf for basic extraction; pdfplumber adds table extraction)")
        return 0

    if not args.input:
        p.error("--input is required (or use --self-test)")
    if not os.path.exists(args.input):
        sys.stderr.write(f"File not found: {args.input}\n")
        return 2

    if pdfplumber is not None:
        result = extract_with_pdfplumber(args.input)
    elif pypdf is not None:
        result = extract_with_pypdf(args.input)
    else:
        sys.stderr.write(
            "No PDF library installed. Install one with:\n"
            "  pip install pypdf       (basic)\n"
            "  pip install pdfplumber  (better, with table extraction)\n"
        )
        return 3

    # Add structure detection
    text = result["full_text"]
    result["sections_detected"] = detect_section_headers(text)
    result["figures_and_tables"] = extract_figures_and_tables(text)

    payload = json.dumps(result, indent=2, ensure_ascii=False, default=str)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(payload)
        print(f"Wrote {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(payload + "\n")

    if args.text_out:
        with open(args.text_out, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"Wrote plain text to {args.text_out}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
