#!/usr/bin/env python3
"""S3: Claude weighted edgelists (challenge + solution) over the 232 docs.

Procedure (matches Dr. Walters' weighting rule and Walters 2022 §2.2.1):
1. Load stage-2 statements for the 232 included transcripts only.
2. Map verbatim cause/effect names to the canonical 17 bins via
   pta_232/factor_grouping_17.csv.
3. Normalize labels to {challenge, solution}. A label of "both"/"challenge/
   solution" (if any) counts in BOTH systems.
4. Per-transcript dedupe on (cause_bin, effect_bin, system): each individual
   counts at most once per connection per system.
5. Weight = number of distinct individuals (transcripts).

Bin-level self-loops are RETAINED (rev 2, for parity with the real N&J
Kumu Connections export, which records them). Structural analyses in s5
zero the diagonal; the edgelists carry the full data.

Outputs:
- pta_232/claude_edges.csv                    long form, both systems
- pta_232/edgelist_claude_challenge.csv       From,To,Weight (Kumu-friendly)
- pta_232/edgelist_claude_solution.csv        From,To,Weight
- pta_232/adjacency_claude_challenge.csv      17x17 matrix
- pta_232/adjacency_claude_solution.csv       17x17 matrix
- Claude Weighted Edgelist.csv (repo root)    From,To,Type,Strength —
  exact schema of the N&J Connections export, both systems combined
"""
from __future__ import annotations

import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "pta_232"
CODED_DIR = ROOT / "pta" / "coded"

BINS = [
    "Capacity Building", "Community / Users", "Community Finance",
    "Community Management", "Coordination", "Environmental",
    "Govt / External Finance", "Govt Management", "Infrastructure",
    "Laws + Regulations", "Monitoring", "O&M", "Planning", "Politics",
    "Private Sector", "Service Performance", "Sustainability",
]


def normalize_label(raw: str) -> list[str]:
    s = (raw or "").strip().lower().rstrip("s")
    if "challenge" in s and "solution" in s:
        return ["challenge", "solution"]
    if s.startswith("challenge"):
        return ["challenge"]
    if s.startswith("solution"):
        return ["solution"]
    return []


def main() -> None:
    ids = {int(line) for line in
           (OUT_DIR / "included_ids.txt").read_text().split()}
    grouping = {}
    with (OUT_DIR / "factor_grouping_17.csv").open(newline="") as fh:
        for row in csv.DictReader(fh):
            grouping[row["verbatim_factor"]] = row["cross_case_factor"]
    print(f"{len(ids)} included docs, {len(grouping):,} grouped factors")

    stmts = []
    label_counts = Counter()
    for path in sorted(CODED_DIR.glob("WASH_KII_*.jsonl")):
        doc_id = int(re.search(r"(\d+)", path.stem).group(1))
        if doc_id not in ids:
            continue
        with path.open() as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                if rec.get("stmt_id") is None or rec.get("cause") is None:
                    continue
                label_counts[rec.get("label")] += 1
                stmts.append((doc_id, rec))
    print(f"{len(stmts):,} statements; raw labels: {dict(label_counts)}")

    misses = Counter()
    self_loop_stmts = 0
    # doc -> set of (cause_bin, effect_bin, system)
    per_doc = defaultdict(set)
    # (cause,effect,system) -> polarity counter (statement-level, pre-dedupe)
    pol = defaultdict(Counter)
    for doc_id, rec in stmts:
        c = grouping.get(rec["cause"])
        e = grouping.get(rec["effect"])
        if c is None or e is None:
            misses[rec["cause"] if c is None else rec["effect"]] += 1
            continue
        if c == e:
            self_loop_stmts += 1
        for system in normalize_label(rec.get("label")):
            per_doc[doc_id].add((c, e, system))
            pol[(c, e, system)][rec.get("polarity", "+")] += 1

    print(f"{sum(misses.values())} grouping misses; "
          f"{self_loop_stmts:,} bin-level self-loop statements RETAINED")

    edges = Counter()
    for doc_id, triples in per_doc.items():
        for t in triples:
            edges[t] += 1

    rows = []
    for (c, e, system), w in edges.items():
        pc = pol[(c, e, system)]
        rows.append({
            "cause": c, "effect": e, "system": system, "weight": w,
            "stmt_pos": pc.get("+", 0), "stmt_neg": pc.get("-", 0),
        })
    rows.sort(key=lambda r: (r["system"], -r["weight"], r["cause"], r["effect"]))

    with (OUT_DIR / "claude_edges.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=[
            "cause", "effect", "system", "weight", "stmt_pos", "stmt_neg"])
        w.writeheader()
        w.writerows(rows)

    for system in ("challenge", "solution"):
        srows = [r for r in rows if r["system"] == system]
        with (OUT_DIR / f"edgelist_claude_{system}.csv").open(
                "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["From", "To", "Weight"])
            for r in srows:
                w.writerow([r["cause"], r["effect"], r["weight"]])
        # adjacency matrix
        with (OUT_DIR / f"adjacency_claude_{system}.csv").open(
                "w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["cause"] + BINS)
            cell = {(r["cause"], r["effect"]): r["weight"] for r in srows}
            for c in BINS:
                w.writerow([c] + [cell.get((c, e), 0) for e in BINS])
        total = sum(r["weight"] for r in srows)
        n_sl = sum(1 for r in srows if r["cause"] == r["effect"])
        w_sl = sum(r["weight"] for r in srows if r["cause"] == r["effect"])
        print(f"\n{system}: {len(srows)} edges ({n_sl} self-loops), "
              f"total weight {total} (self-loop weight {w_sl})")
        print("  top 10:")
        for r in srows[:10]:
            print(f"    {r['weight']:3d}  {r['cause']:26s} -> {r['effect']}")

    # Combined root deliverable in the exact N&J Connections schema.
    with (ROOT / "Claude Weighted Edgelist.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["From", "To", "Type", "Strength"])
        for r in rows:
            w.writerow([r["cause"], r["effect"],
                        r["system"].capitalize(), r["weight"]])

    print("\nwrote claude_edges.csv, edgelist_claude_*.csv, "
          "adjacency_claude_*.csv, and root Claude Weighted Edgelist.csv")


if __name__ == "__main__":
    main()
