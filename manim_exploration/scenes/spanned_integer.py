"""Spanned-integer approach + MDM result.

Six-beat structure (high-school / general audience). The visual must TELL
the story, not prove the algorithm.

  Beat 0: Carry-over cleanup. Title swaps to "Spanned-integer approach".
          Fade out the multi-particle pile, big count labels, the curved
          arrow + "rounded" label, and the "x N" multiplier. Replace the
          pile with ONE midrange-sized representative particle per tier.
          Chart and error bar reset to a "moderate" error.

  Beat 1: Particles GROW to the largest size in each band -> K_+. Mid +
          fine particles end up TANGENT to their upper sieve datum lines.
          K-vector morphs to K_+ values (1, 4.1, 11.8), all shifted LEFT
          inside a wider bracket; K_+ label appears above-left. Realized
          curve drops below target; error bar grows red.

  Beat 2: SHRINK companion: smaller particles appear TANGENT to the
          lower sieve datums. K_- values (6.8, 13.4) fade in on the
          RIGHT column of the same wider bracket; K_- label below-right.
          Second realized curve appears above target.

  Beat 3: STANDALONE BINGO reveal. Spanned integers (1, 5, 12) pop in
          (0.6x->1.4x->1.0x) in YELLOW, just outside the bracket on
          the right at y-positions proportional to where each integer
          sits between K_+ and K_- particle y. Caption: "A whole number
          is between them!"

  Beat 4: Resolution. The two particles per tier merge into a single
          intermediate-size particle at the integer's y. Both realized
          curves fade out and the target curve appears; white dots land
          ON the smoothed curve. Error bar -> 0.

  Beat 5: K_+/K_- entries + bracket + labels FADE. The MDM box hugs
          the spanned-integer column + merged-particle column; red
          "Minimal Discrete Match" label below; particle-count subtitle.

Numbers (per manuscript): K_+ = (1, 4.1, 11.8), K_- = (1, 6.8, 13.4),
spanned integers = (1, 5, 12), in [coarse, mid, fine] order.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    WHITE,
    YELLOW,
    Brace,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    Rectangle,
    Scene,
    Tex,
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
    tex_text,
)
from rounding import (
    CHART_X,
    ERR_BAR_BOTTOM_Y,
    ERR_BAR_HEIGHT,
    ERR_BAR_X,
    ERR_FRACS,
    LEFT_X,
    NUM_LABEL_X,
    PILE_BAND_HEIGHT,
    PILE_X_RANGE,
    QVEC_X,
    ROW_YS,
    SIEVE_XS,
    TARGET_PP,
    _build_chart,
    _datums,
    _err_bar,
    _err_bar_frame,
    _error_band,
    _piles_with_counts,
    _quantity_ratio_vector,
    _round_match,
    _rounded_arrow,
    _smooth_curve,
    _stair_curve,
    _sieve_dots,
    smoothed_pp_at_sieves,
)

config.background_color = BACKGROUND


# ---- Numbers (per manuscript) ----
# Order matches the q_vec rows: [coarse, mid, fine].
K_PLUS = (1.0, 4.1, 11.8)             # max-size end of each range
K_MINUS = (1.0, 6.8, 13.4)            # min-size end of each range
Q_VEC_MID = (1.0, 4.6, 12.1)          # midrange (= original quantity ratio)
SPANNED_INTEGERS_DISPLAY = (1, 5, 12) # [coarse, mid, fine]


# ---- Per-tier radii at HI / LO / MID of each sieve interval. ----
MID_R_HI, MID_R_LO = MID_R * 1.55, MID_R * 0.65
MID_R_MID = (MID_R_HI + MID_R_LO) / 2
FINE_R_HI, FINE_R_LO = FINE_R * 1.55, FINE_R * 0.55
FINE_R_MID = (FINE_R_HI + FINE_R_LO) / 2


# ---- Sieve datum y values (must mirror _datums() in rounding.py). ----
DATUM_TOP = ROW_YS[0] + PILE_BAND_HEIGHT / 2 + 0.3        # 2.6 (above coarse)
DATUM_COARSE_MID = (ROW_YS[0] + ROW_YS[1]) / 2            # 0.9 (between coarse + mid)
DATUM_MID_FINE = (ROW_YS[1] + ROW_YS[2]) / 2              # -0.9 (between mid + fine)
DATUM_BOT = ROW_YS[-1] - PILE_BAND_HEIGHT / 2 - 0.3       # -2.6 (below fine)


# ---- Tangent particle y-positions (ON the sieve lines). ----
# Particle CENTER = datum ± radius. K_+ particle is tangent to upper datum,
# K_- particle to lower datum. Coarse uses row center (no HI/LO defined).
COARSE_PILE_Y = ROW_YS[0]
MID_KPLUS_PILE_Y = DATUM_COARSE_MID - MID_R_HI
MID_KMINUS_PILE_Y = DATUM_MID_FINE + MID_R_LO
FINE_KPLUS_PILE_Y = DATUM_MID_FINE - FINE_R_HI
FINE_KMINUS_PILE_Y = DATUM_BOT + FINE_R_LO


def _interp_radius(integer: int, k_plus: float, k_minus: float,
                   r_hi: float, r_lo: float) -> float:
    """Pick a radius for the merged spanned-integer particle: position 0 =
    max-size end (k_plus), position 1 = min-size end (k_minus)."""
    frac = float(np.clip((integer - k_plus) / max(k_minus - k_plus, 1e-9), 0, 1))
    return r_hi - frac * (r_hi - r_lo)


MID_R_SPAN = _interp_radius(SPANNED_INTEGERS_DISPLAY[1], K_PLUS[1], K_MINUS[1],
                            MID_R_HI, MID_R_LO)
FINE_R_SPAN = _interp_radius(SPANNED_INTEGERS_DISPLAY[2], K_PLUS[2], K_MINUS[2],
                             FINE_R_HI, FINE_R_LO)


# ---- Hand-tuned realized cumulative-passing per beat. ----
# Format: [pan, fine_dot, mid_dot, coarse_dot]. Target is approx
# [0, 0.107, 0.433, 1.0]. We exaggerate small mathematical differences
# for pedagogical clarity (matching the rounding scene's style).
PP_BEAT0 = np.array([0.0, 0.13, 0.50, 0.96])    # midrange: slight overshoot
PP_KPLUS = np.array([0.0, 0.05, 0.27, 0.85])    # large size: under target
PP_KMINUS = np.array([0.0, 0.20, 0.62, 1.0])    # small size: over target


# ---- Error bar fractions (visual scale, 0=zero, 1=max). ----
ERR_FRAC_BEAT0 = 0.35
ERR_FRAC_KPLUS = 0.55
ERR_FRAC_KMINUS = 0.65
ERR_FRAC_SPANNED = 0.0


# ---- K vector layout — horizontal: K_+ LEFT, K_- RIGHT. ----
# Entries stay at fixed y-offsets from row centers (≠ particle tangent
# positions). Decoupling is intentional: the entries must fit cleanly
# inside each tier's band, while particles sit precisely on the datum.
KVEC_Y_OFFSET = 0.45
K_VEC_X_OFFSET = 0.55                 # K_+ / K_- column offset from QVEC_X
KPLUS_X = QVEC_X - K_VEC_X_OFFSET     # ~ -5.75
KMINUS_X = QVEC_X + K_VEC_X_OFFSET    # ~ -4.65
BRACKET_HALF_WIDTH = 1.05             # bracket extends ±this from QVEC_X


# ---- Caption position + style. ----
CAPTION_Y = -3.05
CAPTION_FONT = 30
CAPTION_FONT_BIG = 38


# ---- Spanned-integer column (outside bracket on the right). ----
SPAN_X = QVEC_X + 1.7                 # ~ -3.5
INTEGER_FONT = 70


def _spanned_integer_y_positions() -> tuple[float, float, float]:
    """Y for each spanned integer. Coarse: row center (K_+ = K_-). Mid /
    fine: visually proportional between K_+ and K_- *particle* y based on
    where the integer falls between K_+ and K_-. The merged particle in
    Beat 4 lands at this same y, so integer + particle stay aligned."""
    mid_frac = float(np.clip(
        (SPANNED_INTEGERS_DISPLAY[1] - K_PLUS[1])
        / max(K_MINUS[1] - K_PLUS[1], 1e-9), 0, 1
    ))
    fine_frac = float(np.clip(
        (SPANNED_INTEGERS_DISPLAY[2] - K_PLUS[2])
        / max(K_MINUS[2] - K_PLUS[2], 1e-9), 0, 1
    ))
    mid_y = MID_KPLUS_PILE_Y - mid_frac * (MID_KPLUS_PILE_Y - MID_KMINUS_PILE_Y)
    fine_y = FINE_KPLUS_PILE_Y - fine_frac * (FINE_KPLUS_PILE_Y - FINE_KMINUS_PILE_Y)
    return (COARSE_PILE_Y, mid_y, fine_y)


def _bracket_geom() -> tuple[float, float, float]:
    """(width, height, center_y) of the wider K_+/K_- horizontal-layout
    bracket. Fixed enclosing rectangle that covers both K_+ entries (top
    half, mid+fine pushed UP) and K_- entries (bottom half, mid+fine pushed
    DOWN), with a small margin."""
    top_y = ROW_YS[0] + 0.2
    bot_y = ROW_YS[-1] - KVEC_Y_OFFSET - 0.2
    return (2 * BRACKET_HALF_WIDTH, top_y - bot_y, (top_y + bot_y) / 2)


def _wider_bracket(center_x: float) -> VGroup:
    width, height, cy = _bracket_geom()
    anchor = Rectangle(
        width=width,
        height=height,
        stroke_opacity=0,
        fill_opacity=0,
    ).move_to([center_x, cy, 0])
    return VGroup(Brace(anchor, LEFT), Brace(anchor, RIGHT))


def _fmt(v: float) -> str:
    return "1" if abs(v - 1.0) < 1e-9 else f"{v:.1f}"


def _kplus_entries() -> VGroup:
    """K_+ values (coarse, mid, fine) in the LEFT column of the bracket.
    Mid + fine are pushed UP by KVEC_Y_OFFSET; coarse on its row center."""
    return VGroup(
        MathTex(_fmt(K_PLUS[0]), color=COARSE).scale(1.4).move_to(
            [KPLUS_X, ROW_YS[0], 0]
        ),
        MathTex(_fmt(K_PLUS[1]), color=MID).scale(1.4).move_to(
            [KPLUS_X, ROW_YS[1] + KVEC_Y_OFFSET, 0]
        ),
        MathTex(_fmt(K_PLUS[2]), color=FINE).scale(1.4).move_to(
            [KPLUS_X, ROW_YS[2] + KVEC_Y_OFFSET, 0]
        ),
    )


def _kminus_entries() -> VGroup:
    """K_- values (mid, fine) in the RIGHT column of the bracket. Pushed
    DOWN by KVEC_Y_OFFSET. Coarse is skipped (K_+ = K_- = 1)."""
    return VGroup(
        MathTex(_fmt(K_MINUS[1]), color=MID).scale(1.4).move_to(
            [KMINUS_X, ROW_YS[1] - KVEC_Y_OFFSET, 0]
        ),
        MathTex(_fmt(K_MINUS[2]), color=FINE).scale(1.4).move_to(
            [KMINUS_X, ROW_YS[2] - KVEC_Y_OFFSET, 0]
        ),
    )


def _kplus_label() -> VMobject:
    """K_+ label, anchored above the LEFT column."""
    width, height, cy = _bracket_geom()
    top_y = cy + height / 2
    return MathTex("K_+", color=FOREGROUND).scale(1.2).move_to(
        [KPLUS_X, top_y + 0.35, 0]
    )


def _kminus_label() -> VMobject:
    """K_- label, anchored below the RIGHT column."""
    width, height, cy = _bracket_geom()
    bot_y = cy - height / 2
    return MathTex("K_-", color=FOREGROUND).scale(1.2).move_to(
        [KMINUS_X, bot_y - 0.35, 0]
    )


def _single_particle_pile(radii: tuple[float, float, float],
                          ys: tuple[float, float, float],
                          pile_x: float) -> VGroup:
    """One particle per tier at (pile_x, ys[i]) with the given radii.
    Order: coarse, mid, fine."""
    return VGroup(
        make_particle(radii[0], COARSE).move_to([pile_x, ys[0], 0]),
        make_particle(radii[1], MID).move_to([pile_x, ys[1], 0]),
        make_particle(radii[2], FINE).move_to([pile_x, ys[2], 0]),
    )


def _build_realized_curve(pp: np.ndarray, axes, color, width: float = 3) -> VMobject:
    return _stair_curve(axes, pp, color).set_stroke(width=width)


def _build_caption(text: str, big: bool = False, color=FOREGROUND) -> VMobject:
    """Captions may contain LaTeX math (`$...$`); use Tex directly so command
    sequences like ``\\to`` aren't escaped to text."""
    fs = CAPTION_FONT_BIG if big else CAPTION_FONT
    return Tex(text, font_size=fs, color=color).move_to([0, CAPTION_Y, 0])


