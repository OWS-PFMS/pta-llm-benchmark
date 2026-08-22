#!/usr/bin/env python3
"""Figure 1b — the LLM's PTA workflow, pictorial (per Jeff, 2026-08-21).

Companion to the Figure 1 study-overview infographic: a step-by-step view
of what the LLM actually does, so a reader can replicate the pipeline.
Same hand-drawn icon set and palette as Figure 1 (imported from
make_figure1_pictorial_variants.py, which must sit in the same directory).
Yellow badges mark the two steps performed by the LLM itself; gray badges
are deterministic scripted steps.

Drawn at portrait print width so point sizes are true at print.
"""
from matplotlib.patches import Circle, FancyBboxPatch, Polygon

from make_figure1_pictorial_variants import (
    NEUT, NEUT_TINT, YELLOW_DARK, YELLOW_TINT, INK, MUTED,
    canvas, save, arrow, badge,
    icon_docs, icon_network, icon_quadrant)

# ------------------------------------------------- icons new to this figure
def icon_prompt(ax, cx, cy, s, c):
    """Terminal/prompt card: > with a command line and a cursor block."""
    w, h = 1.10 * s, 0.86 * s
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - h / 2), w, h,
        boxstyle=f"round,pad=0,rounding_size={0.10 * s}",
        facecolor="white", edgecolor=c, linewidth=1.7, zorder=4))
    px, py = cx - 0.34 * s, cy + 0.13 * s
    ax.plot([px, px + 0.15 * s, px], [py + 0.12 * s, py, py - 0.12 * s],
            color=c, lw=1.8, solid_capstyle="round",
            solid_joinstyle="round", zorder=5)
    ax.plot([px + 0.27 * s, px + 0.72 * s], [py, py],
            color=c, lw=1.6, solid_capstyle="round", zorder=5)
    ax.add_patch(Polygon(
        [(px + 0.02 * s, py - 0.40 * s), (px + 0.14 * s, py - 0.40 * s),
         (px + 0.14 * s, py - 0.24 * s), (px + 0.02 * s, py - 0.24 * s)],
        facecolor=c, edgecolor="none", zorder=5))

def icon_causal(ax, cx, cy, s, c):
    """Two factors joined by a signed causal arrow."""
    a = (cx - 0.42 * s, cy - 0.08 * s)
    b = (cx + 0.42 * s, cy - 0.08 * s)
    ax.add_patch(Circle(a, 0.16 * s, facecolor=c, edgecolor="none",
                        zorder=5))
    ax.add_patch(Circle(b, 0.16 * s, facecolor="white", edgecolor=c,
                        linewidth=1.7, zorder=5))
    ax.annotate("", xy=(b[0] - 0.22 * s, b[1]), xytext=(a[0] + 0.22 * s, a[1]),
                arrowprops=dict(arrowstyle="-|>", color=c, lw=1.7,
                                mutation_scale=11))
    ax.text(cx, cy + 0.34 * s, "+/−", fontsize=15 * s, color=c,
            fontweight="bold", ha="center", va="center", zorder=5)

def icon_funnel(ax, cx, cy, s, c):
    """Many context-specific factors funneled into few cross-case factors."""
    top, waist = 0.46 * s, 0.10 * s
    pts = [(cx - top, cy + 0.36 * s), (cx + top, cy + 0.36 * s),
           (cx + waist, cy - 0.04 * s), (cx + waist, cy - 0.38 * s),
           (cx - waist, cy - 0.38 * s), (cx - waist, cy - 0.04 * s)]
    ax.add_patch(Polygon(pts, facecolor="white", edgecolor=c,
                         linewidth=1.7, zorder=4))
    for dx, dy, rr in ((-0.27, 0.52, 0.055), (0.0, 0.62, 0.045),
                       (0.25, 0.50, 0.055)):
        ax.add_patch(Circle((cx + dx * s, cy + dy * s), rr * s,
                            facecolor=c, edgecolor="none", zorder=5))
    ax.add_patch(Circle((cx, cy - 0.54 * s), 0.065 * s, facecolor=c,
                        edgecolor="none", zorder=5))

# ------------------------------------------------------------------ layout
STEPS_1B = [
    # (title, sub, ring, tint, icon)
    ("Interview Transcripts",
     "232 WASH key-informant interviews",
     NEUT, NEUT_TINT, icon_docs),
    ("PTA Coding Prompt",
     "purposive text analysis coding rules issued to the\n"
     "LLM as a version-controlled, reproducible prompt",
     YELLOW_DARK, YELLOW_TINT, icon_prompt),
    ("Causal Statement Extraction",
     "cause–effect pairs with polarity, challenge/solution\n"
     "label, and a verbatim source excerpt per statement",
     YELLOW_DARK, YELLOW_TINT, icon_causal),
    ("Factor Aggregation",
     "context-specific factor names mapped onto the\n"
     "17 cross-case WASH factors by deterministic rules",
     NEUT, NEUT_TINT, icon_funnel),
    ("Network Assembly",
     "weighted, directed challenge & solution networks:\n"
     "edge lists and adjacency matrices",
     NEUT, NEUT_TINT, icon_network),
    ("Structural Analysis",
     "eigenvector centrality · influence–dependence\n"
     "quadrants · feedback-loop inventory",
     NEUT, NEUT_TINT, icon_quadrant),
]

def build():
    W, H = 7.2, 9.7
    fig, ax = canvas(W, H)
    sx = 1.40
    ys = [8.80 - 1.44 * i for i in range(6)]

    ax.plot([sx, sx], [ys[-1], ys[0]], color="#cfd8dc", lw=3.5, zorder=1,
            solid_capstyle="round")

    for i, (title, sub, ring, tint, icon) in enumerate(STEPS_1B):
        y = ys[i]
        ax.text(0.52, y, f"0{i + 1}", fontsize=21, fontweight="bold",
                color="#7f8d96", ha="center", va="center", zorder=2)
        badge(ax, sx, y, 0.48, ring, tint)
        icon(ax, sx, y, 0.50, ring)
        ax.text(2.55, y + 0.29, title, fontsize=15, fontweight="bold",
                color=INK, ha="left", va="center", zorder=6)
        ax.text(2.55, y + 0.02, sub, fontsize=10.6, color=MUTED,
                ha="left", va="top", linespacing=1.35, zorder=6)

    for y0, y1 in zip(ys[:-1], ys[1:]):
        arrow(ax, (sx, y0 - 0.52), (sx, y1 + 0.52), lw=1.6, ms=12)

    ax.text(3.60, 0.52,
            "Yellow badges: steps performed by the LLM (Claude).  Gray "
            "badges: deterministic, scripted steps —\n"
            "re-running them on the LLM's coded statements reproduces the "
            "published networks exactly.",
            fontsize=9.6, color=MUTED, ha="center", va="center",
            linespacing=1.4, zorder=6)

    save(fig, "figure1b_llm_workflow")

if __name__ == "__main__":
    build()
