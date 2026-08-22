#!/usr/bin/env python3
"""Figure 1 — five PICTORIAL process-diagram candidates (per Jeff, 2026-08-20).

Jeff asked for a high-level, graphical-abstract-style view: only the
top-level steps (e.g. "Expert Coding"), no methodological citations inside
boxes, with icons next to / under each step. These five variants share one
icon set and the paper's palette (blue = expert, yellow = LLM) but differ
in layout so the team can pick a favorite or combine elements:

  v1  horizontal strip with a fork (classic graphical abstract)
  v2  parallel swimlanes (emphasizes the benchmark design)
  v3  vertical numbered infographic (portrait / single column)
  v4  chevron band (process ribbon)
  v5  numbered cards on an S-path

All icons are hand-drawn vector shapes (no emoji, no external images), so
the PDF/SVG output stays fully scalable and journal-safe.
"""
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import (Circle, FancyBboxPatch, Polygon, Wedge)
from pathlib import Path

OUT = Path(__file__).resolve().parent

BLUE = "#2166AC"        # expert coders (matches Figure 3)
BLUE_TINT = "#E1EBF5"
YELLOW = "#E8A50C"      # LLM (matches Figure 3)
YELLOW_DARK = "#8a6207" # legible stand-in for yellow in text
YELLOW_TINT = "#FBF1D9"
NEUT = "#455A64"        # neutral pipeline steps (blue-gray)
NEUT_TINT = "#ECEFF1"
INK = "#1a1a1a"
MUTED = "#6b6b6b"
ARROW = "#9aa5ad"

mpl.rcParams.update({"font.family": "Helvetica"})

STEPS = {
    "transcripts": ("Interview Transcripts", "232 WASH key-informant interviews"),
    "expert": ("Expert Coding", "human benchmark"),
    "llm": ("LLM Coding", "Claude"),
    "networks": ("Causal Networks", "17 factors · challenge & solution"),
    "analysis": ("Structural Analysis", "centrality · quadrants · feedback loops"),
    "compare": ("Benchmark Comparison", "expert vs. LLM agreement"),
}

# ---------------------------------------------------------------- canvas ----
def canvas(W, H):
    fig = plt.figure(figsize=(W, H))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.set_aspect("equal")
    ax.axis("off")
    return fig, ax

def save(fig, stem):
    fig.savefig(OUT / f"{stem}.png", dpi=300, facecolor="white",
                bbox_inches="tight", pad_inches=0.25)
    fig.savefig(OUT / f"{stem}.pdf", facecolor="white",
                bbox_inches="tight", pad_inches=0.25)
    plt.close(fig)
    print("wrote", OUT / f"{stem}.png")

def arrow(ax, p0, p1, rad=0.0, color=ARROW, lw=1.8, ms=14):
    ax.annotate("", xy=p1, xytext=p0,
                arrowprops=dict(arrowstyle="-|>", color=color, lw=lw,
                                mutation_scale=ms, shrinkA=0, shrinkB=0,
                                connectionstyle=f"arc3,rad={rad}"))

def badge(ax, cx, cy, r, ring, tint, lw=2.2):
    ax.add_patch(Circle((cx, cy), r, facecolor=tint, edgecolor=ring,
                        linewidth=lw, zorder=3))

def title_sub(ax, x, y, key, ts=12, ss=9, ha="center", gap=0.30,
              color=INK, sub_color=MUTED):
    t, s = STEPS[key]
    ax.text(x, y, t, fontsize=ts, fontweight="bold", color=color,
            ha=ha, va="center", zorder=6)
    ax.text(x, y - gap, s, fontsize=ss, color=sub_color,
            ha=ha, va="center", zorder=6)

# ----------------------------------------------------------------- icons ----
# Each draws centered on (cx, cy); s is a scale in inches; c is glyph color.

