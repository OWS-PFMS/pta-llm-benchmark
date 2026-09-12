#!/usr/bin/env python3
"""Figure 3 — influence/dependence map comparison, Expert (N&J) vs LLM (Claude).

Two panels (challenge, solution). Each factor appears twice — once per coder —
joined by a gray displacement arrow (expert -> LLM). Axes are influence
(weighted out-degree) and dependence (weighted in-degree), normalized to the
max factor in each network, matching the manuscript's §2.6 conventions.
Median-split quadrant thresholds are drawn per coder (dashed, series color)
because quadrant assignment in §2.6 uses each network's own medians.

Data: analysis/centrality_{nj,claude}_{challenge,solution}.csv (verified to
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

def panel(ax, system, title, k=1.0, grid="median", scale="max"):
    # k scales fonts/marks so one panel definition serves both the in-column
    # variants and the full-landscape-page variant Jeff asked for (2026-08-20).
    # grid:  "median" (paper; crosshair at the coders' medians, see below)
    #        "fixed"  (conventional; crosshair at 0.5/0.5 — Walters 2022's
    #                  "four equal quadrants", per Jeff's 2026-09-03 request)
    # scale: "max"    (paper; each score divided by the network's max factor)
    #        "minmax" (Walters 2022; lowest factor -> 0, highest -> 1)
    nj, cl = load(system)
    if scale == "minmax":
        for df in (nj, cl):
            for col in ("influence", "dependence"):
                lo, hi = df[col].min(), df[col].max()
                df[col] = (df[col] - lo) / (hi - lo)
    factors = nj.index.tolist()

    # Single quadrant crosshair (per Jeff, 2026-08-16): the drawn lines are
    # the midpoint of the two coders' median splits — a visual delineation of
    # the four quadrants. Each network's exact classification threshold is
    # its own median (§2.6); near-boundary factors are discussed in §3.3.
    if grid == "fixed":
        xq = yq = 0.5
    else:
        xq = (nj["dependence"].median() + cl["dependence"].median()) / 2
        yq = (nj["influence"].median() + cl["influence"].median()) / 2
    ax.axvline(xq, color="#b3b3b3", lw=0.9, ls=(0, (4, 3)), zorder=1)
    ax.axhline(yq, color="#b3b3b3", lw=0.9, ls=(0, (4, 3)), zorder=1)

    # Displacement arrows expert -> LLM.
    for f in factors:
        x0, y0 = nj.loc[f, "dependence"], nj.loc[f, "influence"]
        x1, y1 = cl.loc[f, "dependence"], cl.loc[f, "influence"]
        ax.annotate("", xy=(x1, y1), xytext=(x0, y0),
                    arrowprops=dict(arrowstyle="-|>", color="#9a9a9a", lw=0.9,
                                    alpha=0.75, shrinkA=4.5, shrinkB=4.5),
                    zorder=2)

    ax.scatter(nj["dependence"], nj["influence"], s=52 * k**2, color=BLUE,
               edgecolor="white", linewidth=0.8, zorder=3, label="Expert coders")
    ax.scatter(cl["dependence"], cl["influence"], s=52 * k**2, color=YELLOW,
               edgecolor=YELLOW_EDGE, linewidth=0.9, zorder=3, label="LLM")

    # One label per factor, anchored to the displacement midpoint, repelled
    # from marks, with a leader line back to the anchor and a white halo so
    # labels stay readable where arrows cross.
    import matplotlib.patheffects as pe
    halo = [pe.withStroke(linewidth=2.2 * k, foreground="white")]
    texts = []
    for f in factors:
        # Anchor every label at the expert (blue) point — the arrow tail —
        # so label-to-pair association follows one consistent rule.
        xm = nj.loc[f, "dependence"] + 0.012
        ym = nj.loc[f, "influence"] + 0.012
        texts.append(ax.text(xm, ym, SHORT.get(f, f), fontsize=7.4 * k,
                             color=INK, zorder=5, path_effects=halo))
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
    lab = dict(fontsize=8 * k, color=MUTED, style="italic", zorder=1)
    ax.text(0.02, 1.075, "LEVERAGE", ha="left", **lab)
    ax.text(1.06, 1.075, "DYNAMIC", ha="right", **lab)
    ax.text(1.06, -0.115, "OUTCOME", ha="right", **lab)
    ax.text(0.02, -0.115, "AUTONOMOUS", ha="left", **lab)

    ax.set_title(title, fontsize=11 * k, color=INK, pad=14, fontweight="bold")
    norm = "min\u2013max normalized" if scale == "minmax" else "normalized"
    ax.set_xlabel(f"Dependence (weighted in-degree, {norm})", fontsize=9 * k)
    ax.tick_params(labelsize=9 * k)
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
labels.append(r"Displacement (experts $\rightarrow$ LLM)")
handles.append(mlines.Line2D([], [], color="#b3b3b3", lw=1.1, ls=(0, (4, 3))))
labels.append("Quadrant boundaries")
fig.legend(handles, labels, loc="lower center", ncol=4, frameon=False,
           fontsize=9, bbox_to_anchor=(0.5, -0.015))
fig.tight_layout(rect=(0, 0.045, 1, 1))

fig.savefig(OUT / "figure3_influence_maps.png", dpi=300, bbox_inches="tight")
fig.savefig(OUT / "figure3_influence_maps.pdf", bbox_inches="tight")
print("wrote", OUT / "figure3_influence_maps.png")

# ---- Standalone single-panel versions (3a challenge, 3b solution) ----------
# Same panels, same run — regenerated together with the combined figure so
# the three outputs can never drift apart. Gives layout freedom in the doc.
def proxy_handles():
    dot = dict(marker="o", ls="", markersize=7)
    return ([mlines.Line2D([], [], color=BLUE, markeredgecolor="white", **dot),
             mlines.Line2D([], [], color=YELLOW, markeredgecolor=YELLOW_EDGE,
                           **dot),
             mlines.Line2D([], [], color="#9a9a9a", lw=1.1, marker=">",
                           markersize=5, markevery=(1, 1)),
             mlines.Line2D([], [], color="#b3b3b3", lw=1.1, ls=(0, (4, 3)))],
            ["Expert coders", "LLM",
             r"Displacement (experts $\rightarrow$ LLM)",
             "Quadrant boundaries"])

for system, title, stem in (("challenge", "Challenge system", "figure3a_challenge"),
                            ("solution", "Solution system", "figure3b_solution")):
    f1, a1 = plt.subplots(figsize=(7.8, 7.6))
    panel(a1, system, title)
    a1.set_ylabel("Influence (weighted out-degree, normalized)")
    h, l = proxy_handles()
    f1.legend(h, l, loc="lower center", ncol=3, frameon=False, fontsize=8.2,
              bbox_to_anchor=(0.5, -0.005))
    f1.tight_layout(rect=(0, 0.075, 1, 1))
    f1.savefig(OUT / f"{stem}.png", dpi=300, bbox_inches="tight")
    f1.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    print("wrote", OUT / f"{stem}.png")

# ---- Vertically stacked combined version (per Jeff: stacked + larger) ------
figs, axs = plt.subplots(2, 1, figsize=(8.8, 13.6))
panel(axs[0], "challenge", "Challenge system")
panel(axs[1], "solution", "Solution system")
for a in axs:
    a.set_ylabel("Influence (weighted out-degree, normalized)")
h, l = proxy_handles()
figs.legend(h, l, loc="lower center", ncol=2, frameon=False, fontsize=9,
            bbox_to_anchor=(0.5, -0.002))
figs.tight_layout(rect=(0, 0.035, 1, 1), h_pad=2.6)
figs.savefig(OUT / "figure3_influence_maps_stacked.png", dpi=300,
             bbox_inches="tight")
figs.savefig(OUT / "figure3_influence_maps_stacked.pdf", bbox_inches="tight")
print("wrote", OUT / "figure3_influence_maps_stacked.png")

# ---- Landscape full-page version (per Jeff, 2026-08-20) --------------------
# Side-by-side panels sized so the figure prints at ~100% on a landscape
# letter page (0.75" margins leave ~9.5" of width) with room below the plot
# for a caption — Jeff wants figure + caption to fill the page. Fonts are
# scaled up (k) so they are real point sizes at print, not shrunk-to-fit.
K = 1.15
figl, axl = plt.subplots(1, 2, figsize=(10.6, 6.9), sharey=True)
panel(axl[0], "challenge", "Challenge system", k=K)
panel(axl[1], "solution", "Solution system", k=K)
axl[0].set_ylabel("Influence (weighted out-degree, normalized)",
                  fontsize=9 * K)
h, l = proxy_handles()
figl.legend(h, l, loc="lower center", ncol=4, frameon=False, fontsize=9 * K,
            bbox_to_anchor=(0.5, -0.012))
figl.tight_layout(rect=(0, 0.05, 1, 1))
figl.savefig(OUT / "figure3_influence_maps_landscape.png", dpi=300,
             bbox_inches="tight")
figl.savefig(OUT / "figure3_influence_maps_landscape.pdf",
             bbox_inches="tight")
print("wrote", OUT / "figure3_influence_maps_landscape.png")

# ---- Conventional 0.5/0.5 grid (per Jeff, 2026-09-03) ----------------------
# "What would it look like with the grid unnormalized to the median, as it is
# usually shown?" Same points, same arrows — only the crosshair moves to the
# fixed midpoint of the [0, 1] axes (Walters 2022 / Godet: "four equal
# quadrants"). Two flavors: (a) our max-normalized scores (the paper's axes),
# and (b) Walters 2022's min-max rescale (lowest factor -> 0), which shifts
# points slightly and is the literal antecedent-study convention.
def grid05_legend():
    h, l = proxy_handles()
    l[-1] = "Quadrant boundaries (fixed at 0.5)"
    return h, l

for scale, stem, tag in (("max", "figure3_influence_maps_grid05", ""),
                         ("minmax", "figure3_influence_maps_grid05_minmax",
                          " (min\u2013max scaled, Walters 2022)")):
    fg, ag = plt.subplots(1, 2, figsize=(14.2, 7.1), sharey=True)
    panel(ag[0], "challenge", "Challenge system" + tag, grid="fixed",
          scale=scale)
    panel(ag[1], "solution", "Solution system" + tag, grid="fixed",
          scale=scale)
    norm = "min\u2013max normalized" if scale == "minmax" else "normalized"
    ag[0].set_ylabel(f"Influence (weighted out-degree, {norm})")
    h, l = grid05_legend()
    fg.legend(h, l, loc="lower center", ncol=4, frameon=False, fontsize=9,
              bbox_to_anchor=(0.5, -0.015))
    fg.tight_layout(rect=(0, 0.045, 1, 1))
    fg.savefig(OUT / f"{stem}.png", dpi=300, bbox_inches="tight")
    fg.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    print("wrote", OUT / f"{stem}.png")

# Stacked (Jeff's preferred in-doc layout) for the primary 0.5-grid variant.
fgs, ags = plt.subplots(2, 1, figsize=(8.8, 13.6))
panel(ags[0], "challenge", "Challenge system", grid="fixed")
panel(ags[1], "solution", "Solution system", grid="fixed")
for a in ags:
    a.set_ylabel("Influence (weighted out-degree, normalized)")
h, l = grid05_legend()
fgs.legend(h, l, loc="lower center", ncol=2, frameon=False, fontsize=9,
           bbox_to_anchor=(0.5, -0.002))
fgs.tight_layout(rect=(0, 0.035, 1, 1), h_pad=2.6)
fgs.savefig(OUT / "figure3_influence_maps_grid05_stacked.png", dpi=300,
            bbox_inches="tight")
fgs.savefig(OUT / "figure3_influence_maps_grid05_stacked.pdf",
            bbox_inches="tight")
print("wrote", OUT / "figure3_influence_maps_grid05_stacked.png")
