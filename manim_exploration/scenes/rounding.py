"""Rounding approach + reducing error.

Layout (matches the MDM storyboard sketch):
  - Left:   three particle rows separated by sieve datums, each with a big
            integer count next to it.
  - Middle: cumulative-mass GSD curve. The target S-curve is solid; the
            realized curve from the current particle counts is drawn over
            it. Colored dots mark the cumulative point at each sieve. The
            shaded region between the two curves is the error.
  - Right:  the (unrounded) quantity-ratios vector [1, 4.6, 12.1].

`RoundingApproach` shows iteration i=0 (counts [1, 5, 12]).
`ReducingError` runs the loop: i=0 → i=1 → i=2 with counts converging
on the target curve.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Axes,
    Brace,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    MathTex,
    Polygon,
    Scene,
    Text,
    VGroup,
    VMobject,
    Write,
    config,
)

from _common import (
    BACKGROUND,
    COARSE,
    FINE,
    FOREGROUND,
    MID,
    COARSE_R,
    MID_R,
    FINE_R,
    make_particle,
    scatter_in_band,
)

config.background_color = BACKGROUND


# Numbers from the MDM storyboard sketch.
QUANTITY_RATIO = np.array([12.1, 4.6, 1.0])  # fine -> mid -> coarse
SCALES = [1, 2, 3]  # iteration multipliers; produces [1,5,12], [2,9,24], [3,14,36]

# Per-particle mass ~ x^3. Pick illustrative grain sizes so the curve shape
# matches the storyboard sketch.
SIZES = np.array([0.5, 1.0, 2.0])  # x_1 (fine), x_2 (mid), x_3 (coarse)
PER_PARTICLE_MASS = SIZES ** 3
TIER_COLORS = [FINE, MID, COARSE]

# Layout regions.
LEFT_X = -5.5  # center of pile column
DATUM_X = (-6.6, -3.6)
ROW_YS = (1.8, 0.0, -1.8)  # coarse, mid, fine (top to bottom matches storyboard)
PILE_BAND_HEIGHT = 1.0


def _round_match(scale: int) -> np.ndarray:
    return np.round(QUANTITY_RATIO * scale).astype(int)


def _cum_passing(counts: np.ndarray) -> np.ndarray:
    """Cumulative mass fraction at each sieve.

    counts ordered [fine, mid, coarse]. Returns 4 cumulative-passing values
    at sieve edges [pan, x_1, x_2, x_3]:
      pp[0] = 0
      pp[1] = m_fine / total
      pp[2] = (m_fine + m_mid) / total
      pp[3] = 1.0
    """
    masses = counts * PER_PARTICLE_MASS  # [m_fine, m_mid, m_coarse]
    total = masses.sum()
    return np.array([0.0, masses[0], masses[0] + masses[1], total]) / total


# Target curve uses the unrounded quantity ratio.
TARGET_PP = _cum_passing(QUANTITY_RATIO)
SIEVE_XS = np.array([0.0, 0.5, 1.0, 2.0])  # pan, x_1, x_2, x_3 (linear axis)


def _build_axes() -> Axes:
    return (
        Axes(
            x_range=[0, 2.2, 1],
            y_range=[0, 1.05, 0.25],
            x_length=4.0,
            y_length=2.8,
            tips=False,
            axis_config={
                "color": FOREGROUND,
                "stroke_width": 2,
                "include_ticks": False,
            },
        ).shift(DOWN * 0.2)
    )


def _smooth_curve(axes: Axes, target_pp: np.ndarray) -> VMobject:
    """A smooth interpolation through the four target points (S-shape)."""
    xs_dense = np.linspace(SIEVE_XS[0], SIEVE_XS[-1], 80)
    # Cubic Hermite-ish interpolation via numpy.interp on a stretched x.
    pp_dense = np.interp(xs_dense, SIEVE_XS, target_pp)
    # Soften the corners by averaging with a sigmoid through the same points.
    sig = 1 / (1 + np.exp(-3.5 * (xs_dense - 1.0)))
    sig = (sig - sig.min()) / (sig.max() - sig.min())
    pp_soft = 0.4 * pp_dense + 0.6 * sig
    pts = [axes.c2p(x, y) for x, y in zip(xs_dense, pp_soft)]
    curve = VMobject(stroke_color=FOREGROUND, stroke_width=3)
    curve.set_points_smoothly(pts)
    return curve


def _stair_curve(axes: Axes, pp: np.ndarray, color, dashed: bool = False) -> VMobject:
    """Realized cumulative curve: piecewise-linear through the sieve points."""
    pts = [axes.c2p(x, y) for x, y in zip(SIEVE_XS, pp)]
    curve = VMobject(
        stroke_color=color,
        stroke_width=3,
    )
    curve.set_points_as_corners(pts)
    return curve


def _error_band(axes: Axes, target_pp: np.ndarray, realized_pp: np.ndarray) -> Polygon:
    """Translucent band between target (smooth) and realized (piecewise) curves."""
    xs_dense = np.linspace(SIEVE_XS[0], SIEVE_XS[-1], 80)
    target_dense = np.interp(xs_dense, SIEVE_XS, target_pp)
    sig = 1 / (1 + np.exp(-3.5 * (xs_dense - 1.0)))
    sig = (sig - sig.min()) / (sig.max() - sig.min())
    target_smooth = 0.4 * target_dense + 0.6 * sig
    realized_dense = np.interp(xs_dense, SIEVE_XS, realized_pp)

    top_pts = [axes.c2p(x, y) for x, y in zip(xs_dense, target_smooth)]
    bot_pts = [axes.c2p(x, y) for x, y in zip(xs_dense[::-1], realized_dense[::-1])]
    return Polygon(
        *top_pts, *bot_pts,
        color=FOREGROUND,
        stroke_width=0,
        fill_color=FOREGROUND,
        fill_opacity=0.22,
    )


def _sieve_dots(axes: Axes, pp: np.ndarray) -> VGroup:
    """One colored dot per non-zero sieve, on the realized curve."""
    return VGroup(
        Dot(axes.c2p(SIEVE_XS[1], pp[1]), color=FINE, radius=0.09),
        Dot(axes.c2p(SIEVE_XS[2], pp[2]), color=MID, radius=0.09),
        Dot(axes.c2p(SIEVE_XS[3], pp[3]), color=COARSE, radius=0.09),
    )


def _piles_with_counts(counts: np.ndarray, rng: np.random.Generator) -> VGroup:
    """Three rows of particles with big integer labels.

    counts ordered [fine, mid, coarse]; rendered top→bottom as coarse, mid, fine.
    """
    n_fine, n_mid, n_coarse = int(counts[0]), int(counts[1]), int(counts[2])
    rows = VGroup()
    specs = [
        (n_coarse, COARSE_R, COARSE, ROW_YS[0]),
        (n_mid, MID_R, MID, ROW_YS[1]),
        (n_fine, FINE_R, FINE, ROW_YS[2]),
    ]
    for n, r, color, y in specs:
        band = (y - PILE_BAND_HEIGHT / 2, y + PILE_BAND_HEIGHT / 2)
        pile = scatter_in_band(
            n, r, color, band, (LEFT_X - 1.4, LEFT_X + 0.6), rng,
        )
        label = Text(str(n), font_size=72, color=color).move_to(
            [LEFT_X + 1.6, y, 0]
        )
        rows.add(VGroup(pile, label))
    return rows


def _datums() -> VGroup:
    ys = (
        (ROW_YS[0] + ROW_YS[1]) / 2,
        (ROW_YS[1] + ROW_YS[2]) / 2,
        ROW_YS[2] - PILE_BAND_HEIGHT / 2 - 0.3,
        ROW_YS[0] + PILE_BAND_HEIGHT / 2 + 0.3,
    )
    return VGroup(*[
        DashedLine(
            [DATUM_X[0], y, 0],
            [DATUM_X[1], y, 0],
            color=FOREGROUND,
            stroke_width=1.5,
            dash_length=0.12,
        )
        for y in ys
    ])


def _quantity_ratio_vector() -> VGroup:
    one = MathTex("1", color=COARSE)
    mid = MathTex("4.6", color=MID)
    fine = MathTex("12.1", color=FINE)
    stack = VGroup(one, mid, fine).arrange(DOWN, buff=0.55).move_to([5.0, 0, 0])
    bracket = VGroup(Brace(stack, LEFT), Brace(stack, RIGHT))
    title = Text("Quantity ratios", font_size=22, color=FOREGROUND).next_to(
        stack, UP, buff=0.3
    )
    return VGroup(bracket, stack, title)


def _build_chart(counts: np.ndarray) -> VGroup:
    axes = _build_axes().move_to([0.5, -0.2, 0])
    realized_pp = _cum_passing(counts)
    target = _smooth_curve(axes, TARGET_PP)
    realized = _stair_curve(axes, realized_pp, FOREGROUND)
    realized.set_stroke(width=3)
    band = _error_band(axes, TARGET_PP, realized_pp)
    dots = _sieve_dots(axes, realized_pp)
    x_lbl = Text("size", font_size=18, color=FOREGROUND).next_to(axes, DOWN, buff=0.1)
    y_lbl = Text("Mass", font_size=18, color=FOREGROUND).next_to(axes, LEFT, buff=0.1).shift(UP * 0.8)
    return VGroup(axes, band, target, realized, dots, x_lbl, y_lbl)


class RoundingApproach(Scene):
    def construct(self):
        title = Text("ERROR", font_size=44, color=FOREGROUND).to_edge(UP, buff=0.3)

        rng = np.random.default_rng(7)
        counts = _round_match(SCALES[0])  # [1, 5, 12]

        datums = _datums()
        piles = _piles_with_counts(counts, rng)
        chart = _build_chart(counts)
        ratio_vec = _quantity_ratio_vector()

        self.play(Write(title), run_time=0.5)
        self.play(FadeIn(datums), run_time=0.4)
        self.play(FadeIn(piles), run_time=0.7)
        self.play(FadeIn(ratio_vec), run_time=0.7)
        self.play(FadeIn(chart), run_time=1.0)
        self.wait(1.8)


class ReducingError(Scene):
    def construct(self):
        title = Text("ERROR", font_size=44, color=FOREGROUND).to_edge(UP, buff=0.3)

        datums = _datums()
        ratio_vec = _quantity_ratio_vector()

        self.play(Write(title), run_time=0.5)
        self.play(FadeIn(datums), FadeIn(ratio_vec), run_time=0.7)

        prev = None
        rng_seed = 11
        for scale in SCALES:
            rng = np.random.default_rng(rng_seed)
            rng_seed += 1
            counts = _round_match(scale)
            piles = _piles_with_counts(counts, rng)
            chart = _build_chart(counts)
            group = VGroup(piles, chart)

            if prev is None:
                self.play(FadeIn(group), run_time=0.9)
            else:
                self.play(FadeOut(prev), FadeIn(group), run_time=0.9)
            self.wait(1.0)
            prev = group

        self.wait(1.2)
