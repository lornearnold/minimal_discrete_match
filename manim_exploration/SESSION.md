# Session recovery — manim_exploration storyboard work

sfsdfasdf

Snapshot of an in-progress session. Hand this file (or its path) to a new
Claude conversation to pick up the thread.

## Goal

Implement every storyboard beat in `NOTES.md` as a Manim scene, plus a
master scene that stitches them together.

## Files of interest

- `NOTES.md` — per-scene change requests (the brief).
- `storyboard.md` — narration / order.
- `MDM_storyboard.pdf` — hand sketches; canonical for the rounding-error
  visualization and the spanned-integer page.
- `../minimal_packing_manuscript/minimal_packing.qmd` — manuscript;
  canonical for the verification scene's `fig-demo`.
- `scenes/_common.py` — shared colors, particle/sieve helpers (unchanged).

## Scenes implemented

| File                          | Class(es)                                      | Status                                                  |
|-------------------------------|------------------------------------------------|---------------------------------------------------------|
| `sieve_stack.py`              | `SieveStack`                                   | bumped to 18/55/160 particles                           |
| `pile_to_gsd.py`              | `PileToGSD`                                    | unchanged                                               |
| `continuum_reveal.py`         | `DefiningG` (alias `ContinuumReveal`)          | renamed per NOTES                                       |
| `defining_s.py`               | `DefiningS`                                    | new — three crowded subsets → `?` + MDM caption         |
| `ratios.py`                   | `MassRatios`, `VolumeRatios`                   | `MassRatios` now uses amorphous blobs labeled `M_i/M_1` |
| `quantity_ratio.py`           | `QuantityRatio`                                | new — mass × volume = quantity, `[1, ?.?, ?.?]`         |
| `rounding.py`                 | `RoundingApproach`, `ReducingError`            | redone to match storyboard layout (curve + dots + band) |
| `spanned_integer.py`          | `SpannedIntegerApproach`, `SpannedIntegerError`| uses storyboard ratios; `MDM` box on perfect match     |
| `verification.py`             | `Verification`                                 | replicates `fig-demo` with real Z-S numbers + real MDM predictions |
| `full_video.py`               | `FullStory`                                    | stitches all 12 scenes (97 animations)                  |

## Render commands

```bash
cd manim_exploration
uv run manim -ql --disable_caching scenes/<file>.py <ClassName>
uv run manim -pqh scenes/full_video.py FullStory   # high quality, plays it
```

## Numbers wired in (canonical sources)

### Rounding sequence (from MDM_storyboard.pdf, pages 7–9)

- Quantity ratios shown: red `1`, blue `4.6`, green `12.1`
- In code: `QUANTITY_RATIO = [12.1, 4.6, 1.0]` (fine → mid → coarse)
- Iteration counts (fine, mid, coarse):
  - i=0, scale=1: `[12, 5, 1]`
  - i=1, scale=2: `[24, 9, 2]`
  - i=2, scale=3: `[36, 14, 3]`
- Computed via `_round_match(scale) = np.round(QUANTITY_RATIO * scale)`.

### Spanned integer (storyboard last page)

- `K_- = (1.0, 6.8, 13.4)` — min size end → larger ratio
- `K_+ = (1.0, 4.1, 11.8)` — max size end → smaller ratio
- Spanned integers: `[1, 5, 12]` (fine → mid → coarse)
- **Note**: K_-/K_+ were swapped in an earlier revision; corrected per
  manuscript algorithm definition (smaller x → larger ζ → larger K, so
  K_- > K_+).

### Verification (manuscript `fig-demo`)

- Reported N: copied from manuscript table (Z-S 2025).
- Predicted N: actually computed by running
  `gsd_lib.MinimalPackingGenerator` against the Athabasca GSD scaled
  by SF, with reported void ratio and sample volume. See
  `verification.py:ZS_POINTS` and `ZS_UNSCALED_PREDICTED`. Reproducer
  script (run from repo root):
  ```python
  import numpy as np
  from gsd_lib import GSD, MinimalPackingGenerator
  athabasca_sizes = np.array([0.076, 0.11, 0.15, 0.25, 0.43, 0.85, 2.40])
  athabasca_sizes = np.insert(athabasca_sizes, 0, athabasca_sizes[0]/2)
  athabasca_pp = np.array([0.0, 3.86, 5.14, 15.27, 60.13, 81.35, 93.40, 100])
  retained = np.diff(athabasca_pp, append=athabasca_pp[-1])[:-1]
  retained = np.append(retained, 0.0)
  # then for each (D, SF, H, e_c) in the Z-S table:
  g = GSD(sizes=athabasca_sizes*SF, masses=retained)
  mdm = MinimalPackingGenerator(g, x_n_factor=0.5, tol=1e-2, flex=True).mps
  Npred = sum(mdm.quantities) * (np.pi*(D/2)**2*H) / (mdm.total_volume*(1+e_c))
  ```

## Open threads (next steps)

1. **User flagged "wrong slots" in numbers.** I fixed the K_-/K_+ swap;
   user implied there are *more* slot mismatches I haven't identified.
   Need user to point them out before another fix pass.
2. **`ReducingError` count source.** Currently driven by
   `_round_match(scale)`. I offered to convert to a hand-rolled list of
   `(fine, mid, coarse)` tuples per iteration so the user can edit a
   single integer (e.g. 9 → 8) and have both the label and the pile
   update from one source. User has not yet decided.
3. **Storyboard text in `storyboard.md`** has uncommitted modifications
   (M file at session start) — not my changes; leave alone.

## Coupling notes (asked about by user)

In `rounding.py:_piles_with_counts`, each `counts[i]` value is used both
as the big integer label (`Text(str(n))`) AND as the `count` argument to
`scatter_in_band`. Single source of truth — one edit updates both.

## Render verification

All 12 individual scenes and `FullStory` rendered cleanly at -ql on the
last pass. No cached artifacts relied upon (`--disable_caching` used).
