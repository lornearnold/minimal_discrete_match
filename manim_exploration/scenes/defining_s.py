"""Defining S: many subsets share the same GSD; we want the minimal one.

Storyboard:
  - Three short beats, each ~1 s, showing a subset of particles in three
    size bands. Subsets differ in total particle count but all match the
    same GSD shape. A large integer is overlaid on each band, indicating
    a particle count that is *not* expected to be a minimum.
  - Final beat: collapse to one particle per band with a big "?" overlay,
    indicating the Minimal Discrete Match — unknown until we solve for it.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    UP,
    FadeIn,
    FadeOut,
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
    scatter_in_band,
)
from pile_to_gsd import (
    COARSE_BAND,
    FINE_BAND,
    MID_BAND,
    PILE_X,
    build_datums,
)

config.background_color = BACKGROUND


# Three subsets that all satisfy the same GSD shape (counts kept large to
# crowd each band). Ratios held roughly constant across rows.
SUBSETS = [
    (10, 28, 80),
    (6, 17, 48),
    (14, 39, 112),
]


class DefiningS(Scene):
    def construct(self):
        title = Text(
            "Many subsets satisfy the same GSD",
            font_size=28,
            color=FOREGROUND,
        ).to_edge(UP, buff=0.35)
        subtitle = Text(
            "We want the minimum.",
            font_size=22,
            color=FOREGROUND,
        ).next_to(title, DOWN, buff=0.15)

        datums = build_datums()
        self.play(Write(title), Write(subtitle), run_time=0.7)
        self.play(FadeIn(datums), run_time=0.4)

        prev_group = None
        for nc, nm, nf in SUBSETS:
            rng = np.random.default_rng(nc * 31 + nm)
            coarse = scatter_in_band(nc, COARSE_R, COARSE, COARSE_BAND, PILE_X, rng)
            mid = scatter_in_band(nm, MID_R, MID, MID_BAND, PILE_X, rng)
            fine = scatter_in_band(nf, FINE_R, FINE, FINE_BAND, PILE_X, rng)
            piles = VGroup(coarse, mid, fine)

            labels = VGroup(
                Text(str(nc), font_size=84, color=COARSE).move_to(
                    [PILE_X[1] + 1.5, sum(COARSE_BAND) / 2, 0]
                ),
                Text(str(nm), font_size=84, color=MID).move_to(
                    [PILE_X[1] + 1.5, sum(MID_BAND) / 2, 0]
                ),
                Text(str(nf), font_size=84, color=FINE).move_to(
                    [PILE_X[1] + 1.5, sum(FINE_BAND) / 2, 0]
                ),
            )

            new_group = VGroup(piles, labels)
            if prev_group is None:
                self.play(FadeIn(new_group), run_time=0.5)
            else:
                self.play(FadeOut(prev_group), FadeIn(new_group), run_time=0.6)
            self.wait(0.9)
            prev_group = new_group

        # Final beat: one particle per band + question mark.
        rng = np.random.default_rng(99)
        single = VGroup(
            scatter_in_band(1, COARSE_R, COARSE, COARSE_BAND, PILE_X, rng),
            scatter_in_band(1, MID_R, MID, MID_BAND, PILE_X, rng),
            scatter_in_band(1, FINE_R, FINE, FINE_BAND, PILE_X, rng),
        )
        question = Text("?", font_size=240, color=FOREGROUND).move_to([-3.5, 0, 0])
        mdm_label = Text(
            "Minimal Discrete Match = ?",
            font_size=28,
            color=FOREGROUND,
        ).next_to(question, DOWN, buff=0.6)

        self.play(FadeOut(prev_group), run_time=0.5)
        self.play(FadeIn(single), run_time=0.4)
        self.play(Write(question), Write(mdm_label), run_time=0.9)
        self.wait(1.6)