class SpannedIntegerApproach(Scene):
    def construct(self):
        seamless = hasattr(self, "_re_pile")

        # ---- Pull state from previous scene OR build fresh. ----
        if seamless:
            title = self._re_title
            ratio_vec = self._qr_q_vec  # [LEFT_brace, stack, RIGHT_brace]
            old_pile = self._re_pile
            old_labels = self._re_labels
            old_arrow = self._qr_arrow
            old_rounded_lbl = self._qr_rounded_lbl
            old_times_n = getattr(self, "_re_times_n", None)
            old_chart = self._re_chart
            old_err_bar = self._re_err_bar
            existing_k_label = getattr(self, "_re_k_label", None)
        else:
            # Standalone: build the iter-3 layout (matching ReducingError end).
            title = tex_text(
                "Fixed size iteration", font_size=44, color=FOREGROUND,
            ).to_edge(UP, buff=0.3)
            rng = np.random.default_rng(13)
            counts3 = _round_match(3)
            ratio_vec_2 = _quantity_ratio_vector()
            ratio_vec = VGroup(ratio_vec_2[0][0], ratio_vec_2[1], ratio_vec_2[0][1])
            arrow_grp = _rounded_arrow()
            old_arrow = arrow_grp[0]
            old_rounded_lbl = arrow_grp[1]
            old_times_n = tex_text("x 3", font_size=28, color=FOREGROUND).next_to(
                old_rounded_lbl, UP, buff=0.15
            )
            piles_with_labels = _piles_with_counts(counts3, rng)
            old_pile = VGroup(*[row[0] for row in piles_with_labels])
            old_labels = VGroup(*[row[1] for row in piles_with_labels])
            old_chart = _build_chart(counts3, scale=3)
            err_frame = _err_bar_frame()
            old_err_bar = _err_bar(ERR_FRACS[2])
            existing_k_label = MathTex("K", color=FOREGROUND).scale(1.0).next_to(
                ratio_vec, UP, buff=0.15
            )
            datums = _datums()
            self.add(
                title, ratio_vec, old_arrow, old_rounded_lbl, old_times_n,
                datums, old_pile, old_labels, old_chart, err_frame, old_err_bar,
                existing_k_label,
            )
            self.wait(0.3)

        axes = old_chart[0]
        chart_band = old_chart[1]
        chart_realized = old_chart[3]
        chart_dots = old_chart[4]

        # =========================================================
        # Beat 0 — Carry-over cleanup (~0.6 s)
        # =========================================================
        new_title = tex_text(
            "Spanned-integer approach", font_size=44, color=FOREGROUND,
        ).to_edge(UP, buff=0.3)

        single_mid_pile = _single_particle_pile(
            (COARSE_R, MID_R_MID, FINE_R_MID),
            (ROW_YS[0], ROW_YS[1], ROW_YS[2]),
            LEFT_X,
        )

        beat0_realized = _stair_curve(axes, PP_BEAT0, FOREGROUND).set_stroke(width=3)
        beat0_dots = _sieve_dots(axes, PP_BEAT0)
        beat0_band = _error_band(axes, TARGET_PP, PP_BEAT0)
        beat0_err_bar = _err_bar(ERR_FRAC_BEAT0)

        cleanup = [
            Transform(title, new_title),
            FadeOut(old_pile),
            FadeOut(old_labels),
            FadeOut(old_arrow),
            FadeOut(old_rounded_lbl),
            FadeIn(single_mid_pile),
            Transform(chart_band, beat0_band),
            Transform(chart_realized, beat0_realized),
            Transform(chart_dots, beat0_dots),
            Transform(old_err_bar, beat0_err_bar),
        ]
        if old_times_n is not None:
            cleanup.append(FadeOut(old_times_n))
        self.play(*cleanup, run_time=0.6)
        self.wait(0.4)

        # =========================================================
        # Beat 1 — Particles GROW to K_+ tangent positions (~1.5 s)
        # =========================================================
        # K_+ particles tangent to UPPER sieve datum.
        kplus_pile = _single_particle_pile(
            (COARSE_R, MID_R_HI, FINE_R_HI),
            (COARSE_PILE_Y, MID_KPLUS_PILE_Y, FINE_KPLUS_PILE_Y),
            LEFT_X,
        )
        kplus_entries = _kplus_entries()
        wider_bracket = _wider_bracket(QVEC_X)
        kplus_label = _kplus_label()

        kplus_curve = _build_realized_curve(PP_KPLUS, axes, MID, width=3)
        kplus_dots_chart = _sieve_dots(axes, PP_KPLUS).set_color(MID)
        kplus_err_bar = _err_bar(ERR_FRAC_KPLUS)

        caption_kplus = _build_caption(
            r"Use the LARGEST size in each range $\to K_+$"
        )

        beat1_anims = [
            Transform(single_mid_pile, kplus_pile),
            Transform(ratio_vec[0], wider_bracket[0]),
            Transform(ratio_vec[1], kplus_entries),
            Transform(ratio_vec[2], wider_bracket[1]),
            Transform(chart_realized, kplus_curve),
            Transform(chart_dots, kplus_dots_chart),
            FadeOut(chart_band),
            Transform(old_err_bar, kplus_err_bar),
            FadeIn(caption_kplus),
        ]
        if existing_k_label is not None:
            beat1_anims.append(Transform(existing_k_label, kplus_label))
        else:
            existing_k_label = kplus_label
            beat1_anims.append(FadeIn(kplus_label))
        self.play(*beat1_anims, run_time=1.5)
        self.wait(0.5)

        # =========================================================
        # Beat 2 — SHRINK companion: K_- tangent to lower datum (~1.5 s)
        # =========================================================
        # K_- particles tangent to LOWER sieve datum.
        small_mid = make_particle(MID_R_LO, MID).move_to(
            [LEFT_X, MID_KMINUS_PILE_Y, 0]
        )
        small_fine = make_particle(FINE_R_LO, FINE).move_to(
            [LEFT_X, FINE_KMINUS_PILE_Y, 0]
        )
        small_particles = VGroup(small_mid, small_fine)

        kminus_entries = _kminus_entries()
        kminus_label = _kminus_label()

        kminus_curve = _build_realized_curve(PP_KMINUS, axes, COARSE, width=3)
        kminus_dots_chart = _sieve_dots(axes, PP_KMINUS).set_color(COARSE)
        kminus_err_bar = _err_bar(ERR_FRAC_KMINUS)

        caption_kminus = _build_caption(
            r"Use the SMALLEST size $\to K_-$"
        )

        self.play(
            FadeOut(caption_kplus),
            FadeIn(small_particles),
            FadeIn(kminus_entries),
            FadeIn(kminus_label),
            FadeIn(kminus_curve),
            FadeIn(kminus_dots_chart),
            Transform(old_err_bar, kminus_err_bar),
            FadeIn(caption_kminus),
            run_time=1.5,
        )
        self.wait(0.6)

        # =========================================================
        # Beat 3 — STANDALONE BINGO reveal (~2 s)
        # NOTHING else moves on screen during this beat.
        # =========================================================
        coarse_y, mid_y, fine_y = _spanned_integer_y_positions()

        coarse_int = tex_text(
            str(SPANNED_INTEGERS_DISPLAY[0]), font_size=INTEGER_FONT, color=YELLOW,
        ).move_to([SPAN_X, coarse_y, 0])
        mid_int = tex_text(
            str(SPANNED_INTEGERS_DISPLAY[1]), font_size=INTEGER_FONT, color=YELLOW,
        ).move_to([SPAN_X, mid_y, 0])
        fine_int = tex_text(
            str(SPANNED_INTEGERS_DISPLAY[2]), font_size=INTEGER_FONT, color=YELLOW,
        ).move_to([SPAN_X, fine_y, 0])
        integers = VGroup(coarse_int, mid_int, fine_int)

        caption_bingo = _build_caption(
            "A whole number is between them!", big=True, color=YELLOW,
        )

        # First fade out the prior caption on its own.
        self.play(FadeOut(caption_kminus), run_time=0.3)

        # Pop integers (0.6x -> 1.4x -> 1.0x) in two short plays. The notes
        # require this beat to land alone — do NOT couple to the merge.
        for integer in integers:
            integer.scale(0.6)
            integer.set_opacity(0)
        self.add(integers)
        self.play(
            FadeIn(caption_bingo),
            *[integer.animate.set_opacity(1).scale(1.4 / 0.6)
              for integer in integers],
            run_time=0.35,
        )
        self.play(
            *[integer.animate.scale(1.0 / 1.4) for integer in integers],
            run_time=0.2,
        )
        self.wait(2.0)  # let the audience feel the click

        # ---- Stash everything Beat 4 / 5 will need. ----
        self.title_mob = title
        self.large_pile = single_mid_pile  # has been transformed to kplus_pile
        self.small_particles = small_particles
        self.chart_mob = old_chart
        self.kplus_curve = chart_realized   # transformed to kplus_curve
        self.kplus_dots = chart_dots        # transformed to kplus_dots
        self.kminus_curve = kminus_curve
        self.kminus_dots = kminus_dots_chart
        self.err_bar_mob = old_err_bar
        self.integers_mob = integers
        self.caption_bingo_mob = caption_bingo
        self.kplus_label_mob = existing_k_label  # transformed to K_+
        self.kminus_label_mob = kminus_label
        self.kplus_entries_mob = ratio_vec[1]   # transformed to kplus_entries
        self.kminus_entries_mob = kminus_entries
        self.bracket_mob = VGroup(ratio_vec[0], ratio_vec[2])
        self.pile_x = LEFT_X


