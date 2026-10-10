#!/usr/bin/env python3
from pathlib import Path
import math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Polygon

BG = "#0f1117"
SPINE = "#3a3f4b"
FG = "#c9d1d9"
MUTED = "#8b949e"
TITLE = "#e6edf3"

LEFT_COLOR = "#38bdf8"
RIGHT_COLOR = "#f2cc60"
FILL_COLOR = "#60a5fa"

SQRT3_2 = math.sqrt(3) / 2

def ternary_to_xy(a, c, e):
    return a + 0.5 * c, SQRT3_2 * c

def style_axis(ax):
    ax.set_facecolor(BG)
    ax.tick_params(colors=MUTED, labelsize=9)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["bottom"].set_color(SPINE)
    ax.spines["left"].set_color(SPINE)
    ax.spines["bottom"].set_linewidth(1.1)
    ax.spines["left"].set_linewidth(1.1)

def draw_left_construction(ax):
    style_axis(ax)
    ax.set_xlim(-0.12, 1.32)
    ax.set_ylim(-0.08, 1.18)
    ax.set_aspect("equal")

    E = (0.0, 0.0)
    A = (1.0, 0.5)
    C = (1.0, 1.0)

    poly = Polygon([E, A, C], closed=True,
                   facecolor=FILL_COLOR, edgecolor="#60a5fa",
                   alpha=0.35, lw=2.0)
    ax.add_patch(poly)
    ax.plot([E[0], A[0], C[0], E[0]],
            [E[1], A[1], C[1], E[1]],
            color="#60a5fa", lw=2.0)

    for (x, y), label, dx, dy in [
        (E, "E", -0.08, 0.06),
        (A, "A",  0.08, 0.06),
        (C, "C", -0.04, 0.10),
    ]:
        ax.scatter([x], [y], s=180, color="#60a5fa",
                   alpha=0.35, edgecolors="none", zorder=4, clip_on=False)
        ax.scatter([x], [y], s=45, color="#60a5fa",
                   edgecolors="#60a5fa", zorder=5, clip_on=False)
        ax.text(x + dx, y + dy, label, color="#60a5fa",
                fontsize=16, zorder=6)

    ax.set_xticks([0, 1])
    ax.set_yticks([0, 1])
    ax.set_xlabel("rMZ", color=MUTED, fontsize=11, labelpad=10)
    ax.set_ylabel("rDZ", color=MUTED, fontsize=11, labelpad=10)
    ax.grid(color=SPINE, alpha=0.35, lw=0.7)

    # Arrowheads for a more typical graph appearance
    ax.annotate("", xy=(1.29, 0), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=SPINE, lw=1.1),
                annotation_clip=False, zorder=3)
    ax.annotate("", xy=(0, 1.15), xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=SPINE, lw=1.1),
                annotation_clip=False, zorder=3)

def draw_center_arrow(ax):
    ax.set_facecolor(BG)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    arrow = FancyArrowPatch((0.12, 0.5), (0.88, 0.5),
                            arrowstyle="simple", mutation_scale=32,
                            lw=0, color=FG, alpha=0.95)
    ax.add_patch(arrow)

def draw_right_ace(ax):
    ax.set_facecolor(BG)
    ax.set_aspect("equal")
    ax.axis("off")

    E = (0.0, 0.0)
    A = (1.0, 0.0)
    C = (0.5, SQRT3_2)

    ax.plot([E[0], A[0], C[0], E[0]],
            [E[1], A[1], C[1], E[1]],
            color=SPINE, linewidth=1.4, zorder=2)

    for frac in (0.2, 0.4, 0.6, 0.8):
        p1, p2 = ternary_to_xy(frac, 1 - frac, 0), ternary_to_xy(frac, 0, 1 - frac)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=SPINE, lw=.6, ls="--", zorder=1)
        p1, p2 = ternary_to_xy(1 - frac, frac, 0), ternary_to_xy(0, frac, 1 - frac)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=SPINE, lw=.6, ls="--", zorder=1)
        p1, p2 = ternary_to_xy(1 - frac, 0, frac), ternary_to_xy(0, 1 - frac, frac)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=SPINE, lw=.6, ls=":", zorder=1)

        tx, ty = ternary_to_xy(frac, 1 - frac, 0)
        ax.text(tx, ty - .028, str(int(frac * 100)),
                ha="center", va="top", fontsize=7.5, color=MUTED, zorder=3)

    poly = Polygon([E, A, C], closed=True,
                   facecolor=FILL_COLOR, edgecolor="none", alpha=0.10, zorder=0)
    ax.add_patch(poly)

    # Vertex markers
    for (x, y), color in [
        (E, LEFT_COLOR),
        (A, RIGHT_COLOR),
        (C, FG),
    ]:
        ax.scatter([x], [y], s=55, color=color, edgecolors="#d0d7de",
                   linewidths=.6, zorder=5)

    # Put E and A just outside their lower vertex tips, matching the data-plot convention.
    ax.text(E[0] - 0.030, E[1] - 0.018, "E",
            ha="right", va="top", fontsize=14, color=LEFT_COLOR,
            fontweight="bold", zorder=6)
    ax.text(A[0] + 0.030, A[1] - 0.018, "A",
            ha="left", va="top", fontsize=14, color=RIGHT_COLOR,
            fontweight="bold", zorder=6)
    ax.text(C[0], C[1] + 0.045, "C",
            ha="center", va="bottom", fontsize=14, color=FG,
            fontweight="bold", zorder=6)


    ax.set_xlim(-.10, 1.10)
    ax.set_ylim(-.08, SQRT3_2 + .10)

def make_plot(output_path):
    # Symmetric canvas and panel geometry:
    # equal-width left/right panels, narrow centered arrow panel.
    fig = plt.figure(figsize=(14, 6.4), facecolor=BG)
    gs = fig.add_gridspec(
        1, 3,
        width_ratios=[1.0, 0.20, 1.0],
        left=0.055, right=0.945,
        bottom=0.10, top=0.87,
        wspace=0.055
    )

    ax_left = fig.add_subplot(gs[0, 0])
    ax_mid = fig.add_subplot(gs[0, 1])
    ax_right = fig.add_subplot(gs[0, 2])

    draw_left_construction(ax_left)
    draw_center_arrow(ax_mid)
    draw_right_ace(ax_right)

    # Center the title on the full figure.
    fig.suptitle(
        "How the ACE triangle is formed",
        x=0.5, y=0.955,
        ha="center", va="center",
        color=TITLE, fontsize=16, fontweight="bold"
    )

    fig.text(.985, .025, "antisymmetry.substack.com",
             ha="right", va="bottom", fontsize=11, color=TITLE)

    fig.savefig(
        output_path,
        dpi=180,
        facecolor=fig.get_facecolor()
    )
    plt.close(fig)

if __name__ == "__main__":
    make_plot(Path("ace_triangle_construction.png"))
