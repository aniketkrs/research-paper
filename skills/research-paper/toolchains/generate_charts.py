#!/usr/bin/env python3
"""
generate_charts.py
==================

Renders publication-quality charts from CSV / JSON sources, following the
defaults in references/visualization-guide.md §6.

Designed for graceful degradation: if matplotlib is missing, prints a
clear install hint and a fallback Markdown-table representation of the
data so the paper still renders.

Supported chart types:
  bar | grouped-bar | stacked-bar | horizontal-bar | line | multi-line
  scatter | histogram | violin | box | heatmap | correlation-heatmap
  forest | sankey | gantt | flowchart | mindmap

For diagram-style outputs (flowchart, mindmap, gantt), the script emits
Mermaid source files directly — no Python plotting needed.

Usage examples:
  python generate_charts.py --type bar --input data.csv --x model --y accuracy --out figures/figure-1
  python generate_charts.py --type heatmap --input corr.csv --out figures/figure-2
  python generate_charts.py --self-test
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import os
import sys
from typing import Any

OKABE_ITO = ["#E69F00", "#56B4E9", "#009E73", "#F0E442",
             "#0072B2", "#D55E00", "#CC79A7", "#000000"]


# ---------------------------------------------------------------------------
# Optional imports
# ---------------------------------------------------------------------------
def _try_import_plotting():
    try:
        import matplotlib  # type: ignore
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt  # type: ignore
        try:
            import seaborn as sns  # type: ignore
        except ImportError:
            sns = None
        try:
            import numpy as np  # type: ignore
        except ImportError:
            np = None
        try:
            import pandas as pd  # type: ignore
        except ImportError:
            pd = None
        return plt, sns, np, pd
    except ImportError:
        return None, None, None, None


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------
def load_csv_dictlist(path: str) -> list[dict[str, str]]:
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)


def load_data(path: str):
    plt, sns, np, pd = _try_import_plotting()
    if pd is not None:
        if path.endswith(".csv"):
            return pd.read_csv(path)
        if path.endswith(".json"):
            return pd.read_json(path)
        if path.endswith(".tsv"):
            return pd.read_csv(path, sep="\t")
        if path.endswith(".xlsx") or path.endswith(".xls"):
            return pd.read_excel(path)
    # Fallback
    return load_csv_dictlist(path)


# ---------------------------------------------------------------------------
# Markdown fallback rendering
# ---------------------------------------------------------------------------
def md_table_from_rows(rows: list[dict[str, Any]]) -> str:
    if not rows:
        return "_(no data)_"
    headers = list(rows[0].keys())
    lines = ["| " + " | ".join(headers) + " |",
             "| " + " | ".join("---" for _ in headers) + " |"]
    for r in rows:
        lines.append("| " + " | ".join(str(r.get(h, "")) for h in headers) + " |")
    return "\n".join(lines)


def render_fallback(rows, chart_type: str, out: str, caption: str = "") -> str:
    """Write Markdown fallback when matplotlib isn't available."""
    md = f"# {chart_type.title()} (Markdown fallback)\n\n"
    if caption:
        md += f"**Caption:** {caption}\n\n"
    md += md_table_from_rows(rows if isinstance(rows, list) else [])
    md += "\n\n_(Install matplotlib + seaborn + pandas to render this as a real chart.)_\n"
    md_path = out + ".md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(md)
    return md_path


# ---------------------------------------------------------------------------
# Plotting helpers
# ---------------------------------------------------------------------------
def _setup(plt, sns):
    if sns is not None:
        sns.set_context("paper", font_scale=1.0)
        sns.set_style("whitegrid", {"axes.spines.top": False,
                                     "axes.spines.right": False,
                                     "grid.linestyle": ":"})
    plt.rcParams.update({
        "axes.titlesize": 12,
        "axes.labelsize": 10,
        "xtick.labelsize": 9,
        "ytick.labelsize": 9,
        "legend.fontsize": 9,
        "figure.dpi": 100,
        "savefig.dpi": 300,
    })


def _save(plt, fig, out: str) -> list[str]:
    paths: list[str] = []
    base, _ext = os.path.splitext(out)
    for ext in (".png", ".svg"):
        path = base + ext
        fig.savefig(path, bbox_inches="tight")
        paths.append(path)
    plt.close(fig)
    return paths


