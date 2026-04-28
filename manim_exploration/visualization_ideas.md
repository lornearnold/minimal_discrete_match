# Visualizing the Minimal Discrete Match (MDM)

Brainstorming Manim animations that make the MDM concept intuitive. The goal: take a viewer from "a GSD is a curve on a chart" to "the MDM is the smallest *integer* set of particles that reproduces that curve" — and show *why* the spanned-integer trick beats fixed-size rounding.

## Core concepts to convey

1. A grain size distribution (GSD) is a mass-by-size description, not a particle list.
2. Mapping a continuous mass curve to a *discrete* set of particles requires integer counts at chosen sizes.
3. Mass scales with size cubed — so a single large particle "spends" the mass of many small ones.
4. The choice of representative size within each sieve interval is a free parameter; exploiting it minimizes total particle count.
5. Match error is a residual between the requested retained mass and what the integer particles deliver.

## Visualization ideas

### 1. Sieve stack → particle pile
Animate a column of stacked sieves with a cloud of particles raining through. Particles settle on the sieve they cannot pass. The retained piles morph into the bars of a bar-chart, which then morph into the canonical cumulative-percent-passing curve. Establishes the physical-to-mathematical translation.

### 2. The "mass budget" metaphor
Each sieve interval has a mass budget (a horizontal bar). Adding a particle of size `x` consumes `f(x) = ρπ/6 · x³` from the budget. Show particles being "spent" into the bar, with the bar shrinking by the cubed amount. The viewer feels viscerally that *one* big particle empties a budget that *thousands* of small particles couldn't.

### 3. Fixed-size vs. spanned-integer, side by side
Two panels. Same target GSD. Left panel runs the FS algorithm: fixed representative sizes, integer rounding leaves residual error, iterate by scaling up — particle count balloons. Right panel runs the SI algorithm: sizes slide continuously within each interval until integer counts "click" into place at zero residual. The click should be audible/visual — a satisfying snap.

### 4. The K-vector number line
Plot the elements of K (relative quantity ratios) as points on a real number line. Show integer ticks. FS algorithm: snap each point to nearest integer (visible jumps = error). SI algorithm: slide each point along its allowable range (a colored segment between K⁻ and K⁺) until it lands *exactly* on an integer. The segments either contain an integer (green) or don't (red, triggering iteration).

### 5. Error as residual mass
For a candidate sample, draw the target GSD curve and overlay the actual cumulative mass delivered by the integer particles as a step function. The gap between them is the error. Animate the gap shrinking as the SI algorithm finds better sizes.

### 6. Volume-ratio cube tower
ζᵢ = (x_max / xᵢ)³. Draw a cube for the largest particle. Stack cubes for the next size — there are ζ of them, often hundreds or thousands. The visual exponential blowup with size ratio explains why broad GSDs cost so much. Tie this directly to fig-uscs_N's range across O(10¹) to O(10¹⁰).

### 7. From MDM to simulation
Start with the MDM (a few dozen to a few thousand particles in a small box). Tile/replicate it to fill a representative-volume cylinder. Counter ticks up from N_MDM to N_sim. Reinforces that MDM is a *unit*, not a sample.

### 8. USCS classification "atlas"
A grid of small multiples — one per USCS group symbol. Each cell shows a representative GSD curve and a swarm of N_MDM particles. The viewer scans across SP, SW, GP, GW, SM, etc. and sees the orders-of-magnitude variation in particle count for visually similar curves.

### 9. Walk the Athabasca scale-factor ladder
Animate SF = 20 → 15 → 10 → 5 → 1 (unscaled). At each step, the GSD curve slides left (smaller particles), the particle swarm densifies, and the counter ticks from O(10³) up to O(10⁸). Concrete payoff for the abstract math.

### 10. The "spanned integer" geometric proof
For a 2-size case, plot K⁻ and K⁺ as endpoints of a segment in 2D quantity-space. Show the integer lattice. Sweep x_n (the largest size) and watch the segment translate/rotate. When the segment crosses a lattice point, freeze: that's the MDM. Generalizes intuition for n-D.

## Suggested first build

Start with **#2 (mass budget)** combined with **#4 (K-vector number line)** — they are the conceptual core and lend themselves naturally to Manim's transform machinery. #3 is the natural second piece because it turns the algorithm into a visible competition.
