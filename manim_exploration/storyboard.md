# Storyboard

What each Manim scene shows and the conceptual beat it carries. Scenes are
listed in narrative order — the order a viewer would watch them — which is
not the same as the order they were built. Page numbers refer to
`MDM_storyboard.pdf`.

The visual grammar is shared across scenes: black background, white
foreground, three particle tiers `COARSE`/`MID`/`FINE` (red/blue/green) at
fixed radii (0.30 / 0.18 / 0.10), and dashed horizontal "datum" lines that
stand in for sieve plates when the sieves themselves aren't drawn. See
`scenes/_common.py` for the shared definitions.

---

## `SieveStack` — `scenes/sieve_stack.py` (pages 0–2)

**Beat 0 — the raw sample.** A heterogeneous cloud of ~95 particles fills
the frame: 8 coarse + 22 mid + 65 fine, colors interleaved (not grouped) so
the cloud reads as one mixed sample.

**Beat 1 — staging.** The cloud condenses into a tight blob above where
the sieve stack is about to appear. Three sieve plates fade in from below,
stacked top-to-bottom with progressively smaller mesh openings.

**Beat 2 — drop and sort.** Particles fall at constant speed (run_time
proportional to fall distance) and each one settles on the first plate
whose mesh openings cannot pass it. Resting positions are sampled across
the plate's depth (not just along the front edge) so each retained pile
reads as a real spread of grains. Coarse lands first, fines last.

The same Mobjects persist across all three beats so transitions are
smooth `Transform`s, not re-creates.

---

## `PileToGSD` — `scenes/pile_to_gsd.py` (page 3)

**Left half.** Three retained piles (4 / 7 / 12 particles), scattered with
natural jitter so they don't read as a regular grid, separated by dashed
sieve datums (drawn as datums rather than full plates).

**Right half.** Axes labeled `grain size` × `Mass`. Three colored bars,
each spanning one sieve interval and reaching the cumulative mass at the
right edge. Bar colors run green → blue → red across the x-axis. No
smooth curve and no polyline — this is the honest discrete picture.

Caption: "Three sieves give a coarse picture — real soil holds many more
sizes." This sets up the next scene.

> The bar visualization keeps the cumulative-mass framing while making
> the "we only know mass at a few sizes" limitation visible. As the next
> scene refines the bar count, the staircase converges visually toward
> the smooth GSD curve without ever being drawn explicitly.

---

## `ContinuumReveal` — `scenes/continuum_reveal.py` (bridge scene)

Starts on the exact end-state of `PileToGSD`: three stratified piles +
dashed sieve datums on the left, three colored bars on the right.

Then refines in three steps:

1. **3 → 5 bars.** Sieve datums fade out; ~30 continuum particles trickle
   in across the whole left half.
2. **5 → 9 bars.** ~50 more particles.
3. **9 → 15 bars.** ~80 more particles.

New particles fill the entire left half. Each particle's radius is
determined by its y-position (largest at the top, smallest at the
bottom), so the original three stratified tiers blend in naturally rather
than overlaying as a separate cloud. Colors follow the FINE → MID →
COARSE gradient by radius. Existing pile particles act as fixed obstacles
during placement, with a small overlap budget so the cloud can densify.

Caption: "More sizes — finer approximation. The smooth curve is the
limit."

The viewer reads this as: more sieves give a finer staircase, and more
particle sizes are the continuum that the GSD curve was always
describing.

---

## `MassRatios` — `scenes/ratios.py` (page 4)

Three datum-separated rows, coarse on top. Each row shows that tier's
full retained pile (numerator) over the coarse retained pile
(denominator), separated by a diagonal slash. The denominator is the
*same coarse pile* on every row — repeated three times to make the "÷ M_1"
operation visible.

A right-side brace gathers the resulting mass-ratio vector:

```
{ M_1/M_1,  M_2/M_1,  M_3/M_1 }
```

Coarse-tier expression is colored red, mid blue, fine green, matching the
piles. The takeaway: each tier's *bulk mass* compared to the reference
tier — the ratio that the GSD itself encodes.

---

## `VolumeRatios` — `scenes/ratios.py` (page 5)

Same three-row layout as `MassRatios`, but with single particles instead
of piles. On every row the numerator is **one coarse particle**; the
denominator is one particle of that row's tier. The right-side brace
encloses the per-particle volume-ratio vector:

```
{ M(x_1)/M(x_1),  M(x_1)/M(x_2),  M(x_1)/M(x_3) }
```

This is `ζ_i = (x_1 / x_i)^3` — how many times heavier the coarse particle
is than one particle of size `x_i`. Numerically (from the radii in
`_common.py`): 1, 4.63, 27.

> **Note:** the hand storyboard drew this inverted as `M(x_i)/M(x_1)`
> (small over big). The animation flips it to match the paper, where the
> volume ratio is always large-over-small.

---

## Coming next (not yet implemented)

- **Quantity ratios** (page 6): `q_i = (M_i/M_1) · ζ_i` — the integer
  count of size-`x_i` particles needed to match the coarse mass on that
  sieve. Visually: 1 coarse / 5 mid / 12 fine, drawn as discrete particle
  groups with the bracket showing the numeric vector.
- **Error / iteration** (pages 7–10): the same row layout as quantity
  ratios, but now the discrete counts produce a step-function GSD that
  trails the smooth target curve. The error shrinks as counts scale up
  (1→2→3 coarse, 5→9→14 mid, 12→24→36 fine).
- **Spanned-integer payoff** (page 11): with the size of the
  representative particle allowed to slide within a sieve interval, the
  K-vector hits an integer lattice point exactly, and the iteration
  collapses to a single step.
