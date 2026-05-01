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
    LEFT,
    RIGHT,
    UP,
    WHITE,
    Brace,
    FadeIn,
    FadeOut,
    MathTex,
    Rectangle,
    Scene,
    Text,
    Transform,
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
            "Many sets of particles (S) are compatible with G",
            font_size=28,
            color=FOREGROUND,
        ).to_edge(UP, buff=0.35)

        datums = build_datums()
        self.play(Write(title), run_time=0.7)
        self.play(FadeIn(datums), run_time=0.4)

        # ---- Curly braces flanking the per-band number labels. ----
        numbers_x = PILE_X[1] + 1.5
        brace_anchor = Rectangle(
            width=1.5,
            height=COARSE_BAND[1] - FINE_BAND[0] + 0.6,
            stroke_opacity=0,
            fill_opacity=0,
        ).move_to([numbers_x, 0, 0])
        left_brace = Brace(brace_anchor, LEFT)
        right_brace = Brace(brace_anchor, RIGHT)

        # Prominent S, sitting just past the right brace.
        s_label = Text("S", font_size=110, color=WHITE).move_to([3.4, 0.6, 0])
        n_counter = MathTex("N = ?", color=WHITE).scale(1.1).next_to(
            s_label, DOWN, buff=0.35
        )

        self.play(
            FadeIn(left_brace),
            FadeIn(right_brace),
            Write(s_label),
            Write(n_counter),
            run_time=0.7,
        )

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
            n_total = nc + nm + nf
            new_n = MathTex(f"N = {n_total}", color=WHITE).scale(1.1).next_to(
                s_label, DOWN, buff=0.35
            )

            if prev_group is None:
                self.play(FadeIn(new_group), Transform(n_counter, new_n), run_time=0.5)
            else:
                self.play(
                    FadeOut(prev_group),
                    FadeIn(new_group),
                    Transform(n_counter, new_n),
                    run_time=0.6,
                )
            self.wait(0.9)
            prev_group = new_group

        # ---- Final beat: one coarse particle, scattered "?"s in mid/fine. ----
        rng = np.random.default_rng(99)
        single_labels = VGroup(
            Text("1", font_size=84, color=COARSE).move_to(
                [numbers_x, sum(COARSE_BAND) / 2, 0]
            ),
            Text("?", font_size=84, color=MID).move_to(
                [numbers_x, sum(MID_BAND) / 2, 0]
            ),
            Text("?", font_size=84, color=FINE).move_to(
                [numbers_x, sum(FINE_BAND) / 2, 0]
            ),
        )

        def _band_questions(n: int, color, band, font_size: int) -> VGroup:
            qs = VGroup()
            for _ in range(n):
                x = rng.uniform(PILE_X[0] + 0.3, PILE_X[1] - 0.3)
                y = rng.uniform(band[0] + 0.2, band[1] - 0.2)
                qs.add(Text("?", font_size=font_size, color=color).move_to([x, y, 0]))
            return qs

        single = VGroup(
            scatter_in_band(1, COARSE_R, COARSE, COARSE_BAND, PILE_X, rng),
            _band_questions(5, MID, MID_BAND, font_size=36),
            _band_questions(8, FINE, FINE_BAND, font_size=28),
            single_labels,
        )
        n_mdm = MathTex(r"N_{\mathrm{MDM}} = \, ?", color=WHITE).scale(1.4).next_to(
            s_label, DOWN, buff=0.35
        )
        mdm_caption = Text(
            "S with the least particles is the Minimal Discrete Match",
            font_size=24,
            color=FOREGROUND,
        ).to_edge(DOWN, buff=0.5)

        self.play(FadeOut(prev_group), run_time=0.5)
        self.play(
            FadeIn(single),
            Transform(n_counter, n_mdm),
            Write(mdm_caption),
            run_time=0.9,
        )
        self.wait(1.7)
