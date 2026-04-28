# MDM Manim exploration

Animations visualizing the minimal discrete match concept. See `visualization_ideas.md` for the broader brainstorm and `MDM_storyboard.pdf` for the hand-sketched storyboard this implementation follows.

## Layout

- `scenes/sieve_stack.py` — pages 1–2: stacked sieves with particles raining through.
- `scenes/pile_to_gsd.py` — page 3: retained piles morphing into the mass-vs-size plot.
- `scenes/ratios.py` — pages 4–5: `MassRatios` (M_i/M_1) and `VolumeRatios` (ζ_i = M(x_1)/M(x_i)).
- `scenes/_common.py` — shared colors, sieve geometry, particle layout helpers.

## Run

```bash
# Low-quality preview (fast)
uv run manim -pql scenes/sieve_stack.py SieveStack

# High quality
uv run manim -pqh scenes/pile_to_gsd.py PileToGSD
```

Output lands in `media/` (gitignored).