def icon_docs(ax, cx, cy, s, c, page="white"):
    w, h, rd = 0.82 * s, 1.04 * s, 0.05 * s
    for dx, dy, alpha in ((0.13 * s, 0.13 * s, 0.5), (0, 0, 1.0)):
        ax.add_patch(FancyBboxPatch(
            (cx - w / 2 + dx, cy - h / 2 + dy), w, h,
            boxstyle=f"round,pad=0,rounding_size={rd}",
            facecolor=page, edgecolor=c, linewidth=1.7, alpha=alpha,
            zorder=4 if alpha == 1 else 3.5))
    for i, frac in enumerate((0.72, 0.55, 0.62)):
        y = cy + (0.22 - 0.22 * i) * s
        ax.plot([cx - w * 0.32, cx - w * 0.32 + w * frac * 0.72], [y, y],
                color=c, lw=1.5, solid_capstyle="round", zorder=5)

def _person(ax, px, py, s, c, alpha=1.0):
    ax.add_patch(Circle((px, py + 0.30 * s), 0.20 * s, facecolor=c,
                        edgecolor="none", alpha=alpha, zorder=5))
    ax.add_patch(Wedge((px, py - 0.34 * s), 0.34 * s, 0, 180,
                       facecolor=c, edgecolor="none", alpha=alpha, zorder=5))

def icon_people(ax, cx, cy, s, c):
    _person(ax, cx - 0.26 * s, cy + 0.10 * s, 0.82 * s, c, alpha=0.45)
    _person(ax, cx + 0.16 * s, cy - 0.02 * s, s, c)

def _star4(cx, cy, r, waist=0.24):
    pts = [(0, 1), (waist, waist), (1, 0), (waist, -waist), (0, -1),
           (-waist, -waist), (-1, 0), (-waist, waist)]
    return [(cx + px * r, cy + py * r) for px, py in pts]

def icon_sparkle(ax, cx, cy, s, c):
    w = 1.06 * s
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - w / 2), w, w,
        boxstyle=f"round,pad=0,rounding_size={0.12 * s}",
        facecolor="none", edgecolor=c, linewidth=1.7, zorder=4))
    for side in (-1, 1):  # chip pins
        for dy in (-0.26 * s, 0, 0.26 * s):
            x0 = cx + side * w / 2
            ax.plot([x0, x0 + side * 0.14 * s], [cy + dy, cy + dy],
                    color=c, lw=1.5, solid_capstyle="round", zorder=4)
    ax.add_patch(Polygon(_star4(cx - 0.06 * s, cy - 0.05 * s, 0.34 * s),
                         facecolor=c, edgecolor="none", zorder=5))
    ax.add_patch(Polygon(_star4(cx + 0.27 * s, cy + 0.26 * s, 0.14 * s),
                         facecolor=c, edgecolor="none", zorder=5))

def icon_network(ax, cx, cy, s, c):
    import math
    outer = [(cx + 0.52 * s * math.cos(math.radians(a)),
              cy + 0.52 * s * math.sin(math.radians(a)))
             for a in (25, 115, 205, 295)]
    for x, y in outer:
        ax.plot([cx, x], [cy, y], color=c, lw=1.5, zorder=4)
    ax.plot([outer[0][0], outer[1][0]], [outer[0][1], outer[1][1]],
            color=c, lw=1.2, alpha=0.6, zorder=4)
    ax.plot([outer[2][0], outer[3][0]], [outer[2][1], outer[3][1]],
            color=c, lw=1.2, alpha=0.6, zorder=4)
    ax.add_patch(Circle((cx, cy), 0.13 * s, facecolor=c, zorder=5))
    for x, y in outer:
        ax.add_patch(Circle((x, y), 0.095 * s, facecolor=c, zorder=5))

