#!/usr/bin/env python3
"""Generate Tables 1-3 as an editable Word document (pandoc markdown -> docx).

Table 1: coding/network volume (Expert column left of LLM, per Jeff's comment).
Table 2: cross-coder agreement metrics.
Table 3: top-10 highest-scoring feedback loops per coder and system, built
directly from analysis/loops_*.csv (referenced in §3.4, currently mis-cited
there as "Table 2").
"""
import csv
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "analysis"
OUT = Path(__file__).resolve().parent

COMPACT = {"Community / Users": "Community/Users",
           "Govt / External Finance": "Govt/Ext Finance",
           "Laws + Regulations": "Laws + Regs"}

def top_loops(name, n=10):
    with open(DATA / f"loops_{name}.csv") as f:
        rows = list(csv.DictReader(f))
    out = []
    for r in rows[:n]:
        loop = r["loop"]
        for k, v in COMPACT.items():
            loop = loop.replace(k, v)
        # Drop the repeated closing factor; the loop-back is implied.
        parts = loop.split(" -> ")
        if len(parts) > 1 and parts[0] == parts[-1]:
            parts = parts[:-1]
        out.append((" → ".join(parts) + " ↺", float(r["score"])))
    return out

md = []
md.append("**Table 1.** Coding and network volume over the identical "
          "232-transcript corpus.\n")
md.append("|  | Expert (benchmark) | LLM (Claude) |")
md.append("|:---|---:|---:|")
for row in [
    ("Causal statements", "4,230", "5,802"),
    ("Statements per interview", "18.2", "25.0"),
    ("Distinct factor names (pre-aggregation)", "332", "7,274"),
    ("Challenge network (self-loops excluded)",
     "175 edges, Σw = 1,165", "205 edges, Σw = 1,738"),
    ("Solution network (self-loops excluded)",
     "196 edges, Σw = 1,569", "216 edges, Σw = 2,313"),
    ("Bin-level self-loops (recorded, not analyzed)",
     "24 edges, Σw = 436", "32 edges, Σw = 786"),
]:
    md.append("| " + " | ".join(row) + " |")
md.append("")

md.append("**Table 2.** Cross-coder agreement, by system (Challenge or "
          "Solution).\n")
md.append("| Metric | Challenge | Solution |")
md.append("|:---|---:|---:|")
for row in [
    ("Spearman ρ — eigenvector centrality", "0.858", "0.820"),
    ("Spearman ρ — influence (weighted out-degree)", "0.780", "0.762"),
    ("Spearman ρ — dependence (weighted in-degree)", "0.886", "0.803"),
    ("Godet quadrant agreement", "11/17", "10/17"),
    ("Edge-set Jaccard", "0.689", "0.695"),
    ("Spearman ρ — weights on shared edges", "0.592", "0.598"),
    ("Top-10 loop overlap (node sets)", "0/10", "0/10"),
]:
    md.append("| " + " | ".join(row) + " |")
md.append("")

md.append("**Table 3.** Ten highest-scoring feedback loops in each network, "
          "by coder and system. Loops are scored with the salience metric of "
          "Gottschamer and Walters (2023); ↺ marks the closure of the "
          "cycle back to its first factor.\n")
for system in ("challenge", "solution"):
    md.append(f"*({'a' if system == 'challenge' else 'b'}) "
              f"{system.capitalize()} system*\n")
    md.append("| Rank | Expert (benchmark) | Score | LLM (Claude) | Score |")
    md.append("|---:|:---|---:|:---|---:|")
    nj, cl = top_loops(f"nj_{system}"), top_loops(f"claude_{system}")
    for i, ((nl, ns), (ll, ls)) in enumerate(zip(nj, cl), 1):
        md.append(f"| {i} | {nl} | {ns:.1f} | {ll} | {ls:.1f} |")
    md.append("")

src = OUT / "tables_1-3.md"
src.write_text("\n".join(md), encoding="utf-8")
subprocess.run(["pandoc", str(src), "-o", str(OUT / "tables_1-3.docx")],
               check=True)
print("wrote", OUT / "tables_1-3.docx")
