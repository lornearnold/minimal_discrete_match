"""Quantity ratio: mass-ratio vector × volume-ratio vector = quantity ratios.

Visual: the mass-ratio vector (blobs) on the left, multiplied by the
volume-ratio vector (single particles) in the middle, equals a quantity-
ratio vector on the right whose first entry is 1 and the others are "?.?"
to flag that integer-ness is not guaranteed.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Arrow,
    Brace,
    FadeIn,
    FadeOut,
    GrowArrow,
    MathTex,
    Rectangle,
    Scene,
    Text,
    Transform,
    VGroup,
    Write,
    config,
)

import numpy as np

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
from ratios import mass_blob
from rounding import (
    ARROW_X,
    LEFT_X,
    NUM_LABEL_X,
    PILE_BAND_HEIGHT,
    QVEC_X,
    ROW_YS,
)

config.background_color = BACKGROUND


def _uniform_bracket(inner: VGroup, center_x: float, brace_height: float) -> VGroup:
    """Wrap `inner` in left/right braces sized to a fixed height so multiple
    bracketed groups end up with visually matched braces."""
    inner.move_to([center_x, 0, 0])
    anchor = Rectangle(
        width=max(inner.width, 0.5) + 0.4,
        height=brace_height,
        stroke_opacity=0,
        fill_opacity=0,
    ).move_to([center_x, 0, 0])
    return VGroup(Brace(anchor, LEFT), inner, Brace(anchor, RIGHT))


class QuantityRatio(Scene):
    def construct(self):
        title = tex_text("Quantity Ratio, K", font_size=42, color=FOREGROUND).to_edge(UP, buff=0.4)
        self._qr_title = title  # stashed so ReducingError can fade it out

        ys = (1.6, 0.0, -1.6)
        brace_height = ys[0] - ys[-1] + 1.2  # uniform across all three vectors

        # ---- Mass-ratio vector (blob_i / blob_1). ----
        blob_r = 0.5
        mass_rows = VGroup()
        for y, (color, lbl) in zip(
            ys,
            [(COARSE, r"M_1"), (MID, r"M_2"), (FINE, r"M_3")],
        ):
            row = VGroup(
                mass_blob(blob_r, color, lbl),
                MathTex("/", color=FOREGROUND).scale(0.9),
                mass_blob(blob_r, COARSE, r"M_1"),
            ).arrange(RIGHT, buff=0.18).move_to([0, y, 0])
            mass_rows.add(row)
        mass_vec = _uniform_bracket(mass_rows, center_x=-5.0, brace_height=brace_height)

        # ---- Volume-ratio vector (one coarse particle / one tier-i particle). ----
        vol_rows = VGroup()
        for y, (color, rad) in zip(
            ys,
            [(COARSE, COARSE_R), (MID, MID_R), (FINE, FINE_R)],
        ):
            row = VGroup(
                make_particle(COARSE_R, COARSE),
                MathTex("/", color=FOREGROUND).scale(0.9),
                make_particle(rad, color),
            ).arrange(RIGHT, buff=0.2).move_to([0, y, 0])
            vol_rows.add(row)
        vol_vec = _uniform_bracket(vol_rows, center_x=-0.4, brace_height=brace_height)

        # Place × halfway between mass_vec right brace and vol_vec left brace.
        mass_right_x = mass_vec[2].get_center()[0]
        vol_left_x = vol_vec[0].get_center()[0]
        times = MathTex(r"\times", color=FOREGROUND).scale(1.4).move_to(
            [(mass_right_x + vol_left_x) / 2, 0, 0]
        )

        # ---- Quantity-ratio result vector with [1, ?.?, ?.?]. ----
        q_entries = VGroup(
            MathTex("1").set_color(COARSE).scale(1.2).move_to([0, ys[0], 0]),
            MathTex("?.?").set_color(MID).scale(1.2).move_to([0, ys[1], 0]),
            MathTex("?.?").set_color(FINE).scale(1.2).move_to([0, ys[2], 0]),
        )
        q_vec = _uniform_bracket(q_entries, center_x=4.4, brace_height=brace_height)

        vol_right_x = vol_vec[2].get_center()[0]
        q_left_x = q_vec[0].get_center()[0]
        equals = MathTex("=", color=FOREGROUND).scale(1.4).move_to(
            [(vol_right_x + q_left_x) / 2, 0, 0]
        )

        q_label = tex_text(
            "Quantity Ratio",
            font_size=30,
            color=FOREGROUND,
        ).next_to(q_vec, DOWN, buff=0.3)

        self.play(Write(title), run_time=0.6)
        self.play(FadeIn(mass_vec), run_time=0.9)
        self.play(Write(times), FadeIn(vol_vec), run_time=0.9)
        self.play(Write(equals), FadeIn(q_vec), Write(q_label), run_time=1.0)

        caveat = tex_text(
            "Only the first entry is guaranteed to be an integer.",
            font_size=30,
            color=FOREGROUND,
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(caveat), run_time=0.9)
        self.wait(1.4)

        # ---- Replace glyphs with numerical values whose products land on
        # the quantity ratios used by the error scene: [1, 4.6, 12.1].
        mass_x = -5.0
        vol_x = -0.4
        q_x = 4.4
        mass_numbers = VGroup(
            MathTex("1.0", color=COARSE).scale(1.4).move_to([mass_x, ys[0], 0]),
            MathTex("1.15", color=MID).scale(1.4).move_to([mass_x, ys[1], 0]),
            MathTex("0.605", color=FINE).scale(1.4).move_to([mass_x, ys[2], 0]),
        )
        vol_numbers = VGroup(
            MathTex("1.0", color=COARSE).scale(1.4).move_to([vol_x, ys[0], 0]),
            MathTex("4.0", color=MID).scale(1.4).move_to([vol_x, ys[1], 0]),
            MathTex("20.0", color=FINE).scale(1.4).move_to([vol_x, ys[2], 0]),
        )
        q_numbers = VGroup(
            MathTex("1", color=COARSE).scale(1.4).move_to([q_x, ys[0], 0]),
            MathTex("4.6", color=MID).scale(1.4).move_to([q_x, ys[1], 0]),
            MathTex("12.1", color=FINE).scale(1.4).move_to([q_x, ys[2], 0]),
        )
        # Wider braces sized for the numerical values so they don't clip "12.1".
        wider_anchor = Rectangle(
            width=q_numbers.width + 0.5,
            height=brace_height,
            stroke_opacity=0,
            fill_opacity=0,
        ).move_to([q_x, 0, 0])
        wider_braces = (Brace(wider_anchor, LEFT), Brace(wider_anchor, RIGHT))

        self.play(
            FadeOut(mass_rows),
            FadeIn(mass_numbers),
            FadeOut(vol_rows),
            FadeIn(vol_numbers),
            Transform(q_entries, q_numbers),
            Transform(q_vec[0], wider_braces[0]),
            Transform(q_vec[2], wider_braces[1]),
            run_time=1.2,
        )
        self.wait(0.7)

        # ---- Teaser into the rounding view: q_vec slides left to QVEC_X,
        # arrow → "rounded" + first integer pile + count labels appear, all
        # at the rounding scene's ROW_YS so the next scene reuses them. ----
        rounding_brace_h = ROW_YS[0] - ROW_YS[-1] + 0.4
        new_q = VGroup(
            MathTex("1", color=COARSE).scale(1.4).move_to([QVEC_X, ROW_YS[0], 0]),
            MathTex("4.6", color=MID).scale(1.4).move_to([QVEC_X, ROW_YS[1], 0]),
            MathTex("12.1", color=FINE).scale(1.4).move_to([QVEC_X, ROW_YS[2], 0]),
        )
        new_anchor = Rectangle(
            width=new_q.width + 0.4,
            height=rounding_brace_h,
            stroke_opacity=0,
            fill_opacity=0,
        ).move_to([QVEC_X, 0, 0])
        new_q_vec = VGroup(
            Brace(new_anchor, LEFT), new_q, Brace(new_anchor, RIGHT)
        )

        arrow = Arrow(
            start=[ARROW_X - 0.6, 0, 0],
            end=[ARROW_X + 0.6, 0, 0],
            color=FOREGROUND,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.25,
            buff=0,
        )
        rounded_lbl = tex_text("rounded", font_size=28, color=FOREGROUND).next_to(
            arrow, UP, buff=0.1
        )

        # Particle pile + count labels for iter 1 (1 coarse, 5 mid, 12 fine).
        rng = np.random.default_rng(7)
        pile_specs = [
            (1, COARSE_R, COARSE, ROW_YS[0]),
            (5, MID_R, MID, ROW_YS[1]),
            (12, FINE_R, FINE, ROW_YS[2]),
        ]
        pile = VGroup()
        for n, r, color, y in pile_specs:
            band = (y - PILE_BAND_HEIGHT / 2, y + PILE_BAND_HEIGHT / 2)
            pile.add(scatter_in_band(
                n, r, color, band, (LEFT_X - 1.1, LEFT_X + 0.9), rng,
            ))

        count_labels = VGroup(
            tex_text("1", font_size=84, color=COARSE).move_to([NUM_LABEL_X, ROW_YS[0], 0]),
            tex_text("5", font_size=84, color=MID).move_to([NUM_LABEL_X, ROW_YS[1], 0]),
            tex_text("12", font_size=84, color=FINE).move_to([NUM_LABEL_X, ROW_YS[2], 0]),
        )

        self.play(
            FadeOut(mass_vec[0]),
            FadeOut(mass_vec[2]),
            FadeOut(vol_vec[0]),
            FadeOut(vol_vec[2]),
            FadeOut(mass_numbers),
            FadeOut(vol_numbers),
            FadeOut(times),
            FadeOut(equals),
            FadeOut(q_label),
            FadeOut(caveat),
            Transform(q_vec[0], new_q_vec[0]),
            Transform(q_vec[2], new_q_vec[2]),
            Transform(q_entries, new_q),
            run_time=0.9,
        )
        self.play(
            GrowArrow(arrow),
            Write(rounded_lbl),
            FadeIn(pile),
            FadeIn(count_labels),
            run_time=0.7,
        )
        self.wait(0.3)

        # Stash for the seamless handoff to ReducingError.
        self._qr_q_vec = q_vec  # already transformed to new_q_vec position
        self._qr_arrow = arrow
        self._qr_rounded_lbl = rounded_lbl
        self._qr_pile = pile
        self._qr_count_labels = count_labels