def icon_quadrant(ax, cx, cy, s, c):
    w, rd = 1.12 * s, 0.10 * s
    ax.add_patch(FancyBboxPatch(
        (cx - w / 2, cy - w / 2), w, w,
        boxstyle=f"round,pad=0,rounding_size={rd}",
        facecolor="white", edgecolor=c, linewidth=1.7, zorder=4))
    ax.plot([cx, cx], [cy - w * 0.42, cy + w * 0.42], color=c, lw=1.1,
            ls=(0, (2, 2)), zorder=5)
    ax.plot([cx - w * 0.42, cx + w * 0.42], [cy, cy], color=c, lw=1.1,
            ls=(0, (2, 2)), zorder=5)
    ax.add_patch(Circle((cx - 0.24 * s, cy + 0.26 * s), 0.10 * s,
                        facecolor=c, zorder=6))
    ax.add_patch(Circle((cx + 0.26 * s, cy + 0.18 * s), 0.065 * s,
                        facecolor=c, alpha=0.45, zorder=6))
    ax.add_patch(Circle((cx - 0.18 * s, cy - 0.26 * s), 0.065 * s,
                        facecolor=c, alpha=0.45, zorder=6))

def icon_compare(ax, cx, cy, s, check=True):
    ax.add_patch(Circle((cx - 0.21 * s, cy), 0.40 * s, facecolor=BLUE,
                        edgecolor="none", alpha=0.85, zorder=4))
    ax.add_patch(Circle((cx + 0.21 * s, cy), 0.40 * s, facecolor=YELLOW,
                        edgecolor=YELLOW_DARK, linewidth=1.0, alpha=0.80,
                        zorder=5))
    if check:
        ax.plot([cx - 0.12 * s, cx - 0.01 * s, cx + 0.19 * s],
                [cy + 0.01 * s, cy - 0.13 * s, cy + 0.17 * s],
                color="white", lw=2.4, solid_capstyle="round",
                solid_joinstyle="round", zorder=6)

# ------------------------------------------------- v1: horizontal strip ----
def build_v1():
    W, H = 13.6, 5.3
    fig, ax = canvas(W, H)
    cy, r = 3.15, 0.60

    xs = {"transcripts": 1.45, "fork": 4.15, "networks": 6.95,
          "analysis": 9.70, "compare": 12.35}

    badge(ax, xs["transcripts"], cy, r, NEUT, NEUT_TINT)
    icon_docs(ax, xs["transcripts"], cy, 0.62, NEUT)
    title_sub(ax, xs["transcripts"], 2.10, "transcripts", ts=11.5, ss=8.8)

    # fork: expert above, LLM below
    ex, lx = (xs["fork"], 3.92), (xs["fork"], 2.38)
    badge(ax, *ex, 0.50, BLUE, BLUE_TINT)
    icon_people(ax, ex[0], ex[1], 0.50, BLUE)
    ax.text(ex[0], 4.75, STEPS["expert"][0], fontsize=11.5,
            fontweight="bold", color=INK, ha="center", va="center")
    ax.text(ex[0], 4.47, STEPS["expert"][1], fontsize=8.8, color=MUTED,
            ha="center", va="center")
    badge(ax, *lx, 0.50, YELLOW_DARK, YELLOW_TINT)
    icon_sparkle(ax, lx[0], lx[1], 0.50, YELLOW_DARK)
    ax.text(lx[0], 1.55, STEPS["llm"][0], fontsize=11.5,
            fontweight="bold", color=INK, ha="center", va="center")
    ax.text(lx[0], 1.27, STEPS["llm"][1], fontsize=8.8, color=MUTED,
            ha="center", va="center")

    badge(ax, xs["networks"], cy, r, NEUT, NEUT_TINT)
    icon_network(ax, xs["networks"], cy, 0.62, NEUT)
    title_sub(ax, xs["networks"], 2.10, "networks", ts=11.5, ss=8.8)

    badge(ax, xs["analysis"], cy, r, NEUT, NEUT_TINT)
    icon_quadrant(ax, xs["analysis"], cy, 0.60, NEUT)
    title_sub(ax, xs["analysis"], 2.10, "analysis", ts=11.5, ss=8.8)

    badge(ax, xs["compare"], cy, r, NEUT, "white")
    icon_compare(ax, xs["compare"], cy, 0.62)
    title_sub(ax, xs["compare"], 2.10, "compare", ts=11.5, ss=8.8)

    # arrows: fork out of transcripts, converge into networks, then chain
    arrow(ax, (xs["transcripts"] + r + 0.06, cy + 0.18),
          (ex[0] - 0.56, ex[1] - 0.08), rad=-0.22)
    arrow(ax, (xs["transcripts"] + r + 0.06, cy - 0.18),
          (lx[0] - 0.56, lx[1] + 0.08), rad=0.22)
    arrow(ax, (ex[0] + 0.56, ex[1] - 0.08),
          (xs["networks"] - r - 0.06, cy + 0.18), rad=-0.22)
    arrow(ax, (lx[0] + 0.56, lx[1] + 0.08),
          (xs["networks"] - r - 0.06, cy - 0.18), rad=0.22)
    arrow(ax, (xs["networks"] + r + 0.06, cy),
          (xs["analysis"] - r - 0.06, cy))
    arrow(ax, (xs["analysis"] + r + 0.06, cy),
          (xs["compare"] - r - 0.06, cy))
    save(fig, "figure1_pictorial_v1_strip")

