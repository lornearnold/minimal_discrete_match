"""Light-background conceptual figures for the poster.

Reimplements four key visuals from the storyboard/manim scenes as static
matplotlib figures suitable for a printed poster:

  1. concept1_question.png       — Scene 1: CDF curves + N_min=??? + DEM image.
  2. concept2_quantity_ratio.png — Scene 4: Φ × Z = K with "Non integers!".
  3. concept3_spanned_integer.png — NEW: where the spanned integer is found
                                    (between size extremes K_+ / K_-).
  4. concept4_verification.png   — Scene 5: predicted vs reported + checklist.

Color palette mirrors the manim scenes (RED / BLUE / GREEN tiers) but on a
white background with black foreground.
"""

from __future__ import annotations

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from matplotlib.patches import (
    Circle,
    ConnectionPatch,
    Ellipse,
    FancyArrowPatch,
    FancyBboxPatch,
    PathPatch,
    Polygon,
    Rectangle,
)
from matplotlib.path import Path as MplPath

REPO_ROOT = Path(__file__).resolve().parents[2]
POSTER_DIR = REPO_ROOT / "minimal_packing_poster"
OUT_DIR = POSTER_DIR / "assets" / "figures"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ----- Color palette (light-bg adaptation of manim defaults) -----------------
COARSE = "#D14B3F"   # red tier (slightly darker than 3B1B red for white bg)
MID    = "#3B95B5"   # blue tier
FINE   = "#5DA052"   # green tier
FG     = "#111111"   # foreground / text
BG     = "#FFFFFF"   # background
ACCENT = "#C68A00"   # callout (yellow, readable on white)
GREEN_OK = "#2E9B3F"
RED_BAD  = "#C82828"


def _lighten(hex_color: str, t: float = 0.55) -> tuple[float, float, float]:
    """Mix hex color toward white by fraction t (0 = original, 1 = white)."""
    r = int(hex_color[1:3], 16) / 255
    g = int(hex_color[3:5], 16) / 255
    b = int(hex_color[5:7], 16) / 255
    return (r + (1 - r) * t, g + (1 - g) * t, b + (1 - b) * t)


# Disable LaTeX globally — concept figures use mathtext for portability.
plt.rcParams.update({
    "text.usetex": False,
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "mathtext.fontset": "dejavusans",
    "savefig.dpi": 600,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.15,
})


def save(fig: plt.Figure, name: str) -> None:
    out = OUT_DIR / name
    fig.savefig(out)
    print(f"  wrote {out.relative_to(REPO_ROOT)}")
    plt.close(fig)


