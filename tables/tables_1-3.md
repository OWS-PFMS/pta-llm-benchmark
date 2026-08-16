**Table 1.** Coding and network volume over the identical 232-transcript corpus.

|  | Expert (benchmark) | LLM (Claude) |
|:---|---:|---:|
| Causal statements | 4,230 | 5,802 |
| Statements per interview | 18.2 | 25.0 |
| Distinct factor names (pre-aggregation) | 332 | 7,274 |
| Challenge network (self-loops excluded) | 175 edges, Σw = 1,165 | 205 edges, Σw = 1,738 |
| Solution network (self-loops excluded) | 196 edges, Σw = 1,569 | 216 edges, Σw = 2,313 |
| Bin-level self-loops (recorded, not analyzed) | 24 edges, Σw = 436 | 32 edges, Σw = 786 |

**Table 2.** Cross-coder agreement, by system (Challenge or Solution).

| Metric | Challenge | Solution |
|:---|---:|---:|
| Spearman ρ — eigenvector centrality | 0.858 | 0.820 |
| Spearman ρ — influence (weighted out-degree) | 0.780 | 0.762 |
| Spearman ρ — dependence (weighted in-degree) | 0.886 | 0.803 |
| Godet quadrant agreement | 11/17 | 10/17 |
| Edge-set Jaccard | 0.689 | 0.695 |
| Spearman ρ — weights on shared edges | 0.592 | 0.598 |
| Top-10 loop overlap (node sets) | 0/10 | 0/10 |

**Table 3.** Ten highest-scoring feedback loops in each network, by coder and system. Loops are scored with the salience metric of Gottschamer and Walters (2023); ↺ marks the closure of the cycle back to its first factor.

*(a) Challenge system*

| Rank | Expert (benchmark) | Score | LLM (Claude) | Score |
|---:|:---|---:|:---|---:|
| 1 | O&M → Sustainability ↺ | 35.7 | Service Performance → Community/Users ↺ | 59.4 |
| 2 | O&M → Sustainability → Capacity Building ↺ | 28.4 | Service Performance → Infrastructure ↺ | 50.5 |
| 3 | O&M → Sustainability → Community Finance ↺ | 27.9 | Service Performance → Community/Users → Infrastructure ↺ | 46.7 |
| 4 | O&M → Sustainability → Govt/Ext Finance ↺ | 27.4 | Service Performance → Infrastructure → Community/Users ↺ | 43.9 |
| 5 | O&M → Sustainability → Community/Users ↺ | 25.1 | Govt/Ext Finance → Infrastructure → Service Performance ↺ | 37.1 |
| 6 | O&M → Sustainability → Politics ↺ | 24.2 | Govt/Ext Finance → Infrastructure → Service Performance → Community/Users ↺ | 36.4 |
| 7 | O&M → Sustainability → Community/Users → Service Performance ↺ | 22.5 | Govt/Ext Finance → Infrastructure → Community/Users → Service Performance ↺ | 35.5 |
| 8 | O&M → Sustainability → Community/Users → Community Finance ↺ | 21.7 | O&M → Infrastructure → Service Performance → Community/Users ↺ | 35.4 |
| 9 | O&M → Sustainability → Community/Users → Capacity Building ↺ | 21.6 | Service Performance → Environmental → Infrastructure ↺ | 34.4 |
| 10 | O&M → Sustainability → Govt/Ext Finance → Capacity Building ↺ | 21.5 | Service Performance → Community/Users → Environmental → Infrastructure ↺ | 34.3 |

*(b) Solution system*

| Rank | Expert (benchmark) | Score | LLM (Claude) | Score |
|---:|:---|---:|:---|---:|
| 1 | O&M → Sustainability → Govt/Ext Finance ↺ | 25.6 | Service Performance → Community/Users ↺ | 53.0 |
| 2 | Capacity Building → O&M → Sustainability → Community/Users ↺ | 25.0 | Service Performance → Infrastructure ↺ | 52.9 |
| 3 | O&M → Sustainability → Infrastructure ↺ | 23.6 | Service Performance → Community/Users → Infrastructure ↺ | 52.2 |
| 4 | Capacity Building → O&M → Sustainability → Service Performance → Community/Users ↺ | 23.2 | Service Performance → Community/Users → Coordination → Infrastructure ↺ | 42.8 |
| 5 | Capacity Building → O&M → Sustainability → Govt/Ext Finance ↺ | 23.1 | Govt/Ext Finance → Infrastructure → Service Performance → Community/Users ↺ | 41.8 |
| 6 | O&M → Sustainability → Community/Users ↺ | 23.1 | Service Performance → Coordination → Infrastructure ↺ | 41.2 |
| 7 | O&M → Sustainability → Community Management ↺ | 22.6 | Service Performance → Community/Users → Coordination ↺ | 40.3 |
| 8 | O&M → Sustainability → Private Sector ↺ | 22.6 | Service Performance → Community/Users → Sustainability → Infrastructure ↺ | 40.3 |
| 9 | Capacity Building → O&M → Sustainability → Private Sector ↺ | 22.5 | Service Performance → Community/Users → Govt Management → Infrastructure ↺ | 39.6 |
| 10 | Capacity Building → O&M → Sustainability → Govt Management ↺ | 22.5 | O&M → Infrastructure → Service Performance → Community/Users ↺ | 39.5 |
