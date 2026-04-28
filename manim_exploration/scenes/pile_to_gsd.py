"""Storyboard page 3: retained piles map to a mass-vs-size plot.

Carries the design language from `sieve_stack`: same color tiers, same
particle radii, same per-tier counts (8 / 22 / 65). Three piles sit on the
left, separated by dashed datum lines (representing the sieves they were
retained on); on the right, axes show a smooth cumulative-mass curve and
three colored slices whose areas correspond to the retained masses on each
sieve. A caption reminds the viewer that real soil has many more grains
than the figure can render.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Axes,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    Polygon,
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
    particle_cluster,
)

config.background_color = BACKGROUND


# Tier counts mirror the cloud in `sieve_stack` so the two scenes feel
# continuous when watched back-to-back.
N_COARSE, N_MID, N_FINE = 8, 22, 65


class PileToGSD(Scene):
    def construct(self):
        # ---- Left half: three particle piles separated by dashed datums.
        # Roughly equal-area bboxes so each pile reads as the same "amount of
        # stuff" visually — the visual story is about retained-mass parity,
        # not particle count parity.
        coarse_pile = particle_cluster(
            count=N_COARSE, radius=COARSE_R, color=COARSE,
            bbox=(1.7, 0.9), seed=1,
        )
        mid_pile = particle_cluster(
            count=N_MID, radius=MID_R, color=MID,
            bbox=(1.7, 0.9), seed=2,
        )
        fine_pile = particle_cluster(
            count=N_FINE, radius=FINE_R, color=FINE,
            bbox=(1.7, 0.9), seed=3,
        )

        piles = VGroup(coarse_pile, mid_pile, fine_pile).arrange(DOWN, buff=0.7)
        piles.to_edge(LEFT, buff=1.0).shift(UP * 0.2)

        # Dashed datum lines: the sieves the piles were retained on. One
        # above each pile and one below the bottom pile (the pan).
        datum_x_lo, datum_x_hi = -6.5, -2.0

        def datum_at_y(y):
            return DashedLine(
                start=[datum_x_lo, y, 0],
                end=[datum_x_hi, y, 0],
                color=FOREGROUND,
                stroke_width=1.5,
                dash_length=0.12,
            )

        datums = VGroup(
            datum_at_y(coarse_pile.get_top()[1] + 0.3),
            datum_at_y((coarse_pile.get_bottom()[1] + mid_pile.get_top()[1]) / 2),
            datum_at_y((mid_pile.get_bottom()[1] + fine_pile.get_top()[1]) / 2),
            datum_at_y(fine_pile.get_bottom()[1] - 0.3),
        )

        self.play(Create(datums), run_time=0.8)
        self.play(
            FadeIn(coarse_pile, shift=DOWN * 0.2),
            FadeIn(mid_pile, shift=DOWN * 0.2),
            FadeIn(fine_pile, shift=DOWN * 0.2),
            run_time=1.0,
        )
        self.wait(0.4)

        # ---- Right half: mass vs. size axes.
        axes = Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            x_length=4.6,
            y_length=3.4,
            tips=False,
            axis_config={"color": FOREGROUND, "stroke_width": 2, "include_ticks": False},
        ).to_edge(RIGHT, buff=0.9).shift(DOWN * 0.2)

        x_label = Text("size", font_size=22, color=FOREGROUND).next_to(
            axes.x_axis, RIGHT, buff=0.15
        )
        y_label = Text("Mass", font_size=22, color=FOREGROUND).next_to(
            axes.y_axis, UP, buff=0.15
        )

        # Cumulative mass curve. Slope between consecutive sieve sizes
        # corresponds to the retained mass on that sieve (the slice area).
        def curve_func(x):
            return 0.4 + 3.2 / (1 + np.exp(-2.2 * (x - 2.0)))

        curve = axes.plot(
            curve_func, x_range=[0.3, 3.8], color=FOREGROUND, stroke_width=3
        )

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=0.9)
        self.play(Create(curve), run_time=1.0)

        # ---- Three colored retained-mass slices, each anchored to a tier.
        # The slice's vertical extent equals the curve's rise across the
        # sieve interval — i.e., the retained mass on that sieve.
        slices_spec = [
            ((0.5, 1.3), FINE),    # finest grains  -> leftmost slice
            ((1.5, 2.5), MID),
            ((2.7, 3.6), COARSE),  # coarsest -> rightmost slice
        ]

        slice_mobjects = VGroup()
        endpoint_dots = VGroup()
        for (x0, x1), color in slices_spec:
            xs = np.linspace(x0, x1, 32)
            top_pts = [axes.c2p(x, curve_func(x)) for x in xs]
            bottom_pts = [axes.c2p(x1, 0), axes.c2p(x0, 0)]
            slice_mobjects.add(
                Polygon(
                    *top_pts, *bottom_pts,
                    color=color,
                    stroke_width=2.5,
                    fill_opacity=0.22,
                )
            )
            endpoint_dots.add(
                Dot(
                    point=axes.c2p(x1, curve_func(x1)),
                    color=FOREGROUND,
                    radius=0.07,
                )
            )

        self.play(*[FadeIn(s) for s in slice_mobjects], run_time=1.1)
        self.play(FadeIn(endpoint_dots), run_time=0.4)

        # ---- Caption: real soil has many more grains than we can show.
        note = Text(
            "Real soil holds many more grains than this —\n"
            "counting them is infeasible.",
            font_size=22,
            color=FOREGROUND,
        ).to_edge(UP, buff=0.35)
        self.play(Write(note), run_time=1.0)

        self.wait(1.5)
