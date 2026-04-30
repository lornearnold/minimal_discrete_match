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
    Brace,
    FadeIn,
    MathTex,
    Scene,
    Text,
    VGroup,
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
)
from ratios import mass_blob

config.background_color = BACKGROUND


def _bracket(group: VGroup) -> VGroup:
    return VGroup(Brace(group, LEFT), group, Brace(group, RIGHT))


class QuantityRatio(Scene):
    def construct(self):
        title = Text("Quantity Ratio", font_size=30, color=FOREGROUND).to_edge(UP, buff=0.4)

        ys = (1.6, 0.0, -1.6)

        # ---- Mass-ratio vector (blob_i / blob_1). ----
        mass_rows = VGroup()
        for y, (color, rad, lbl) in zip(
            ys,
            [(COARSE, 0.55, r"M_1"), (MID, 0.4, r"M_2"), (FINE, 0.28, r"M_3")],
        ):
            row = VGroup(
                mass_blob(rad, color, lbl, seed=abs(int(y * 10)) + 1),
                MathTex("/", color=FOREGROUND).scale(0.9),
                mass_blob(0.55, COARSE, r"M_1", seed=abs(int(y * 10)) + 7),
            ).arrange(RIGHT, buff=0.18).move_to([-4.6, y, 0])
            mass_rows.add(row)
        mass_vec = _bracket(mass_rows)

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
            ).arrange(RIGHT, buff=0.2).move_to([-1.0, y, 0])
            vol_rows.add(row)
        vol_vec = _bracket(vol_rows)

        times = MathTex(r"\times", color=FOREGROUND).scale(1.2).move_to([-2.85, 0, 0])
        equals = MathTex("=", color=FOREGROUND).scale(1.2).move_to([1.5, 0, 0])

        # ---- Quantity-ratio result vector with [1, ?.?, ?.?]. ----
        q_entries = VGroup(
            MathTex("1").set_color(COARSE),
            MathTex("?.?").set_color(MID),
            MathTex("?.?").set_color(FINE),
        ).arrange(DOWN, buff=0.7).move_to([3.5, 0, 0])
        q_vec = _bracket(q_entries)
        q_label = Text(
            "Quantity Ratio",
            font_size=22,
            color=FOREGROUND,
        ).next_to(q_vec, DOWN, buff=0.3)

        self.play(Write(title), run_time=0.6)
        self.play(FadeIn(mass_vec), run_time=0.9)
        self.play(Write(times), FadeIn(vol_vec), run_time=0.9)
        self.play(Write(equals), FadeIn(q_vec), Write(q_label), run_time=1.0)

        caveat = Text(
            "Only the first entry is guaranteed to be an integer.",
            font_size=22,
            color=FOREGROUND,
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(caveat), run_time=0.9)
        self.wait(1.6)
