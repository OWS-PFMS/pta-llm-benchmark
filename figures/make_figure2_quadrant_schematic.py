#!/usr/bin/env python3
"""Figure 2 — influence/dependence quadrant schematic, redrawn (per Jeff,
2026-08-21, replacing the PowerPoint original in the draft).

Conventions match Figure 3: dashed lines mark the quadrant boundaries,
quadrant names and positions are Leverage (I, top-left), Dynamic (II,
top-right), Outcome (III, bottom-right), Autonomous (IV, bottom-left).
Each cell carries its own high/low descriptor, replacing the corner
callouts of the original. Neutral palette (coder-agnostic), Helvetica.

Drawn at print size (per Jeff, 2026-08-22): the figure occupies about a
third of a portrait page's height, so the canvas is ~3.3 in tall and the
font sizes below are the sizes that actually print — no downscaling.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from pathlib import Path

OUT = Path(__file__).resolve().parent

NEUT = "#455A64"
TINT = "#ECEFF1"
INK = "#1a1a1a"
MUTED = "#6b6b6b"
DASH = "#9099a3"

mpl.rcParams.update({"font.family": "Helvetica"})

W, H = 3.75, 3.30
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect("equal")
ax.axis("off")

x0, x1, y0, y1 = 0.66, 3.67, 0.60, 3.22   # the square
cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
gap = 0.035                                # half-gap around the boundaries

cells = [
    # (cell x, cell y, numeral, name, descriptor)
    (x0, cy + gap, "I", "Leverage Factors",
     "high influence\nlow dependence"),
    (cx + gap, cy + gap, "II", "Dynamic Factors",
     "high influence\nhigh dependence"),
    (cx + gap, y0, "III", "Outcome Factors",
     "low influence\nhigh dependence"),
    (x0, y0, "IV", "Autonomous Factors",
     "low influence\nlow dependence"),
]
cw, ch = cx - gap - x0, cy - gap - y0

for px, py, numeral, name, desc in cells:
    ax.add_patch(FancyBboxPatch(
        (px, py), cw, ch, boxstyle="round,pad=0,rounding_size=0.06",
        facecolor=TINT, edgecolor="none", zorder=1))
    tx, ty = px + cw / 2, py + ch / 2
    ax.text(tx, ty + 0.37, numeral, fontsize=11, fontweight="bold",
            color="#78838d", ha="center", va="center", zorder=3)
    ax.text(tx, ty + 0.07, name, fontsize=10, fontweight="bold",
            color=INK, ha="center", va="center", zorder=3)
    ax.text(tx, ty - 0.13, desc, fontsize=7.5, color=MUTED,
            ha="center", va="top", linespacing=1.35, zorder=3)

# dashed quadrant boundaries, echoing Figure 3
ax.plot([cx, cx], [y0, y1], color=DASH, lw=1.0, ls=(0, (4, 3)), zorder=2)
ax.plot([x0, x1], [cy, cy], color=DASH, lw=1.0, ls=(0, (4, 3)), zorder=2)

# axes
ax.annotate("", xy=(x1, 0.335), xytext=(x0, 0.335),
            arrowprops=dict(arrowstyle="-|>", color=NEUT, lw=1.5,
                            mutation_scale=13))
ax.text(cx, 0.14, "Increasing dependence", fontsize=9.5, fontweight="bold",
        color=INK, ha="center", va="center")
ax.annotate("", xy=(0.36, y1), xytext=(0.36, y0),
            arrowprops=dict(arrowstyle="-|>", color=NEUT, lw=1.5,
                            mutation_scale=13))
ax.text(0.15, cy, "Increasing influence", fontsize=9.5, fontweight="bold",
        color=INK, ha="center", va="center", rotation=90)

fig.savefig(OUT / "figure2_quadrant_schematic.png", dpi=300,
            facecolor="white", bbox_inches="tight", pad_inches=0.15)
fig.savefig(OUT / "figure2_quadrant_schematic.pdf", facecolor="white",
            bbox_inches="tight", pad_inches=0.15)
print("wrote", OUT / "figure2_quadrant_schematic.png")