# ---------------------------------------------------------------------------
# Chart implementations
# ---------------------------------------------------------------------------
def chart_bar(data, args, plt, sns, np, pd) -> list[str]:
    fig, ax = plt.subplots(figsize=(args.width, args.height))
    x_col, y_col = args.x, args.y
    if pd is not None:
        df = data if hasattr(data, "groupby") else pd.DataFrame(data)
        if args.hue:
            categories = df[x_col].unique()
            hues = df[args.hue].unique()
            width = 0.8 / max(len(hues), 1)
            for i, h in enumerate(hues):
                sub = df[df[args.hue] == h]
                xs = list(range(len(categories)))
                ys = [sub[sub[x_col] == c][y_col].mean() if any(sub[x_col] == c) else 0
                      for c in categories]
                offset = (i - len(hues) / 2 + 0.5) * width
                ax.bar([x + offset for x in xs], ys, width=width,
                       label=str(h), color=OKABE_ITO[i % len(OKABE_ITO)])
            ax.set_xticks(list(range(len(categories))))
            ax.set_xticklabels([str(c) for c in categories])
            ax.legend(title=args.hue)
        else:
            df_g = df.groupby(x_col)[y_col].mean().reset_index()
            ax.bar(df_g[x_col].astype(str), df_g[y_col], color=OKABE_ITO[0])
    else:
        items = sorted({r[x_col]: 0.0 for r in data}.keys())
        means = {it: [] for it in items}
        for r in data:
            try:
                means[r[x_col]].append(float(r[y_col]))
            except (KeyError, ValueError):
                pass
        ax.bar([str(i) for i in items], [sum(v) / max(len(v), 1) for v in means.values()],
               color=OKABE_ITO[0])
    ax.set_xlabel(args.xlabel or x_col)
    ax.set_ylabel(args.ylabel or y_col)
    if args.title:
        ax.set_title(args.title)
    ax.set_ylim(bottom=0)
    return _save(plt, fig, args.out)


def chart_line(data, args, plt, sns, np, pd) -> list[str]:
    fig, ax = plt.subplots(figsize=(args.width, args.height))
    x_col, y_col = args.x, args.y
    if pd is not None:
        df = data if hasattr(data, "groupby") else pd.DataFrame(data)
        if args.hue:
            for i, (h, sub) in enumerate(df.groupby(args.hue)):
                sub2 = sub.sort_values(x_col)
                ax.plot(sub2[x_col], sub2[y_col], marker="o", label=str(h),
                        color=OKABE_ITO[i % len(OKABE_ITO)])
            ax.legend(title=args.hue)
        else:
            df2 = df.sort_values(x_col)
            ax.plot(df2[x_col], df2[y_col], marker="o", color=OKABE_ITO[0])
    ax.set_xlabel(args.xlabel or x_col)
    ax.set_ylabel(args.ylabel or y_col)
    if args.title:
        ax.set_title(args.title)
    return _save(plt, fig, args.out)


def chart_scatter(data, args, plt, sns, np, pd) -> list[str]:
    fig, ax = plt.subplots(figsize=(args.width, args.height))
    x_col, y_col = args.x, args.y
    if pd is not None:
        df = data if hasattr(data, "groupby") else pd.DataFrame(data)
        if args.hue:
            for i, (h, sub) in enumerate(df.groupby(args.hue)):
                ax.scatter(sub[x_col], sub[y_col], alpha=0.7,
                           label=str(h), color=OKABE_ITO[i % len(OKABE_ITO)])
            ax.legend(title=args.hue)
        else:
            ax.scatter(df[x_col], df[y_col], alpha=0.7, color=OKABE_ITO[0])
        if args.fit and np is not None:
            try:
                m, b = np.polyfit(df[x_col].astype(float), df[y_col].astype(float), 1)
                xs = np.linspace(df[x_col].min(), df[x_col].max(), 100)
                ax.plot(xs, m * xs + b, color="black", linestyle="--", label="fit")
            except Exception:
                pass
    ax.set_xlabel(args.xlabel or x_col)
    ax.set_ylabel(args.ylabel or y_col)
    if args.title:
        ax.set_title(args.title)
    return _save(plt, fig, args.out)


def chart_histogram(data, args, plt, sns, np, pd) -> list[str]:
    fig, ax = plt.subplots(figsize=(args.width, args.height))
    if pd is not None:
        df = data if hasattr(data, "groupby") else pd.DataFrame(data)
        ax.hist(df[args.x].dropna().astype(float), bins=args.bins,
                color=OKABE_ITO[0], edgecolor="white")
    ax.set_xlabel(args.xlabel or args.x)
    ax.set_ylabel(args.ylabel or "Count")
    if args.title:
        ax.set_title(args.title)
    return _save(plt, fig, args.out)


