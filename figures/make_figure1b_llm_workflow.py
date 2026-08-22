#!/usr/bin/env python3
"""Figure 1b — the LLM's PTA workflow, pictorial (per Jeff, 2026-08-21).

Companion to the Figure 1 study-overview infographic: a step-by-step view
of what the LLM actually does, so a reader can replicate the pipeline.
Same hand-drawn icon set and palette as Figure 1 (imported from
make_figure1_pictorial_variants.py, which must sit in the same directory).

Color encodes role (per Charles, 2026-08-22): green = the input corpus
(not part of the process), yellow = the two steps performed by the LLM
itself, gray = deterministic scripted steps.

Two layouts from one script: the vertical numbered list, and a staged
grid (input on top, LLM row, script row) that keeps type large.
"""
from matplotlib.patches import Circle, FancyBboxPatch, Polygon

from make_figure1_pictorial_variants import (
    NEUT, NEUT_TINT, YELLOW_DARK, YELLOW_TINT, INK, MUTED,
    canvas, save, arrow, badge,
    icon_docs, icon_network, icon_quadrant)

GREEN = "#3A7D44"        # input corpus (distinct from process colors)
GREEN_TINT = "#E7F1E8"

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
     GREEN, GREEN_TINT, icon_docs),
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
            "Green: the input corpus.  Yellow: steps performed by the LLM "
            "(Claude).  Gray: deterministic,\nscripted steps — re-running "
            "them on the LLM's coded statements reproduces the published "
            "networks exactly.",
            fontsize=9.6, color=MUTED, ha="center", va="center",
            linespacing=1.4, zorder=6)

    save(fig, "figure1b_llm_workflow")

# Sub text re-wrapped for narrow columns (same content as STEPS_1B)
SUBS_G = [
    "232 WASH key-informant interviews",
    "purposive text analysis coding\nrules issued to the LLM as a\n"
    "version-controlled prompt",
    "cause–effect pairs with polarity,\nchallenge/solution label, and a\n"
    "verbatim excerpt per statement",
    "context-specific factor names\nmapped onto the 17 cross-case\n"
    "WASH factors · deterministic rules",
    "weighted, directed challenge &\nsolution networks: edge lists\n"
    "and adjacency matrices",
    "eigenvector centrality ·\ninfluence–dependence quadrants ·\n"
    "feedback-loop inventory",
]

def build_grid():
    """Staged-grid variant (per Charles, 2026-08-22): input corpus on top
    (green), the two LLM-performed steps (yellow), then the three
    deterministic script steps (gray). The legend fills the grid's empty
    top-right cell."""
    W, H = 8.2, 7.5
    fig, ax = canvas(W, H)
    xs = [1.5, 4.1, 6.7]
    by1, by2, by3 = 6.30, 4.60, 1.85

    def num(cx, by, i):
        ax.text(cx - 0.80, by + 0.72, f"0{i}", fontsize=17,
                fontweight="bold", color="#7f8d96", ha="center",
                va="center", zorder=2)

    def cell(cx, by, i, entry, sub):
        title, _, ring, tint, icon = entry
        num(cx, by, i)
        badge(ax, cx, by, 0.50, ring, tint)
        icon(ax, cx, by, 0.52, ring)
        ax.text(cx, by - 0.82, title, fontsize=12.5, fontweight="bold",
                color=INK, ha="center", va="center", zorder=6)
        ax.text(cx, by - 1.06, sub, fontsize=9.5, color=MUTED,
                ha="center", va="top", linespacing=1.3, zorder=6)

    # 01 — the input, side text so the top row stays compact
    num(xs[0], by1, 1)
    badge(ax, xs[0], by1, 0.50, GREEN, GREEN_TINT)
    icon_docs(ax, xs[0], by1, 0.52, GREEN)
    ax.text(2.30, by1 + 0.15, STEPS_1B[0][0], fontsize=12.5,
            fontweight="bold", color=INK, ha="left", va="center", zorder=6)
    ax.text(2.30, by1 - 0.15, SUBS_G[0], fontsize=9.5, color=MUTED,
            ha="left", va="center", zorder=6)

    cell(xs[0], by2, 2, STEPS_1B[1], SUBS_G[1])
    cell(xs[1], by2, 3, STEPS_1B[2], SUBS_G[2])
    cell(xs[0], by3, 4, STEPS_1B[3], SUBS_G[3])
    cell(xs[1], by3, 5, STEPS_1B[4], SUBS_G[4])
    cell(xs[2], by3, 6, STEPS_1B[5], SUBS_G[5])

    # no arrows: the numbering and the staged rows imply the flow
    # (per Charles, 2026-08-22 — the row-2 -> row-3 connector could not
    # cross the text cleanly, and the numbers carry the order anyway)

    # legend in the empty top-right cell
    keys = [(GREEN, GREEN_TINT, "input data"),
            (YELLOW_DARK, YELLOW_TINT, "steps performed by the LLM"),
            (NEUT, NEUT_TINT, "deterministic scripted steps")]
    for j, (ring, tint, label) in enumerate(keys):
        yk = by2 + 0.42 - 0.34 * j
        ax.add_patch(Circle((5.95, yk), 0.11, facecolor=tint,
                            edgecolor=ring, linewidth=1.6, zorder=3))
        ax.text(6.18, yk, label, fontsize=9.5, color=INK, ha="left",
                va="center", zorder=6)
    ax.text(5.84, by2 - 0.62,
            "re-running the gray steps on the\nLLM's coded statements "
            "reproduces\nthe published networks exactly",
            fontsize=8.8, color=MUTED, ha="left", va="top",
            linespacing=1.3, zorder=6)

    save(fig, "figure1b_llm_workflow_grid")

if __name__ == "__main__":
    build()
    build_grid()