class SpannedIntegerCombined(Scene):
    """Approach + Error combined into one scene — useful when rendering as
    a single standalone clip (e.g. for the per-scene revealjs slideshow)."""
    def construct(self):
        SpannedIntegerApproach.construct(self)
        SpannedIntegerError.construct(self)


class SpannedIntegerError(Scene):
    def construct(self):
        # Standalone fallback: just label the result.
        if not getattr(self, "title_mob", None):
            label = tex_text(
                "Minimal Discrete Match", font_size=44, color=COARSE,
            )
            self.play(Write(label), run_time=0.7)
            self.wait(2.0)
            return

        title = self.title_mob
        chart = self.chart_mob
        axes = chart[0]
        large_pile = self.large_pile
        small_particles = self.small_particles
        pile_x = self.pile_x
        caption_bingo = self.caption_bingo_mob

        coarse_y, mid_y, fine_y = _spanned_integer_y_positions()

        # =========================================================
        # Beat 4 — Resolution (~1.5 s)
        # =========================================================
        # MDM pile: actual integer counts (1 coarse, 5 mid, 12 fine) at
        # intermediate (spanned) sizes, scattered in their respective bands.
        mdm_rng = np.random.default_rng(91)
        mid_band = (DATUM_MID_FINE, DATUM_COARSE_MID)
        fine_band = (DATUM_BOT, DATUM_MID_FINE)
        coarse_band = (DATUM_COARSE_MID, DATUM_TOP)
        mdm_coarse = scatter_in_band(
            SPANNED_INTEGERS_DISPLAY[0], COARSE_R, COARSE,
            coarse_band, PILE_X_RANGE, mdm_rng,
        )
        mdm_mid = scatter_in_band(
            SPANNED_INTEGERS_DISPLAY[1], MID_R_SPAN, MID,
            mid_band, PILE_X_RANGE, mdm_rng,
        )
        mdm_fine = scatter_in_band(
            SPANNED_INTEGERS_DISPLAY[2], FINE_R_SPAN, FINE,
            fine_band, PILE_X_RANGE, mdm_rng,
        )
        mdm_pile = VGroup(mdm_coarse, mdm_mid, mdm_fine)

        target_overlay = _smooth_curve(axes, TARGET_PP).set_stroke(
            color=FOREGROUND, width=4
        )
        # Place dots ON the smoothed curve (not at raw TARGET_PP) so the
        # mid + fine dots visibly land on the target line — "error → 0".
        target_dots = _sieve_dots(axes, smoothed_pp_at_sieves(TARGET_PP)).set_color(WHITE)
        err_bar_zero = _err_bar(ERR_FRAC_SPANNED)

        caption_resolved = _build_caption(
            r"\dots the right size exists. Error $\to 0$."
        )

        # The K_+/K_- pair fades out; the MDM pile (matching counts 1, 5, 12)
        # fades in. FadeOut + FadeIn for the curves rather than Transform:
        # the K+/K- stair curves (4 control points) and the target overlay
        # (80 points) have very different topologies, and Transform produces
        # transient path artifacts during interpolation.
        self.play(
            # K_+/K_- particles fade out, MDM pile fades in.
            FadeOut(large_pile),
            FadeOut(small_particles),
            FadeIn(mdm_pile),
            # Both realized curves fade out; target curve appears.
            FadeOut(self.kplus_curve),
            FadeOut(self.kminus_curve),
            FadeIn(target_overlay),
            FadeOut(self.kplus_dots),
            FadeOut(self.kminus_dots),
            FadeIn(target_dots),
            # Error bar -> 0.
            Transform(self.err_bar_mob, err_bar_zero),
            # Swap caption.
            FadeOut(caption_bingo),
            FadeIn(caption_resolved),
            run_time=1.5,
        )
        self.wait(0.6)
        # Stash so Beat 5 box can size around it.
        self.mdm_pile_mob = mdm_pile

        # =========================================================
        # Beat 5 — MDM box; fade K_+/K_- vector + labels (hold for outro)
        # =========================================================
        # Box wraps the spanned-integer column + multi-particle MDM pile.
        # Pile spans full sieve stack (coarse band top to fine band bottom),
        # so the box has to grow to enclose those scatter regions.
        box_left = SPAN_X - 0.5
        box_right = pile_x + 0.9
        box_top = DATUM_TOP + 0.05
        box_bot = DATUM_BOT - 0.1
        box = Rectangle(
            width=box_right - box_left,
            height=box_top - box_bot,
            color=COARSE,
            stroke_width=3,
        ).move_to([(box_left + box_right) / 2, (box_top + box_bot) / 2, 0])
        mdm_label = tex_text(
            "Minimal Discrete Match", font_size=38, color=COARSE,
        ).move_to([(box_left + box_right) / 2, -3.2, 0])

        # Total particle count (1 + 5 + 12 = 18) — the "number of particles
        # needed to represent the MDM".
        n_total = sum(SPANNED_INTEGERS_DISPLAY)
        total_label = MathTex(
            rf"N_{{\mathrm{{total}}}} = {n_total}",
            color=FOREGROUND,
        ).scale(0.9).next_to(mdm_label, DOWN, buff=0.2)

        self.play(
            FadeOut(caption_resolved),
            # Fade the K vector, its bracket, and both K labels — the
            # algorithm has resolved; only the MDM matters from here.
            FadeOut(self.kplus_entries_mob),
            FadeOut(self.kminus_entries_mob),
            FadeOut(self.bracket_mob),
            FadeOut(self.kplus_label_mob),
            FadeOut(self.kminus_label_mob),
            FadeIn(box),
            Write(mdm_label),
            Write(total_label),
            run_time=1.0,
        )
        self.wait(4.5)
