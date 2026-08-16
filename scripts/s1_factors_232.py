#!/usr/bin/env python3
"""S1: verbatim factor frequencies over the 232-transcript subset.

The 232-doc ID list is derived from the folder Dr. Walters shared
(`new docs/232 WASH KII Transcripts (txt files)/`), not hard-coded.

Reads the existing stage-2 coded JSONL (pta/coded/) — no re-coding.

Outputs:
- pta_232/included_ids.txt   one ID per line (integer, 1..311)
- pta_232/factors_232.csv    rank, factor, total_refs, as_cause, as_effect, transcripts
"""
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
NEW_DOCS = ROOT / "new docs" / "232 WASH KII Transcripts (txt files)"
CODED_DIR = ROOT / "pta" / "coded"
OUT_DIR = ROOT / "pta_232"


def included_ids() -> set[int]:
    ids = set()
    for p in NEW_DOCS.glob("WASH KII (*).txt"):
        m = re.search(r"\((\d+)\)", p.name)
        if m:
            ids.add(int(m.group(1)))
    return ids


def main() -> None:
    ids = included_ids()
    print(f"{len(ids)} included transcript IDs")
    assert len(ids) == 232, f"expected 232, got {len(ids)}"

    (OUT_DIR / "included_ids.txt").write_text(
        "\n".join(str(i) for i in sorted(ids)) + "\n")

    stats = defaultdict(lambda: {"total": 0, "cause": 0, "effect": 0,
                                 "transcripts": set()})
    n_stmts = 0
    n_docs = 0
    for path in sorted(CODED_DIR.glob("WASH_KII_*.jsonl")):
        doc_id = int(re.search(r"(\d+)", path.stem).group(1))
        if doc_id not in ids:
            continue
        n_docs += 1
        with path.open() as fh:
            for line in fh:
                line = line.strip()
                if not line:
                    continue
                rec = json.loads(line)
                if rec.get("stmt_id") is None or rec.get("cause") is None:
                    continue
                n_stmts += 1
                for role in ("cause", "effect"):
                    f = rec[role]
                    stats[f]["total"] += 1
                    stats[f][role] += 1
                    stats[f]["transcripts"].add(doc_id)

    print(f"{n_docs} coded transcripts in subset, {n_stmts:,} statements, "
          f"{len(stats):,} unique verbatim factors")

    rows = sorted(stats.items(), key=lambda kv: (-kv[1]["total"], kv[0]))
    with (OUT_DIR / "factors_232.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["rank", "factor", "total_refs", "as_cause", "as_effect",
                    "transcripts"])
        for i, (f, s) in enumerate(rows, 1):
            w.writerow([i, f, s["total"], s["cause"], s["effect"],
                        len(s["transcripts"])])
    print(f"wrote {OUT_DIR / 'factors_232.csv'}")


if __name__ == "__main__":
    main()