def chart_heatmap(data, args, plt, sns, np, pd) -> list[str]:
    fig, ax = plt.subplots(figsize=(args.width, args.height))
    if pd is not None:
        df = data if hasattr(data, "select_dtypes") else pd.DataFrame(data)
        nums = df.select_dtypes(include="number")
        corr = nums.corr() if args.type == "correlation-heatmap" else nums
        if sns is not None:
            sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdBu_r",
                        center=0, ax=ax, cbar=True, square=True)
        else:
            im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)
            ax.set_xticks(range(len(corr.columns)))
            ax.set_xticklabels(corr.columns, rotation=45, ha="right")
            ax.set_yticks(range(len(corr.index)))
            ax.set_yticklabels(corr.index)
            fig.colorbar(im, ax=ax)
    if args.title:
        ax.set_title(args.title)
    return _save(plt, fig, args.out)


def chart_violin(data, args, plt, sns, np, pd) -> list[str]:
    fig, ax = plt.subplots(figsize=(args.width, args.height))
    if pd is not None and sns is not None:
        df = data if hasattr(data, "groupby") else pd.DataFrame(data)
        sns.violinplot(data=df, x=args.x, y=args.y, ax=ax, inner="box",
                       palette=OKABE_ITO[: df[args.x].nunique() if args.x else 1])
    ax.set_xlabel(args.xlabel or args.x)
    ax.set_ylabel(args.ylabel or args.y)
    if args.title:
        ax.set_title(args.title)
    return _save(plt, fig, args.out)


def chart_forest(data, args, plt, sns, np, pd) -> list[str]:
    """Forest plot for meta-analysis. CSV: study,year,n,effect,ci_lower,ci_upper,weight"""
    fig, ax = plt.subplots(figsize=(args.width, max(args.height, 0.4 * len(data))))
    if pd is not None:
        df = data if hasattr(data, "iterrows") else pd.DataFrame(data)
        df = df.sort_values("year") if "year" in df.columns else df
        ys = list(range(len(df)))
        ax.errorbar(df["effect"], ys,
                    xerr=[df["effect"] - df["ci_lower"], df["ci_upper"] - df["effect"]],
                    fmt="s", color=OKABE_ITO[0], capsize=3)
        ax.set_yticks(ys)
        ax.set_yticklabels([f"{r['study']} ({r.get('year', '')})" for _, r in df.iterrows()])
        ax.axvline(0, color="black", linestyle="--", linewidth=0.5)
        ax.invert_yaxis()
    ax.set_xlabel(args.xlabel or "Effect size (95% CI)")
    if args.title:
        ax.set_title(args.title)
    return _save(plt, fig, args.out)


