# Scene Notes

Use this file to capture suggested changes for each Manim scene. Add bullets under the relevant scene.

## sieve_stack.py — `SieveStack`

- start out with many more particles

## continuum_reveal.py — `ContinuumReveal`

- rename to "DefiningG"

## defining_s.py - `DefiningS`

Show subsets for about one second (still with many particles)2 that have different total numbers of particles, but the same GSD. Show an integer for each size in each subset that is not expected to be a minimum. Make the integers large. and feel free to crowd the number of particles in each range to illustrate that there are a lot.

In the very last frame, show only one particle in each size range, with a big question mark over the top, indicating that we're looking for the Minimal Discrete Match, but we don't know exactly what it wil be

## mass ratio

Change the mass representation from several particles to an amorphous blob with "M_x" inscribed.

## volume ratio

## quantity ratio

Take the illustrations of mass ratio and volume ratio and show them being multiplied (graphic x graphic) and equaling a vector that's labeled "Quantity Ratio".

The quantity ratio vector should have 1 in the first entry and then "?.?" in the other entries, indicating that except for the largest size, other quantities are not guaranteed to be integers.

## rounding approach

Take the numbers from the MDM storyboard sketch and show a discrete match with rounded integers, and then also show that there's error between the target GSD and the actual GSD.

## reducing error

Show the sequence of increasing the total number of particles and reducing the error to at least 3 iterations, with the error going down with each iteration.

## spanned integer approach (revised — for high school / general audience)

This is the climax of the video. The audience is a general one (high school
program), so the goal is to TELL the story, not prove the algorithm.

### What the visual must communicate (in order)

1. Within each sieve range, we get to pick the size of the representative
   particle.
2. If we pick the LARGEST size in each range, we get a count called K₊.
3. If we pick the SMALLEST size in each range, we get a count called K₋.
4. If a whole number sits between K₊ and K₋ for each range — bingo! a size
   exists that gives an integer count and matches the target exactly.
5. The error drops to numerical zero. That's the Minimal Discrete Match.

### Audience simplifications (do NOT do)

- Do NOT show the iteration step (SI₃/SI₄). Assume the spanned integer exists
  on the first try.
- Do NOT show a number line with integer ticks. Too abstract for the audience.
- Do NOT show step SI₆ math (`X = f⁻¹(Φ/Q)`). The merge animation is enough.
- Do NOT introduce notation beyond `K`, `K₊`, `K₋`.

### Beat-by-beat

#### Beat 0 — Carry-over cleanup (~0.5 s)
Audience just watched FS-iter-3 end with [3, 14, 36] particles. Title swaps to
"Spanned-integer approach." When this happens, also fade out the residual
artifacts from the FS scene: the "× 3" multiplier above the curved arrow and
any leftover dashed-line fragments hanging near the error bar.

The pile reduces to ONE representative particle per tier, all sized at the
midrange of their sieve interval. The K vector reads (1, 4.6, 12.1). Chart and
error bar reset to "moderate error" (whatever a midrange size produces — not
zero, not extreme).

#### Beat 1 — Particles GROW to the largest sizes → K₊ (~1.5 s)
Each particle smoothly grows to the largest allowable size (touching the upper
sieve datum line in its band). Run as ONE continuous animation, not a fade:

- Particle radii animate from midrange → MID_R_HI / FINE_R_HI / COARSE_R.
- The K vector entries morph continuously: "4.6" → "4.1", "12.1" → "11.8".
  ("1" stays at "1".)
- The bracket label gains a `+` subscript: `K` → `K₊`.

Simultaneously, the chart's realized curve slides BELOW the target (fewer big
particles → less mass at the fines end), and the error bar grows red, well
above tolerance.

Optional in-frame caption: *"Use the LARGEST size in each range → K₊"*

#### Beat 2 — Particles SHRINK to the smallest sizes → K₋ (~1.5 s)
Particles smoothly shrink to the smallest allowable size (touching the lower
sieve datum line). The K₊ entries STAY on screen. The K₋ values fade in just
below each K₊ value inside the same bracket — so the bracket reads as pairs:

```
   K₊  K₋
    1   1   ← coarse (K₋ = K₊ here, can be a single "1")
   4.1 6.8  ← mid
  11.8 13.4 ← fine
```

A `−` subscript appears below: the bracket now spans both `K₊` (above) and `K₋`
(below). The chart adds a SECOND realized curve, this one ABOVE the target
(more small particles → more mass at fines). Error bar stays red.

Optional in-frame caption: *"Use the SMALLEST size → K₋"*

#### Beat 3 — The "BINGO" reveal (~2 s) — STANDALONE BEAT
This is the climax. NOTHING else moves on screen during this beat.

For each tier, draw a thin colored connector (or a small bracket) on the right
side of the K vector, linking that tier's K₊ and K₋ entries. Inside this
connector, the spanned integer pops in with a quick scale animation
(0.6× → 1.4× → 1.0×) in a bright contrast color (white or yellow):

- coarse tier: 1
- mid tier: 5 (visually centered between 4.1 and 6.8)
- fine tier: 12 (visually centered between 11.8 and 13.4)

Centered caption (large): *"A whole number is between them!"*

Hold ~2 s. Chart and error bar do NOT change yet. This is the audience's
moment to feel the click — it MUST land on its own, not buried under the
particle merge or chart snap. Do not run the merge inside the same `self.play`
as the integer reveal.

#### Beat 4 — Resolution: the right size exists, error → 0 (~1.5 s)
Now everything resolves at once:

- The two particles per tier (large + small) merge into a single
  intermediate-size particle. Use the existing `_interp_radius` math; no need
  to compute the true `f⁻¹(Φ/Q)`.
- The chart's two realized curves (above-target and below-target) collapse onto
  the target as a single white curve.
- The error bar drops to numerical zero (or into the green tolerance zone).

Optional caption: *"…the right size exists. Error → 0."*

#### Beat 5 — Label as MDM (~hold for outro)
Box draws around {merged particles + spanned integer column}. Caption
underneath in red: *"Minimal Discrete Match"*. Hold ~3–5 s through the outro
narration.

### Visual hygiene notes

- Captions: one per beat, fade in / fade out cleanly, never overlap. They are
  reinforcement for narration, not a script.
- Color palette: keep coarse / mid / fine consistent with earlier scenes.
  Check that the pink/coral/red shades are distinguishable on a projector.
- Title "Spanned-integer approach" stays pinned at the top throughout.
- The spanned integers (1, 5, 12) are the same numbers as FS-iter-0; do NOT
  call attention to this — it would distract from the "no error" punchline.

# Verification

Show a version of the comparison of MDM-predicted sample sizes for scaled GSDs in Z study from the minimial packing manuscript.


