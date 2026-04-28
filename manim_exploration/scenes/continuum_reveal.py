"""Bridge scene: a continuous spectrum of grain sizes <-> the smooth GSD curve.

The other scenes use only three discrete particle tiers for clarity, but real
soil contains a continuum of grain sizes. This beat establishes that
correspondence once: a wide cloud of particles with many different radii on
the left, paired with the smooth cumulative-mass curve on the right. After
this, viewers can accept the three-tier simplification used elsewhere.

There are no sieve lines or sorting in this scene — the message is purely
"the smooth curve represents a real continuum of sizes."
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    RIGHT,
    UP,
    Axes,
    Create,
    FadeIn,
    Scene,
    Text,
    VGroup,
    Write,
    config,
    interpolate_color,
)

from _common import (
    BACKGROUND,
    COARSE,
    COARSE_R,
    FINE,
    FINE_R,
    FOREGROUND,
    MID,
    make_particle,
)

config.background_color = BACKGROUND


# Continuous radius range. Much wider than the three-tier scenes use, so the
# spectrum reads as a true continuum rather than three blurred categories.
R_MIN = FINE_R * 0.3   # ~0.03 — visibly tiny grains
R_MAX = COARSE_R * 1.3  # ~0.39 — clearly larger than the COARSE tier

# Particle count — big enough that no two adjacent radii feel like a "tier".
N_PARTICLES = 280


def continuum_color(radius: float, r_min: float = R_MIN, r_max: float = R_MAX):
    """Map a radius to a color along the FINE -> MID -> COARSE gradient.

    Smaller particles take on the FINE (green) hue, mid-sized particles the
    MID (blue) hue, and the largest particles the COARSE (red) hue. Provides
    visual continuity with the three-tier scenes without quantizing.
    """
    t = (radius - r_min) / (r_max - r_min)
    t = float(np.clip(t, 0.0, 1.0))
    if t < 0.5:
        return interpolate_color(FINE, MID, t * 2.0)
    return interpolate_color(MID, COARSE, (t - 0.5) * 2.0)


def place_with_soft_packing(
    radii: np.ndarray,
    bbox: tuple[float, float, float, float],
    rng: np.random.Generator,
    tries_per_particle: int = 30,
    overlap_tolerance: float = 1.05,
) -> list[np.ndarray]:
    """Greedy placement: each particle picks the trial position with the
    fewest overlaps. Place largest particles first so the big ones get prime
    real estate.

    Some overlap is expected and acceptable — the colored strokes keep
    overlapping particles readable.
    """
    x_lo, y_lo, x_hi, y_hi = bbox
    order = np.argsort(-radii)  # descending
    placed: list[tuple[np.ndarray, float]] = []
    positions: list[np.ndarray | None] = [None] * len(radii)

    for idx in order:
        r = radii[idx]
        best_pos = None
        best_overlap = np.inf
        for _ in range(tries_per_particle):
            x = rng.uniform(x_lo + r, x_hi - r)
            y = rng.uniform(y_lo + r, y_hi - r)
            pos = np.array([x, y, 0.0])
            overlap = sum(
                max(0.0, (r + er) * overlap_tolerance - np.linalg.norm(pos - ep))
                for ep, er in placed
            )
            if overlap < best_overlap:
                best_overlap = overlap
                best_pos = pos
                if overlap == 0.0:
                    break
        positions[idx] = best_pos
        placed.append((best_pos, r))

    return positions


class ContinuumReveal(Scene):
    def construct(self):
        rng = np.random.default_rng(11)

        # ---- Sample radii log-uniformly so all decades are represented.
        log_radii = rng.uniform(np.log(R_MIN), np.log(R_MAX), N_PARTICLES)
        radii = np.exp(log_radii)

        # Place particles on the left half of the frame. Wider bbox + more
        # placement tries to absorb the larger particle count gracefully.
        cloud_bbox = (-6.8, -3.0, -0.3, 3.0)
        positions = place_with_soft_packing(
            radii, cloud_bbox, rng, tries_per_particle=50
        )

        cloud = VGroup()
        for r, pos in zip(radii, positions):
            cloud.add(make_particle(r, continuum_color(r)).move_to(pos))

        self.play(FadeIn(cloud), run_time=1.4)
        self.wait(0.8)

        # ---- Smooth GSD curve on the right.
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
        y_label = Text("Mass", font_size=22, color=FOREGROUND).next_to(
            axes.y_axis, UP, buff=0.15
        )

        def curve_func(x):
            return 0.4 + 3.2 / (1 + np.exp(-2.2 * (x - 2.0)))

        curve = axes.plot(
            curve_func, x_range=[0.3, 3.8], color=FOREGROUND, stroke_width=3
        )

        self.play(Create(axes), Write(x_label), Write(y_label), run_time=0.9)
        self.play(Create(curve), run_time=1.0)

        # ---- Caption establishing the correspondence.
        caption = Text(
            "Real soil holds a continuum of grain sizes —\n"
            "the smooth curve captures them all at once.",
            font_size=22,
            color=FOREGROUND,
        ).to_edge(UP, buff=0.35)
        self.play(Write(caption), run_time=1.2)

        self.wait(2.0)
