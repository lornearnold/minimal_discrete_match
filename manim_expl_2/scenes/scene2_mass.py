"""Scene 2 — Total mass ratios.

Layout (per row):

  [mountain pile (M_i)]  /   [mountain pile (M_N)]     |  vector entry
                                                       |  (Phi above)

Three explicit rows (M_N, M_{N-1}, M_1) plus a dots row in between.
Dashed lines hold the upper two piles, a solid line holds the bottom
M_1 pile, and one extra dashed line sits in the dots region as a
ghost sieve. The vector on the right (1 / R / ⋮ / R) is wrapped in a
brace with the Greek letter Φ above. Vector row y-positions match the
pile centers so the ellipses (⋮) line up between the sieve stack and
the vector.
"""

from __future__ import annotations

import numpy as np
from manim import (
    BLACK,
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
    Polygon,
    Rectangle,
    Scene,
    Tex,
    VGroup,
    Write,
    config,
    interpolate_color,
    WHITE,
)

from _common import BACKGROUND, COARSE, FINE, FOREGROUND, MID, tex_text

config.background_color = BACKGROUND


# --- Shared row geometry (used by scenes 2, 3, 4) -----------------------

# Row centers. The vector entries and pile centers sit at these y-values
# so the ⋮ glyph aligns perfectly between the sieve stack and the vector.
ROW_YS = (1.55, 0.35, -0.95, -2.30)

# Pile heights — bigger than the first pass so labels read clearly inside.
PILE_HEIGHTS = {
    "M_N": 0.70,
    "M_N-1": 0.60,
    "M_1": 0.78,
}

# Dashed/solid line positions are derived so piles rest exactly on a line.
DASHED_YS = (
    ROW_YS[0] - PILE_HEIGHTS["M_N"] / 2,        # M_N rests here
    ROW_YS[1] - PILE_HEIGHTS["M_N-1"] / 2,      # M_{N-1} rests here
    -1.70,                                       # ghost sieve in dots area
)
SOLID_Y = ROW_YS[3] - PILE_HEIGHTS["M_1"] / 2   # M_1 rests here

# Greek-letter label sits well above the top row.
GREEK_Y = ROW_YS[0] + 0.95

# Vector on the right (shared x for all sieve-stack scenes).
VECTOR_X = 4.0

# Scene 2 column positions.
PILE_X = -5.0           # numerator pile centers
SLASH_X = -3.0
DENOM_X = -1.0          # denominator pile centers (full-size M_N pile)
LINE_X_LO_S2 = -6.4
LINE_X_HI_S2 = 0.4


# --- Mountain pile silhouette ------------------------------------------


def mountain_pile(
    width: float,
    height: float,
    color,
    label: str,
    seed: int | None = None,
    n_pts: int = 56,
) -> VGroup:
    """A pile-of-granular-material silhouette: triangular profile with a
    slightly rounded peak and small low-frequency irregularity along the
    top edge. Flat bottom (rests on y=0).

    The shape reads as "pile of sand/gravel" rather than "blob of liquid."
    """
    if seed is None:
        seed = sum(ord(c) for c in label) + len(label) * 17
    rng = np.random.default_rng(seed)

    # Profile: y(x) = (1 - |2x/w|^p)^q
    # p ~ 1.4 keeps slopes near-linear (mountain-like), q ~ 0.85 rounds the peak.
    p_exp = rng.uniform(1.30, 1.50)
    q_exp = rng.uniform(0.78, 0.95)

    n_modes = 3
    amps = rng.uniform(-0.025, 0.025, n_modes)
    phases = rng.uniform(0, 2 * np.pi, n_modes)

    pts: list[list[float]] = []
    for k in range(n_pts + 1):
        u = k / n_pts                    # 0..1
        x = -width / 2 + u * width
        norm = 2 * u - 1                 # -1..1
        base = max(0.0, 1.0 - abs(norm) ** p_exp) ** q_exp
        perturb = sum(
            amps[m] * np.cos((m + 2) * norm * np.pi + phases[m])
            for m in range(n_modes)
        )
        y = max(0.005, height * (base + perturb))
        pts.append([x, y, 0])
    pts.append([width / 2, 0, 0])
    pts.append([-width / 2, 0, 0])

    fill = interpolate_color(color, WHITE, 0.55)
    blob = Polygon(
        *pts,
        color=color,
        fill_color=fill,
        fill_opacity=1.0,
        stroke_width=3.0,
    )
    # Dark version of the pile color for strong contrast against the light fill.
    label_color = interpolate_color(color, BLACK, 0.60)
    text = MathTex(label, color=label_color).scale(0.80 * height / 0.55)
    # Slightly above the geometric center so the label sits comfortably
    # under the rounded peak instead of in the wide base.
    text.move_to(blob.get_center() + np.array([0, height * 0.08, 0]))
    return VGroup(blob, text)