# ------------------------------------------------------ v2: swimlanes ------
def build_v2():
    W, H = 13.6, 6.4
    fig, ax = canvas(W, H)
    mid = 3.2

    badge(ax, 1.25, mid, 0.62, NEUT, NEUT_TINT)
    icon_docs(ax, 1.25, mid, 0.64, NEUT)
    title_sub(ax, 1.25, 2.05, "transcripts", ts=11, ss=8.6)

    lanes = [(BLUE, BLUE_TINT, 4.55, "EXPERT  ·  human benchmark",
              icon_people),
             (YELLOW_DARK, YELLOW_TINT, 1.85, "LLM  ·  Claude",
              icon_sparkle)]
    for color, tint, cy, label, coder_icon in lanes:
        ax.add_patch(FancyBboxPatch(
            (2.65, cy - 0.92), 6.45, 1.84,
            boxstyle="round,pad=0,rounding_size=0.18",
            facecolor=tint, edgecolor=color, linewidth=1.4, alpha=0.9,
            zorder=2))
        ax.text(2.95, cy + 0.68, label, fontsize=8.6, fontweight="bold",
                color=color, ha="left", va="center", zorder=6)
        # step 1 in lane: coding
        badge(ax, 4.05, cy - 0.10, 0.44, color, "white", lw=1.8)
        coder_icon(ax, 4.05, cy - 0.10, 0.44, color)
        ax.text(4.05, cy - 0.74, "Purposive Coding", fontsize=9.2,
                fontweight="bold", color=INK, ha="center", va="center",
                zorder=6)
        # step 2 in lane: network
        badge(ax, 7.45, cy - 0.10, 0.44, color, "white", lw=1.8)
        icon_network(ax, 7.45, cy - 0.10, 0.46, color)
        ax.text(7.45, cy - 0.74, "Causal Network", fontsize=9.2,
                fontweight="bold", color=INK, ha="center", va="center",
                zorder=6)
        arrow(ax, (4.60, cy - 0.10), (6.90, cy - 0.10), color=color, lw=1.5)

    # note sits in the gap between the two Causal Network icons
    ax.text(7.45, 3.18, "17 shared factors · challenge & solution",
            fontsize=8.6, color=MUTED, ha="center", va="center", zorder=6)

    badge(ax, 10.45, mid, 0.60, NEUT, NEUT_TINT)
    icon_quadrant(ax, 10.45, mid, 0.60, NEUT)
    title_sub(ax, 10.45, 2.05, "analysis", ts=11, ss=8.6)

    badge(ax, 12.55, mid, 0.60, NEUT, "white")
    icon_compare(ax, 12.55, mid, 0.62)
    title_sub(ax, 12.55, 2.05, "compare", ts=11, ss=8.6)

    arrow(ax, (1.92, mid + 0.18), (2.60, 4.35), rad=-0.25)
    arrow(ax, (1.92, mid - 0.18), (2.60, 2.05), rad=0.25)
    arrow(ax, (9.15, 4.45), (10.05, mid + 0.42), rad=-0.25)
    arrow(ax, (9.15, 1.95), (10.05, mid - 0.42), rad=0.25)
    arrow(ax, (11.10, mid), (11.90, mid))
    save(fig, "figure1_pictorial_v2_lanes")

