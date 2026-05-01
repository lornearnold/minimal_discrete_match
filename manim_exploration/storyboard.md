# Storyboard


Order  (target durations at ~190 wpm)
 - intro — ~13 s
   - In soil mechanics, we have this problem: we want to model soil, but there are too many particles to count. And even if we could, there would be far too many particles to simulate.
 - sieve stack — ~7 s
   - So we use sieves to find out how much mass is in different size ranges.
 - continuum reveal (defining "g") — ~13 s
   - In practice, we'd use many more sieve sizes to get a smoother curve, but we're going to stick with three for the rest of the visuals
 - define "s" — ~11 s
   - there are many sets of particles that could be compatible with G, but we're interested in finding the one with the smallest number of particles. We call this the Minimal Discrete Match (MDM) to find the MDM, it's helpful to have some ratios to work with
 - mass ratio — ~6 s
 - volume ratio — ~14 s
 - define quantity ratio — ~10 s
   - multiply mass ratio times volume ratio
   - problem: only one entry is guaranteed to be an integer
 - error — ~9 s (rounding) + ~19 s (spanned integer)



# script  (timing assumes ~190 wpm ≈ 3.17 words/sec)

[intro — 41 words ≈ 13 s]
When faced with a soil mechanics problem, we may need to simulate the soil itself. The problem with this is we can't individually measure all the particles, and even if we could, there would be far too many particles to simulate. 

[sieve stack — 20 words ≈ 7 s]
To help with this, we can use sieves to find the weight of all the grains within a certain diameter. 

[continuum reveal / defining G — 41 words ≈ 13 s]
This curve describes the mass distribution of the sample's grain sizes, which we will call "G." We can use this as a baseline to find a set of particles to simulate - we will try to find a solution that satisfies G. 

[defining S — 33 words ≈ 10 s]
There are many sets of particles (or "S") that are compatible "G," but we are interested in finding the one with the fewest particles. We call this solution the Minimal Discrete Match. (MDM)

[ratios intro — 11 words ≈ 4 s]
To find the MDM, it is helpful to have some ratios.

[mass ratio — 18 words ≈ 6 s]
We can calculate the ratios of mass by dividing each mass by the mass of the biggest grains.

[volume ratio — 45 words ≈ 14 s]
Similarly, we can find volume ratios by comparing the volume of a representative grain from each size range to the volume of the largest grain. Since we get to choose which grain represents each range, these ratios aren't locked in — we can adjust them later.

[quantity ratio — 30 words ≈ 10 s]
By multiplying these ratios, we get quantity ratios - or ratios of how many particles are in each size range. The problem now becomes finding an integer solution to these ratios.

[rounding — 26 words ≈ 9 s]
We can now write an algorithm to find an integer solution by duplicating and rounding the quantity ratio until we fall under our margin of error. 

[spanned integer / outro — 58 words ≈ 19 s]
This approach uses only fixed volume ratios, but we can utilize the ability to change them to find a smaller solution. We can calculate a range of quantity ratios and find an integer number of particles falls between them. Using this new algorithm, we can accurately predict the number of particles needed to build models of real-world soil.

Total narration: 323 words → ~102 s (~1:42) at 190 wpm.

