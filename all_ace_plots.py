#!/usr/bin/env python3
"""
Generate all ACE ternary plots from the cleaned CSV files.

Expected default input files:
    iq_ace_studies.csv
    personality_ace_studies.csv
    height_ace_studies.csv
    obesity_bmi_ace_studies.csv

Default output files:
    iq_ace.png
    personality_ace.png
    height_ace.png
    obesity_bmi_ace.png

Usage:
    python all_ace_plots.py
"""

from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

BG = "#0f1117"
SPINE = "#3a3f4b"
FG = "#c9d1d9"
MUTED = "#8b949e"
TITLE = "#e6edf3"

AGE_COLORS = {
    "child": "#38bdf8",
    "teen": "#56d364",
    "adult": "#f2cc60",
    "mixed": "#8b949e",
}
AGE_LABELS = {
    "child": "Children (0–12)",
    "teen": "Teenagers (13–17)",
    "adult": "Adults (18+)",
    "mixed": "Mixed / unspecified age",
}
FALLBACK_COLORS = [
    "#a78bfa", "#fb7185", "#22d3ee", "#f97316",
    "#84cc16", "#e879f9", "#facc15", "#60a5fa",
    "#14b8a6", "#ef4444",
]

SQRT3_2 = np.sqrt(3) / 2

DEFAULT_PLOTS = [
    {"csv": "iq_ace_studies.csv", "trait": "IQ", "output": "iq_ace.png"},
    {"csv": "personality_ace_studies.csv", "trait": "personality traits", "output": "personality_ace.png"},
    {"csv": "height_ace_studies.csv", "trait": "height", "output": "height_ace.png"},
    {"csv": "obesity_bmi_ace_studies.csv", "trait": "obesity (BMI)", "output": "obesity_bmi_ace.png"},
]

def to_xy(a, c, e):
    return a + 0.5 * c, SQRT3_2 * c

def read_data(path: Path) -> pd.DataFrame:
    df = pd.read_csv(path)
    required = {"label", "A", "C", "E"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"{path.name} is missing required columns: {sorted(missing)}")

    for col in ("A", "C", "E"):
        df[col] = pd.to_numeric(df[col], errors="raise")

    ace = df[["A", "C", "E"]].to_numpy(float)
    if np.nanmax(ace) > 1.5:
        df[["A", "C", "E"]] = df[["A", "C", "E"]] / 100.0

    if (df[["A", "C", "E"]] < 0).any().any():
        raise ValueError(f"{path.name}: A, C, and E must be non-negative.")

    totals = df[["A", "C", "E"]].sum(axis=1)
    if (totals <= 0).any():
        raise ValueError(f"{path.name}: every row must have A + C + E > 0.")

    df[["A", "C", "E"]] = df[["A", "C", "E"]].div(totals, axis=0)

    if "N" not in df.columns:
        df["N"] = 1
    df["N"] = pd.to_numeric(df["N"], errors="coerce").fillna(1).clip(lower=1)

    if "age_band" not in df.columns:
        df["age_band"] = "mixed"
    df["age_band"] = df["age_band"].fillna("mixed").astype(str).str.strip().str.lower()

    if "group" in df.columns:
        df["group"] = df["group"].fillna("").astype(str)

    return df

def point_sizes(n, scale="log", min_size=45, max_size=230):
    n = np.asarray(n, dtype=float)
    if scale == "none" or len(n) == 1:
        return np.full_like(n, (min_size + max_size) / 2)
    if scale == "log":
        x = np.log10(np.maximum(n, 1))
    elif scale == "sqrt":
        x = np.sqrt(np.maximum(n, 1))
    else:
        x = n
    lo, hi = np.nanmin(x), np.nanmax(x)
    if hi <= lo:
        return np.full_like(n, (min_size + max_size) / 2)
    return min_size + (max_size - min_size) * (x - lo) / (hi - lo)

def build_group_colors(groups):
    if all(g in AGE_COLORS for g in groups):
        colors = dict(AGE_COLORS)
    else:
        colors = {}
    extras = [g for g in groups if g not in colors]
    for i, g in enumerate(extras):
        colors[g] = FALLBACK_COLORS[i % len(FALLBACK_COLORS)]
    return colors