# =============================================================================
# Concept 1 — Scene 1: The motivating question
# =============================================================================
def concept1_question() -> None:
    fig = plt.figure(figsize=(11, 5.5))

    # Left: CDF curves on log-x. All three curves anchor at the upper-right
    # (largest sieve → 100% passing) and only the lower-left tail moves —
    # broader GSDs extend further into the fines.
    ax_left = fig.add_axes([0.05, 0.18, 0.34, 0.66])
    ax_left.set_xlim(0.01, 5.4)
    ax_left.set_ylim(-2, 104)
    ax_left.set_xscale("log")
    # Sigmoid-shaped CDFs: in log-x, % passing = 100 * S((log10 x − μ) / σ).
    # All three share x_top = X_RIGHT mapping to ≈100%.
    X_RIGHT = 4.6
    log_x = np.log10(np.geomspace(0.01, X_RIGHT, 600))
    log_x_top = np.log10(X_RIGHT)
    curve_specs = [
        # (mu, sigma, color)  — larger σ = broader distribution = reaches
        # further into the fines on the left.
        ( np.log10(2.6), 0.20, COARSE),  # narrow, far right
        ( np.log10(1.0), 0.40, MID),
        ( np.log10(0.20), 0.65, FINE),   # broadest
    ]
    for mu, sigma, color in curve_specs:
        # Anchor the upper tail at (X_RIGHT, 100): subtract the residual so
        # all curves pass through that point exactly.
        raw_top = 100 / (1 + np.exp(-(log_x_top - mu) / sigma))
        scale = 100 / raw_top
        yv = 100 / (1 + np.exp(-(log_x - mu) / sigma)) * scale
        ax_left.plot(10 ** log_x, np.clip(yv, 0, 100),
                     color=color, linewidth=3.4)
    ax_left.set_xlabel("grain size", fontsize=14, color=FG)
    ax_left.set_ylabel("% finer", fontsize=14, color=FG)
    for side in ("top", "right"):
        ax_left.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax_left.spines[side].set_color(FG)
    ax_left.tick_params(colors=FG, length=0)
    ax_left.set_xticks([])
    ax_left.set_yticks([])
    # Axis arrow tips, slightly longer so they actually render.
    ax_left.annotate("", xy=(1.04, -0.005), xytext=(0.92, -0.005),
                     xycoords="axes fraction",
                     arrowprops=dict(arrowstyle="-|>", color=FG, lw=2,
                                     mutation_scale=16))
    ax_left.annotate("", xy=(0.0, 1.04), xytext=(0.0, 0.92),
                     xycoords="axes fraction",
                     arrowprops=dict(arrowstyle="-|>", color=FG, lw=2,
                                     mutation_scale=16))

    # Center: block arrow with N_min = ??? above it
    ax_arrow = fig.add_axes([0.39, 0.28, 0.18, 0.44])
    ax_arrow.set_xlim(-1, 1)
    ax_arrow.set_ylim(-1.05, 1.05)
    ax_arrow.axis("off")
    arrow_pts = np.array([
        [-0.85, -0.20], [ 0.20, -0.20], [ 0.20, -0.55],
        [ 0.85,  0.00], [ 0.20,  0.55], [ 0.20,  0.20],
        [-0.85,  0.20],
    ])
    ax_arrow.add_patch(Polygon(
        arrow_pts, closed=True,
        facecolor=_lighten(FG, 0.85), edgecolor=FG, linewidth=2,
    ))
    # N_min label centered over the arrow.
    ax_arrow.text(0.0, 0.75, r"$N_{\min}=\,???$",
                  ha="center", va="bottom", fontsize=22, color=FG,
                  clip_on=False)

    # Right: DEM packing image
    ax_img = fig.add_axes([0.56, 0.10, 0.40, 0.80])
    dem_path = REPO_ROOT / "manim_expl_2" / "GSD_0.png"
    if dem_path.exists():
        ax_img.imshow(mpimg.imread(dem_path))
    ax_img.axis("off")

    # Title across the top
    title = ("What is the smallest number of discrete particles\n"
             "needed to match a given grain size distribution?")
    fig.text(0.5, 0.94, title,
             ha="center", va="top", fontsize=18, color=FG,
             bbox=dict(facecolor=BG, edgecolor=FG, linewidth=1.5,
                       boxstyle="round,pad=0.5"))
    fig.text(0.5, 0.06, "Minimal Discrete Match (MDM)",
             ha="center", va="bottom", fontsize=16, color=FG,
             weight="bold")
    fig.text(0.78, 0.015, "DEM render: modified from Claudio Esperança (2023)",
             ha="center", va="bottom", fontsize=10, color=FG, alpha=0.7,
             style="italic")
    fig.patch.set_facecolor(BG)
    save(fig, "concept1_question.png")


