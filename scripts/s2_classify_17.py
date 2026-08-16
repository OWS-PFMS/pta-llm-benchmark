#!/usr/bin/env python3
"""S2: classify every verbatim factor (232-doc subset) into one of the
17 canonical Walters/N&J bins.

Same deterministic keyword/priority classifier as pta/scripts/stage4_classify.py,
pointed at pta_232/canonical_17.yaml. See that script's docstring for the
matching and confidence rules.

Outputs:
- pta_232/factor_grouping_17.csv  rank, verbatim_factor, total_refs,
                                  transcripts, cross_case_factor,
                                  confidence, rationale
- pta_232/_classifier_debug_17.csv
"""
from __future__ import annotations

import csv
import re
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
OUT_DIR = ROOT / "pta_232"
SCHEMA_PATH = OUT_DIR / "canonical_17.yaml"
FACTORS_PATH = OUT_DIR / "factors_232.csv"
GROUPING_PATH = OUT_DIR / "factor_grouping_17.csv"
DEBUG_PATH = OUT_DIR / "_classifier_debug_17.csv"

# Broadest canonical bin — used only when nothing matches at all.
DEFAULT_BIN = "Community / Users"


def load_schema() -> list[dict]:
    with SCHEMA_PATH.open() as fh:
        data = yaml.safe_load(fh)
    factors = data["factors"]
    for f in factors:
        compiled = []
        for k in f.get("keywords", []):
            kl = k.lower().strip()
            if not kl:
                continue
            if len(kl) <= 5 and " " not in kl and "-" not in kl:
                pat = re.compile(r"\b" + re.escape(kl) + r"\b")
            else:
                pat = re.compile(re.escape(kl))
            compiled.append((kl, pat))
        f["_keywords_lc"] = compiled
    factors.sort(key=lambda f: f["priority"])
    return factors


def load_factors() -> list[dict]:
    rows = []
    with FACTORS_PATH.open(newline="") as fh:
        for row in csv.DictReader(fh):
            rows.append({
                "rank": int(row["rank"]),
                "factor": row["factor"],
                "total_refs": int(row["total_refs"]),
                "transcripts": int(row["transcripts"]),
            })
    return rows


def find_matches(verbatim_lc: str, factors: list[dict]) -> list[tuple[dict, str]]:
    matches = []
    for f in factors:
        best_kw = None
        for kw, pat in f["_keywords_lc"]:
            if pat.search(verbatim_lc):
                if best_kw is None or len(kw) > len(best_kw):
                    best_kw = kw
        if best_kw is not None:
            matches.append((f, best_kw))
    return matches


def token_overlap_fallback(verbatim_lc: str, factors: list[dict]) -> tuple[dict, str]:
    tokens = {t for t in re.findall(r"[a-z]+", verbatim_lc) if len(t) >= 4}
    best, best_score = None, 0
    for f in factors:
        score = sum(1 for kw, _p in f["_keywords_lc"] for t in tokens if t in kw)
        if score > best_score:
            best, best_score = f, score
    if best is None:
        for f in factors:
            if f["name"] == DEFAULT_BIN:
                return f, f"no match — defaulted to {DEFAULT_BIN}"
    return best, f"token-overlap fallback ({best_score})"


def classify(verbatim: str, factors: list[dict]) -> tuple[str, str, str]:
    verbatim_lc = verbatim.lower()
    matches = find_matches(verbatim_lc, factors)

    if not matches:
        bucket, rationale = token_overlap_fallback(verbatim_lc, factors)
        return bucket["name"], "low", rationale[:60]

    def score(item):
        f, kw = item
        return len(kw) * 100 - f["priority"]

    matches.sort(key=score, reverse=True)
    best_factor, best_kw = matches[0]

    if len(matches) == 1:
        confidence = "high" if len(best_kw) >= 6 else "medium"
        return best_factor["name"], confidence, f"matched '{best_kw}'"[:60]

    second_factor, second_kw = matches[1]
    score_gap = score(matches[0]) - score(matches[1])
    if score_gap >= 200 and len(best_kw) >= 6:
        confidence = "high"
    elif score_gap >= 50:
        confidence = "medium"
    else:
        confidence = "low"
    return best_factor["name"], confidence, f"'{best_kw}' over '{second_kw}'"[:60]


def main() -> None:
    factors = load_schema()
    print(f"loaded {len(factors)} canonical bins")
    assert len(factors) == 17

    rows = load_factors()
    print(f"loaded {len(rows):,} verbatim factors")

    print("\nschema self-check (each bin's examples should map to itself):")
    misses = 0
    for f in factors:
        for ex in f.get("examples", []):
            assigned, _c, rat = classify(ex, factors)
            if assigned != f["name"]:
                misses += 1
                print(f"  MISS: '{ex}' -> {assigned} (expected {f['name']}; {rat})")
    print(f"  {misses} self-check misses\n")

    grouping_rows, debug_rows = [], []
    bucket_counts = defaultdict(int)
    bucket_refs = defaultdict(int)
    confidence_counts = defaultdict(int)

    for r in rows:
        bucket, conf, rat = classify(r["factor"], factors)
        grouping_rows.append({
            "rank": r["rank"],
            "verbatim_factor": r["factor"],
            "total_refs": r["total_refs"],
            "transcripts": r["transcripts"],
            "cross_case_factor": bucket,
            "confidence": conf,
            "rationale": rat,
        })
        bucket_counts[bucket] += 1
        bucket_refs[bucket] += r["total_refs"]
        confidence_counts[conf] += 1
        debug_rows.append({
            "factor": r["factor"], "bucket": bucket, "confidence": conf,
            "rationale": rat, "total_refs": r["total_refs"],
        })

    with GROUPING_PATH.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=[
            "rank", "verbatim_factor", "total_refs", "transcripts",
            "cross_case_factor", "confidence", "rationale"])
        w.writeheader()
        w.writerows(grouping_rows)
    print(f"wrote {GROUPING_PATH} ({len(grouping_rows):,} rows)")

    with DEBUG_PATH.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=[
            "factor", "bucket", "confidence", "rationale", "total_refs"])
        w.writeheader()
        w.writerows(debug_rows)

    print("\nbin counts (unique verbatim factors / total refs):")
    for b in sorted(bucket_counts, key=lambda k: -bucket_refs[k]):
        print(f"  {bucket_counts[b]:5d} / {bucket_refs[b]:6d}  {b}")

    print("\nconfidence counts:")
    for c in ("high", "medium", "low"):
        print(f"  {c:>6s}: {confidence_counts[c]:,}")

    low_high_ref = [g["verbatim_factor"] for g in grouping_rows
                    if g["confidence"] == "low" and g["transcripts"] >= 8]
    if low_high_ref:
        print(f"\nlow-confidence high-ref factors ({len(low_high_ref)}):")
        for x in low_high_ref:
            print(f"  - {x}")


if __name__ == "__main__":
    main()
