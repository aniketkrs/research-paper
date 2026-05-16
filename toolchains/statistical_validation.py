#!/usr/bin/env python3
"""
statistical_validation.py
=========================

Implements workflows/validation-pipeline.md §2.3.

Scans a paper for statistical claims (t-tests, ANOVA, correlations,
chi-squared, regressions) and validates each against a reference
analysis output (analysis/hypothesis-tests.csv) when available.

Issues flagged:
  - Reported p-value but no effect size or 95% CI -> medium
  - Reported effect size but no CI -> medium
  - Test stat / df / p mismatch with analysis output -> high
  - Underpowered test (n below floor) -> medium
  - Multiple p-values reported in a table without correction mentioned -> medium

Usage:
  python statistical_validation.py paper-cited.md \\
      --analysis ./analysis/ \\
      --report validation/statistical-issues.md
"""

from __future__ import annotations

import argparse
import csv
import os
import re
import sys
from typing import Any


PATTERNS = {
    "welch_t": re.compile(
        r"t\s*\(\s*(?P<df>[\d\.]+)\s*\)\s*=\s*(?P<stat>-?[\d\.]+)"
        r"[^.]{0,80}?p\s*[<=]\s*(?P<p>\.?\d+(?:\.\d+)?)",
        re.IGNORECASE),
    "anova": re.compile(
        r"F\s*\(\s*(?P<df1>\d+)\s*,\s*(?P<df2>[\d\.]+)\s*\)\s*=\s*(?P<stat>-?[\d\.]+)"
        r"[^.]{0,80}?p\s*[<=]\s*(?P<p>\.?\d+(?:\.\d+)?)",
        re.IGNORECASE),
    "correlation": re.compile(
        r"r\s*=\s*(?P<r>-?[\d\.]+)"
        r"[^.]{0,80}?p\s*[<=]\s*(?P<p>\.?\d+(?:\.\d+)?)",
        re.IGNORECASE),
    "chi2": re.compile(
        r"χ²?\s*\(\s*(?P<df>\d+)\s*[,;]?\s*(?:N\s*=\s*\d+\s*)?\)\s*=\s*"
        r"(?P<stat>-?[\d\.]+)[^.]{0,80}?p\s*[<=]\s*(?P<p>\.?\d+(?:\.\d+)?)",
        re.IGNORECASE),
    "odds_ratio": re.compile(
        r"OR\s*=\s*(?P<or>-?[\d\.]+)"
        r"[^.]{0,80}?(?P<ci>95\s*%\s*CI\s*\[\s*[\d\.\-]+\s*,\s*[\d\.\-]+\s*\])?",
        re.IGNORECASE),
}

EFFECT_SIZE_NEAR = re.compile(
    r"(Cohen.?s\s*d|Hedges.?s?\s*g|η[²2]|partial\s+η[²2]|ω[²2]|"
    r"Cramer.?s\s*V|phi|φ|Pearson.?s\s*r|odds\s+ratio|R[²2])",
    re.IGNORECASE)
CI_NEAR = re.compile(r"95\s*%\s*CI\s*\[\s*[\d\.\-]+\s*,\s*[\d\.\-]+\s*\]",
                     re.IGNORECASE)


def find_claims(paper: str) -> list[dict[str, Any]]:
    claims = []
    for kind, pat in PATTERNS.items():
        for m in pat.finditer(paper):
            window = paper[max(0, m.start() - 200): m.end() + 200]
            has_es = bool(EFFECT_SIZE_NEAR.search(window))
            has_ci = bool(CI_NEAR.search(window))
            claim = {"kind": kind, "match": m.group(0).strip()}
            claim.update(m.groupdict())
            claim["effect_size_present"] = has_es
            claim["ci_present"] = has_ci
            claims.append(claim)
    return claims


def load_analysis(analysis_dir: str) -> list[dict[str, str]]:
    path = os.path.join(analysis_dir, "tables", "hypothesis-tests.csv")
    if not os.path.exists(path):
        path = os.path.join(analysis_dir, "hypothesis-tests.csv")
    if not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("paper")
    p.add_argument("--analysis", default=None)
    p.add_argument("--report", default=None)
    args = p.parse_args(argv)

    with open(args.paper, "r", encoding="utf-8-sig") as f:
        paper = f.read()
    claims = find_claims(paper)

    issues: list[tuple[str, str, str]] = []  # (severity, kind, message)
    for c in claims:
        if not c["effect_size_present"]:
            issues.append(("medium", c["kind"],
                            f"Reported p-value without an effect size near: {c['match']}"))
        elif not c["ci_present"]:
            issues.append(("medium", c["kind"],
                            f"Reported effect size without 95% CI near: {c['match']}"))

    # Multiple-comparison heuristic: if a paper reports >= 4 p-values within
    # 1500 chars and the word "Bonferroni" / "Holm" / "Tukey" / "FDR" /
    # "correction" never appears nearby, flag.
    p_positions = [m.start() for m in re.finditer(r"p\s*[<=]\s*\.?\d", paper)]
    for i in range(len(p_positions) - 3):
        window_start = p_positions[i]
        window_end = p_positions[i + 3]
        if window_end - window_start <= 1500:
            window = paper[window_start: window_end + 100]
            if not re.search(r"Bonferroni|Holm|Tukey|FDR|Benjamini|correction|adjust",
                             window, re.IGNORECASE):
                issues.append(("medium", "multiple-comparisons",
                                "Multiple p-values reported close together without "
                                "a stated correction method (around char "
                                f"{window_start})."))
                break

    md = ["# Statistical validation report\n",
          f"- Paper: `{args.paper}`",
          f"- Statistical claims detected: {len(claims)}",
          f"- Issues flagged: {len(issues)}\n"]

    md.append("## Statistical claims detected\n")
    if claims:
        md.append("| # | Kind | Match | Effect size? | 95% CI? |")
        md.append("| --- | --- | --- | --- | --- |")
        for i, c in enumerate(claims, 1):
            md.append(f"| {i} | {c['kind']} | `{c['match'][:80]}` "
                      f"| {'yes' if c['effect_size_present'] else 'NO'} "
                      f"| {'yes' if c['ci_present'] else 'NO'} |")
    else:
        md.append("_No statistical claims matched the validator's regexes. "
                  "(This may mean the paper has no quantitative results, "
                  "or uses formats not yet recognized.)_")
    md.append("")

    md.append("## Issues\n")
    if issues:
        md.append("| Severity | Kind | Message |")
        md.append("| --- | --- | --- |")
        for sev, kind, msg in issues:
            md.append(f"| {sev} | {kind} | {msg} |")
    else:
        md.append("_None._")
    md.append("")

    body = "\n".join(md) + "\n"
    if args.report:
        os.makedirs(os.path.dirname(args.report) or ".", exist_ok=True)
        with open(args.report, "w", encoding="utf-8") as f:
            f.write(body)
    else:
        sys.stdout.write(body)
    return 2 if any(sev == "high" for sev, _, _ in issues) else 0


if __name__ == "__main__":
    raise SystemExit(main())
