# Scene Notes

Use this file to capture suggested changes for each Manim scene. Add bullets under the relevant scene.

## pile_to_gsd.py — `PileToGSD`

- LEFT SIDE: 
  - the particles should be spaced to not overlap and only have a few particles of each size.
  - when the sieves disappear and more particles are added, use the whole left half of the

- RIGHT SIDE:
    - the bars representing the 3 sieves should not smooth out
    - more and more bars should be added to better approximate the curve.
    - the bars' colors should transition from green to blue to red 
    - go from 3 to 15 sieves
    
- "size" could be replaced with something else to not confuse with each particle size

## sieve_stack.py — `SieveStack`

-

## continuum_reveal.py — `ContinuumReveal`

- I don't think this scene is working for me. Maybe it should come first or something... I'm not sure. the point was to make it clear why we show these smooth grain size distribution curves even though in the video we only have three sizes, but it doesn't really do that job. I can't quite describe what would be needed to do it better, though.

## mass ratio

## volume ratio

# Script

When faced with a soil mechanics problem, we may need to simulate the soil itself. The problem with this is that simulating every single particle is very difficult, and we can't individually measure all the particles. To help with this, we can use sieves to find the weight of all the grains within a certain diameter, which we convert into a set of ratios, or "G". With enough sieves, you can achieve a smooth curve, but for this video we will only be using three. There are many sets of particles (or "S") that satisfy "G," but we are interested in finding the one with the least particles.
