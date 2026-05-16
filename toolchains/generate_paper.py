#!/usr/bin/env python3
"""
generate_paper.py
=================

Convenience wrapper that bootstraps a paper-writing project. It does NOT
write the paper itself — the LLM does that, following SKILL.md and the
workflows in this skill. What it does is:

  1. Create the working-directory structure expected by the workflows.
  2. Drop in template stub files (paper-spec.md, outline.md,
     bibliography.yaml, methodology.md, figures-plan.md).
  3. Print a short "next steps" message reminding the model / user what
     to read next.

Usage:
  python generate_paper.py --topic "LLMs in code review" \\
                           --format ieee \\
                           --out ./paper-llm-code-review/
"""

from __future__ import annotations

import argparse
import datetime as dt
import os
import textwrap


PAPER_SPEC_STUB = """# Paper specification

Generated: {now}

## Topic and scope
- Topic: {topic}
- Specific research question(s):
  1. ...
- Out of scope:
  - ...

## Output
- Type: {paper_type}
- Format: {format}
- Audience: ...
- Target length: ...
- Citation style: {citation_style}

## Inputs from user
- Dataset: ...
- Code: ...
- References: ...

## Constraints
- Deadline: ...
- Anonymization required: ...
- Language: en-US
- Special venue requirements: ...

## Defaults assumed
- ...

## Plan
- Phase 1: literature review
- Phase 2: methodology design
- Phase 3: data analysis
- Phase 4: drafting
- Phase 5: citation pass
- Phase 6: validation pass
- Phase 7: review pass
- Phase 8: final delivery

## Risks / unknowns
- ...
"""

OUTLINE_STUB = """# Outline

(Fill in section by section, copying the structure from
templates/{format}-paper.md and turning each <<...>> slot into a
1-2-sentence statement of what that section will say.)
"""

BIBLIOGRAPHY_STUB = """# bibliography.yaml — single source of truth for citations.
# Schema: schemas/citation-schema.json
# Format: list of entries.

# Example entry:
# - id: smith_2023_llm
#   type: article-journal
#   authors:
#     - {family: Smith, given: Jane A.}
#     - {family: Doe, given: Alice}
#   year: 2023
#   title: "Large language models in software engineering: A systematic survey"
#   container: "ACM Computing Surveys"
#   volume: 55
#   issue: 4
#   pages: "1-37"
#   doi: "10.1145/3589334"
#   verification: unverified-offline

references: []
"""

METHODOLOGY_STUB = """# Methodology

(To be drafted using prompts/methodology-design.md and the relevant
blueprint in references/methodology-guide.md.)
"""

FIGURES_PLAN_STUB = """# figures-plan.md — every figure / table to be produced.
# Schema: schemas/figure-schema.json + schemas/table-schema.json

# Example entry:
# - id: figure-1
#   section: 4. Method
#   type: architecture-diagram
#   source: described in section 4.1
#   caption: "System architecture: input → preprocessor → encoder →
#     classifier → output."
#   render_method: mermaid

figures: []
tables: []
"""

KNOWN_GAPS_STUB = """# Known gaps

(This file is filled in automatically as the validation and review passes
identify open issues. Items listed here MUST be addressed before
submission.)
"""

NEXT_STEPS = """\
# Next steps

The working directory is ready. The model should now:

1. Open paper-spec.md and confirm / extend the spec.
2. Read SKILL.md and workflows/research-orchestration.md.
3. Run the orchestration phases:
   - §3 Literature review (writes bibliography.yaml + lit-themes.md)
   - §4 Methodology (writes methodology.md)
   - §5 Data analysis (if applicable; writes analysis/)
   - §6 Visualization planning (writes figures-plan.md + figures/)
   - §7 Drafting (writes sections/ + paper-draft.md)
   - §8 Citation pass (writes paper-cited.md)
   - §9 Validation pass (writes validation/)
   - §10 Review pass (writes review/ + paper-final.md)
   - §11 Final delivery (writes index.md)
"""


def write(path: str, body: str) -> None:
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--topic", required=True)
    p.add_argument("--format", default="arxiv",
                   choices=["arxiv", "ieee", "acm", "nature", "harvard",
                            "literature-review", "thesis-chapter", "whitepaper",
                            "survey", "policy"])
    p.add_argument("--paper-type", default="research-paper")
    p.add_argument("--citation-style", default=None,
                   help="Defaults to a sensible style for the chosen format.")
    p.add_argument("--out", default="./paper-out/")
    args = p.parse_args(argv)

    style_default = {
        "arxiv": "apa",
        "ieee": "ieee",
        "acm": "ieee",  # ACM Reference Format is numeric; "ieee" closest in this script
        "nature": "nature",
        "harvard": "harvard",
        "literature-review": "harvard",
        "thesis-chapter": "harvard",
        "whitepaper": "harvard",
        "survey": "ieee",
        "policy": "harvard",
    }
    citation_style = args.citation_style or style_default[args.format]

    out = os.path.abspath(args.out)
    os.makedirs(out, exist_ok=True)
    for sub in ("sections", "figures", "tables", "analysis", "validation", "review"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)

    now = dt.datetime.now().isoformat(timespec="seconds")

    write(os.path.join(out, "paper-spec.md"),
          PAPER_SPEC_STUB.format(now=now, topic=args.topic,
                                  paper_type=args.paper_type,
                                  format=args.format,
                                  citation_style=citation_style))
    write(os.path.join(out, "outline.md"),
          OUTLINE_STUB.format(format=args.format))
    write(os.path.join(out, "bibliography.yaml"), BIBLIOGRAPHY_STUB)
    write(os.path.join(out, "methodology.md"), METHODOLOGY_STUB)
    write(os.path.join(out, "figures-plan.md"), FIGURES_PLAN_STUB)
    write(os.path.join(out, "Known-gaps.md"), KNOWN_GAPS_STUB)
    write(os.path.join(out, "NEXT-STEPS.md"), NEXT_STEPS)

    print(f"Bootstrapped paper project at: {out}")
    print()
    print(NEXT_STEPS)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