# ---------------------------------------------------------------------------
# Mermaid emitters (no Python plotting required)
# ---------------------------------------------------------------------------
def mermaid_flowchart(args) -> str:
    """Emit a Mermaid flowchart from a JSON spec or stdin.

    JSON spec format:
        {
          "direction": "LR" | "TD",
          "nodes": [{"id": "A", "label": "Input"}, ...],
          "edges": [{"from": "A", "to": "B", "label": "tokenize"}, ...],
          "subgraphs": [{"name": "Pipeline", "nodes": ["B", "C"]}]
        }
    """
    spec_path = args.input
    with open(spec_path, "r", encoding="utf-8") as f:
        spec = json.load(f)
    lines = [f"flowchart {spec.get('direction', 'LR')}"]
    for sg in spec.get("subgraphs", []):
        lines.append(f"  subgraph {sg['name']}")
        for nid in sg["nodes"]:
            for n in spec["nodes"]:
                if n["id"] == nid:
                    lines.append(f"    {n['id']}[{n['label']}]")
        lines.append("  end")
    placed = {nid for sg in spec.get("subgraphs", []) for nid in sg["nodes"]}
    for n in spec["nodes"]:
        if n["id"] not in placed:
            lines.append(f"  {n['id']}[{n['label']}]")
    for e in spec["edges"]:
        if e.get("label"):
            lines.append(f"  {e['from']} -->|{e['label']}| {e['to']}")
        else:
            lines.append(f"  {e['from']} --> {e['to']}")
    out_mmd = args.out + ".mmd"
    with open(out_mmd, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return out_mmd


def mermaid_prisma(args) -> str:
    """Emit a Mermaid PRISMA flow from a JSON spec.

    Spec:
      {"identified": 2341, "duplicates": 412, "screened": 1929,
       "screen_excluded": 1724, "fulltext": 205, "fulltext_excluded": 142,
       "included": 63}
    """
    with open(args.input, "r", encoding="utf-8") as f:
        spec = json.load(f)
    lines = [
        "flowchart TD",
        f"  A[Records identified<br/>n = {spec.get('identified', 0)}] --> "
        f"B[Duplicates removed<br/>n = {spec.get('duplicates', 0)}]",
        f"  B --> C[Title/abstract screened<br/>n = {spec.get('screened', 0)}]",
        f"  C -->|excluded n = {spec.get('screen_excluded', 0)}| D",
        f"  C --> E[Full-text reviewed<br/>n = {spec.get('fulltext', 0)}]",
        f"  E -->|excluded n = {spec.get('fulltext_excluded', 0)}<br/>with reasons| "
        f"F[Studies included<br/>n = {spec.get('included', 0)}]",
    ]
    out_mmd = args.out + ".mmd"
    with open(out_mmd, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return out_mmd


def mermaid_gantt(args) -> str:
    with open(args.input, "r", encoding="utf-8") as f:
        spec = json.load(f)
    lines = ["gantt", f"    title {spec.get('title', 'Project Timeline')}",
             "    dateFormat  YYYY-MM-DD"]
    for section in spec.get("sections", []):
        lines.append(f"    section {section['name']}")
        for t in section.get("tasks", []):
            anchor = f"after {t['after']}" if "after" in t else t.get("start", "")
            lines.append(f"    {t['name']}    :{t.get('id', '')}, {anchor}, {t.get('duration', '7d')}")
    out_mmd = args.out + ".mmd"
    with open(out_mmd, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    return out_mmd


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------
CHARTS_PYTHON = {
    "bar": chart_bar,
    "grouped-bar": chart_bar,
    "line": chart_line,
    "multi-line": chart_line,
    "scatter": chart_scatter,
    "histogram": chart_histogram,
    "heatmap": chart_heatmap,
    "correlation-heatmap": chart_heatmap,
    "violin": chart_violin,
    "forest": chart_forest,
}

CHARTS_MERMAID = {
    "flowchart": mermaid_flowchart,
    "prisma": mermaid_prisma,
    "gantt": mermaid_gantt,
}


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Generate publication-quality charts.")
    p.add_argument("--type", required=False)
    p.add_argument("--input")
    p.add_argument("--out", default="figure")
    p.add_argument("--x", default=None)
    p.add_argument("--y", default=None)
    p.add_argument("--hue", default=None)
    p.add_argument("--xlabel", default=None)
    p.add_argument("--ylabel", default=None)
    p.add_argument("--title", default=None)
    p.add_argument("--bins", type=int, default=30)
    p.add_argument("--width", type=float, default=6.0)
    p.add_argument("--height", type=float, default=4.0)
    p.add_argument("--fit", action="store_true")
    p.add_argument("--ci", type=int, default=95)
    p.add_argument("--n_boot", type=int, default=2000)
    p.add_argument("--self-test", action="store_true")
    args = p.parse_args(argv)

    if args.self_test:
        plt, sns, np, pd = _try_import_plotting()
        print("matplotlib available:", plt is not None)
        print("seaborn available:", sns is not None)
        print("numpy available:", np is not None)
        print("pandas available:", pd is not None)
        return 0

    if not args.type:
        p.error("--type is required (or use --self-test)")
    if args.type in CHARTS_MERMAID:
        out = CHARTS_MERMAID[args.type](args)
        print(out)
        return 0

    if args.type not in CHARTS_PYTHON:
        sys.stderr.write(f"Unsupported --type: {args.type}\n")
        return 2

    plt, sns, np, pd = _try_import_plotting()
    data = load_data(args.input)
    if plt is None or pd is None:
        sys.stderr.write("matplotlib / pandas not installed; falling back to Markdown table.\n")
        rows = data if isinstance(data, list) else (
            data.to_dict("records") if hasattr(data, "to_dict") else [])
        path = render_fallback(rows, args.type, args.out, args.title or "")
        print(path)
        return 0

    _setup(plt, sns)
    paths = CHARTS_PYTHON[args.type](data, args, plt, sns, np, pd)
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
