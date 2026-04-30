"""Spanned integer approach + perfect-match labeling.

Storyboard numbers (last sketch page):
  - K_- (uses largest size in each range): [1, 4.1, 11.8]
  - K_+ (uses smallest size in each range): [1, 6.8, 13.4]
  - integers spanned: 1, {5 or 6}, {12 or 13}

`SpannedIntegerApproach`: shows two stacked particles per row at the
extreme allowable sizes, "?" between them; on the right, the two ratio
vectors with the spanned integers between.

`SpannedIntegerError`: realized cumulative curve overlays the target
exactly (zero error). Box around the result, labeled "Minimal Discrete
Match".
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    Brace,
    DashedLine,
    FadeIn,
    MathTex,
    Rectangle,
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
from rounding import (
    DATUM_X,
    ROW_YS,
    TARGET_PP,
    _build_axes,
    _build_chart,
    _datums,
    _piles_with_counts,
    _smooth_curve,
)

config.background_color = BACKGROUND


# Numbers from the storyboard. Per the manuscript, K_- uses the MIN
# allowable x in each range (smaller x → larger ζ → larger K), so K_- is
# the larger of the two ratios.
K_MINUS = (1.0, 6.8, 13.4)   # min-size end of each range (larger ratio)
K_PLUS = (1.0, 4.1, 11.8)    # max-size end of each range (smaller ratio)
SPANNED_INTEGERS = np.array([1, 5, 12])  # fine -> mid -> coarse for _piles_with_counts


def _ratio_pair_block() -> VGroup:
    """Two stacked vectors (K_- and K_+) with the spanned integer between."""
    title = Text("Quantity ratios", font_size=22, color=FOREGROUND)

    def vec(values, decimals=1):
        rows = []
        for v in values:
            s = "1" if v == 1.0 else f"{v:.{decimals}f}"
            rows.append(s)
        body = r" \\ ".join(rows)
        return MathTex(rf"\begin{{bmatrix}} {body} \end{{bmatrix}}")

    minus_vec = vec(K_MINUS)
    plus_vec = vec(K_PLUS)
    int_vec = MathTex(
        r"\begin{bmatrix} 1 \\ 5 \\ 12 \end{bmatrix}",
        color=COARSE,
    )

    minus_lbl = Text("K_-", font_size=18, color=FOREGROUND)
    plus_lbl = Text("K_+", font_size=18, color=FOREGROUND)
    int_lbl = Text("spanned\nintegers", font_size=18, color=COARSE)

    left_col = VGroup(minus_lbl, minus_vec).arrange(DOWN, buff=0.15)
    mid_col = VGroup(int_lbl, int_vec).arrange(DOWN, buff=0.15)
    right_col = VGroup(plus_lbl, plus_vec).arrange(DOWN, buff=0.15)

    body = VGroup(left_col, mid_col, right_col).arrange(RIGHT, buff=0.55)
    full = VGroup(title, body).arrange(DOWN, buff=0.3).move_to([3.5, 0, 0])
    return full


def _two_size_rows() -> VGroup:
    """Per row: a particle at the largest allowed size, '?', and a particle
    at the smallest allowed size. Top row = coarse tier, etc."""
    rng = np.random.default_rng(0)
    rows = VGroup()
    # Pairs (large_r, small_r) for each tier — illustrative, larger than the
    # nominal MID_R / FINE_R / COARSE_R used elsewhere.
    pairs = [
        (COARSE_R * 1.15, COARSE_R * 0.85, COARSE),
        (MID_R * 1.25, MID_R * 0.85, MID),
        (FINE_R * 1.45, FINE_R * 0.75, FINE),
    ]
    for y, (r_big, r_small, color) in zip(ROW_YS, pairs):
        big = make_particle(r_big, color).move_to([-5.5, y + 0.35, 0])
        q = MathTex("?", color=FOREGROUND).scale(0.9).move_to([-4.6, y, 0])
        small = make_particle(r_small, color).move_to([-5.5, y - 0.45, 0])
        rows.add(VGroup(big, q, small))
    return rows


class SpannedIntegerApproach(Scene):
    def construct(self):
        title = Text(
            "Spanned-integer approach",
            font_size=30,
            color=FOREGROUND,
        ).to_edge(UP, buff=0.4)

        datums = _datums()
        rows = _two_size_rows()
        ratios = _ratio_pair_block()

        self.play(Write(title), run_time=0.5)
        self.play(FadeIn(datums), run_time=0.4)
        self.play(FadeIn(rows), run_time=0.8)
        self.play(FadeIn(ratios), run_time=1.0)

        caption = Text(
            "An integer falls between K_- and K_+ for each range.",
            font_size=20,
            color=FOREGROUND,
        ).to_edge(DOWN, buff=0.4)
        self.play(Write(caption), run_time=0.7)
        self.wait(1.6)


class SpannedIntegerError(Scene):
    def construct(self):
        title = Text(
            "Spanned integers → exact GSD match",
            font_size=28,
            color=FOREGROUND,
        ).to_edge(UP, buff=0.4)

        datums = _datums()
        rng = np.random.default_rng(3)
        # Use the spanned integers as the realized counts; choosing matching
        # intermediate sizes makes the realized curve coincide with target.
        piles = _piles_with_counts(SPANNED_INTEGERS, rng)
        chart = _build_chart(SPANNED_INTEGERS)
        # For the spanned-integer match, stamp out the (visually distracting)
        # error band by overdrawing the smooth target curve on top.
        target_overlay = _smooth_curve(chart[0], TARGET_PP).set_stroke(
            color=FOREGROUND, width=4
        )

        result = VGroup(piles, chart, target_overlay)

        self.play(Write(title), run_time=0.5)
        self.play(FadeIn(datums), run_time=0.3)
        self.play(FadeIn(result), run_time=1.2)

        # Box + label.
        box = Rectangle(
            width=result.width + 0.7,
            height=result.height + 0.7,
            color=COARSE,
            stroke_width=3,
        ).move_to(result.get_center())
        mdm_label = Text(
            "Minimal Discrete Match",
            font_size=28,
            color=COARSE,
        ).next_to(box, DOWN, buff=0.25)

        self.play(FadeIn(box), Write(mdm_label), run_time=1.0)
        self.wait(1.8)
