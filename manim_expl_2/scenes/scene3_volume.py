"""Scene 3 — Particle "Volume" ratios.

Layout (per row):

   [coarse particle]   /   [per-tier particle]      |  1
                                                    |  R > 1
                                                    |  ⋮      Z
                                                    |  R > 1

Compared to Scene 2 the sieve stack is moved into the horizontal middle
of the slide (less blank space). Same vertical row positions as Scene 2
so the ⋮ aligns. The smallest particle is rendered as a bold dot.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Brace,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    Line,
    MathTex,
    Rectangle,
    Scene,
    VGroup,
    Write,
    config,
)

from _common import (
    BACKGROUND,
    COARSE,
    COARSE_R,
    FINE,
    FOREGROUND,
    MID,
    make_particle,
    tex_text,
)
from scene2_mass import (
    DASHED_YS,
    GREEK_Y,
    ROW_YS,
    SOLID_Y,
    VECTOR_X,
    _slash,
)

config.background_color = BACKGROUND


# Volume figure positioned toward the middle of the frame (less blank space).
NUMER_X = -1.4    # coarse particle (numerator)
SLASH_X = -0.4
TIER_X = 0.6      # per-tier particle (denominator)

# Lines just span the figure area.
LINE_X_LO_S3 = -2.4
LINE_X_HI_S3 = 1.5


def _make_lines_s3():
    dashed = VGroup(
        *[
            DashedLine(
                start=[LINE_X_LO_S3, y, 0],
                end=[LINE_X_HI_S3, y, 0],
                color=FOREGROUND,
                stroke_width=1.5,
                dash_length=0.14,
            )
            for y in DASHED_YS
        ]
    )
    solid = Line(
        start=[LINE_X_LO_S3, SOLID_Y, 0],
        end=[LINE_X_HI_S3, SOLID_Y, 0],
        color=FOREGROUND,
        stroke_width=2.5,
    )
    return dashed, solid


class VolumeRatios(Scene):
    def construct(self):
        title = tex_text(
            r"Particle ``Volume'' Ratios", font_size=44, color=FOREGROUND
        ).to_edge(UP, buff=0.35)

        dashed_lines, solid_line = _make_lines_s3()

        # Tier specs: (row_y, line_y, particle_radius, color, is_dot)
        tier_specs = [
            (ROW_YS[0], DASHED_YS[0], COARSE_R, COARSE, False),
            (ROW_YS[1], DASHED_YS[1], COARSE_R * 0.62, MID, False),
            (ROW_YS[3], SOLID_Y,      COARSE_R * 0.18, FINE, True),
        ]

        numerators = VGroup()
        denominators = VGroup()
        slashes = VGroup()
        for row_y, line_y, r, color, is_dot in tier_specs:
            # Coarse numerator — same size every row, rests on the line.
            num = make_particle(COARSE_R, COARSE).move_to(
                [NUMER_X, line_y + COARSE_R + 0.05, 0]
            )
            numerators.add(num)

            if is_dot:
                den = Dot(point=[TIER_X, line_y + 0.10, 0], radius=0.10, color=color)
            else:
                den = make_particle(r, color).move_to(
                    [TIER_X, line_y + r + 0.05, 0]
                )
            denominators.add(den)

            sl = _slash(height=COARSE_R * 2.4 + 0.15).move_to(
                [SLASH_X, line_y + COARSE_R + 0.05, 0]
            )
            slashes.add(sl)

        # ⋮ glyphs aligned with the vector dots at ROW_YS[2].
        DOT_SCALE = 1.3
        sieve_dots = (
            MathTex(r"\vdots", color=FOREGROUND).scale(DOT_SCALE)
            .move_to([SLASH_X, ROW_YS[2], 0])
        )

        v1 = MathTex("1", color=COARSE).scale(1.5).move_to([VECTOR_X, ROW_YS[0], 0])
        v2 = MathTex(r"\mathbb{R} > 1", color=MID).scale(1.5).move_to(
            [VECTOR_X, ROW_YS[1], 0]
        )
        v3 = MathTex(r"\vdots", color=FOREGROUND).scale(DOT_SCALE).move_to(
            [VECTOR_X, ROW_YS[2], 0]
        )
        v4 = MathTex(r"\mathbb{R} > 1", color=FINE).scale(1.5).move_to(
            [VECTOR_X, ROW_YS[3], 0]
        )
        entries = [v1, v2, v3, v4]
        stack = VGroup(*entries)
        anchor = Rectangle(
            width=stack.width + 0.5,
            height=ROW_YS[0] - ROW_YS[3] + 0.7,
            stroke_opacity=0,
            fill_opacity=0,
        ).move_to([VECTOR_X, (ROW_YS[0] + ROW_YS[3]) / 2, 0])
        vector = VGroup(Brace(anchor, LEFT), stack, Brace(anchor, RIGHT))

        zeta_label = MathTex(r"Z", color=FOREGROUND).scale(2.0).move_to(
            [VECTOR_X, GREEK_Y, 0]
        )

        # ---- Animate ----
        self.play(Write(title), run_time=0.6)
        self.play(
            Create(dashed_lines, lag_ratio=0.1),
            Create(solid_line),
            run_time=0.7,
        )

        # Storyboard order: tier particles (denominators) first, then slash,
        # then coarse numerator.
        for den in denominators:
            self.play(FadeIn(den, shift=DOWN * 0.1), run_time=0.30)
        self.play(*[Create(sl) for sl in slashes], run_time=0.5)
        for num in numerators:
            self.play(FadeIn(num, shift=DOWN * 0.1), run_time=0.30)
        self.play(Write(sieve_dots), run_time=0.4)

        self.play(
            FadeIn(vector[0]),
            FadeIn(vector[2]),
            *[Write(e) for e in entries],
            run_time=1.0,
        )
        self.play(Write(zeta_label), run_time=0.5)
        self.wait(2.8)

        # Stash for the Scene 3 → Scene 4 transition.
        self._dashed_lines = dashed_lines
        self._solid_line = solid_line
        self._numerators = numerators
        self._denominators = denominators
        self._slashes = slashes
        self._sieve_dots = sieve_dots
        self._vector = vector
        self._zeta = zeta_label
        self._title = title
