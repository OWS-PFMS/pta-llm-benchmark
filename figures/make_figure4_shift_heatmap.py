#!/usr/bin/env python3
"""Figure 4 - factor-level displacement between expert and LLM codings.

A 17 x 4 diverging heatmap of the *signed* shift in normalized influence and
dependence, LLM minus expert, for both systems. Each cell is one component of
the displacement arrows drawn in Figure 3: positive (yellow) means the LLM
scored the factor higher, negative (blue) means the expert coding did, and
near-zero (neutral gray) means the two codings agree on that coordinate.

Poles reuse the Figure 3 series colors so the encoding is inherited rather
than re-learned - blue is the expert coding in both figures, yellow the LLM.
The pair validates at CVD dE 32.8 / normal dE 38.9 on a white surface; every
cell also carries its printed value, which is the required relief for the
yellow pole's sub-3:1 contrast against white.

Rows are ordered by total displacement (the sum of the two panels' arrow
lengths in Figure 3), so the factors the two coders disagree about most sit
at the top.

Data: analysis/centrality_{nj,claude}_{challenge,solution}.csv
"""
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from matplotlib.colors import LinearSegmentedColormap, to_rgb
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "analysis"
OUT = Path(__file__).resolve().parent

BLUE = "#2166AC"     # expert scored higher
YELLOW = "#E8A50C"   # LLM scored higher
NEUTRAL = "#F0EFEC"  # agreement
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
})


# --- Lab-interpolated diverging ramp ---------------------------------------
# Straight RGB interpolation between two saturated poles muddies the midtones;
# stepping through CIELab keeps each arm perceptually even.
def _srgb_to_lab(rgb):
    r = np.where(rgb <= 0.04045, rgb / 12.92, ((rgb + 0.055) / 1.055) ** 2.4)
    m = np.array([[0.4124, 0.3576, 0.1805],
                  [0.2126, 0.7152, 0.0722],
                  [0.0193, 0.1192, 0.9505]])
    xyz = m @ r / np.array([0.95047, 1.0, 1.08883])
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.array([116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])])


def _lab_to_srgb(lab):
    fy = (lab[0] + 16) / 116
    f = np.array([fy + lab[1] / 500, fy, fy - lab[2] / 200])
    xyz = np.where(f ** 3 > 0.008856, f ** 3, (f - 16 / 116) / 7.787)
    xyz = xyz * np.array([0.95047, 1.0, 1.08883])
    m = np.array([[3.2406, -1.5372, -0.4986],
                  [-0.9689, 1.8758, 0.0415],
                  [0.0557, -0.2040, 1.0570]])
    lin = m @ xyz
    srgb = np.where(lin <= 0.0031308, 12.92 * lin,
                    1.055 * np.abs(lin) ** (1 / 2.4) - 0.055)
    return np.clip(srgb, 0, 1)


def diverging_cmap(lo, mid, hi, n=256):
    labs = [_srgb_to_lab(np.array(to_rgb(c))) for c in (lo, mid, hi)]
    half = n // 2
    stops = ([_lab_to_srgb(labs[0] + (labs[1] - labs[0]) * t)
              for t in np.linspace(0, 1, half, endpoint=False)]
             + [_lab_to_srgb(labs[1] + (labs[2] - labs[1]) * t)
                for t in np.linspace(0, 1, n - half)])
    return LinearSegmentedColormap.from_list("expert_llm", stops)


CMAP = diverging_cmap(BLUE, NEUTRAL, YELLOW)


def shifts():
    """Signed LLM-minus-expert shift on each Figure 3 axis, per system."""
    out = {}
    for system in ("challenge", "solution"):
        nj = pd.read_csv(DATA / f"centrality_nj_{system}.csv").set_index("bin")
        cl = pd.read_csv(DATA / f"centrality_claude_{system}.csv").set_index("bin")
        for f in nj.index:
            r = out.setdefault(f, {})
            r[f"{system}_influence"] = cl.loc[f, "influence"] - nj.loc[f, "influence"]
            r[f"{system}_dependence"] = cl.loc[f, "dependence"] - nj.loc[f, "dependence"]
            r[f"{system}_flip"] = nj.loc[f, "quadrant"] != cl.loc[f, "quadrant"]
    df = pd.DataFrame(out).T
    num = [c for c in df.columns if not c.endswith("_flip")]
    df[num] = df[num].astype(float)
    # Displacement = Figure 3 arrow length, one per panel; their sum orders rows.
    for s in ("challenge", "solution"):
        df[f"{s}_disp"] = np.hypot(df[f"{s}_influence"], df[f"{s}_dependence"])
    df["total_disp"] = df["challenge_disp"] + df["solution_disp"]
    return df.sort_values("total_disp", ascending=False)


