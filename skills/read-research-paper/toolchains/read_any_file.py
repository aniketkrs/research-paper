#!/usr/bin/env python3
"""
read_any_file.py
================

Universal file reader for the read-research-paper skill (and reusable
by the other two). Detects format by extension and extracts text +
metadata.

Supported input formats:
  .pdf                          via pypdf / pdfplumber
  .docx                         via python-docx
  .pptx                         via python-pptx
  .md, .markdown                native text
  .tex, .latex                  native text + light de-LaTeX
  .html, .htm                   via beautifulsoup4 / fallback regex
  .txt                          native text
  .rtf                          via striprtf (or pandoc fallback)
  .epub                         via ebooklib
  .png, .jpg, .jpeg, .tiff      via pytesseract OCR (optional)
  .json                         native
  .csv, .tsv                    via csv stdlib (or pandas)
  .xlsx, .xls                   via openpyxl / pandas

Designed for graceful degradation: every format has a "no-deps" fallback
or a clear "install X to enable" message.

Usage:
  python read_any_file.py --input paper.pdf --out paper.json
  python read_any_file.py --input slides.pptx --text-out slides.txt
  python read_any_file.py --self-test
  python read_any_file.py --list-formats
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Optional imports — every reader checks before using
# ---------------------------------------------------------------------------
def _opt(mod_name):
    try:
        return __import__(mod_name)
    except ImportError:
        return None


# ---------------------------------------------------------------------------
# Format → reader registry
# ---------------------------------------------------------------------------
def detect_format(path: str) -> str:
    ext = Path(path).suffix.lower().lstrip(".")
    aliases = {
        "markdown": "md",
        "htm": "html",
        "yml": "yaml",
        "tsv": "csv",
        "latex": "tex",
        "jpeg": "jpg",
        "tiff": "tif",
    }
    return aliases.get(ext, ext)


def read_text(path: str, encoding: str = "utf-8-sig") -> str:
    with open(path, "r", encoding=encoding, errors="replace") as f:
        return f.read()


def read_bytes(path: str) -> bytes:
    with open(path, "rb") as f:
        return f.read()


# ---------------------------------------------------------------------------
# Per-format readers
# ---------------------------------------------------------------------------
def read_md(path: str) -> dict:
    text = read_text(path)
    return {"format": "md", "text": text, "structure": _md_outline(text)}


def _md_outline(text: str) -> list[dict]:
    """Extract H1/H2/H3 headings as a structure outline."""
    out = []
    for m in re.finditer(r"^(#{1,3})\s+(.+)$", text, re.MULTILINE):
        level = len(m.group(1))
        out.append({"level": level, "title": m.group(2).strip()})
    return out


def read_txt(path: str) -> dict:
    return {"format": "txt", "text": read_text(path)}


def read_html(path: str) -> dict:
    raw = read_text(path)
    bs4 = _opt("bs4")
    if bs4 is None:
        # Fallback regex strip
        text = re.sub(r"<script[^>]*>.*?</script>", "", raw,
                       flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<style[^>]*>.*?</style>", "", text,
                       flags=re.DOTALL | re.IGNORECASE)
        text = re.sub(r"<[^>]+>", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return {"format": "html", "text": text,
                "extractor": "regex-fallback",
                "warning": "Install beautifulsoup4 (pip install beautifulsoup4) for better extraction."}
    soup = bs4.BeautifulSoup(raw, "html.parser")
    for tag in soup(["script", "style"]):
        tag.decompose()
    return {"format": "html", "text": soup.get_text(" ", strip=True),
            "extractor": "beautifulsoup4",
            "title": (soup.title.string if soup.title else "") or ""}


def read_tex(path: str) -> dict:
    """Light de-LaTeX: strip commands, keep text."""
    raw = read_text(path)
    text = raw
    # Strip comments
    text = re.sub(r"(?<!\\)%.*$", "", text, flags=re.MULTILINE)
    # Strip preamble before \begin{document}
    m = re.search(r"\\begin\{document\}", text)
    if m:
        text = text[m.end():]
    m = re.search(r"\\end\{document\}", text)
    if m:
        text = text[:m.start()]
    # Replace common commands
    text = re.sub(r"\\(?:title|author|abstract|section|subsection|subsubsection)\*?\s*\{([^}]*)\}",
                   r"\n\n\1\n\n", text)
    text = re.sub(r"\\(?:textbf|textit|emph|texttt|underline)\s*\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\cite[pt]?\{[^}]*\}", "[CITE]", text)
    text = re.sub(r"\\ref\{[^}]*\}", "[REF]", text)
    text = re.sub(r"\\label\{[^}]*\}", "", text)
    text = re.sub(r"\\(?:begin|end)\{[^}]*\}", "", text)
    text = re.sub(r"\\[a-zA-Z]+\*?(?:\[[^\]]*\])?(?:\{[^}]*\})?", "", text)
    text = re.sub(r"[{}]", "", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return {"format": "tex", "text": text.strip(), "raw_size": len(raw)}


def read_pdf(path: str) -> dict:
    pdfplumber = _opt("pdfplumber")
    pypdf = _opt("pypdf")
    if pdfplumber is None and pypdf is None:
        return {"format": "pdf", "text": "",
                "error": "No PDF library installed.",
                "install_hint": "pip install pdfplumber  (recommended)\nor: pip install pypdf"}
    if pdfplumber is not None:
        pages = []
        tables = []
        with pdfplumber.open(path) as pdf:
            for i, page in enumerate(pdf.pages[:300]):
                pages.append(page.extract_text() or "")
                for j, t in enumerate(page.extract_tables() or []):
                    tables.append({"page": i + 1, "rows": t})
        return {"format": "pdf", "text": "\n\n".join(pages),
                "n_pages": len(pages), "tables": tables,
                "extractor": "pdfplumber"}
    # pypdf fallback
    reader = pypdf.PdfReader(path)
    pages = []
    for page in reader.pages[:300]:
        try:
            pages.append(page.extract_text() or "")
        except Exception:
            pages.append("")
    md = {}
    if reader.metadata:
        for k, v in reader.metadata.items():
            md[k.lstrip("/")] = str(v)
    return {"format": "pdf", "text": "\n\n".join(pages),
            "n_pages": len(pages), "metadata": md,
            "extractor": "pypdf"}


def read_docx(path: str) -> dict:
    docx = _opt("docx")
    if docx is None:
        return {"format": "docx", "text": "",
                "error": "python-docx not installed.",
                "install_hint": "pip install python-docx"}
    doc = docx.Document(path)
    paragraphs = [p.text for p in doc.paragraphs]
    tables = []
    for t in doc.tables:
        rows = [[cell.text for cell in row.cells] for row in t.rows]
        tables.append({"rows": rows})
    return {"format": "docx", "text": "\n".join(paragraphs),
            "tables": tables, "n_paragraphs": len(paragraphs),
            "extractor": "python-docx"}


def read_pptx(path: str) -> dict:
    pptx = _opt("pptx")
    if pptx is None:
        return {"format": "pptx", "text": "",
                "error": "python-pptx not installed.",
                "install_hint": "pip install python-pptx"}
    pres = pptx.Presentation(path)
    slides = []
    for i, slide in enumerate(pres.slides):
        parts = []
        for shape in slide.shapes:
            if hasattr(shape, "text") and shape.text:
                parts.append(shape.text)
        slides.append({"slide": i + 1, "text": "\n".join(parts)})
    full = "\n\n--- slide break ---\n\n".join(s["text"] for s in slides)
    return {"format": "pptx", "text": full, "slides": slides,
            "n_slides": len(slides), "extractor": "python-pptx"}


def read_image(path: str) -> dict:
    pytesseract = _opt("pytesseract")
    PIL = _opt("PIL")
    if pytesseract is None or PIL is None:
        return {"format": "image", "text": "",
                "error": "OCR not available.",
                "install_hint": "pip install pytesseract Pillow  (also requires Tesseract installed)"}
    from PIL import Image  # type: ignore
    img = Image.open(path)
    text = pytesseract.image_to_string(img)
    return {"format": "image", "text": text,
            "size": img.size, "mode": img.mode,
            "extractor": "pytesseract"}


def read_json(path: str) -> dict:
    raw = read_text(path)
    try:
        obj = json.loads(raw)
    except json.JSONDecodeError as e:
        return {"format": "json", "text": raw, "error": f"Invalid JSON: {e}"}
    return {"format": "json", "data": obj, "text": json.dumps(obj, indent=2)}


def read_csv(path: str) -> dict:
    pd = _opt("pandas")
    if pd is not None:
        df = pd.read_csv(path) if path.endswith(".csv") else pd.read_csv(path, sep="\t")
        return {"format": "csv", "n_rows": len(df), "n_cols": len(df.columns),
                "columns": list(df.columns),
                "text": df.head(50).to_markdown(index=False),
                "extractor": "pandas"}
    rows = []
    with open(path, "r", encoding="utf-8-sig", newline="") as f:
        reader = csv.reader(f, delimiter="\t" if path.endswith(".tsv") else ",")
        for row in reader:
            rows.append(row)
    headers = rows[0] if rows else []
    return {"format": "csv", "n_rows": max(0, len(rows) - 1),
            "n_cols": len(headers), "columns": headers,
            "text": "\n".join("\t".join(r) for r in rows[:51]),
            "extractor": "csv-stdlib"}


def read_xlsx(path: str) -> dict:
    pd = _opt("pandas")
    openpyxl = _opt("openpyxl")
    if pd is not None:
        # pandas + openpyxl combo handles xlsx best
        try:
            df = pd.read_excel(path, sheet_name=0)
            return {"format": "xlsx", "n_rows": len(df), "n_cols": len(df.columns),
                    "columns": list(df.columns),
                    "text": df.head(50).to_markdown(index=False),
                    "extractor": "pandas+openpyxl"}
        except Exception as e:
            return {"format": "xlsx", "text": "", "error": str(e),
                    "install_hint": "pip install pandas openpyxl"}
    if openpyxl is not None:
        wb = openpyxl.load_workbook(path, read_only=True, data_only=True)
        sheets = []
        for name in wb.sheetnames:
            ws = wb[name]
            rows = []
            for row in ws.iter_rows(max_row=200, values_only=True):
                rows.append(["" if c is None else str(c) for c in row])
            sheets.append({"name": name, "rows": rows})
        text = "\n\n".join(
            "## " + s["name"] + "\n" + "\n".join("\t".join(r) for r in s["rows"][:51])
            for s in sheets)
        return {"format": "xlsx", "sheets": [s["name"] for s in sheets],
                "text": text, "extractor": "openpyxl"}
    return {"format": "xlsx", "text": "",
            "error": "Neither pandas nor openpyxl installed.",
            "install_hint": "pip install pandas openpyxl"}


def read_rtf(path: str) -> dict:
    striprtf = _opt("striprtf")
    if striprtf is not None:
        from striprtf.striprtf import rtf_to_text  # type: ignore
        text = rtf_to_text(read_text(path))
        return {"format": "rtf", "text": text, "extractor": "striprtf"}
    # fallback regex strip
    raw = read_text(path)
    text = re.sub(r"\\[a-z]+-?\d* ?", "", raw)
    text = re.sub(r"[{}]", "", text)
    return {"format": "rtf", "text": text.strip(),
            "extractor": "regex-fallback",
            "warning": "Install striprtf for better extraction (pip install striprtf)."}


def read_epub(path: str) -> dict:
    ebooklib = _opt("ebooklib")
    if ebooklib is None:
        return {"format": "epub", "text": "",
                "error": "ebooklib not installed.",
                "install_hint": "pip install ebooklib beautifulsoup4"}
    from ebooklib import epub, ITEM_DOCUMENT  # type: ignore
    bs4 = _opt("bs4")
    book = epub.read_epub(path)
    chapters = []
    for item in book.get_items_of_type(ITEM_DOCUMENT):
        content = item.get_content().decode("utf-8", errors="replace")
        if bs4 is not None:
            soup = bs4.BeautifulSoup(content, "html.parser")
            for tag in soup(["script", "style"]):
                tag.decompose()
            chapters.append(soup.get_text(" ", strip=True))
        else:
            text = re.sub(r"<[^>]+>", " ", content)
            chapters.append(re.sub(r"\s+", " ", text).strip())
    return {"format": "epub", "n_chapters": len(chapters),
            "text": "\n\n".join(chapters), "extractor": "ebooklib"}


# ---------------------------------------------------------------------------
# Dispatcher
# ---------------------------------------------------------------------------
READERS = {
    "md": read_md,
    "txt": read_txt,
    "html": read_html,
    "tex": read_tex,
    "pdf": read_pdf,
    "docx": read_docx,
    "pptx": read_pptx,
    "png": read_image,
    "jpg": read_image,
    "tif": read_image,
    "bmp": read_image,
    "gif": read_image,
    "json": read_json,
    "csv": read_csv,
    "xlsx": read_xlsx,
    "xls": read_xlsx,
    "rtf": read_rtf,
    "epub": read_epub,
}


def read_any(path: str) -> dict:
    if not os.path.exists(path):
        return {"format": "unknown", "text": "", "error": f"File not found: {path}"}
    fmt = detect_format(path)
    reader = READERS.get(fmt)
    if reader is None:
        # Fallback: try as text
        try:
            return {"format": "text-fallback",
                    "text": read_text(path),
                    "warning": f"Unknown format '{fmt}' — read as plain text."}
        except Exception as e:
            return {"format": "unknown", "text": "", "error": str(e)}
    result = reader(path)
    result["path"] = path
    result["size_bytes"] = os.path.getsize(path)
    result["read_at"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
    return result


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def list_formats() -> None:
    print("Supported input formats:")
    for fmt, fn in sorted(READERS.items()):
        print(f"  .{fmt:<6} -> {fn.__name__}")


def self_test() -> None:
    print("read_any_file.py self-test")
    print("=" * 40)
    libs = [
        ("pypdf", "PDF basic"),
        ("pdfplumber", "PDF + tables"),
        ("python-docx", "DOCX"),
        ("python-pptx", "PPTX"),
        ("openpyxl", "XLSX"),
        ("pandas", "CSV/XLSX (better)"),
        ("beautifulsoup4 (bs4)", "HTML"),
        ("striprtf", "RTF"),
        ("ebooklib", "EPUB"),
        ("Pillow (PIL)", "Image OCR"),
        ("pytesseract", "Image OCR"),
    ]
    print(f"{'Library':<30} {'Available':<10} {'For'}")
    print("-" * 60)
    for name, purpose in libs:
        mod = name.split(" ", 1)[0].replace("-", "_")
        if mod == "PIL":
            mod = "PIL"
        elif mod == "bs4":
            mod = "bs4"
        elif mod == "beautifulsoup4":
            mod = "bs4"
        elif mod == "python_docx":
            mod = "docx"
        elif mod == "python_pptx":
            mod = "pptx"
        elif mod == "Pillow":
            mod = "PIL"
        avail = _opt(mod) is not None
        sym = "[ok]" if avail else "[..]"
        print(f"{name:<30} {sym:<10} {purpose}")
    print()
    print("Always-available stdlib readers: md, txt, tex, json, csv (basic), html (regex), rtf (regex)")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Universal file reader.")
    p.add_argument("--input", help="Input file path.")
    p.add_argument("--out", default=None, help="Write JSON result here.")
    p.add_argument("--text-out", default=None, help="Write extracted text here.")
    p.add_argument("--list-formats", action="store_true")
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)

    if args.list_formats:
        list_formats()
        return 0
    if args.self_test:
        self_test()
        return 0
    if not args.input:
        p.error("--input is required (or use --self-test / --list-formats)")

    result = read_any(args.input)
    if "error" in result:
        sys.stderr.write(f"{result['error']}\n")
        if "install_hint" in result:
            sys.stderr.write(f"Install: {result['install_hint']}\n")
        return 2

    payload = json.dumps({k: v for k, v in result.items() if k != "text"},
                         indent=2, default=str)
    if args.out:
        with open(args.out, "w", encoding="utf-8") as f:
            f.write(payload)
        print(f"Wrote metadata to {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(payload + "\n")

    if args.text_out:
        with open(args.text_out, "w", encoding="utf-8") as f:
            f.write(result.get("text", ""))
        print(f"Wrote text to {args.text_out}", file=sys.stderr)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