# =============================================================================
# Concept 2 — Scene 4: Φ × Z = K, with "Non integers!"
# =============================================================================
def concept2_quantity_ratio() -> None:
    fig, ax = plt.subplots(figsize=(11, 6.5))
    ax.set_xlim(0, 22)
    ax.set_ylim(-0.3, 7.5)
    ax.set_aspect("equal")
    ax.axis("off")
    fig.patch.set_facecolor(BG)

    # Each row has a baseline (where the pile sits) and a row-center y used
    # for in-line math symbols (×, =, K entries). Center = baseline + h/2
    # for that row's mountain height.
    PILE_H = {"coarse": 0.55, "mid": 0.40, "fine": 0.75}
    BASE_Y = {"coarse": 5.55, "mid": 3.95, "fine": 1.05}
    CENTER_Y = {tier: BASE_Y[tier] + PILE_H[tier] / 2 for tier in PILE_H}
    DOTS_Y = (CENTER_Y["mid"] + CENTER_Y["fine"]) / 2

    # Sieve lines: dashed under coarse and mid piles, solid under M_1.
    line_x0, line_x1 = 0.3, 12.6
    for tier in ("coarse", "mid"):
        y = BASE_Y[tier]
        ax.plot([line_x0, line_x1], [y, y], ":", color=FG, linewidth=1.4)
    ax.plot([line_x0, line_x1], [BASE_Y["fine"], BASE_Y["fine"]],
            "-", color=FG, linewidth=1.8)

    # Column x-positions
    PHI_NUM_X = 1.6
    PHI_SLASH_X = 3.3
    PHI_DEN_X = 4.9
    TIMES_X = 6.4
    Z_NUM_X = 7.5
    Z_SLASH_X = 8.5
    Z_DEN_X = 9.6
    EQ_X = 10.8
    K_X = 12.4
    NON_INT_X = 15.0

    # Top labels Φ, Z, K
    label_y = 6.95
    ax.text((PHI_NUM_X + PHI_DEN_X) / 2, label_y, r"$\Phi$",
            ha="center", va="center", fontsize=34, color=FG)
    ax.text((Z_NUM_X + Z_DEN_X) / 2, label_y, r"$Z$",
            ha="center", va="center", fontsize=34, color=FG, style="italic")
    ax.text(K_X, label_y, r"$K$",
            ha="center", va="center", fontsize=34, color=FG, style="italic")

    # ---- Mountain pile primitive -----------------------------------------
    def mountain(cx, baseline_y, w, h, color, label):
        """Mound-shaped pile with baseline ON the sieve datum."""
        verts = [
            (cx - w / 2, baseline_y),
            (cx - w * 0.42, baseline_y + h * 0.85),
            (cx - w * 0.20, baseline_y + h),
            (cx + w * 0.10, baseline_y + h * 0.95),
            (cx + w * 0.42, baseline_y + h * 0.55),
            (cx + w / 2, baseline_y),
        ]
        codes = [MplPath.MOVETO, MplPath.CURVE3, MplPath.CURVE3,
                 MplPath.CURVE3, MplPath.CURVE3, MplPath.LINETO]
        ax.add_patch(PathPatch(MplPath(verts, codes),
                               facecolor=_lighten(color, 0.55),
                               edgecolor=color, linewidth=2))
        ax.text(cx, baseline_y + h * 0.50, label,
                ha="center", va="center",
                fontsize=13, color=FG)  # FG label for legibility

    # Φ numerator piles
    mountain(PHI_NUM_X, BASE_Y["coarse"], 1.5, PILE_H["coarse"], COARSE, r"$M_N$")
    mountain(PHI_NUM_X, BASE_Y["mid"],    1.3, PILE_H["mid"],    MID,    r"$M_{N-1}$")
    mountain(PHI_NUM_X, BASE_Y["fine"],   1.7, PILE_H["fine"],   FINE,   r"$M_1$")

    # Φ denominator: identical M_N pile on every row
    for tier in ("coarse", "mid", "fine"):
        mountain(PHI_DEN_X, BASE_Y[tier], 1.5, PILE_H["coarse"], COARSE, r"$M_N$")

    # Slashes sized to each row's pile height
    def slash(cx, baseline_y, pile_h):
        ax.plot([cx - 0.14, cx + 0.14],
                [baseline_y - 0.05, baseline_y + pile_h + 0.20],
                color=FG, linewidth=2.0)

    for tier in ("coarse", "mid", "fine"):
        slash(PHI_SLASH_X, BASE_Y[tier], max(PILE_H[tier], PILE_H["coarse"]))

    # Vertical dots in Φ numerator (between mid and fine)
    ax.text(PHI_NUM_X, DOTS_Y, r"$\vdots$",
            ha="center", va="center", fontsize=24, color=FG)
    ax.text(PHI_DEN_X, DOTS_Y, r"$\vdots$",
            ha="center", va="center", fontsize=24, color=FG)

    # ---- × symbols on row centers ----------------------------------------
    for tier in ("coarse", "mid", "fine"):
        ax.text(TIMES_X, CENTER_Y[tier], r"$\times$",
                ha="center", va="center", fontsize=22, color=FG)

    # ---- Particle ratios (Z) ---------------------------------------------
    def particle(cx, cy, r, color):
        ax.add_patch(Circle((cx, cy), r,
                            facecolor=_lighten(color, 0.55),
                            edgecolor=color, linewidth=2))

    R_C, R_M, R_F = 0.40, 0.24, 0.08
    # Z numerator (largest particle on every row)
    for tier in ("coarse", "mid", "fine"):
        particle(Z_NUM_X, CENTER_Y[tier], R_C, COARSE)
    # Z denominator (per-tier particle)
    particle(Z_DEN_X, CENTER_Y["coarse"], R_C, COARSE)
    particle(Z_DEN_X, CENTER_Y["mid"],    R_M, MID)
    particle(Z_DEN_X, CENTER_Y["fine"],   R_F, FINE)

    # Z slashes — slightly shorter than the mass slashes
    for tier in ("coarse", "mid", "fine"):
        cy = CENTER_Y[tier]
        ax.plot([Z_SLASH_X - 0.14, Z_SLASH_X + 0.14],
                [cy - R_C - 0.05, cy + R_C + 0.05],
                color=FG, linewidth=2.0)

    # Z dots column between mid and fine
    ax.text(Z_NUM_X, DOTS_Y, r"$\vdots$",
            ha="center", va="center", fontsize=24, color=FG)
    ax.text(Z_DEN_X, DOTS_Y, r"$\vdots$",
            ha="center", va="center", fontsize=24, color=FG)

    # ---- = sign on the vertical midline ---------------------------------
    eq_y = (CENTER_Y["coarse"] + CENTER_Y["fine"]) / 2
    ax.text(EQ_X, eq_y, r"$=$",
            ha="center", va="center", fontsize=34, color=FG)

    # ---- K vector --------------------------------------------------------
    bracket_top = CENTER_Y["coarse"] + 0.55
    bracket_bot = CENTER_Y["fine"]   - 0.55
    bracket_w = 0.30
    for sign, x_off in [(+1, -0.50), (-1, +0.50)]:
        verts = [
            (K_X + x_off + sign * bracket_w, bracket_top),
            (K_X + x_off,                    bracket_top),
            (K_X + x_off,                    bracket_bot),
            (K_X + x_off + sign * bracket_w, bracket_bot),
        ]
        codes = [MplPath.MOVETO, MplPath.LINETO, MplPath.LINETO, MplPath.LINETO]
        ax.add_patch(PathPatch(MplPath(verts, codes),
                               facecolor="none", edgecolor=FG, linewidth=2))

    # K entries
    ax.text(K_X, CENTER_Y["coarse"], "1",
            ha="center", va="center", fontsize=30, color=COARSE, weight="bold")
    ax.text(K_X, CENTER_Y["mid"], "?.?",
            ha="center", va="center", fontsize=24, color=MID, weight="bold")
    ax.text(K_X, DOTS_Y, r"$\vdots$",
            ha="center", va="center", fontsize=24, color=FG)
    ax.text(K_X, CENTER_Y["fine"], "?.?",
            ha="center", va="center", fontsize=24, color=FINE, weight="bold")

    # ---- "Non integers!" callout around mid + fine + dots entries -------
    callout_top = CENTER_Y["mid"] + 0.45
    callout_bot = CENTER_Y["fine"] - 0.45
    callout_box = Rectangle(
        (K_X - 0.60, callout_bot),
        1.2, callout_top - callout_bot,
        facecolor="none", edgecolor=ACCENT, linewidth=2.8,
    )
    ax.add_patch(callout_box)
    label_y_callout = (callout_top + callout_bot) / 2
    # Single-line label, placed clear of the K bracket; widen xlim if needed.
    ax.set_xlim(0, 22)
    ax.text(NON_INT_X + 1.0, label_y_callout,
            "Non integers!",
            ha="left", va="center", fontsize=22, color=ACCENT,
            weight="bold")
    ax.annotate("",
                xy=(NON_INT_X + 0.9, label_y_callout),
                xytext=(K_X + 0.65, label_y_callout),
                arrowprops=dict(arrowstyle="-", color=ACCENT, lw=2.2))

    save(fig, "concept2_quantity_ratio.png")


