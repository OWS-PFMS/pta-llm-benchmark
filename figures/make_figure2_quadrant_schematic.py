#!/usr/bin/env python3
"""Figure 2 — influence/dependence quadrant schematic, redrawn (per Jeff,
2026-08-21, replacing the PowerPoint original in the draft).

Conventions match Figure 3: dashed lines mark the quadrant boundaries,
quadrant names and positions are Leverage (I, top-left), Dynamic (II,
top-right), Outcome (III, bottom-right), Autonomous (IV, bottom-left).
Each cell carries its own high/low descriptor, replacing the corner
callouts of the original. Neutral palette (coder-agnostic), Helvetica,
drawn at print size.
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

W, H = 5.8, 5.5
fig = plt.figure(figsize=(W, H))
ax = fig.add_axes([0, 0, 1, 1])
ax.set_xlim(0, W)
ax.set_ylim(0, H)
ax.set_aspect("equal")
ax.axis("off")

x0, x1, y0, y1 = 1.05, 5.45, 0.95, 5.35   # the square
cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
gap = 0.055                                # half-gap around the boundaries

cells = [
    # (cell x, cell y, numeral, name, descriptor)
    (x0, cy + gap, "I", "Leverage Factors",
     "high influence · low dependence"),
    (cx + gap, cy + gap, "II", "Dynamic Factors",
     "high influence · high dependence"),
    (cx + gap, y0, "III", "Outcome Factors",
     "low influence · high dependence"),
    (x0, y0, "IV", "Autonomous Factors",
     "low influence · low dependence"),
]
cw, ch = cx - gap - x0, cy - gap - y0

for px, py, numeral, name, desc in cells:
    ax.add_patch(FancyBboxPatch(
        (px, py), cw, ch, boxstyle="round,pad=0,rounding_size=0.10",
        facecolor=TINT, edgecolor="none", zorder=1))
    tx, ty = px + cw / 2, py + ch / 2
    ax.text(tx, ty + 0.42, numeral, fontsize=13, fontweight="bold",
            color="#78838d", ha="center", va="center", zorder=3)
    ax.text(tx, ty - 0.02, name, fontsize=12.5, fontweight="bold",
            color=INK, ha="center", va="center", zorder=3)
    ax.text(tx, ty - 0.42, desc, fontsize=8.6, color=MUTED,
            ha="center", va="center", zorder=3)

# dashed quadrant boundaries, echoing Figure 3
ax.plot([cx, cx], [y0, y1], color=DASH, lw=1.3, ls=(0, (4, 3)), zorder=2)
ax.plot([x0, x1], [cy, cy], color=DASH, lw=1.3, ls=(0, (4, 3)), zorder=2)

# axes
ax.annotate("", xy=(x1, 0.52), xytext=(x0, 0.52),
            arrowprops=dict(arrowstyle="-|>", color=NEUT, lw=1.8,
                            mutation_scale=16))
ax.text(cx, 0.22, "Increasing dependence", fontsize=11, fontweight="bold",
        color=INK, ha="center", va="center")
ax.annotate("", xy=(0.55, y1), xytext=(0.55, y0),
            arrowprops=dict(arrowstyle="-|>", color=NEUT, lw=1.8,
                            mutation_scale=16))
ax.text(0.24, cy, "Increasing influence", fontsize=11, fontweight="bold",
        color=INK, ha="center", va="center", rotation=90)

fig.savefig(OUT / "figure2_quadrant_schematic.png", dpi=300,
            facecolor="white", bbox_inches="tight", pad_inches=0.2)
fig.savefig(OUT / "figure2_quadrant_schematic.pdf", facecolor="white",
            bbox_inches="tight", pad_inches=0.2)
print("wrote", OUT / "figure2_quadrant_schematic.png")
