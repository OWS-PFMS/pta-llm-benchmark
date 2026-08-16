#!/usr/bin/env python3
"""S5: head-to-head structural comparison — Claude system vs. N&J system.

Rev 2 (2026-07-24): the N&J side now comes from the REAL Kumu Connections
export (pta_232/nj_real_edges.csv, via s6) rather than the S4
reconstruction. Both edgelists carry bin-level self-loops; all structural
metrics below zero the diagonal (MICMAC convention, and consistent with
the Kumu Elements metrics N&J exported), and loop enumeration considers
cycles of length >= 2 only.

For each coder (claude, nj) and each system (challenge, solution):
1. Weighted eigenvector centrality (same method as pta/scripts/stage6_analysis.py).
2. Influence (weighted out-degree) / Dependence (weighted in-degree),
   normalized 0-1, with Godet quadrant classification (median split).
3. Feedback loops: simple cycles up to length 5, scored as the average of
   (edge_weight * normalized eigenvector of downstream factor).

Cross-coder comparison per system (the three axes in Dr. Walters' email):
- Spearman rank correlation of eigenvector centrality, influence, dependence.
- Quadrant agreement (how many of the 17 bins land in the same quadrant).
- Edge overlap: Jaccard on edge sets + Spearman of weights on shared edges.
- Overlap of top-10 loops.

Outputs:
- pta_232/centrality_{coder}_{system}.csv
- pta_232/loops_{coder}_{system}.csv       (top 25)
- pta_232/comparison_summary.md
"""
from __future__ import annotations

import csv
from pathlib import Path

import networkx as nx
import numpy as np
from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "pta_232"

BINS = [
    "Capacity Building", "Community / Users", "Community Finance",
    "Community Management", "Coordination", "Environmental",
    "Govt / External Finance", "Govt Management", "Infrastructure",
    "Laws + Regulations", "Monitoring", "O&M", "Planning", "Politics",
    "Private Sector", "Service Performance", "Sustainability",
]


def load_edges(coder: str) -> list[dict]:
    path = OUT_DIR / ("claude_edges.csv" if coder == "claude"
                      else "nj_real_edges.csv")
    rows = []
    with path.open(newline="") as fh:
        for r in csv.DictReader(fh):
            if r["cause"] == r["effect"]:
                continue  # diagonal zeroed for all structural metrics
            rows.append({"cause": r["cause"], "effect": r["effect"],
                         "system": r["system"], "weight": int(r["weight"])})
    return rows


def normalize(values: dict) -> dict:
    mx = max(values.values()) if values else 1
    return {k: (v / mx if mx else 0.0) for k, v in values.items()}


def quadrant(infl, dep, im, dm) -> str:
    hi_i, hi_d = infl >= im, dep >= dm
    if hi_i and not hi_d:
        return "Target/Leverage"
    if hi_i and hi_d:
        return "Dynamic/Core"
    if not hi_i and hi_d:
        return "Outcome"
    return "Incidental"


def analyze(coder: str, system: str, edges: list[dict]) -> dict:
    g = nx.DiGraph()
    for e in edges:
        if e["system"] == system:
            g.add_edge(e["cause"], e["effect"], weight=e["weight"])
    for b in BINS:
        if b not in g:
            g.add_node(b)

    try:
        eig = nx.eigenvector_centrality_numpy(g, weight="weight")
    except Exception:
        eig = nx.eigenvector_centrality(g, weight="weight", max_iter=2000)
    eig_norm = normalize(eig)

    infl = {b: sum(d["weight"] for _, _, d in g.out_edges(b, data=True))
            for b in BINS}
    dep = {b: sum(d["weight"] for _, _, d in g.in_edges(b, data=True))
           for b in BINS}
    infl_n, dep_n = normalize(infl), normalize(dep)
    im, dm = float(np.median(list(infl_n.values()))), float(
        np.median(list(dep_n.values())))

    cycles = list(nx.simple_cycles(g, length_bound=5))
    loop_rows = []
    loop_appearances = {b: 0 for b in BINS}
    for cyc in cycles:
        w_sum, score = 0, 0.0
        n = len(cyc)
        for i, node in enumerate(cyc):
            nxt = cyc[(i + 1) % n]
            w = g[node][nxt]["weight"]
            w_sum += w
            score += w * eig_norm[nxt]
        score /= n
        for node in cyc:
            loop_appearances[node] += 1
        loop_rows.append({"loop": " -> ".join(cyc + [cyc[0]]),
                          "length": n, "total_weight": w_sum,
                          "score": round(score, 3)})
    loop_rows.sort(key=lambda r: -r["score"])

    cent_rows = []
    for b in BINS:
        cent_rows.append({
            "bin": b,
            "eigenvector": round(eig_norm[b], 4),
            "influence_raw": infl[b], "dependence_raw": dep[b],
            "influence": round(infl_n[b], 4), "dependence": round(dep_n[b], 4),
            "out_degree": g.out_degree(b), "in_degree": g.in_degree(b),
            "quadrant": quadrant(infl_n[b], dep_n[b], im, dm),
            "loop_appearances": loop_appearances[b],
        })
    cent_rows.sort(key=lambda r: -r["eigenvector"])

    with (OUT_DIR / f"centrality_{coder}_{system}.csv").open(
            "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cent_rows[0].keys()))
        w.writeheader()
        w.writerows(cent_rows)
    with (OUT_DIR / f"loops_{coder}_{system}.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["loop", "length", "total_weight",
                                           "score"])
        w.writeheader()
        w.writerows(loop_rows[:25])

    return {"cent": {r["bin"]: r for r in cent_rows},
            "loops": loop_rows, "n_cycles": len(cycles),
            "edges": {(e["cause"], e["effect"]): e["weight"]
                      for e in edges if e["system"] == system}}