# Compatibility alias for scene 4's earlier import.
pile_blob = mountain_pile


# --- Common helpers ----------------------------------------------------


def make_horizontal_lines(
    x_lo: float = LINE_X_LO_S2,
    x_hi: float = LINE_X_HI_S2,
) -> tuple[VGroup, Line]:
    dashed = VGroup(
        *[
            DashedLine(
                start=[x_lo, y, 0],
                end=[x_hi, y, 0],
                color=FOREGROUND,
                stroke_width=1.5,
                dash_length=0.14,
            )
            for y in DASHED_YS
        ]
    )
    solid = Line(
        start=[x_lo, SOLID_Y, 0],
        end=[x_hi, SOLID_Y, 0],
        color=FOREGROUND,
        stroke_width=2.5,
    )
    return dashed, solid


def _slash(height: float = 0.9, width_factor: float = 0.55) -> Line:
    h = height / 2
    return Line(
        [-h * width_factor, -h, 0],
        [h * width_factor, h, 0],
        color=FOREGROUND,
        stroke_width=2.5,
    )


def _vector_rows_and_brace(
    entries: list[MathTex],
    row_ys: list[float],
    center_x: float,
    label_scale: float = 1.5,
    brace_pad: float = 0.6,
) -> VGroup:
    for lbl, y in zip(entries, row_ys):
        lbl.scale(label_scale).move_to([center_x, y, 0])
    stack = VGroup(*entries)
    anchor = Rectangle(
        width=max(stack.width, 0.4) + 0.5,
        height=row_ys[0] - row_ys[-1] + brace_pad,
        stroke_opacity=0,
        fill_opacity=0,
    ).move_to([center_x, (row_ys[0] + row_ys[-1]) / 2, 0])
    return VGroup(Brace(anchor, LEFT), stack, Brace(anchor, RIGHT))


# Place a pile so its BASE sits exactly on `line_y` and its horizontal
# center is at `x`. Mountain piles are centered around (0,0) on creation
# with the BASE at y=0, so positioning is straightforward.
def place_pile_on_line(pile: VGroup, x: float, line_y: float) -> VGroup:
    pile.shift([x, line_y, 0])
    return pile