# ------------------------------------------- v3: vertical infographic ------
def build_v3():
    W, H = 7.4, 9.8
    fig, ax = canvas(W, H)
    sx = 1.55                      # spine x
    ys = [8.55, 6.85, 5.15, 3.45, 1.75]
    ax.plot([sx, sx], [ys[-1], ys[0]], color="#cfd8dc", lw=3.5, zorder=1,
            solid_capstyle="round")

    def num(i, y):
        ax.text(0.62, y, f"0{i}", fontsize=20, fontweight="bold",
                color="#dde4e9", ha="center", va="center", zorder=2)

    def step_txt(y, key, tx=2.65):
        t, s = STEPS[key]
        ax.text(tx, y + 0.16, t, fontsize=13, fontweight="bold", color=INK,
                ha="left", va="center", zorder=6)
        ax.text(tx, y - 0.20, s, fontsize=9.4, color=MUTED, ha="left",
                va="center", zorder=6)

    num(1, ys[0])
    badge(ax, sx, ys[0], 0.52, NEUT, NEUT_TINT)
    icon_docs(ax, sx, ys[0], 0.54, NEUT)
    step_txt(ys[0], "transcripts")

    num(2, ys[1])
    badge(ax, sx, ys[1], 0.52, BLUE, BLUE_TINT)
    icon_people(ax, sx, ys[1], 0.52, BLUE)
    badge(ax, sx + 1.28, ys[1], 0.52, YELLOW_DARK, YELLOW_TINT)
    icon_sparkle(ax, sx + 1.28, ys[1], 0.52, YELLOW_DARK)
    t1, _ = STEPS["expert"]
    ax.text(3.55, ys[1] + 0.16, "Expert + LLM Coding", fontsize=13,
            fontweight="bold", color=INK, ha="left", va="center")
    ax.text(3.55, ys[1] - 0.20, "two independent coders of every interview",
            fontsize=9.4, color=MUTED, ha="left", va="center")

    num(3, ys[2])
    badge(ax, sx, ys[2], 0.52, NEUT, NEUT_TINT)
    icon_network(ax, sx, ys[2], 0.54, NEUT)
    step_txt(ys[2], "networks")

    num(4, ys[3])
    badge(ax, sx, ys[3], 0.52, NEUT, NEUT_TINT)
    icon_quadrant(ax, sx, ys[3], 0.52, NEUT)
    step_txt(ys[3], "analysis")

    num(5, ys[4])
    badge(ax, sx, ys[4], 0.52, NEUT, "white")
    icon_compare(ax, sx, ys[4], 0.54)
    step_txt(ys[4], "compare")

    for y0, y1 in zip(ys[:-1], ys[1:]):
        arrow(ax, (sx, y0 - 0.56), (sx, y1 + 0.56), lw=1.6, ms=12)
    save(fig, "figure1_pictorial_v3_vertical")

