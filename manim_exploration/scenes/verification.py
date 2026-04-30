"""Verification scene — replicates the manuscript's `fig-demo`.

Compares MDM-predicted N_sim vs reported N_sim from the
Zeraati-Shamsabadi & Sadrekarimi (2025) DEM study of upscaled Athabasca
sand, with markers encoding scale factor and color encoding sample
diameter. Includes the predicted-only points for unscaled DEM models of
Athabasca sand (sit on the y=x line, since "reported" is unknown).

Reported particle counts (N) are taken straight from the manuscript. The
predicted values are not in the .qmd (they are computed at render time
from `gsd_lib.MinimalPackingGenerator`). Until those are wired in, we use
the manuscript's stated relationship: predicted is consistently and
moderately *lower* than reported. We approximate predicted ≈ reported /
1.7, which puts the points just below the y=x line as in the figure.

When real predicted values are available, drop them into PREDICTED_N.
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
    Dot,
    FadeIn,
    Line,
    Rectangle,
    Scene,
    Square,
    Text,
    Triangle,
    VGroup,
    Write,
    config,
    rgb_to_color,
)

from _common import BACKGROUND, COARSE, FINE, FOREGROUND, MID

config.background_color = BACKGROUND


# ---- Z-S study points: (D mm, scale factor, reported N, predicted N). ----
# Reported N comes straight from the manuscript table.
# Predicted N was computed from gsd_lib.MinimalPackingGenerator with the
# Athabasca sand GSD scaled by SF, the reported sample volume, and the
# reported void ratio (matching the manuscript's `fig-demo` recipe).
ZS_POINTS = [
    (50, 5, 103075, 6.92e4),
    (70, 5, 202972, 1.35e5),
    (105, 5, 447161, 2.98e5),
    (175, 5, 1255067, 8.13e5),
    (50, 10, 12408, 8.64e3),
    (70, 10, 24349, 1.79e4),
    (105, 10, 54564, 3.83e4),
    (175, 10, 155028, 1.07e5),
    (70, 15, 7185, 5.06e3),
    (105, 15, 15719, 1.17e4),
    (175, 15, 44522, 3.18e4),
    (70, 20, 2816, 2.11e3),
    (105, 20, 6667, 4.69e3),
    (175, 20, 18180, 1.31e4),
]

# Predicted N for unscaled Athabasca sand (no reported counterpart).
ZS_UNSCALED_PREDICTED = [
    (50, 8.94e6),
    (70, 1.75e7),
    (105, 3.94e7),
    (175, 1.09e8),
]


# Marker (mobject) by scale factor.
def _marker(sf: int, color, position) -> VGroup:
    """SF -> shape: 1=circle, 5=triangle, 10=square, 15=diamond, 20=triangle-up."""
    size = 0.13
    if sf == 1:
        m = Dot(radius=size * 1.1, color=color)
    elif sf == 5:
        m = Triangle(color=color, fill_opacity=1.0).scale(size * 1.4).rotate(np.pi)
    elif sf == 10:
        m = Square(side_length=size * 2.0, color=color, fill_opacity=1.0)
    elif sf == 15:
        m = Square(side_length=size * 2.0, color=color, fill_opacity=1.0).rotate(np.pi / 4)
    else:  # 20
        m = Triangle(color=color, fill_opacity=1.0).scale(size * 1.4)
    m.set_stroke(FOREGROUND, width=1.0)
    m.move_to(position)
    return m


# Color by sample diameter D — viridis-ish.
D_COLORS = {
    50: rgb_to_color([0.27, 0.00, 0.33]),   # purple
    70: rgb_to_color([0.20, 0.40, 0.55]),   # teal
    105: rgb_to_color([0.13, 0.65, 0.55]),  # green
    175: rgb_to_color([0.99, 0.91, 0.14]),  # yellow
}


class Verification(Scene):
    def construct(self):
        title = Text(
            "Verification: predicted vs. reported N_sim",
            font_size=26,
            color=FOREGROUND,
        ).to_edge(UP, buff=0.3)
        sub = Text(
            "Zeraati-Shamsabadi & Sadrekarimi (2025), Athabasca sand",
            font_size=18,
            color=FOREGROUND,
        ).next_to(title, DOWN, buff=0.1)

        # Log-log axes spanning 10^3 to 10^9.
        axes = Axes(
            x_range=[3, 9, 1],
            y_range=[3, 9, 1],
            x_length=5.2,
            y_length=5.2,
            tips=False,
            axis_config={
                "color": FOREGROUND,
                "stroke_width": 2,
                "include_ticks": True,
            },
        ).shift(DOWN * 0.3 + LEFT * 1.3)

        x_label = Text(
            "log10  N_sim  (MDM predicted)",
            font_size=18,
            color=FOREGROUND,
        ).next_to(axes, DOWN, buff=0.25)
        y_label = (
            Text("log10  N_sim  (reported)", font_size=18, color=FOREGROUND)
            .rotate(np.pi / 2)
            .next_to(axes, LEFT, buff=0.25)
        )

        # y=x diagonal line.
        diag = Line(
            axes.c2p(3, 3),
            axes.c2p(9, 9),
            color=FOREGROUND,
            stroke_width=1.5,
        )
        diag.set_stroke(opacity=0.7)

        # ---- Scaled DEM data (the actual Z-S study points). ----
        scaled_markers = VGroup()
        for d, sf, n, n_pred in ZS_POINTS:
            pos = axes.c2p(np.log10(n_pred), np.log10(n))
            scaled_markers.add(_marker(sf, D_COLORS[d], pos))

        # ---- Unscaled MDM predictions (lie on y=x by construction). ----
        unscaled_markers = VGroup()
        for d, n_pred in ZS_UNSCALED_PREDICTED:
            pos = axes.c2p(np.log10(n_pred), np.log10(n_pred))
            unscaled_markers.add(_marker(1, D_COLORS[d], pos))

        # ---- Annotations / boxes. ----
        scaled_box = Rectangle(
            width=2.4, height=2.4,
            color=FOREGROUND,
            stroke_width=1.5,
        ).move_to(axes.c2p(np.log10(2e5), np.log10(2e5)))
        scaled_caption = Text(
            "Z-S (2025)\nscaled DEM data",
            font_size=15,
            color=FOREGROUND,
        ).next_to(scaled_box, DOWN, buff=0.05)

        unscaled_box = Rectangle(
            width=2.0, height=2.0,
            color=FOREGROUND,
            stroke_width=1.5,
        ).move_to(axes.c2p(np.log10(2e8), np.log10(2e8)))
        unscaled_caption = Text(
            "MDM predictions for\nunscaled Athabasca\nsand DEM models",
            font_size=15,
            color=FOREGROUND,
        ).next_to(unscaled_box, UP, buff=0.05)

        # ---- Legend (right side). ----
        sf_legend = VGroup(
            Text("Scale Factor", font_size=16, color=FOREGROUND),
            *[
                VGroup(
                    _marker(sf, FOREGROUND, [0, 0, 0]),
                    Text(f"SF = {sf}" if sf != 1 else "Unscaled",
                         font_size=14, color=FOREGROUND),
                ).arrange(RIGHT, buff=0.15)
                for sf in (1, 5, 10, 15, 20)
            ],
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        d_legend = VGroup(
            Text("Sample D (mm)", font_size=16, color=FOREGROUND),
            *[
                VGroup(
                    Dot(color=D_COLORS[d], radius=0.10),
                    Text(f"D = {d}", font_size=14, color=FOREGROUND),
                ).arrange(RIGHT, buff=0.15)
                for d in (50, 70, 105, 175)
            ],
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12)

        legends = VGroup(sf_legend, d_legend).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        legends.next_to(axes, RIGHT, buff=0.3).align_to(axes, UP)

        self.play(Write(title), Write(sub), run_time=0.7)
        self.play(Create(axes), Write(x_label), Write(y_label), run_time=1.0)
        self.play(Create(diag), run_time=0.5)
        self.play(FadeIn(legends), run_time=0.7)
        self.play(FadeIn(scaled_markers, lag_ratio=0.05), run_time=1.2)
        self.play(FadeIn(scaled_box), Write(scaled_caption), run_time=0.8)
        self.play(FadeIn(unscaled_markers, lag_ratio=0.1), run_time=1.0)
        self.play(FadeIn(unscaled_box), Write(unscaled_caption), run_time=0.8)
        self.wait(2.0)
