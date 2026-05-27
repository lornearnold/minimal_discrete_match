"""Scene 1 — Title question.

Layout: left half shows a CDF axes with grain-size distribution curves;
right half shows a DEM packing photo. A block arrow between them carries
the question "N_min = ???". The CDF accumulates curves (rightmost first,
each new one stretches further lower-left). The DEM image cycles through
GSD_0 -> GSD_1 -> GSD_2 in lockstep with the CDF additions.

At the end, the question fills the top, a box is drawn around it, and
"Minimal Discrete Match (MDM)" appears just below in bold.

A small footnote at the bottom attributes the DEM renders.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Axes,
    Create,
    FadeIn,
    FadeOut,
    ImageMobject,
    MathTex,
    Polygon,
    Rectangle,
    Scene,
    Tex,
    Triangle,
    VGroup,
    Write,
    config,
)

from _common import BACKGROUND, FOREGROUND, tex_text

config.background_color = BACKGROUND


# --- Layout ---------------------------------------------------------------

# Axes (left).
AXES_CENTER = np.array([-4.7, -0.5, 0])
AXES_X_LENGTH = 4.6
AXES_Y_LENGTH = 4.4

# Block arrow (between halves).
ARROW_CENTER = np.array([-0.8, -0.5, 0])

# Image frame (right).
IMAGE_CENTER = np.array([3.9, -0.5, 0])
IMAGE_HEIGHT = 5.2  # max height that still leaves room above for the title

# Footnote position.
FOOTNOTE_Y = -3.75


# --- CDF curve generator --------------------------------------------------


def _sigmoid_cdf(x: np.ndarray, x_mid: float, k: float) -> np.ndarray:
    return 1.0 / (1.0 + np.exp(-k * (x - x_mid)))


CURVE_PARAMS = [
    (3.8, 4.0),
    (2.8, 2.5),
    (1.6, 1.6),
]
CURVE_COLORS = ["#FC6255", "#58C4DD", "#83C167"]


def _block_arrow() -> Polygon:
    w = 0.85
    h_body = 0.40
    h_head = 0.85
    body_end = 0.20
    points = [
        [-w, -h_body, 0],
        [body_end, -h_body, 0],
        [body_end, -h_head, 0],
        [w, 0, 0],
        [body_end, h_head, 0],
        [body_end, h_body, 0],
        [-w, h_body, 0],
    ]
    return Polygon(
        *points,
        color=FOREGROUND,
        stroke_width=3,
        fill_color=FOREGROUND,
        fill_opacity=0.15,
    )


def _small_axis_tip(direction: str) -> Triangle:
    """A small filled triangle for an axis end-cap. `direction` in {"up","right"}."""
    t = Triangle(color=FOREGROUND, fill_color=FOREGROUND, fill_opacity=1.0)
    t.scale(0.08)
    if direction == "right":
        t.rotate(-np.pi / 2)
    # up = default orientation
    return t


class TitleQuestion(Scene):
    def construct(self):
        # ---- Axes (left). Tips suppressed; we add small custom triangles. ----
        axes = Axes(
            x_range=[0, 5, 1],
            y_range=[0, 1.05, 0.25],
            x_length=AXES_X_LENGTH,
            y_length=AXES_Y_LENGTH,
            tips=False,
            axis_config={
                "color": FOREGROUND,
                "stroke_width": 2,
                "include_ticks": False,
            },
        ).move_to(AXES_CENTER)

        x_tip = _small_axis_tip("right").move_to(axes.x_axis.get_end())
        y_tip = _small_axis_tip("up").move_to(axes.y_axis.get_end())

        x_label = tex_text("grain size", font_size=22, color=FOREGROUND).next_to(
            x_tip, RIGHT, buff=0.12
        )
        y_label = tex_text("% finer", font_size=22, color=FOREGROUND).next_to(
            y_tip, UP, buff=0.10
        )

        # ---- Block arrow + N_min label --------------------------------------
        arrow = _block_arrow().move_to(ARROW_CENTER)
        nmin_label = MathTex(
            r"N_{\min} = ???", color=FOREGROUND
        ).scale(0.90).next_to(arrow, UP, buff=0.30)

        # ---- CDF curves -----------------------------------------------------
        xs = np.linspace(0, 5, 200)
        curves = []
        for (x_mid, k), color in zip(CURVE_PARAMS, CURVE_COLORS):
            ys = _sigmoid_cdf(xs, x_mid, k)
            curve = axes.plot_line_graph(
                x_values=xs,
                y_values=ys,
                line_color=color,
                add_vertex_dots=False,
                stroke_width=4,
            )
            curves.append(curve)

        # ---- GSD images (no border; large; below the eventual question box).
        img_dir = Path(__file__).resolve().parent.parent
        gsd_paths = [img_dir / f"GSD_{i}.png" for i in range(3)]
        gsd_images = []
        for p in gsd_paths:
            im = ImageMobject(str(p))
            im.height = IMAGE_HEIGHT
            im.move_to(IMAGE_CENTER)
            im.set_z_index(-5)  # below any text/box overlays
            gsd_images.append(im)

        # ---- Footnote attribution (bottom of frame, persistent) -------------
        footnote = tex_text(
            "Modified from Claudio Esperança (2023)",
            font_size=20,
            color=FOREGROUND,
        ).move_to([3.9, FOOTNOTE_Y, 0])
        footnote.set_opacity(0.7)

        # ---- Beat 1: axes + first curve -------------------------------------
        self.play(
            Create(axes),
            FadeIn(x_tip),
            FadeIn(y_tip),
            Write(x_label),
            Write(y_label),
            run_time=0.9,
        )
        self.play(Create(curves[0]), run_time=0.8)

        # ---- Beat 2: arrow + GSD_0 + N_min + footnote -----------------------
        self.play(FadeIn(arrow, shift=RIGHT * 0.2), run_time=0.5)
        self.play(
            FadeIn(gsd_images[0]),
            Write(nmin_label),
            FadeIn(footnote),
            run_time=0.7,
        )
        self.wait(0.6)

        # ---- Beat 3: add curve 2 + swap to GSD_1 ----------------------------
        self.play(
            FadeOut(gsd_images[0]),
            FadeIn(gsd_images[1]),
            Create(curves[1]),
            run_time=0.9,
        )
        self.wait(0.3)

        # ---- Beat 4: add curve 3 + swap to GSD_2 ----------------------------
        self.play(
            FadeOut(gsd_images[1]),
            FadeIn(gsd_images[2]),
            Create(curves[2]),
            run_time=0.9,
        )
        self.wait(0.5)

        # ---- Beat 5: question across the top, then box, then bold MDM -------
        question = tex_text(
            "What is the smallest number of discrete particles\n"
            "needed to match a given grain size distribution?",
            font_size=46,
            color=FOREGROUND,
        ).move_to([0, 3.0, 0])

        q_box = Rectangle(
            width=question.width + 0.8,
            height=question.height + 0.5,
            color=FOREGROUND,
            stroke_width=3.0,
        ).move_to(question.get_center())

        # Bold via \textbf{} in Tex.
        mdm = Tex(
            r"\textbf{Minimal Discrete Match (MDM)}",
            color=FOREGROUND,
        ).scale(1.05).next_to(q_box, DOWN, buff=0.25)

        self.play(Write(question), run_time=1.1)
        self.play(Create(q_box), run_time=0.5)
        self.play(Write(mdm), run_time=0.7)
        self.wait(3.7)