# =============================================================================
# Concept 3 — Spanned integer (function-graph form)
# =============================================================================
def concept3_spanned_integer() -> None:
    """K is a continuous monotonic function of the chosen particle size x
    inside an allowable range [x_min, x_max]. As x sweeps that range, K
    traces a continuous curve from K_+ (at x_max) to K_- (at x_min). When
    that interval [K_+, K_-] brackets an integer N, the equation K(x) = N
    has a unique solution x_SI — that's the spanned-integer particle.

    Spherical particles: K(x) = φ · (x_max / x)³.
    """
    fig, ax = plt.subplots(figsize=(10, 6))
    fig.patch.set_facecolor(BG)

    # --- Pick example numbers: a single integer (5) is spanned. ----------
    # Use a size range that hits K_+ = 4.3 (right end) and K_- = 5.7 (left).
    x_max = 1.00
    K_plus = 4.3
    # K(x) = K_plus * (x_max / x)^3  → choose x_min so K(x_min) = K_minus.
    K_minus = 5.7
    x_min = x_max / (K_minus / K_plus) ** (1 / 3)
    N_SI = 5
    x_SI = x_max / (N_SI / K_plus) ** (1 / 3)

    # --- Axes setup ------------------------------------------------------
    x_lo_view, x_hi_view = x_min - 0.012, x_max + 0.012
    K_lo_view, K_hi_view = 3.5, 6.5
    ax.set_xlim(x_lo_view, x_hi_view)
    ax.set_ylim(K_lo_view, K_hi_view)
    ax.set_xlabel("particle size  $x$  (within one sieve range)",
                  fontsize=14, color=FG)
    ax.set_ylabel("quantity ratio  $K(x)$", fontsize=14, color=FG)
    ax.tick_params(colors=FG)
    for s in ax.spines.values():
        s.set_color(FG)

    # --- Integer grid on K axis -----------------------------------------
    # Faint horizontal lines at every integer; highlight the spanned one.
    for k in range(int(np.ceil(K_lo_view)), int(np.floor(K_hi_view)) + 1):
        if k == N_SI:
            continue
        ax.axhline(k, color=FG, linewidth=0.6, alpha=0.20, zorder=1)
    ax.axhline(N_SI, color=ACCENT, linewidth=2.5, alpha=0.85, zorder=2)
    ax.text(x_lo_view + 0.002, N_SI + 0.06, f"$K = {N_SI}$  (integer)",
            ha="left", va="bottom", fontsize=12, color=ACCENT, weight="bold")

    # --- K(x) curve ------------------------------------------------------
    xs = np.linspace(x_min, x_max, 300)
    Ks = K_plus * (x_max / xs) ** 3
    ax.plot(xs, Ks, color=MID, linewidth=3.5, zorder=3,
            label=r"$K(x) = \phi \cdot (x_{\max}/x)^3$")

    # --- Shaded vertical band: [K_+, K_-] interval on the K axis --------
    ax.axhspan(K_plus, K_minus, color=MID, alpha=0.08, zorder=0)

    # --- Endpoint markers: (x_max, K_+) and (x_min, K_-) ---------------
    ax.scatter([x_max], [K_plus], s=110, color=MID,
               edgecolor=FG, linewidth=1.3, zorder=4)
    ax.scatter([x_min], [K_minus], s=110, color=MID,
               edgecolor=FG, linewidth=1.3, zorder=4)
    # Plain-text labels avoid the unreliable subscript/decimal rendering
    # of the mathtext fontset at small sizes. The "+" / "-" are kept inline
    # rather than subscripted; the math symbol K_+/K_- shows in the title.
    ax.annotate(f"K+ = {K_plus}\n(largest allowed size)",
                xy=(x_max, K_plus), xytext=(x_max - 0.018, K_plus - 0.55),
                ha="right", va="top", fontsize=13, color=FG,
                arrowprops=dict(arrowstyle="-", color=FG, lw=1))
    ax.annotate(f"K− = {K_minus}\n(smallest allowed size)",
                xy=(x_min, K_minus), xytext=(x_min + 0.018, K_minus + 0.40),
                ha="left", va="bottom", fontsize=13, color=FG,
                arrowprops=dict(arrowstyle="-", color=FG, lw=1))

    # --- The spanned-integer particle: (x_SI, N_SI) ---------------------
    ax.scatter([x_SI], [N_SI], s=180, color=ACCENT,
               edgecolor=FG, linewidth=1.5, zorder=5)
    # Drop lines from the intersection down to the x-axis and across to
    # the K axis so x_SI is unambiguous.
    ax.plot([x_SI, x_SI], [K_lo_view, N_SI],
            linestyle="--", color=ACCENT, linewidth=1.5, zorder=2)
    ax.plot([x_lo_view, x_SI], [N_SI, N_SI],
            linestyle="--", color=ACCENT, linewidth=1.5, zorder=2,
            alpha=0)  # the highlighted integer gridline already shows this
    # x_SI label placed just inside the plot, above the x-axis, so it
    # doesn't collide with the axis label below.
    ax.text(x_SI, K_lo_view + 0.10, r"$x_{\mathrm{SI}}$",
            ha="center", va="bottom", fontsize=14, color=ACCENT,
            weight="bold")

    # --- Tick labels at the size endpoints ------------------------------
    # Only x_min and x_max get tick labels; x_SI is labeled by the annotation
    # below the spanned-integer marker.
    ax.set_xticks([x_min, x_max])
    ax.set_xticklabels([r"$x_{\min}$", r"$x_{\max}$"],
                       fontsize=12, color=FG)
    ax.set_yticks([4, 5, 6])
    ax.tick_params(axis="y", labelsize=11)

    # --- Caption / title -----------------------------------------------
    ax.set_title(
        r"$K_+ \leq N \leq K_-$  $\Rightarrow$  "
        r"some size $x_{\mathrm{SI}}$ gives  $K(x_{\mathrm{SI}}) = N$",
        fontsize=15, color=FG, pad=15,
    )

    fig.tight_layout()
    save(fig, "concept3_spanned_integer.png")