# --------------------------------------------------- v4: chevron band ------
def build_v4():
    W, H = 13.8, 4.6
    fig, ax = canvas(W, H)
    ramp = ["#7FA8CD", "#5589BC", "#3B77B5", "#2166AC", "#12508D"]
    cy, h, tip = 2.85, 1.55, 0.42
    w = 2.42
    x0s = [0.5 + i * (w + 0.10) for i in range(5)]

    keys = ["transcripts", "coding", "networks", "analysis", "compare"]
    for i, (x0, color) in enumerate(zip(x0s, ramp)):
        pts = [(x0, cy + h / 2), (x0 + w, cy + h / 2), (x0 + w + tip, cy),
               (x0 + w, cy - h / 2), (x0, cy - h / 2), (x0 + tip, cy)]
        ax.add_patch(Polygon(pts, facecolor=color, edgecolor="white",
                             linewidth=1.6, zorder=2))
        cx = x0 + (w + tip) / 2 + 0.05
        if keys[i] == "coding":
            icon_people(ax, cx - 0.52, cy, 0.44, "white")
            icon_sparkle(ax, cx + 0.50, cy, 0.44, "white")
        elif keys[i] == "transcripts":
            icon_docs(ax, cx, cy, 0.52, "white", page=color)
        elif keys[i] == "networks":
            icon_network(ax, cx, cy, 0.54, "white")
        elif keys[i] == "analysis":
            # white-line quadrant, transparent fill so the chevron shows
            wq = 0.60
            ax.plot([cx, cx], [cy - wq * 0.47, cy + wq * 0.47], color="white",
                    lw=1.2, ls=(0, (2, 2)), zorder=5)
            ax.plot([cx - wq * 0.47, cx + wq * 0.47], [cy, cy], color="white",
                    lw=1.2, ls=(0, (2, 2)), zorder=5)
            ax.add_patch(FancyBboxPatch(
                (cx - wq * 0.56, cy - wq * 0.56), wq * 1.12, wq * 1.12,
                boxstyle=f"round,pad=0,rounding_size={0.07}",
                facecolor="none", edgecolor="white", linewidth=1.6,
                zorder=5))
            ax.add_patch(Circle((cx - 0.14, cy + 0.15), 0.06,
                                facecolor="white", zorder=6))
            ax.add_patch(Circle((cx + 0.14, cy - 0.13), 0.045,
                                facecolor="white", alpha=0.65, zorder=6))
        elif keys[i] == "compare":
            ax.add_patch(Circle((cx - 0.13, cy), 0.26, facecolor="none",
                                edgecolor="white", linewidth=1.9, zorder=5))
            ax.add_patch(Circle((cx + 0.13, cy), 0.26, facecolor="none",
                                edgecolor="white", linewidth=1.9, zorder=5))

        tx = cx
        if keys[i] == "coding":
            ax.text(tx - 0.10, 1.55, "Expert", fontsize=11.5,
                    fontweight="bold", color=BLUE, ha="right", va="center")
            ax.text(tx, 1.55, "+", fontsize=11.5, color=MUTED, ha="center",
                    va="center")
            ax.text(tx + 0.12, 1.55, "LLM", fontsize=11.5,
                    fontweight="bold", color=YELLOW_DARK, ha="left",
                    va="center")
            ax.text(tx, 1.55 - 0.34, "Coding", fontsize=11.5,
                    fontweight="bold", color=INK, ha="center", va="center")
            ax.text(tx, 1.55 - 0.66, "two independent coders", fontsize=8.6,
                    color=MUTED, ha="center", va="center")
        else:
            t, s = STEPS[keys[i]]
            ax.text(tx, 1.55, t, fontsize=11.5, fontweight="bold",
                    color=INK, ha="center", va="center")
            ax.text(tx, 1.55 - 0.34, s, fontsize=8.6, color=MUTED,
                    ha="center", va="center", wrap=True)
    save(fig, "figure1_pictorial_v4_chevrons")

