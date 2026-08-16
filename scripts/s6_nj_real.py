#!/usr/bin/env python3
"""S6: ingest the REAL N&J weighted edgelist (Kumu Connections export,
received 2026-07-24) and quantify how close the S4 reconstruction got.

Inputs:
- new docs/Weighted Edgelist N&J.xlsx - Connections.csv  (From,To,Type,Strength)
- pta_232/nj_edges.csv                                   (S4 reconstruction)

Outputs:
- pta_232/nj_real_edges.csv                    cause,effect,system,weight
- pta_232/edgelist_nj_real_{challenge,solution}.csv
- pta_232/adjacency_nj_real_{challenge,solution}.csv
- pta_232/reconstruction_fidelity.md           reconstruction vs. real
"""
from __future__ import annotations

import csv
from pathlib import Path

from scipy.stats import spearmanr

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "pta_232"
CONN_CSV = ROOT / "new docs" / "Weighted Edgelist N&J.xlsx - Connections.csv"

BINS = [
    "Capacity Building", "Community / Users", "Community Finance",
    "Community Management", "Coordination", "Environmental",
    "Govt / External Finance", "Govt Management", "Infrastructure",
    "Laws + Regulations", "Monitoring", "O&M", "Planning", "Politics",
    "Private Sector", "Service Performance", "Sustainability",
]


def main() -> None:
    real = {}
    with CONN_CSV.open(newline="") as fh:
        for r in csv.DictReader(fh):
            key = (r["From"].strip(), r["To"].strip(), r["Type"].strip().lower())
            assert key[0] in BINS and key[1] in BINS, key
            assert key not in real
            real[key] = int(r["Strength"])
    print(f"real N&J edgelist: {len(real)} edges")

    rows = [{"cause": c, "effect": e, "system": s, "weight": w}
            for (c, e, s), w in real.items()]
    rows.sort(key=lambda r: (r["system"], -r["weight"], r["cause"], r["effect"]))
    with (OUT_DIR / "nj_real_edges.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["cause", "effect", "system", "weight"])
        w.writeheader()
        w.writerows(rows)

    for system in ("challenge", "solution"):
        srows = [r for r in rows if r["system"] == system]
        with (OUT_DIR / f"edgelist_nj_real_{system}.csv").open(
                "w", newline="") as fh:
            wtr = csv.writer(fh)
            wtr.writerow(["From", "To", "Weight"])
            for r in srows:
                wtr.writerow([r["cause"], r["effect"], r["weight"]])
        with (OUT_DIR / f"adjacency_nj_real_{system}.csv").open(
                "w", newline="") as fh:
            wtr = csv.writer(fh)
            wtr.writerow(["cause"] + BINS)
            cell = {(r["cause"], r["effect"]): r["weight"] for r in srows}
            for c in BINS:
                wtr.writerow([c] + [cell.get((c, e), 0) for e in BINS])

    # ---- fidelity of the S4 reconstruction ----
    recon = {}
    with (OUT_DIR / "nj_edges.csv").open(newline="") as fh:
        for r in csv.DictReader(fh):
            recon[(r["cause"], r["effect"], r["system"])] = int(r["weight"])

    lines = ["# Reconstruction fidelity — S4 reconstruction vs. real Kumu "
             "Connections export", "",
             "The reconstruction excluded bin-level self-loops; the real "
             "export includes them. Fidelity is therefore assessed on "
             "non-self-loop edges.", ""]
    for system in ("challenge", "solution"):
        rl = {(c, e): w for (c, e, s), w in real.items()
              if s == system and c != e}
        rc = {(c, e): w for (c, e, s), w in recon.items() if s == system}
        shared = set(rl) & set(rc)
        jac = len(shared) / len(set(rl) | set(rc))
        rho, p = spearmanr([rl[k] for k in sorted(shared)],
                           [rc[k] for k in sorted(shared)])
        w_real = sum(rl.values())
        w_rec = sum(rc.values())
        diffs = sorted(((abs(rl.get(k, 0) - rc.get(k, 0)), k,
                         rl.get(k, 0), rc.get(k, 0))
                        for k in set(rl) | set(rc)), reverse=True)
        lines.append(f"## {system.capitalize()}")
        lines.append("")
        lines.append(f"- real: {len(rl)} non-self-loop edges, total weight "
                     f"{w_real}; reconstruction: {len(rc)} edges, total "
                     f"weight {w_rec} ({(w_rec - w_real) / w_real:+.1%})")
        lines.append(f"- edge-set Jaccard: **{jac:.3f}** "
                     f"({len(shared)} shared)")
        lines.append(f"- Spearman rho of weights on shared edges: "
                     f"**{rho:.3f}** (p={p:.2e})")
        lines.append("- largest weight discrepancies (|real − recon|):")
        for d, (c, e), wr, wc in diffs[:8]:
            lines.append(f"    - {c} -> {e}: real {wr}, recon {wc} (Δ{d})")
        lines.append("")

    out = OUT_DIR / "reconstruction_fidelity.md"
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