# =============================================================================
# Concept 4 — Scene 5: verification scatter + capabilities checklist
# =============================================================================
def concept4_verification() -> None:
    fig = plt.figure(figsize=(11, 6))
    fig.patch.set_facecolor(BG)
    ax = fig.add_axes([0.07, 0.12, 0.50, 0.78])

    # Data from scene5_verification.py
    zs_points = [
        (50, 5, 103075, 6.92e4),
        (70, 5, 202972, 1.35e5),
        (105, 5, 447161, 2.98e5),
        (175, 5, 1255067, 8.13e5),
        (50, 10, 12408, 8.64e3),
        (70, 10, 24349, 1.79e4),
        (105, 10, 54564, 3.83e4),
        (175, 10, 155028, 1.07e5),
        (70, 15, 7185, 5.06e3),
        (105, 15, 15719, 1.17e4),
        (175, 15, 44522, 3.18e4),
        (70, 20, 2816, 2.11e3),
        (105, 20, 6667, 4.69e3),
        (175, 20, 18180, 1.31e4),
    ]
    zs_unscaled_predicted = [
        (50, 8.94e6),
        (70, 1.75e7),
        (105, 3.94e7),
        (175, 1.09e8),
    ]
    d_colors = {
        50: "#4C1F6E",
        70: "#27689F",
        105: "#2BB48C",
        175: "#F8C92F",
    }
    sf_marker = {1: "o", 5: "v", 10: "s", 15: "D", 20: "^"}

    # Plot scaled data
    for d, sf, n, n_pred in zs_points:
        ax.scatter(n_pred, n, s=70, c=d_colors[d], marker=sf_marker[sf],
                   edgecolors=FG, linewidths=0.8, zorder=3)
    # Plot unscaled predictions (no reported value -> place on y=x)
    for d, n_pred in zs_unscaled_predicted:
        ax.scatter(n_pred, n_pred, s=130, c=d_colors[d], marker="o",
                   edgecolors=FG, linewidths=0.9, zorder=4)

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e3, 5e8)
    ax.set_ylim(1e3, 5e8)
    ax.set_aspect("equal")
    ax.plot([1e3, 5e8], [1e3, 5e8], "--", color=FG, linewidth=1, zorder=2)
    ax.set_xlabel(r"$\log_{10}\,N_{sim}$  (predicted)", fontsize=13, color=FG)
    ax.set_ylabel(r"$\log_{10}\,N_{sim}$  (reported)", fontsize=13, color=FG)
    ax.tick_params(colors=FG)
    for spine in ax.spines.values():
        spine.set_color(FG)
    ax.grid(False)

    # Slope-aligned ellipses around each cluster, drawn in log-space as a
    # parametric polyline (avoids matplotlib's log-aware patch transforms).
    log_scaled = np.array([(np.log10(n_pred), np.log10(n))
                           for _, _, n, n_pred in zs_points])
    cx, cy = log_scaled.mean(axis=0)
    diag = np.array([1, 1]) / np.sqrt(2)
    perp = np.array([-1, 1]) / np.sqrt(2)
    proj_d = (log_scaled - [cx, cy]) @ diag
    proj_p = (log_scaled - [cx, cy]) @ perp
    major = (proj_d.max() - proj_d.min()) / 2 + 0.35
    minor = (proj_p.max() - proj_p.min()) / 2 + 0.30
    theta = np.linspace(0, 2 * np.pi, 200)
    ex = cx + major * np.cos(theta) * diag[0] + minor * np.sin(theta) * perp[0]
    ey = cy + major * np.cos(theta) * diag[1] + minor * np.sin(theta) * perp[1]
    ax.plot(10 ** ex, 10 ** ey, color=ACCENT, linewidth=2.2, zorder=5)
    # "Verification" label placed perpendicular to the ellipse's major
    # axis on its UPPER side (toward the y-axis side, but offset enough
    # to clear the rotated y-axis label). The "perp" direction times a
    # positive scalar puts us above-left of the ellipse center.
    verif_lx = cx + minor * perp[0] * 1.8
    verif_ly = cy + minor * perp[1] * 1.8
    ax.text(10 ** verif_lx, 10 ** verif_ly, "Verification",
            ha="center", va="center", fontsize=13, color=ACCENT,
            weight="bold", rotation=45, rotation_mode="anchor")

    # Ellipse around the unscaled prediction cluster
    log_un = np.array([(np.log10(n_pred), np.log10(n_pred))
                       for _, n_pred in zs_unscaled_predicted])
    ux, uy = log_un.mean(axis=0)
    proj_d_u = (log_un - [ux, uy]) @ diag
    proj_p_u = (log_un - [ux, uy]) @ perp
    major_u = (proj_d_u.max() - proj_d_u.min()) / 2 + 0.35
    minor_u = (proj_p_u.max() - proj_p_u.min()) / 2 + 0.30
    ex2 = ux + major_u * np.cos(theta) * diag[0] + minor_u * np.sin(theta) * perp[0]
    ey2 = uy + major_u * np.cos(theta) * diag[1] + minor_u * np.sin(theta) * perp[1]
    ax.plot(10 ** ex2, 10 ** ey2, color=FG, linewidth=2.0, zorder=5)

    # Bullet list in a right-hand panel
    ax_bullets = fig.add_axes([0.62, 0.12, 0.36, 0.78])
    ax_bullets.set_xlim(0, 1)
    ax_bullets.set_ylim(0, 1)
    ax_bullets.axis("off")
    bullets = [
        ("ok",  "Experimental design"),
        ("ok",  "Any grain size dist."),
        ("ok",  "Arbitrary shapes"),
        ("ok",  "Closed form"),
        ("ok",  r"$N_{\min}(\mathrm{GSD})$"),
        ("ok",  r"GSD $\rightarrow$ computation cost"),
        ("bad", "Representative volume"),
    ]
    bullet_ys = []
    for i, (kind, label) in enumerate(bullets):
        y = 0.92 - i * 0.115
        bullet_ys.append(y)
        if kind == "ok":
            ax_bullets.plot([0.04, 0.10, 0.18], [y, y - 0.025, y + 0.030],
                            color=GREEN_OK, linewidth=4,
                            solid_capstyle="round", solid_joinstyle="round")
        else:
            ax_bullets.plot([0.04, 0.18], [y - 0.025, y + 0.030],
                            color=RED_BAD, linewidth=4, solid_capstyle="round")
            ax_bullets.plot([0.04, 0.18], [y + 0.030, y - 0.025],
                            color=RED_BAD, linewidth=4, solid_capstyle="round")
        ax_bullets.text(0.26, y, label, ha="left", va="center",
                        fontsize=14, color=FG)

    # Connect the right edge of the unscaled-prediction ellipse to the
    # first bullet using ConnectionPatch so the endpoints lock to each
    # axes' own data coordinates.
    arrow_src_data = (10 ** (ux + major_u * diag[0]),    # right tip of ellipse
                      10 ** (uy + major_u * diag[1]))
    arrow_dst_data = (0.02, bullet_ys[0])
    arrow = ConnectionPatch(
        xyA=arrow_src_data, coordsA=ax.transData,
        xyB=arrow_dst_data, coordsB=ax_bullets.transData,
        arrowstyle="-|>", color=FG, linewidth=2.2, mutation_scale=18,
    )
    fig.add_artist(arrow)

    # ---- Inline legend: stacked vertically in the lower-right quadrant --
    # Scale factor on top, Sample-D below — each group's swatches in a
    # single column so headers can't collide.
    legend_x = 3.0e7
    label_x  = 6.0e7

    sf_header_y = 5e5
    ax.text(legend_x, sf_header_y, "Scale factor",
            ha="left", va="center", fontsize=10, color=FG, weight="bold")
    sf_labels = [(1, "unscaled"), (5, "5"), (10, "10"), (15, "15"), (20, "20")]
    for i, (sf, lbl) in enumerate(sf_labels):
        ypos = 10 ** (np.log10(sf_header_y) - 0.24 * (i + 1))
        ax.scatter(legend_x, ypos, s=55, marker=sf_marker[sf],
                   facecolor=FG, edgecolor=FG, linewidths=0.6, zorder=6)
        ax.text(label_x, ypos, lbl,
                ha="left", va="center", fontsize=9, color=FG)

    d_header_y = 10 ** (np.log10(sf_header_y) - 0.24 * (len(sf_labels) + 1.2))
    ax.text(legend_x, d_header_y, "Sample D (mm)",
            ha="left", va="center", fontsize=10, color=FG, weight="bold")
    for i, d in enumerate([50, 70, 105, 175]):
        ypos = 10 ** (np.log10(d_header_y) - 0.24 * (i + 1))
        ax.scatter(legend_x, ypos, s=70, marker="o",
                   facecolor=d_colors[d], edgecolor=FG, linewidths=0.7, zorder=6)
        ax.text(label_x, ypos, str(d),
                ha="left", va="center", fontsize=9, color=FG)

    fig.text(0.5, 0.97, "Verification and example usage",
             ha="center", va="top", fontsize=17, color=FG)

    save(fig, "concept4_verification.png")


# =============================================================================
if __name__ == "__main__":
    print("Rendering concept figures …")
    concept1_question()
    concept2_quantity_ratio()
    concept3_spanned_integer()
    concept4_verification()
    print(f"\nAll figures written to {OUT_DIR.relative_to(REPO_ROOT)}")