def draw_triangle(ax, left_label, right_label, top_label):
    verts = [(0, 0), (1, 0), (0.5, SQRT3_2), (0, 0)]
    xs, ys = zip(*verts)
    ax.plot(xs, ys, color=SPINE, linewidth=1.4, zorder=2)

    for frac in (0.2, 0.4, 0.6, 0.8):
        p1, p2 = to_xy(frac, 1 - frac, 0), to_xy(frac, 0, 1 - frac)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=SPINE, lw=.6, ls="--", zorder=1)
        p1, p2 = to_xy(1 - frac, frac, 0), to_xy(0, frac, 1 - frac)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=SPINE, lw=.6, ls="--", zorder=1)
        p1, p2 = to_xy(1 - frac, 0, frac), to_xy(0, 1 - frac, frac)
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=SPINE, lw=.6, ls=":", zorder=1)

        tx, ty = to_xy(frac, 1 - frac, 0)
        ax.text(tx, ty - .028, str(int(frac * 100)), ha="center", va="top",
                fontsize=7.5, color=MUTED, zorder=3)

    ax.text(0.0, -.055, left_label, ha="center", va="top",
            fontsize=11.5, fontweight="bold", color="#38bdf8")
    ax.text(1.0, -.055, right_label, ha="center", va="top",
            fontsize=11.5, fontweight="bold", color="#f2cc60")
    ax.text(.5, SQRT3_2 + .055, top_label, ha="center", va="bottom",
            fontsize=11.5, fontweight="bold", color=FG)

def make_plot(csv_path: Path, output_path: Path, trait: str,
              footer: str = "antisymmetry.substack.com",
              size_scale: str = "log",
              title: str | None = None):
    df = read_data(csv_path)
    title = title or f"ACE variance components of {trait}"

    fig, ax = plt.subplots(figsize=(12.4, 10.2))
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    ax.set_aspect("equal")
    ax.axis("off")

    draw_triangle(
        ax,
        left_label="non-shared\nenvironment",
        right_label="genetic",
        top_label="shared\nenvironment",
    )

    xy = np.array([to_xy(r.A, r.C, r.E) for r in df.itertuples()])
    sizes = point_sizes(df["N"], scale=size_scale)

    group_col = "group" if "group" in df.columns else "age_band"
    groups = list(dict.fromkeys(df[group_col].fillna("mixed").astype(str).tolist()))
    if group_col == "age_band":
        preferred = [g for g in ("child", "teen", "adult", "mixed") if g in groups]
        groups = preferred + [g for g in groups if g not in preferred]

    colors = build_group_colors(groups)

    for grp in groups:
        mask = df[group_col].eq(grp).to_numpy()
        edge = "#d0d7de" if grp != "mixed" else SPINE
        ax.scatter(
            xy[mask, 0], xy[mask, 1],
            s=sizes[mask], color=colors[grp], alpha=.80,
            edgecolors=edge, linewidths=.9, zorder=4
        )

    handles = []
    for grp in groups:
        if group_col == "age_band":
            label = AGE_LABELS.get(grp, grp.replace("_", " ").title())
        else:
            label = grp
        edge = "#d0d7de" if grp != "mixed" else SPINE
        handles.append(
            Line2D([0], [0], marker="o", color="none",
                   markerfacecolor=colors[grp], markeredgecolor=edge,
                   markersize=11, alpha=.95, label=label)
        )

    ax.legend(
        handles=handles,
        facecolor="#1c2128",
        edgecolor=SPINE,
        labelcolor=FG,
        fontsize=10.2,
        framealpha=.92,
        loc="upper left",
        bbox_to_anchor=(.02, .90),
        ncol=1,
    )

    fig.suptitle(title, color=TITLE, fontsize=14, fontweight="bold", y=.975)

    if footer:
        fig.text(.99, .01, footer, ha="right", va="bottom",
                 fontsize=10.5, color=TITLE)

    ax.set_xlim(-.18, 1.18)
    ax.set_ylim(-.14, SQRT3_2 + .05)
    fig.tight_layout(rect=[0.01, 0.01, 0.99, .97])

    fig.savefig(output_path, dpi=180, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)

def main():
    parser = argparse.ArgumentParser(description="Generate all ACE ternary plots from the cleaned CSV files.")
    parser.add_argument("--base-dir", type=Path, default=Path("."),
                        help="Directory containing the CSV files and where outputs should be written.")
    parser.add_argument("--size-scale", choices=["log", "sqrt", "linear", "none"], default="log",
                        help="Point-size scaling for N.")
    args = parser.parse_args()

    base = args.base_dir
    generated = []
    missing = []

    for spec in DEFAULT_PLOTS:
        csv_path = base / spec["csv"]
        output_path = base / spec["output"]
        if not csv_path.exists():
            missing.append(csv_path)
            continue

        make_plot(
            csv_path=csv_path,
            output_path=output_path,
            trait=spec["trait"],
            footer="antisymmetry.substack.com",
            size_scale=args.size_scale,
            title=f"ACE variance components of {spec['trait']}",
        )
        generated.append(output_path)

    print("Generated files:")
    for path in generated:
        print(f"  {path}")

    if missing:
        print("\nMissing CSV files:")
        for path in missing:
            print(f"  {path}")

if __name__ == "__main__":
    main()
