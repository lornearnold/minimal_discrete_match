"""Bridge scene: 3 sieves -> 15 sieves, with the left half filling in.

Starts on the exact end state of `PileToGSD` (three stratified piles +
dashed sieve datums on the left, three colored bars on the right). Then
refines in three steps:

  step 1: 3 -> 5 bars; datums fade out; ~30 continuum particles trickle in.
  step 2: 5 -> 9 bars; ~50 more particles.
  step 3: 9 -> 15 bars; ~80 more particles.

New particles fill the whole left half; their radius is determined by
their y-position (largest at the top). Because the original three piles
were already stratified that way, the continuum particles blend in around
them rather than overlaying as a separate cloud.

The viewer reads this as: "more sieves -> finer approximation, more
particle sizes -> the continuum that the GSD curve was always describing."
"""

from __future__ import annotations

import numpy as np
from manim import (
    WHITE,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    Scene,
    Text,
    UP,
    VGroup,
    VMobject,
    Write,
    config,
)

from _common import (
    BACKGROUND,
    COARSE_R,
    FINE_R,
    FOREGROUND,
    MID_R,
    build_gsd_bars,
    continuum_color,
    make_particle,
    target_func,
    y_to_radius,
)

# Reuse the layout + builders from PileToGSD so the two scenes line up.
from pile_to_gsd import (
    DATUM_YS,
    PILE_X,
    SIEVE_XS_3,
    X_LEFT,
    build_axes_and_labels,
    build_datums,
    build_piles,
)

config.background_color = BACKGROUND


# Continuum radius range. Chosen so y_to_radius across the screen lands
# the original tier sizes near their respective bands (top -> coarse-ish,
# bottom -> fine-ish), letting the originals blend in.
R_MIN_NEW = 0.05
R_MAX_NEW = 0.34

# Vertical extent of the left-half cloud.
Y_SCREEN_LO, Y_SCREEN_HI = DATUM_YS[-1], DATUM_YS[0]  # bottom and top datums


def _try_place(
    radius: float,
    y: float,
    obstacles: list[tuple[np.ndarray, float]],
    rng: np.random.Generator,
    tries: int = 50,
    overlap_tolerance: float = 1.04,
) -> np.ndarray | None:
    """Find an x-position in PILE_X for a particle of `radius` at height `y`.

    Returns None if no spot with acceptable overlap is found. We allow a
    small overlap budget so the cloud can densify even when packing is
    tight; the colored strokes keep particles legible.
    """
    x_lo, x_hi = PILE_X
    best_pos = None
    best_overlap = np.inf
    for _ in range(tries):
        x = rng.uniform(x_lo + radius, x_hi - radius)
        pos = np.array([x, y, 0.0])
        overlap = sum(
            max(0.0, (radius + er) * overlap_tolerance - np.linalg.norm(pos - ep))
            for ep, er in obstacles
        )
        if overlap < best_overlap:
            best_overlap = overlap
            best_pos = pos
            if overlap == 0.0:
                return pos
    # Accept the best-found spot if its overlap is modest.
    if best_overlap < radius * 0.6:
        return best_pos
    return None


def _generate_batch(
    n: int,
    obstacles: list[tuple[np.ndarray, float]],
    rng: np.random.Generator,
) -> VGroup:
    """Generate `n` continuum particles whose radius follows their y."""
    batch = VGroup()
    for _ in range(n):
        y = rng.uniform(Y_SCREEN_LO + 0.1, Y_SCREEN_HI - 0.1)
        r = y_to_radius(y, Y_SCREEN_LO, Y_SCREEN_HI, R_MIN_NEW, R_MAX_NEW)
        # A little vertical jitter so the size-vs-y rule isn't a perfect
        # gradient — helps the originals blend in.
        y_j = y + rng.uniform(-0.15, 0.15)
        pos = _try_place(r, y_j, obstacles, rng)
        if pos is None:
            continue
        color = continuum_color(r, R_MIN_NEW, R_MAX_NEW)
        batch.add(make_particle(r, color).move_to(pos))
        obstacles.append((pos, r))
    return batch


