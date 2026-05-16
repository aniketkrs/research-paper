#!/usr/bin/env python3
"""
convert_output.py
=================

Universal output converter for the research-paper skill.

Takes a Markdown paper (the skill's native output format) and converts
it to any of: HTML, DOCX, PDF, LaTeX, RTF, EPUB, ODT, PPTX.

Uses Pandoc when installed (preferred); falls back to native Markdown
output when not.

Supported output formats:
  md       (default - native, no conversion)
  html     via pandoc
  docx     via pandoc
  pdf      via pandoc + LaTeX (texlive recommended)
  tex      via pandoc
  rtf      via pandoc
  epub     via pandoc
  odt      via pandoc
  pptx     via pandoc (note: poor for technical papers, OK for slides)

Usage:
  python convert_output.py --input paper-final.md --to pdf --out paper.pdf
  python convert_output.py --input paper-final.md --to html --out paper.html
  python convert_output.py --input paper-final.md --to docx
  python convert_output.py --self-test
  python convert_output.py --list-formats
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

PANDOC_FORMATS = {
    "md", "markdown", "html", "html5", "docx", "pdf", "tex", "latex",
    "rtf", "epub", "epub3", "odt", "pptx", "rst", "asciidoc",
    "org", "muse", "textile", "mediawiki", "dokuwiki",
}


# ---------------------------------------------------------------------------
# Pandoc detection
# ---------------------------------------------------------------------------
def find_pandoc() -> str | None:
    return shutil.which("pandoc")


def find_latex() -> str | None:
    """Find a LaTeX engine (for PDF output)."""
    for engine in ("pdflatex", "xelatex", "lualatex", "tectonic"):
        path = shutil.which(engine)
        if path:
            return path
    return None


def pandoc_version() -> str | None:
    pandoc = find_pandoc()
    if not pandoc:
        return None
    try:
        out = subprocess.run([pandoc, "--version"], capture_output=True,
                             text=True, timeout=10)
        return out.stdout.split("\n", 1)[0]
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Format normalization
# ---------------------------------------------------------------------------
def normalize_format(fmt: str) -> str:
    fmt = fmt.lower().lstrip(".")
    aliases = {
        "markdown": "md",
        "html5": "html",
        "htm": "html",
        "epub3": "epub",
        "latex": "tex",
    }
    return aliases.get(fmt, fmt)


def default_extension(fmt: str) -> str:
    table = {
        "md": ".md", "html": ".html", "docx": ".docx", "pdf": ".pdf",
        "tex": ".tex", "rtf": ".rtf", "epub": ".epub", "odt": ".odt",
        "pptx": ".pptx", "rst": ".rst", "asciidoc": ".adoc",
    }
    return table.get(fmt, "." + fmt)


# ---------------------------------------------------------------------------
# Conversion
# ---------------------------------------------------------------------------
def convert_md_passthrough(input_path: str, out_path: str) -> int:
    """No-op: just copy if input is already markdown."""
    if os.path.abspath(input_path) == os.path.abspath(out_path):
        return 0
    shutil.copy2(input_path, out_path)
    return 0


def convert_via_pandoc(input_path: str, out_format: str, out_path: str,
                       extra_args: list[str] | None = None) -> int:
    pandoc = find_pandoc()
    if not pandoc:
        sys.stderr.write(
            "Pandoc is not installed. To enable conversion to non-Markdown\n"
            "formats, install Pandoc:\n"
            "  macOS:    brew install pandoc\n"
            "  Linux:    apt install pandoc  (or your distro's package manager)\n"
            "  Windows:  choco install pandoc  (or download from pandoc.org)\n"
            "\n"
            "For PDF output, also install a LaTeX engine:\n"
            "  brew install --cask mactex-no-gui   (macOS)\n"
            "  apt install texlive                  (Linux)\n"
            "  install MiKTeX or TeX Live           (Windows)\n"
        )
        return 4

    cmd = [pandoc, input_path, "-o", out_path]

    # PDF needs a LaTeX engine
    if out_format == "pdf":
        latex = find_latex()
        if not latex:
            sys.stderr.write(
                "PDF output requires a LaTeX engine (pdflatex / xelatex / "
                "lualatex / tectonic). None found on PATH.\n"
                "Install texlive (Linux), MacTeX (macOS), or MiKTeX (Windows).\n"
            )
            return 5
        cmd.extend(["--pdf-engine", os.path.basename(latex).split(".")[0]])

    # Pandoc EPUB / DOCX produces best results with --reference-doc / metadata
    # but we keep it simple here.

    if extra_args:
        cmd.extend(extra_args)

    print(f"Running: {' '.join(cmd)}", file=sys.stderr)
    try:
        result = subprocess.run(cmd, check=False, capture_output=True, text=True)
    except Exception as e:
        sys.stderr.write(f"Failed to run pandoc: {e}\n")
        return 6

    if result.returncode != 0:
        sys.stderr.write(f"Pandoc exited with code {result.returncode}.\n")
        if result.stderr:
            sys.stderr.write(result.stderr)
        return result.returncode

    return 0


def convert(input_path: str, out_format: str, out_path: str | None = None,
            extra_args: list[str] | None = None) -> int:
    out_format = normalize_format(out_format)
    if out_path is None:
        out_path = str(Path(input_path).with_suffix(default_extension(out_format)))

    if out_format in ("md", "markdown"):
        return convert_md_passthrough(input_path, out_path)

    if out_format in PANDOC_FORMATS:
        return convert_via_pandoc(input_path, out_format, out_path, extra_args)

    sys.stderr.write(f"Unsupported output format: {out_format}\n")
    sys.stderr.write(f"Supported: {', '.join(sorted(PANDOC_FORMATS))}\n")
    return 7


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
def list_formats() -> None:
    print("Supported output formats:")
    for fmt in sorted(PANDOC_FORMATS):
        ext = default_extension(fmt)
        renderer = "native" if fmt in ("md", "markdown") else "pandoc"
        if fmt == "pdf":
            renderer = "pandoc + LaTeX"
        print(f"  {fmt:<10} ({ext})  via {renderer}")


def self_test() -> None:
    print("convert_output.py self-test")
    print("=" * 40)
    pandoc_v = pandoc_version()
    latex = find_latex()
    print(f"Pandoc:       {pandoc_v or 'NOT INSTALLED'}")
    print(f"LaTeX engine: {latex or 'NOT INSTALLED (PDF output unavailable)'}")
    print()
    print("Conversion availability:")
    print("  md      [ok]   always (passthrough)")
    if pandoc_v:
        for fmt in ("html", "docx", "tex", "rtf", "epub", "odt", "pptx"):
            print(f"  {fmt:<7} [ok]   via pandoc")
        if latex:
            print(f"  pdf     [ok]   via pandoc + {os.path.basename(latex)}")
        else:
            print(f"  pdf     [..]  pandoc OK; LaTeX engine missing")
    else:
        for fmt in ("html", "docx", "pdf", "tex", "rtf", "epub", "odt", "pptx"):
            note = "install pandoc" + (" + LaTeX" if fmt == "pdf" else "")
            print(f"  {fmt:<7} [..]  {note}")
    print()
    if not pandoc_v:
        print("To enable non-MD output formats, install pandoc:")
        print("  https://pandoc.org/installing.html")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Convert Markdown papers to other formats.")
    p.add_argument("--input", help="Input Markdown path.")
    p.add_argument("--to", default="md",
                   help="Target format (md / html / docx / pdf / tex / rtf / epub / odt / pptx).")
    p.add_argument("--out", default=None, help="Output path.")
    p.add_argument("--bibliography", default=None,
                   help="Path to bibliography for --citeproc.")
    p.add_argument("--csl", default=None,
                   help="Path to CSL file for citation style.")
    p.add_argument("--extra", default="",
                   help="Extra Pandoc args, comma-separated.")
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

    extra: list[str] = []
    if args.bibliography:
        extra += ["--citeproc", "--bibliography", args.bibliography]
    if args.csl:
        extra += ["--csl", args.csl]
    if args.extra:
        extra += [s.strip() for s in args.extra.split(",") if s.strip()]

    return convert(args.input, args.to, args.out, extra)


if __name__ == "__main__":
    raise SystemExit(main())
