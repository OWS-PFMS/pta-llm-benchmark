#!/usr/bin/env python3
"""Figure 3 — influence/dependence map comparison, Expert (N&J) vs LLM (Claude).

Two panels (challenge, solution). Each factor appears twice — once per coder —
joined by a gray displacement arrow (expert -> LLM). Axes are influence
(weighted out-degree) and dependence (weighted in-degree), normalized to the
max factor in each network, matching the manuscript's §2.6 conventions.
Median-split quadrant thresholds are drawn per coder (dashed, series color)
because quadrant assignment in §2.6 uses each network's own medians.

Data: pta_232/centrality_{nj,claude}_{challenge,solution}.csv (verified to
reproduce the manuscript's Spearman/quadrant values exactly).
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "analysis"
OUT = Path(__file__).resolve().parent

# Series colors (validated: CVD dE 32.8, normal dE 38.9 on white surface).
BLUE = "#2166AC"    # Expert (N&J)
YELLOW = "#E8A50C"  # LLM (Claude) — low contrast vs white, so dark edge + labels
YELLOW_EDGE = "#8a6207"
INK = "#1a1a1a"
MUTED = "#6b6b6b"
FAINT = "#c9c9c9"

SHORT = {"Govt / External Finance": "Govt/Ext Finance",
         "Community Management": "Community Mgmt",
         "Laws + Regulations": "Laws + Regs",
         "Community / Users": "Community/Users"}

mpl.rcParams.update({
    "font.family": "Helvetica",
    "font.size": 9,
    "axes.edgecolor": FAINT,
    "axes.labelcolor": INK,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "axes.linewidth": 0.8,
})

def load(system):
    nj = pd.read_csv(DATA / f"centrality_nj_{system}.csv").set_index("bin")
    cl = pd.read_csv(DATA / f"centrality_claude_{system}.csv").set_index("bin")
    return nj, cl

def panel(ax, system, title):
    nj, cl = load(system)
    factors = nj.index.tolist()

    # Per-coder median-split thresholds (normalized units).
    for df, color in ((nj, BLUE), (cl, YELLOW_EDGE)):
        ax.axvline(df["dependence"].median(), color=color, lw=0.8, ls=(0, (4, 3)),
                   alpha=0.35, zorder=1)
        ax.axhline(df["influence"].median(), color=color, lw=0.8, ls=(0, (4, 3)),
                   alpha=0.35, zorder=1)

    # Displacement arrows expert -> LLM.
    for f in factors:
        x0, y0 = nj.loc[f, "dependence"], nj.loc[f, "influence"]
        x1, y1 = cl.loc[f, "dependence"], cl.loc[f, "influence"]
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color="#9a9a9a", lw=0.9,
                                    alpha=0.75, shrinkA=4.5, shrinkB=4.5),
                    zorder=2)

    ax.scatter(nj["dependence"], nj["influence"], s=52, color=BLUE,
               edgecolor="white", linewidth=0.8, zorder=3, label="Expert (N&J)")
    ax.scatter(cl["dependence"], cl["influence"], s=52, color=YELLOW,
               edgecolor=YELLOW_EDGE, linewidth=0.9, zorder=3, label="LLM (Claude)")

    # One label per factor, anchored to the displacement midpoint, repelled
    # from marks, with a leader line back to the anchor and a white halo so
    # labels stay readable where arrows cross.
    import matplotlib.patheffects as pe
    halo = [pe.withStroke(linewidth=2.2, foreground="white")]
    texts = []
    for f in factors:
        # Anchor every label at the expert (blue) point — the arrow tail —
        # so label-to-pair association follows one consistent rule.
        xm = nj.loc[f, "dependence"] + 0.012
        ym = nj.loc[f, "influence"] + 0.012
        texts.append(ax.text(xm, ym, SHORT.get(f, f), fontsize=7.4, color=INK,
                             zorder=5, path_effects=halo))
    try:
        from adjustText import adjust_text
        adjust_text(texts, ax=ax,
                    expand=(1.45, 1.75), force_text=(0.35, 0.6),
                    arrowprops=dict(arrowstyle="-", color="#8f8f8f", lw=0.7,
                                    shrinkA=2, shrinkB=2),
                    zorder=4)
    except ImportError:
        pass

    # Quadrant corner labels (muted, uppercase, recessive).
    lab = dict(fontsize=8, color=MUTED, style="italic", zorder=1)
    ax.text(0.02, 1.075, "LEVERAGE", ha="left", **lab)
    ax.text(1.06, 1.075, "DYNAMIC", ha="right", **lab)
    ax.text(1.06, -0.115, "OUTCOME", ha="right", **lab)
    ax.text(0.02, -0.115, "INCIDENTAL", ha="left", **lab)

    ax.set_title(title, fontsize=11, color=INK, pad=14, fontweight="bold")
    ax.set_xlabel("Dependence (weighted in-degree, normalized)")
    ax.set_xlim(-0.05, 1.09)
    ax.set_ylim(-0.15, 1.12)
    ax.spines[["top", "right"]].set_visible(False)
    ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])

fig, axes = plt.subplots(1, 2, figsize=(14.2, 7.1), sharey=True)
panel(axes[0], "challenge", "Challenge system")
panel(axes[1], "solution", "Solution system")
axes[0].set_ylabel("Influence (weighted out-degree, normalized)")

handles, labels = axes[0].get_legend_handles_labels()
import matplotlib.lines as mlines
handles.append(mlines.Line2D([], [], color="#9a9a9a", lw=1.1, marker=">",
                             markersize=5, markevery=(1, 1)))
labels.append(r"Displacement (expert $\rightarrow$ LLM)")
fig.legend(handles, labels, loc="lower center", ncol=3, frameon=False,
           fontsize=9, bbox_to_anchor=(0.5, -0.015))
fig.tight_layout(rect=(0, 0.045, 1, 1))

fig.savefig(OUT / "figure3_influence_maps.png", dpi=300, bbox_inches="tight")
fig.savefig(OUT / "figure3_influence_maps.pdf", bbox_inches="tight")
print("wrote", OUT / "figure3_influence_maps.png")
