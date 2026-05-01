"""Spanned-integer approach + MDM result.

Picks up the layout left by the Fixed-size-iteration scene (q_vec → arrow →
integer pile → cumulative chart → error bar) and animates:

  - reduce pile to one particle per tier (only the coarse "largest" stays);
  - mid + fine slide up to their bands' upper limits and grow → realized
    quantity ratios become K_+ = (1, 4.1, 11.8); error remains;
  - shift the pile right, add a K_- vector and a second mid + fine particle
    sliding to each band's lower limit (smaller); both curves on the chart
    show non-zero error;
  - spanned-integer reveal: large+small particles in each tier merge into a
    single intermediate-size particle whose size is proportional to where
    the integer falls between K_- and K_+; realized curve hits the target,
    error band collapses, error bar drops to zero;
  - MDM box + label.

Numbers: K_PLUS = (1, 4.1, 11.8), K_MINUS = (1, 6.8, 13.4),
spanned integers = (1, 5, 12) for [coarse, mid, fine].
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
    Brace,
    Create,
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

from _common import (
    BACKGROUND,
    COARSE,
    COARSE_R,
    FINE,
    FINE_R,
    FOREGROUND,
    MID,
    MID_R,
    make_particle,
    scatter_in_band,
)
from rounding import (
    ARROW_X,
    CHART_X,
    ERR_BAR_BOTTOM_Y,
    ERR_BAR_HEIGHT,
    ERR_BAR_WIDTH,
    ERR_BAR_X,
    ERR_FRACS,
    ERR_HIGH_COLOR,
    ERR_OK_COLOR,
    LEFT_X,
    NUM_LABEL_X,
    PILE_BAND_HEIGHT,
    QVEC_X,
    ROW_YS,
    SIEVE_XS,
    TARGET_PP,
    TOLERANCE_FRAC,
    _build_chart,
    _datums,
    _err_bar,
    _err_bar_frame,
    _piles_with_counts,
    _quantity_ratio_vector,
    _round_match,
    _rounded_arrow,
    _smooth_curve,
    _stair_curve,
    _sieve_dots,
    _build_axes,
)

config.background_color = BACKGROUND


# ---- Numbers (per manuscript) ----
# Order matches the q_vec rows: [coarse, mid, fine].
K_PLUS = (1.0, 4.1, 11.8)    # max-size end of each range (smaller ratio)
K_MINUS = (1.0, 6.8, 13.4)   # min-size end of each range (larger ratio)
SPANNED_INTEGERS_DISPLAY = (1, 5, 12)            # [coarse, mid, fine]
# _piles_with_counts expects [fine, mid, coarse]:
SPANNED_INTEGERS_FMC = np.array([12, 5, 1])


# ---- Sizes for each tier at the upper / lower limits of its size range. ----
# "Upper limit" = larger particle (smaller ratio). The merged spanned-integer
# size is placed proportionally between min and max based on where the
# integer count falls between K_- and K_+.
MID_R_HI, MID_R_LO = MID_R * 1.55, MID_R * 0.65
FINE_R_HI, FINE_R_LO = FINE_R * 1.55, FINE_R * 0.55


def _interp_radius(integer: int, k_plus: float, k_minus: float, r_hi: float, r_lo: float) -> float:
    """Pick a radius for the spanned integer particle: position 0 = max
    size end (k_plus), position 1 = min size end (k_minus)."""
    frac = float(np.clip((integer - k_plus) / max(k_minus - k_plus, 1e-9), 0, 1))
    return r_hi - frac * (r_hi - r_lo)


# Sizes used for the merged spanned-integer particles.
MID_R_SPAN = _interp_radius(SPANNED_INTEGERS_DISPLAY[1], K_PLUS[1], K_MINUS[1], MID_R_HI, MID_R_LO)
FINE_R_SPAN = _interp_radius(SPANNED_INTEGERS_DISPLAY[2], K_PLUS[2], K_MINUS[2], FINE_R_HI, FINE_R_LO)


# ---- Realized cumulative-passing for K_+ and K_- ratios. ----
PER_PARTICLE_MASS_3 = np.array([0.5, 1.0, 2.0]) ** 3  # [fine, mid, coarse]


def _pp_from_ratios(ratios_cmf: tuple[float, float, float]) -> np.ndarray:
    """Cumulative passing at sieves [pan, x_1, x_2, x_3] from quantity
    ratios in [coarse, mid, fine] order."""
    coarse, mid, fine = ratios_cmf
    counts = np.array([fine, mid, coarse])  # convert to [fine, mid, coarse]
    masses = counts * PER_PARTICLE_MASS_3
    total = masses.sum()
    return np.array([0.0, masses[0], masses[0] + masses[1], total]) / total


PP_KPLUS = _pp_from_ratios(K_PLUS)
PP_KMINUS = _pp_from_ratios(K_MINUS)


def _err_magnitude(pp: np.ndarray) -> float:
    return float(np.sum(np.abs(pp[1:-1] - TARGET_PP[1:-1])))


# Fractions for the error bar. Using the rounding scene's reference so the
# bars read on the same scale.
_ERR_REF = max(ERR_FRACS) * (1 / max(ERR_FRACS))  # = 1.0 at iter 1
ERR_FRAC_KPLUS = max(0.4, _err_magnitude(PP_KPLUS) / _err_magnitude(PP_KPLUS))  # placeholder; see below
# We want a non-zero (but visible) error for K_+ and K_-. The raw magnitudes
# are tiny relative to iter-1 of the rounding scene, so we display them at
# fixed visible fractions for clarity.
ERR_FRAC_KPLUS = 0.55
ERR_FRAC_KMINUS = 0.65
ERR_FRAC_SPANNED = 0.0


# Vertical offset of K_+ entries (above each tier row) vs K_- entries (below).
# Used for both the values inside the combined K_+/K_- bracket AND the
# particles in the sieve stack, so numbers and particles line up.
KVEC_Y_OFFSET = 0.30


def _combined_anchor_geom() -> tuple[float, float]:
    """(height, center_y) of the rectangle that the combined K_+/K_- bracket
    encloses: from above the coarse row down to below the fine K_- row."""
    top_y = ROW_YS[0] + 0.2
    bot_y = ROW_YS[-1] - KVEC_Y_OFFSET - 0.2
    return (top_y - bot_y, (top_y + bot_y) / 2)


def _fmt(v: float) -> str:
    return "1" if abs(v - 1.0) < 1e-9 else f"{v:.1f}"


def _kplus_entries(center_x: float) -> VGroup:
    """K_+ values: coarse at row center; mid + fine pushed UP."""
    return VGroup(
        MathTex(_fmt(K_PLUS[0]), color=COARSE).scale(1.4).move_to([center_x, ROW_YS[0], 0]),
        MathTex(_fmt(K_PLUS[1]), color=MID).scale(1.4).move_to(
            [center_x, ROW_YS[1] + KVEC_Y_OFFSET, 0]
        ),
        MathTex(_fmt(K_PLUS[2]), color=FINE).scale(1.4).move_to(
            [center_x, ROW_YS[2] + KVEC_Y_OFFSET, 0]
        ),
    )


def _kminus_entries(center_x: float) -> VGroup:
    """K_- values: mid + fine pushed DOWN. Coarse skipped (= K_+ coarse)."""
    return VGroup(
        MathTex(_fmt(K_MINUS[1]), color=MID).scale(1.4).move_to(
            [center_x, ROW_YS[1] - KVEC_Y_OFFSET, 0]
        ),
        MathTex(_fmt(K_MINUS[2]), color=FINE).scale(1.4).move_to(
            [center_x, ROW_YS[2] - KVEC_Y_OFFSET, 0]
        ),
    )


def _combined_bracket(center_x: float, ref_width: float) -> VGroup:
    h, cy = _combined_anchor_geom()
    anchor = Rectangle(
        width=ref_width + 0.3,
        height=h,
        stroke_opacity=0,
        fill_opacity=0,
    ).move_to([center_x, cy, 0])
    return VGroup(Brace(anchor, LEFT), Brace(anchor, RIGHT))


def _fmt(v: float) -> str:
    return "1" if abs(v - 1.0) < 1e-9 else f"{v:.1f}"


def _single_particle_pile(counts_cmf: tuple[int, int, int], radii: tuple[float, float, float], y_offsets: tuple[float, float, float], pile_x: float) -> VGroup:
    """Place exactly one particle per tier at the row y plus an offset, with
    custom radii — used for the K_+ / K_- visualization where we want full
    control over per-tier size and y-position."""
    pile = VGroup()
    coarse = make_particle(radii[0], COARSE).move_to([pile_x, ROW_YS[0] + y_offsets[0], 0])
    mid = make_particle(radii[1], MID).move_to([pile_x, ROW_YS[1] + y_offsets[1], 0])
    fine = make_particle(radii[2], FINE).move_to([pile_x, ROW_YS[2] + y_offsets[2], 0])
    pile.add(coarse, mid, fine)
    return pile


def _build_realized_curve(pp: np.ndarray, axes, color, width: float = 3) -> VMobject:
    return _stair_curve(axes, pp, color).set_stroke(width=width)


class SpannedIntegerApproach(Scene):
    def construct(self):
        # Seamless mode: pull state from ReducingError (iter 3 layout already
        # on screen). Otherwise build everything fresh.
        seamless = hasattr(self, "_re_pile")

        if seamless:
            title = self._re_title
            ratio_vec = self._qr_q_vec
            arrow = self._qr_arrow
            rounded_lbl = self._qr_rounded_lbl
            datums = self._re_datums
            chart = self._re_chart
            err_frame = self._re_err_frame
            err_bar_init = self._re_err_bar
            piles_init = self._re_pile
            labels_init = self._re_labels

            # De-clutter for the spanned-integer view: drop the arrow,
            # "rounded" label, and per-tier integer labels (those will
            # reappear inside the spanned-integer vector later).
            new_title = Text(
                "Spanned-integer approach",
                font_size=32,
                color=FOREGROUND,
            ).to_edge(UP, buff=0.3)
            self.play(
                Transform(title, new_title),
                FadeOut(arrow),
                FadeOut(rounded_lbl),
                FadeOut(labels_init),
                run_time=0.6,
            )
        else:
            title = Text(
                "Spanned-integer approach",
                font_size=32,
                color=FOREGROUND,
            ).to_edge(UP, buff=0.3)
            rng = np.random.default_rng(7)
            counts1 = _round_match(1)
            ratio_vec = _quantity_ratio_vector()
            arrow_grp = _rounded_arrow()
            arrow = arrow_grp[0]
            rounded_lbl = arrow_grp[1]
            datums = _datums()
            piles_with_labels = _piles_with_counts(counts1, rng)
            piles_init = VGroup(*[row[0] for row in piles_with_labels])
            labels_init = VGroup(*[row[1] for row in piles_with_labels])
            chart = _build_chart(counts1, scale=1)
            err_frame = _err_bar_frame()
            err_bar_init = _err_bar(ERR_FRACS[0])
            self.add(
                title, ratio_vec, arrow, rounded_lbl, datums,
                piles_init, labels_init, chart, err_frame, err_bar_init,
            )
            self.wait(0.6)

        # ---- Beat 2: collapse pile to one of each tier with K_+ sizes high;
        # q_vec entries morph to K_+ values (coarse at row center, mid + fine
        # pushed UP); bracket grows to the combined K_+/K_- final extent;
        # "K" label morphs to "K_+"; chart + err_bar update.
        pile_x = LEFT_X
        # Particles aligned to numbers — same y offsets as K_+ entries.
        single_hi = _single_particle_pile(
            (1, 1, 1),
            (COARSE_R, MID_R_HI, FINE_R_HI),
            (0, KVEC_Y_OFFSET, KVEC_Y_OFFSET),  # coarse center; mid+fine UP
            pile_x,
        )

        kplus_entries = _kplus_entries(QVEC_X)
        combined_bracket = _combined_bracket(QVEC_X, ref_width=kplus_entries.width)
        kplus_label = MathTex("K_+", color=FOREGROUND).scale(0.9).next_to(
            combined_bracket[0], UP, buff=0.15
        )

        axes = chart[0]
        kplus_curve = _build_realized_curve(PP_KPLUS, axes, MID, width=3)
        kplus_dots = _sieve_dots(axes, PP_KPLUS).set_color(MID)
        old_realized = chart[3]
        old_dots = chart[4]
        old_band = chart[1]

        err_bar_kplus = _err_bar(ERR_FRAC_KPLUS)

        # ratio_vec is VGroup(LEFT_brace, stack, RIGHT_brace).
        existing_k_label = getattr(self, "_re_k_label", None)
        anims = [
            FadeOut(piles_init),
            FadeIn(single_hi),
            Transform(ratio_vec[0], combined_bracket[0]),
            Transform(ratio_vec[1], kplus_entries),
            Transform(ratio_vec[2], combined_bracket[1]),
            Transform(old_realized, kplus_curve),
            Transform(old_dots, kplus_dots),
            FadeOut(old_band),
            Transform(err_bar_init, err_bar_kplus),
        ]
        if existing_k_label is not None:
            anims.append(Transform(existing_k_label, kplus_label))
        else:
            anims.append(FadeIn(kplus_label))
            self._re_k_label = kplus_label
        self.play(*anims, run_time=1.5)
        self.wait(0.4)

        # ---- Beat 3: K_- entries fill the lower half of the same bracket;
        # small mid + small fine particles appear at the K_- y-positions
        # (DOWN), aligned with the K_- numbers. ----
        small_mid = make_particle(MID_R_LO, MID).move_to(
            [pile_x, ROW_YS[1] - KVEC_Y_OFFSET, 0]
        )
        small_fine = make_particle(FINE_R_LO, FINE).move_to(
            [pile_x, ROW_YS[2] - KVEC_Y_OFFSET, 0]
        )
        small_particles = VGroup(small_mid, small_fine)

        kminus_entries = _kminus_entries(QVEC_X)
        kminus_label = MathTex("K_-", color=FOREGROUND).scale(0.9).next_to(
            combined_bracket[0], DOWN, buff=0.15
        )

        err_bar_kminus = _err_bar(ERR_FRAC_KMINUS)

        # K_- realized curve on the chart.
        kminus_curve = _build_realized_curve(PP_KMINUS, axes, COARSE, width=3)
        kminus_dots = _sieve_dots(axes, PP_KMINUS).set_color(COARSE)

        self.play(
            FadeIn(kminus_entries),
            FadeIn(kminus_label),
            FadeIn(small_particles),
            FadeIn(kminus_curve),
            FadeIn(kminus_dots),
            Transform(err_bar_init, err_bar_kminus),
            run_time=1.6,
        )
        self.wait(0.6)

        # Stash for the SpannedIntegerError handoff.
        self.title_mob = title
        self.large_pile = single_hi
        self.small_particles = small_particles
        self.chart_mob = chart
        self.kplus_curve = old_realized  # transformed to kplus_curve
        self.kplus_dots = old_dots
        self.kminus_curve = kminus_curve
        self.kminus_dots = kminus_dots
        self.err_frame_mob = err_frame
        self.err_bar_mob = err_bar_init
        self.pile_x = pile_x


class SpannedIntegerError(Scene):
    def construct(self):
        # Pulls everything from the previous scene's stash via shared `self`
        # when stitched in FullStory. Otherwise (standalone) renders a brief
        # static MDM result.
        if not getattr(self, "title_mob", None):
            # Standalone fallback: just label the result.
            label = Text(
                "Minimal Discrete Match",
                font_size=32,
                color=COARSE,
            )
            self.play(Write(label), run_time=0.7)
            self.wait(2.0)
            return

        # ---- Beat 4: spanned-integer reveal: large+small particles in each
        # tier merge into a single intermediate-size particle whose size is
        # proportional to where the integer falls between K_+ and K_-.
        # Realized curve hits target, error → 0. ----
        title = self.title_mob
        chart = self.chart_mob
        axes = chart[0]
        large_pile = self.large_pile
        small_particles = self.small_particles
        pile_x = self.pile_x

        # Merged particles: y position interpolated proportionally between
        # K_+ (high) and K_- (low) by the integer's position in the span.
        mid_frac = float(np.clip((SPANNED_INTEGERS_DISPLAY[1] - K_PLUS[1]) /
                                 max(K_MINUS[1] - K_PLUS[1], 1e-9), 0, 1))
        fine_frac = float(np.clip((SPANNED_INTEGERS_DISPLAY[2] - K_PLUS[2]) /
                                  max(K_MINUS[2] - K_PLUS[2], 1e-9), 0, 1))
        mid_merged_y = ROW_YS[1] + KVEC_Y_OFFSET + mid_frac * (-2 * KVEC_Y_OFFSET)
        fine_merged_y = ROW_YS[2] + KVEC_Y_OFFSET + fine_frac * (-2 * KVEC_Y_OFFSET)

        merged_mid = make_particle(MID_R_SPAN, MID).move_to([pile_x, mid_merged_y, 0])
        merged_fine = make_particle(FINE_R_SPAN, FINE).move_to([pile_x, fine_merged_y, 0])

        # Spanned-integer column between the particle stack and the chart.
        span_x = 0.5
        span_title = Text("Spanned\nintegers", font_size=18, color=COARSE).move_to(
            [span_x, ROW_YS[0] + 1.0, 0]
        )
        span_labels = VGroup(
            Text("1", font_size=56, color=COARSE).move_to([span_x, ROW_YS[0], 0]),
            Text("5", font_size=56, color=MID).move_to([span_x, mid_merged_y, 0]),
            Text("12", font_size=56, color=FINE).move_to([span_x, fine_merged_y, 0]),
        )
        span_anchor = Rectangle(
            width=span_labels.width + 0.3,
            height=ROW_YS[0] - ROW_YS[-1] + 2 * KVEC_Y_OFFSET + 0.3,
            stroke_opacity=0,
            fill_opacity=0,
        ).move_to([span_x, 0, 0])
        span_brace = VGroup(Brace(span_anchor, LEFT), Brace(span_anchor, RIGHT))

        # Realized curve becomes the target (zero error).
        target_overlay = _smooth_curve(axes, TARGET_PP).set_stroke(
            color=FOREGROUND, width=4
        )
        target_dots = _sieve_dots(axes, TARGET_PP).set_color(WHITE)
        err_bar_zero = _err_bar(ERR_FRAC_SPANNED)

        # Move the large mid → merged_mid position/size; small mid → same
        # target. Same for fine.
        self.play(
            # Merge mid pair.
            Transform(large_pile[1], merged_mid),
            Transform(small_particles[0], merged_mid.copy()),
            # Merge fine pair.
            Transform(large_pile[2], merged_fine),
            Transform(small_particles[1], merged_fine.copy()),
            # Bring spanned integer column in.
            FadeIn(span_brace),
            FadeIn(span_labels),
            Write(span_title),
            # Chart: realized → target, error band → 0.
            Transform(self.kplus_curve, target_overlay),
            Transform(self.kminus_curve, target_overlay.copy()),
            FadeOut(self.kplus_dots),
            FadeOut(self.kminus_dots),
            FadeIn(target_dots),
            Transform(self.err_bar_mob, err_bar_zero),
            run_time=1.8,
        )
        self.wait(0.6)

        # ---- Beat 5: MDM box + label. ----
        result = VGroup(span_brace, span_labels, large_pile, small_particles)
        box = Rectangle(
            width=result.width + 0.7,
            height=result.height + 0.7,
            color=COARSE,
            stroke_width=3,
        ).move_to(result.get_center())
        mdm_label = Text(
            "Minimal Discrete Match",
            font_size=28,
            color=COARSE,
        ).next_to(box, DOWN, buff=0.25)

        self.play(FadeIn(box), Write(mdm_label), run_time=1.0)
        self.wait(5.0)
