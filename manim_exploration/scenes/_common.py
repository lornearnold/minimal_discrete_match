"""Shared geometry, colors, and helpers for MDM storyboard scenes.

Design language (set here once, inherited by every scene):

- Background: black (3Blue1Brown style).
- Foreground (sieves, axes, text): white.
- Particle tiers: COARSE / MID / FINE, using manim's default 3B1B palette
  (RED = #FC6255, BLUE = #58C4DD, GREEN = #83C167).
- Mesh openings are sized to the particles they retain: a sieve's openings
  are larger than the next-finer particle tier and smaller than its own.
"""

from __future__ import annotations

import numpy as np
from manim import (
    BLACK,
    BLUE,
    GREEN,
    RED,
    WHITE,
    Circle,
    Line,
    VGroup,
    interpolate_color,
)

# ---- Colors -----------------------------------------------------------------

BACKGROUND = BLACK
FOREGROUND = WHITE  # sieves, axes, text

COARSE = RED
MID = BLUE
FINE = GREEN

# ---- Particle sizes (scene units; "diameter" = 2 * radius) ------------------

COARSE_R = 0.30
MID_R = 0.18
FINE_R = 0.10

# ---- Sieve openings (must satisfy coarse_d > top_opening > mid_d, etc.) -----

TOP_OPENING = 0.45     # > 2*MID_R = 0.36, < 2*COARSE_R = 0.60
MID_OPENING = 0.28     # > 2*FINE_R = 0.20, < 2*MID_R = 0.36
BOTTOM_OPENING = 0.14  # < 2*FINE_R = 0.20 (retains fines)

# ---- Sieve plate geometry ---------------------------------------------------

SIEVE_WIDTH = 4.0          # x-extent in scene units
SIEVE_DEPTH = 1.6          # y-extent (perspective foreshortening)
SIEVE_SKEW = 1.0           # x-shift applied to the back edge for parallax
SIEVE_VERTICAL_GAP = 1.8   # vertical separation between stacked sieves


def sieve_plate(
    opening_size: float,
    width: float = SIEVE_WIDTH,
    depth: float = SIEVE_DEPTH,
    skew: float = SIEVE_SKEW,
    stroke: float = 2.0,
) -> VGroup:
    """A parallelogram sieve plate whose mesh cell size matches `opening_size`.

    The mesh-line count is derived from the plate dimensions so that one cell
    of the rendered mesh corresponds to one physical sieve opening.
    """
    n_cells_x = max(1, int(round(width / opening_size)))
    n_cells_y = max(1, int(round(depth / opening_size)))

    fl = np.array([0.0, 0.0, 0.0])
    fr = np.array([width, 0.0, 0.0])
    br = np.array([width + skew, depth, 0.0])
    bl = np.array([skew, depth, 0.0])

    border = VGroup(
        Line(fl, fr, stroke_width=stroke),
        Line(fr, br, stroke_width=stroke),
        Line(br, bl, stroke_width=stroke),
        Line(bl, fl, stroke_width=stroke),
    )

    mesh = VGroup()
    for i in range(1, n_cells_x):
        t = i / n_cells_x
        mesh.add(Line(fl + t * (fr - fl), bl + t * (br - bl), stroke_width=stroke * 0.5))
    for j in range(1, n_cells_y):
        t = j / n_cells_y
        mesh.add(Line(fl + t * (bl - fl), fr + t * (br - fr), stroke_width=stroke * 0.5))

    plate = VGroup(border, mesh)
    plate.set_color(FOREGROUND)
    return plate


def make_particle(
    radius: float,
    color,
    stroke_width: float = 2.0,
    fill_opacity: float = 1.0,
    fill_lighten: float = 0.55,
) -> Circle:
    """A particle drawn as a single disk with a colored rim and lighter fill.

    The colored stroke (in the tier color) keeps overlapping particles
    visually separable; the lighter fill (interpolated toward white) avoids
    the flat poster-paint look without resorting to a 3D highlight.

    `fill_lighten` is the interpolation factor toward white: 0 keeps the
    fill identical to the stroke, 1 makes the fill pure white.
    """
    fill_color = interpolate_color(color, WHITE, fill_lighten)
    return Circle(
        radius=radius,
        color=color,
        stroke_width=stroke_width,
        fill_color=fill_color,
        fill_opacity=fill_opacity,
    )


def particle_cluster(
    count: int,
    radius: float,
    color,
    bbox: tuple[float, float] = (1.5, 0.8),
    seed: int = 0,
    stroke_width: float = 1.5,
) -> VGroup:
    """A deterministic-grid cluster of `count` open circles.

    Used for the static piles in `pile_to_gsd.py`. The grid layout (vs random
    scatter) keeps Transform animations between cluster sizes smooth.
    """
    bw, bh = bbox
    cols = max(1, int(np.ceil(np.sqrt(count * bw / max(bh, 1e-6)))))
    rows = int(np.ceil(count / cols))

    dx = bw / cols
    dy = bh / rows

    rng = np.random.default_rng(seed)
    cluster = VGroup()
    for k in range(count):
        i = k % cols
        j = k // cols
        x = -bw / 2 + dx * (i + 0.5) + rng.uniform(-dx * 0.05, dx * 0.05)
        y = -bh / 2 + dy * (j + 0.5) + rng.uniform(-dy * 0.05, dy * 0.05)
        cluster.add(make_particle(radius, color, stroke_width).move_to([x, y, 0]))
    return cluster


def mixed_cloud(
    n_coarse: int,
    n_mid: int,
    n_fine: int,
    center: tuple[float, float],
    width: float = 2.4,
    height: float = 1.0,
    seed: int = 7,
) -> VGroup:
    """A visually mixed cloud of particles above the sieve stack.

    Particles of all three tiers are interleaved (not grouped by color) so the
    initial frame reads as one heterogeneous sample, mirroring physical reality.
    The returned VGroup carries a `.tier` attribute on each child: a string in
    {"coarse", "mid", "fine"} that downstream code uses to route each particle
    to its destination sieve.
    """
    rng = np.random.default_rng(seed)

    # Build a flat list of (tier, radius, color), then shuffle so colors
    # interleave spatially when we lay them out.
    items: list[tuple[str, float, object]] = (
        [("coarse", COARSE_R, COARSE)] * n_coarse
        + [("mid", MID_R, MID)] * n_mid
        + [("fine", FINE_R, FINE)] * n_fine
    )
    rng.shuffle(items)

    cx, cy = center
    cloud = VGroup()
    for tier, r, color in items:
        x = cx + rng.uniform(-width / 2, width / 2)
        y = cy + rng.uniform(-height / 2, height / 2)
        circle = make_particle(r, color).move_to([x, y, 0])
        circle.tier = tier  # stash for routing in the falling animation
        cloud.add(circle)
    return cloud
