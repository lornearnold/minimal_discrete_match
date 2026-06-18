"""Render Figures 1–6 from minimal_packing.qmd into assets/figures at 600 DPI.

This script extracts the figure-producing chunks from the manuscript and runs
them in order, saving each output as a high-resolution PNG. It's intended to
be re-run whenever the manuscript figures change.

Usage (from repo root):
    uv run python minimal_packing_poster/scripts/render_figures.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Make the package importable when running this script from anywhere.
REPO_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "src"))


import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
import seaborn as sns  # noqa: E402

from gsd_lib import GSD, MinimalPackingGenerator  # noqa: E402

OUT_DIR = REPO_ROOT / "minimal_packing_poster" / "assets" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# -----------------------------------------------------------------------------
# rcParams — copied from the qmd setup chunk
# -----------------------------------------------------------------------------
plt.rcParams.update(
    {
        "figure.figsize": (5, 4),
        "figure.dpi": 400,
        "savefig.dpi": 600,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.1,
        "font.size": 12,
        "text.usetex": True,
        "font.family": "serif",
        "font.sans-serif": ["cmss10", "Arial"],
        "axes.formatter.use_mathtext": True,
        "axes.titlesize": 14,
        "axes.labelsize": 12,
        "xtick.labelsize": 10,
        "ytick.labelsize": 10,
        "legend.fontsize": 10,
        "axes.linewidth": 1.0,
        "axes.spines.top": True,
        "axes.spines.right": True,
        "axes.grid": True,
        "grid.alpha": 0.3,
        "grid.linewidth": 0.5,
        "lines.linewidth": 1.5,
        "lines.markersize": 6,
        "scatter.marker": "o",
        "legend.frameon": True,
        "legend.framealpha": 0.8,
        "legend.fancybox": True,
        "legend.numpoints": 1,
        "xtick.direction": "in",
        "ytick.direction": "in",
        "xtick.major.size": 4,
        "ytick.major.size": 4,
        "xtick.minor.size": 2,
        "ytick.minor.size": 2,
    }
)


def save(fig: plt.Figure, name: str) -> None:
    out = OUT_DIR / name
    fig.savefig(out, dpi=600)
    print(f"  wrote {out.relative_to(REPO_ROOT)}")


# -----------------------------------------------------------------------------
# Shared setup (sieve set, mass_dist, small GSD batch)
# -----------------------------------------------------------------------------
x1 = np.array(
    [
        0.0001,  # Pan
        0.075,
        0.15,
        0.3,
        0.6,
        1.18,
        2.36,
        4.75,
        9.5,
        19,
        25,
        37.5,
        50,
        63,
        75,
    ]
)
sieve_sizes = x1.copy()


def mass_dist(n_sieves, rng=None, exponent=4.0, extra_randomness=0):
    if rng is None:
        rng = np.random.default_rng()
    base_dist = np.ones(n_sieves) + rng.random(n_sieves)
    lower = 1 + n_sieves // 4
    upper = 1 + 3 * n_sieves // 4
    center_idx = rng.integers(lower, upper)
    distances = np.abs(np.arange(n_sieves) - center_idx) / center_idx
    scale_factor = np.exp(-exponent * distances)
    dist = base_dist * scale_factor
    for _ in range(extra_randomness):
        dist *= 1 + rng.random(n_sieves)
    return dist


rng = np.random.default_rng(1)
tol = 1e-2

gsd_list = []
set_size_list = []
flex_list = []

x = x1.copy()
min_span = 5
for start in range(0, len(x) - min_span):
    for end in range(start + min_span, len(x)):
        new_x = x[start:end]
        n_sieves = len(new_x)
        for j in range(10):
            mass = mass_dist(n_sieves, rng, exponent=2, extra_randomness=7)
            mass[-1] = 0.0
            g = GSD(sizes=new_x, masses=mass)
            mps_f = MinimalPackingGenerator(
                g, x_n_factor=0.5, tol=tol, flex=True, density=1.0
            )
            mps_s = MinimalPackingGenerator(
                g, x_n_factor=0.5, tol=tol, flex=False, density=1.0
            )
            gsd_list.append(g)
            set_size_list.append(mps_s)
            flex_list.append(mps_f)

print(f"Built {len(gsd_list)} GSDs for small-batch figures.")


# -----------------------------------------------------------------------------
# Figure 1 — GSD subset with curvature index annotation
# -----------------------------------------------------------------------------
def make_fig1():
    fig, ax = plt.subplots()
    for gsd in gsd_list:
        ax.plot(
            gsd.sizes[1:],
            100 * gsd.percent_passing[1:],
            color="k",
            alpha=0.2,
            linewidth=0.5,
        )

    ex_i = 39
    example_gsd = gsd_list[ex_i]
    ax.plot(
        example_gsd.sizes[1:],
        100 * example_gsd.percent_passing[1:],
        color="r",
        linewidth=2,
        label="Example GSD",
    )
    ax.plot(
        [
            example_gsd.sizes[1],
            example_gsd.sizes[1],
            example_gsd.sizes[-1],
            example_gsd.sizes[-1],
        ],
        [
            100 * example_gsd.percent_passing[1],
            0.5,
            0.5,
            100 * example_gsd.percent_passing[-1],
        ],
        color="r",
        linewidth=2,
        label="Example Retained",
    )
    ax.plot(
        [
            0.075,
            example_gsd.sizes[-1],
            example_gsd.sizes[-1],
            0.075,
            0.075,
            example_gsd.sizes[-1],
        ],
        [0.5, 0.5, 100, 100 * example_gsd.percent_passing[1], 0, 0],
        color="b",
        linestyle=":",
        linewidth=2,
        label="Uniform Distribution",
    )
    ax.plot([11, 40], [52, 52], color="k", linewidth=1, zorder=4)
    left, bottom, width, height = (5.5, 40, 80, 30)
    rect = plt.Rectangle(
        (left, bottom), width, height, fill=True, color="1", alpha=0.8, zorder=3
    )
    ax.add_patch(rect)
    ax.annotate(
        r"\textbf{Curvature Index:}",
        xy=(5, 65),
        xytext=(6.5, 65),
        fontsize=11,
        color="k",
        ha="left",
        va="center",
    )
    bbox_r = dict(fc="1", ec="r", linewidth=2, alpha=1)
    ax.annotate(
        r"Area",
        xy=(5, 65),
        xytext=(20, 58),
        fontsize=11,
        bbox=bbox_r,
        color="k",
        ha="center",
        va="center",
    )
    bbox_b = dict(fc="1", ec="b", linestyle=":", linewidth=2, alpha=1)
    ax.annotate(
        r"Area",
        xy=(5, 65),
        xytext=(20, 46),
        fontsize=11,
        bbox=bbox_b,
        color="k",
        ha="center",
        va="center",
    )
    ax.set_xscale("log")
    ax.grid()
    ax.set_xlabel("Particle Size (mm)")
    ax.set_ylabel(r"Percent Passing (\%)")
    ax.set_ylim(0, 100)
    ax.set_xlim(0.055, 100)
    save(fig, "figure1_gsd_curvature_index.png")
    plt.close(fig)


# -----------------------------------------------------------------------------
# Figure 2 — Convergence (Fixed Size vs Spanned Integer)
# -----------------------------------------------------------------------------
def make_fig2():
    from matplotlib.lines import Line2D

    fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, height_ratios=[4, 1])

    nf = []
    ns = []
    for i in range(len(set_size_list)):
        s = set_size_list[i]
        xs = [n[-1] - 1 for n in s.qs]
        ns.append(xs[-1])
        ax1.plot(xs, s.error, color="r", alpha=0.5)

    for i in range(len(flex_list)):
        f = flex_list[i]
        xf = [n[-1] - 1 for n in f.qs]
        nf.append(xf[-1])
        ax1.plot(xf, f.error, color="k", alpha=0.5)
        ax2.plot(xf, f.error, color="k", alpha=0.5)
        ax2.scatter(xf, f.error, marker="o", color="k", alpha=0.5)

    ax1.plot([0, 200], [tol, tol], color="k", linestyle="--", linewidth=1)

    ax1.set_yscale("log")
    ax1.set_ylim(1e-4, 5e-1)
    ax1.set_xlim(0, 16)
    ax2.set_yscale("log")
    ax2.set_ylim(5e-18, 5e-16)
    ax2.set_xlabel(r"Iterations")
    ax1.set_ylabel("Discrete Match Error")

    arrowprops = dict(arrowstyle="->", color="k", lw=1)
    bbox = dict(fc="1", ec="1")
    ax1.annotate(
        r"$\epsilon_{tol}$",
        xy=(10, tol),
        xytext=(12, 1e-3),
        fontsize=14,
        arrowprops=arrowprops,
        bbox=bbox,
        color="k",
        ha="left",
        va="center",
    )
    ax2.annotate(
        "If any iteration needed,\nSI converges to numeric zero quickly.",
        xy=(2.5, 1e-16),
        xytext=(3.5, 5e-17),
        fontsize=12,
        arrowprops=arrowprops,
        bbox=bbox,
        color="k",
        ha="left",
        va="center",
    )
    custom_lines = [
        Line2D([0], [0], color="red", lw=2, alpha=0.5, label="Fixed Size"),
        Line2D([0], [0], color="black", lw=2, alpha=0.5, label="Spanned Integer"),
    ]
    ax1.legend(title="MDM Algorithm", handles=custom_lines, loc="upper right")
    save(fig, "figure2_convergence.png")
    plt.close(fig)


# -----------------------------------------------------------------------------
# Figure 3 — MDM-predicted vs reported sample sizes
# -----------------------------------------------------------------------------
def make_fig3():
    zs_data = {
        "D": [50, 70, 105, 175, 50, 70, 105, 175, 70, 105, 175, 70, 105, 175],
        "SF": [5, 5, 5, 5, 10, 10, 10, 10, 15, 15, 15, 20, 20, 20],
        "H": [
            24.4,
            24.3,
            23.6,
            23.6,
            24.8,
            25.2,
            24.4,
            24.4,
            25.6,
            24.6,
            24.1,
            26.0,
            24.8,
            25.0,
        ],
        "e_c": [
            0.683,
            0.684,
            0.669,
            0.699,
            0.714,
            0.645,
            0.678,
            0.672,
            0.754,
            0.645,
            0.644,
            0.800,
            0.741,
            0.748,
        ],
        "N": [
            103075,
            202972,
            447161,
            1255067,
            12408,
            24349,
            54564,
            155028,
            7185,
            15719,
            44522,
            2816,
            6667,
            18180,
        ],
    }
    df = pd.DataFrame(zs_data)
    df["sample_volume"] = np.pi * (df["D"] / 2) ** 2 * df["H"]

    athabasca_sizes = np.array([0.076, 0.11, 0.15, 0.25, 0.43, 0.85, 2.40])
    athabasca_sizes = np.insert(athabasca_sizes, 0, athabasca_sizes[0] / 2)
    athabasca_percent_passing = np.array([3.86, 5.14, 15.27, 60.13, 81.35, 93.40, 100])
    athabasca_percent_passing = np.insert(athabasca_percent_passing, 0, 0.0)
    athabasca_retained = np.zeros(len(athabasca_sizes))
    for i in range(len(athabasca_sizes) - 1):
        athabasca_retained[i] = (
            athabasca_percent_passing[i + 1] - athabasca_percent_passing[i]
        )

    df["G"] = [
        GSD(sizes=athabasca_sizes * sf, masses=athabasca_retained) for sf in df["SF"]
    ]
    df["MDM"] = [
        MinimalPackingGenerator(gsd, x_n_factor=0.5, tol=1e-2, flex=True).mps
        for gsd in df["G"]
    ]
    df["N_mdm"] = [sum(mdm.quantities) for mdm in df["MDM"]]
    df["V_solids_mdm"] = [mdm.total_volume for mdm in df["MDM"]]
    df["V_total_mdm"] = df["V_solids_mdm"] * (1 + df["e_c"])
    df["MDM_per_sample"] = df["sample_volume"] / df["V_total_mdm"]
    df["N_predicted"] = df["N_mdm"] * df["MDM_per_sample"]

    unscaled_df = pd.DataFrame({"D": [50, 70, 105, 175]})
    unscaled_df["G"] = [
        GSD(sizes=athabasca_sizes, masses=athabasca_retained) for _ in range(4)
    ]
    unscaled_df["MDM"] = [
        MinimalPackingGenerator(gsd, x_n_factor=0.5, tol=1e-2, flex=True).mps
        for gsd in unscaled_df["G"]
    ]
    unscaled_df["N_mdm"] = [sum(mdm.quantities) for mdm in unscaled_df["MDM"]]
    unscaled_df["V_solids_mdm"] = [mdm.total_volume for mdm in unscaled_df["MDM"]]
    unscaled_df["V_total_mdm"] = unscaled_df["V_solids_mdm"] * (1 + 0.67)
    unscaled_df["MDM_per_sample"] = (
        25 * np.pi * (unscaled_df["D"] / 2) ** 2
    ) / unscaled_df["V_total_mdm"]
    unscaled_df["N_predicted"] = unscaled_df["N_mdm"] * unscaled_df["MDM_per_sample"]

    plt.close("all")
    fig, ax = plt.subplots()

    markers = ["v", "s", "D", "^"]
    colors = plt.cm.viridis(np.linspace(0, 1, len(df["D"].unique())))

    sf_values = sorted(df["SF"].unique())
    sf_to_marker = {sf: markers[i % len(markers)] for i, sf in enumerate(sf_values)}
    sf_to_marker[1] = "o"

    d_values = sorted(df["D"].unique())
    d_to_color = {d: colors[i] for i, d in enumerate(d_values)}

    for _, row in df.iterrows():
        ax.scatter(
            row["N_predicted"],
            row["N"],
            s=50,
            marker=sf_to_marker[row["SF"]],
            color=d_to_color[row["D"]],
            alpha=1,
            edgecolors="black",
            linewidth=0.5,
        )

    for _, row in unscaled_df.iterrows():
        ax.scatter(
            row["N_predicted"],
            row["N_predicted"],
            s=100,
            marker=sf_to_marker[1],
            color=d_to_color[row["D"]],
            alpha=1,
            edgecolors="black",
            linewidth=0.5,
            zorder=5,
        )

    from matplotlib.patches import FancyBboxPatch

    prediction_box = FancyBboxPatch(
        (8e3, 5e6),
        width=2e8,
        height=2e8,
        boxstyle="round",
        edgecolor="k",
        facecolor="none",
    )
    ax.add_patch(prediction_box)
    data_box = FancyBboxPatch(
        (1.2e3, 1.2e3),
        width=2e6,
        height=2e6,
        boxstyle="round",
        edgecolor="k",
        facecolor="none",
    )
    ax.add_patch(data_box)

    ax.text(
        x=1e4,
        y=1e7,
        s="MDM predictions for N\nrequired to build\nunscaled DEM models\nof Athabasca sand",
        fontsize=12,
    )
    ax.text(
        x=1.3e3,
        y=1.1e5,
        s="Zeraati-Shamsabadi \nand Sadrekarimi\n(2025) scaled\nDEM data",
        fontsize=12,
    )

    all_sf_values = sorted(list(sf_values) + [1])
    marker_legend_elements = [
        plt.scatter(
            [],
            [],
            marker=sf_to_marker[sf],
            color="gray",
            s=50,
            label=f"SF = {sf}" if sf != 1 else "Unscaled",
        )
        for sf in all_sf_values
    ]
    color_legend_elements = [
        plt.scatter([], [], marker="o", color=d_to_color[d], s=50, label=f"D = {d}")
        for d in d_values
    ]

    ax.plot([1e3, 5e8], [1e3, 5e8], color="k", linestyle="--", linewidth=1)
    legend1 = ax.legend(
        handles=marker_legend_elements,
        title="Scale Factor",
        loc="upper left",
        bbox_to_anchor=(0.62, 0.66),
        framealpha=1,
        edgecolor="1",
        fontsize="x-small",
    )
    ax.legend(
        handles=color_legend_elements,
        title="Sample D (mm)",
        loc="upper left",
        bbox_to_anchor=(0.57, 0.33),
        framealpha=1,
        edgecolor="1",
        fontsize="x-small",
    )
    ax.add_artist(legend1)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim([1e3, 5e8])
    ax.set_ylim([1e3, 5e8])
    ax.set_aspect("equal")
    ax.set_xlabel(r"$N_{sim}$ (MDM predicted)")
    ax.set_ylabel(r"$N_{sim}$ (reported)")
    ax.grid(False)
    save(fig, "figure3_demo_comparison.png")
    plt.close(fig)


# -----------------------------------------------------------------------------
# Larger dataset for figures 4, 5, 6 (~ qmd line 1034)
# -----------------------------------------------------------------------------
def build_large_df():
    def add_data_row(data_rows, mpgen):
        sample = mpgen.mps
        total_particles = sum(sample.quantities)
        mass_max = sample.total_masses[-1]
        mass_min = sample.total_masses[0]
        mass_ratio = mass_min / mass_max
        percent_fines = mass_min / sum(sample.total_masses)
        size_max = sample.sizes[-1]
        size_min = sample.sizes[0]
        size_ratio = int(np.round(size_max / size_min, 0))
        data_rows.append(
            {
                "GSD": mpgen.g,
                "n_sieves": len(sample.sizes),
                "mass_ratio": mass_ratio,
                "size_ratio": size_ratio,
                "vol_ratio": size_ratio**3,
                "percent_fines": percent_fines,
                "total_particles": total_particles,
                "d_10": mpgen.g.d_10,
                "d_30": mpgen.g.d_30,
                "d_60": mpgen.g.d_60,
                "cc": np.round(mpgen.g.cc, 3),
                "cu": np.round(mpgen.g.cu, 3),
                "gs_index": mpgen.g.gs_index,
                "curvature_index": mpgen.g.curvature_index,
                "slope": mpgen.g.slope,
                "curvature": np.mean(mpgen.g.curvature),
                "shape_factor": np.log10(
                    size_ratio**3 * (1 + np.mean(mpgen.g.curvature))
                ),
                "asdf": mass_ratio * size_ratio**3,
                "group_symbol": mpgen.g.uscs_symbol,
                "group_name": mpgen.g.uscs_name,
            }
        )

    rng_big = np.random.default_rng(1)
    # Re-burn the small-batch rng draws so the large-batch results match the qmd
    # (the qmd uses the same rng instance after the small batch ran).
    for start in range(0, len(x1) - min_span):
        for end in range(start + min_span, len(x1)):
            n_sieves = len(x1[start:end])
            for _ in range(10):
                mass_dist(n_sieves, rng_big, exponent=2, extra_randomness=7)

    data_rows = []
    for start in range(0, len(x1) - min_span):
        for end in range(start + min_span, len(x1)):
            new_x = x1[start:end]
            n_sieves = len(new_x)
            for _ in range(50):
                mass = mass_dist(n_sieves, rng_big, exponent=2, extra_randomness=7)
                mass[-1] = 0.0
                g = GSD(sizes=new_x, masses=mass)
                mps = MinimalPackingGenerator(
                    g, x_n_factor=0.001, tol=tol, flex=True, density=1.0
                )
                add_data_row(data_rows, mps)
    return pd.DataFrame(data_rows)


# -----------------------------------------------------------------------------
# Figures 4, 5, 6 — MDM vs mass-ratio / curvature-index / USCS class
# -----------------------------------------------------------------------------
def make_fig4(df):
    fig, ax = plt.subplots()
    ax.scatter(
        df["mass_ratio"],
        df["total_particles"],
        c=np.log10(df["vol_ratio"]),
        s=10,
        cmap="viridis",
        alpha=1,
    )
    colorbar = plt.colorbar(ax.collections[0], ax=ax)
    colorbar.set_label(r"Log$_{10}$Volume Ratio ($\zeta_1$)")
    ax.set_xlabel(r"Mass Ratio ($\phi_1$)")
    ax.set_ylabel("Particles in Discrete Match ($N_{MDM}$)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    save(fig, "figure4_phi_n.png")
    plt.close(fig)


def make_fig5(df):
    fig, ax = plt.subplots()
    ax.scatter(
        df["curvature_index"],
        df["total_particles"],
        c=np.log10(df["vol_ratio"]),
        s=10,
        cmap="viridis",
        alpha=1,
    )
    colorbar = plt.colorbar(ax.collections[0], ax=ax)
    colorbar.set_label(r"Log$_{10}$Volume Ratio ($\zeta_1$)")
    ax.set_xlabel("Curvature Index")
    ax.set_ylabel("Particles in Discrete Match ($N_{MDM}$)")
    ax.set_yscale("log")
    save(fig, "figure5_curvature_n.png")
    plt.close(fig)


def make_fig6(df):
    fig, ax = plt.subplots(figsize=(5, 7), layout="constrained")
    x_param = "gs_index"
    y_param = "total_particles"
    group_param = "group_name"
    categories = ["graded gravel", "graded sand", "silty"]
    markers = ["1", ".", "."]

    for j, cat in enumerate(categories):
        df_plot = df[df[group_param].str.contains(cat)]
        if cat == "silty":
            palette = ["#77B3C9", "#F2A900"]
        else:
            palette = sns.color_palette()
        for i, (label, group) in enumerate(df_plot.groupby(group_param)):
            symbol = group["group_symbol"].iloc[0]
            ax.scatter(
                group[x_param],
                group[y_param],
                label=f"{symbol} - {label.capitalize()}",
                marker=markers[j],
                color=palette[i],
                s=40,
            )

    fig.legend(
        loc="outside upper center",
        fontsize="small",
        ncols=1,
        frameon=False,
        handlelength=2,
    )
    ax.set_xlabel("Grain Size Index")
    ax.set_ylabel("Particles in Discrete Match ($N_{MDM}$)")
    ax.set_ylim(1e0, 2e10)
    ax.set_xlim(0.0, 0.6)
    ax.set_yscale("log")
    ax.grid(True, which="both", axis="both")
    save(fig, "figure6_uscs_n.png")
    plt.close(fig)


# -----------------------------------------------------------------------------
# Main
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("Figure 1 — GSD subset / curvature index")
    make_fig1()

    print("Figure 2 — Convergence")
    make_fig2()

    print("Figure 3 — MDM predicted vs reported")
    make_fig3()

    print("Building large dataset for figures 4–6 …")
    df_large = build_large_df()
    print(f"  {len(df_large)} rows")

    print("Figure 4 — phi vs N")
    make_fig4(df_large)

    print("Figure 5 — curvature index vs N")
    make_fig5(df_large)

    print("Figure 6 — USCS classification vs N")
    make_fig6(df_large)

    print(f"\nAll figures written to {OUT_DIR.relative_to(REPO_ROOT)}")
