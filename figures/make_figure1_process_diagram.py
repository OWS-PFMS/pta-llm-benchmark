#!/usr/bin/env python3
"""Figure 1 — LLM-PTA benchmarking workflow (graphical-abstract layout).

Left-to-right pipeline matching §2 of the manuscript stage for stage, with
two parallel coding lanes (expert blue / LLM yellow, matching Figure 3's
series colors) and dashed provenance callouts showing where PTA principles,
the 17-factor WASH schema, and established structural-analysis methods
enter the workflow.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch
from pathlib import Path

OUT = Path(__file__).resolve().parent

BLUE, BLUE_T = "#2166AC", "#E8EFF7"
YEL, YEL_T = "#8a6207", "#FBF3DC"
INK, MUTED, EDGE = "#1a1a1a", "#5f5f5f", "#9a9a9a"
GRAY_T = "#F4F4F2"

mpl.rcParams.update({"font.family": "Helvetica"})

fig, ax = plt.subplots(figsize=(14.4, 7.8))
ax.set_xlim(0, 144)
ax.set_ylim(0, 78)
ax.axis("off")

def box(x, y, w, title, lines, sub=None, fc="white", ec=EDGE, tc=INK,
        dashed=False, title_size=11.2, body_size=9.2):
    """Draw a box sized to its content; returns (x, y_bottom, w, h)."""
    step = body_size * 0.365
    h = 3.6 + step * (len(lines) + (1 if sub else 0)) + 1.5
    y0 = y - h  # y is the TOP of the box
    ax.add_patch(FancyBboxPatch(
        (x, y0), w, h, boxstyle="round,pad=0.6,rounding_size=1.4",
        facecolor=fc, edgecolor=ec, linewidth=1.2,
        linestyle=(0, (5, 3)) if dashed else "solid", zorder=2))
    cy = y - 3.1
    ax.text(x + w / 2, cy, title, ha="center", va="center", fontsize=title_size,
            fontweight="bold", color=tc, zorder=3)
    if sub:
        cy -= step + 0.25
        ax.text(x + w / 2, cy, sub, ha="center", va="center",
                fontsize=body_size - 0.4, style="italic", color=MUTED, zorder=3)
    for ln in lines:
        cy -= step
        ax.text(x + w / 2, cy, ln, ha="center", va="center",
                fontsize=body_size, color=INK if tc == INK else tc, zorder=3)
    return x, y0, w, h

def arrow(p0, p1, color=EDGE, lw=1.6, conn="arc3,rad=0"):
    ax.add_patch(FancyArrowPatch(
        p0, p1, arrowstyle="-|>", mutation_scale=13, color=color, lw=lw,
        connectionstyle=conn, shrinkA=1.5, shrinkB=1.5, zorder=1))

# ---- Column 1: corpus -------------------------------------------------------
corpus = box(3, 48, 24, "Interview corpus", [
    "232 key informant interviews",
    "Rural water service sustainability",
    "Ethiopia · Uganda · Kenya",
    "drawn from a 311-interview corpus",
], sub="§2.1  Data", fc=GRAY_T, ec="#7d7d7d")

# ---- Column 2: parallel coding lanes + PTA callout --------------------------
expert = box(34, 71, 30, "Expert PTA coding", [
    "Two domain experts, hand-coded",
    "4,230 causal statements",
    "332 context-specific factor labels",
], sub="§2.2  Benchmark (Walters et al., 2022)", fc=BLUE_T, ec=BLUE, tc=BLUE)

llm = box(34, 22, 30, "LLM PTA coding", [
    "Claude, per-transcript & independent",
    "5,802 causal statements (232 subset)",
    "7,274 verbatim factor labels",
], sub="§2.3  Structured prompt, archived", fc=YEL_T, ec=YEL, tc=YEL)

pta = box(34, 46.5, 30, "PTA principles", [
    "One cause–effect pair per record",
    "Verbatim factor language",
    "Polarity · challenge/solution",
    "Traceable source excerpts",
], sub="Kim & Andersen (2012)", dashed=True, ec=MUTED, tc=MUTED,
    title_size=9.9, body_size=8.4)

# ---- Column 3: aggregation + provenance callouts ----------------------------
agg = box(73, 56, 25, "Factor aggregation", [
    "Common 17-factor schema",
    "Expert bins as published",
    "LLM: deterministic classifier",
    "with confidence flags",
], sub="§2.4", fc=GRAY_T, ec="#7d7d7d")

wash = box(71, 75, 29, "17 cross-case factors", [
    "WASH-for-development theory:",
    "sustainability building blocks",
], sub="Walters et al. (2022); WASH literature", dashed=True, ec=MUTED,
    tc=MUTED, title_size=9.9, body_size=8.4)

methods = box(71, 24, 29, "Established systems methods", [
    "Godet (1994) influence maps",
    "Bonacich (1987) centrality",
    "Johnson (1975) cycle enumeration",
    "Gottschamer & Walters (2023) loop score",
], sub="Prior structural-analysis studies", dashed=True, ec=MUTED, tc=MUTED,
    title_size=9.9, body_size=8.4)

# ---- Column 4: networks -> analysis -> agreement ----------------------------
net = box(107, 71, 26, "Network construction", [
    "4 weighted directed networks:",
    "expert & LLM × challenge & solution",
    "Edge weight = unique informants",
    "17 factors, self-loops zeroed",
], sub="§2.5", fc=GRAY_T, ec="#7d7d7d")

struct = box(107, 45.5, 26, "Structural analysis", [
    "Eigenvector centrality",
    "Influence–dependence quadrants",
    "Feedback-loop salience",
], sub="§2.6", fc=GRAY_T, ec="#7d7d7d")

agree = box(107, 22, 26, "Agreement assessment", [
    "Spearman ρ · quadrant match",
    "Jaccard edges · top-loop overlap",
    r"$\rightarrow$  RQ1–RQ3",
], sub="§2.6", fc=GRAY_T, ec="#7d7d7d")

# ---- Flow arrows ------------------------------------------------------------
cx_r = corpus[0] + corpus[2] + 0.8
arrow((cx_r, 42), (expert[0] - 0.8, 60))
arrow((cx_r, 33), (llm[0] - 0.8, 15))
arrow((expert[0] + expert[2] + 0.8, 62), (agg[0] - 0.8, 50), color=BLUE)
arrow((llm[0] + llm[2] + 0.8, 15), (agg[0] - 0.8, 42), color=YEL)
arrow((agg[0] + agg[2] + 0.8, 48), (net[0] - 0.8, 60))
arrow((120, net[1] - 0.8), (120, 46.3))
arrow((120, struct[1] - 0.8), (120, 22.8))

# ---- Callout arrows (dashed provenance) -------------------------------------
arrow((49, 47.3), (49, expert[1] + 0.3), color=MUTED, lw=1.1)
arrow((49, pta[1] - 0.8), (49, 22.8), color=MUTED, lw=1.1)
arrow((85.5, wash[1] - 0.8), (85.5, 56.8), color=MUTED, lw=1.1)
arrow((methods[0] + methods[2] + 0.8, 16), (struct[0] - 0.8, 33),
      color=MUTED, lw=1.1, conn="arc3,rad=-0.12")

fig.tight_layout(pad=0.4)
fig.savefig(OUT / "figure1_process_diagram.png", dpi=300, bbox_inches="tight")
fig.savefig(OUT / "figure1_process_diagram.pdf", bbox_inches="tight")
fig.savefig(OUT / "figure1_process_diagram.svg", bbox_inches="tight")
print("wrote", OUT / "figure1_process_diagram.png")
