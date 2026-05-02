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
    WHITE,
    Arrow,
    Axes,
    Brace,
    Create,
    CurvedArrow,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    GrowArrow,
    MathTex,
    Polygon,
    Rectangle,
    Scene,
    Text,
    Transform,
    VGroup,
    VMobject,
    Write,
    config,
)
from manim.utils.color import GREEN, RED

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
    tex_text,
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

# Layout regions (q_vec → arrow → pile → chart → error_bar).
QVEC_X = -5.2
ARROW_X = -4.0
LEFT_X = -1.8  # center of integer pile column
DATUM_X = (-3.6, -0.3)
NUM_LABEL_X = -3.1  # numbers sit inside the sieve stack, left of particles
PILE_X_RANGE = (-2.5, -1.1)  # particle scatter range
CHART_X = 3.5
ERR_BAR_X = 6.5
ROW_YS = (1.8, 0.0, -1.8)  # coarse, mid, fine (top to bottom)
PILE_BAND_HEIGHT = 1.0
NUM_LABEL_FONT = 70

# Error-bar geometry.
ERR_BAR_BOTTOM_Y = -1.8
ERR_BAR_HEIGHT = 3.4
ERR_BAR_WIDTH = 0.3
TOLERANCE_FRAC = 0.20  # fraction of full bar height
ERR_HIGH_COLOR = RED
ERR_OK_COLOR = GREEN


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