COLS = [("challenge_influence", "Influence"),
        ("challenge_dependence", "Dependence"),
        ("solution_influence", "Influence"),
        ("solution_dependence", "Dependence")]


def build(df, k=1.0, stem="figure4_shift_heatmap"):
    n = len(df)
    vmax = 0.55                      # symmetric; covers the largest |shift| (0.52)
    gap = 0.34                       # separates the two system blocks
    xs = [0.0, 1.0, 2.0 + gap, 3.0 + gap]
    right = xs[-1] + 1.0

    fig, ax = plt.subplots(figsize=(7.1, 7.6))
    ax.set_xlim(-2.45, right + 1.35)
    ax.set_ylim(-1.75, n + 1.45)
    ax.axis("off")

    halo_w = 0.04                    # surface gap between cells
    for row, (factor, r) in enumerate(df.iterrows()):
        y = n - 1 - row
        name = SHORT.get(factor, factor)
        ax.text(-0.22, y + 0.5, name, ha="right", va="center",
                fontsize=8.6 * k, color=INK)
        for (key, _), x in zip(COLS, xs):
            v = r[key]
            rgba = CMAP((v + vmax) / (2 * vmax))
            ax.add_patch(Rectangle((x + halo_w, y + halo_w),
                                   1 - 2 * halo_w, 1 - 2 * halo_w,
                                   facecolor=rgba, edgecolor="none"))
            # Printed value doubles as the table view and as the contrast
            # relief the yellow pole requires; ink flips on dark blue only.
            lum = 0.2126 * rgba[0] + 0.7152 * rgba[1] + 0.0722 * rgba[2]
            # |shift| < 0.005 rounds to zero; print it unsigned rather
            # than as a spurious "-0.00".
            txt = ("0.00" if abs(v) < 0.005
                   else f"{v:+.2f}".replace("-", "−"))
            ax.text(x + 0.5, y + 0.5, txt,
                    ha="center", va="center", fontsize=7.9 * k,
                    color="white" if lum < 0.42 else INK)
        ax.text(right + 0.62, y + 0.5, f"{r['total_disp']:.2f}",
                ha="center", va="center", fontsize=8.2 * k, color=MUTED)

    # Column headers, grouped by system.
    for (_, sub), x in zip(COLS, xs):
        ax.text(x + 0.5, n + 0.18, sub, ha="center", va="bottom",
                fontsize=8.4 * k, color=INK)
    for label, (a, b) in (("Challenge system", (xs[0], xs[1] + 1)),
                          ("Solution system", (xs[2], xs[3] + 1))):
        ax.text((a + b) / 2, n + 0.92, label, ha="center", va="bottom",
                fontsize=9.6 * k, color=INK, fontweight="bold")
        ax.plot([a + halo_w, b - halo_w], [n + 0.82] * 2, color=FAINT, lw=0.9)
    ax.text(right + 0.62, n + 0.18, "Total\ndisplacement", ha="center",
            va="bottom", fontsize=7.6 * k, color=MUTED, linespacing=1.25)

    # Colorbar: a strip of the ramp, poles named in words rather than signs.
    cy, ch = -1.12, 0.3
    grad = np.linspace(-vmax, vmax, 256)
    cx0, cx1 = xs[0], xs[3] + 1
    ax.imshow(grad.reshape(1, -1), cmap=CMAP, vmin=-vmax, vmax=vmax,
              extent=(cx0, cx1, cy, cy + ch), aspect="auto", zorder=2)
    ax.add_patch(Rectangle((cx0, cy), cx1 - cx0, ch, fill=False,
                           edgecolor=FAINT, lw=0.8, zorder=3))
    for frac, txt in ((0.0, f"−{vmax:.2f}"), (0.5, "0"), (1.0, f"+{vmax:.2f}")):
        ax.text(cx0 + frac * (cx1 - cx0), cy - 0.14, txt, ha="center",
                va="top", fontsize=7.6 * k, color=MUTED)
    ax.text(cx0, cy - 0.66, r"$\leftarrow$  Expert coders scored higher", ha="left",
            va="top", fontsize=8.2 * k, color=BLUE)
    ax.text(cx1, cy - 0.66, r"LLM scored higher  $\rightarrow$", ha="right",
            va="top", fontsize=8.2 * k, color="#8a6207")
    ax.text((cx0 + cx1) / 2, cy + ch + 0.12, "agreement", ha="center",
            va="bottom", fontsize=8.2 * k, color=MUTED, style="italic")

    fig.tight_layout()
    fig.savefig(OUT / f"{stem}.png", dpi=300, bbox_inches="tight")
    fig.savefig(OUT / f"{stem}.pdf", bbox_inches="tight")
    print("wrote", OUT / f"{stem}.png")


if __name__ == "__main__":
    build(shifts())
