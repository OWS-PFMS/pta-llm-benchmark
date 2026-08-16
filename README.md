# LLM-Driven Purposive Text Analysis — Benchmark Materials

> **⚠️ PRE-RELEASE — PRIVATE.** This repository is staged for public release
> but is private pending the checks in [`RELEASE_CHECKLIST.md`](RELEASE_CHECKLIST.md)
> (consent/IRB confirmation for interview-derived content). Do not share
> access or contents until the checklist is signed off.

Supplemental materials for:

> Walters, J., Bryan, C. F., & Valcourt, N. *Scaling System Model Development
> and Learning from Qualitative Data: Benchmarking LLM-Driven Purposive Text
> Analysis Against Expert Coding.* (In preparation.)

The study applies an LLM (Claude, Anthropic) as a Purposive Text Analysis
(PTA) coder to 232 key informant interviews on rural water service
sustainability in East Africa — the same transcripts independently hand-coded
by two domain experts (Walters et al., 2022) — and compares the resulting
challenge and solution system networks over an identical 17-factor schema.
Headline agreement: Spearman ρ = 0.86 (challenge) / 0.82 (solution) on
weighted eigenvector centrality, with *Coordination* emerging as the sole
Target/Leverage factor in all four networks, independently for both coders.

## Repository map

| Directory | Contents | Manuscript section |
|---|---|---|
| `prompts/` | The exact PTA coding rules given to the LLM (the versioned prompt artifact) | §2.3 |
| `transcripts/` | The 311 interview transcripts (`WASH KII (001–311).txt`) and `included_ids.txt`, the 232-transcript benchmark subset | §2.1 |
| `coded_statements/` | LLM-coded causal statements: per-transcript JSONL (with polarity, challenge/solution label, and verbatim source excerpts) and a flat CSV | §2.3 |
| `aggregation/` | The canonical 17-factor schema (`canonical_17.yaml`), the deterministic factor→bin classifier output with confidence flags, and corpus factor frequencies | §2.4 |
| `benchmark/` | The expert (N&J) final aggregated edgelist, exported from the Kumu model underlying Walters et al. (2022) | §2.2 |
| `networks/` | Edge lists and adjacency matrices for all four networks: (expert \| LLM) × (challenge \| solution) | §2.5 |
| `analysis/` | Weighted eigenvector centrality, influence/dependence + Godet quadrants, feedback-loop inventories, and the full comparison summary | §2.6, §3 |
| `scripts/` | The pipeline stages, archived as run (see provenance note below) | §2 |
| `figures/` | Figures 1 and 3 (PNG + vector) with the scripts that generate them | §2, §3.3 |
| `tables/` | Tables 1–3 with the script that generates them | §3 |

## Reproducing the analysis

Everything downstream of transcript coding is deterministic. With Python ≥ 3.9
and `pandas`, `numpy`, `networkx`, `scipy`, `matplotlib` (+ `adjustText`;
`pandoc` for the tables' .docx):

```bash
# Figures and tables, regenerated from the archived network/analysis CSVs:
python3 figures/make_figure3_influence_maps.py
python3 figures/make_figure1_process_diagram.py
python3 tables/make_tables.py
```

The pipeline-stage scripts in `scripts/` (`s1`–`s6`, minus the superseded
`s4`) are archived exactly as run in the working repository and reference its
directory layout; they are included for audit rather than turnkey re-execution.
Their stage order: `s1` (corpus factor frequencies) → `s2` (deterministic
17-bin classification) → `s3` (LLM network construction) → `s6` (expert
benchmark ingest from `benchmark/`) → `s5` (all structural analyses and
agreement statistics; regenerates everything in `analysis/`).

The LLM *coding* stage itself (transcripts → `coded_statements/`) is
approximately reproducible only: it queries a commercial model
(prompt in `prompts/coding_rules.md`; development on Claude Opus 4.7, final
coding with Claude Sonnet 4.6). Its complete output is archived here, and
every coded statement carries its source excerpt for verification against
`transcripts/`.

## Traceability chain

```
transcripts/  →  coded_statements/ (verbatim factors + excerpts)
              →  aggregation/     (17-bin assignments + confidence)
              →  networks/        (informant-weighted edge lists)
              →  analysis/        (centrality, quadrants, loops, agreement)
              →  figures/ tables/
```

Every edge weight in `networks/` can be traced to the verbatim statements and
source excerpts in `coded_statements/` that produced it — the "visible
cohesion between map and source" that PTA requires (Kim & Andersen, 2012).

## Data provenance and licensing

- Code (`scripts/`, `figures/*.py`, `tables/*.py`) is released under the MIT
  License (see `LICENSE`).
- Interview transcripts and the expert benchmark edgelist originate from the
  data collection described in Walters et al. (2022). Redistribution terms
  for interview-derived content are pending the consent/IRB confirmation
  tracked in `RELEASE_CHECKLIST.md`.

## Citation

Citation details (and an archived DOI snapshot) will be added when the
manuscript is accepted.