# ------------------------------------------------ v5: cards on S-path ------
def build_v5():
    W, H = 12.8, 7.4
    fig, ax = canvas(W, H)
    cw, chh = 3.30, 2.65

    def card(cx, cy, n):
        ax.add_patch(FancyBboxPatch(
            (cx - cw / 2 + 0.05, cy - chh / 2 - 0.05), cw, chh,
            boxstyle="round,pad=0,rounding_size=0.16",
            facecolor="#e8ecef", edgecolor="none", zorder=1))
        ax.add_patch(FancyBboxPatch(
            (cx - cw / 2, cy - chh / 2), cw, chh,
            boxstyle="round,pad=0,rounding_size=0.16",
            facecolor="white", edgecolor="#d5dbe0", linewidth=1.2,
            zorder=2))
        ax.text(cx + cw / 2 - 0.30, cy + chh / 2 - 0.38, str(n),
                fontsize=24, fontweight="bold", color="#e2e8ed",
                ha="center", va="center", zorder=3)

    top_y, bot_y = 5.35, 1.95
    pos = {1: (2.25, top_y), 2: (6.40, top_y), 3: (10.55, top_y),
           4: (8.45, bot_y), 5: (4.30, bot_y)}

    # 1 transcripts
    cx, cy = pos[1]
    card(cx, cy, 1)
    badge(ax, cx, cy + 0.42, 0.44, NEUT, NEUT_TINT, lw=1.8)
    icon_docs(ax, cx, cy + 0.42, 0.46, NEUT)
    title_sub(ax, cx, cy - 0.52, "transcripts", ts=10.8, ss=8.4, gap=0.28)

    # 2 coding (split: expert | LLM)
    cx, cy = pos[2]
    card(cx, cy, 2)
    badge(ax, cx - 0.62, cy + 0.42, 0.42, BLUE, BLUE_TINT, lw=1.8)
    icon_people(ax, cx - 0.62, cy + 0.42, 0.42, BLUE)
    badge(ax, cx + 0.62, cy + 0.42, 0.42, YELLOW_DARK, YELLOW_TINT, lw=1.8)
    icon_sparkle(ax, cx + 0.62, cy + 0.42, 0.42, YELLOW_DARK)
    ax.text(cx, cy - 0.52, "Expert + LLM Coding", fontsize=10.8,
            fontweight="bold", color=INK, ha="center", va="center",
            zorder=6)
    ax.text(cx, cy - 0.80, "two independent coders", fontsize=8.4,
            color=MUTED, ha="center", va="center", zorder=6)

    # 3 networks
    cx, cy = pos[3]
    card(cx, cy, 3)
    badge(ax, cx, cy + 0.42, 0.44, NEUT, NEUT_TINT, lw=1.8)
    icon_network(ax, cx, cy + 0.42, 0.46, NEUT)
    title_sub(ax, cx, cy - 0.52, "networks", ts=10.8, ss=8.4, gap=0.28)

    # 4 analysis
    cx, cy = pos[4]
    card(cx, cy, 4)
    badge(ax, cx, cy + 0.42, 0.44, NEUT, NEUT_TINT, lw=1.8)
    icon_quadrant(ax, cx, cy + 0.42, 0.44, NEUT)
    title_sub(ax, cx, cy - 0.52, "analysis", ts=10.8, ss=8.4, gap=0.28)

    # 5 compare
    cx, cy = pos[5]
    card(cx, cy, 5)
    badge(ax, cx, cy + 0.42, 0.44, NEUT, "white", lw=1.8)
    icon_compare(ax, cx, cy + 0.42, 0.46)
    title_sub(ax, cx, cy - 0.52, "compare", ts=10.8, ss=8.4, gap=0.28)

    arrow(ax, (pos[1][0] + cw / 2 + 0.06, top_y),
          (pos[2][0] - cw / 2 - 0.06, top_y))
    arrow(ax, (pos[2][0] + cw / 2 + 0.06, top_y),
          (pos[3][0] - cw / 2 - 0.06, top_y))
    arrow(ax, (pos[3][0], top_y - chh / 2 - 0.08),
          (pos[4][0] + 0.9, bot_y + chh / 2 + 0.08), rad=-0.28)
    arrow(ax, (pos[4][0] - cw / 2 - 0.06, bot_y),
          (pos[5][0] + cw / 2 + 0.06, bot_y))
    save(fig, "figure1_pictorial_v5_cards")