class TotalMassRatios(Scene):
    def construct(self):
        title = tex_text(
            "Total Mass Ratios", font_size=44, color=FOREGROUND
        ).to_edge(UP, buff=0.35)

        # --- Lines ----------------------------------------------------
        dashed_lines, solid_line = make_horizontal_lines()

        # --- Per-row pile specs ---------------------------------------
        # Bigger piles so the M-labels fit clearly inside.
        # (line_y, width, height, color, label)
        MN_W = 2.4   # full-size M_N pile (same in numerator and denominator)
        numer_specs = [
            (DASHED_YS[0], MN_W, PILE_HEIGHTS["M_N"], COARSE, r"M_N"),
            (DASHED_YS[1], 2.10, PILE_HEIGHTS["M_N-1"], MID, r"M_{N-1}"),
            (SOLID_Y, 2.70, PILE_HEIGHTS["M_1"], FINE, r"M_1"),
        ]

        numerators = VGroup()
        denominators = VGroup()
        slashes = VGroup()
        for line_y, w, h, color, lbl in numer_specs:
            num = mountain_pile(w, h, color, lbl)
            place_pile_on_line(num, PILE_X, line_y)
            numerators.add(num)

            # Denominator on every row is the *M_N* pile — EXACTLY the same
            # shape and size as the M_N numerator in the top row (same
            # mathematical object).
            den = mountain_pile(MN_W, PILE_HEIGHTS["M_N"], COARSE, r"M_N")
            place_pile_on_line(den, DENOM_X, line_y)
            denominators.add(den)

            sl = _slash(height=h + 0.45).move_to(
                [SLASH_X, line_y + h / 2 + 0.05, 0]
            )
            slashes.add(sl)

        # A single ⋮ glyph in the sieve stack (numerator column). It appears
        # alongside the masses, not with the math operation.
        DOT_SCALE = 1.3
        sieve_dots = (
            MathTex(r"\vdots", color=FOREGROUND).scale(DOT_SCALE)
            .move_to([PILE_X, ROW_YS[2], 0])
        )

        # --- Vector (built manually so the dots row uses DOT_SCALE) ---
        v1 = MathTex("1", color=COARSE).scale(1.5).move_to([VECTOR_X, ROW_YS[0], 0])
        v2 = MathTex(r"\mathbb{R}", color=MID).scale(1.5).move_to([VECTOR_X, ROW_YS[1], 0])
        v3 = MathTex(r"\vdots", color=FOREGROUND).scale(DOT_SCALE).move_to(
            [VECTOR_X, ROW_YS[2], 0]
        )
        v4 = MathTex(r"\mathbb{R}", color=FINE).scale(1.5).move_to([VECTOR_X, ROW_YS[3], 0])
        entries = [v1, v2, v3, v4]
        stack = VGroup(*entries)
        anchor = Rectangle(
            width=stack.width + 0.5,
            height=ROW_YS[0] - ROW_YS[3] + 0.7,
            stroke_opacity=0,
            fill_opacity=0,
        ).move_to([VECTOR_X, (ROW_YS[0] + ROW_YS[3]) / 2, 0])
        vector = VGroup(Brace(anchor, LEFT), stack, Brace(anchor, RIGHT))

        phi_label = MathTex(r"\Phi", color=FOREGROUND).scale(2.0).move_to(
            [VECTOR_X, GREEK_Y, 0]
        )

        # --- Animate -------------------------------------------------
        self.play(Write(title), run_time=0.6)
        self.play(
            Create(dashed_lines, lag_ratio=0.1),
            Create(solid_line),
            run_time=0.9,
        )
        # Numerator piles top to bottom — the ⋮ comes in at the start,
        # together with the first piles (not with the math operation).
        self.play(
            FadeIn(numerators[0], shift=DOWN * 0.15),
            Write(sieve_dots),
            run_time=0.5,
        )
        for num in numerators[1:]:
            self.play(FadeIn(num, shift=DOWN * 0.15), run_time=0.4)
        # Math operation: slashes + denominator piles.
        self.play(
            *[Create(sl) for sl in slashes],
            *[FadeIn(d, shift=DOWN * 0.1) for d in denominators],
            run_time=0.9,
        )
        # Vector brace + entries + Φ label.
        self.play(
            FadeIn(vector[0]),
            FadeIn(vector[2]),
            *[Write(e) for e in entries],
            run_time=1.0,
        )
        self.play(Write(phi_label), run_time=0.5)
        self.wait(2.5)

        # Stash for the seamless Scene 2 → Scene 3 transition (used by
        # FullStoryV2 if it wants to keep the lines and just fade the rest).
        self._dashed_lines = dashed_lines
        self._solid_line = solid_line
        self._numerators = numerators
        self._denominators = denominators
        self._slashes = slashes
        self._sieve_dots = sieve_dots
        self._vector = vector
        self._phi = phi_label
        self._title = title
