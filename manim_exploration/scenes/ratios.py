"""Storyboard pages 4-5: mass ratios and volume (per-particle) ratios.

Both scenes reuse the dashed-datum row layout from `pile_to_gsd`, with the
coarsest tier on top. On the right, a brace gathers the three ratio
expressions into a vector.

Mass ratio for tier i: total retained mass on sieve i divided by the
coarsest tier's retained mass — M_i / M_1.

Volume ratio for tier i: mass of *one* coarse particle divided by *one*
tier-i particle — M(x_1) / M(x_i) = (x_1 / x_i)^3. The storyboard drew
this inverted (small over large); the paper's ζ uses large over small,
so this scene matches the paper.
"""

from __future__ import annotations

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Brace,
    Create,
    DashedLine,
    FadeIn,
    Line,
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
    particle_cluster,
)

config.background_color = BACKGROUND


# Mirror pile_to_gsd so the three scenes feel continuous.
N_COARSE, N_MID, N_FINE = 8, 22, 65

ROW_YS = (2.0, 0.0, -2.0)
DATUM_X_LO, DATUM_X_HI = -6.5, 2.4


def _datum(y: float) -> DashedLine:
    return DashedLine(
        start=[DATUM_X_LO, y, 0],
        end=[DATUM_X_HI, y, 0],
        color=FOREGROUND,
        stroke_width=1.5,
        dash_length=0.12,
    )


def _slash(height: float = 0.9) -> Line:
    """Diagonal divider between numerator and denominator."""
    h = height / 2
    return Line(
        [-h * 0.55, -h, 0],
        [h * 0.55, h, 0],
        color=FOREGROUND,
        stroke_width=2.5,
    )


def _bracketed(rows: VGroup, center_x: float) -> VGroup:
    """Wrap a vertical stack of expressions in matching left/right braces."""
    rows.move_to([center_x, 0, 0])
    return VGroup(Brace(rows, LEFT), rows, Brace(rows, RIGHT))


class MassRatios(Scene):
    """Pile of tier i ÷ pile of coarse, with the M_i/M_1 vector on the right."""

    def construct(self):
        title = Text("Mass Ratios", font_size=30, color=FOREGROUND).to_edge(UP, buff=0.4)

        # Numerator piles: each tier's full retained pile.
        numerators = [
            particle_cluster(N_COARSE, COARSE_R, COARSE, bbox=(1.5, 0.8), seed=1),
            particle_cluster(N_MID, MID_R, MID, bbox=(1.5, 0.8), seed=2),
            particle_cluster(N_FINE, FINE_R, FINE, bbox=(1.5, 0.8), seed=3),
        ]
        # Denominators: the coarse pile, repeated on every row (different
        # seeds so the three copies don't look identical).
        denominators = [
            particle_cluster(N_COARSE, COARSE_R, COARSE, bbox=(1.5, 0.8), seed=s)
            for s in (11, 12, 13)
        ]

        rows = VGroup()
        for y, num, den in zip(ROW_YS, numerators, denominators):
            num.move_to([-5.0, y, 0])
            den.move_to([-2.0, y, 0])
            slash = _slash(height=1.3).move_to([-3.5, y, 0])
            rows.add(VGroup(num, slash, den))

        datums = VGroup(
            _datum((ROW_YS[0] + ROW_YS[1]) / 2),
            _datum((ROW_YS[1] + ROW_YS[2]) / 2),
        )

        # Vector of mass-ratio expressions.
        m1 = MathTex(r"M_1/M_1").set_color(COARSE)
        m2 = MathTex(r"M_2/M_1").set_color(MID)
        m3 = MathTex(r"M_3/M_1").set_color(FINE)
        stack = VGroup(m1, m2, m3).arrange(DOWN, buff=0.7)
        bracket = _bracketed(stack, center_x=4.3)

        self.play(Write(title), run_time=0.6)
        self.play(Create(datums), run_time=0.5)
        for row in rows:
            self.play(FadeIn(row, shift=DOWN * 0.1), run_time=0.55)
        self.play(
            FadeIn(bracket[0]),
            FadeIn(bracket[2]),
            Write(m1),
            Write(m2),
            Write(m3),
            run_time=1.2,
        )
        self.wait(1.5)


class VolumeRatios(Scene):
    """One coarse particle ÷ one tier-i particle = ζ_i = (x_1/x_i)^3."""

    def construct(self):
        title = Text("Volume Ratios", font_size=30, color=FOREGROUND).to_edge(UP, buff=0.4)

        # Numerator on every row: a single coarse particle.
        # Denominator: a single particle of the row's tier.
        tier_specs = [
            (COARSE_R, COARSE),
            (MID_R, MID),
            (FINE_R, FINE),
        ]

        rows = VGroup()
        for y, (r, color) in zip(ROW_YS, tier_specs):
            num = make_particle(COARSE_R, COARSE).move_to([-5.0, y, 0])
            den = make_particle(r, color).move_to([-2.0, y, 0])
            slash = _slash(height=1.3).move_to([-3.5, y, 0])
            rows.add(VGroup(num, slash, den))

        datums = VGroup(
            _datum((ROW_YS[0] + ROW_YS[1]) / 2),
            _datum((ROW_YS[1] + ROW_YS[2]) / 2),
        )

        # Coarse-on-top is the fix: paper's ζ_i = M(x_1)/M(x_i), not the
        # inverted M(x_i)/M(x_1) that appeared in the hand storyboard.
        v1 = MathTex(r"M(x_1)/M(x_1)").set_color(COARSE)
        v2 = MathTex(r"M(x_1)/M(x_2)").set_color(MID)
        v3 = MathTex(r"M(x_1)/M(x_3)").set_color(FINE)
        stack = VGroup(v1, v2, v3).arrange(DOWN, buff=0.7)
        bracket = _bracketed(stack, center_x=4.3)

        self.play(Write(title), run_time=0.6)
        self.play(Create(datums), run_time=0.5)
        for row in rows:
            self.play(FadeIn(row, shift=DOWN * 0.1), run_time=0.55)
        self.play(
            FadeIn(bracket[0]),
            FadeIn(bracket[2]),
            Write(v1),
            Write(v2),
            Write(v3),
            run_time=1.2,
        )
        self.wait(1.5)