class DefiningG(Scene):
    def construct(self):
        rng = np.random.default_rng(17)

        skip_setup = getattr(self, "_skip_continuum_setup", False)

        if skip_setup:
            # Reuse axes/bars stashed by PileToGSD; obstacles are inferred
            # from whatever circular particles are already on screen.
            axes = self.axes
            bars = self.bars
            datums = getattr(self, "datums", VGroup())
            obstacles: list[tuple[np.ndarray, float]] = []
            for m in self.mobjects:
                # Picks up Circle particles regardless of which scene placed them.
                if hasattr(m, "radius") and m.get_center()[0] < 0:
                    obstacles.append((m.get_center(), float(m.radius)))
        else:
            # ---- Reproduce PileToGSD's end state exactly. ----
            # Use the same RNG seed so the piles render in the same positions.
            init_rng = np.random.default_rng(13)
            coarse_pile, mid_pile, fine_pile = build_piles(init_rng)

            datums = build_datums()
            axes, x_label, y_label = build_axes_and_labels()
            bars = build_gsd_bars([X_LEFT, *SIEVE_XS_3], axes)

            self.add(
                datums, coarse_pile, mid_pile, fine_pile,
                axes, x_label, y_label, bars,
            )
            self.wait(0.7)

            # ---- Existing pile particles act as fixed obstacles. ----
            obstacles = []
            for pile, r in (
                (coarse_pile, COARSE_R),
                (mid_pile, MID_R),
                (fine_pile, FINE_R),
            ):
                for p in pile:
                    obstacles.append((p.get_center(), r))

        # ---- Refinement schedule: (n_sieves, n_new_particles). ----
        steps = [(5, 30), (9, 50), (15, 80)]

        prev_bars = bars
        first_step = True

        for n_sieves, n_new in steps:
            new_edges = list(np.linspace(X_LEFT, SIEVE_XS_3[-1], n_sieves + 1))
            new_bars = build_gsd_bars(new_edges, axes)

            new_particles = _generate_batch(n_new, obstacles, rng)

            anims = [
                FadeOut(prev_bars),
                FadeIn(new_bars),
                FadeIn(new_particles, lag_ratio=0.04),
            ]
            if first_step:
                anims.append(FadeOut(datums))
                leftover_note = getattr(self, "_note_mob", None)
                if leftover_note is not None:
                    anims.append(FadeOut(leftover_note))
                first_step = False

            self.play(*anims, run_time=1.6)
            prev_bars = new_bars

        caption = Text(
            "More sizes — finer approximation.\n"
            "The smooth curve is the limit.",
            font_size=22,
            color=FOREGROUND,
        ).to_edge(UP, buff=0.35)
        self.play(Write(caption), run_time=1.2)

        # ---- Draw G: the smooth target curve over the bar tops. ----
        final_n_sieves = steps[-1][0]
        final_edges = list(np.linspace(X_LEFT, SIEVE_XS_3[-1], final_n_sieves + 1))
        xs_dense = np.linspace(final_edges[0], final_edges[-1], 120)
        curve_pts = [axes.c2p(x, target_func(x)) for x in xs_dense]
        g_curve = VMobject(stroke_color=WHITE, stroke_width=4)
        g_curve.set_points_smoothly(curve_pts)

        bar_top_dots = VGroup(
            *[
                Dot(axes.c2p(x, target_func(x)), color=WHITE, radius=0.06)
                for x in final_edges[1:]
            ]
        )

        g_label = Text("G", font_size=64, color=WHITE).move_to(
            axes.c2p(final_edges[-1] - 0.25, target_func(final_edges[-1]) + 0.55)
        )

        self.play(Create(g_curve), FadeIn(bar_top_dots), run_time=1.5)
        self.play(Write(g_label), run_time=0.7)

        self.wait(2.5)


# Backwards-compat alias.
ContinuumReveal = DefiningG
