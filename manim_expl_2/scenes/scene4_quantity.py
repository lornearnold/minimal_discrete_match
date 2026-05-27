"""Scene 4 — Quantity ratios.

Layout (left to right, using more of the available frame width):

  Φ                Z              K

  [pile]/[pile] × [coarse]/[coarse] = {  1     }
  [pile]/[pile] × [coarse]/[mid]    = {  ?.?   }
       ⋮             ⋮                {  ⋮     }                Non
  [pile]/[pile] × [coarse]/[fine]   = {  ?.?   }              integers!

When stitched after Scene 3 (full_video_v2 sets `self._from_scene3=True`),
the volume figure slides right and the Scene 3 lines extend left while
the mass figure and the rest of Scene 4 fade in.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    YELLOW,
    Brace,
    Create,
    DashedLine,
    Dot,
    FadeIn,
    FadeOut,
    Line,
    MathTex,
    Polygon,
    Rectangle,
    Scene,
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
    FOREGROUND,
    MID,
    make_particle,
    tex_text,
)
from scene2_mass import (
    DASHED_YS,
    GREEK_Y,
    PILE_HEIGHTS,
    ROW_YS,
    SOLID_Y,
    _slash,
    mountain_pile,
)

config.background_color = BACKGROUND


# Scene 4 column positions (spread across the full frame width).
# The volume figure was pulled in by 0.1 and EQ moved further left from
# the K vector to remove the brace/equals overlap.
MASS_PILE_X = -5.5
MASS_SLASH_X = -3.9
MASS_DENOM_X = -2.5
TIMES_X = -1.1
VOL_COARSE_X = -0.4
VOL_SLASH_X = 0.6
VOL_TIER_X = 1.6
EQ_X = 2.3
KVEC_X = 3.7
NON_INT_X = 5.5

LINE_X_LO_S4 = -6.7
LINE_X_HI_S4 = 2.0

# Volume figure x-shift when transitioning from Scene 3 (NUMER_X=-1.4,
# SLASH_X=-0.4, TIER_X=0.6) into Scene 4 (-0.4, 0.6, 1.6). +1.0 each.
VOL_SLIDE_RIGHT = 1.0


def _make_lines_s4():
    dashed = VGroup(
        *[
            DashedLine(
                start=[LINE_X_LO_S4, y, 0],
                end=[LINE_X_HI_S4, y, 0],
                color=FOREGROUND,
                stroke_width=1.5,
                dash_length=0.14,
            )
            for y in DASHED_YS
        ]
    )
    solid = Line(
        start=[LINE_X_LO_S4, SOLID_Y, 0],
        end=[LINE_X_HI_S4, SOLID_Y, 0],
        color=FOREGROUND,
        stroke_width=2.5,
    )
    return dashed, solid


class QuantityRatios(Scene):
    def construct(self):
        from_scene3 = bool(getattr(self, "_from_scene3", False))

        title = tex_text(
            "Quantity Ratios", font_size=44, color=FOREGROUND
        ).to_edge(UP, buff=0.35)

        # ---- Mass figure pile specs (3 rows + dots) ------------------
        # Smaller widths than Scene 2 to fit alongside the volume figure,
        # but SAME heights so the piles rest on the shared DASHED/SOLID lines.
        # The M_N denominator on every row is exactly the same shape AND
        # size as the M_N numerator in the top row.
        MN_W_S4 = 1.45
        mass_specs = [
            (DASHED_YS[0], ROW_YS[0], MN_W_S4, PILE_HEIGHTS["M_N"], COARSE, r"M_N"),
            (DASHED_YS[1], ROW_YS[1], 1.20, PILE_HEIGHTS["M_N-1"], MID, r"M_{N-1}"),
            (SOLID_Y, ROW_YS[3], 1.65, PILE_HEIGHTS["M_1"], FINE, r"M_1"),
        ]
        mass_nums = VGroup()
        mass_dens = VGroup()
        mass_slashes = VGroup()
        for line_y, row_y, w, h, color, lbl in mass_specs:
            num = mountain_pile(w, h, color, lbl)
            num.shift([MASS_PILE_X, line_y, 0])
            mass_nums.add(num)

            # M_N pile as denominator — EXACTLY the same as the M_N
            # numerator in the top row (same width, height, color, label).
            den = mountain_pile(MN_W_S4, PILE_HEIGHTS["M_N"], COARSE, r"M_N")
            den.shift([MASS_DENOM_X, line_y, 0])
            mass_dens.add(den)

            sl = _slash(height=h + 0.4).move_to(
                [MASS_SLASH_X, row_y + 0.04, 0]
            )
            mass_slashes.add(sl)

        DOT_SCALE = 1.2
        # One ⋮ in the mass-numerator column (no dots in the denominator or
        # × columns — those are math-op columns).
        mass_num_dots = (
            MathTex(r"\vdots", color=FOREGROUND).scale(DOT_SCALE)
            .move_to([MASS_PILE_X, ROW_YS[2], 0])
        )

        # ---- × symbols (per row, no dots column) ---------------------
        times_marks = VGroup(
            *[
                MathTex(r"\times", color=FOREGROUND).scale(1.1).move_to(
                    [TIMES_X, ROW_YS[i] + 0.05, 0]
                )
                for i in (0, 1, 3)
            ]
        )

        # ---- Volume figure (built or slid in from Scene 3) -----------
        vol_tier_specs = [
            (ROW_YS[0], DASHED_YS[0], COARSE_R, COARSE, False),
            (ROW_YS[1], DASHED_YS[1], COARSE_R * 0.62, MID, False),
            (ROW_YS[3], SOLID_Y, COARSE_R * 0.18, FINE, True),
        ]

        if from_scene3:
            # Reuse Scene 3's mobjects (already on stage). They sit at the
            # Scene 3 x-positions; we'll slide them right by VOL_SLIDE_RIGHT.
            vol_nums = self._numerators
            vol_dens = self._denominators
            vol_slashes = self._slashes
            vol_dots = self._sieve_dots
        else:
            # Build fresh at the Scene 4 positions.
            vol_nums = VGroup()
            vol_dens = VGroup()
            vol_slashes = VGroup()
            for row_y, line_y, r, color, is_dot in vol_tier_specs:
                num = make_particle(COARSE_R, COARSE).move_to(
                    [VOL_COARSE_X, line_y + COARSE_R + 0.05, 0]
                )
                vol_nums.add(num)
                if is_dot:
                    den = Dot(
                        point=[VOL_TIER_X, line_y + 0.10, 0],
                        radius=0.10,
                        color=color,
                    )
                else:
                    den = make_particle(r, color).move_to(
                        [VOL_TIER_X, line_y + r + 0.05, 0]
                    )
                vol_dens.add(den)
                sl = _slash(height=COARSE_R * 2.4 + 0.15).move_to(
                    [VOL_SLASH_X, line_y + COARSE_R + 0.05, 0]
                )
                vol_slashes.add(sl)
            vol_dots = (
                MathTex(r"\vdots", color=FOREGROUND).scale(DOT_SCALE)
                .move_to([VOL_SLASH_X, ROW_YS[2], 0])
            )

        # ---- = sign --------------------------------------------------
        eq = MathTex("=", color=FOREGROUND).scale(1.3).move_to(
            [EQ_X, (ROW_YS[0] + ROW_YS[3]) / 2, 0]
        )

        # ---- K vector ------------------------------------------------
        k_entries = [
            MathTex("1", color=COARSE).scale(1.4).move_to([KVEC_X, ROW_YS[0], 0]),
            MathTex("?.?", color=MID).scale(1.2).move_to([KVEC_X, ROW_YS[1], 0]),
            MathTex(r"\vdots", color=FOREGROUND).scale(DOT_SCALE).move_to(
                [KVEC_X, ROW_YS[2], 0]
            ),
            MathTex("?.?", color=FINE).scale(1.2).move_to([KVEC_X, ROW_YS[3], 0]),
        ]
        k_stack = VGroup(*k_entries)
        k_anchor = Rectangle(
            width=k_stack.width + 0.4,
            height=ROW_YS[0] - ROW_YS[3] + 0.7,
            stroke_opacity=0,
            fill_opacity=0,
        ).move_to([KVEC_X, (ROW_YS[0] + ROW_YS[3]) / 2, 0])
        k_brace_l = Brace(k_anchor, LEFT)
        k_brace_r = Brace(k_anchor, RIGHT)
        k_vec = VGroup(k_brace_l, k_stack, k_brace_r)

        # ---- Greek labels at the top --------------------------------
        phi_label = MathTex(r"\Phi", color=FOREGROUND).scale(1.7).move_to(
            [(MASS_PILE_X + MASS_DENOM_X) / 2, GREEK_Y, 0]
        )
        z_label_target_pos = np.array(
            [(VOL_COARSE_X + VOL_TIER_X) / 2, GREEK_Y, 0]
        )
        z_label = MathTex(r"Z", color=FOREGROUND).scale(1.7).move_to(z_label_target_pos)
        k_label = MathTex(r"K", color=FOREGROUND).scale(1.7).move_to(
            [KVEC_X, GREEK_Y, 0]
        )

        # ---- "Non integers!" callout (two lines) --------------------
        non_int_label = tex_text(
            "Non\nintegers!",
            font_size=34,
            color=YELLOW,
            line_buff=0.10,
        ).move_to([NON_INT_X, 0, 0])
        non_int_box_top = ROW_YS[1] + 0.55
        non_int_box_bot = ROW_YS[3] - 0.55
        non_int_box_l = k_brace_l.get_left()[0] - 0.05
        non_int_box_r = k_brace_r.get_right()[0] + 0.05
        non_int_box = Rectangle(
            width=non_int_box_r - non_int_box_l,
            height=non_int_box_top - non_int_box_bot,
            color=YELLOW,
            stroke_width=3,
        ).move_to(
            [
                (non_int_box_l + non_int_box_r) / 2,
                (non_int_box_top + non_int_box_bot) / 2,
                0,
            ]
        )

        # ---- Now drive the animations --------------------------------
        if from_scene3:
            # Phase A: transition Scene 3 → Scene 4 (slide + extend + appear)
            # The Z vector (self._vector) fades out; the Greek Z label
            # currently sits at the Scene-3 vector position and slides left
            # to its Scene-4 position above the volume figure.
            scene3_zeta = self._zeta

            # Build long Scene 4 dashed/solid lines that the Scene 3 lines
            # will Transform into.
            new_dashed_lines, new_solid_line = _make_lines_s4()

            # Slide-right amounts for the volume figure mobjects.
            slide = np.array([VOL_SLIDE_RIGHT, 0, 0])

            anims = []
            # Fade the Z vector (brace + entries) but keep the Z label.
            anims.append(FadeOut(self._vector))
            # Fade out the Scene 3 title — it gets replaced by Scene 4 title.
            if hasattr(self, "_title") and self._title is not None:
                anims.append(FadeOut(self._title))
            # Slide volume figure mobjects.
            for m in [*vol_nums, *vol_dens, *vol_slashes, vol_dots]:
                anims.append(m.animate.shift(slide))
            # Move Z label from above old vector to above new volume figure.
            anims.append(scene3_zeta.animate.move_to(z_label_target_pos))
            # Extend dashed and solid lines.
            for old, new in zip(self._dashed_lines, new_dashed_lines):
                anims.append(Transform(old, new))
            anims.append(Transform(self._solid_line, new_solid_line))
            self.play(*anims, run_time=1.4)

            # Bring up Scene 4 title and mass figure. The ⋮ glyph appears
            # alongside the first mass pile (not with the math operation).
            self.play(Write(title), run_time=0.5)
            self.play(
                FadeIn(mass_nums[0], shift=DOWN * 0.15),
                Write(mass_num_dots),
                run_time=0.5,
            )
            self.play(
                *[FadeIn(p, shift=DOWN * 0.15) for p in mass_nums[1:]],
                run_time=0.55,
            )
            # Math op: slashes + denominator piles (no dots in this beat).
            self.play(
                *[Create(sl) for sl in mass_slashes],
                *[FadeIn(d, shift=DOWN * 0.1) for d in mass_dens],
                run_time=0.8,
            )
            self.play(Write(phi_label), run_time=0.4)

            # × symbols.
            self.play(
                *[Write(t) for t in times_marks],
                run_time=0.6,
            )

            # = sign, K vector, K label.
            self.play(
                Write(eq),
                FadeIn(k_brace_l),
                FadeIn(k_brace_r),
                *[Write(e) for e in k_entries],
                run_time=0.9,
            )
            self.play(Write(k_label), run_time=0.4)

            # The Z label is already in its Scene-4 position from the
            # transition; nothing more to do for it.
        else:
            # Standalone: build everything from scratch.
            dashed_lines, solid_line = _make_lines_s4()

            self.play(Write(title), run_time=0.4)
            self.play(
                Create(dashed_lines, lag_ratio=0.1),
                Create(solid_line),
                run_time=0.7,
            )
            # Mass numerators + ⋮ together (mass column).
            self.play(
                FadeIn(mass_nums[0], shift=DOWN * 0.1),
                Write(mass_num_dots),
                run_time=0.5,
            )
            self.play(
                *[FadeIn(p, shift=DOWN * 0.1) for p in mass_nums[1:]],
                run_time=0.5,
            )
            self.play(
                *[Create(sl) for sl in mass_slashes],
                *[FadeIn(d, shift=DOWN * 0.08) for d in mass_dens],
                run_time=0.7,
            )
            self.play(Write(phi_label), run_time=0.4)
            # Volume figure + its ⋮ (ride with the first volume element).
            self.play(
                *[Write(t) for t in times_marks],
                FadeIn(vol_dens[0], shift=DOWN * 0.1),
                Write(vol_dots),
                run_time=0.7,
            )
            self.play(
                *[FadeIn(d, shift=DOWN * 0.1) for d in vol_dens[1:]],
                run_time=0.4,
            )
            self.play(
                *[Create(sl) for sl in vol_slashes],
                *[FadeIn(n, shift=DOWN * 0.1) for n in vol_nums],
                run_time=0.6,
            )
            self.play(Write(z_label), run_time=0.4)
            self.play(
                Write(eq),
                FadeIn(k_brace_l),
                FadeIn(k_brace_r),
                *[Write(e) for e in k_entries],
                run_time=0.9,
            )
            self.play(Write(k_label), run_time=0.4)

        # ---- "Non integers!" callout ---------------------------------
        self.play(Create(non_int_box), Write(non_int_label), run_time=0.7)
        self.wait(1.0)

        # ---- Poster overlay (two-beat reveal, bigger font) ----------
        q_line1 = tex_text(
            "How to find the minimum possible integer",
            font_size=34, color=FOREGROUND,
        )
        q_line2 = tex_text(
            "representation of $K$ for a zero error match?",
            font_size=34, color=FOREGROUND,
        )
        poster_line = tex_text(
            "Come see Poster 2205!",
            font_size=42, color=FOREGROUND,
        )

        question_group = VGroup(q_line1, q_line2).arrange(DOWN, buff=0.14)
        full_group = VGroup(question_group, poster_line).arrange(DOWN, buff=0.4)

        banner_w = max(full_group.width, 8.5) + 0.7
        banner_h = full_group.height + 0.55
        banner_center_x = (LINE_X_LO_S4 + k_brace_r.get_right()[0]) / 2
        banner_bg = Rectangle(
            width=banner_w,
            height=banner_h,
            color=FOREGROUND,
            stroke_width=2.5,
            fill_color=BACKGROUND,
            fill_opacity=0.95,
        ).move_to([banner_center_x, ROW_YS[2], 0])
        full_group.move_to(banner_bg.get_center())

        self.play(
            FadeIn(banner_bg),
            Write(q_line1),
            Write(q_line2),
            run_time=1.0,
        )
        self.wait(1.0)
        self.play(Write(poster_line), run_time=0.8)
        self.wait(2.5)
