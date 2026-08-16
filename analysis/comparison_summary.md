# Claude vs. N&J — structural comparison (232 docs, 17 bins)

## Challenge system

- Spearman rho, eigenvector: **0.858** (p=0.0000)
- Spearman rho, influence: **0.780** (p=0.0002)
- Spearman rho, dependence: **0.886** (p=0.0000)
- Quadrant agreement: **11/17** bins
- Edge sets: claude 205, nj 175, shared 155 (Jaccard 0.689)
- Spearman rho of weights on shared edges: **0.592** (p=5.28e-16)
- Top-10 loop overlap (unordered node sets): **0/10**

| rank | Claude eig | N&J eig |
|---|---|---|
| 1 | Service Performance (1.000) | Sustainability (1.000) |
| 2 | Community / Users (0.639) | Service Performance (0.512) |
| 3 | Infrastructure (0.522) | O&M (0.410) |
| 4 | Sustainability (0.495) | Community / Users (0.376) |
| 5 | O&M (0.378) | Community Finance (0.226) |
| 6 | Environmental (0.226) | Infrastructure (0.163) |
| 7 | Community Finance (0.106) | Govt / External Finance (0.147) |
| 8 | Govt / External Finance (0.099) | Capacity Building (0.096) |
| 9 | Community Management (0.083) | Community Management (0.094) |
| 10 | Govt Management (0.082) | Environmental (0.060) |
| 11 | Planning (0.071) | Govt Management (0.045) |
| 12 | Monitoring (0.054) | Monitoring (0.038) |
| 13 | Coordination (0.050) | Private Sector (0.029) |
| 14 | Private Sector (0.048) | Coordination (0.024) |
| 15 | Capacity Building (0.048) | Planning (0.023) |
| 16 | Politics (0.007) | Politics (0.015) |
| 17 | Laws + Regulations (0.004) | Laws + Regulations (0.004) |

Top 5 loops, Claude:
- [59.434] Service Performance -> Community / Users -> Service Performance
- [50.542] Service Performance -> Infrastructure -> Service Performance
- [46.723] Service Performance -> Community / Users -> Infrastructure -> Service Performance
- [43.891] Service Performance -> Infrastructure -> Community / Users -> Service Performance
- [37.098] Govt / External Finance -> Infrastructure -> Service Performance -> Govt / External Finance

Top 5 loops, N&J:
- [35.705] O&M -> Sustainability -> O&M
- [28.373] O&M -> Sustainability -> Capacity Building -> O&M
- [27.852] O&M -> Sustainability -> Community Finance -> O&M
- [27.402] O&M -> Sustainability -> Govt / External Finance -> O&M
- [25.135] O&M -> Sustainability -> Community / Users -> O&M

Target/Leverage quadrant (high influence, low dependence):
- Claude: Govt Management, Coordination
- N&J: Environmental, Coordination

## Solution system

- Spearman rho, eigenvector: **0.820** (p=0.0001)
- Spearman rho, influence: **0.762** (p=0.0004)
- Spearman rho, dependence: **0.803** (p=0.0001)
- Quadrant agreement: **10/17** bins
- Edge sets: claude 216, nj 196, shared 169 (Jaccard 0.695)
- Spearman rho of weights on shared edges: **0.598** (p=8.69e-18)
- Top-10 loop overlap (unordered node sets): **0/10**

| rank | Claude eig | N&J eig |
|---|---|---|
| 1 | Service Performance (1.000) | Sustainability (1.000) |
| 2 | Community / Users (0.730) | Community / Users (0.625) |
| 3 | Sustainability (0.603) | O&M (0.600) |
| 4 | Infrastructure (0.518) | Service Performance (0.553) |
| 5 | O&M (0.438) | Community Management (0.324) |
| 6 | Govt / External Finance (0.236) | Community Finance (0.231) |
| 7 | Environmental (0.229) | Govt / External Finance (0.225) |
| 8 | Community Management (0.170) | Infrastructure (0.185) |
| 9 | Coordination (0.147) | Govt Management (0.130) |
| 10 | Govt Management (0.143) | Capacity Building (0.121) |
| 11 | Community Finance (0.134) | Environmental (0.107) |
| 12 | Monitoring (0.121) | Monitoring (0.100) |
| 13 | Planning (0.116) | Private Sector (0.088) |
| 14 | Capacity Building (0.083) | Planning (0.055) |
| 15 | Private Sector (0.083) | Coordination (0.036) |
| 16 | Laws + Regulations (0.052) | Politics (0.029) |
| 17 | Politics (0.029) | Laws + Regulations (0.017) |

Top 5 loops, Claude:
- [52.992] Service Performance -> Community / Users -> Service Performance
- [52.939] Service Performance -> Infrastructure -> Service Performance
- [52.175] Service Performance -> Community / Users -> Infrastructure -> Service Performance
- [42.754] Service Performance -> Community / Users -> Coordination -> Infrastructure -> Service Performance
- [41.806] Govt / External Finance -> Infrastructure -> Service Performance -> Community / Users -> Govt / External Finance

Top 5 loops, N&J:
- [25.553] O&M -> Sustainability -> Govt / External Finance -> O&M
- [25.04] Capacity Building -> O&M -> Sustainability -> Community / Users -> Capacity Building
- [23.591] O&M -> Sustainability -> Infrastructure -> O&M
- [23.237] Capacity Building -> O&M -> Sustainability -> Service Performance -> Community / Users -> Capacity Building
- [23.131] Capacity Building -> O&M -> Sustainability -> Govt / External Finance -> Capacity Building

Target/Leverage quadrant (high influence, low dependence):
- Claude: Coordination, Capacity Building, Monitoring
- N&J: Coordination, Govt Management