def main() -> None:
    results = {}
    for coder in ("claude", "nj"):
        edges = load_edges(coder)
        for system in ("challenge", "solution"):
            print(f"analyzing {coder}/{system}...")
            results[(coder, system)] = analyze(coder, system, edges)
            print(f"  {len(results[(coder, system)]['edges'])} edges, "
                  f"{results[(coder, system)]['n_cycles']:,} cycles")

    lines = ["# Claude vs. N&J — structural comparison (232 docs, 17 bins)",
             ""]
    for system in ("challenge", "solution"):
        c, n = results[("claude", system)], results[("nj", system)]
        lines.append(f"## {system.capitalize()} system")
        lines.append("")

        for metric in ("eigenvector", "influence", "dependence"):
            cv = [c["cent"][b][metric] for b in BINS]
            nv = [n["cent"][b][metric] for b in BINS]
            rho, p = spearmanr(cv, nv)
            lines.append(f"- Spearman rho, {metric}: **{rho:.3f}** (p={p:.4f})")

        agree = sum(1 for b in BINS
                    if c["cent"][b]["quadrant"] == n["cent"][b]["quadrant"])
        lines.append(f"- Quadrant agreement: **{agree}/17** bins")

        ce, ne = set(c["edges"]), set(n["edges"])
        shared = ce & ne
        jac = len(shared) / len(ce | ne)
        cw = [c["edges"][e] for e in sorted(shared)]
        nw = [n["edges"][e] for e in sorted(shared)]
        rho_w, p_w = spearmanr(cw, nw)
        lines.append(f"- Edge sets: claude {len(ce)}, nj {len(ne)}, "
                     f"shared {len(shared)} (Jaccard {jac:.3f})")
        lines.append(f"- Spearman rho of weights on shared edges: "
                     f"**{rho_w:.3f}** (p={p_w:.2e})")

        c_top = {tuple(sorted(r["loop"].split(" -> ")[:-1]))
                 for r in c["loops"][:10]}
        n_top = {tuple(sorted(r["loop"].split(" -> ")[:-1]))
                 for r in n["loops"][:10]}
        lines.append(f"- Top-10 loop overlap (unordered node sets): "
                     f"**{len(c_top & n_top)}/10**")
        lines.append("")

        lines.append(f"| rank | Claude eig | N&J eig |")
        lines.append("|---|---|---|")
        c_sorted = sorted(BINS, key=lambda b: -c["cent"][b]["eigenvector"])
        n_sorted = sorted(BINS, key=lambda b: -n["cent"][b]["eigenvector"])
        for i in range(17):
            lines.append(f"| {i+1} | {c_sorted[i]} "
                         f"({c['cent'][c_sorted[i]]['eigenvector']:.3f}) "
                         f"| {n_sorted[i]} "
                         f"({n['cent'][n_sorted[i]]['eigenvector']:.3f}) |")
        lines.append("")

        lines.append("Top 5 loops, Claude:")
        for r in c["loops"][:5]:
            lines.append(f"- [{r['score']}] {r['loop']}")
        lines.append("")
        lines.append("Top 5 loops, N&J:")
        for r in n["loops"][:5]:
            lines.append(f"- [{r['score']}] {r['loop']}")
        lines.append("")

        lines.append("Target/Leverage quadrant (high influence, low dependence):")
        for coder, res in (("Claude", c), ("N&J", n)):
            tl = [b for b in BINS
                  if res["cent"][b]["quadrant"] == "Target/Leverage"]
            tl.sort(key=lambda b: -res["cent"][b]["influence"])
            lines.append(f"- {coder}: {', '.join(tl)}")
        lines.append("")

    out = OUT_DIR / "comparison_summary.md"
    out.write_text("\n".join(lines) + "\n")
    print(f"\nwrote {out}")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
