# File Format Support

The `read-research-paper` skill (and the other two via integration)
can **read** the formats below as input and **write** outputs in any
of the supported formats. The same Python toolchains live in
`research-paper/toolchains/convert_output.py` (write) and
`read-research-paper/toolchains/read_any_file.py` (read).

> **Posture:** every format has a "no-extra-deps" path or a clear
> "install X to enable" message. The skills never silently skip a
> file format — failure is always explicit.

---

## 1. Read (input formats)

| Extension                 | Library used               | Install               | Notes                                    |
| ------------------------- | -------------------------- | --------------------- | ---------------------------------------- |
| `.md`, `.markdown`         | stdlib                     | (none)                 | Always available                          |
| `.txt`                     | stdlib                     | (none)                 | Always available                          |
| `.tex`, `.latex`           | stdlib + regex              | (none)                 | Light de-LaTeX; preserves text content    |
| `.html`, `.htm`            | `beautifulsoup4` (or regex) | `pip install beautifulsoup4` | Falls back to regex if BS4 missing |
| `.json`                    | stdlib                     | (none)                 | Always available                          |
| `.csv`, `.tsv`             | stdlib (or `pandas`)        | `pip install pandas`   | pandas gives better Markdown rendering    |
| `.pdf`                     | `pdfplumber` or `pypdf`     | `pip install pdfplumber` (recommended) | pdfplumber adds table extraction |
| `.docx`                    | `python-docx`               | `pip install python-docx` |                                           |
| `.pptx`                    | `python-pptx`               | `pip install python-pptx` | Extracts text from all shapes              |
| `.xlsx`, `.xls`            | `pandas` + `openpyxl`       | `pip install pandas openpyxl` |                                  |
| `.rtf`                     | `striprtf` (or regex)       | `pip install striprtf`  | Regex fallback when missing               |
| `.epub`                    | `ebooklib` + `bs4`          | `pip install ebooklib beautifulsoup4` |                                |
| `.png`, `.jpg`, `.tiff`, etc. | `pytesseract` + `PIL`     | `pip install pytesseract Pillow` + Tesseract OCR | OCR for image-based papers |

### One-line install for everything

```bash
pip install pdfplumber python-docx python-pptx pandas openpyxl \
            beautifulsoup4 striprtf ebooklib pytesseract Pillow
```

(Plus install Tesseract OCR for `.png`/`.jpg`/`.tiff` — system package
manager: `brew install tesseract` / `apt install tesseract-ocr` /
choco / scoop on Windows.)

### Self-test

```bash
python skills/read-research-paper/toolchains/read_any_file.py --self-test
python skills/read-research-paper/toolchains/read_any_file.py --list-formats
```

### Usage

```bash
# Read any input file into structured JSON + extracted text
python read_any_file.py --input paper.pdf --text-out paper.txt
python read_any_file.py --input slides.pptx --out slides.json
python read_any_file.py --input chart.png  --text-out chart-ocr.txt

# Or via the orchestrator (triggers the read-research-paper skill):
/read-research-paper ./paper.pdf
/read-research-paper ./slides.pptx
/read-research-paper ./diagram.png
```

---

## 2. Write (output formats)

The `research-paper` skill produces Markdown by default. To convert
to other formats, the toolchain wraps Pandoc.

| Format    | Extension | Renderer        | Requires                                  |
| --------- | --------- | --------------- | ----------------------------------------- |
| Markdown   | `.md`      | native          | (always available)                         |
| HTML       | `.html`    | pandoc          | `pandoc`                                   |
| DOCX        | `.docx`    | pandoc          | `pandoc`                                   |
| PDF         | `.pdf`     | pandoc + LaTeX  | `pandoc` + `pdflatex`/`xelatex`/`tectonic` |
| LaTeX       | `.tex`     | pandoc          | `pandoc`                                   |
| RTF         | `.rtf`     | pandoc          | `pandoc`                                   |
| EPUB        | `.epub`    | pandoc          | `pandoc`                                   |
| ODT         | `.odt`     | pandoc          | `pandoc`                                   |
| PPTX        | `.pptx`    | pandoc          | `pandoc` (note: not great for technical papers; OK for slides) |

### Install Pandoc

| OS        | Command                                                         |
| --------- | --------------------------------------------------------------- |
| macOS      | `brew install pandoc` (and `brew install --cask mactex-no-gui` for PDF) |
| Linux      | `apt install pandoc texlive` (or your distro's equivalents)      |
| Windows    | `choco install pandoc miktex`  (or scoop, or installers from pandoc.org) |

### Self-test

```bash
python skills/research-paper/toolchains/convert_output.py --self-test
python skills/research-paper/toolchains/convert_output.py --list-formats
```

### Usage

```bash
# Convert paper-final.md to PDF (requires pandoc + LaTeX)
python convert_output.py --input paper-final.md --to pdf --out paper.pdf

# Convert to DOCX with citations in IEEE style
python convert_output.py --input paper-final.md --to docx \
    --bibliography bibliography.yaml --csl ieee.csl

# Convert to HTML (lightest dependency)
python convert_output.py --input paper-final.md --to html
```

The skill auto-invokes this when the user requests a non-Markdown
output:

```
/research "topic" --output paper.pdf
/research "topic" --output paper.docx
/research "topic" --output paper.html
```

---

## 3. End-to-end format flow

```
INPUT (any format)
      │
      ▼
   read_any_file.py (read-research-paper skill)
      │
      ▼
   structured paper-data.json
      │
      ▼
   visual rendering or paper writing
      │
      ▼
   paper-visual.md / paper-final.md (Markdown)
      │
      ▼
   convert_output.py (research-paper skill)
      │
      ▼
OUTPUT (any format: PDF, DOCX, HTML, LaTeX, etc.)
```

Each step is a discrete tool — the user can stop at the Markdown
intermediate, or convert further.

---

## 4. Graceful degradation matrix

| Scenario                                 | Behavior                                              |
| ---------------------------------------- | ----------------------------------------------------- |
| User asks to read `.pdf` but pdf libs missing | Clear "install X" message; fail honestly             |
| User asks to convert to `.pdf` but pandoc missing | Clear "install pandoc" message; output `.md` instead, flag |
| User asks to convert to `.pdf` but LaTeX missing | Clear "install LaTeX" message; output `.html` instead, flag |
| User asks to read `.png` but no OCR installed | Clear "install pytesseract + Tesseract" message     |
| User asks to read unknown extension       | Try as plain text with warning; flag in `Known-gaps.md` |

Every degradation is logged in `Known-gaps.md` so the user knows
exactly what was lost.

---

## 5. Performance notes

- PDF text extraction with `pdfplumber`: ~1 page/second.
- DOCX / PPTX extraction: nearly instant (XML parse).
- OCR with `pytesseract`: ~5–15 seconds per page (depending on image
  resolution and system).
- Pandoc conversion to HTML / DOCX / TeX: < 1 second for typical
  papers.
- Pandoc → PDF (via LaTeX): 5–30 seconds on first run; faster after
  cache warm-up.

For batch processing, run conversions in parallel via the agent
runtime's parallel-task primitive.
