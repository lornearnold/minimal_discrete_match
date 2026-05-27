"""Scene 5 — Verification and Example usage.

Left half: log-log scatter of MDM-predicted vs. reported particle counts
(Zeraati-Shamsabadi 2025 study). Two clusters: the scaled data (along
y=x with offset) labeled "Verification" inside a slope-aligned ellipse,
and the unscaled MDM predictions on y=x, also ellipse-circled. An arrow
points off to the right, into a feature checklist.

Right half: seven bullets, each prefixed with a green check mark or a
red X. Small footnote citation at the bottom.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RED,
    RIGHT,
    UP,
    Arrow,
    Axes,
    Create,
    Dot,
    Ellipse,
    FadeIn,
    GREEN,
    Line,
    MathTex,
    Polygon,
    Scene,
    Square,
    Tex,
    Triangle,
    VGroup,
    Write,
    config,
    rgb_to_color,
)

from _common import BACKGROUND, FOREGROUND, tex_text

config.background_color = BACKGROUND


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

ZS_UNSCALED_PREDICTED = [
    (50, 8.94e6),
    (70, 1.75e7),
    (105, 3.94e7),
    (175, 1.09e8),
]

D_COLORS = {
    50: rgb_to_color([0.30, 0.10, 0.55]),
    70: rgb_to_color([0.20, 0.45, 0.65]),
    105: rgb_to_color([0.15, 0.70, 0.55]),
    175: rgb_to_color([0.99, 0.85, 0.20]),
}


def _marker(sf: int, color, position) -> VGroup:
    size = 0.11
    if sf == 1:
        m = Dot(radius=size * 1.2, color=color)
    elif sf == 5:
        m = Triangle(color=color, fill_opacity=1.0).scale(size * 1.4).rotate(np.pi)
    elif sf == 10:
        m = Square(side_length=size * 2.0, color=color, fill_opacity=1.0)
    elif sf == 15:
        m = Square(side_length=size * 2.0, color=color, fill_opacity=1.0).rotate(np.pi / 4)
    else:
        m = Triangle(color=color, fill_opacity=1.0).scale(size * 1.4)
    m.set_stroke(FOREGROUND, width=0.8)
    m.move_to(position)
    return m


def _check_glyph(size: float = 0.32, color=GREEN) -> VGroup:
    return VGroup(
        Line(
            [-size * 0.6, 0, 0],
            [-size * 0.1, -size * 0.55, 0],
            color=color,
            stroke_width=6,
        ),
        Line(
            [-size * 0.1, -size * 0.55, 0],
            [size * 0.75, size * 0.55, 0],
            color=color,
            stroke_width=6,
        ),
    )


def _x_glyph(size: float = 0.32, color=RED) -> VGroup:
    return VGroup(
        Line(
            [-size * 0.55, -size * 0.55, 0],
            [size * 0.55, size * 0.55, 0],
            color=color,
            stroke_width=6,
        ),
        Line(
            [-size * 0.55, size * 0.55, 0],
            [size * 0.55, -size * 0.55, 0],
            color=color,
            stroke_width=6,
        ),
    )


GREEN_OK = rgb_to_color([0.32, 0.86, 0.41])
RED_BAD = rgb_to_color([0.95, 0.34, 0.34])


def _bullet_labels():
    return [
        ("ok", Tex("Experimental design", color=FOREGROUND)),
        ("ok", Tex("Any grain size dist.", color=FOREGROUND)),
        ("ok", Tex("Arbitrary shapes", color=FOREGROUND)),
        ("ok", Tex("Closed form", color=FOREGROUND)),
        ("ok", MathTex(r"N_{\min}(\mathrm{GSD})", color=FOREGROUND)),
        ("ok", Tex(r"GSD $\rightarrow$ computation cost", color=FOREGROUND)),
        ("bad", Tex("Representative volume", color=FOREGROUND)),
    ]


class VerificationUsage(Scene):
    def construct(self):
        title = tex_text(
            "Verification and\nExample usage",
            font_size=40,
            color=FOREGROUND,
            line_buff=0.10,
        ).to_corner(UP + LEFT, buff=0.35)

        # ---- Axes (wider) ------------------------------------------
        axes = Axes(
            x_range=[3, 9, 1],
            y_range=[3, 9, 1],
            x_length=5.6,
            y_length=5.0,
            tips=False,
            axis_config={
                "color": FOREGROUND,
                "stroke_width": 2,
                "include_ticks": True,
            },
        ).shift(DOWN * 0.4 + LEFT * 3.5)

        x_label = MathTex(
            r"\log_{10} N_{\mathrm{sim}}\ (\mathrm{predicted})",
            color=FOREGROUND,
        ).scale(0.55).next_to(axes, DOWN, buff=0.35)
        y_label = (
            MathTex(
                r"\log_{10} N_{\mathrm{sim}}\ (\mathrm{reported})",
                color=FOREGROUND,
            )
            .scale(0.55)
            .rotate(np.pi / 2)
            .next_to(axes, LEFT, buff=0.35)
        )

        tick_labels = VGroup()
        for v in range(3, 10):
            tick_labels.add(
                MathTex(f"10^{{{v}}}", color=FOREGROUND).scale(0.45).next_to(
                    axes.c2p(v, 3), DOWN, buff=0.10
                )
            )
            tick_labels.add(
                MathTex(f"10^{{{v}}}", color=FOREGROUND).scale(0.45).next_to(
                    axes.c2p(3, v), LEFT, buff=0.10
                )
            )

        diag = Line(
            axes.c2p(3, 3),
            axes.c2p(9, 9),
            color=FOREGROUND,
            stroke_width=1.2,
        ).set_stroke(opacity=0.6)

        # ---- Scaled (verification) data + slope-aligned ellipse ----
        scaled_markers = VGroup()
        scaled_positions = []
        for d, sf, n, n_pred in ZS_POINTS:
            pos = axes.c2p(np.log10(n_pred), np.log10(n))
            scaled_markers.add(_marker(sf, D_COLORS[d], pos))
            scaled_positions.append(pos[:2])

        scaled_positions = np.array(scaled_positions)
        s_center = scaled_positions.mean(axis=0)

        # Diagonal unit vector in scene coordinates.
        p_lo = axes.c2p(3, 3)
        p_hi = axes.c2p(9, 9)
        diag_vec = np.array(p_hi[:2]) - np.array(p_lo[:2])
        diag_unit = diag_vec / np.linalg.norm(diag_vec)
        perp_unit = np.array([-diag_unit[1], diag_unit[0]])

        rel = scaled_positions - s_center
        s_major = np.max(np.abs(rel @ diag_unit)) + 0.55  # generous padding
        s_minor = np.max(np.abs(rel @ perp_unit)) + 0.45  # WIDER ellipse

        scaled_ellipse = Ellipse(
            width=2 * s_major,
            height=2 * s_minor,
            color=FOREGROUND,
            stroke_width=2.4,
        ).rotate(np.pi / 4).move_to([*s_center, 0])

        verif_label = tex_text(
            "Verification",
            font_size=28,
            color=FOREGROUND,
        ).move_to(axes.c2p(4.0, 7.5))

        # ---- Unscaled + slope-aligned ellipse ----------------------
        unscaled_markers = VGroup()
        unscaled_positions = []
        for d, n_pred in ZS_UNSCALED_PREDICTED:
            pos = axes.c2p(np.log10(n_pred), np.log10(n_pred))
            unscaled_markers.add(_marker(1, D_COLORS[d], pos))
            unscaled_positions.append(pos[:2])

        unscaled_positions = np.array(unscaled_positions)
        u_center = unscaled_positions.mean(axis=0)
        rel_u = unscaled_positions - u_center
        u_major = np.max(np.abs(rel_u @ diag_unit)) + 0.60
        u_minor = np.max(np.abs(rel_u @ perp_unit)) + 0.55
        unscaled_ellipse = Ellipse(
            width=2 * u_major,
            height=2 * u_minor,
            color=FOREGROUND,
            stroke_width=2.4,
        ).rotate(np.pi / 4).move_to([*u_center, 0])

        # ---- Bullet list (further right) ---------------------------
        bullets = VGroup()
        for kind, label in _bullet_labels():
            glyph = _check_glyph(0.32, GREEN_OK) if kind == "ok" else _x_glyph(0.32, RED_BAD)
            label.scale(0.95)
            row = VGroup(glyph, label).arrange(RIGHT, buff=0.28)
            bullets.add(row)
        bullets.arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        # Place bullets close to the right edge, top aligned with the
        # unscaled ellipse.
        bullets.next_to(axes, RIGHT, buff=1.2)
        target_top_y = unscaled_ellipse.get_top()[1] - 0.15
        delta_y = target_top_y - bullets[0].get_top()[1]
        bullets.shift(UP * delta_y)

        # Arrow from the unscaled cluster's right edge to the first bullet.
        arrow_start = unscaled_ellipse.get_right() + np.array([0.05, 0, 0])
        arrow_end = bullets[0].get_left() + np.array([-0.10, 0, 0])
        arrow = Arrow(
            arrow_start,
            arrow_end,
            color=FOREGROUND,
            stroke_width=3.5,
            buff=0.05,
            max_tip_length_to_length_ratio=0.10,
        )

        # ---- Citation footnote -------------------------------------
        citation = tex_text(
            "Verification data: Zeraati-Shamsabadi \\& Sadrekarimi (2025)",
            font_size=20,
            color=FOREGROUND,
        ).move_to([0, -3.78, 0])
        citation.set_opacity(0.75)

        # ---- Animate -----------------------------------------------
        self.play(Write(title), run_time=0.7)
        self.play(
            Create(axes),
            Write(x_label),
            Write(y_label),
            FadeIn(tick_labels),
            run_time=1.0,
        )
        self.play(Create(diag), run_time=0.4)
        self.play(FadeIn(scaled_markers, lag_ratio=0.04), run_time=1.0)
        self.play(Create(scaled_ellipse), Write(verif_label), run_time=0.7)
        self.play(
            FadeIn(unscaled_markers, lag_ratio=0.08),
            Create(unscaled_ellipse),
            run_time=0.8,
        )
        self.play(Create(arrow), FadeIn(citation), run_time=0.6)

        # Bullets revealed slowly; last item gets 2s on screen.
        # 7 bullets: ~0.7s each except the last which gets a longer reveal
        # followed by a 2s dwell.
        for i, row in enumerate(bullets):
            run_time = 0.50 if i < len(bullets) - 1 else 0.70
            self.play(FadeIn(row, shift=RIGHT * 0.15), run_time=run_time)
        self.wait(2.0)
