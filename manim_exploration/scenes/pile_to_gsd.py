"""Storyboard page 3: retained piles + 3-bar cumulative-mass approximation.

Three piles (only a few particles each, scattered with natural jitter) sit
on the left, separated by dashed sieve datums. On the right, an axes shows
three colored bars: each bar spans one sieve interval and reaches the
cumulative mass at the right edge of that interval. The bar colors run
green -> blue -> red across the x-axis.

This scene is the *discrete* picture. `ContinuumReveal` continues from
this end state and refines it (3 -> 5 -> 9 -> 15 bars) while filling the
left half with continuum-sized particles.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Axes,
    Create,
    DashedLine,
    FadeIn,
    Scene,
    Text,
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
    build_gsd_bars,
    scatter_in_band,
)

config.background_color = BACKGROUND


# ---- Layout shared with ContinuumReveal so the handoff is seamless. ----

# Left-half particle area.
PILE_X = (-6.5, -0.6)

# Stacked y-bands, coarse on top.
COARSE_BAND = (1.0, 2.6)
MID_BAND = (-0.5, 0.5)
FINE_BAND = (-2.6, -1.0)

# Datum y-positions (sieves drawn as dashed lines).
DATUM_YS = (2.8, 0.75, -0.75, -2.8)
DATUM_X = (-6.7, -0.4)

# Pile counts: just a handful, so the eye reads "a few representative
# particles" and so the continuum reveal has room to fill in.
N_COARSE, N_MID, N_FINE = 4, 7, 12

# Right-side axes / bar geometry.
SIEVE_XS_3 = (1.3, 2.5, 3.6)
X_LEFT = 0.3


def build_piles(rng: np.random.Generator):
    coarse = scatter_in_band(N_COARSE, COARSE_R, COARSE, COARSE_BAND, PILE_X, rng)
    mid = scatter_in_band(N_MID, MID_R, MID, MID_BAND, PILE_X, rng)
    fine = scatter_in_band(N_FINE, FINE_R, FINE, FINE_BAND, PILE_X, rng)
    return coarse, mid, fine


def build_datums() -> VGroup:
    return VGroup(
        *[
            DashedLine(
                start=[DATUM_X[0], y, 0],
                end=[DATUM_X[1], y, 0],
                color=FOREGROUND,
                stroke_width=1.5,
                dash_length=0.12,
            )
            for y in DATUM_YS
        ]
    )


def build_axes_and_labels():
    axes = (
        Axes(
            x_range=[0, 4, 1],
            y_range=[0, 4, 1],
            x_length=4.6,
            y_length=3.4,
            tips=False,
            axis_config={
                "color": FOREGROUND,
                "stroke_width": 2,
                "include_ticks": False,
            },
        )
        .to_edge(RIGHT, buff=0.9)
        .shift(DOWN * 0.2)
    )
    x_label = Text("size", font_size=22, color=FOREGROUND).next_to(
        axes.x_axis, RIGHT, buff=0.15
    )
    y_label = Text("Percent mass", font_size=22, color=FOREGROUND).next_to(
        axes.y_axis, UP, buff=0.15
    )
    return axes, x_label, y_label


class PileToGSD(Scene):
    def construct(self):
        # When stitched into FullStory, the prior scene leaves piles + datums
        # on the canvas already; skip the redundant setup beats.
        skip_setup = getattr(self, "_skip_pile_setup", False)

        if not skip_setup:
            rng = np.random.default_rng(13)

            coarse_pile, mid_pile, fine_pile = build_piles(rng)
            datums = build_datums()

            self.play(Create(datums), run_time=0.7)
            self.play(
                FadeIn(coarse_pile, shift=DOWN * 0.2),
                FadeIn(mid_pile, shift=DOWN * 0.2),
                FadeIn(fine_pile, shift=DOWN * 0.2),
                run_time=1.0,
            )
            self.wait(0.3)

        axes, x_label, y_label = build_axes_and_labels()
        bars = build_gsd_bars([X_LEFT, *SIEVE_XS_3], axes)

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=0.9)
        self.play(*[FadeIn(b) for b in bars], run_time=1.0)

        # Stash for the seamless handoff to ContinuumReveal.
        self.axes = axes
        self.bars = bars
        self._note_mob = None

        note = Text(
            "Three sieves give a coarse picture —\n"
            "real soil holds many more sizes.",
            font_size=22,
            color=FOREGROUND,
        ).to_edge(UP, buff=0.35)
        self.play(Write(note), run_time=1.0)
        self._note_mob = note

        self.wait(1.1)