# ------------------------- v2 FINAL: Jeff's pick, tightened ----------------
def build_v2_final():
    """Jeff chose v2 (2026-08-21). Final version keeps the original
    horizontal-lane composition and compresses the dead width (per
    Charles, 2026-08-22): in-lane arrows shortened to match the
    Structural Analysis -> Benchmark Comparison arrow, lane boxes
    narrowed, and the padding left of Coding / right of Network
    tightened. The narrower canvas means everything renders larger
    once the figure is placed at page width; fonts also get a ~10%
    bump on top."""
    W, H = 10.5, 5.2
    fig, ax = canvas(W, H)
    # content spans y ~1.5..5.5; crop half the dead band off top and bottom
    ax.set_ylim(0.75, 5.95)
    mid = 3.2
    F = 1.3   # font bump vs. the menu version of v2

    badge(ax, 1.25, mid, 0.62, NEUT, NEUT_TINT)
    icon_docs(ax, 1.25, mid, 0.64, NEUT)
    title_sub(ax, 1.25, 2.05, "transcripts", ts=11 * F, ss=8.6 * F,
              gap=0.34)

    bx0, cxc, cxn = 2.65, 3.43, 5.38   # lane box left, coding x, network x
    bx1 = cxn + 0.78                   # lane box right
    lanes = [(BLUE, BLUE_TINT, 4.55, "EXPERT  ·  human benchmark",
              icon_people),
             (YELLOW_DARK, YELLOW_TINT, 1.85, "LLM  ·  Claude",
              icon_sparkle)]
    for color, tint, cy, label, coder_icon in lanes:
        ax.add_patch(FancyBboxPatch(
            (bx0, cy - 0.92), bx1 - bx0, 1.84,
            boxstyle="round,pad=0,rounding_size=0.18",
            facecolor=tint, edgecolor=color, linewidth=1.4, alpha=0.9,
            zorder=2))
        ax.text(bx0 + 0.30, cy + 0.68, label, fontsize=8.6 * F,
                fontweight="bold", color=color, ha="left", va="center",
                zorder=6)
        badge(ax, cxc, cy - 0.10, 0.44, color, "white", lw=1.8)
        coder_icon(ax, cxc, cy - 0.10, 0.44, color)
        ax.text(cxc, cy - 0.74, "Purposive Coding", fontsize=9.2 * F,
                fontweight="bold", color=INK, ha="center", va="center",
                zorder=6)
        badge(ax, cxn, cy - 0.10, 0.44, color, "white", lw=1.8)
        icon_network(ax, cxn, cy - 0.10, 0.46, color)
        ax.text(cxn, cy - 0.74, "Causal Network", fontsize=9.2 * F,
                fontweight="bold", color=INK, ha="center", va="center",
                zorder=6)
        arrow(ax, (cxc + 0.55, cy - 0.10), (cxn - 0.55, cy - 0.10),
              color=color, lw=1.5)

    # note sits in the gap between the two Causal Network icons
    ax.text(cxn, 3.18, "17 shared factors\nchallenge & solution",
            fontsize=8.6 * F, color=MUTED, ha="center", va="center",
            linespacing=1.35, zorder=6)

    xa, xc = bx1 + 1.30, bx1 + 3.40
    badge(ax, xa, mid, 0.60, NEUT, NEUT_TINT)
    icon_quadrant(ax, xa, mid, 0.60, NEUT)
    ax.text(xa, 2.05, STEPS["analysis"][0], fontsize=11 * F,
            fontweight="bold", color=INK, ha="center", va="center",
            zorder=6)
    ax.text(xa, 1.66, "centrality · quadrants\nfeedback loops",
            fontsize=8.6 * F, color=MUTED, ha="center", va="center",
            linespacing=1.35, zorder=6)

    badge(ax, xc, mid, 0.60, NEUT, "white")
    icon_compare(ax, xc, mid, 0.62)
    title_sub(ax, xc, 2.05, "compare", ts=11 * F, ss=8.6 * F,
              gap=0.34)

    arrow(ax, (1.92, mid + 0.18), (2.60, 4.35), rad=-0.25)
    arrow(ax, (1.92, mid - 0.18), (2.60, 2.05), rad=0.25)
    arrow(ax, (bx1 + 0.05, 4.45), (xa - 0.40, mid + 0.42), rad=-0.25)
    arrow(ax, (bx1 + 0.05, 1.95), (xa - 0.40, mid - 0.42), rad=0.25)
    arrow(ax, (xa + 0.65, mid), (xc - 0.62, mid))
    save(fig, "figure1_pictorial_v2_final")

if __name__ == "__main__":
    build_v1()
    build_v2()
    build_v3()
    build_v4()
    build_v5()
    build_v2_final()