# Hand-tuned realized cumulative-passing values per iteration. These drive
# the chart's realized curve, dots, and error band so the visualization
# matches the MDM_storyboard error sketches (rather than the strictly
# computed _cum_passing, which would always pin the red dot at 100%).
# Order: [pan=0, fine_dot, mid_dot, coarse_dot]. Values normalized so the
# target plateau = 1.0.
ITER_PP = {
    1: np.array([0.0, 0.05, 0.58, 0.80]),  # red below, blue above, green below
    2: np.array([0.0, 0.08, 0.50, 0.88]),  # same above/below by color
    3: np.array([0.0, 0.11, 0.46, 0.99]),  # all dots within 2% of target
}


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
    """Realized cumulative curve: smooth (not stair) line through the sieve
    dots, so the dots read as samples on a continuous mass-distribution."""
    pts = [axes.c2p(x, y) for x, y in zip(SIEVE_XS, pp)]
    curve = VMobject(
        stroke_color=color,
        stroke_width=3,
    )
    curve.set_points_smoothly(pts)
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
            n, r, color, band, PILE_X_RANGE, rng,
        )
        label = tex_text(str(n), font_size=NUM_LABEL_FONT, color=color).move_to(
            [NUM_LABEL_X, y, 0]
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
    coarse_lbl = MathTex("1", color=COARSE).scale(1.4).move_to([QVEC_X, ROW_YS[0], 0])
    mid_lbl = MathTex("4.6", color=MID).scale(1.4).move_to([QVEC_X, ROW_YS[1], 0])
    fine_lbl = MathTex("12.1", color=FINE).scale(1.4).move_to([QVEC_X, ROW_YS[2], 0])
    stack = VGroup(coarse_lbl, mid_lbl, fine_lbl)
    anchor = Rectangle(
        width=stack.width + 0.5,
        height=ROW_YS[0] - ROW_YS[-1] + 0.4,
        stroke_opacity=0,
        fill_opacity=0,
    ).move_to([QVEC_X, 0, 0])
    bracket = VGroup(Brace(anchor, LEFT), Brace(anchor, RIGHT))
    return VGroup(bracket, stack)


def _times_n_label(scale: int, anchor) -> VGroup:
    """`x N` label that sits above the 'rounded' arrow label, where N is the
    current iteration's scale factor."""
    return tex_text(f"x {scale}", font_size=28, color=FOREGROUND).next_to(
        anchor, UP, buff=0.15
    )


def _rounded_arrow() -> VGroup:
    # Curved (concave-down) arrow from above q_vec to above the numbers.
    # The "rounded" label sits above the arrow.
    arrow_y = 2.35
    start = [QVEC_X + 0.9, arrow_y, 0]
    end = [NUM_LABEL_X - 0.05, arrow_y, 0]
    arrow = CurvedArrow(
        start_point=start,
        end_point=end,
        color=FOREGROUND,
        stroke_width=4,
        angle=-1.0,
        tip_length=0.2,
    )
    label = tex_text("rounded", font_size=28, color=FOREGROUND).move_to(
        [(start[0] + end[0]) / 2, 3.05, 0]
    )
    return VGroup(arrow, label)


def _build_chart(counts: np.ndarray, scale: int | None = None) -> VGroup:
    """Build the cumulative chart. If `scale` is provided, the realized curve
    + dots + error band use the hand-tuned `ITER_PP[scale]` values; otherwise
    they're computed from `counts` via `_cum_passing`."""
    axes = _build_axes().move_to([CHART_X, -0.2, 0])
    realized_pp = ITER_PP[scale] if scale in ITER_PP else _cum_passing(counts)
    target = _smooth_curve(axes, TARGET_PP)
    realized = _stair_curve(axes, realized_pp, FOREGROUND)
    realized.set_stroke(width=3)
    band = _error_band(axes, TARGET_PP, realized_pp)
    dots = _sieve_dots(axes, realized_pp)
    x_lbl = tex_text("size", font_size=24, color=FOREGROUND).next_to(axes, DOWN, buff=0.1)
    # Mass label sits above the y-axis so it doesn't fight with the
    # spanned-integer column to the chart's left.
    y_lbl = tex_text("Mass", font_size=24, color=FOREGROUND).next_to(
        axes.y_axis.get_top(), UP, buff=0.05
    )
    return VGroup(axes, band, target, realized, dots, x_lbl, y_lbl)


def _error_magnitude_from_pp(pp: np.ndarray) -> float:
    """Sum of |realized - target| at the sieve points (excluding endpoints)."""
    return float(np.sum(np.abs(pp[1:-1] - TARGET_PP[1:-1])) + abs(pp[-1] - TARGET_PP[-1]))


# Precompute per-iteration error so the bar can scale to iter-1 = full height.
_ERRORS = [_error_magnitude_from_pp(ITER_PP[s]) for s in SCALES]
_ERR_REF = max(_ERRORS) if _ERRORS else 1.0
ERR_FRACS = [e / _ERR_REF for e in _ERRORS]


def _err_bar(frac: float) -> VGroup:
    """One-bar bar chart at ERR_BAR_X with height proportional to `frac`.
    Color is GREEN if frac is below the tolerance line, else RED."""
    bar_h = max(0.05, frac * ERR_BAR_HEIGHT)
    color = ERR_OK_COLOR if frac < TOLERANCE_FRAC else ERR_HIGH_COLOR
    bar = Rectangle(
        width=ERR_BAR_WIDTH,
        height=bar_h,
        color=color,
        fill_color=color,
        fill_opacity=0.7,
        stroke_width=2,
    )
    bar.move_to([ERR_BAR_X, ERR_BAR_BOTTOM_Y + bar_h / 2, 0])
    return VGroup(bar)


def _err_bar_frame() -> VGroup:
    """Static parts of the error-bar chart: baseline, tolerance line, label."""
    baseline = DashedLine(
        start=[ERR_BAR_X - ERR_BAR_WIDTH * 1.5, ERR_BAR_BOTTOM_Y, 0],
        end=[ERR_BAR_X + ERR_BAR_WIDTH * 1.5, ERR_BAR_BOTTOM_Y, 0],
        color=FOREGROUND,
        stroke_width=2,
        dash_length=0.06,
    )
    tol = DashedLine(
        start=[ERR_BAR_X - ERR_BAR_WIDTH * 2.0,
               ERR_BAR_BOTTOM_Y + TOLERANCE_FRAC * ERR_BAR_HEIGHT, 0],
        end=[ERR_BAR_X + ERR_BAR_WIDTH * 2.0,
             ERR_BAR_BOTTOM_Y + TOLERANCE_FRAC * ERR_BAR_HEIGHT, 0],
        color=WHITE,
        stroke_width=2,
        dash_length=0.08,
    )
    label = tex_text("error", font_size=22, color=FOREGROUND).move_to(
        [ERR_BAR_X, ERR_BAR_BOTTOM_Y - 0.3, 0]
    )
    return VGroup(baseline, tol, label)


class RoundingApproach(Scene):
    def construct(self):
        title = tex_text("Fixed size iteration", font_size=44, color=FOREGROUND).to_edge(
            UP, buff=0.3
        )

        rng = np.random.default_rng(7)
        counts = _round_match(SCALES[0])  # [1, 5, 12]

        ratio_vec = _quantity_ratio_vector()
        arrow = _rounded_arrow()
        times_n = _times_n_label(SCALES[0], arrow[1])
        datums = _datums()
        piles = _piles_with_counts(counts, rng)
        chart = _build_chart(counts, scale=SCALES[0])
        err_frame = _err_bar_frame()
        err_bar = _err_bar(ERR_FRACS[0])

        self.play(Write(title), run_time=0.5)
        self.play(
            FadeIn(ratio_vec),
            Create(arrow[0]),
            Write(arrow[1]),
            Write(times_n),
            run_time=0.7,
        )
        self.play(FadeIn(datums), FadeIn(piles), run_time=0.6)
        self.play(FadeIn(chart), FadeIn(err_frame), FadeIn(err_bar), run_time=0.9)
        self.wait(0.5)


class ReducingError(Scene):
    def construct(self):
        title = tex_text("Fixed size iteration", font_size=44, color=FOREGROUND).to_edge(
            UP, buff=0.3
        )

        # Seamless mode: QR teaser already left q_vec, arrow + "rounded",
        # iter-1 pile, and count labels on screen. Add only what's missing.
        seamless = hasattr(self, "_qr_q_vec")
        datums = _datums()
        err_frame = _err_bar_frame()

        if seamless:
            existing_pile = self._qr_pile
            existing_labels = self._qr_count_labels
            qr_title = getattr(self, "_qr_title", None)
            qr_q_vec = self._qr_q_vec
            qr_rounded_lbl = self._qr_rounded_lbl
            k_label = MathTex("K", color=FOREGROUND).scale(1.0).next_to(
                qr_q_vec, UP, buff=0.15
            )
            times_n = _times_n_label(SCALES[0], qr_rounded_lbl)
            fade_extra = [FadeOut(qr_title)] if qr_title is not None else []
            self.play(
                Write(title),
                *fade_extra,
                FadeIn(datums),
                FadeIn(err_frame),
                Write(k_label),
                Write(times_n),
                run_time=0.7,
            )
            self._re_k_label = k_label
        else:
            ratio_vec = _quantity_ratio_vector()
            arrow = _rounded_arrow()
            times_n = _times_n_label(SCALES[0], arrow[1])
            self.play(Write(title), run_time=0.5)
            self.play(
                FadeIn(datums),
                FadeIn(ratio_vec),
                Create(arrow[0]),
                Write(arrow[1]),
                Write(times_n),
                FadeIn(err_frame),
                run_time=0.7,
            )
            existing_pile = None
            existing_labels = None
        self._re_times_n_anchor = (
            qr_rounded_lbl if seamless else arrow[1]
        )

        prev_chart = None
        on_scene_bar = None
        prev_pile = existing_pile
        prev_labels = existing_labels
        rng_seed = 11
        for i, scale in enumerate(SCALES):
            rng = np.random.default_rng(rng_seed)
            rng_seed += 1
            counts = _round_match(scale)
            new_piles_with_labels = _piles_with_counts(counts, rng)
            # Split into pile particles and integer labels.
            new_pile = VGroup(*[row[0] for row in new_piles_with_labels])
            new_labels = VGroup(*[row[1] for row in new_piles_with_labels])
            chart = _build_chart(counts, scale=scale)
            err_bar = _err_bar(ERR_FRACS[i])

            if i == 0:
                # First iteration: in seamless mode the pile + labels already
                # exist (iter 1 = same numbers); just add chart + err_bar.
                if seamless:
                    self.play(FadeIn(chart), FadeIn(err_bar), run_time=0.7)
                else:
                    self.play(
                        FadeIn(new_pile),
                        FadeIn(new_labels),
                        FadeIn(chart),
                        FadeIn(err_bar),
                        run_time=0.7,
                    )
                    prev_pile = new_pile
                    prev_labels = new_labels
                on_scene_bar = err_bar
                prev_chart = chart
            else:
                new_times_n = _times_n_label(scale, self._re_times_n_anchor)
                self.play(
                    FadeOut(prev_pile),
                    FadeOut(prev_labels),
                    FadeIn(new_pile),
                    FadeIn(new_labels),
                    FadeOut(prev_chart),
                    FadeIn(chart),
                    Transform(on_scene_bar, err_bar),
                    Transform(times_n, new_times_n),
                    run_time=0.7,
                )
                prev_pile = new_pile
                prev_labels = new_labels
                prev_chart = chart
            self.wait(0.4)

        # Stash for SpannedIntegerApproach.
        self._re_title = title
        self._re_datums = datums
        self._re_pile = prev_pile
        self._re_labels = prev_labels
        self._re_chart = prev_chart
        self._re_err_frame = err_frame
        self._re_err_bar = on_scene_bar

        self.wait(0.5)
