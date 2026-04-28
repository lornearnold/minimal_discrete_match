"""Storyboard pages 0-2: raw sample -> stacked sieves -> sorted result.

Story beats:
  0. (Storyboard "missing page".) A wide, heterogeneous cloud of particles
     fills the frame — the raw soil sample, before any sieving.
  1. The cloud condenses to a tight staging area; sieves enter from below.
  2. Particles fall. Each settles on the first sieve whose openings cannot
     pass it, landing spread across the plate's depth (not just the front
     edge), so the result reads like a real retained-on-sieve pile.
"""

from __future__ import annotations

import numpy as np
from manim import (
    DOWN,
    UP,
    FadeIn,
    Scene,
    VGroup,
    config,
    rate_functions,
)

from _common import (
    BACKGROUND,
    BOTTOM_OPENING,
    COARSE,
    COARSE_R,
    FINE,
    FINE_R,
    MID,
    MID_OPENING,
    MID_R,
    SIEVE_DEPTH,
    SIEVE_SKEW,
    SIEVE_VERTICAL_GAP,
    SIEVE_WIDTH,
    TOP_OPENING,
    make_particle,
    sieve_plate,
)

config.background_color = BACKGROUND


# Map each tier to (destination plate index, particle radius).
TIER_DESTINATION = {
    "coarse": (0, COARSE_R),
    "mid": (1, MID_R),
    "fine": (2, FINE_R),
}


class SieveStack(Scene):
    def construct(self):
        rng = np.random.default_rng(7)

        # ---- Build the particle cloud once. We re-use the same Mobjects for
        # all three beats (wide cloud -> condensed staging -> sorted on
        # plates) so transitions are smooth Transforms rather than re-creates.
        n_coarse, n_mid, n_fine = 8, 22, 65
        items = (
            [("coarse", COARSE_R, COARSE)] * n_coarse
            + [("mid", MID_R, MID)] * n_mid
            + [("fine", FINE_R, FINE)] * n_fine
        )
        rng.shuffle(items)  # interleave colors so the cloud looks heterogeneous

        cloud = VGroup()
        for tier, r, color in items:
            wx = rng.uniform(-5.5, 5.5)
            wy = rng.uniform(-1.8, 2.2)
            p = make_particle(r, color).move_to([wx, wy, 0])
            p.tier = tier  # used by the fall step to route to a sieve
            cloud.add(p)

        # ---- Beat 0: the raw sample.
        self.play(FadeIn(cloud), run_time=1.2)
        self.wait(1.0)

        # ---- Beat 1: condense the cloud above where the sieves will appear,
        # while the sieve stack fades in from below.
        plates = VGroup(
            sieve_plate(opening_size=TOP_OPENING),
            sieve_plate(opening_size=MID_OPENING),
            sieve_plate(opening_size=BOTTOM_OPENING),
        )
        for i, plate in enumerate(plates):
            plate.shift(UP * (SIEVE_VERTICAL_GAP * (1 - i)))
        plates.move_to([0, -0.3, 0])

        spawn_x = plates[0].get_center()[0]
        spawn_y = plates[0].get_top()[1] + 1.4

        condense_anims = []
        for p in cloud:
            cx = spawn_x + rng.uniform(-1.4, 1.4)
            cy = spawn_y + rng.uniform(-0.45, 0.45)
            condense_anims.append(p.animate.move_to([cx, cy, 0]))

        self.play(
            *condense_anims,
            *[FadeIn(plate, shift=DOWN * 0.3) for plate in plates],
            run_time=1.4,
        )
        self.wait(0.4)

        # ---- Beat 2: drop and sort. Per-particle run_time proportional to
        # distance gives uniform fall speed — coarse particles land first
        # (shortest fall), fines land last, narrating the sieving sequence.
        fall_speed = 5.5  # scene units per second

        # Margin on the plate where particles can rest (avoid edges).
        u_lo, u_hi = 0.06, 0.94
        v_lo, v_hi = 0.10, 0.90

        anims = []
        for p in cloud:
            plate_idx, r = TIER_DESTINATION[p.tier]
            target_plate = plates[plate_idx]

            # Sample a random (u, v) on the plate's surface. u runs along the
            # left-right direction, v from the front edge toward the back. The
            # parallax skew shifts back-of-plate points to the right.
            u = rng.uniform(u_lo, u_hi)
            v = rng.uniform(v_lo, v_hi)

            front_left_x = target_plate.get_left()[0]
            front_y = target_plate.get_bottom()[1]

            rest_x = front_left_x + u * SIEVE_WIDTH + v * SIEVE_SKEW
            rest_y = front_y + v * SIEVE_DEPTH + r * 1.05

            # Stack particles back-to-front: high v (back) draws first
            # (lower z_index), so front particles overlap back ones.
            p.set_z_index(int((1.0 - v) * 100))

            distance = max(0.1, p.get_y() - rest_y)
            duration = max(0.3, distance / fall_speed)

            anims.append(
                p.animate(
                    run_time=duration, rate_func=rate_functions.linear
                ).move_to([rest_x, rest_y, 0])
            )

        self.play(*anims)
        self.wait(1.5)
