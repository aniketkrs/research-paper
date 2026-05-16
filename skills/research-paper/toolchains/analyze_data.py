#!/usr/bin/env python3
"""
analyze_data.py
===============

Implements the data-analysis pipeline (workflows/data-analysis-pipeline.md).

Reads a CSV / Excel / JSON / Parquet dataset and produces:

  analysis/
    data-dictionary.md
    data-dictionary.csv
    missing-data.md
    univariate-summary.md
    bivariate-summary.md
    hypothesis-tests.md           (skeleton, even with no hypothesis)
    findings.md                   (writer agent expands this)
    figures/dist_<col>.png         (distributions per numeric column)
    figures/corr-heatmap.png       (correlation heatmap if >= 2 numerics)
    tables/descriptive.csv

Designed for graceful degradation if pandas / matplotlib aren't installed.

Usage:
  python analyze_data.py --input data.csv --out ./analysis/ [--outcome y]
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from typing import Any


def _try_imports():
    try:
        import pandas as pd  # type: ignore
    except ImportError:
        pd = None
    try:
        import numpy as np  # type: ignore
    except ImportError:
        np = None
    try:
        import matplotlib  # type: ignore
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt  # type: ignore
    except ImportError:
        plt = None
    try:
        import scipy.stats as stats  # type: ignore
    except ImportError:
        stats = None
    return pd, np, plt, stats


def safe_mkdirs(out: str) -> None:
    for sub in ("", "figures", "tables"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)


def load_dataset(path: str, pd):
    if pd is None:
        with open(path, "r", encoding="utf-8") as f:
            return list(csv.DictReader(f))
    if path.endswith(".csv"):
        return pd.read_csv(path)
    if path.endswith(".tsv"):
        return pd.read_csv(path, sep="\t")
    if path.endswith(".xlsx") or path.endswith(".xls"):
        return pd.read_excel(path)
    if path.endswith(".json"):
        return pd.read_json(path)
    if path.endswith(".parquet"):
        return pd.read_parquet(path)
    return pd.read_csv(path)


def write_text(path: str, body: str) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(body)


def data_dictionary(df, pd, out: str) -> str:
    rows: list[dict[str, Any]] = []
    if pd is not None and hasattr(df, "columns"):
        for col in df.columns:
            s = df[col]
            row: dict[str, Any] = {"column": col, "dtype": str(s.dtype)}
            row["n_missing"] = int(s.isna().sum())
            row["pct_missing"] = round(100.0 * row["n_missing"] / max(len(s), 1), 2)
            row["n_unique"] = int(s.nunique(dropna=True))
            try:
                if s.dtype.kind in "biufc":
                    row["mean"] = round(float(s.mean()), 4) if s.notna().any() else None
                    row["sd"] = round(float(s.std(ddof=1)), 4) if s.notna().any() else None
                    row["min"] = float(s.min()) if s.notna().any() else None
                    row["median"] = float(s.median()) if s.notna().any() else None
                    row["max"] = float(s.max()) if s.notna().any() else None
            except Exception:
                pass
            rows.append(row)
    else:
        if df:
            cols = list(df[0].keys())
            for col in cols:
                vals = [r[col] for r in df if r.get(col) not in (None, "")]
                row = {"column": col, "n_missing": len(df) - len(vals),
                       "n_unique": len(set(vals))}
                try:
                    nums = [float(v) for v in vals]
                    if nums:
                        row["mean"] = round(sum(nums) / len(nums), 4)
                        row["min"] = min(nums)
                        row["max"] = max(nums)
                except Exception:
                    pass
                rows.append(row)

    # Write CSV
    csv_path = os.path.join(out, "data-dictionary.csv")
    if rows:
        keys = sorted({k for r in rows for k in r.keys()})
        with open(csv_path, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            for r in rows:
                writer.writerow(r)
    # Write Markdown
    md_path = os.path.join(out, "data-dictionary.md")
    md = ["# Data dictionary\n"]
    if rows:
        keys = sorted({k for r in rows for k in r.keys()})
        md.append("| " + " | ".join(keys) + " |")
        md.append("| " + " | ".join(["---"] * len(keys)) + " |")
        for r in rows:
            md.append("| " + " | ".join(str(r.get(k, "")) for k in keys) + " |")
    write_text(md_path, "\n".join(md) + "\n")
    return md_path


def univariate(df, pd, plt, out: str) -> str:
    md = ["# Univariate summary\n"]
    figs_dir = os.path.join(out, "figures")
    if pd is None or not hasattr(df, "select_dtypes"):
        md.append("_(pandas not installed; install pandas + matplotlib for full analysis)_\n")
        write_text(os.path.join(out, "univariate-summary.md"), "\n".join(md))
        return os.path.join(out, "univariate-summary.md")

    nums = df.select_dtypes(include="number")
    cats = df.select_dtypes(exclude="number")
    md.append(f"- Numeric columns: {list(nums.columns)}")
    md.append(f"- Categorical columns: {list(cats.columns)}")
    md.append("")

    md.append("## Numeric variables")
    md.append("")
    md.append("| Column | n | mean | sd | min | median | max |")
    md.append("| --- | --- | --- | --- | --- | --- | --- |")
    for col in nums.columns:
        s = nums[col].dropna()
        if len(s) == 0:
            continue
        md.append(f"| {col} | {len(s)} | {s.mean():.3f} | {s.std(ddof=1):.3f} | "
                  f"{s.min()} | {s.median()} | {s.max()} |")
        if plt is not None:
            try:
                fig, ax = plt.subplots(figsize=(5, 3))
                ax.hist(s, bins=min(30, max(10, len(s) // 5)), color="#56B4E9", edgecolor="white")
                ax.set_xlabel(col)
                ax.set_ylabel("Count")
                ax.set_title(f"Distribution of {col}")
                fig.savefig(os.path.join(figs_dir, f"dist_{col}.png"), dpi=200, bbox_inches="tight")
                plt.close(fig)
            except Exception:
                pass
    md.append("")
    md.append("## Categorical variables")
    md.append("")
    for col in cats.columns:
        vc = df[col].value_counts(dropna=False).head(10)
        md.append(f"### {col}")
        md.append("")
        md.append("| Value | Count |")
        md.append("| --- | --- |")
        for v, c in vc.items():
            md.append(f"| {v} | {int(c)} |")
        md.append("")
    path = os.path.join(out, "univariate-summary.md")
    write_text(path, "\n".join(md) + "\n")
    return path


def bivariate(df, pd, plt, out: str, outcome: str | None) -> str:
    md = ["# Bivariate summary\n"]
    if pd is None or not hasattr(df, "select_dtypes"):
        md.append("_(pandas not installed; install pandas for full analysis)_\n")
        write_text(os.path.join(out, "bivariate-summary.md"), "\n".join(md))
        return os.path.join(out, "bivariate-summary.md")

    nums = df.select_dtypes(include="number")

    if outcome and outcome in df.columns:
        md.append(f"## Bivariate against outcome `{outcome}`\n")
        if outcome in nums.columns:
            md.append("| Predictor | r | n |")
            md.append("| --- | --- | --- |")
            for col in nums.columns:
                if col == outcome:
                    continue
                pair = df[[outcome, col]].dropna()
                if len(pair) >= 5:
                    r = pair[outcome].corr(pair[col])
                    md.append(f"| {col} | {r:.3f} | {len(pair)} |")
        md.append("")
    else:
        md.append("## Correlation matrix (numeric variables)\n")
        if len(nums.columns) >= 2:
            corr = nums.corr()
            md.append("| | " + " | ".join(corr.columns) + " |")
            md.append("| --- |" + " --- |" * len(corr.columns))
            for idx, row in corr.iterrows():
                md.append(f"| {idx} | " + " | ".join(f"{v:.2f}" for v in row.values) + " |")
            if plt is not None:
                try:
                    fig, ax = plt.subplots(figsize=(max(4, 0.5 * len(corr)), max(4, 0.5 * len(corr))))
                    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
                    ax.set_xticks(range(len(corr.columns)))
                    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
                    ax.set_yticks(range(len(corr.index)))
                    ax.set_yticklabels(corr.index)
                    for i in range(len(corr.index)):
                        for j in range(len(corr.columns)):
                            ax.text(j, i, f"{corr.values[i, j]:.2f}",
                                    ha="center", va="center", fontsize=8)
                    fig.colorbar(im, ax=ax)
                    fig.savefig(os.path.join(out, "figures", "corr-heatmap.png"),
                                dpi=200, bbox_inches="tight")
                    plt.close(fig)
                except Exception:
                    pass
    path = os.path.join(out, "bivariate-summary.md")
    write_text(path, "\n".join(md) + "\n")
    return path


def missing_report(df, pd, out: str) -> str:
    md = ["# Missing data report\n"]
    if pd is None or not hasattr(df, "isna"):
        md.append("_(pandas not installed)_\n")
        write_text(os.path.join(out, "missing-data.md"), "\n".join(md))
        return os.path.join(out, "missing-data.md")
    miss = df.isna().sum()
    pct = (miss / max(len(df), 1) * 100).round(2)
    md.append("| Column | Missing | % Missing |")
    md.append("| --- | --- | --- |")
    for col in df.columns:
        md.append(f"| {col} | {int(miss[col])} | {pct[col]} |")
    md.append("")
    n_full = (df.notna().all(axis=1)).sum()
    md.append(f"**Complete rows:** {int(n_full)} / {len(df)} "
              f"({(100.0 * n_full / max(len(df), 1)):.1f}%)")
    path = os.path.join(out, "missing-data.md")
    write_text(path, "\n".join(md) + "\n")
    return path


def hypothesis_skeleton(out: str, outcome: str | None) -> str:
    md = [
        "# Hypothesis tests\n",
        "_This file is a skeleton. Fill in hypotheses from `paper-spec.md` "
        "and re-run with `--hypotheses` set._\n",
    ]
    if outcome:
        md.append(f"Outcome variable: `{outcome}`\n")
    write_text(os.path.join(out, "hypothesis-tests.md"), "\n".join(md))
    return os.path.join(out, "hypothesis-tests.md")


def findings_stub(out: str, outcome: str | None) -> str:
    md = [
        "# Findings — auto-generated by analyze_data.py\n",
        "## Sample",
        "- n: see analysis/data-dictionary.md",
        "- After exclusions: TBD",
        "- Demographics: TBD\n",
        "## Descriptive statistics",
        "[Table 1: tables/descriptive.csv]",
        "[Figure 1: figures/corr-heatmap.png]\n",
    ]
    if outcome:
        md.append(f"## Bivariate analyses against `{outcome}`")
        md.append("See bivariate-summary.md.\n")
    md.append("## Hypothesis tests")
    md.append("See hypothesis-tests.md (writer agent expands).\n")
    md.append("## Robustness checks")
    md.append("- Re-run excluding outliers (Tukey 1.5×IQR)")
    md.append("- Bootstrap n_boot=2000 for main effects")
    md.append("- Sensitivity to imputation (MICE) where missing > 5%\n")
    md.append("## Open questions / anomalies")
    md.append("- TBD\n")
    write_text(os.path.join(out, "findings.md"), "\n".join(md))
    return os.path.join(out, "findings.md")


def descriptive_csv(df, pd, out: str) -> None:
    if pd is None or not hasattr(df, "describe"):
        return
    desc = df.describe(include="all").transpose()
    desc.to_csv(os.path.join(out, "tables", "descriptive.csv"))


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Analyze a dataset for academic reporting.")
    p.add_argument("--input", required=False)
    p.add_argument("--out", default="./analysis/")
    p.add_argument("--outcome", default=None)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)

    pd, np, plt, stats = _try_imports()
    if args.self_test:
        print("pandas:", pd is not None)
        print("numpy:", np is not None)
        print("matplotlib:", plt is not None)
        print("scipy.stats:", stats is not None)
        return 0

    if not args.input:
        p.error("--input is required (or use --self-test)")

    safe_mkdirs(args.out)
    df = load_dataset(args.input, pd)

    paths = []
    paths.append(data_dictionary(df, pd, args.out))
    paths.append(missing_report(df, pd, args.out))
    paths.append(univariate(df, pd, plt, args.out))
    paths.append(bivariate(df, pd, plt, args.out, args.outcome))
    paths.append(hypothesis_skeleton(args.out, args.outcome))
    paths.append(findings_stub(args.out, args.outcome))
    descriptive_csv(df, pd, args.out)

    print("Wrote:")
    for p_ in paths:
        print(" ", p_)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
